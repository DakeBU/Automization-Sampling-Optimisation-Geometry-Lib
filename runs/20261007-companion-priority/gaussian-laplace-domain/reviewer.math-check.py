import hashlib,json,re,subprocess,sys
from pathlib import Path
from datetime import datetime, timezone
sys.path.insert(0,'tools');import astis
R=Path('runs/20261007-companion-priority/gaussian-laplace-domain')
B='a7f567dcf516c9706eaee12f0b82348f9dd469e3'
def sha(b): return hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n')
def fp(p):
 b=Path(p).read_bytes();return dict(path=str(p).replace('\\','/'),raw_sha256=sha(b),lf_sha256=sha(lf(b)),bytes=len(b))
def read(p):return json.loads(Path(p).read_bytes())
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==B
freeze=read(R/'math-freeze.json');claim=read(R/'claim.json')
inputs=[]
for n,x in enumerate(freeze['inputs']):
 assert fp(x['path'])==x
 out=R/f'reviewer.math-input.{n:03d}.raw.snapshot';assert not out.exists()
 out.write_bytes(Path(x['path']).read_bytes());inputs.append(dict(x,reviewer_snapshot=str(out).replace('\\','/')))
prior=read('runs/20261007-companion-priority/positive-step-proximal-rgo/whole-math-review.json')
parent_checks=[]
for x in prior['unchanged_parent_checks']:
 now=fp(x['path']);assert now['lf_sha256']==x['lf_sha256']
 blob=subprocess.check_output(['git','show',f'{B}:{x["path"]}'])
 assert sha(lf(blob))==now['lf_sha256']
 parent_checks.append(dict(now,prior_whole_math_LF_match=True,prior_raw_match=now['raw_sha256']==x['raw_sha256'],base_git_raw_sha256=sha(blob),base_git_LF_match=True))
old=Path(claim['prior_versions'][0]['snapshot']).read_text(encoding='utf-8')
new=Path(claim['lean_files'][1]).read_text(encoding='utf-8')
private_checks=[]
for name in ['actual_gradient_bounds','parameterized_damped_point','actual_quadratic_minimum']:
 pat=r'private theorem '+name+r'\b.*?(?=\nprivate theorem |\nset_option maxHeartbeats)'
 a=re.search(pat,old,re.S).group();b=re.search(pat,new,re.S).group();assert a==b
 private_checks.append(dict(name=name,proof_text_unchanged=True,normalized_SHA256=sha(b.encode())))
seals=read(R/'preproof/statement-seals.accepted.json');sig_checks=[]
for signature,file in zip(seals['signatures'],claim['lean_files']):
 text=Path(file).read_text(encoding='utf-8');short=signature['full_declaration'].rsplit('.',1)[1]
 actual=text[text.index('theorem '+short):].split(' := by',1)[0]
 assert actual==signature['signature_text']
 assert sha(actual.encode())==signature['signature_lf_sha256']
 sig_checks.append(dict(declaration=signature['full_declaration'],signature_lf_sha256=sha(actual.encode()),exact_sealed_signature=True))
reachable={};queue=claim['lean_files']+claim['test_files']
while queue:
 p=queue.pop();path=Path(p)
 if p in reachable:continue
 reachable[p]=fp(p)
 text=path.read_text(encoding='utf-8')
 for module in re.findall(r'^import\s+(\S+)',text,re.M):
  if module.startswith(('AutoSamplingTheory.','Tests.')):
   q=module.replace('.','/')+'.lean'
   if Path(q).exists():queue.append(q)
hits=[]
for p in reachable:
 for n,line in enumerate(astis.strip_lean_comments_and_strings(Path(p).read_text(encoding='utf-8')).splitlines(),1):
  if astis.FORBIDDEN_REGEX.search(line):hits.append(dict(path=p,line=n,text=line))
assert not hits
mathlib=['.lake/packages/mathlib/Mathlib/Probability/Distributions/Gaussian/Fernique.lean','.lake/packages/mathlib/Mathlib/Probability/Distributions/Gaussian/Basic.lean','.lake/packages/mathlib/Mathlib/Probability/Distributions/Gaussian/Multivariate.lean','.lake/packages/mathlib/Mathlib/Algebra/Order/Field/Basic.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Bochner/Basic.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Function/L1Space/Integrable.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Function/L2Space.lean']
api_inputs=[fp(p) for p in mathlib]
primary=[]
for ident in ['S1.E1','S2.E1','S2.p2.2','S3.SS1.p1.1','S3.SS1.p2.1','S3.E2','S4.E3','S4.Ex3','S4.E4','S4.E5','S4.Thmtheorem2']:
 p=R/f'preproof/source-primary.{ident}.raw.snapshot.html';assert p.exists()
 # Review actual raw source elements rather than source-review verdicts.
 raw=p.read_text(encoding='utf-8');assert '<' in raw and '</' in raw
 primary.append(fp(p))
comp=read(R/'reviewer.compile-results.json');assert len(comp)==4 and all(c['exit_code']==0 for c in comp)
axioms=[]
for c in comp:
 assert sha(Path(c['log']).read_bytes())==c['raw_sha256']
 text=Path(c['log']).read_text(encoding='utf-8')
 for match in re.finditer(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]",text):
  names=[s.strip() for s in match[2].split(',')];assert set(names)=={'propext','Classical.choice','Quot.sound'}
  axioms.append(dict(declaration=match[1],axioms=names,log=c['log']))
assert len(axioms)==18
assert 'Build completed successfully (3731 jobs)' in Path(comp[0]['log']).read_text()
assert all(fp(x['path'])==x for x in freeze['inputs'])
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==B
module_counts=[]
for p in claim['lean_files']+claim['test_files']:
 text=Path(p).read_text(encoding='utf-8')
 module_counts.append(dict(path=p,lines=len(text.splitlines()),private_declarations=len(re.findall(r'^private (?:theorem|def|lemma)',text,re.M)),public_theorems=len(re.findall(r'^theorem ',text,re.M)),entire_body_read=True))
receipt=dict(schema_version=1,advance_id=claim['advance_id'],reviewer_id='picard_commit_verifier_20261005',reviewer_role='independent_whole_mathematics',status='passed-scoped',verification_status='passed-scoped',review_phase='pre-PROVED_LOCAL; not exact-commit VERIFIED',checked_base_commit=B,checked_HEAD=B,production_changes_uncommitted=True,
 frozen_inputs=inputs,original_freeze=fp(R/'math-freeze.json'),before_after_inputs='All14 original frozen raw/LF/size fields exactly unchanged before and after compiler checks.',
 whole_body_review=module_counts,private_provider_reuse=private_checks,unchanged_parent_checks=parent_checks,reachable_source_inputs=list(reachable.values()),pinned_API_inputs=api_inputs,primary_raw_inputs=primary,signature_checks=sig_checks,
 pins=dict(toolchain='leanprover/lean4:v4.33.0',mathlib_commit='db584cd6d46c92f209a44c0f1c829460d327499d',threads=2),
 mathematical_checks=[
  dict(name='actual Gaussian meaning',result='IsGaussian has real continuous-dual Gaussian pushforwards and canonically produces IsProbabilityMeasure. Fernique is for arbitrary (including noncentered/degenerate) Gaussian on a second-countable Banach Borel space; no centered/covariance/nondegeneracy premise added.'),
  dict(name='scalar first moment',result='Lipschitz growth |f(x)|<=L*norm(x)+|f(0)| is dominated by true Gaussian identity L1 plus finite constant; continuity supplies AEStronglyMeasurable. Scalar mean is therefore a genuine integral.'),
  dict(name='all signed exponential domains',result='b=|t|L>=0 and D=|t|(|f(0)|+|mean f|). The exponent is <=b*norm(x)+D. Fernique supplies C>0; Young 2norm(x)b<=Cnorm(x)^2+b^2/C and nonnegativity yield the looser sufficient <=D+b^2/C+Cnorm(x)^2. exp(D+b^2/C)*exp(Cnorm(x)^2) is integrable. This is only a domain proof, with no sharp Gaussian coefficient claim.'),
  dict(name='same genuine output kernel',result='Retained fixed point/minimizer and joint measurable G are unchanged. K=(id times const stdGaussian).map G is Markov and K(s)=map(G_s,stdGaussian) exactly. No posterior/RGO/HMC substitution.'),
  dict(name='vector first moment',result='For each fixed s, genuine sqrt(eta_s)-Lip bound gives norm(G_s(z))<=sqrt(eta_s)norm(z)+norm(G_s(0)). Actual vector L1 follows by domination. Identity K(s) L1 is transferred using integrable_map_measure with actual map measurability; there is no assumed moment certificate.'),
  dict(name='directional center identification',result='f_s,a(z)=inner(a,G_s(z)) has actual Lip norm(a)sqrt(eta_s), including a=0. Leaf gives all t centered scalar exponential L1. Actual vector integral_map and integral_inner(hGi,a) identify its scalar mean with inner(a, integral identity dK(s)). Thus the public center is exactly the same K Bochner mean; no unbiasedness against smoothed gradient is assumed or proved.'),
  dict(name='full positive eta and quantifiers',result='No eta upper/uniform cap enters domain proof. Each s has finite positive eta and a pointwise Gaussian growth coefficient; all directional a and signed t are allowed. Joint kernel measurability is inherited from actual parameterized selector, not a joint choice of Fernique constants.'),
  dict(name='boundary cases',result='L=0, t=0, arbitrary negative t, Gaussian degeneracy and E0 are admitted. Source E0 is actual constant7 potential with genuine stdGaussian/Markov Dirac law; norm/gradient quotient identities have no Nontrivial hypothesis.'),
  dict(name='real consumer and no circularity',result='Only new public Gaussian leaf is called inside original source oracle. All3 source private proofs are text-identical to independently reviewed packet28. No selfcall, wrapper-only consumer, supplied law/moment/Laplace premise, background copy or assumed smoothed-gradient equality found.')],
 independent_compile=dict(checks=[dict(c,footprint=fp(c['log'])) for c in comp],focused_jobs=3731,direct_fresh_production_elaborations=2,source_of_stress=fp(R/'reviewer.stress.stdin.txt'),all_terminal_exit0=True),standard_axioms=dict(printed_declarations=len(axioms),records=axioms),
 stress_checks=[dict(name='positive nonlinear unbounded observable',result='IndependentPacket29 nonlinear_positive_parameter proves true norm first moment and positive3 centered exponential L1; positive exponential grows rather than being bounded as in the official negative3 case.'),dict(name='actual E0 whole domain consumer',result='IndependentPacket29 actual_zero_dimension_domains extracts same actual source K, true K()=Dirac0, vector L1 and all a,t centered Laplace L1 for constant7 potential and eta4. No artificial zero law or supplied final graph/domain.'),dict(name='official boundary consumers',result='Official three files elaborate: nonlinear norm negative3, zero Lipschitz constant, E0 scalar domain, actual varying/unbounded eta=n+2 K and directional a2,t-3 domain, original RGO eta1 sharp1/2/eta2 position,Fisher/signed affine/E0 posterior retain distinct laws.')],
 fake_closure_scan=dict(files=len(reachable),scope='All recursively reachable canonical ASTIS/Test imports of both production and all three Tests; canonical comment/string stripping and FORBIDDEN_REGEX',hits=hits),
 reader_review=dict(status='reader not yet authored for packet29 per root assignment; no reader or publication/source admission claimed',typed_historical_sentence='Frozen claim and math-freeze still contain prior preproof-pending sentence, although preproof statement/topology acceptance artifacts exist. Preserve historical bytes; replace lifecycle prose only in later independently reconciled authoring. This is not a mathematical binder/body change.'),
 exposure=dict(entire_current_Lean_and_Tests_read=True,prior_packet28_math_exposure_disclosed=True,current_anonymous_decoder_or_final_source_review_not_read=True,preproof_signature_topology_are_scope_only_not_proof_correctness_evidence=True),
 remaining_boundary=['Sharp dimension-free centered MGF coefficient1/2, mean=smoothed-gradient/unbiasedness, source bias, FIRST W2 comparison, LSI/T2/Wp/warmness/fullLemma4.2 and both main results/query cost/composition remain open.','This produces necessary Laplace domains for actual Gaussian gradient-output law, not a posterior law or numerical proximal cost algorithm.','Final independent sourceblind/source audit, real publication, PROVED_LOCAL/exact-commit VERIFIED and serialized repository admission remain separate future stages.'],
 leases=dict(compiler='CLOSED; all4 checks terminal exit0',sessions='CLOSED',write='CLOSED after receipt',read='CLOSED'),authorized_writes_only='Own run raw snapshots, compiler script/logs, stdin stress and math receipt; no canonical production/Test/cell/audit/ledger/shared mutation.',no_state_transitions_or_shared_mutations=True,created_utc=datetime.now(timezone.utc).isoformat())
out=R/'whole-math-review.json';assert not out.exists()
out.write_bytes((json.dumps(receipt,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps(dict(status='passed-scoped',receipt=fp(out),frozen_inputs=len(inputs),parents=len(parent_checks),reachable=len(reachable),printed_std3=len(axioms),all_leases='CLOSED')))
