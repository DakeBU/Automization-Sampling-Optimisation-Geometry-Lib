from verify102 import *
import datetime,os
ID='ASTIS-SA-20261012-PBPSActualWeightedSector';ME='/root/exact_verifier96'
assert head()==C and not git('diff','--cached','--name-only').strip()
freeze=load(O/'input-freeze102.json');checks=load(O/'checks-complete102.json');source=load(O/'source-acceptance102.native.json')
for x in [freeze,checks,source,load(O/'science-scope102.json'),load(O/'kernel-transfer102.json'),load(O/'metadata-transfer102.json'),load(O/'primary-scope102.native.json')]:assert x['status']=='PASS' and x['verified_commit']==C
for x in freeze['exact_commit_matches']+freeze['local_pinned_or_excluded_inputs']+freeze['preserved_collaborator_inputs']:assert info(x['path'])['raw_sha256']==x['raw_sha256'],x['path']
for x in load(B/'independent-whole-math102/prepared-inputs102.native.json')['inputs']:assert info(x['path'])['raw_sha256']==x['raw_sha256'],x['path']
sys.path[:0]=[str(R),str(R/'tools')]
from tools.astis_advance import transition_advance,current_advances
from tools import astis_publication as pub
pub.check_advance([D],reviewed=True)
before=current_advances();assert before[ID]['state']=='PROVED_LOCAL' and before[ID]['owner_id']!=ME
lane={k:v for k,v in before.items() if v['state']=='STABILIZING'};assert set(lane)=={'ASTIS-SA-20261011-PBPSActualPrescribedPathDensity'}
cp=R/CELL;cell=load(cp);assert cell['status']=='proved_locally'
(O/'cell.before-admission102.exactraw.json').write_bytes(cp.read_bytes())
other={rel(p):sha(p.read_bytes()) for p in cp.parent.glob('*.json') if p!=cp};save('other-cells.before-admission102.json',other)
ledger=R/'runs/substantive_advances.jsonl';lb=ledger.read_bytes();save('ledger.before-admission102.json',info(ledger))
audit=load(A);assert audit['state']==audit['source_review']['state']=='accepted'
v=dict(status='PASS_INDEPENDENT_EXACT_COMMIT_VERIFICATION',verifier_id=ME,verified_commit=C,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),publication_declarations=[D],gate=checks,source_audit=source,semantic_roundtrip_audit=audit['id'],publication_binding_sha256=audit['publication_binding_sha256'],fake_closure_scan=info(O/'fake-closure102.json'),axiom_scan=info(O/'axiom-scan102.json'),whole_math=info(B/'independent-whole-math102/whole-math-decision102.native.json'),exact_input_freeze=info(O/'input-freeze102.json'),archives=info(O/'archive-audit102.json'),science_scope=info(O/'science-scope102.json'),kernel_transfer=info(O/'kernel-transfer102.json'),all21collaborator_RAWs_preserved=True,inherited_storage_transfer=info(O/'inherited-storage-transfer102.native.json'),source_schema_adapter=info(B/'source-schema-adapter102/source-delta-schema-adapter102.native.json'),canonical_source_transfer='Seven slots, verdict, repairs and source_review transfer exactly apart from the evidence path with native prose retained. Three deltas use the exact separately reviewer-authored informational schema adapter; underlying evidence, scope and nonblocking judgments unchanged.',archive_policy='Original RAW bytes recovered from exact Git blobs or committed lossless gzip/plain snapshots; fixed config newline equivalence and pinned runtime/library/primary exclusions explicit.',truth_boundary='Actual unnormalized fixed-n weighted-sector ENNReal integral substitution under one actual endpoint/time reversal rho, for every measurable phase-times-Prefix test. Exact six original sampler hypotheses and literal actual q times terminal survival; parents93/97/101 supply joint density measurability, phase-first base measure preservation and pointwise weighted balance. Includes n0,T0,rank0,zero weights and infinite tests/integrals. No normalized stationary probability or countable/signed sector assembly claim.',remaining=['Sole SAU94 stabilization: aggregate repository/build/graph/site checks and reader delivery','Merge and postmerge purification with exposition seal','Normalization, countable and signed sector assembly, stationary averaging/invariance, remaining paper results and actual-input composition'],stabilization=False,merged=False,PURIFIED=False,whole_paper=False,Goal_complete=False,new_full_primary_archive=False)
save('verified.json',v)
e={k:v[k] for k in ['verifier_id','verified_commit','source_audit','fake_closure_scan','publication_declarations','semantic_roundtrip_audit']};e['gate']=info(O/'verified.json')
transition_advance(ID,'VERIFIED',worker_id=ME,evidence=e)
la=ledger.read_bytes();assert la.startswith(lb) and len(la[len(lb):].splitlines())==1
(O/'verified-ledger-tail102.exactraw.snapshot').write_bytes(la[len(lb):])
new=copy.deepcopy(cell);new['status']='independently_verified';new['evidence']['independent_verification']=rel(O/'verified.json');cp.write_bytes((json.dumps(new,ensure_ascii=False,indent=2)+'\n').encode())
after=current_advances();assert after[ID]['state']=='VERIFIED'
assert {k:v for k,v in before.items() if k!=ID}=={k:v for k,v in after.items() if k!=ID}
assert {k:v for k,v in after.items() if v['state']=='STABILIZING'}==lane
assert {rel(p):sha(p.read_bytes()) for p in cp.parent.glob('*.json') if p!=cp}==other
for x in freeze['preserved_collaborator_inputs']:assert info(x['path'])['raw_sha256']==x['raw_sha256']
for x in freeze['exact_commit_matches']:
 if x['path'] not in [CELL,'runs/substantive_advances.jsonl']:assert info(x['path'])['raw_sha256']==x['raw_sha256'],x['path']
save('admission102.json',dict(state='VERIFIED',cell_state='independently_verified',verified_commit=C,verifier_id=ME,verified=info(O/'verified.json'),cell=info(cp),ledger=info(ledger),one_append_only_event=True,preceding_ledger_RAW_preserved=True,all_other_advances_and_cells_unchanged=True,all21collaborator_RAWs_preserved=True,existing_stabilizing_owners=[dict(id=k,owner=v['owner_id']) for k,v in lane.items()],production_edits=False,Goal_complete=False))
env=os.environ.copy();env['PYTHONUTF8']='1'
argv=[sys.executable,'-X','utf8','tools/astis_frontier_cells.py','check'];p=subprocess.run(argv,cwd=R,capture_output=True,env=env)
(O/'post-admission-frontier.stdout.log').write_bytes(p.stdout);(O/'post-admission-frontier.stderr.log').write_bytes(p.stderr);save('post-admission-frontier.receipt.json',dict(command=argv,exit_code=p.returncode));assert p.returncode==0 and head()==C
save('closed-RAW-manifest102.json',dict(status='CLOSED_INDEPENDENT_EXACT_SCIENCE_ADMISSION',verified_commit=C,verifier_id=ME,checked_science_inputs=freeze['exact_commit_matches'],local_pinned_or_excluded_inputs=freeze['local_pinned_or_excluded_inputs'],preserved_collaborator_inputs=freeze['preserved_collaborator_inputs'],owned_artifacts=[info(p) for p in sorted(O.rglob('*')) if p.is_file() and '__pycache__' not in p.parts],self_hash_intentionally_omitted=True,postscience_changes='Only SAU102 cell independently_verified status/evidence and one native VERIFIED ledger event; all other advances/cells and sole SAU94 stabilization lane preserved.',main_aggregate_reader_Goal_credit=False))
for n in ['verified.json','admission102.json','closed-RAW-manifest102.json']:print(json.dumps(info(O/n)),flush=True)
