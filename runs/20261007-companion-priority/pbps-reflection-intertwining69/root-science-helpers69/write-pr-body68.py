from pathlib import Path
import json,subprocess
r=Path('runs/20261007-companion-priority/pbps-sharp-energy68');load=lambda p:json.loads(Path(p).read_bytes())
assert load(r/'root.repository68.adoption.json')['accepted_scoped_aggregate']
proof=load(r/'root.exact-verification68.adoption.json');assert proof['native_verified']
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert head!=proof['verified_commit']
n=load(r/'integration.notes.json');assert n['registry_count']==516
text=f'''PBPS Appendix B.3 needs a sharp corrector estimate on the same actual probability laws and centered Hilbert space. Starting from the original finite-dimensional C2 potential, both global Hessian bounds and positive capped step size, this change proves the exact pair bound |C(u,v)| <= (norm(u)^2+norm(v)^2)/(2 gamma), and the actual globally centered-f bound |C(fP,fV)| <= norm(f)^2/(2 gamma). A genuine original-input Test obtains half/three-halves modified-energy equivalence and the exact perturbation bounds for every 0<omegaWeight<=gamma. The same root, inverse, polar and conditional decomposition are retained, including rank zero and alpha eta=1.

The reusable Hilbert estimate derives the sharp c/2 bound from selfadjoint K,D, I+K^2=D^2 and norm(D)<=c, without finite dimension, nontriviality, positivity or commutation assumptions. The actual PBPS consumer supplies these facts internally. Only one consuming paper route is currently evidenced; the Test is its transitive consumer. Stable cell identity and the canonical TechnicalLemmas declaration are preserved. A separately reviewed S,T notation overlay improves the mathematical explanation and refreshes the source packet without changing Lean or proof spans.

Validation: exact corrected science commit {proof['verified_commit']} is independently VERIFIED by a non-author. Focused compilation, standard axioms, separate mathematical review, anonymous decoding and primary-first source review are accepted. The earlier metadata gate failure is retained; the corrected commit passes all required checks. Serialized root/Tests builds pass at {n['root_jobs']}/{n['test_jobs']} jobs, Registry516, publication237, and contributor/semantic/frontier/site/affected graph gates. Two full attributed statements, eleven literal formula/BODY steps and the actual branch were inspected; initially folded Lean, four isolated copy callbacks and four exact RAW source downloads were checked. The 296 Python regression results are reused from INT64 after verifying unchanged tools and site scripts.

Exact integration commit: {head}. Independent scoped repository/reader admission and current final-cell graph freshness are accepted. INT66's historical graph-freshness debt remains separate. This integration commit's remote CI is pending; main/live delivery, full Exposition Seal, post-merge purification and whole-paper/Goal completion remain open. Inherited notation and dense graph layout remain explicit reader debt.

The next sealed target is actual full-micro reflection intertwining, V0* D=-A0 V0*, with unchanged original caller inputs and D=R U inclusion. It has not yet been proved. B21 rotation, weak H1/B2, B4 dynamics, invariance/nonexplosion, main mixing, implementation errors/caps, expected query costs and actual-input PBPS/SPHMC composition remain open. TV proximity does not transfer unbounded expected cost. Existing four-paper priorities and collaborator frontiers are preserved.

Bounded evidence: runs/20261007-companion-priority/pbps-sharp-energy68/integration.notes.json, root.exact-verification68.adoption.json and root.repository68.adoption.json. Current checkpoint: docs/companion-papers-handoff.md.
'''
p=r/'integration68/pr315-body68.md';assert not p.exists();p.write_text(text,encoding='utf-8',newline='\n')
print('Wrote exact INT68 PR body with source-faithful sharp energy scope and remote CI pending.')
