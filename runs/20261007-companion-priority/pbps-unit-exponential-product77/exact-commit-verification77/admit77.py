"""Publish only this independent VERIFIED admission after all bounded checks pass."""
import datetime, hashlib, json, os, subprocess, sys
from pathlib import Path
ROOT=Path('E:/Samplinglib')
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'tools'))
from tools.astis_advance import transition_advance
P=ROOT/'runs/20261007-companion-priority/pbps-unit-exponential-product77/exact-commit-verification77'
COMMIT='4f88383540a865aea304c63c40de5a699ea61611'
DECL='AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws'
CELL=ROOT/'research-wiki/frontier-cells/ASTIS-SHARED-unit-exponential-product.json'
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def info(p):
    b=Path(p).read_bytes()
    return {'path':str(p),'RAW_bytes':len(b),'RAW_sha256':hashlib.sha256(b).hexdigest()}
def save(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert load(P/'checks-complete.json')['status']=='PASS'
assert load(P/'prior-evidence-readback.json')['status']=='PASS_EXACT_PRIOR_EVIDENCE'
mathlib=subprocess.run(['git','-C',str(ROOT/'.lake/packages/mathlib'),'rev-parse','HEAD'],capture_output=True,check=True).stdout.decode().strip()
assert mathlib=='db584cd6d46c92f209a44c0f1c829460d327499d'
module=ROOT/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean'
assert info(module)['RAW_sha256']=='c4a93999f287008d9ddb3f3624f52f302df122e5e007a54fd427a9985edc5ec0'
assert subprocess.run(['git','show',COMMIT+':AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean'],capture_output=True,check=True,cwd=ROOT).stdout==module.read_bytes()
checks=['fresh-whole-module-axioms','focused-module','contributor-successor','publication-successor','semantic-successor','frontier-recheck','packet']
receipts=[]
for name in checks:
    r=load(P/(name+'.receipt.json'))
    assert r['exit_code']==0 and r['terminal_closed']
    assert info(r['stdout']['path'])['RAW_sha256']==r['stdout']['RAW_sha256']
    assert info(r['stderr']['path'])['RAW_sha256']==r['stderr']['RAW_sha256']
    receipts.append(info(P/(name+'.receipt.json')))
assert not load(P/'fake-closure-scan.json')['hits']
cell=load(CELL)
assert cell['status']=='proved_locally'
save(P/'cell.before-independent-admission.json',cell)
proof_checks=[
    'Private Prop expands to literal P=infinitePi Exp(1), X=evaluation, epsilon=toNNReal(X); five conjuncts and zero public mathematical premises.',
    'Positive rate factor probability is proved before the actual infinite-product probability/marginal/independence APIs; no fallback product or iid provider premise.',
    'CDF at zero proves nonpositive coordinates null. Coordinate pushforwards and countability give one simultaneous AE positive/clamp-equality event.',
    'Indicator B_k=1_(X_k>1) has internally derived integrability, measurable transform independence and identical distributions.',
    'CDF at one and indicator integration prove E[B_0]=exp(-1)>0. No exponential first moment is assumed or exported.',
    'Pinned strong_law_ae_real consumes only internally proved conditions and yields AE average convergence to the exact positive mean.',
    'Multiplication by n gives indicator-sum divergence with n=0 handled explicitly. Universal B_k<=epsilon_k transfers divergence by finite-sum domination, including exceptional nonpositive coordinates.'
]
verdict={'status':'PASS_INDEPENDENT_EXACT_COMMIT_VERIFICATION','verifier_id':'/root/exact_verify77',
    'verified_commit':COMMIT,'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'actual_admission_helper_PID':os.getpid(),'lean_module':info(module),'gate':receipts,
    'fresh_full_source_elaboration':True,'axioms':['propext','Classical.choice','Quot.sound'],
    'fixed_mathlib_revision':mathlib,'semantic_roundtrip_audit':'ASTIS-RT-20261010-UnitExponentialProduct',
    'source_audit':{'state':'accepted','reviewer':'/root/source_review77',
       'review_result':info(P.parent/'resume-source-review77/source-review.result.json'),
       'review_run':info(P.parent/'resume-source-review77/review-run-manifest.json'),
       'packet_sha256':'1c3feb5057d8e15852de39a725181e585ce07787c904873c8d77db95feebb1dc'},
    'publication_binding_sha256':'465fcece1be5adf9e62da6bad2639b3d4c65943b35b733b75e6f44227b6e09bf',
    'prior_evidence_readback':info(P/'prior-evidence-readback.json'),
    'successor_metadata_delta_and_unchanged_evidence':info(P/'successor-delta.json'),
    'original_fresh_compilation_commit':'24cacd367f9936a68fc709a02b3b051802033aa6',
    'fresh_evidence_reuse_reason':'Successor changes only source-detail vocabulary and its helper, while module/lesson/audit/publication/packet/manifest/toolchain remain exact to independently elaborated science.',
    'fake_closure_scan':info(P/'fake-closure-scan.json'),'publication_declarations':[DECL],
    'independent_whole_proof_checks':proof_checks,'seven_formula_and_BODY_lesson_steps':'Exact contiguous full public BODY and formulas independently inspected; input-freeze.json records the raw region hashes.',
    'source_route_boundary':'Selected actual Exp(1) input-law leaf only. Author direct Exp integrability/mean-one SLLN route remains separate OPEN; ASTIS indicator route is a sufficient OR-route. Full Ex9 clock/nonaccumulation/process/Markov/invariance/error/query-cost/composition not admitted.',
    'remaining_acceptance':['aggregate/root Tests and astis.py check','generated graph/site gates and visual reader acceptance','serialized stabilization','main merge and remote CI','live validation','Exposition Seal and postmerge purification','whole paper/composition and existing four-paper Goal'],
    'production_edits':False,'stabilization':False,'Goal_complete':False,
    'provenance':'Named input hashes, real foreground process command receipts, direct whole-proof readback and independently reviewed source evidence. No fabricated native reasoning trajectory.'}
save(P/'verified.json',verdict)
evidence={k:verdict[k] for k in ['verifier_id','verified_commit','source_audit','fake_closure_scan','publication_declarations','semantic_roundtrip_audit']}
evidence['gate']=info(P/'verified.json')
transition_advance('ASTIS-SA-20261010-UnitExponentialProduct','VERIFIED',worker_id='/root/exact_verify77',evidence=evidence)
cell['status']='independently_verified'
cell['evidence']['independent_verification']=(P/'verified.json').relative_to(ROOT).as_posix()
save(P/'cell.after-independent-admission.json',cell)
os.replace(P/'cell.after-independent-admission.json',CELL)
save(P/'admission.json',{'state':'VERIFIED','cell_state':'independently_verified','verifier_id':'/root/exact_verify77',
    'verified_commit':COMMIT,'verified':info(P/'verified.json'),'cell':info(CELL),
    'remaining_acceptance':verdict['remaining_acceptance'],'stabilization':False,'Goal_complete':False})
print('VERIFIED independent admission:',COMMIT)
