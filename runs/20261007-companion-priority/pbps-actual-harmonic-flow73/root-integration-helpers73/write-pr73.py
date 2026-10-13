from pathlib import Path
import json
r=Path('runs/20261007-companion-priority/pbps-actual-harmonic-flow73');n=json.loads((r/'integration.notes.json').read_bytes())
body=f'''PBPS Proposition 3.1 needs the actual harmonic segment before stochastic bounce-clock construction. This adds the literal source flow with its original six analytic callers, joint continuity/Borel measurability, zero/group/inverse laws, both ODE derivatives, nonnegative conserved weighted-sum energy, and the exact pi endpoint. It also retains the preceding actual corrector change and perturbation results.

The harmonic theorem has independent mathematics, source-blind reconstruction and source review. The first exact commit was blocked only by missing Samplinglib retrieval labels; the independently approved two-string metadata repair is preserved as a separate child, verified at {n['proof_commit']}. No source assumption or Lean body changed in that repair.

Validation: fixed Lean 4.33.0/Mathlib manifest; focused fresh Lean and standard axioms; serialized astis.py check (root {n['root_jobs']}, Tests {n['test_jobs']}), publication/contributor/semantic/frontier and current graph/site gates. Registry522/243 publication items. One complete attributed statement, six formula/BODY steps and the affected branch were rendered; three isolated copy callbacks and three exact RAW Lean downloads checked. Unchanged full Python/browser regressions are reused from packet72 with the runtime qualification recorded in integration73. Immutable RAW whitespace findings remain disclosed; authored complement passes.

Actual bounce/rate/clocks/random PDMP construction, nonexplosion, invariance/reversal, full hypocoercivity, implementation errors, expected-query costs, actual-input composition and complete paper results remain open. No main merge, live publication, full Exposition Seal, purification or whole-Goal completion is claimed.

Evidence: runs/20261007-companion-priority/pbps-actual-harmonic-flow73/integration.notes.json and final-reader-repository-packet73.json.
'''
p=r/'integration73/pr315-body73.md';assert not p.exists();p.write_text(body,encoding='utf8',newline='\n')
print('PASS73 exact PR body file written; reader acceptance still separate.')
