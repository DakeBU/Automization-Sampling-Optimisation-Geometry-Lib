from pathlib import Path
import sys,json,hashlib,subprocess,os,shutil,re,datetime
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC');S=ROOT/'.astis/semantic-neutral-20261111/kr_src_c47e12';P=S/'phase5-normal-sourceV';W=ROOT/'.astis/huanjian-gc-fixed-spectrum-krylov-range-20261110';E=ROOT/'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-krylov-range-semantic-evidence';N=W/'independent-native-reader-5f09a3/phase1-972d8994'
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(P))
from tools import astis_publication as pub
from tools.astis_semantic_roundtrip_core import semantic_reviewer_packet
import preservation_guard as guard
h=lambda b:hashlib.sha256(b).hexdigest()
request=json.loads((W/'exact-normal-sourceV-request.json').read_text())
assert h((W/'exact-normal-sourceV-request.json').read_bytes())=='974f4d7a4d6eb10d211b103a4a42873ca090c16d357ff891c9d7577f2f769d21'
originals=P/'original-inputs';originals.mkdir(exist_ok=True)
shutil.copyfile(W/'exact-normal-sourceV-request.json',originals/'exact-normal-sourceV-request.json')
gitrows=[]
paths=json.loads((S/'phase4/candidate-process-request.json').read_text())['permitted_readonly_git_paths']+['lean-toolchain','lake-manifest.json','research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-krylov-range.json','research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-krylov-range.json']
gdir=P/'metadata-git-readback';gdir.mkdir(exist_ok=True)
for k,path in enumerate(paths):
 argv=['git','show',request['metadata_checked_commit']+':'+path]
 r=subprocess.run(argv,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
 (gdir/(str(k)+'.raw')).write_bytes(r.stdout);(gdir/(str(k)+'.stderr')).write_bytes(r.stderr)
 (gdir/(str(k)+'.receipt.json')).write_text(json.dumps({'argv':argv,'exit_code':r.returncode,'stdout_sha256':h(r.stdout),'stderr_sha256':h(r.stderr)},indent=2)+'\n')
 assert r.returncode==0 and r.stdout==(ROOT/path).read_bytes(),path
 if k<7:assert r.stdout==(S/'phase4/git-snapshots'/(str(k)+'.raw')).read_bytes(),path
 gitrows.append({'path':path,'sha256':h(r.stdout),'exact_commit_and_current_working_bytes':True})
audit=json.loads((ROOT/paths[7]).read_text());frontier=json.loads((ROOT/paths[8]).read_text())
overlay=json.loads((S/'phase4/source-review-overlay.json').read_text());semantic=json.loads((S/'phase4/canonical-semantic-review-result.v2.json').read_text());packet=json.loads((S/'phase3/inputs/canonical-reviewer-packet.json').read_text())
assert audit['state']=='source-reviewed'and audit['source_review']==overlay['source_review']
for k in ['semantic_slots','deltas','verdict','repairs']:assert audit[k]==semantic[k],k
assert semantic_reviewer_packet(audit)==packet
item=json.loads((ROOT/paths[3]).read_text())['items'][0];binding=item['bindings'][0]
assert pub.binding_payload(item,binding)==json.loads((S/'phase4/exact-binding-payload.json').read_text())
assert pub.binding_digest(item,binding)==request['publication_binding_sha256']==audit['publication_binding_sha256']
pub.check_advance([binding['declaration']],reviewed=True)
gates=[]
for row in request['actual_metadata_gate_receipts']:
 rb=(ROOT/row['receipt']).read_bytes();lb=Path(row['log']).read_bytes();assert h(rb)==row['receipt_sha256']and h(lb)==row['log_sha256']
 r=json.loads(rb);assert r['exit_code']==0 and r['head_before']==r['head_after']==request['metadata_checked_commit']and r['log_sha256']==h(lb)
 shutil.copyfile(ROOT/row['receipt'],originals/Path(row['receipt']).name);shutil.copyfile(row['log'],originals/Path(row['log']).name)
 gates.append({'original_receipt':row,'actual_receipt_full':r,'actual_log_full':lb.decode()})
for rel,row in request['artifact_inputs'].items():
 path=ROOT/rel;b=path.read_bytes();assert len(b)==row['bytes']and h(b)==row['sha256']
 shutil.copyfile(path,originals/path.name)
for name in ['fresh-source-c47e12-phases1-4-all-original-files.archive-manifest.json','fresh-native-5f09a3-all-original-files.archive-manifest.json']:
 m=json.loads((E/name).read_text());path=ROOT/m['archive'];assert h(path.read_bytes())==m['sha256'];shutil.copyfile(path,originals/path.name)
native=json.loads((N/'native-inventory.json').read_text());summary=json.loads((N/'native-summary.json').read_text());verdict=json.loads((N/'independent-verdict.json').read_text());static=json.loads((N/'static-render-report.json').read_text());adj=json.loads((N/'static-exact-adjacency-supplement.json').read_text())
for row in native['owned']:
 assert all(row[k]is True for k in ['is_prop','has_value','closed_value','closed_type','std3_only'])
 assert row['kind']=='theorem'and set(row['axioms'])<={'propext','Classical.choice','Quot.sound'}
assert len(native['owned'])==4 and summary['unreachable_owned']==[]
for row in native['exact_seal_type_comparisons']:
 assert row['expected_closed']and row['expected_is_prop']and row['defeq']and row['literal_expr_equal']is False
assert all(r['byte_equal']for r in summary['literal_source_signature_checks'])
owned={r['name']:r for r in native['owned']};producer=binding['declaration'];consumer=next(r['name']for r in native['owned']if r['name'].endswith('.actual_krylov_quadratic_coordinates'))
def first_public(n,seen=frozenset()):
 if n in seen:return set()
 out=set()
 for parent in owned[n]['direct_value_parents']:
  q=parent['name']
  if q==producer:out.add(q)
  elif q in owned:out|=first_public(q,seen|{n})
  elif parent['module'].startswith('AutoSamplingTheory.'):out.add(q)
 return out
assert first_public(producer)==set()and first_public(consumer)=={producer}
receipts=[]
for name in ['019-native-FixedSpectrumKrylovRange.json','020-native-GaussianComplexityFixedSpectrumKrylovRange.json','029-native-IndependentInventory.json']:
 path=N/'logs'/name;r=json.loads(path.read_text());assert r['exit_code']==0
 for k in ['stdout','stderr']:
  b=(N/r[k+'_file']).read_bytes();assert h(b)==r[k+'_sha256']
 shutil.copyfile(path,originals/name)
 receipts.append({'receipt':r,'receipt_sha256':h(path.read_bytes())})
assert static['step_count']==6 and all(r['exact_code']and r['outer_closed']and r['code_fold_closed']and not r['adjacent_copy_or_download_controls']and not r['context_link_in_fold']for r in static['steps'])
assert static['private_T_full_text_exact_in_step6']and static['private_T_provenance_context_has_copy_or_download']is False
assert all(r['candidate_contiguous_text_exact']for r in adj['main_P_folds'])
assert frontier['evidence']['reader_HOLD'] and frontier['status']=='proved_locally'and frontier['owner_id']==request['owner_id_preserve']
plraw=(E/'actual-PROVED_LOCAL-append.exact.jsonl').read_bytes();plevent=json.loads(plraw);capsule=json.loads((E/'local-proof-capsule.json').read_text())
assert plevent['to_state']=='PROVED_LOCAL'and plevent['worker_id']==request['owner_id_preserve']and capsule['owner']==request['owner_id_preserve']
fullboundary={'request_truth_boundary':request['truth_boundary'],'original_frontier_truth_boundary':frontier['truth_boundary'],'original_capsule_truth_boundary':capsule['truth_boundary'],'original_frontier_reader_contract':frontier['reader_contract'],'original_frontier_reader_HOLD':frontier['evidence']['reader_HOLD'],'native_verdict_full':verdict,'native_static_report_full':static,'native_static_adjacency_full':adj}
accept={'actual_verifier':guard.ACTOR,'mathematical_candidate':request['mathematical_candidate'],'metadata_checked_commit':request['metadata_checked_commit'],'final_bounded_review_accepted':True,'normal_API_not_yet_called':True,'actual_native_full_bounded_summary':summary,'native_program_sha256':h((N/'candidate/IndependentInventory.lean').read_bytes()),'actual_native_compile_receipts':receipts,'current_source_audit_matches_original_overlay_and_7_slots':True,'canonical_packet_exact':packet['packet_sha256'],'publication_binding_exact':request['publication_binding_sha256'],'metadata_gate_receipts_full':gates,'candidate_exact_checks':gitrows,'raw_Expr_structural_equality':False,'literal_Prop_defeq':True,'reader_and_global_boundary_full_values':fullboundary,'no_whole_source_DAG_or_live_reader_acceptance':True,'new_mathematical_repair':False}
(P/'final-independent-bounded-preflight.json').write_text(json.dumps(accept,ensure_ascii=False,indent=2)+'\n')
shutil.copyfile(ROOT/paths[7],originals/'own-source-reviewed-audit.before.raw.json');shutil.copyfile(ROOT/paths[8],originals/'own-frontier.before.raw.json')
print(json.dumps({'final_bounded_review':'ACCEPT','normal_API_calls':0,'actual_actor':guard.ACTOR,'checked_math_commit':request['mathematical_candidate'],'checked_metadata_commit':request['metadata_checked_commit'],'native_closed_owned_theorems':4,'literal_raw_signatures_byte_equal':True,'defeq':True,'raw_Expr_equality':False,'public_ASTIS_parents':{'P':[],'T':[producer]},'metadata_gates_at_exact_commit':4,'publication_check_advance_readonly_preflight':'PASS','source_audit_exact_attached':True,'binding_reproduced':True,'reader_HOLD_preserved':True},indent=2))

