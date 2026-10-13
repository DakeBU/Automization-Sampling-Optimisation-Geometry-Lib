from pathlib import Path
import copy,datetime,hashlib,json,subprocess,sys
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent;C='ad3b80a339bf1cf0dd88685f202632a92eeb0797';ME='/root/independent_whole_math93';ID='ASTIS-SA-20261011-PBPSActualPrescribedPathDensity';D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedPathDensity.actual_prescribed_path_density_rewrite'
CELL=R/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-prescribed-path-density.json';A=R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualPrescribedPathDensity.json';S=B/'primary-source94';W=B/'independent-whole-math94'
sys.path[:0]=[str(R),str(R/'tools')]
from tools.astis_advance import transition_advance,current_advances
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def load(p):return json.loads(p.read_bytes())
def save(n,v):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
def head():return subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()
assert head()==C
checks=load(O/'checks-complete94.json');assert checks['status']=='PASS' and checks['verified_commit']==C
freeze=load(O/'input-freeze94.json')
for x in freeze['exact_commit_matches']+freeze['local_pinned_or_excluded_inputs']+freeze['preserved_collaborator_inputs']:assert sha((R/x['path']).read_bytes())==x['raw_sha256']
before=current_advances();assert before[ID]['state']=='PROVED_LOCAL' and before[ID]['owner_id']!=ME
lane={k:v for k,v in before.items() if v['state']=='STABILIZING'};cell=load(CELL);assert cell['status']=='claimed'
assert cell['evidence']['whole_target_compiled']['raw_sha256']=='60792981d3d2bac30d78a2373f7eed0002def8600e92553e9b5b0c87761599ec'
(O/'cell.before-admission94.exactraw.json').write_bytes(CELL.read_bytes())
other_cells={p.relative_to(R).as_posix():sha(p.read_bytes()) for p in CELL.parent.glob('*.json') if p!=CELL};save('other-cells.before-admission94.json',other_cells)
ledger=R/'runs/substantive_advances.jsonl';lb=ledger.read_bytes();save('ledger.before-admission94.json',info(ledger))
audit=load(A);native=load(S/'source-review-decision94.native.json');assert audit['state']=='accepted' and native['source_review']['state']=='accepted' and not native['blocking_findings']
cov=load(S/'compiled-source-coverage-exposition94.native.json');assert cov['all_selected_source_items_disposed'] and not cov['unmapped_nodes'] and not cov['unmapped_edges'] and not cov['unmapped_source_items']
assert (cov['node_count'],cov['edge_count'],cov['inherited_count'],cov['focused_count'],len(cov['authored_exposition']))==(25,54,55,17,7)
dr=load(R/'runs/semantic-roundtrip/anonymous94/decoder/decoder-report.json');assert dr['access_boundary']['files_read_as_task_input']==['E:/Samplinglib/runs/semantic-roundtrip/anonymous94/input.json'] and not dr['access_boundary']['prior_mathematical_reports_read']
v=dict(status='PASS_INDEPENDENT_EXACT_COMMIT_VERIFICATION',verifier_id=ME,verified_commit=C,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),publication_declarations=[D],gate=checks['receipts'],publication_binding_sha256=audit['publication_binding_sha256'],semantic_roundtrip_audit=audit['id'],source_audit=dict(state='accepted',reviewer=native['reviewer'],independent_from_formalizer=True,independent_from_decoder=True,review_result=info(S/'source-review-decision94.native.json'),review_run=info(S/'review-run94.native.json'),native_manifest=info(S/'closed-RAW-review94.native.json'),reviewer_packet_sha256=audit['source_review']['reviewer_packet_sha256'],review_run_canonical_sha256=audit['source_review']['review_run_sha256'],native_to_canonical_seven_semantic_slots_identical=True,binder_count=6,literal_definition_count=20,body_exposition_regions=7,source_nodes=25,source_edges=54,inherited_dispositions=55,focused_dispositions=17,acceptance_boundary=native['acceptance_boundary']),fake_closure_scan=info(O/'fake-closure-scan94.json'),standard_axioms=['propext','Classical.choice','Quot.sound'],independent_mathematics=info(W/'whole-math-decision94.native.json'),independent_exposition=info(W/'exposition94/exposition-decision94.native.json'),exact_LF_transfer=info(W/'lf-transfer94/LF-transfer-decision94.native.json'),publication_metadata_transfer=info(O/'publication-metadata-transfer94.json'),fresh_exact_sealed_kernel=info(O/'current-sealed-kernel.receipt.json'),fresh_leaf_build=info(O/'focused-module.receipt.json'),exact_science_inputs=info(O/'input-freeze94.json'),lossless_committed_archive_audit=info(O/'archive-audit94.json'),source_decoder_hash_binding=info(O/'source-decoder-bindings94.json'),decoder_full_chain_checked=True,all21collaborator_RAWs_preserved=True,native_review_evidence_lossless_commit_binding=True,archive_count=70,local_source_preread_boundary=freeze['local_pinned_or_excluded_inputs'],control_plane_ledger_binding='Current native ledger including the four SAU94 pre-verification events is preserved exactly in committed runs/substantive_advances.jsonl.gz; the plain science ledger blob retains its earlier prefix. No earlier event is rewritten.',truth_boundary=load(B/'claim.json')['truth_boundary'],remaining=['Sole-lane shared imports/Registry/root Tests and repository aggregate gate','Graph/site/reader delivery and actual visual acceptance','Merge and postmerge purification','Actual finite-count composition TERM93, countable full A7 and signed convergence','Remaining PBPS/SPHMC, Gaussian Cloud, midpoint and four-paper Goal'],stabilization=False,merged=False,PURIFIED=False,full_A7=False,Goal_complete=False)
save('verified.json',v)
e={k:v[k] for k in ['verifier_id','verified_commit','source_audit','fake_closure_scan','publication_declarations','semantic_roundtrip_audit']};e['gate']=info(O/'verified.json')
transition_advance(ID,'VERIFIED',worker_id=ME,evidence=e)
la=ledger.read_bytes();assert la.startswith(lb);tail=la[len(lb):];assert len(tail.splitlines())==1
(O/'verified-ledger-tail94.exactraw.snapshot').write_bytes(tail)
new=copy.deepcopy(cell);new['status']='independently_verified';new['evidence']['independent_verification']=(O/'verified.json').relative_to(R).as_posix()
with CELL.open('w',encoding='utf8',newline='\n') as f:json.dump(new,f,ensure_ascii=False,indent=2);f.write('\n')
after=current_advances();assert after[ID]['state']=='VERIFIED' and {k:v for k,v in before.items() if k!=ID}=={k:v for k,v in after.items() if k!=ID}
assert {k:v for k,v in after.items() if v['state']=='STABILIZING'}==lane
assert {p.relative_to(R).as_posix():sha(p.read_bytes()) for p in CELL.parent.glob('*.json') if p!=CELL}==other_cells
for x in freeze['preserved_collaborator_inputs']:assert sha((R/x['path']).read_bytes())==x['raw_sha256']
save('admission94.json',dict(state='VERIFIED',cell_state='independently_verified',cell_previous_status=cell['status'],stale_cell_status_reconciled_from_authoritative_PROVED_LOCAL=True,verified_commit=C,verifier_id=ME,verified=info(O/'verified.json'),cell=info(CELL),ledger=info(ledger),one_append_only_event=True,preceding_ledger_RAW_preserved=True,all_other_advances_unchanged=True,all_other_frontier_cells_RAW_preserved=True,all21collaborator_RAWs_preserved=True,existing_stabilizing_owners=[dict(id=k,owner=v.get('owner_id')) for k,v in lane.items()],production_edits=False,shared_aggregator_edits=False,stabilization=False,Goal_complete=False))
cmd=[sys.executable,'-X','utf8','tools/astis_frontier_cells.py','check'];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (O/'post-admission-frontier.stdout.log').open('xb') as out,(O/'post-admission-frontier.stderr.log').open('xb') as err:
 p=subprocess.Popen(cmd,cwd=R,stdout=out,stderr=err);code=p.wait()
save('post-admission-frontier.receipt.json',dict(command=cmd,foreground_PID=p.pid,checked_science_commit=C,exit_code=code,terminal_closed=True,started_utc=start,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),stdout=info(O/'post-admission-frontier.stdout.log'),stderr=info(O/'post-admission-frontier.stderr.log')));assert code==0
assert head()==C
for x in freeze['preserved_collaborator_inputs']:assert sha((R/x['path']).read_bytes())==x['raw_sha256']
save('closed-RAW-manifest94.json',dict(status='CLOSED_INDEPENDENT_EXACT_SCIENCE_ADMISSION',verified_commit=C,verifier_id=ME,checked_science_inputs=freeze['exact_commit_matches'],local_pinned_or_excluded_inputs=freeze['local_pinned_or_excluded_inputs'],preserved_collaborator_inputs=freeze['preserved_collaborator_inputs'],owned_artifacts=[info(p) for p in sorted(O.iterdir()) if p.is_file()],self_hash_intentionally_omitted=True,postscience_changes='Only independently_verified cell status/evidence and one legitimate VERIFIED ledger event; input hashes bind named science commit before admission.',source_reviewer_distinct=True,main_aggregate_reader_Goal_credit=False))
for p in [O/'verified.json',O/'admission94.json',O/'closed-RAW-manifest94.json']:print(json.dumps(info(p)),flush=True)
