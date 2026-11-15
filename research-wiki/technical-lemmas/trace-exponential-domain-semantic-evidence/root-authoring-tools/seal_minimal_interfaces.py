from pathlib import Path
import json,hashlib,datetime,subprocess
r=Path.cwd();w=r/'.astis/huanjian-gc-trace-mgf-domain-20261115'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(name,x):
    p=w/name;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return {'file':str(p.relative_to(r)),'sha256':sha(p)}
p=w/'P.candidate.v2.txt';t=w/'T.candidate.v2.txt'
assert sha(p)=='b39869331ad510104d34bcf5c6d2833333b51e028d54ad2ad34f4aaf78033e97'
assert sha(t)=='9013c0f1a28e9f9a0b2175208ea91abaded7fa3a760172f7b8ead404aebbefe1'
receipt=r/'.astis/huanjian-resume-20261103/20261115T062240179009Z-gc-trace-mgf-domain-minimal-P-pointwise-T-proposition-formation-only.receipt.json'
v=json.loads(receipt.read_text());assert v['exit_code']==0
assert sha(Path(v['log']))==v['log_sha256']
assert sha(r/'lean-toolchain')=='302cd63c54178885b89e669f33b38f12f4dd7ae7e5cac537b3203e3768d8fb2b'
assert sha(r/'lake-manifest.json')=='b83ca83b9cf7caa85fa8b023c2ff9a3fb7a7cce7e1c332e810c348535ec49c37'
P='AutoSamplingTheory.TechnicalLemmas.Analysis.MatrixTraceExponentialBounds.trace_exp_pos_and_le_card_mul_exp_abs_mul_norm'
T='AutoSamplingTheory.Tests.GaussianComplexityTraceMgfDomain.actual_source_four_trace_mgfs_integrable_positive_and_bounded'
binders=[]
def b(target,name,cls,meaning,expansion):binders.append({'target':target,'binder':name,'classification':cls,'meaning':meaning,'recursive_expansion':expansion,'EXCESS':False})
for name,meaning in [('universe u','universe of the finite matrix index'),('ι','finite real matrix index'),('[Fintype ι]','finite index enumeration'),('[DecidableEq ι]','matrix indexing equality'),('[Nonempty ι]','positive matrix dimension; needed for strict trace positivity')]:
    b('P',name,'TYPING',meaning,'standard carrier/typeclass only; no project-owned Prop bundle')
b('P','A','SOURCE','arbitrary real square matrix in the exact canonical-library problem','Matrix ι ι ℝ = ι → ι → ℝ; L2Operator norm scope')
b('P','hA : A.IsHermitian','SOURCE','self-adjointness in the exact generic matrix problem','Matrix.IsHermitian = conjugate transpose equals A; over ℝ ordinary transpose equality; no norm/moment/result fields')
b('P','s : ℝ','SOURCE','all real exponential parameters, including zero and negative','ordinary real scalar; no positivity binder')
for name,meaning in [('d : ℕ','source ambient dimension'),('q : ℕ','source Krylov degree')]:b('T',name,'TYPING',meaning,'natural scalar index')
b('T','hq : 2*q+1<d','SOURCE','exact original Gaussian experiment range','natural strict inequality only; d>0 is derived, never a new binder')
b('T','s : ℝ','SOURCE','all-real parameter of the explicitly inferred finite-MGF domain bridge','no s>0 restriction, source-derived bridge rather than an additional printed paper theorem')
b('T','useCos : Bool','TYPING','enumerates the actual ordinary and cos((2q+1)α_i) sums','two literal choices; no random sign or symmetry premise')
b('T','minus : Bool','TYPING','enumerates both global signs of each actual sum','two literal choices; no law or MGF symmetry premise')
definitions=[
 ('D','EuclideanSpace ℝ (Fin d)','source ambient Euclidean space'),
 ('E','EuclideanSpace ℝ (Fin(q+1))','row vector space with ℓ2 norm'),
 ('Ω','Fin(q+1) → D','source q+1 Gaussian probes as full sample carrier'),
 ('μ','Measure.pi (fun _ => stdGaussian D)','original unconditional probability law; not conditioned on truncation'),
 ('M','Matrix (Fin(q+1) × Fin(q+1)) (Fin(q+1) × Fin(q+1)) ℝ','Gaussian-first/feature-second Kronecker index; dimension(q+1)^2'),
 ('r','((q+1:ℕ):ℝ)','source r=q+1, retainingq0'),
 ('L','2*r+3*Real.log(1000*(d:ℝ))','literal source cutoff'),
 ('α','((i.val:ℝ)+1-1/2)*π/(d:ℝ)','source midpoint grid with Lean0-based/source1-based index shift'),
 ('tvec','if k.val=0 then1 else sqrt2*cos(k.val*α i)','literal source cosine basis; the zeroth basis coordinate is1'),
 ('row','WithLp.toLp2 (fun b => ω b i)','literal independent Gaussian row extraction'),
 ('Y','if ‖row i ω‖²≤L then d⁻¹•kronecker(rowouter)(featureouter) else0','inclusive own-row cutoff, source-prescribed zero branch; no invented fallback'),
 ('mean','∫ω,Y i ω∂μ','actual full-law Bochner mean; integrability produced upstream/inside consumer, not supplied'),
 ('Z','Y i ω-mean i','literal centered source summands'),
 ('w','if useCos=true then cos(((2*q+1:ℕ):ℝ)*α i) else1','literal ordinary/cosine source families'),
 ('sign','if minus=true then-1 else1','both global signs, no symmetry identification'),
 ('S','sign minus • ∑i,w useCos i • Z i ω','actual signed weighted centered sum'),
 ('Rstar','2*r*(L+1)/(d:ℝ)','literal source Ex112 deterministic centered radius; proving it is a dependency, not a premise'),
 ('f','trace(exp(s•S useCos minus ω))','ordinary unnormalized real trace; NormedSpace.exp is matrix algebra power series'),
 ('B','r²*exp(|s|*((d:ℝ)*Rstar))','exact finite r²-scaled pointwise envelope, not a variance bound'),
]
audit={'schema':'singleton-binder-and-literal-definition-audit-v1','status':'AUTHOR_AUDITED_NO_EXCESS_AWAIT_DISTINCT_SOURCE_GRAPH_TOPOLOGY_ADMISSION',
 'P_level':'Canonical Library Node; its SOURCE labels mean inputs to the exact stated generic deterministic problem, not a claim that Tropp prints this signature verbatim.',
 'T_level':'Source-derived private actual-experiment interface for the omitted all-real trace-MGF domain bridge; no separate public T credit.',
 'binders':binders,'definition_audit':[{'name':name,'kind':'literal','body_summary':body,'source_semantics':meaning,'exact_body_in_T_sha256':sha(t)} for name,body,meaning in definitions],
 'project_owned_Prop_bundles':[],'EXCESS_count':0,
 'produced_inside_T_not_binders':['probability normalization','all matrix/sum measurability','Y and actual mean integrability','pointwise Hermitian centered sum','pointwise norm bounddRstar','finite and nonnegative domination','trace-exponential integrability for every real s','strict pointwise and ordinary-integral positivity','exactr² cardinality and ordinary integral cap'],
 'meaning_audit':{'norm':'Matrix.Norms.L2Operator, not Frobenius or row-sum norm','trace':'ordinary unnormalized finite diagonal sum','exponential':'NormedSpace.exp in the matrix algebra, not entrywise exp','endpoints':'own-row cutoff≤L; allreal s; no tail event or strict/non-strict probability exchange'},
 'old_candidates_preserved':True,'target_proof_search_started':False}
a=dump('binder-definition-audit.sealed.v1.json',audit)
sources=[(r/'.astis/semantic-neutral-20261113/bernstein_raw_intake_74ab/Tro11-User-Friendly-preprint.pdf','f4c3cff8661011395e793972a1f8d9a199fae4ca0fd098535d7a42166cf8fc86'),(r/'.astis/huanjian-handoff-20261019/2610.20492v1.html','6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915')]
for file,digest in sources:assert sha(file)==digest
seal={'schema':'exact-statement-seal-v1','seal_id':'GC-TRACE-MGF-DOMAIN-20261115-v1','status':'STATEMENTS_SEALED_AUTHOR_ONLY_AWAIT_INDEPENDENT_SOURCE_GRAPH_AND_TOPOLOGY',
 'sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
 'canonical_producer':{'declaration':P,'file':'AutoSamplingTheory/TechnicalLemmas/Analysis/MatrixTraceExponentialBounds.lean','exact_proposition':p.read_text(),'sha256':sha(p)},
 'private_real_consumer':{'declaration':T,'file':'Tests/GaussianComplexityTraceMgfDomain.lean','exact_proposition':t.read_text(),'sha256':sha(t),'public_node':False},
 'source_anchor':'Source-derived omitted finite trace-MGF bridge: Tropp author preprint §§2.1–2.4 and §3.1 finite-expectation-domain caveat; Gaussian arXiv2610.20492v1 AppendixC.2 actual experiment, Ex107–112 and downstream Ex121/p15.2. Not the full Bernstein conclusion.',
 'source_files':[{'file':str(file.relative_to(r)),'sha256':digest} for file,digest in sources],
 'binder_definition_audit':a,'actual_type_formation':{'receipt':str(receipt.relative_to(r)),'sha256':sha(receipt),'exit_code':0,'only_Prop_formation_not_any_target_theorem':True},
 'fixed_toolchain_sha256':sha(r/'lean-toolchain'),'fixed_manifest_sha256':sha(r/'lake-manifest.json'),
 'truth_boundary':'Only deterministic all-real strict trace-exponential/cardinality/norm estimate and its actual four-family Gaussian finite-domain/pointwise-cap/ordinary-expectation consumer. No independence-sum MGF/Lieb/Jensen/mastertail/Bernstein/norm-tail/C6/main-bound/oracle/TV/precision/cap/cost/main/site/purification credit.',
 'proof_search_authorized_by_this_author_seal':False,'required_next':'Independent source-only reconstruction and distinct topology challenge must admit the exact seal before any target proof search.',
 'R15_preservation':'All preceding P/T/core metadata, ledger/frontier, normalPL and independent pending reader/V remain untouched. This is an untracked pre-intake only.'}
s=dump('statement-seal.sealed.v1.json',seal)
print(json.dumps({'seal':s,'audit':a,'target_proof_calls':0,'ledger_or_production_mutations':0}))
