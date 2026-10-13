"""Bind partial proof evidence without claiming the sealed SAU is proved."""
from pathlib import Path
import json,hashlib,datetime,sys,subprocess
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from tools import astis_advance as advance
RUN=Path(__file__).resolve().parent
PRE=ROOT/'runs/20261007-companion-priority/pbps-ordered-iteration-preread92'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def d(p):
 p=Path(p)
 if not p.is_absolute(): p=ROOT/p
 b=p.read_bytes()
 return dict(path=p.as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
checked={}
def verify(o):
 if isinstance(o,dict):
  if 'path' in o and 'raw_sha256' in o:
   v=d(o['path']);assert v['raw_sha256']==o['raw_sha256'],o['path']
   if 'bytes' in o:assert v['bytes']==o['bytes'],o['path']
   checked[v['path']]=v
  for v in o.values():verify(v)
 elif isinstance(o,list):
  for v in o:verify(v)
reviews=[RUN/'independent-fragments92/fragment-review92.native.json',
 RUN/'independent-coordinate-fragments92/coordinate-fragment-review92.native.json']
manifests=[RUN/'independent-fragments92/fragment-review-closed-RAW92.native.json',
 RUN/'independent-coordinate-fragments92/coordinate-review-closed-RAW92.native.json']
for p in reviews+manifests:verify(read(p))
verify(read(PRE/'resume-before-seal92/preserved-collaborator92.json'))
receipts=[RUN/'focused'/x/'receipt.json' for x in ['geometry10-zero-time','coordinates7-typed-interval','recursion3-folded-state','base2-subtype-domain']]
for p in receipts:
 o=read(p);assert o['exit_code']==0;verify(o)
files=[RUN/x for x in ['Geometry92.lean','Coordinates92.lean','Recursion92.lean','Base92.lean']]
import re
for p in files:
 assert not re.search(r'\b(sorry|admit|axiom)\b',p.read_text(encoding='utf8')),p
residual=('Prove the positive-depth actual probability-law induction using actual91 localized to the old prefix guard. '
 'Still required: identify B_(n+1) with the intersection of old strict-prefix B_n and actual91 next-event B; '
 'instantiate state/weight algebra by literal bounce-after-flow and rate-times-survival; '
 'identify appendAbs(K_n(t),u) with K_(n+1)(snoc(t,u)); derive ENNReal factorization with proved nonnegativity; '
 'bridge subtype comap integrals to ambient restricted-volume integrals; '
 'use the induction identity for the Borel inner integral; derive full law, all tests, and mass, then assemble exact sealed header. '
 'No full theorem, PROVED_LOCAL, full decoder/source review, stabilization or paper completion is claimed.')
cp={
 'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'advance_id':'ASTIS-SA-20261011-PBPSActualOrderedPrefix','state':'EXPLORING',
 'statement_seal':d(RUN/'root.statement-seal92.json'),
 'compiled_internal_fragments':[d(p) for p in files],
 'focused_receipts':[d(p) for p in receipts],
 'independent_fragment_reviews':[d(p) for p in reviews],
 'independent_review_manifests':[d(p) for p in manifests],
 'review_inputs_rehashed':list(checked.values()),
 'base_fragment_review':'pending at checkpoint creation; compile passed, no independent acceptance inferred',
 'closed_internal_boundaries':['Delta/A measurability; parameter-joint K/q Borel and qReal nonnegative',
  'Pointwise complete actual/prescribed history reconstruction on every raw input in strict prefix B',
  'Ordered-simplex snoc decomposition and Lebesgue-preserving last-coordinate transport',
  'Tonelli simplex integral identity for arbitrary nonnegative extended Borel integrands',
  'Finite induction state-prefix/last-state and product-factor decomposition',
  'n=0 actual canonicalP all-history-test integral base case (compiled; independent review pending)'],
 'exact_residual':residual,
 'next_implementation_route':[
  'Use actual91 with b(h)=T and its old-history localization event A_n(T). Its inner ENNReal integral is Borel.',
  'Prove the literal actual event intersection is B_(n+1); use the induction hypothesis on the inner Borel history test.',
  'For scalar g(t)=F(K_(n+1)t)*q_(n+1)t on the simplex subtype, reuse MeasurableEmbedding.exists_measurable_extend (Embedding.lean:114) to choose a Borel ambient extension. This avoids reimplementing total off-simplex dynamics.',
  'Use map_comap_subtype_coe and lintegral_subtype_comap to change to ambient restricted volume; apply compiled simplex_lintegral_snoc.',
  'On strict fibers prove exact K append and q product using compiled recursion algebra and actual91 density; no terminal survival is inserted.',
  'After the integral law is proved for all n, derive measure equality using indicator tests, total mass via F=1, and P(B)<=1 from canonical input probability.'
 ],
 'failure_diagnoses':[
  {'class':'API_BLOCKED','scope':'geometry1/2','diagnosis':'Pinned Mathlib uses MeasurableSet.iInter and measurable_coe_nnreal_real; guessed forall aliases were unavailable. Resolved by exact definition retrieval.'},
  {'class':'IMPLEMENTATION_FAILED','scope':'geometry4/5/6','diagnosis':'Identical printed readTime functions came from distinct generated matchers. After three same-boundary outputs, pp.all diagnostic isolated matcher constants; branchwise function equality resolves geometry8. No statement change.'},
  {'class':'IMPLEMENTATION_FAILED','scope':'coordinates1-6','diagnosis':'Dependent Fin motive inference, explicit product-integrand inference and Set.Ioo indicator typing. Resolved with explicit existing types; mathematical target unchanged.'},
  {'class':'IMPLEMENTATION_FAILED','scope':'recursion1/2','diagnosis':'CastSucc/succ orientation and eager unfolding beneath recursive lambda prevented rewrite. Retaining folded state and changing only the outer recursion closes recursion3.'},
  {'class':'IMPLEMENTATION_FAILED','scope':'base1','diagnosis':'Fin(0+1) subsingleton TC reduction and global rewriting of Delta0 changed subtype carrier in the auxiliary mass equation. Fin.ext and RHS-only rewriting preserve sealed subtype and close base2.'}
 ],
 'preserved_collaborator_files':21,
 'production_target_exists':(ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualOrderedPrefix.lean').exists(),
 'publication':'Pending complete proof; no new Registry/import/site completion status.',
 'push':'Latest pushed integration remains57ffbfed9ecde5d49c9dae4f9d2cb5aa593f26fe; this92 exploration is local.'}
out=RUN/'checkpoint92-first-proof-fragments.json';assert not out.exists()
out.write_text(json.dumps(cp,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
advance.checkpoint_advance(cp['advance_id'],worker_id='companion_root_20261005',
 route_fingerprint='actual-prefix/absolute-coordinate-induction/complete-history',
 progress_signature=hashlib.sha256(out.read_bytes()).hexdigest(),
 mathematical_delta='Compiled joint Borel/positivity, pointwise actual-history identification, ordered simplex Tonelli and recursion factorization; first two fragment groups independently reviewed; actual n=0 integral base compiled.',
 exact_residual=residual)
cellpath=ROOT/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-ordered-prefix.json'
cell=read(cellpath)
cell['evidence']['partial_checkpoint']=out.relative_to(ROOT).as_posix()
cell['evidence']['partial_proof_reviews']=[p.relative_to(ROOT).as_posix() for p in reviews]
cell['blocked']['reason']='Active proof implementation: partial internal fragments compiled/reviewed; full positive-depth law induction remains open.'
cellpath.write_text(json.dumps(cell,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'checkpoint':d(out),'state':'EXPLORING','review_bound_inputs_checked':len(checked)},indent=2))
