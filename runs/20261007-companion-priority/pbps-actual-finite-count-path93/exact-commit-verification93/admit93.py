from pathlib import Path
import copy,datetime,hashlib,json,subprocess,sys
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent
C='8ec33d055fb8a9b3ba376d4113e388b00882026f';ME='/root/independent_whole_math93';ID='ASTIS-SA-20261011-PBPSActualFiniteCountPath';D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteCountPath.actual_finite_count_path_law'
CELL=R/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-finite-count-path.json';A=R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualFiniteCountPath.json';S=B/'primary-source93/scoped-transfer93'
sys.path[:0]=[str(R),str(R/'tools')]
from tools.astis_advance import transition_advance,current_advances
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def load(p):return json.loads(p.read_bytes())
def save(n,v):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
def head():return subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()
assert head()==C
checks=load(O/'checks-complete93.json');assert checks['status']=='PASS' and checks['verified_commit']==C
freeze=load(O/'input-freeze93.json')
for x in freeze['exact_commit_matches']+freeze['local_pinned_or_excluded_inputs']+freeze['all21collaborator_RAWs']:assert sha((R/x['path']).read_bytes())==x['raw_sha256']
before=current_advances();assert before[ID]['state']=='PROVED_LOCAL' and before[ID]['owner_id']!=ME
lane={k:v for k,v in before.items() if v['state']=='STABILIZING'}
cell=load(CELL);assert cell['status']=='proved_locally'
(O/'cell.before-independent-admission93.exactraw.json').write_bytes(CELL.read_bytes())
other_cells={p.relative_to(R).as_posix():sha(p.read_bytes()) for p in CELL.parent.glob('*.json') if p!=CELL};save('other-cells.before-admission93.json',other_cells)
ledger=R/'runs/substantive_advances.jsonl';lb=ledger.read_bytes();save('ledger.before-admission93.json',info(ledger))
audit=load(A);native=load(S/'source-review-decision93.native.json');assert audit['state']=='accepted' and native['source_review_status']=='accepted' and not native['blocking_findings']
cov=load(S/'compiled-source-coverage-exposition93.native.json');assert cov['all_regions_exact'] and len(cov['exposition_regions'])==9
v=dict(status='PASS_INDEPENDENT_EXACT_COMMIT_VERIFICATION',verifier_id=ME,verified_commit=C,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),publication_declarations=[D],gate=checks['receipts'],publication_binding_sha256=audit['publication_binding_sha256'],semantic_roundtrip_audit=audit['id'],source_audit=dict(state='accepted',reviewer=native['reviewer'],review_result=info(S/'source-review-decision93.native.json'),review_run=info(S/'review-run93.native.json'),native_manifest=info(S/'closed-RAW-transfer93.native.json'),reviewer_packet_sha256=audit['source_review']['reviewer_packet_sha256'],review_run_canonical_sha256=audit['source_review']['review_run_sha256'],native_to_canonical_seven_semantic_slots_identical=True,binder_count=6,literal_definition_count=36,body_exposition_regions=9,source_nodes=35,source_edges=94,source_dispositions=55,acceptance_scope=native['nonclaims']),fake_closure_scan=info(O/'fake-closure-scan93.json'),standard_axioms=['propext','Classical.choice','Quot.sound'],independent_mathematics=info(B/'independent-whole-math93/whole-math-decision93.native.json'),reviewed_implementation_delta_chain=[info(B/'independent-whole-math93/scoped-classical93/scoped-classical-transfer93.native.json')],exposition=info(S/'compiled-source-coverage-exposition93.native.json'),fresh_exact_commit_kernel=info(O/'current-kernel.receipt.json'),fresh_leaf_build=info(O/'focused-module.receipt.json'),exact_science_inputs=info(O/'input-freeze93.json'),lossless_committed_archive_audit=info(O/'archive-audit93.json'),blind_decoder_binding=info(O/'decoder-binding93.json'),source_native_hash_binding=info(O/'source-binding93.json'),decoder_full_chain_checked=True,all21collaborator_RAWs_preserved=True,production_or_shared_aggregator_edits=False,historical_reference_resolution='Exact historical RAW recovered from immutable committed gzip or committed plain RAW snapshots, never waived or replaced by normalized public text.',native_review_evidence_lossless_commit_binding=True,truth_boundary=load(B/'claim.json')['truth_boundary'],remaining=['Serialized shared imports/Registry/root Tests and full repository aggregate gate','Graph/site/reader integration, actual visual/live verification and merge','Postmerge purification and Exposition Seal','Hazard stitching, left limits, full countable A7 assembly, restart/Markovness, main/composition/full papers and four-paper Goal'],stabilization=False,main_or_aggregate_or_reader_complete=False,PURIFIED=False,Goal_complete=False)
save('verified.json',v)
e={k:v[k] for k in ['verifier_id','verified_commit','source_audit','fake_closure_scan','publication_declarations','semantic_roundtrip_audit']};e['gate']=info(O/'verified.json')
transition_advance(ID,'VERIFIED',worker_id=ME,evidence=e)
la=ledger.read_bytes();assert la.startswith(lb);tail=la[len(lb):];assert len(tail.splitlines())==1
(O/'verified-ledger-tail93.original.exactraw.snapshot').write_bytes(tail)
normalized=tail.replace(b'\r\n',b'\n')
if normalized!=tail:ledger.write_bytes(lb+normalized)
assert ledger.read_bytes().startswith(lb)
new=copy.deepcopy(cell);new['status']='independently_verified';new['evidence']['independent_verification']=(O/'verified.json').relative_to(R).as_posix()
with CELL.open('w',encoding='utf8',newline='\n') as f:json.dump(new,f,ensure_ascii=False,indent=2);f.write('\n')
after=current_advances();assert after[ID]['state']=='VERIFIED' and {k:v for k,v in before.items() if k!=ID}=={k:v for k,v in after.items() if k!=ID}
assert {k:v for k,v in after.items() if v['state']=='STABILIZING'}==lane
assert {p.relative_to(R).as_posix():sha(p.read_bytes()) for p in CELL.parent.glob('*.json') if p!=CELL}==other_cells
for x in freeze['all21collaborator_RAWs']:assert sha((R/x['path']).read_bytes())==x['raw_sha256']
save('admission93.json',dict(state='VERIFIED',cell_state='independently_verified',verified_commit=C,verifier_id=ME,verified=info(O/'verified.json'),cell=info(CELL),ledger=info(ledger),one_append_only_event=True,preceding_ledger_RAW_preserved=True,new_owned_tail_only_normalized=tail!=normalized,all_other_advances_unchanged=True,all_other_frontier_cells_RAW_preserved=True,all21collaborator_RAWs_preserved=True,existing_stabilizing_owners=[dict(id=k,owner=v.get('owner_id')) for k,v in lane.items()],production_edits=False,shared_aggregator_edits=False,stabilization=False,Goal_complete=False))
cmd=[sys.executable,'-X','utf8','tools/astis_frontier_cells.py','check'];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (O/'post-admission-frontier.stdout.log').open('xb') as out,(O/'post-admission-frontier.stderr.log').open('xb') as err:
 p=subprocess.Popen(cmd,cwd=R,stdout=out,stderr=err);code=p.wait()
save('post-admission-frontier.receipt.json',dict(command=cmd,foreground_PID=p.pid,checked_science_commit=C,exit_code=code,terminal_closed=True,started_utc=start,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),stdout=info(O/'post-admission-frontier.stdout.log'),stderr=info(O/'post-admission-frontier.stderr.log')));assert code==0
assert head()==C
for x in freeze['all21collaborator_RAWs']:assert sha((R/x['path']).read_bytes())==x['raw_sha256']
save('closed-RAW-manifest93.json',dict(status='CLOSED_INDEPENDENT_EXACT_SCIENCE_ADMISSION',verified_commit=C,verifier_id=ME,checked_science_inputs=freeze['exact_commit_matches'],local_pinned_or_excluded_inputs=freeze['local_pinned_or_excluded_inputs'],preserved_collaborator_inputs=freeze['all21collaborator_RAWs'],owned_artifacts=[info(p) for p in sorted(O.iterdir()) if p.is_file()],self_hash_intentionally_omitted=True,postscience_changes='Only independently_verified cell status/evidence and one legitimate VERIFIED ledger event; input hashes bind named science commit before admission.',source_reviewer_distinct=True,main_aggregate_reader_Goal_credit=False))
for p in [O/'verified.json',O/'admission93.json',O/'closed-RAW-manifest93.json']:print(json.dumps(info(p)),flush=True)
