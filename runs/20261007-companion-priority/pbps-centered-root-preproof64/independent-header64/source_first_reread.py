from pathlib import Path
import hashlib,json,datetime,os,re
out=Path(r'E:/Samplinglib/runs/20261007-companion-priority/pbps-centered-root-preproof64/independent-header64');primary=out.parent/'independent-primary64'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
lease={'schema':1,'owner':'/root/preproof_centered64','task':'independent-preproof-header-review64','state':'OPEN','opened_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'owned_prefix':str(out),'primary64_prefix_read_only':str(primary),'forbidden':['proof search','compile','header/canonical/ledger/Git/site writes','theorem/science/Goal admission']}
(out/'owned-lease.json').write_bytes((json.dumps(lease,indent=2)+'\n').encode())
seal=json.loads((primary/'source-first-graph-seal.json').read_bytes());graphraw=(primary/'source-proof-graph.json').read_bytes();graph=json.loads(graphraw);coverage_raw=(primary/'source-coverage-inventory.json').read_bytes();coverage=json.loads(coverage_raw);regions=json.loads((primary/'primary-regions-receipt.json').read_bytes());source=Path(regions['source']).read_bytes()
assert hashlib.sha256(source).hexdigest()==seal['source_raw_sha256'];assert hashlib.sha256(graphraw).hexdigest()==seal['graph_sha256'];assert hashlib.sha256(coverage_raw).hexdigest()==seal['coverage_sha256'];assert json.loads((primary/'owned-lease.json').read_bytes())['state']=='CLOSED_LAST'
selected=['S1.p1','S2.SS2','A2.SS1','A2.SS2','A3.SS1','A4.SS1']
read_pins=[]
for r in regions['regions']:
 a,b=r['byte_range_zero_based_half_open'];chunk=source[a:b];assert chunk==Path(r['raw_file']).read_bytes();assert sha(r['raw_file'])==r['raw_sha256'];assert sha(r['lf_file'])==r['lf_sha256'];assert sha(r['readable_file'])==r['readable_sha256'];assert sha(r['alttext_file'])==r['alttext_sha256']
 read_pins.append({'region':r['source_region'],'byte_range_zero_based_half_open':[a,b],'raw_sha256':r['raw_sha256'],'lf_sha256':r['lf_sha256'],'readable_sha256':r['readable_sha256'],'alttext_sha256':r['alttext_sha256']})
 if r['source_region'] in selected:print('SOURCE REGION '+r['source_region']+'\n'+Path(r['readable_file']).read_text(encoding='utf8'))
for c in coverage['inventory']:
 a,b=c['byte_range_zero_based_half_open'];assert hashlib.sha256(source[a:b]).hexdigest()==c['literal_sha256'];assert c['disposition'] in ['NODE','EXCLUDED']
immutable=[{'name':p.name,'raw_sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(primary.iterdir()) if p.is_file()]
receipt={'schema':1,'event':'SOURCE_GRAPH_AND_ORIGINAL_ASSUMPTIONS_REREAD_BEFORE_EXACT_HEADERS','actual_pid':os.getpid(),'actual_exit_expected':0,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'primary_source':regions['source'],'primary_source_raw_sha256':seal['source_raw_sha256'],'graph_sha256':hashlib.sha256(graphraw).hexdigest(),'coverage_sha256':hashlib.sha256(coverage_raw).hexdigest(),'graph_nodes':[{'id':n['id'],'parents':n['parents'],'classification':n['classification']} for n in graph['nodes']],'regions':read_pins,'primary64_immutable_outputs':immutable,'exact_header0_or_header1_received_or_read':False,'source_inputs':['C2 V','both global Hessian bounds','0<alpha<=beta','eta>0','beta eta<=1','real probability L2; HP=ran(P); exact mean-zero centered space'],'coverage_items_rechecked':len(coverage['inventory']),'science63_review_or_admission':False}
(out/'primary-before-header-reread-receipt.json').write_bytes((json.dumps(receipt,indent=2)+'\n').encode())
print('PREREAD RECEIPT SHA256 '+sha(out/'primary-before-header-reread-receipt.json'))
print('ACTUAL PID '+str(os.getpid())+'; EXIT_EXPECTED 0; HEADERS NOT READ')
