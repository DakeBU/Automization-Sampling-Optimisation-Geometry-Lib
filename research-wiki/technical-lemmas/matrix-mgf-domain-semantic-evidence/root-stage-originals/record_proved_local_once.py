from pathlib import Path
import json,hashlib,subprocess,os,sys,datetime,stat
r=Path.cwd();sys.path.insert(0,str(r));from tools import astis_advance as api
w=r/'.astis/huanjian-gc-matrix-mgf-domain-20261115';e=r/'research-wiki/technical-lemmas/matrix-mgf-domain-semantic-evidence'
A='ASTIS-SA-20261115-MatrixExponentialDomain';O='huanjian_20261115_matrix_exponential_domain'
P='AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveDefIntegral.integral_posDef'
carrier='affe4e783fa90a5ebb6286368c76e161e8cb51d8';math='a8bb8ea5b4474be5214bd83ae380a612e2cecb78'
sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(p.read_text())
git=lambda *a:subprocess.check_output(['git',*a],env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'})
def ident(p):return {'file':str(p.relative_to(r)),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
assert git('rev-parse','HEAD').decode().strip()==carrier and not git('diff','--name-only').strip()
marker=w/'normal-PL-attempted.once.json';assert not marker.exists()
old_a=(r/'runs/substantive_advances.jsonl').read_bytes();old_d=(r/'runs/substantive_discoveries.jsonl').read_bytes()
assert old_a.endswith(b'\n') and old_d.endswith(b'\n')
states=api._replay_advances(json.loads(v) for v in old_a.splitlines());ds=api._replay_discoveries(json.loads(v) for v in old_d.splitlines())
assert states[A]['state']=='EXPLORING' and states[A]['owner_id']==O
c=r/'research-wiki/frontier-cells/ASTIS-SHARED-REAL-MATRIX-EXPONENTIAL-DOMAIN.json';cell=load(c)
pa=load(r/'research-wiki/semantic-roundtrip/audits/huanjian-matrix-mgf-domain.json');ta=load(e/'private-consumer-audit.source-reviewed.v2.json')
assert pa['state']==ta['state']=='source-reviewed' and pa['verdict']==ta['verdict']=='equivalent-after-elaboration'
assert pa['publication_binding_sha256']==ta['publication_binding_sha256']=='5e79fa3d4390c4d1e689174b0c014d67fb8dbfb550f986b4af7d8474ef644691'
native=e/'independent-native-originals/matrix_domain_native_61e4/native-mathematics-report.v1.json'
assert sha(native.read_bytes())=='b9d494dc7402ec65930714729534ee69e3dd1ba52b85a16d9544691f5c4b73ee'
gates=[]
for label in ['publication','contributor','semantic','private-semantic','frontier','whitespace']:
 ps=list((r/'.astis/huanjian-resume-20261103').glob('20261115T143533*-gc-matrix-mgf-frozen-reviewed-metadata-'+label+'-gate.receipt.json'))
 assert len(ps)==1;v=load(ps[0]);assert v['exit_code']==0 and v['head_before']==v['head_after']==carrier
 assert sha(Path(v['log']).read_bytes())==v['log_sha256'];gates.append({'gate':label,**ident(ps[0])})
payload={'result_kind':'reusable-interface','theorem_delta':(w/'P.candidate.v1.txt').read_text(),'lean_files':['AutoSamplingTheory/TechnicalLemmas/Probability/RealMatrixPositiveDefIntegral.lean','Tests/GaussianComplexityMatrixMgfDomain.lean'],'lean_declarations':[P],'publication_declarations':[P],'focused_checks':{'root_actual_P_T':cell['evidence']['focused_checks'],'independent_exact_immutable_native':ident(native),'actual_frozen_metadata_gates':gates},'truth_boundary':cell['truth_boundary'],'conceptual_mirror_audit':cell['conceptual_mirror_audit'],'checked_metadata_commit':carrier,'actual_native_rebuilt_math_commit':math,'statement_seal':ident(r/'research-wiki/technical-lemmas/matrix-mgf-domain-statement-seal.json'),'binder_definition_audit':ident(e/'binder-definition-audit.original.v1.json'),'independent_preproof_admission':ident(e/'preproof-source-admission.original.v1.json'),'preproof_originals35':ident(e/'preproof-originals/selected-preproof-formation-intake-originals35.v1.tar.gz'),'source_to_Lean_correspondence':ident(e/'source-to-lean.correspondence.locators-reviewed-v2.json'),'source_blind_decoding':{'actor':'/root/blind_decoder_8f2c','source_text_visible':False,'originals':str((e/'decoder-originals/blind_decoder_8f2c').relative_to(r)),'run_sha256':'e99cfb25a546fd7b75db934dce5660b20c41e1a9f012d7089458aed9a656afa6'},'fresh_source_whole_module_seven_slots_five_steps':cell['evidence']['source_review'],'native_type_value_kernel':{'report':ident(native),'selected_originals187_plus_manifest':ident(e/'independent-native-originals/matrix_domain_native_61e4/native-selected-originals.v1.tar.gz'),'scope':'13 exact immutablea8bb source modules freshly recompiled, literal P/T types/actual values/kernel/recursive closure Std3/unsafe0/sorryAx0; P empty/single/AE-only null-badpoint and Tq0d2 allreal/fourBool/12specifics tests. No whole-repository or rootTests build.'},'private_material_consumer':'Literal full original product Gaussian experiment with only hq2q+1<d; inclusive own-row cutoff, true full-law means, gamma-first paired r² index, q0, every real s, both weights and both global signs. Proves actual matrix exp Bochner integrability and true mean PD, trace commutation and strict positive r² envelope. Natural P integrability/AE-PD hypotheses are proved internally in T; no extra T premise/public T node.','actual_build_identity_qualification':'Root built exact newly added working-file bytes whileHEAD960c, then frozea8bb; independent native actually rebuilt immutablea8bb. No retroactive bare960c/metadataaffe/future-public build claim.','proof_digestion':cell['proof_digestion'],'current_reader_snapshot':{'status':'PENDING_ACTUAL_BROWSER_AND_INDEPENDENT_VISUAL_REVIEW','actual_static_fixture':'.astis/huanjian-gc-matrix-mgf-domain-20261115/reader-preview-v1/static-closure-v3/fixtures/candidate/','actual_static_checks':'270 checks0false; renderer exit0. Current MathJax/sharedstyles. No Chrome/server yet at this original PL snapshot.','whole_site_production_physical_touch_purification':'Not accepted.'},'preserved_failures':'First Prop formation failed missing Gaussian import (compiler-generated sorry is failed probe only), then unchanged interface type-formed; first publication gate failed honestly while source review pending; one frontier metadata classification failed then corrected to one serial root proof route with concurrent independent review roles retained; original narrow gap locator maps and graph-edge findings preserved with independent exact overlays. No mathematical proof failure/refutation.','integration_notes':cell['integration_notes'],'preservation_scope':'Exactly one ROOT normal target PROVED_LOCAL append; old prefixes/fullD/allforeignstates/otherfrontiers/HEAD/branch/index/trackedbytes/modes preserved during API window. Full private guard maps stay memory-only. Root V0. Reader/normalV/main/publication/purification/Goal completion remain distinct.'}
ev=e/'PROVED_LOCAL-evidence.full.json';assert not ev.exists();dump(ev,payload)
tracked={n.decode():(stat.S_IMODE((r/n.decode()).lstat().st_mode),sha((r/n.decode()).read_bytes())) for n in git('ls-files','-z').split(b'\0') if n}
front={str(p.relative_to(r)):sha(p.read_bytes()) for p in (r/'research-wiki/frontier-cells').rglob('*') if p.is_file()}
ip=Path(git('rev-parse','--git-path','index').decode().strip());ip=ip if ip.is_absolute() else r/ip
ih=sha(ip.read_bytes());branch=git('symbolic-ref','-q','HEAD')
with marker.open('x') as f:
 os.chmod(marker,0o600);json.dump({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'driver_sha256':sha(Path(__file__).read_bytes()),'payload_sha256':sha(ev.read_bytes()),'normal_PL_calls_authorized':1,'ROOT_V_calls_authorized':0,'checked_metadata_commit':carrier},f,indent=2);f.write('\n')
api.transition_advance(A,'PROVED_LOCAL',worker_id=O,modes=['proof-design','compiler-diagnosis','source-review'],evidence=payload)
new_a=(r/'runs/substantive_advances.jsonl').read_bytes();assert new_a.startswith(old_a)
delta=[json.loads(v) for v in new_a[len(old_a):].splitlines()];assert len(delta)==1 and delta[0]['advance_id']==A and delta[0]['to_state']=='PROVED_LOCAL'
new=api._replay_advances(json.loads(v) for v in new_a.splitlines());assert {k:v for k,v in new.items() if k!=A}=={k:v for k,v in states.items() if k!=A}
assert (r/'runs/substantive_discoveries.jsonl').read_bytes()==old_d
assert git('rev-parse','HEAD').decode().strip()==carrier and git('symbolic-ref','-q','HEAD')==branch and sha(ip.read_bytes())==ih
for n,(mode,h) in tracked.items():
 assert stat.S_IMODE((r/n).lstat().st_mode)==mode
 if n!='runs/substantive_advances.jsonl':assert sha((r/n).read_bytes())==h,n
assert {str(p.relative_to(r)):sha(p.read_bytes()) for p in (r/'research-wiki/frontier-cells').rglob('*') if p.is_file()}==front
append=e/'actual-PROVED_LOCAL-append.exact.jsonl';assert not append.exists();append.write_bytes(new_a[len(old_a):])
cell['status']='proved_locally';cell['evidence']['normal_PL']={'normal_calls':1,'checked_metadata_commit':carrier,'full_evidence':ident(ev),'actual_append':ident(append)}
cell['phase_snapshot']='One actual normal PROVED_LOCAL after independent immutable native/source/locator acceptance and six real metadata gates. Actual browser/visual and independent normal V remain pending. No main/global/production/purification/Goal completion.';dump(c,cell)
memory=e/'local-cycle-memory.json';assert not memory.exists();dump(memory,{'advance_id':A,'owner':O,'state':'PROVED_LOCAL','actual_math_commit':math,'checked_metadata_commit':carrier,'normal_PL_calls':1,'Root_V_calls':0,'independent_native_and_source':'accepted scoped; originals preserved','reader':'actual runtime/visual pending at this original snapshot','both_full_main_lower_bounds_completed':0,'main_production_purification':'held/pending','next':'Complete actual isolated reader; independently execute one normal V; owned-only safe-public candidate/review/CAS push/readback.'})
out={'actual_normal_state':new[A]['state'],'normal_PL_calls':1,'Root_V_calls':0,'original_evidence_sha256':sha(ev.read_bytes()),'actual_append_sha256':sha(append.read_bytes()),'all_old_foreign_state_frontier_HEAD_branch_index_tracked_guards_passed':True,'reader_actual':'pending'};dump(w/'actual-PL-result.v1.json',out);print(json.dumps(out))
