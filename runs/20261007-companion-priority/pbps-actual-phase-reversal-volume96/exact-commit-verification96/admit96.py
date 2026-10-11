"""Independent exact-commit admission only after all closed checks pass."""
from pathlib import Path
import hashlib,json,subprocess,sys,copy,datetime
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent
C=sys.argv[1];ID='ASTIS-SA-20261011-PBPSActualPhaseReversalVolume';ME='/root/exact_verifier96'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseReversalVolume.actual_phase_reversal_volume_laws'
CELL=R/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-phase-reversal-volume.json'
sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(p.read_bytes())
def info(p):return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def save(n,v):
 p=O/n;assert not p.exists(),str(p);p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
def head():return subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()
assert head()==C and not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=R).strip()
freeze=load(O/'input-freeze96.json');checks=load(O/'checks-complete96.json');source=load(O/'source-acceptance96.native.json')
for x in [freeze,checks,source,load(O/'science-scope96.json'),load(O/'metadata-transfer96.json')]:assert x['status']=='PASS' and x['verified_commit']==C
for x in freeze['exact_commit_matches']+freeze['local_pinned_or_excluded_inputs']+freeze['preserved_collaborator_inputs']:
 assert sha((R/x['path']).read_bytes())==x['raw_sha256'],x['path']
sys.path[:0]=[str(R),str(R/'tools')]
from tools.astis_advance import transition_advance,current_advances
before=current_advances();assert before[ID]['state']=='PROVED_LOCAL' and before[ID]['owner_id']!=ME
lane={k:v for k,v in before.items() if v['state']=='STABILIZING'}
assert set(lane)=={'ASTIS-SA-20261011-PBPSActualPrescribedPathDensity'}
cell=load(CELL);assert cell['status']=='proved_locally'
(O/'cell.before-admission96.exactraw.json').write_bytes(CELL.read_bytes())
other={p.relative_to(R).as_posix():sha(p.read_bytes()) for p in CELL.parent.glob('*.json') if p!=CELL};save('other-cells.before-admission96.json',other)
ledger=R/'runs/substantive_advances.jsonl';lb=ledger.read_bytes();save('ledger.before-admission96.json',info(ledger))
audit=load(R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualPhaseReversalVolume.json')
assert audit['state']==audit['source_review']['state']=='accepted'
v=dict(status='PASS_INDEPENDENT_EXACT_COMMIT_VERIFICATION',verifier_id=ME,verified_commit=C,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),publication_declarations=[D],gate=checks,source_audit=source,semantic_roundtrip_audit=audit['id'],publication_binding_sha256=audit['publication_binding_sha256'],fake_closure_scan=info(O/'fake-closure.json'),axiom_scan=info(O/'axiom-scan96.json'),whole_math=info(B/'independent-whole-math96/whole-math-decision96.native.json'),exposition=info(B/'independent-whole-math96/exposition96/exposition-decision96.native.json'),exact_input_freeze=info(O/'input-freeze96.json'),archives=info(O/'archive-audit96.json'),source_decoder_bindings=info(O/'source-decoder-bindings96.json'),all21collaborator_RAWs_preserved=True,archive_policy='Original RAW hashes resolve through exact Git blobs or lossless committed gzip/plain snapshots; fixed tool/config newline equivalence and local primary/library exclusions are explicit. Final source-run hash is SHA256 of exact native bytes. Coverage-only publication metadata transfer is checked against preserved reviewed publication and unchanged current binding.',truth_boundary='Actual harmonic flow, zero-safe bounce and momentum reversal preserve canonical phase product volume; joint Borel, inverse, reversal, rate and real-integrable A6 laws under the original six analytic assumptions. Includes rank zero, zero normals, all real times. No finite prescribed-path reversal, Gibbs cocycle, stationary law, semigroup, hypocoercivity, full paper or composition claim.',remaining=['Sole SAU94 lane aggregate repository/build/graph/site gates','Rendered reader and fine-branch visual acceptance','Merge and postmerge purification','Remaining four-paper results and actual-input composition'],stabilization=False,merged=False,PURIFIED=False,whole_paper=False,Goal_complete=False)
v.update(metadata_transfer=info(O/'metadata-transfer96.json'),all_scoped_git_blobs=info(O/'science-scope96.json'),original_kernel_execution_commit='949bd4cb5e780c590055aefe327358d7ffe8f2e8',kernel_transfer_reason='Only exact two-file reuse-parent metadata repair; every prior science input except that mechanically checked cell metadata remains RAW-identical.')
save('verified.json',v)
e={k:v[k] for k in ['verifier_id','verified_commit','source_audit','fake_closure_scan','publication_declarations','semantic_roundtrip_audit']};e['gate']=info(O/'verified.json')
transition_advance(ID,'VERIFIED',worker_id=ME,evidence=e)
la=ledger.read_bytes();assert la.startswith(lb) and len(la[len(lb):].splitlines())==1
(O/'verified-ledger-tail96.exactraw.snapshot').write_bytes(la[len(lb):])
new=copy.deepcopy(cell);new['status']='independently_verified';new['evidence']['independent_verification']=(O/'verified.json').relative_to(R).as_posix();CELL.write_bytes((json.dumps(new,ensure_ascii=False,indent=2)+'\n').encode())
after=current_advances();assert after[ID]['state']=='VERIFIED'
assert {k:v for k,v in before.items() if k!=ID}=={k:v for k,v in after.items() if k!=ID}
assert {k:v for k,v in after.items() if v['state']=='STABILIZING'}==lane
assert {p.relative_to(R).as_posix():sha(p.read_bytes()) for p in CELL.parent.glob('*.json') if p!=CELL}==other
for x in freeze['preserved_collaborator_inputs']:assert sha((R/x['path']).read_bytes())==x['raw_sha256']
save('admission96.json',dict(state='VERIFIED',cell_state='independently_verified',verified_commit=C,verifier_id=ME,verified=info(O/'verified.json'),cell=info(CELL),ledger=info(ledger),one_append_only_event=True,preceding_ledger_RAW_preserved=True,all_other_advances_and_cells_unchanged=True,all21collaborator_RAWs_preserved=True,existing_stabilizing_owners=[dict(id=k,owner=v['owner_id']) for k,v in lane.items()],production_edits=False,Goal_complete=False))
argv=[sys.executable,'-X','utf8','tools/astis_frontier_cells.py','check'];p=subprocess.run(argv,cwd=R,capture_output=True)
(O/'post-admission-frontier.stdout.log').write_bytes(p.stdout);(O/'post-admission-frontier.stderr.log').write_bytes(p.stderr);save('post-admission-frontier.receipt.json',dict(command=argv,exit_code=p.returncode));assert p.returncode==0 and head()==C
save('closed-RAW-manifest96.json',dict(status='CLOSED_INDEPENDENT_EXACT_SCIENCE_ADMISSION',verified_commit=C,verifier_id=ME,checked_science_inputs=freeze['exact_commit_matches'],local_pinned_or_excluded_inputs=freeze['local_pinned_or_excluded_inputs'],preserved_collaborator_inputs=freeze['preserved_collaborator_inputs'],owned_artifacts=[info(p) for p in sorted(O.rglob('*')) if p.is_file() and '__pycache__' not in p.parts],self_hash_intentionally_omitted=True,postscience_changes='Only independently_verified cell status/evidence and one VERIFIED ledger event; sole SAU94 stabilization lane unchanged.',main_aggregate_reader_Goal_credit=False))
for name in ['verified.json','admission96.json','closed-RAW-manifest96.json']:print(json.dumps(info(O/name)),flush=True)
