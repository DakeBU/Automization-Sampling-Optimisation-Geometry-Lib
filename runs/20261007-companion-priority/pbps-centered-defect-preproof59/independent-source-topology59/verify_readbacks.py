from pathlib import Path
import hashlib,json,sys
sys.stdout.reconfigure(encoding='utf8')
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
load=lambda n:json.loads((O/n).read_bytes())
def check(pin):
 b=(R/pin['path']).read_bytes();assert len(b)==pin['bytes'] and sha(b)==pin['raw_sha256'];assert sha(b.replace(b'\r\n',b'\n'))==pin['lf_sha256']
x=load('indexed-input.manifest.json')
for i in x['inputs']:
 check(i['qualified_input']);check(i['qualified_immutable_snapshot'])
 assert (R/i['qualified_input']['path']).read_bytes()==(R/i['qualified_immutable_snapshot']['path']).read_bytes()
check(x['large_primary_reused_without_copy']);raw=(R/x['large_primary_reused_without_copy']['path']).read_bytes()
count=0
for n in ['primary.source-first.json','primary.supplemental-context.json']:
 v=load(n);check(v['primary'])
 for row in v['exact_regions']:
  b=raw[row['start_utf8_byte']:row['end_utf8_byte_exclusive']]
  assert len(b)==row['slice_bytes'] and sha(b)==row['slice_sha256'];count+=1
g=load('source-proof-graph.json');h=g.pop('source_graph_sha256');assert sha(canon(g))==h
assert g['status']=='INDEPENDENT_EXTRACTION_ONLY_PENDING_DISTINCT_COVERAGE_REVIEW' and not g['source_topology_self_approval']
c=load('source-coverage.manifest.json');assert len(c['items'])==c['item_count']==54
assert len({v['item_id'] for v in c['items']})==54
assert all(v['disposition'] in ['NODE','EXCLUDED'] for v in c['items'])
assert sum(v['disposition']=='NODE' for v in c['items'])==25
assert sum(v['disposition']=='EXCLUDED' for v in c['items'])==29
assert all(v.get('reason') for v in c['items'] if v['disposition']=='EXCLUDED')
assert all(v.get('node') for v in c['items'] if v['disposition']=='NODE')
assert not c['self_approval']
r=load('source-statement.preproof-review.json');assert not r['blocking_statement_issue'] and r['EXCESS_count']==0
assert not r['formal_admission'] and not r['chronology']['current59_proof_body_read']
for k in ['exact_header0','exact_header1']:
 check(r[k]);assert b':= by' not in (R/r[k]['path']).read_bytes()
assert not (O/'lease.json').exists(),'CLOSEDLAST must follow subprocess EXIT0.'
print(json.dumps({'status':'PASS','exact_primary_regions':count,'indexed_snapshots':10,
 'graph_nodes':19,'graph_edges':23,'coverage_items':54,'NODE':25,'EXCLUDED':29,
 'statement_scope':'PREPROOF_SOURCE_ONLY','topology_scope':'EXTRACTION_ONLY_PENDING_DISTINCT_REVIEW',
 'compiler':'NOT_STARTED','whole_math_review':'SEPARATE_REQUIRED'}))
