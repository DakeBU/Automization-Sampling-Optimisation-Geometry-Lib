from pathlib import Path
import json,hashlib,subprocess,datetime
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-outer-bounded-l2-continuity84';O=Path(__file__).parent
C='5186f92607df617c4e4a8a90d0c5e6b5fc611090';D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOuterBoundedL2Continuity.actual_outer_bounded_l2_continuity'
def info(p):
 p=Path(p);p=p if p.is_absolute() else R/p;b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),RAW_sha256=hashlib.sha256(b).hexdigest(),RAW_bytes=len(b))
def load(p):return json.loads(Path(p).read_bytes())
def save(n,d):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
def blob(p):return subprocess.check_output(['git','show',C+':'+Path(p).relative_to(R).as_posix()],cwd=R)
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==C
cell=R/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-outer-bounded-l2-continuity.json';old=load_bytes=json.loads(blob(cell));cur=load(cell)
assert old['status']=='proved_locally' and cur['status']=='independently_verified' and info(cell)['RAW_sha256']=='d2fefdde6795303e706cfe687e2806dcc39304558a1ff6bf1f0cba0d49d0d493'
oldgraph=load(B/'integration84/graph-check/receipt.json');newgraph=load(B/'integration84/cell-admission-correction/correct-cell-graph.receipt.json')
assert oldgraph['command'][-1]=='ASTIS-SW-PBPS-actual-bounded-test-continuity' and newgraph['command'][-1]=='ASTIS-SW-PBPS-actual-outer-bounded-l2-continuity'
assert oldgraph['exit_code']==newgraph['exit_code']==0 and newgraph['terminal_closed']
graph=load(R/'_site/data/underlying-lean-graph.json');kernel=load(B/'independent-math84/kernel-dependency-summary84.json');target='decl:'+D
incoming=[e for e in graph['edges'] if e.get('target')==target];expected=set(kernel['external_ASTIS_dependencies']);actual_signals={e['source'][5:] for e in incoming if e.get('source','').startswith('decl:')};missing=sorted(expected-actual_signals);extra=sorted(actual_signals-expected)
assert len(expected)==4 and len(missing)==2 and extra==['AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn.prod']
with (O/'integration.corrected.notes.before-graph-clarification.snapshot.json').open('xb') as f:f.write((B/'integration.corrected.notes.json').read_bytes())
save('graph-evidence-mismatch.diagnosis.json',dict(status='TYPED_GRAPH_EVIDENCE_LIMITATION',reviewer_id='/root/exact_verify77',checked_integration_commit=C,created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),graph=info(R/'_site/data/underlying-lean-graph.json'),kernel=info(B/'independent-math84/kernel-dependency-summary84.json'),actual_four_kernel_parents=sorted(expected),incoming_graph_edges=incoming,missing_parent_graph_signals=missing,extra_non_kernel_scanner_signal=extra,correct84_graph_receipt=info(B/'integration84/cell-admission-correction/correct-cell-graph.receipt.json'),reason='The graph coverage gate passed for correct84, but current underlying graph is an explicitly incomplete name scan: only2 of4 actual kernel parents appear. Therefore no certification of four actual dependency edges in current _site graph is possible.',math_issue=False,cell_restore_repair_issue=False,required_resolution='Scope control-plane repair notes/admission honestly to unchanged scanner graph plus separate exact4-parent kernel evidence; alternatively perform a separately serialized graph repair. Do not overwrite old wrong-target receipt.',production_or_shared_edits=False))
print('GRAPH LIMITATION RETAINED',info(O/'graph-evidence-mismatch.diagnosis.json')['RAW_sha256'])
