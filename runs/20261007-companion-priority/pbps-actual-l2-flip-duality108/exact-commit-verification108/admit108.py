from context108 import *
import datetime,os
ID='ASTIS-SA-20261012-PBPSActualL2FlipDuality';ME='/root/exact_verifier96'
assert head()==C and not git('diff','--cached','--name-only').strip()
freeze=load(O/'input-freeze108.json');checks=load(O/'checks-complete108.json');source=load(O/'source-acceptance108.native.json')
for x in [freeze,checks,source,load(O/'science-scope108.json'),load(O/'kernel-transfer108.json'),load(O/'metadata-transfer108.json'),load(O/'primary-scope108.native.json'),load(O/'canonical-ledger-delivery108.native.json')]:assert x['status']=='PASS' and x['verified_commit']==C
for x in freeze['exact_commit_matches']+freeze['local_pinned_or_excluded_inputs']+freeze['preserved_collaborator_inputs']:assert info(x['path'])['raw_sha256']==x['raw_sha256'],x['path']
for x in load(B/'independent-whole-math108/prepared-inputs108.native.json')['inputs']:assert info(x['path'])['raw_sha256']==x['raw_sha256'],x['path']
sys.path[:0]=[str(R),str(R/'tools')]
from tools.astis_advance import transition_advance,current_advances
from tools import astis_publication as pub
pub.check_advance([D],reviewed=True)
before=current_advances();assert before[ID]['state']=='PROVED_LOCAL' and before[ID]['owner_id']!=ME
lane={k:v for k,v in before.items() if v['state']=='STABILIZING'};assert set(lane)=={'ASTIS-SA-20261011-PBPSActualPrescribedPathDensity'}
cp=R/CELL;cell=load(cp);assert cell['status']=='proved_locally'
assert cell['cell_id']=='ASTIS-SW-PBPS-actual-l2-flip-duality' and cell['target_declarations']==[D]
assert before[ID]['owner_id']=='companion_root_20261005' and cell['evidence']['owner']=='companion_root_20261005'
(O/'cell.before-admission108.exactraw.json').write_bytes(cp.read_bytes())
other={rel(p):sha(p.read_bytes()) for p in cp.parent.glob('*.json') if p!=cp};save('other-cells.before-admission108.json',other)
ledger=R/'runs/substantive_advances.jsonl';lb=ledger.read_bytes();assert lb==git('show',C+':runs/substantive_advances.jsonl');save('ledger.before-admission108.json',info(ledger))
audit=load(A);assert audit['state']==audit['source_review']['state']=='accepted'
v=dict(status='PASS_INDEPENDENT_EXACT_COMMIT_VERIFICATION',verifier_id=ME,verified_commit=C,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),publication_declarations=[D],gate=checks,source_audit=source,semantic_roundtrip_audit=audit['id'],publication_binding_sha256=audit['publication_binding_sha256'],fake_closure_scan=info(O/'fake-closure108.json'),axiom_scan=info(O/'axiom-scan108.json'),whole_math=info(B/'independent-whole-math108/whole-math-decision108.native.json'),exact_input_freeze=info(O/'input-freeze108.json'),archives=info(O/'archive-audit108.json'),canonical_ledger_delivery=info(O/'canonical-ledger-delivery108.native.json'),science_scope=info(O/'science-scope108.json'),kernel_transfer=info(O/'kernel-transfer108.json'),all21collaborator_RAWs_preserved=True,canonical_source_transfer='Seven slots, deltas, verdict, repairs transfer exactly; source_review differs only in evidence path with native prose retained.',archive_policy='Original RAW bytes recovered from exact Git blobs or committed lossless gzip/plain snapshots; fixed config newline equivalence and pinned runtime/library/primary exclusions explicit.',truth_boundary='Same global actual PBPS Z and same real L2 family supplied once by107; actual momentum flip preserves literal phase nu; canonical L2 pullback J is isometric and involutive, and each A(T).adjoint=J composed A(T) composed J. Exactly original six analytic hypotheses and one direct public producer107. No time continuity, semigroup/restart/Markovness or complete-paper claim.',remaining=['Sole SAU94 aggregate repository/build/graph/site checks and reader delivery','Main merge and postmerge purification with Exposition Seal remain separate','Restart/Markovness, remaining paper results and actual-input composition'],stabilization=False,merged=False,PURIFIED=False,whole_paper=False,Goal_complete=False,new_full_primary_archive=False)
save('verified.json',v)
e={k:v[k] for k in ['verifier_id','verified_commit','source_audit','fake_closure_scan','publication_declarations','semantic_roundtrip_audit']};e['gate']=info(O/'verified.json')
transition_advance(ID,'VERIFIED',worker_id=ME,evidence=e)
la=ledger.read_bytes();assert la.startswith(lb) and len(la[len(lb):].splitlines())==1
(O/'verified-ledger-tail108.exactraw.snapshot').write_bytes(la[len(lb):])
subprocess.run([sys.executable,'-X','utf8',str(O/'normalize_owned_verified_tail108.py'),'--after-native-VERIFIED'],cwd=R,check=True)
assert ledger.read_bytes().startswith(lb) and ledger.read_bytes().splitlines()==la.splitlines()
new=copy.deepcopy(cell);new['status']='independently_verified';new['evidence']['independent_verification']=rel(O/'verified.json');cp.write_bytes((json.dumps(new,ensure_ascii=False,indent=2)+'\n').encode())
after=current_advances();assert after[ID]['state']=='VERIFIED'
assert {k:v for k,v in before.items() if k!=ID}=={k:v for k,v in after.items() if k!=ID}
assert {k:v for k,v in after.items() if v['state']=='STABILIZING'}==lane
assert {rel(p):sha(p.read_bytes()) for p in cp.parent.glob('*.json') if p!=cp}==other
for x in freeze['preserved_collaborator_inputs']:assert info(x['path'])['raw_sha256']==x['raw_sha256']
for x in freeze['exact_commit_matches']:
 if x['path'] not in [CELL,'runs/substantive_advances.jsonl']:assert info(x['path'])['raw_sha256']==x['raw_sha256'],x['path']
save('admission108.json',dict(state='VERIFIED',cell_state='independently_verified',verified_commit=C,verifier_id=ME,verified=info(O/'verified.json'),cell=info(cp),ledger=info(ledger),one_append_only_event=True,preceding_ledger_RAW_preserved=True,all_other_advances_and_cells_unchanged=True,all21collaborator_RAWs_preserved=True,existing_stabilizing_owners=[dict(id=k,owner=v['owner_id']) for k,v in lane.items()],production_edits=False,owned_tail_EOL_transfer=info(O/'owned-VERIFIED-tail-EOL108.native.json'),final_canonical_ledger_bound=True,Goal_complete=False))
env=os.environ.copy();env['PYTHONUTF8']='1'
argv=[sys.executable,'-X','utf8','tools/astis_frontier_cells.py','check'];p=subprocess.run(argv,cwd=R,capture_output=True,env=env)
(O/'post-admission-frontier.stdout.log').write_bytes(p.stdout);(O/'post-admission-frontier.stderr.log').write_bytes(p.stderr);save('post-admission-frontier.receipt.json',dict(command=argv,exit_code=p.returncode));assert p.returncode==0 and head()==C
save('closed-RAW-manifest108.json',dict(status='CLOSED_INDEPENDENT_EXACT_SCIENCE_ADMISSION',verified_commit=C,verifier_id=ME,checked_science_inputs=freeze['exact_commit_matches'],local_pinned_or_excluded_inputs=freeze['local_pinned_or_excluded_inputs'],preserved_collaborator_inputs=freeze['preserved_collaborator_inputs'],owned_artifacts=[info(p) for p in sorted(O.rglob('*')) if p.is_file() and '__pycache__' not in p.parts],self_hash_intentionally_omitted=True,postscience_changes='Only SAU108 cell independently_verified status/evidence and one native VERIFIED ledger event; only that new tail EOL normalized with lossless original archive before native closure; all other advances/cells and sole SAU94 stabilization lane preserved.',main_aggregate_reader_Goal_credit=False))
for n in ['verified.json','admission108.json','closed-RAW-manifest108.json']:print(json.dumps(info(O/n)),flush=True)
