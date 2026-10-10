from pathlib import Path
import hashlib,json,subprocess
r=Path('runs/20261007-companion-priority/pbps-first-corrector-energy-preproof67/root-library-retrieval67');r.mkdir(parents=True,exist_ok=False)
names=[
'AutoSamplingTheory/TechnicalLemmas/Measure/L2RealComplexOperator.lean',
'AutoSamplingTheory/TechnicalLemmas/Measure/L2RealSquareRootUnique.lean',
'AutoSamplingTheory/TechnicalLemmas/Measure/L2RealSquareOrder.lean',
'AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicDefectRoot.lean',
'AutoSamplingTheory/ExampleCases/ProximalBPS/CenteredRootOrderInverse.lean',
'.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Commute.lean',
'.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/ContinuousFunctionalCalculus/Rpow/Basic.lean',
'research-wiki/sampling-sde-library/cards/AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareRootUnique.md',
'research-wiki/sampling-sde-library/cards/AutoSamplingTheory.TechnicalLemmas.Measure.L2RealComplexOperator.md',
'research-wiki/technical-lemmas/README.md']
sha=lambda b:hashlib.sha256(b).hexdigest();rows=[]
for i,name in enumerate(names):
 p=Path(name);b=p.read_bytes();q=r/f'{i:02d}.exactraw.snapshot';q.write_bytes(b);rows.append(dict(path=name,raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')),exact_raw_snapshot=q.as_posix()))
x=dict(status='RETRIEVAL_ONLY_NOT_A_STATEMENT_SEAL_OR_PROOF',checked_parent=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),inputs=rows,existing_ASTIS=['L2RealComplexOperator.exists_positive_complex_lift requires a positive real operator and provides complete complex action/real embedding','L2RealSquareRootUnique.positive_square_roots_unique descends CFC uniqueness','MacroscopicDefectRoot provides positive SAME GammaP and complete macroscopic square relation','CenteredRootOrderInverse provides SAME complete HP0 Gamma0 and both inverse cancellations'],Mathlib=['Commute.cfcₙ_nnreal in ContinuousFunctionalCalculus/Commute.lean','CFC.sqrt is cfcₙ NNReal.sqrt; CFC.sqrt_unique/ sqrt_mul_self in Rpow/Basic.lean'],candidate_route_not_accepted=['A positive G and a positive D commuting with G squared can be lifted using existing two complex lifts; CFC then returns G-D commutation and embedding descends it.','For actual selfadjoint contraction A, shift D=I+A is internally positive, so a positive-D helper need not add a paper premise.','Transport through SAME e to actual macro space; construct centered restriction from Aq=q and symmetry; derive centered-inverse commutation from both cancellation identities.'],failure_policy='No Lean67 implementation or new public assumptions here. Seal exact source-derived statements and review source graph before proof search; diagnose genuine real/complex API mismatch rather than repeating tactics.',source_numbering='Independent primary67 finding: B20 defines C; sharp corrector energy bound is B23 in LemmaB.3. Actual commutation has genuine B23 and B21 consumers; not yet proved.',mathematical_credit=False)
(r/'retrieval.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Recorded bounded local/pinned Mathlib retrieval67; no Lean proof, SAU claim or canonical write.')
