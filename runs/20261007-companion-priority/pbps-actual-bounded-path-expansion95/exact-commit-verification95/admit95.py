import pathlib,json,hashlib,subprocess,sys,copy,datetime
R=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent;B=O.parent
ID='ASTIS-SA-20261011-PBPSActualBoundedPathExpansion';ME='/root/independent_whole_math93';D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedPathExpansion.actual_bounded_path_functional_expansion'
CELL=R/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-bounded-path-expansion.json';A=R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualBoundedPathExpansion.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):return {'path':p.relative_to(R).as_posix(),'raw_sha256':sha(p.read_bytes()),'bytes':p.stat().st_size}
def load(p):return json.loads(p.read_bytes())
def save(p,x):
 if (O/p).exists():
  assert load(O/p)==x,'Existing verifier artifact differs: '+p
  return
 with (O/p).open('x',encoding='utf-8',newline='\n') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.write('\n')
def head():return subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()
freeze=load(O/'input-freeze95.json');C=freeze['verified_commit'];checks=load(O/'checks-complete95.json')
assert freeze['status']==checks['status']=='PASS' and checks['verified_commit']==C and head()==C
assert load(O/'all-staged-bytes95.json')['status']=='PASS'
assert load(O/'metadata-transfer95.json')['status']=='PASS'
assert load(O/'source-decoder-bindings95.json')['status']=='PASS'
assert load(O/'final-transfer95.json')['status']=='PASS' and load(O/'final-transfer95.json')['verified_commit']==C
for x in freeze['exact_commit_matches']+freeze['local_pinned_or_excluded_inputs']+freeze['preserved_collaborator_inputs']:
 assert sha((R/x['path']).read_bytes())==x['raw_sha256'],x['path']
sys.path[:0]=[str(R),str(R/'tools')]
from tools.astis_advance import transition_advance,current_advances
before=current_advances();assert before[ID]['state']=='PROVED_LOCAL' and before[ID]['owner_id']!=ME
lane={k:v for k,v in before.items() if v['state']=='STABILIZING'};assert set(lane)=={'ASTIS-SA-20261011-PBPSActualPrescribedPathDensity'}
cell=load(CELL);assert cell['status']=='proved_locally'
(O/'cell.before-admission95.exactraw.json').write_bytes(CELL.read_bytes())
other_cells={p.relative_to(R).as_posix():sha(p.read_bytes()) for p in CELL.parent.glob('*.json') if p!=CELL}
save('other-cells.before-admission95.json',other_cells)
ledger=R/'runs/substantive_advances.jsonl';lb=ledger.read_bytes();save('ledger.before-admission95.json',info(ledger))
audit=load(A);source=load(B/'primary-source95/source-review-decision95.native.json');cov=load(B/'primary-source95/compiled-source-coverage95.native.json')
assert audit['state']==source['source_review']['state']=='accepted' and source['blocking_deltas']==0 and not source['repairs']
assert cov['unmapped_nodes']==cov['unmapped_regions']==0 and len(cov['analytic_binders'])==6
v={'status':'PASS_INDEPENDENT_EXACT_COMMIT_VERIFICATION','verifier_id':ME,'verified_commit':C,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'publication_declarations':[D],'gate':checks,'source_audit':{'state':'accepted','reviewer':source['reviewer'],'independent_from_formalizer':True,'independent_from_decoder':True,'decision':info(B/'primary-source95/source-review-decision95.native.json'),'run':info(B/'primary-source95/source-review-run95.native.json'),'closed_manifest':info(B/'primary-source95/closed-raw-manifest95.native.json'),'source_run_canonical_sha256':audit['source_review']['review_run_sha256'],'reviewer_packet_sha256':audit['source_review']['reviewer_packet_sha256'],'six_analytic_binders':True,'source_nodes':26,'source_edges':52,'five_exposition_regions':True,'coverage':info(B/'primary-source95/compiled-source-coverage95.native.json'),'boundary':source['completion_boundary']},'semantic_roundtrip_audit':audit['id'],'publication_binding_sha256':audit['publication_binding_sha256'],'fake_closure_scan':info(O/'fake-closure.json'),'standard_axioms':['propext','Classical.choice','Quot.sound'],'whole_math':info(B/'independent-whole-math95/whole-math-decision95.native.json'),'exposition':info(O/'exposition95.native.json'),'metadata_transfer':info(O/'metadata-transfer95.json'),'exact_input_freeze':info(O/'input-freeze95.json'),'archives':info(O/'archive-audit95.json'),'all_stage_bytes':info(O/'all-staged-bytes95.json'),'source_decoder_bindings':info(O/'source-decoder-bindings95.json'),'historical_lesson_recovery':info(O/'historical-lesson-recovery95.json'),'all21collaborator_RAWs_preserved':True,'archive_policy':'Original native hashes resolved exactly through committed gzip/plain snapshots. Historical draft lesson/audit recoveries are transparent new archives whose decoded bytes match pre-existing frozen SHA pins, not fabricated historical files. Absolute native paths are provenance resolved by explicit E:/Samplinglib-prefix/backslash normalization and immutable archive lookup in verify_inputs95.py. Public/canonical live references are repository-relative.','truth_boundary':'Complete bounded real coordinate-measurable path-functional countable signed expansion under the six original analytic assumptions, including actual process representative and all degenerate cases. No unbounded-test extension, Skorokhod equivalence, restart/Markovness, invariance, hypocoercivity, paper main/composition, reader visual delivery or whole Goal completion.','remaining':['Sole-lane shared aggregation and full repository gate','Graph/site/reader visual acceptance','Merge and postmerge purification','Remaining PBPS/SPHMC, Gaussian Cloud, midpoint and actual-input composition'],'stabilization':False,'merged':False,'PURIFIED':False,'whole_paper':False,'Goal_complete':False}
save('verified.json',v)
e={k:v[k] for k in ['verifier_id','verified_commit','source_audit','fake_closure_scan','publication_declarations','semantic_roundtrip_audit']};e['gate']=info(O/'verified.json')
transition_advance(ID,'VERIFIED',worker_id=ME,evidence=e)
la=ledger.read_bytes();assert la.startswith(lb) and len(la[len(lb):].splitlines())==1
(O/'verified-ledger-tail95.exactraw.snapshot').write_bytes(la[len(lb):])
new=copy.deepcopy(cell);new['status']='independently_verified';new['evidence']['independent_verification']=(O/'verified.json').relative_to(R).as_posix();CELL.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
after=current_advances();assert after[ID]['state']=='VERIFIED'
assert {k:v for k,v in before.items() if k!=ID}=={k:v for k,v in after.items() if k!=ID}
assert {k:v for k,v in after.items() if v['state']=='STABILIZING'}==lane
assert {p.relative_to(R).as_posix():sha(p.read_bytes()) for p in CELL.parent.glob('*.json') if p!=CELL}==other_cells
for x in freeze['preserved_collaborator_inputs']:assert sha((R/x['path']).read_bytes())==x['raw_sha256']
save('admission95.json',{'state':'VERIFIED','cell_state':'independently_verified','verified_commit':C,'verifier_id':ME,'verified':info(O/'verified.json'),'cell':info(CELL),'ledger':info(ledger),'one_append_only_event':True,'preceding_ledger_RAW_preserved':True,'all_other_advances_and_cells_unchanged':True,'all21collaborator_RAWs_preserved':True,'existing_stabilizing_owners':[{'id':k,'owner':v['owner_id']} for k,v in lane.items()],'production_edits':False,'Goal_complete':False})
argv=[sys.executable,'-X','utf8','tools/astis_frontier_cells.py','check']
p=subprocess.run(argv,cwd=R,capture_output=True);(O/'post-admission-frontier.stdout.log').write_bytes(p.stdout);(O/'post-admission-frontier.stderr.log').write_bytes(p.stderr);save('post-admission-frontier.receipt.json',{'command':argv,'exit_code':p.returncode});assert p.returncode==0 and head()==C
save('closed-RAW-manifest95.json',{'status':'CLOSED_INDEPENDENT_EXACT_SCIENCE_ADMISSION','verified_commit':C,'verifier_id':ME,'checked_science_inputs':freeze['exact_commit_matches'],'local_pinned_or_excluded_inputs':freeze['local_pinned_or_excluded_inputs'],'preserved_collaborator_inputs':freeze['preserved_collaborator_inputs'],'owned_artifacts':[info(p) for p in sorted(O.rglob('*')) if p.is_file()],'self_hash_intentionally_omitted':True,'postscience_changes':'Only independently_verified cell status/evidence and one VERIFIED ledger event. Sole SAU94 stabilization lane unchanged.','main_aggregate_reader_Goal_credit':False})
for p in ['verified.json','admission95.json','closed-RAW-manifest95.json']:print(json.dumps(info(O/p)),flush=True)
