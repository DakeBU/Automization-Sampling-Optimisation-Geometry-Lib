"""One actual normal PROVED_LOCAL by the prover; never a prover VERIFIED."""
from pathlib import Path
import json,hashlib,subprocess,os,sys,datetime,stat
r=Path.cwd();sys.path.insert(0,str(r))
from tools import astis_advance as api
w=r/'.astis/huanjian-gc-trace-mgf-domain-20261115'
e=r/'research-wiki/technical-lemmas/trace-exponential-domain-semantic-evidence'
A='ASTIS-SA-20261115-TraceExponentialDomain';O='huanjian_20261115_trace_exponential_domain'
D='ASTIS-DISC-20261115-ScalarSelfadjointExponentialEnvelope'
P='AutoSamplingTheory.TechnicalLemmas.Analysis.MatrixTraceExponentialBounds.trace_exp_pos_and_le_card_mul_exp_abs_mul_norm'
sha=lambda b:hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text())
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def ident(p):return {'file':str(p.relative_to(r)),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
def git(*xs):return subprocess.check_output(['git',*xs],cwd=r,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'})
carrier='ef5cfe9feb38b716aa17595aedcaea81b18fb032'
assert git('rev-parse','HEAD').decode().strip()==carrier and not git('diff','--name-only').strip()
marker=w/'normal-PL-attempted.once.json';assert not marker.exists()
before=(r/'runs/substantive_advances.jsonl').read_bytes();dbefore=(r/'runs/substantive_discoveries.jsonl').read_bytes()
assert before.endswith(b'\n') and dbefore.endswith(b'\n')
states=api._replay_advances(json.loads(v) for v in before.splitlines());ds=api._replay_discoveries(json.loads(v) for v in dbefore.splitlines())
assert states[A]['state']=='EXPLORING' and states[A]['owner_id']==O
assert ds[D]['status']=='validated' and ds[D]['latest_actor']=='trace_exp_fresh_source_51c8'
baseline=read(w/'preservation-baseline.private.json')
for name,h in baseline['all_existing_frontier_sha256'].items():assert sha((r/name).read_bytes())==h,name
pa=read(r/'research-wiki/semantic-roundtrip/audits/huanjian-trace-exponential-domain.json');ta=read(e/'private-consumer-audit.source-reviewed.v2.json')
assert pa['state']==ta['state']=='source-reviewed'
assert pa['publication_binding_sha256']==ta['publication_binding_sha256']=='e44190bca918ce5a1e8f4ff5fc942c56ea400deb7a10af9929a698ef22a9d45c'
native=e/'independent-native-and-preproof-originals/readable-native-originals/native-mathematics-report.v1.json'
assert sha(native.read_bytes())=='51481e488bee3d6de641a61a5dced0bd9bfaa6f7666e64d5c36595f3b0c5c1ca'
gates=[]
for label in ['publication','contributor','semantic','private-semantic','frontier','whitespace']:
    ps=list((r/'.astis/huanjian-resume-20261103').glob(f'20261115T120014*-gc-trace-exp-frozen-metadata-{label}-gate.receipt.json'))
    assert len(ps)==1;v=read(ps[0]);assert v['exit_code']==0 and v['head_before']==v['head_after']==carrier
    assert sha(Path(v['log']).read_bytes())==v['log_sha256'];gates.append({'gate':label,**ident(ps[0])})
cellpath=r/'research-wiki/frontier-cells/ASTIS-SHARED-REAL-TRACE-EXPONENTIAL-DOMAIN.json';cell=read(cellpath)
browser=r/'.astis/semantic-neutral-20261115/trace_exp_reader_61e4/actual-result.json'
b=read(browser);assert sha(browser.read_bytes())=='17654105a8a14921e275ba90191df0ab125a297b7a94032155eab08b577d27c2'
assert b['status']=='PASS' and len(b['checks'])==389 and all(x['pass'] for x in b['checks'])
payload={
 'result_kind':'reusable-interface','theorem_delta':(w/'P.candidate.v2.txt').read_text(),
 'lean_files':['AutoSamplingTheory/TechnicalLemmas/Analysis/MatrixTraceExponentialBounds.lean','Tests/GaussianComplexityTraceMgfDomain.lean'],
 'lean_declarations':[P],'publication_declarations':[P],
 'focused_checks':{'root_actual_exact_source_builds':cell['evidence']['focused_checks'],'independent_immutable_native':ident(native),'actual_frozen_metadata_gates':gates},
 'truth_boundary':cell['truth_boundary'],'conceptual_mirror_audit':cell['conceptual_mirror_audit'],
 'checked_metadata_commit':carrier,'actual_native_rebuilt_math_commit':'30172847ec40c24426f0b39afc4887719810eca0',
 'statement_seal':ident(r/'research-wiki/technical-lemmas/trace-exponential-domain-statement-seal.json'),
 'binder_definition_norm_audit':{'binder':ident(e/'binder-definition-audit.original.v1.json'),'norm':ident(e/'norm-scope-seal-supplement.v1.json')},
 'independent_preproof_coverage_and_topology':ident(e/'preproof-source-admission.json'),
 'source_to_Lean_correspondence':ident(e/'source-to-lean.correspondence.authored-v3.json'),
 'source_blind_decoding':{'actor':'trace_domain_blind_decoder_8a39','source_text_visible':False,'exact_originals':str((e/'decoder-originals/blind_decoder_8a39').relative_to(r))},
 'fresh_source_wholemodule_seven_slots_and_exposition':{'actor':'trace_exp_fresh_source_51c8','binding':pa['publication_binding_sha256'],
    'public_verdict':pa['verdict'],'private_verdict':ta['verdict'],'original_full_run':'f5cbc9dac309eda9127f3551b368c6bd2d2765e5793947f7e59d7d44a1cd212c',
    'exact_six_scope_successor_run':'8543d7d7365431d074a20c5491750620d242a1b3125379fd8221d9e5270bf64c','raw_originals':str((e/'source-review/trace_exp_fresh_source_51c8/originals').relative_to(r))},
 'native_type_value_kernel':{'report':ident(native),'selected_originals278':ident(e/'independent-native-and-preproof-originals/selected-reviewed-originals278.v1.tar.gz'),
    'scope':'11 fresh ASTIS/Tests modules; actual P/T and q0/d2/all-real/four choices plus mixed diag(-3,2); complete recursive type/value/Std3/kernel evidence; two failed private harness originals retained. No full repository build claimed.'},
 'actual_build_identity_qualification':'Root built exact new worktree bytes at1db9, absent from bare1db9; then froze301728. Independent native actually freshly rebuilt immutable301728. No retroactive build of metadataef5c or any future public identity.',
 'private_material_consumer':'Sole hq2q+1<d; literal original unconditional product standard Gaussian, inclusive own-row cutoff, true full-law integral means, Gaussian-first/feature-second r^2, all real s, both actual weights and both global signs. Internally derives regularity/Hermitian/radius/probability/cardinality and 0<f<=B, Integrable f and0<ordinary integral<=B. No separate public T edge/full matrix MGF/sharp tail.',
 'proof_digestion':cell['proof_digestion'],
 'current_reader_snapshot':{'actual_browser_result':ident(browser),'actual_process_exit_code':0,'checks':389,'false_checks':0,'actual_full_viewport_or_fullpage_PNGs':36,
    'independent_visual_acceptance':'PENDING separate actual-PNG/geometry/reader review at this PL snapshot; flags do not certify visual acceptance.',
    'main_production_site_purification':'Held/not accepted; no physical touch or production browser claim.'},
 'preserved_failures':'Native two harness exits1, first renderer missing6citation scopes, private wrapper missing canonical process protocol and reader preparation PATH missingnode retained; relevant repairs do not change P/T. No environment/API/implementation failure treated as mathematical refutation.',
 'integration_notes':cell['integration_notes'],
 'preservation_scope':'One normal target-only PROVED_LOCAL append. Preserve all old prefixes, all other A/D states, original frontiers, tracked bytes/modes and HEAD/branch/index during API window. Full guards remain private. Root proofV0.'}
dump(e/'PROVED_LOCAL-evidence.full.json',payload)
tracked={}
for p in git('ls-files','-z').split(b'\0'):
    if p:
        name=p.decode();q=r/name;tracked[name]={'sha256':sha(q.read_bytes()),'mode':stat.S_IMODE(q.lstat().st_mode)}
frontiers={str(p.relative_to(r)):sha(p.read_bytes()) for p in (r/'research-wiki/frontier-cells').rglob('*') if p.is_file()}
ip=Path(git('rev-parse','--git-path','index').decode().strip());ip=ip if ip.is_absolute() else r/ip
ih=sha(ip.read_bytes());branch=git('symbolic-ref','-q','HEAD')
dump(marker,{'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'normal_PL_calls_authorized':1,
 'executed_driver_sha256':sha(Path(__file__).read_bytes()),'payload_sha256':sha((e/'PROVED_LOCAL-evidence.full.json').read_bytes()),'metadata_commit':carrier})
api.transition_advance(A,'PROVED_LOCAL',worker_id=O,modes=['proof-design','compiler-diagnosis','source-review'],evidence=payload)
after=(r/'runs/substantive_advances.jsonl').read_bytes();assert after.startswith(before)
delta=[json.loads(v) for v in after[len(before):].splitlines()]
assert len(delta)==1 and delta[0]['advance_id']==A and delta[0]['to_state']=='PROVED_LOCAL'
new=api._replay_advances(json.loads(v) for v in after.splitlines())
assert {k:v for k,v in states.items() if k!=A}=={k:v for k,v in new.items() if k!=A}
assert (r/'runs/substantive_discoveries.jsonl').read_bytes()==dbefore
assert git('rev-parse','HEAD').decode().strip()==carrier and git('symbolic-ref','-q','HEAD')==branch and sha(ip.read_bytes())==ih
for name,x in tracked.items():
    q=r/name;assert stat.S_IMODE(q.lstat().st_mode)==x['mode']
    if name!='runs/substantive_advances.jsonl':assert sha(q.read_bytes())==x['sha256'],name
assert {str(p.relative_to(r)):sha(p.read_bytes()) for p in (r/'research-wiki/frontier-cells').rglob('*') if p.is_file()}==frontiers
(e/'actual-PROVED_LOCAL-append.exact.jsonl').write_bytes(after[len(before):])
cell['status']='proved_locally';cell['evidence']['normal_PROVED_LOCAL']={'full_evidence':ident(e/'PROVED_LOCAL-evidence.full.json'),
 'actual_append':ident(e/'actual-PROVED_LOCAL-append.exact.jsonl'),'normal_calls':1,'checked_metadata_commit':carrier}
cell['evidence']['current_normal_stage'].update(advance_state='PROVED_LOCAL',cell_status='proved_locally',theorem_PROVED_LOCAL=True)
cell['phase_snapshot']='One actual normal PROVED_LOCAL. Immutable301728 mathematics, independent native/source and current metadata gates accepted. Actual isolated browser389checks/0false/36PNG; independent visual acceptance and proofV pending. Main/site/global integration/purification/full paper remain open.'
dump(cellpath,cell)
mem=read(e/'local-cycle-memory.json');mem.update(normal_state='PROVED_LOCAL',normal_PL_calls=1,ROOT_V_calls=0,reader_machine_checks='actual389/0false/36PNG; independent visual pending');dump(e/'local-cycle-memory.json',mem)
dump(w/'actual-PL-result.v1.json',{'normal_state':new[A]['state'],'normal_PL_calls':1,'Root_V_calls':0,
 'original_evidence_sha256':sha((e/'PROVED_LOCAL-evidence.full.json').read_bytes()),'exact_append_sha256':sha(after[len(before):]),'preservation_checks_pass':True})
print(json.dumps({'actual_normal_state':new[A]['state'],'normal_PL_calls':1,'Root_V_calls':0,'all_foreign_states_frontiers_HEAD_branch_index_tracked_preserved_in_API_window':True,'independent_reader_visual':'pending'}))
