#!/usr/bin/env python3
"""Render a run folder's JSON files into one self-contained dashboard.html.

Every section is optional: a missing file shows a pending state, so the page
can be re-rendered after each stage and fills in progressively.

Usage:
  python render_dashboard.py RUN_DIR [--out RUN_DIR/dashboard.html]
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from html import escape
from pathlib import Path

SECTIONS = [
    ("brief", "Brief"),
    ("market", "Target market"),
    ("sources", "Sources"),
    ("ideas", "Top 10 ideas"),
    ("pick", "The pick"),
]


def load(run: Path, name: str):
    path = run / name
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"warning: {path} is not valid JSON ({exc}); treating as pending", file=sys.stderr)
        return None


def e(value) -> str:
    return escape("" if value is None else str(value))


def link(url, text=None) -> str:
    if not url:
        return e(text or "")
    safe = str(url)
    if not safe.startswith(("http://", "https://")):
        return e(text or url)
    return f'<a href="{escape(safe, quote=True)}" target="_blank" rel="noopener noreferrer">{e(text or url)}</a>'


def pending(label: str) -> str:
    return f'<p class="pending" role="status"><span class="dot" aria-hidden="true"></span>{e(label)} will appear here once this stage is complete.</p>'


def section(sid: str, num: int, title: str, body: str, done: bool) -> str:
    state = "done" if done else "pending"
    badge = "Complete" if done else "Pending"
    return (
        f'<section id="{sid}" class="card section is-{state}" aria-labelledby="{sid}-h">'
        f'<header class="section-head"><h2 id="{sid}-h"><span class="num">{num}</span>{e(title)}</h2>'
        f'<span class="badge {state}">{badge}</span></header>{body}</section>'
    )


def render_brief(brief) -> str:
    if not brief:
        return pending("The brief")
    rows = [
        ("Space", brief.get("space")),
        ("Playbook", brief.get("playbook")),
        ("Industry", brief.get("industry")),
        ("Use case", brief.get("use_case")),
        ("Geography", brief.get("geography")),
        ("Buyer", brief.get("buyer")),
        ("User", brief.get("user")),
        ("Business model", brief.get("business_model")),
        ("Goal", brief.get("goal")),
    ]
    dl = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in rows if v)
    constraints = brief.get("constraints") or []
    cons = (
        "<h3>Constraints</h3><ul>" + "".join(f"<li>{e(c)}</li>" for c in constraints) + "</ul>"
        if constraints else ""
    )
    return f'<p class="lead">{e(brief.get("summary"))}</p><dl class="facts">{dl}</dl>{cons}'


def render_market(market, ev_index) -> str:
    if not market:
        return pending("The target market")
    segs = market.get("segments") or []
    def seg(s):
        size = f' <span class="muted">· {e(s.get("size_hint"))}</span>' if s.get("size_hint") else ""
        return (f'<li><strong>{e(s.get("name"))}</strong>{size}<br><span class="muted">{e(s.get("description"))}</span>'
                f'{cite_inline(s.get("evidence"), ev_index)}</li>')

    items = "".join(seg(s) for s in segs)
    facts = [
        ("Primary buyer", market.get("buyer")),
        ("Primary user", market.get("user")),
        ("Where", market.get("geography")),
        ("Stage", market.get("stage")),
    ]
    dl = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts if v)
    seg_html = f"<h3>Segments</h3><ul class=\"segments\">{items}</ul>" if items else ""
    return f'<p class="lead">{e(market.get("summary"))}</p><dl class="facts">{dl}</dl>{seg_html}'


def cite_inline(ids, ev_index) -> str:
    if not ids:
        return ""
    parts = []
    for i in ids:
        ev = ev_index.get(i)
        if ev and ev.get("url"):
            parts.append(link(ev["url"], i))
        else:
            parts.append(e(i))
    return f' <span class="cites">[{", ".join(parts)}]</span>'


def render_sources(plan, check) -> str:
    if not plan:
        return pending("The source plan")
    out = []
    if check:
        gaps = check.get("unresolved_gaps") or []
        if gaps:
            out.append(
                '<div class="warn" role="note"><strong>Source checker: unresolved gaps after '
                f'{e(check.get("rounds", "?"))} round(s)</strong><ul>'
                + "".join(f"<li>{e(g)}</li>" for g in gaps) + "</ul></div>"
            )
        elif check.get("verdict") == "PASS":
            out.append(f'<p class="ok">Independent source check passed in {e(check.get("rounds", 1))} round(s).</p>')
    else:
        out.append('<p class="pending small"><span class="dot" aria-hidden="true"></span>Independent source check pending.</p>')

    sources = plan.get("sources") or []
    questions = plan.get("questions") or []
    out.append(f'<p class="muted">{len(sources)} sources across {len(questions)} research questions.</p>')

    groups: dict[str, list] = {}
    for s in sources:
        groups.setdefault(s.get("type") or "Other", []).append(s)
    group_rows = "".join(
        f'<div><dt>{e(t)}</dt><dd>'
        + ", ".join(f'{link(s.get("url"), s.get("name"))} <span class="cred c{e(s.get("credibility"))}">{e(s.get("credibility"))}/5</span>' for s in items)
        + "</dd></div>"
        for t, items in groups.items()
    )
    out.append(f'<dl class="src-groups">{group_rows}</dl>')

    rows = "".join(
        "<tr>"
        f'<td>{link(s.get("url"), s.get("name"))}<div class="muted small">{e(s.get("why"))}</div></td>'
        f'<td>{e(s.get("type"))}</td>'
        f'<td><span class="cred c{e(s.get("credibility"))}" title="Credibility {e(s.get("credibility"))} of 5">{e(s.get("credibility"))}/5</span></td>'
        f'<td>{e(s.get("access"))}</td>'
        f'<td class="small">{e(", ".join(s.get("questions") or []))}</td>'
        "</tr>"
        for s in sources
    )
    out.append(
        '<details class="more"><summary>Full source plan: why chosen, credibility, access</summary>'
        '<div class="table-wrap"><table><caption class="sr-only">Source plan</caption>'
        '<thead><tr><th scope="col">Source</th><th scope="col">Type</th><th scope="col">Credibility</th>'
        '<th scope="col">Access</th><th scope="col">Answers</th></tr></thead>'
        f"<tbody>{rows}</tbody></table></div></details>"
    )
    if questions:
        qs = "".join(f'<li><strong>{e(q.get("id"))}</strong> {e(q.get("question"))}</li>' for q in questions)
        out.append(f'<details class="more"><summary>Research questions ({len(questions)})</summary><ol class="plain">{qs}</ol></details>')
    return "".join(out)


def render_ideas(top10, redteam, ev_index) -> str:
    if not top10:
        return pending("The top 10")
    verdicts = {v.get("idea_id"): v for v in (redteam or {}).get("verdicts", [])}
    rubric = top10.get("rubric") or []
    out = []
    if rubric:
        chips = "".join(f'<li>{e(r.get("criterion"))} <span class="muted">{e(r.get("weight"))}%</span></li>' for r in rubric)
        out.append(f'<details class="more"><summary>Scoring rubric ({e(top10.get("playbook", "playbook"))})</summary><ul class="chips">{chips}</ul></details>')
    if redteam is None:
        out.append('<p class="pending small"><span class="dot" aria-hidden="true"></span>Red-team kill gate pending.</p>')
    else:
        note = "Founder-fit check: " + ("run against your founder profile." if redteam.get("founder_fit_checked") else "skipped (no founder profile provided).")
        out.append(f'<p class="muted small">{e(note)}</p>')

    cards = []
    for idea in top10.get("ideas", []):
        iid = idea.get("id")
        v = verdicts.get(iid)
        badge = ""
        if v:
            outcome = v.get("outcome", "")
            badge = f'<span class="tag {"survive" if outcome == "survive" else "killed"}">{"Survived red team" if outcome == "survive" else "Killed"}</span>'
        score = idea.get("score")
        try:
            pct = max(0, min(100, float(score)))
        except (TypeError, ValueError):
            pct = 0
        scores = idea.get("scores") or {}
        breakdown = "".join(f"<li><span>{e(k)}</span><span>{e(val)}/5</span></li>" for k, val in scores.items())
        risks = "".join(f"<li>{e(r)}</li>" for r in idea.get("risks") or [])
        cites = []
        for eid in idea.get("evidence") or []:
            ev = ev_index.get(eid)
            if not ev:
                cites.append(f'<li>{e(eid)} <span class="muted">(not in evidence log)</span></li>')
                continue
            cites.append(
                f'<li><strong>{e(eid)}</strong> {e(ev.get("claim"))}'
                f'<blockquote>{e(ev.get("quote"))}</blockquote>'
                f'<span class="muted small">{link(ev.get("url"), ev.get("source_name") or ev.get("url"))} · accessed {e(ev.get("accessed"))} · confidence {e(ev.get("confidence"))}</span></li>'
            )
        rt = ""
        if v:
            attacks = "".join(f'<li><strong>{e(a.get("test"))}:</strong> {e(a.get("finding"))}</li>' for a in v.get("attacks") or [])
            rt = f'<h4>Red team</h4><p>{e(v.get("reason"))}</p>' + (f"<ul>{attacks}</ul>" if attacks else "")
        cards.append(
            f'<li class="idea {"is-killed" if v and v.get("outcome") != "survive" else ""}">'
            '<details><summary>'
            f'<span class="rank">#{e(idea.get("rank"))}</span>'
            f'<span class="idea-main"><span class="idea-name">{e(idea.get("name"))}</span>'
            f'<span class="idea-line">{e(idea.get("one_liner"))}</span></span>'
            f'<span class="idea-side"><span class="score" aria-label="Score {e(score)} of 100"><span class="bar"><span style="width:{pct:.0f}%"></span></span>{e(score)}</span>{badge}</span>'
            '</summary><div class="idea-body">'
            f'<h4>Why it ranks here</h4><p>{e(idea.get("why"))}</p>'
            + (f'<h4>Score breakdown</h4><ul class="breakdown">{breakdown}</ul>' if breakdown else "")
            + (f"<h4>Risks</h4><ul>{risks}</ul>" if risks else "")
            + rt
            + (f'<h4>Sources cited</h4><ul class="cite-list">{"".join(cites)}</ul>' if cites else "")
            + "</div></details></li>"
        )
    out.append(f'<ol class="ideas">{"".join(cards)}</ol>')
    return "".join(out)


def render_pick(pick, top10, ev_index) -> str:
    if not pick:
        return pending("The entrepreneur's pick")
    test = pick.get("test") or {}
    test_rows = [("How", test.get("method")), ("Success signal", test.get("success_signal")),
                 ("Cost", test.get("cost")), ("Time", test.get("duration"))]
    tdl = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in test_rows if v)
    others = pick.get("why_not_others") or []
    others_html = (
        '<details class="more"><summary>Why not the other survivors</summary><ul>'
        + "".join(f'<li><strong>{e(o.get("name"))}:</strong> {e(o.get("reason"))}</li>' for o in others)
        + "</ul></details>" if others else ""
    )
    return (
        f'<div class="pick"><p class="kicker">Top pick</p><h3 class="pick-name">{e(pick.get("name"))}</h3>'
        f'<p class="lead">{e(pick.get("one_liner"))}</p></div>'
        f'<h3>Why this one</h3><p>{e(pick.get("why"))}{cite_inline(pick.get("evidence"), ev_index)}</p>'
        f'<div class="risk"><h3>Riskiest assumption to test first</h3><p>{e(pick.get("riskiest_assumption"))}</p>'
        f'<dl class="facts">{tdl}</dl></div>{others_html}'
    )


CSS = """
:root{--bg:#f7f7f5;--card:#fff;--ink:#1c1d1f;--muted:#5b5f66;--line:#e4e4e0;--accent:#1f5fbf;--accent-soft:#e8f0fc;
--ok:#1d6b3a;--ok-soft:#e6f4ea;--warn:#7a4b00;--warn-soft:#fff4dc;--bad:#9b1c1c;--bad-soft:#fde8e8;--radius:12px}
@media (prefers-color-scheme:dark){:root{--bg:#121315;--card:#1b1c1f;--ink:#ececec;--muted:#a3a7ae;--line:#2c2e33;
--accent:#8ab4f8;--accent-soft:#1e2a3d;--ok:#81c995;--ok-soft:#18291e;--warn:#f6c26b;--warn-soft:#2e2614;--bad:#f28b82;--bad-soft:#2f1b1b}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,"Noto Sans",sans-serif}
a{color:var(--accent);text-underline-offset:2px}a:focus-visible,summary:focus-visible{outline:3px solid var(--accent);outline-offset:2px;border-radius:4px}
.wrap{max-width:920px;margin:0 auto;padding:2rem 1.25rem 4rem}
.skip{position:absolute;left:-999px}.skip:focus{left:1rem;top:1rem;background:var(--card);padding:.5rem 1rem;z-index:2}
.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.example{background:var(--warn-soft);color:var(--warn);border:1px solid currentColor;border-radius:var(--radius);padding:.6rem 1rem;margin-bottom:1.25rem;font-weight:600}
.top h1{font-size:clamp(1.5rem,3.5vw,2rem);line-height:1.25;margin:0 0 .25rem}
.top p{margin:0;color:var(--muted)}
.steps{display:flex;flex-wrap:wrap;gap:.5rem;list-style:none;padding:0;margin:1.25rem 0 2rem}
.steps a{display:inline-flex;align-items:center;gap:.4rem;padding:.3rem .75rem;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--muted);text-decoration:none;font-size:.875rem}
.steps a.done{color:var(--ok);border-color:var(--ok);background:var(--ok-soft)}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:1.5rem;margin-bottom:1.5rem}
.section.is-pending{border-style:dashed}.section.is-pending h2{color:var(--muted)}
.section-head{display:flex;justify-content:space-between;align-items:center;gap:1rem;margin-bottom:.75rem}
h2{font-size:1.25rem;margin:0;display:flex;align-items:center;gap:.6rem}
h3{font-size:1rem;margin:1.25rem 0 .4rem}h4{font-size:.9rem;margin:1rem 0 .3rem;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
.num{display:inline-grid;place-items:center;width:1.75rem;height:1.75rem;border-radius:50%;background:var(--accent-soft);color:var(--accent);font-size:.875rem}
.badge{font-size:.75rem;padding:.15rem .6rem;border-radius:999px;font-weight:600}
.badge.done{background:var(--ok-soft);color:var(--ok)}.badge.pending{background:var(--bg);color:var(--muted)}
.pending{color:var(--muted);display:flex;align-items:center;gap:.5rem;margin:.25rem 0}
.dot{width:.55rem;height:.55rem;border-radius:50%;background:var(--muted);opacity:.5;animation:pulse 1.6s ease-in-out infinite}
@keyframes pulse{50%{opacity:.15}}@media (prefers-reduced-motion:reduce){.dot{animation:none}}
.lead{font-size:1.05rem;margin:.25rem 0 1rem}.muted{color:var(--muted)}.small{font-size:.875rem}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:.75rem 1.5rem;margin:0}
.facts dt{font-size:.75rem;text-transform:uppercase;letter-spacing:.05em;color:var(--muted)}.facts dd{margin:0}
ul,ol{padding-left:1.25rem}li{margin:.25rem 0}.plain{padding-left:1.25rem}
.segments li{margin-bottom:.6rem}.cites{font-size:.8rem;color:var(--muted)}
.warn{background:var(--warn-soft);color:var(--warn);border-left:4px solid currentColor;border-radius:8px;padding:.75rem 1rem;margin-bottom:1rem}
.warn ul{margin:.4rem 0 0}.ok{color:var(--ok);margin:.25rem 0 .75rem}
.table-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:8px;margin-top:.75rem}
.src-groups{margin:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:.75rem 1.5rem}.src-groups dt{font-size:.75rem;text-transform:uppercase;letter-spacing:.05em;color:var(--muted)}
.src-groups dd{margin:0}.src-groups .cred{font-size:.75rem}
table{border-collapse:collapse;width:100%;font-size:.9rem}th,td{text-align:left;padding:.6rem .75rem;border-bottom:1px solid var(--line);vertical-align:top}
th{font-size:.75rem;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);background:var(--bg)}tr:last-child td{border-bottom:0}
.cred{font-weight:600;white-space:nowrap}.c5,.c4{color:var(--ok)}.c3{color:var(--warn)}.c2,.c1{color:var(--bad)}
details.more{margin-top:1rem}details.more>summary{cursor:pointer;color:var(--accent);font-weight:600}
.chips{display:flex;flex-wrap:wrap;gap:.4rem;list-style:none;padding:0}.chips li{border:1px solid var(--line);border-radius:999px;padding:.15rem .7rem;font-size:.85rem}
.ideas{list-style:none;padding:0;margin:1rem 0 0;display:grid;gap:.6rem}
.idea details{border:1px solid var(--line);border-radius:10px}.idea details[open]{border-color:var(--accent)}
.idea summary{list-style:none;cursor:pointer;display:grid;grid-template-columns:auto 1fr auto;gap:.9rem;align-items:center;padding:.85rem 1rem}
.idea summary::-webkit-details-marker{display:none}
.rank{font-weight:700;color:var(--muted);min-width:2rem}
.idea-main{display:flex;flex-direction:column;min-width:0}.idea-name{font-weight:650}.idea-line{color:var(--muted);font-size:.9rem}
.idea-side{display:flex;flex-direction:column;align-items:flex-end;gap:.3rem}
.score{display:flex;align-items:center;gap:.5rem;font-weight:700;font-variant-numeric:tabular-nums}
.bar{width:70px;height:6px;border-radius:3px;background:var(--line);overflow:hidden}.bar span{display:block;height:100%;background:var(--accent)}
.tag{font-size:.7rem;font-weight:600;padding:.1rem .5rem;border-radius:999px;white-space:nowrap}
.tag.survive{background:var(--ok-soft);color:var(--ok)}.tag.killed{background:var(--bad-soft);color:var(--bad)}
.is-killed .idea-name{text-decoration:line-through;text-decoration-color:var(--muted)}
.idea-body{padding:0 1rem 1rem 3.9rem;border-top:1px solid var(--line)}
.breakdown{list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:.2rem 1.5rem}
.breakdown li{display:flex;justify-content:space-between;border-bottom:1px dotted var(--line)}
.cite-list{padding-left:1rem}.cite-list li{margin-bottom:.75rem}
blockquote{margin:.3rem 0;padding-left:.75rem;border-left:3px solid var(--line);color:var(--muted);font-style:italic}
.pick{background:var(--accent-soft);border-radius:10px;padding:1.25rem}.pick .lead{margin:0}
.kicker{margin:0;font-size:.75rem;text-transform:uppercase;letter-spacing:.08em;color:var(--accent);font-weight:700}
.pick-name{font-size:1.4rem;margin:.2rem 0 .3rem}
.risk{border:1px solid var(--warn);border-radius:10px;padding:1rem 1.25rem;margin-top:1.25rem}.risk h3{margin-top:0;color:var(--warn)}
footer{color:var(--muted);font-size:.8rem;text-align:center;margin-top:2rem}
@media (max-width:600px){.card{padding:1.1rem}.idea summary{grid-template-columns:auto 1fr}.idea-side{grid-column:2;align-items:flex-start;flex-direction:row}
.idea-body{padding-left:1rem}}
@media print{.steps,.skip{display:none}.card{break-inside:avoid}}
"""


def render(run: Path) -> str:
    brief = load(run, "brief.json")
    market = load(run, "market.json")
    plan = load(run, "source_plan.json")
    check = load(run, "source_check.json")
    evidence = load(run, "evidence.json")
    top10 = load(run, "top10.json")
    redteam = load(run, "redteam.json")
    pick = load(run, "pick.json")

    ev_index = {}
    src_names = {s.get("id"): s.get("name") for s in (plan or {}).get("sources", [])}
    for item in (evidence or {}).get("items", []):
        item = dict(item)
        item.setdefault("source_name", src_names.get(item.get("source_id")))
        ev_index[item.get("id")] = item

    done = {"brief": bool(brief), "market": bool(market), "sources": bool(plan),
            "ideas": bool(top10), "pick": bool(pick)}
    title = (brief or {}).get("title") or run.name
    example = bool((brief or {}).get("example"))

    steps = "".join(
        f'<li><a class="{"done" if done[sid] else ""}" href="#{sid}">{"✓ " if done[sid] else ""}{e(label)}</a></li>'
        for sid, label in SECTIONS
    )
    bodies = {
        "brief": render_brief(brief),
        "market": render_market(market, ev_index),
        "sources": render_sources(plan, check),
        "ideas": render_ideas(top10, redteam, ev_index),
        "pick": render_pick(pick, top10, ev_index),
    }
    sections = "".join(section(sid, i + 1, label, bodies[sid], done[sid]) for i, (sid, label) in enumerate(SECTIONS))
    banner = (
        '<p class="example" role="note">Example dashboard with illustrative placeholder data. '
        'Figures, quotes and scores are not real research.</p>' if example else ""
    )
    stamp = datetime.now().strftime("%d %b %Y, %H:%M")
    n_ev = len(ev_index)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>{e(title)} · Idea pipeline</title>
<style>{CSS}</style></head>
<body><a class="skip" href="#main">Skip to content</a>
<div class="wrap">
{banner}
<header class="top"><p>Idea pipeline</p><h1>{e(title)}</h1>
<p>{sum(done.values())} of {len(SECTIONS)} stages complete · {n_ev} evidence items · updated {e(stamp)}</p></header>
<nav aria-label="Pipeline stages"><ol class="steps">{steps}</ol></nav>
<main id="main">{sections}</main>
<footer>Generated by the idea-pipeline plugin. Every claim links to its source in the evidence log.</footer>
</div></body></html>
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run_dir", type=Path)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    if not args.run_dir.is_dir():
        print(f"error: {args.run_dir} is not a folder", file=sys.stderr)
        return 1
    out = args.out or args.run_dir / "dashboard.html"
    out.write_text(render(args.run_dir), encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
