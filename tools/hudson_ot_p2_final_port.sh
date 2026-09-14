#!/usr/bin/env bash
set -euo pipefail

git config user.name "DakeBU integration"
git config user.email "159223240+DakeBU@users.noreply.github.com"
git fetch origin main hudson/ot-geodesic-p2
git reset --hard origin/main

set +e
git cherry-pick b6501fd222c81c974dcad2b38376c692c212fe1f
rc=$?
set -e
if [ "$rc" -ne 0 ]; then
  python3 - <<'PY'
import json, subprocess
from pathlib import Path
conflicts = subprocess.check_output(["git","diff","--name-only","--diff-filter=U"], text=True).splitlines()
allowed = {"research-wiki/semantic-roundtrip/registry.json", "runs/substantive_advances.jsonl"}
unexpected = sorted(set(conflicts) - allowed)
if unexpected:
    raise SystemExit(f"unexpected conflicts: {unexpected}")
reg = "research-wiki/semantic-roundtrip/registry.json"
if reg in conflicts:
    ours = json.loads(subprocess.check_output(["git","show",f":2:{reg}"], text=True))
    theirs = json.loads(subprocess.check_output(["git","show",f":3:{reg}"], text=True))
    ids = {row["id"] for row in ours.get("audits", [])}
    for row in theirs.get("audits", []):
        if row["id"] not in ids:
            ours.setdefault("audits", []).append(row)
            ids.add(row["id"])
    Path(reg).write_text(json.dumps(ours, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
ledger = "runs/substantive_advances.jsonl"
if ledger in conflicts:
    ours = subprocess.check_output(["git","show",f":2:{ledger}"], text=True).splitlines()
    theirs = subprocess.check_output(["git","show",f":3:{ledger}"], text=True).splitlines()
    seen = set(ours)
    Path(ledger).write_text("\n".join(ours + [x for x in theirs if x and x not in seen]) + "\n", encoding="utf-8")
PY
  git add research-wiki/semantic-roundtrip/registry.json runs/substantive_advances.jsonl
  GIT_EDITOR=true git cherry-pick --continue
fi

git cherry-pick 82e8be516217517b2f3e4bc737804442d39633c8

python3 - <<'PY'
from pathlib import Path
p=Path('AutoSamplingTheory/TechnicalLemmas.lean')
s=p.read_text()
new='import AutoSamplingTheory.TechnicalLemmas.Measure.DisplacementInterpolationP2ConstantSpeed\n'
anchor='import AutoSamplingTheory.TechnicalLemmas.Measure\n'
if new not in s:
    if anchor not in s: raise SystemExit('TechnicalLemmas.lean import anchor missing')
    s=s.replace(anchor, anchor+new, 1); p.write_text(s)
p=Path('Tests.lean'); s=p.read_text(); new='import Tests.DisplacementInterpolationConstantSpeed\n'; anchor='import Tests.DisplacementInterpolation\n'
if new not in s:
    if anchor not in s: raise SystemExit('Tests.lean import anchor missing')
    s=s.replace(anchor, anchor+new, 1); p.write_text(s)
PY

git add AutoSamplingTheory/TechnicalLemmas.lean Tests.lean
git commit -m "integrate arbitrary-P2 displacement speed into public graph"

python3 tools/astis_frontier_cells.py check
python3 tools/astis_semantic_roundtrip.py check
python3 tools/astis_publication.py check --base origin/main
LEAN_NUM_THREADS=2 lake build Tests.DisplacementInterpolationConstantSpeed
LEAN_NUM_THREADS=2 python3 tools/astis.py check
python3 website/scripts/build_site.py
python3 tools/astis_publication.py graph-check --cell ASTIS-SHARED-displacement-interpolation-p2
python3 website/scripts/check_site.py
git diff --check

git push origin HEAD:refs/heads/codex/hudson-ot-p2-final
