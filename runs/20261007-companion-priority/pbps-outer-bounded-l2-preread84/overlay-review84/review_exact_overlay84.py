"""Review distinct proposed source-topology patch only; no source/Lean/shared writes."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,datetime,copy,collections
ROOT=Path('E:/Samplinglib')
BASE='runs/20261007-companion-priority/pbps-outer-bounded-l2-preread84/'
OUT=Path(__file__).resolve().parent
PRIMARY='runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=(ROOT/p).read_bytes();return {'path':p,'raw_sha256':sha(b),'bytes':len(b)}
expected={PRIMARY:'d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760',
 BASE+'source_inventory84.json':'c9e17b30fd27cc9c2b30f4707d9e63c11404a6642bd6348a4bd1c5605cec6265',
 BASE+'source_proof_graph84.json':'d05d7fd9b77f49acd939d31fa858585552956a6793dc4c3e0ab3063d944fafcb',
 BASE+'bounded_candidate84.json':'64d2a26607af9e6e426ca5d0830b592404dca4c516cbac0869bc6c656f3e9e0f',
 BASE+'source_freeze84.seal.json':'80f8c14962a0bc21b7969341e415acc1ee8663220552d799c6f373b732eb8883',
 BASE+'source_freeze84.raw-manifest.json':'b5ebfdb08166f55881ee2eadc4b9faf7844e97608b79abb5a07116b095e47c1b',
 BASE+'independent-topology84/proposed-minimal-topology-overlay84.json':'25287eb89eaa17c29feac3d55a401af06a49abfe47181e6d35b3df7b89911577',
 BASE+'independent-topology84/topology-review.decision84.json':'87408969ab93f913e662931ecf607031193e4a68ea7ecf2887a03cb80740311a',
 BASE+'independent-topology84/topology-review.run-manifest84.json':'0cf8c6cf72c0b9a80433ead44aaccb88d5802cfe004db3deb6aac186b2fd656b'}
# Read/parse primary before loading the overlay or any original topology object.
assert pin(PRIMARY)['raw_sha256']==expected[PRIMARY]
class H(HTMLParser):
 void={'br','hr','meta','link','img','input','source','wbr','area','base','col','embed','param','track'}
 def __init__(self):super().__init__();self.st=[];self.m=0;self.o={}
 def handle_starttag(self,t,a):
  d=dict(a)
  if t not in self.void:self.st.append((t,d.get('id')))
  if t=='math':
   self.m+=1
   if self.m==1:
    for _,i in self.st:
     if i:self.o.setdefault(i,[]).append(d.get('alttext',''))
 def handle_endtag(self,t):
  if t=='math':self.m-=1
  for k in range(len(self.st)-1,-1,-1):
   if self.st[k][0]==t:self.st=self.st[:k];break
 def handle_data(self,s):
  if not self.m:
   for _,i in self.st:
    if i:self.o.setdefault(i,[]).append(s)
 def normalized(self,i):return ' '.join(' '.join(self.o[i]).split())
h=H();h.feed((ROOT/PRIMARY).read_text(encoding='utf-8'))
source_ids=['license-tr','S3.E1','A1.Thmtheorem1','A1.SS1.SSS0.Px1.p6.1','A1.Ex22','A1.SS1.SSS0.Px1.p6.2']
source_pins=[{'source_id':i,'normalized_anchor_sha256':sha(h.normalized(i).encode())} for i in source_ids]
assert 'Density' in h.normalized(source_ids[-1]) and 'contractivity' in h.normalized(source_ids[-1])
assert 'perpetual non-exclusive' in h.normalized('license-tr')

# Locate proposer receipts by exact name if necessary; their verdict content is never loaded.
for key in list(expected):
 if not (ROOT/key).exists():
  matches=[p for p in (ROOT/(BASE+'independent-topology84')).iterdir()
           if p.is_file() and sha(p.read_bytes())==expected[key]]
  assert len(matches)==1,('missing exact RAW receipt',key)
  value=expected.pop(key);expected[matches[0].relative_to(ROOT).as_posix()]=value
for p,v in expected.items():assert pin(p)['raw_sha256']==v,p
original_manifest=json.loads((ROOT/(BASE+'source_freeze84.raw-manifest.json')).read_bytes())
for p in original_manifest['raw_outputs']:
 assert pin(p['path'])==p,('original freeze mutated',p['path'])

inv=json.loads((ROOT/(BASE+'source_inventory84.json')).read_bytes())
graph=json.loads((ROOT/(BASE+'source_proof_graph84.json')).read_bytes())
overlay=json.loads((ROOT/(BASE+'independent-topology84/proposed-minimal-topology-overlay84.json')).read_bytes())
assert overlay['proposer']=='/root/exact_verify77'
assert len(overlay['operations'])==8
assert overlay['frozen_inventory_RAW_sha256']==expected[BASE+'source_inventory84.json']
assert overlay['frozen_graph_RAW_sha256']==expected[BASE+'source_proof_graph84.json']
assert overlay['frozen_candidate_RAW_sha256']==expected[BASE+'bounded_candidate84.json']
g=copy.deepcopy(graph);i=copy.deepcopy(inv)
def row(rows,id):return next(x for x in rows if x.get('id',x.get('inventory_id'))==id)
audit=[]
reason=[
 'Source p6.2 explicitly requires C_c density independently of contractivity. New G84-23 is an OPEN source ingredient over the actual nu_y L2 space, with exact quotient/topology contracts deferred; no proof credit.',
 'The contraction edge now carries contraction alone; source density is not a consequence of invariance/Jensen contraction.',
 'New E84-39 expresses the separate density input into future all-L2 extension. FUTURE_OPEN / OPEN_NOT_USED correctly prevents using it as completed candidate84 evidence.',
 'ALL_L2_AND now requires density together with C_c continuity, well-defined operator and contraction. It is AND_OPEN, not an alternative route or inferred conclusion.',
 'Removing the background-only density string is consistent with moving the same ingredient to a real dependency node/edge; no density obligation is dropped.',
 'I84-45 already records density+all-L2 extension at source p6.2. Adding G84-23 separately accounts for its density ingredient while preserving G84-21 extension mapping.',
 'Mirroring I84-45 graph-node addition in scope_coverage preserves complete inventory/graph correspondence without inventing an additional source assertion.',
 'Exact additions are one OPEN node and one OPEN dependency edge; inventory and excluded associations unchanged. Correct counts:47/23/39,37 dependencies,2 excluded associations;5 future OPEN dependencies.'
]
for k,op in enumerate(overlay['operations']):
 t=op['operation']
 if t=='append_node':
  assert op['value']['id']=='G84-23' and op['value']['status']=='OPEN'
  assert not any(n['id']==op['value']['id'] for n in g['nodes'])
  before=None;g['nodes'].append(copy.deepcopy(op['value']));after=op['value']
 elif t=='replace_edge_field':
  r=row(g['edges'],op['edge_id']);before=copy.deepcopy(r[op['field']]);assert before==op['old']
  r[op['field']]=op['new'];after=op['new']
 elif t=='append_edge':
  assert op['value']['id']=='E84-39' and op['value']['status']=='OPEN_NOT_USED'
  assert not any(e['id']==op['value']['id'] for e in g['edges'])
  before=None;g['edges'].append(copy.deepcopy(op['value']));after=op['value']
 elif t=='append_junction_edge':
  r=row(g['junctions'],op['junction_id']);before=copy.deepcopy(r['edges'])
  assert op['value'] not in r['edges'];r['edges'].append(op['value']);after=copy.deepcopy(r['edges'])
 elif t=='replace_junction_field':
  r=row(g['junctions'],op['junction_id']);before=copy.deepcopy(r[op['field']]);assert before==op['old']
  r[op['field']]=copy.deepcopy(op['new']);after=op['new']
 elif t=='append_inventory_graph_node':
  r=row(i['items'],op['inventory_id']);before=copy.deepcopy(r['graph_nodes'])
  assert op['value'] not in r['graph_nodes'];r['graph_nodes'].append(op['value']);after=copy.deepcopy(r['graph_nodes'])
 elif t=='append_scope_coverage_graph_node':
  r=row(g['scope_coverage'],op['inventory_id']);before=copy.deepcopy(r['graph_nodes'])
  assert op['value'] not in r['graph_nodes'];r['graph_nodes'].append(op['value']);after=copy.deepcopy(r['graph_nodes'])
 elif t=='replace_graph_counts':
  before=copy.deepcopy(g['counts']);assert before==op['old'];g['counts']=copy.deepcopy(op['new']);after=op['new']
 else:raise AssertionError(t)
 audit.append({'patch_id':f'P84-{k+1:02d}','operation':t,'decision':'ACCEPT_EXACT_PATCH',
               'blocking':False,'source_ids':['A1.SS1.SSS0.Px1.p6.2'],
               'reason':reason[k],'before':before,'after':after})

# Exhaustive before/after operation footprint; original frozen objects remain unchanged on disk.
assert len(g['nodes'])==23 and len(g['edges'])==39 and len(i['items'])==47
assert g['nodes'][:-1]==graph['nodes']
for e in graph['edges']:
 after=row(g['edges'],e['id'])
 assert after==({**e,'ingredient':'Future invariance/Jensen contraction'} if e['id']=='E84-36' else e)
for j in graph['junctions']:
 after=row(g['junctions'],j['id'])
 assert after==({**j,'edges':j['edges']+['E84-39'],'background':[]} if j['id']=='ALL_L2_AND' else j)
for r in inv['items']:
 assert row(i['items'],r['id'])==({**r,'graph_nodes':r['graph_nodes']+['G84-23']} if r['id']=='I84-45' else r)
for r in graph['scope_coverage']:
 assert row(g['scope_coverage'],r['inventory_id'])==({**r,'graph_nodes':r['graph_nodes']+['G84-23']} if r['inventory_id']=='I84-45' else r)
assert {k:v for k,v in g.items() if k not in {'nodes','edges','junctions','scope_coverage','counts'}}=={k:v for k,v in graph.items() if k not in {'nodes','edges','junctions','scope_coverage','counts'}}
assert {k:v for k,v in i.items() if k!='items'}=={k:v for k,v in inv.items() if k!='items'}
assert sum(e['dependency_edge'] for e in g['edges'])==37
assert sum(not e['dependency_edge'] for e in g['edges'])==2
assert sum(e['status']=='OPEN_NOT_USED' for e in g['edges'])==5
assert row(g['junctions'],'NORMALIZE_OR')==row(graph['junctions'],'NORMALIZE_OR')
assert row(g['nodes'],'G84-21')['status']=='OPEN'
ids={n['id'] for n in g['nodes']};adj=collections.defaultdict(list);degree={x:0 for x in ids}
for e in g['edges']:
 assert e['from'] in ids and e['to'] in ids
 if e['dependency_edge']:adj[e['from']].append(e['to']);degree[e['to']]+=1
q=collections.deque(x for x,d in degree.items() if not d);seen=[]
while q:
 x=q.popleft();seen.append(x)
 for y in adj[x]:
  degree[y]-=1
  if degree[y]==0:q.append(y)
assert len(seen)==23
assert row(g['junctions'],'ALL_L2_AND')['edges']==['E84-34','E84-35','E84-36','E84-39']
for r in i['items']:assert r['graph_nodes']==row(g['scope_coverage'],r['id'])['graph_nodes']

now=datetime.datetime.now(datetime.timezone.utc).isoformat()
independence={'reviewer':'/root/fresh_source78','proposer':'/root/exact_verify77',
 'original_extraction_author':True,'exact_overlay_proposer':False,
 'review_boundary':'Distinct exact proposal only; no self-approval of original graph and no proof/header/claim verdict.',
 'chronology':'Pinned primary source parsed/read first this review; original frozen pins then checked; exact overlay operations compared with source and original before/after objects.',
 'prior_decisions':'Proposer decision and manifest RAW hashes checked only; decision content not loaded. Overlay diagnosis/classification is untrusted and not an acceptance premise.',
 'candidate84_header_or_body_read':False,'production_or_shared_writes':False,'state_transition':False}
raw_inputs=[pin(p) for p in expected]
for p in original_manifest['raw_outputs']:
 if not any(x['path']==p['path'] for x in raw_inputs):raw_inputs.append(p)
def canonical(x):return sha(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())
evidence={'schema':'astis.exact-topology-overlay-review84.run-evidence.v1','status':'closed','created_utc':now,
 'raw_inputs':raw_inputs,'primary_source_anchor_pins':source_pins,'independence':independence,
 'proposed_overlay_raw_sha256':expected[BASE+'independent-topology84/proposed-minimal-topology-overlay84.json'],
 'patch_operation_count':8,'before_counts':graph['counts'],'after_counts':g['counts'],
 'checks':{'all_old_values_exact':True,'every_operation_applied_in_memory_only':True,'before_after_footprint_exact':True,
  'all_frozen_outputs_raw_unchanged':True,'dependency_DAG_acyclic':True,'future_open_dependencies':5,
  'excluded_associations_unchanged':True,'normalization_OR_unchanged':True,'candidate84_in_scope_branch_unchanged':True,
  'source_density_separate_from_contraction':True,'no_original_source_theorem_repair':True},
 'in_memory_only_effective_graph_canonical_sha256':canonical(g),
 'in_memory_only_effective_inventory_canonical_sha256':canonical(i),
 'hash_semantics':'Derived canonical digests above identify in-memory operation results; they are not RAW file hashes or an adopted graph.',
 'noncircularity':'Evidence does not include result or manifest hashes; result binds exact evidence RAW; final manifest binds all owned outputs and omits selfhash.'}
def emit(name,obj):
 p=OUT/name;assert not p.exists(),str(p);p.write_bytes((json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode())
emit('topology-overlay.run-evidence84.json',evidence)
evidence_pin=pin((OUT/'topology-overlay.run-evidence84.json').relative_to(ROOT).as_posix())
result={'schema':'astis.distinct-exact-source-topology-overlay-review84.v1','status':'closed',
 'verdict':'ACCEPT_EXACT_TOPOLOGY_OVERLAY','verdict_reason':'Source p6.2 invokes density independently of contraction. All8 exact operations faithfully expose that futureOPEN ingredient without changing the bounded candidate84 branch, assumptions, target, normalization alternatives or global truth boundary.',
 'created_utc':now,'review_run_sha256':evidence_pin['raw_sha256'],
 'review_run_path':evidence_pin['path'],'proposed_overlay_raw_sha256':expected[BASE+'independent-topology84/proposed-minimal-topology-overlay84.json'],
 'primary_raw_sha256':expected[PRIMARY],'frozen_inventory_raw_sha256':expected[BASE+'source_inventory84.json'],
 'frozen_graph_raw_sha256':expected[BASE+'source_proof_graph84.json'],
 'frozen_candidate_raw_sha256':expected[BASE+'bounded_candidate84.json'],
 'per_patch_acceptance':audit,'blocking_deltas':[],'additional_required_repairs':[],
 'counts_before':graph['counts'],'counts_after':g['counts'],'future_open_dependencies_before':4,'future_open_dependencies_after':5,
 'source_basis':{'A1.SS1.SSS0.Px1.p6.1':'Invariance and Jensen give contraction; this source ingredient remains separate and OPEN.',
  'A1.SS1.SSS0.Px1.p6.2':'The final extension to all L2 explicitly uses both C_c density and contractivity after compact-test continuity.',
  'S3.E1':'Density node is scoped to the actual conditional Gibbs-position x standard-Gaussian momentum phase law, with exact measure/quotient contracts still to be admitted.'},
 'preserved_boundaries':['Source C_c vs ASTIS bounded real C_b distinction unchanged','M>=0 and4M^2 bounded DCT unchanged; no AS-DCT shortcut',
  'Fixed y/reference; literal actual clock law and independent outer product unchanged; no arbitrary correlated input',
  'Density not a dynamics assumption or candidate84 requirement','All-L2 operator, contraction, density, global Markov/restart/invariance/semigroup/main/cost/composition remain OPEN',
  'Normalization route OR and internal AND preserved','Two excluded associations remain nondependency edges'],
 'independence':independence,'credit':'Exact metadata-overlay review only; no public theorem proof/completion, no84 header or originalgraph self-validation.'}
emit('topology-overlay.decision84.json',result)
outputs=['review_exact_overlay84.py','topology-overlay.run-evidence84.json','topology-overlay.decision84.json']
manifest={'schema':'astis.exact-topology-overlay-review84.raw-manifest.v1','status':'closed','created_utc':now,
 'raw_inputs':raw_inputs,'raw_outputs':[pin((OUT/n).relative_to(ROOT).as_posix()) for n in outputs],
 'selfhash_convention':'Omit own hash; exact final manifest RAW reported externally. Evidence/result/manifest binding is acyclic.',
 'owned_directory':OUT.relative_to(ROOT).as_posix(),'original_freeze_unchanged':True,
 'no_shared_writes':True,'review_scope':'Distinct exact8operation topology proposal only; no statement or proof admission.'}
emit('topology-overlay.run-manifest84.json',manifest)
print(json.dumps({'verdict':result['verdict'],'after_counts':g['counts'],
 'outputs':[pin((OUT/n).relative_to(ROOT).as_posix()) for n in outputs+['topology-overlay.run-manifest84.json']]},indent=2))
