from pathlib import Path
import hashlib,json,subprocess,sys
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_publication as pub
r=Path(__file__).parent;p=Path('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-small-time-continuity.json');x=json.loads(p.read_bytes())
assert x['status']=='proved_locally' and x['graph_contribution']['lean_view']=='theorem-edge'
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
before=hashlib.sha256(p.read_bytes()).hexdigest();x['graph_contribution']['lean_view']='new-node'
p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
pub.check_advance(x['source_targets'],reviewed=True)
record=r/'graph-view-schema-diagnosis82.json';record.write_text(json.dumps(dict(failure_class='CONTROL_PLANE_GRAPH_VIEW_ENUM',failed_science_commit='396c13491e5a9bdf0abcd5d7fb00c1fb8ef97fcc',native_negative='exact-commit-verification82/contributor.receipt.json',field='graph_contribution.lean_view',before='theorem-edge',after='new-node',cause='theorem-edge is SAU result_kind; graph contribution vocabulary is new-node/reuse-only/integration-node.',cell_before_RAW=before,cell_after_RAW=hashlib.sha256(p.read_bytes()).hexdigest(),statement_BODY_and_source_publication_binding_unchanged=True,VERIFIED=False),indent=2)+'\n',encoding='utf8',newline='\n')
subprocess.run(['git','-c','core.autocrlf=false','add','--',p.as_posix(),record.as_posix(),Path(__file__).as_posix()],check=True)
subprocess.run(['git','diff','--cached','--check'],check=True)
subprocess.run(['git','commit','-q','-m','Correct actual PBPS continuity graph contribution view metadata'],check=True)
print('SCIENCE_METADATA_SUCCESSOR',subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip())
