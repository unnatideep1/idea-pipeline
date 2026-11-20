#!/usr/bin/env python3
"""Idea registry: an index of past runs so new runs can reuse prior research.

  registry.py add    RUN_DIR [--registry DATA/registry.json]
  registry.py search QUERY   [--registry DATA/registry.json] [--playbook NAME] [--evidence]

`add` upserts one run (brief, pick, top 10, evidence and source-yield summary).
`search` ranks past runs by keyword overlap with QUERY; with --evidence it also
lists matching evidence items (claim, URL, date accessed) from those runs so the
researcher can re-verify and reuse them instead of starting from scratch.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

STOP = set("a an and or the of for in on to with by from at as is are be ai app apps india indian".split())


def words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if len(w) > 2 and w not in STOP}


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def cmd_add(args) -> int:
    run = args.run_dir.resolve()
    brief = load_json(run / "brief.json", None)
    if not brief:
        print(f"error: {run}/brief.json missing", file=sys.stderr)
        return 1
    top10 = load_json(run / "top10.json", {})
    pick = load_json(run / "pick.json", {})
    evidence = load_json(run / "evidence.json", {}).get("items", [])
    yield_ = load_json(run / "source_yield.json", {})

    text = " ".join(str(brief.get(k, "")) for k in ("title", "industry", "use_case", "buyer", "user", "geography", "business_model"))
    entry = {
        "slug": run.name,
        "path": str(run),
        "date": brief.get("approved") or date.today().isoformat(),
        "title": brief.get("title"),
        "space": brief.get("space"),
        "playbook": brief.get("playbook"),
        "industry": brief.get("industry"),
        "geography": brief.get("geography"),
        "keywords": sorted(words(text)),
        "top10": [i.get("name") for i in top10.get("ideas", [])],
        "pick": pick.get("name"),
        "riskiest_assumption": pick.get("riskiest_assumption"),
        "evidence_count": len(evidence),
        "productive_sources": yield_.get("productive", []),
        "example": bool(brief.get("example")),
    }
    reg = load_json(args.registry, {"runs": []})
    reg["runs"] = [r for r in reg["runs"] if r.get("slug") != entry["slug"]] + [entry]
    args.registry.parent.mkdir(parents=True, exist_ok=True)
    args.registry.write_text(json.dumps(reg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"registered {entry['slug']} ({len(reg['runs'])} runs in {args.registry})")
    return 0


def cmd_search(args) -> int:
    reg = load_json(args.registry, {"runs": []})
    q = words(args.query)
    hits = []
    for r in reg["runs"]:
        if args.playbook and r.get("playbook") != args.playbook:
            continue
        overlap = q & set(r.get("keywords", []))
        score = len(overlap) + (2 if args.playbook else 0)
        if overlap:
            hits.append((score, sorted(overlap), r))
    hits.sort(key=lambda h: -h[0])
    if not hits:
        print("no related past runs")
        return 0
    for score, overlap, r in hits:
        print(f"- {r['slug']} ({r.get('date')}) · {r.get('title')} · playbook {r.get('playbook')} · match: {', '.join(overlap)}")
        print(f"  pick: {r.get('pick')} · evidence items: {r.get('evidence_count')} · path: {r.get('path')}")
        if args.evidence:
            items = load_json(Path(r["path"]) / "evidence.json", {}).get("items", [])
            for it in items:
                if q & words(it.get("claim", "")):
                    print(f"    {it.get('id')}: {it.get('claim')} <{it.get('url')}> accessed {it.get('accessed')} [{it.get('confidence')}]")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("run_dir", type=Path)
    a.add_argument("--registry", type=Path, default=Path("idea-pipeline-data/registry.json"))
    s = sub.add_parser("search")
    s.add_argument("query")
    s.add_argument("--registry", type=Path, default=Path("idea-pipeline-data/registry.json"))
    s.add_argument("--playbook")
    s.add_argument("--evidence", action="store_true")
    args = ap.parse_args()
    return cmd_add(args) if args.cmd == "add" else cmd_search(args)


if __name__ == "__main__":
    sys.exit(main())
