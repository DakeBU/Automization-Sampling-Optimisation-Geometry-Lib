from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
r=Path(__file__).parent;out=r/'integration84/cell-admission-correction';out.mkdir(exist_ok=False)
load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_sha256=hashlib.sha256(b).hexdigest(),RAW_bytes=len(b))
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
cell=Path('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-outer-bounded-l2-continuity.json')
current=pin(cell);assert current['RAW_sha256']==load(r/'integration84/final-admin.json')['cell_RAW_sha256']
assert load(cell)['status']=='independently_verified'
original=load(r/'integration.notes.json');assert original['science_commit']=='dd3a23011b91569acbcd591ccd7b06301147d339'
assert pin('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualOuterBoundedL2Continuity.lean')['RAW_sha256']=='8fd35db26717f46313fc53dd90691828b11c9d78cdcc4a62f68c8d59273cc2bd'
save(out/'diagnosis.json',dict(classification='CONTROL_PLANE_STAGING_AND_FOCUSED_TARGET_OMISSION',published_integration_commit='5186f92607df617c4e4a8a90d0c5e6b5fc611090',wrong_cell='ASTIS-SW-PBPS-actual-bounded-test-continuity',correct_cell=cell.as_posix(),local_cell_unchanged_since_all_gates=current,math_statement_or_BODY_changed=False,source_or_exposition_changed=False,prior_graph_check_kept_as_wrong_target_history=True,repair='Stage current independently verified84 cell; rerun the correct84 focused graph gate and metadata diff admission; retain all native previous receipts.'))
env=os.environ.copy();env['PYTHONUTF8']='1';env.pop('ELAN_TOOLCHAIN',None);env['PATH']=str(Path('.astis/toolchain/lean-4.33.0-windows/bin').resolve())+os.pathsep+env['PATH']
checks=[]
for label,args in [('correct-cell-graph',['tools/astis_publication.py','graph-check','--cell','ASTIS-SW-PBPS-actual-outer-bounded-l2-continuity']),('metadata-publication',['tools/astis_publication.py','check','--base','5186f92607df617c4e4a8a90d0c5e6b5fc611090']),('metadata-contributor',['tools/astis_contributor_contract.py','check','--base','5186f92607df617c4e4a8a90d0c5e6b5fc611090']),('frontier',['tools/astis_frontier_cells.py','check']),('semantic',['tools/astis_semantic_roundtrip.py','check'])]:
 q=subprocess.run([sys.executable,'-X','utf8',*args],capture_output=True,env=env)
 (out/(label+'.stdout.log')).write_bytes(q.stdout);(out/(label+'.stderr.log')).write_bytes(q.stderr)
 receipt=dict(command=[sys.executable,'-X','utf8',*args],exit_code=q.returncode,terminal_closed=True,stdout=pin(out/(label+'.stdout.log')),stderr=pin(out/(label+'.stderr.log')))
 save(out/(label+'.receipt.json'),receipt);assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace')[-6000:];checks.append(dict(label=label,receipt=pin(out/(label+'.receipt.json'))))
assert pin(cell)==current
sys.path.insert(0,str(Path.cwd()/'tools'));sys.path.insert(0,str(Path.cwd()/'website/scripts'))
import astis_site,publication_reader
assert load('.astis/site-lean-gate.json')['source_digest']==astis_site.source_digest()
assert load('_site/data/underlying-lean-graph.json')['publication_inputs_sha256']==publication_reader.graph_input_digest()
assert pin('_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html')['RAW_sha256']==load(r/'integration84/offline-reader.json')['page_RAW_sha256']
note=dict(original);note['status']='LOCAL_SHARED_AGGREGATE_AND_GENERATED_READER_GATES_PASS_CORRECT84_GRAPH_VISUAL_PENDING'
note['prior_integration_note']=pin(r/'integration.notes.json');note['control_plane_correction']=pin(out/'diagnosis.json');note['additional_checks']=checks
note['checks']=[x for x in original['checks'] if x['label']!='graph-check']+[dict(label='graph-check-correct84',receipt=pin(out/'correct-cell-graph.receipt.json'))]
note['reused_same_local_source_evidence']='Root/Tests/check/pycompile/site-build/site-check/underlying graph/full-base publication and HTML/SVG receipts apply to the exact same local Lean, cell, publication, generated graph and HTML bytes. Only previously omitted Git staging and the mistaken focused graph target are repaired.'
save(r/'integration.corrected.notes.json',note)
p=Path('docs/companion-papers-handoff.md');b=p.read_bytes();old=b'/graph checks are bound in84 integration.notes.json.';assert b.count(old)==1
p.write_bytes(b.replace(old,b'/graph checks are bound in84 integration.corrected.notes.json.',1))
print('Correct84 graph and metadata admission PASS; same local source/site evidence retained; correct cell ready to stage')
