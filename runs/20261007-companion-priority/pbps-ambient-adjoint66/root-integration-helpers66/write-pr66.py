from pathlib import Path
import json,subprocess
r=Path('runs/20261007-companion-priority/pbps-ambient-adjoint66');n=json.loads((r/'integration.notes.json').read_bytes());assert n['registry_count']==512 and n['publication_units']==233
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert head!=n['proof_commit']
s=f'''The original finite-dimensional C2 potential, both global Hessian bounds and positive capped step size now produce the actual PBPS defect roots, centered inverse, polar isometry and globally centered first-corrector input geometry. The same laws and conditional projection give canonical R:L2(J)->kerP with Rg=g-Pg and the ambient adjoint identity for every joint g. For every actual mean-zero input, the genuine Test reconstructs f=i0 fP+fperp, proves B*f=GammaP i0 fV and gives ||fV||^2<=||f||^2-||fP||^2. Rank zero and alpha eta=1 remain included.

No root, gap, inverse, onto or functional-calculus certificate becomes a caller premise. Two private definitions hold the complete original propositions literally, with identical public caller conditions; independent review covers both entire modules and their expansions. Reusable real-L2 results and ASTIS domain adapters retain their separate attribution.

Validation: exact science commit {n['proof_commit']} independently VERIFIED; fresh focused checks with standard axioms, independent mathematics, anonymous decoding and primary-first seven-slot source review. Serialized local root/Tests builds pass with {n['root_jobs']}/{n['test_jobs']} jobs and Registry512. All 233 publication items and contributor/semantic/frontier/site/affected graph checks pass. The 296 Python regression results are reused from INT64 after verifying unchanged tools and site scripts. The complete attributed statement, six literal formula steps and actual branch were inspected; initially folded Lean, two isolated copy callbacks and two exact RAW source downloads were checked.

Exact integration commit: {head}. Independent repository/reader admission and this commit's remote CI remain pending. Full Exposition Seal, post-merge purification, merged/live delivery and whole-paper/Goal completion are unclaimed; inherited statement notation, complete-Lean placement and dense graph/spacing debt remain explicit.

Printed B20 defines the corrector; its sharp energy estimate is B23 in Lemma B.3. SAME root/centered-inverse commutation is the next genuine proof ingredient for B23 and B21. Those results, H1/B13/B14, dynamics/invariance/nonexplosion, hypocoercivity/main mixing, implementation errors, expected query costs and actual-input PBPS/SPHMC composition remain open. TV proximity does not transfer unbounded expected costs. Existing four-paper priorities and collaborator frontiers are preserved.

Bounded evidence: runs/20261007-companion-priority/pbps-ambient-adjoint66/integration.notes.json and root.exact-verification66.adoption.json; current checkpoint: docs/companion-papers-handoff.md.
'''
p=r/'integration66/pr315-body66.md';assert not p.exists();p.write_text(s,encoding='utf-8',newline='\n');print('Wrote actual INT66 PR body with remote/repository status explicitly pending.')
