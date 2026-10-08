from common import *
import importlib.util,gzip,re
from unittest.mock import patch
from tools import astis,astis_publication
INTEGRATION='d1b150d6e59b3a9c398cc41e75a3330ef1915790'; assert git('rev-parse','HEAD').decode().strip()==INTEGRATION
p1=J(P/'phase1.inputs.json'); p2=J(P/'phase2.inputs.json'); fixed={q['original']['path']:q['exact_raw_snapshot']['path'] for q in p1['qualified_original_snapshot_pairs']+p2['qualified_original_snapshot_pairs']}
def frozen(p): return path(fixed.get(path(p).as_posix(),path(p)))
def Q(p): return J(frozen(p))
for q in p1['qualified_original_snapshot_pairs']+p2['qualified_original_snapshot_pairs']: matches(q['original'],q['exact_raw_snapshot']['path']); matches(q['exact_raw_snapshot'])
notes=Q(R/'integration.notes.json'); assert (notes['registry_count'],notes['root_jobs'],notes['test_jobs'])==(505,9167,9460)
gate_rows=[]
for check in notes['checks']:
 matches(check['receipt']); receipt=J(path(check['receipt']['path'])); assert receipt['exit_code']==0 and receipt['terminal_closed']
 for k in ['stdout','stderr']: matches(check[k])
 gate_rows.append(dict(label=check['label'],actual_PID=receipt['actual_foreground_pid'],exit_code=0,receipt=check['receipt'],stdout=check['stdout'],stderr=check['stderr']))
for folder in ['publication-final-admin','contributor-final-admin','frontier-final-admin','official-graph-final-admin','graph-producer-final-admin','graph-consumer-final-admin','record-aggregate61','preserve-generated-context61','cache-generated-cards61']:
 p=R/'integration61'/folder/'receipt.json'; q=J(p); assert q['exit_code']==0 and q['terminal_closed'];
 for k in ['stdout','stderr']: matches(q[k])
 gate_rows.append(dict(label=folder,actual_PID=q['actual_foreground_pid'],exit_code=0,receipt=pin(p),stdout=q['stdout'],stderr=q['stderr']))
mandatory=path(next(x['stdout']['path'] for x in gate_rows if x['label']=='mandatory-astis-check')).read_text(encoding='utf8'); assert 'Build completed successfully (9167 jobs).' in mandatory and 'Build completed successfully (9460 jobs).' in mandatory and 'Registry' in mandatory
publication=path(next(x['stdout']['path'] for x in gate_rows if x['label']=='publication-final-admin')).read_text(); assert 'Publication PASS: 226' in publication
preserve=path(next(x['stdout']['path'] for x in gate_rows if x['label']=='preserve-generated-context61')).read_text(); assert 'Restored 82' in preserve and '65 nodes' in preserve and '513 module' in preserve
# Exact committed source and metadata comparison: stable SCI source/lesson/audit bytes remain unchanged.
plan=Q(R/'publication-plan.json'); unchanged=[]
stable=[x['original']['path'] for x in p1['qualified_original_snapshot_pairs'] if any('/'+segment+'/' in x['original']['path'] for segment in ['AutoSamplingTheory','Tests','publications','declaration_lessons','semantic-roundtrip/audits'])]
for absname in stable:
 name=path(absname).relative_to(ROOT).as_posix(); science=git('show',SCI+':'+name); integration=git('show',INTEGRATION+':'+name); assert science==integration
 assert science.replace(b'\r\n',b'\n')==frozen(absname).read_bytes().replace(b'\r\n',b'\n'); unchanged.append(dict(path=name,Git_SCI_integration_same=True,LF_sha256=H(science.replace(b'\r\n',b'\n'))))
cell_changes=[]
for update in notes['cell_administration_updates']:
 matches(update['before']); matches(update['after'],frozen(update['after']['path'])); b=J(path(update['before']['path'])); a=Q(update['after']['path']); assert a['status']=='independently_verified' and a['evidence']['serialized_shared_gate']
 def diffs(x,y,p=''):
  if isinstance(x,dict) and isinstance(y,dict):
   return sum([diffs(x.get(k),y.get(k),p+'/'+k) for k in sorted(set(x)|set(y))],[])
  return [] if x==y else [dict(pointer=p,before=x,after=y)]
 delta=diffs(b,a); allowed={'/evidence/serialized_shared_gate','/graph_contribution/visual_review'}
 assert all(d['pointer'].startswith('/evidence/serialized_shared_gate') or d['pointer'] in allowed for d in delta),delta
 cell_changes.append(dict(cell=update['cell'],before=update['before'],after=update['after'],actual_delta=delta,mathematical_payload_unchanged=True))
# Parse reviewed integration ledger snapshot, keeping future claim outside this scope.
ledger=frozen(ROOT/'runs/substantive_advances.jsonl').read_bytes(); records=[json.loads(l) for l in ledger.splitlines() if l.strip()]; target=[x for x in records if x.get('advance_id')=='ASTIS-SA-20261009-PBPSPositiveRealDefectRoot']; assert target[-1]['to_state']=='VERIFIED' and target[-1]['worker_id']=='independent_whole_math52_exact61'
states={}
for x in records:
 if x.get('advance_id') and x.get('to_state'): states[x['advance_id']]=x['to_state']
assert [k for k,v in states.items() if v=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
# Inspect actual shared integration source and Registry reachability from pinned Git paths.
shared={n:git('show',INTEGRATION+':'+n).decode() for n in ['AutoSamplingTheory/TechnicalLemmas.lean','AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests.lean','Tests/Basic.lean']}
assert 'import AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareRoot' in shared['AutoSamplingTheory/TechnicalLemmas.lean']; assert 'import AutoSamplingTheory.ExampleCases.ProximalBPS.RealDefectRoot' in shared['AutoSamplingTheory/ExampleCases.lean']; assert 'import Tests.ProximalBPSRealDefectRoot' in shared['Tests.lean']
assert '505' in shared['Tests/Basic.lean']
for decl in plan['mathematical_declarations']: assert decl in shared['AutoSamplingTheory/TechnicalLemmas/Registry.lean']
assert all(not re.search(r'^\s*(?:theorem|lemma|def|abbrev)\b',astis.strip_lean_comments_and_strings(shared[n]),re.M) for n in ['AutoSamplingTheory/TechnicalLemmas.lean','AutoSamplingTheory/ExampleCases.lean'])
scan=[]
for q in J(R/'math-freeze.json')['inputs'][:5]:
 text=astis.strip_lean_comments_and_strings(frozen(q['path']).read_text()); assert not astis.FORBIDDEN_REGEX.search(text) and not re.search(r'^\s*import\s+Tests(?:\.|\s|$)',text,re.M); scan.append(pin(frozen(q['path'])))
# Complete official graph digest using exact integration tree paths/items/cells, excluding future62 inputs.
tree={}
for row in git('ls-tree','-rz',INTEGRATION).split(b'\0'):
 if row:
  meta,n=row.split(b'\t',1); tree[n.decode()]=meta.decode().split()[2]
source_names=['AutoSamplingTheory.lean']+[x.relative_to(ROOT).as_posix() for x in sorted(ROOT/n for n in tree if n.startswith('AutoSamplingTheory/') and n.endswith('.lean'))]+['Tests.lean']+[x.relative_to(ROOT).as_posix() for x in sorted(ROOT/n for n in tree if n.startswith('Tests/') and n.endswith('.lean'))]+['lakefile.lean','lean-toolchain','lake-manifest.json']
digest=hashlib.sha256(); source_rows=[]
for n in source_names:
 b=path(n).read_bytes(); assert H(b.replace(b'\r\n',b'\n'))==H(git('show',INTEGRATION+':'+n).replace(b'\r\n',b'\n'))
 digest.update(n.encode()); digest.update(b'\0'); digest.update(b); digest.update(b'\0'); source_rows.append(pin(n))
items=[]
for n in sorted(n for n in tree if n.startswith('website/content/publications/') and n.endswith('.json')): items.extend(json.loads(git('show',INTEGRATION+':'+n))['items'])
cells={}
for item in items:
 for binding in item['bindings']:
  cid=binding['cell']; n='research-wiki/frontier-cells/'+cid+'.json'; cells[cid]=json.loads(git('show',INTEGRATION+':'+n)) if n in tree else None
  if cells[cid] is not None: cells[cid]['__path__']=n
helper=ROOT/'website/scripts/publication_reader.py'; sys.path.insert(0,str(ROOT/'website/scripts')); import publication_reader
with patch.object(publication_reader.publication,'inputs',return_value={'cells':cells}),patch.object(publication_reader.publication,'load',return_value=items),patch.object(publication_reader.astis_site,'source_digest',return_value=digest.hexdigest()): observed=publication_reader.graph_input_digest()
graph=Q(ROOT/'_site/data/underlying-lean-graph.json')
if observed!=graph['publication_inputs_sha256'] and not (P/'graph.freshness.negative.json').exists():
 complete_input=dict(lean=digest.hexdigest(),items=items,cells=cells); W(P/'graph.exact-integration-input.payload.json',complete_input)
 lf_digest=hashlib.sha256()
 for n in source_names:
  lf_digest.update(n.encode()); lf_digest.update(b'\0'); lf_digest.update(path(n).read_bytes().replace(b'\r\n',b'\n')); lf_digest.update(b'\0')
 W(P/'graph.freshness.negative.json',dict(status='GRAPH_EXACT_INTEGRATION_DIGEST_NEGATIVE',checked_commit=INTEGRATION,actual_PID=os.getpid(),actual_exact_native_helper_digest=observed,official_frozen_header=graph['publication_inputs_sha256'],complete_input_payload=pin(P/'graph.exact-integration-input.payload.json'),source_rows=source_rows,source_digest_actual_raw=digest.hexdigest(),diagnostic_LF_source_digest=lf_digest.hexdigest(),diagnostic_LF_graph_digest=H(C(dict(lean=lf_digest.hexdigest(),items=items,cells=cells))),helper_whole=pin(helper),exact_items_count=len(items),exact_referenced_cells_count=len(cells),future62_not_read=True,scope='Root final graph vs complete exact integration tree raw source/native items/cells; no mathematical/source-body issue',original_negative_tools=['6232b5','b1643a']))
assert observed==graph['publication_inputs_sha256'],(observed,graph['publication_inputs_sha256'])
branches=[]
for decl in plan['mathematical_declarations']:
 identity='decl:'+decl; node=next(n for n in graph['nodes'] if n['id']==identity); incident=[e for e in graph['edges'] if e.get('source')==identity or e.get('target')==identity]; assert incident
 branches.append(dict(declaration=decl,node=node,incident_edges=incident,truth='Solid imports/module ownership; dashed name-scanner references are incomplete and not certified proof implication. LogConcaveOn.prod scanner match not credited as actual proof parent.'))
W(P/'graph.input.recipe.json',dict(status='PASS',checked_commit=INTEGRATION,publication_inputs_sha256=observed,actual_helper_whole=pin(helper),helper_selected_lines=[183,187],complete_lean_source_digest=digest.hexdigest(),source_rows=source_rows,production_modules_including_root=513,publication_item_count=len(items),publication_items_digest=H(C(items)),complete_referenced_cells_digest=H(C(cells)),referenced_cell_count=len(cells),recipe='Actual graph_input_digest invoked with exact complete integration Git publication items/referenced cells and source_digest over exact integration native WindowsPath-sorted source path list/actual raw bytes. No projected graph payload/subset substitution, no future working-tree scan.',branches=branches))
stage=J(R/'integration61/staging-whitespace/diagnosis.json'); assert len(stage['findings'])==332 and stage['authored_complement_exit']==0 and stage['full_staged_called_PASS'] is False
W(P/'phase2.review.json',dict(status='PASS_SCOPED_REPOSITORY_EXPOSITION',actual_reviewer_PID=os.getpid(),checked_science_commit=SCI,checked_integration_commit=INTEGRATION,gates=gate_rows,gate_receipt_count=len(gate_rows),Registry=505,root_jobs=9167,Tests_jobs=9460,tracked_production_count=513,science_source_metadata_unchanged=unchanged,exact_cell_admin_deltas=cell_changes,sole_STABILIZING='ASTIS-SA-20261005-SPHMCImplementedPhaseKernel',fake_scan_inputs=scan,graph=pin(P/'graph.input.recipe.json'),whitespace=dict(immutable_staged_findings=332,exact_paths=stage['exact_immutable_raw_paths'],authored_complement_PASS=True,full_staged_PASS=False,diagnosis=pin(R/'integration61/staging-whitespace/diagnosis.json')),unrelated_generated_preservation='Actual82 unrelated HEAD restores/65 existing canonical metadata nodes retained;443 puregenerated cards cached, two enriched new61 cards committed. Exact integration inventory513.',future62='Post-phase2 claim/new-owned body outside this integration/scoped inputs; ledger/cells reviewed through exact phase2 snapshots; no reads of future62',remaining=notes['remaining'],compiler='NOT_STARTED_CLOSED'))
print('PHASE2_REVIEW_PASS',len(gate_rows),'closed receipts',observed)
