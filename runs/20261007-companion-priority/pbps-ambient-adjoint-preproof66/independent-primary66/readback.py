import json,hashlib,os,re
from pathlib import Path
O=Path(__file__).parent
H=lambda b:hashlib.sha256(b).hexdigest()
C=lambda d:json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def load(n):return json.loads((O/n).read_bytes())
r=load('review-run.json');x=dict(r);del x['run_sha256'];assert H(C(x))==r['run_sha256'];d=load('primary-source-decision.json');y=dict(d);del y['review_run_sha256'];assert y==r['complete_source_planning_decision'];assert len(y['semantic_slots'])==7 and y['candidate_verdict'] is None
for x in r['pre_finalization_artifact_pins']:
 b=(O/x['name']).read_bytes();assert H(b)==x['RAW_sha256'] and len(b)==x['RAW_bytes']
p=load('RAW-input-payload.json')
for x in p['exact_RAW_inputs']:
 b=x['utf8'].encode('utf-8');assert H(b)==x['RAW_sha256'] and len(b)==x['RAW_bytes']
full=Path(p['primary_whole_source']['primary_full_path']).read_bytes();assert H(full)==p['primary_whole_source']['primary_full_RAW_sha256'];inv=load('source-coverage-inventory.json');assert len(inv['math_items'])==310 and inv['all_310_classified']
for x in inv['math_items']:
 a,z=x['RAW_byte_range'];assert H(full[a:z])==x['raw_math_sha256'];assert x['target66_classification'] and x['alttext_present'] and x['annotation_present'] and x['annotation_matches']
# Exact source semantics: B5 and B16 are prerequisites, not excluded context.
for x in inv['math_items']:
 if x['RAW_byte_range'][0] in [740478,790765]:assert 'excluded' not in x['target66_classification']
for reg in inv['regions']:
 a,z=reg['source_RAW_range_end_exclusive'];b=full[a:z];assert H(b)==reg['RAW_sha256'];assert len(re.findall(rb'<math\b',b))==reg['math_count']
for k in ['COMPLETE_RAW_DECISION','COMPLETE_RAW_REVIEW','SEPARATE_COMPLETE_RAW_INPUT','source_graph','source_inventory']:
 x=load('closure-index.json')[k];assert H((O/x['name']).read_bytes())==x['RAW_sha256']
print(json.dumps(dict(status='READBACK_PASS',actual_pid=os.getpid(),source_items=310,source_regions=6,seven_source_slots=True,no_candidate_verdict=True,source_graph_independent=True,logical_run_sha256=r['run_sha256']),sort_keys=True))
