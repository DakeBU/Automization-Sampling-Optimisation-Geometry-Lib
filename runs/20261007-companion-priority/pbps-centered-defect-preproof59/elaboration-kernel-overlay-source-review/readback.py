from pathlib import Path
import hashlib,json,os,sys
sys.stdout.reconfigure(encoding='utf8')
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def verify(a):
 b=(R/a['path']).read_bytes();lf=b.replace(b'\r\n',b'\n')
 assert (len(b),len(lf),sha(b),sha(lf))==(a['bytes'],a['lf_bytes'],a['raw_sha256'],a['lf_sha256'])
m=json.loads((O/'input.manifest.json').read_bytes());assert m['count']==33
for x in m['qualified_indexed_immutable_inputs']:
 verify(x['original']);verify(x['snapshot']);assert (R/x['original']['path']).read_bytes()==(R/x['snapshot']['path']).read_bytes()
p=json.loads((O/'named-kernel-overlay-source.payload.json').read_bytes())
for k in ('review','comparison','inputs','proposal'):verify(p[k])
for x in p['headers']:verify(x['parent']);verify(x['successor'])
r=json.loads((O/'source-overlay-review.json').read_bytes());assert r['EXCESS']==0 and r['source_hypothesis_changes']==0 and r['source_graph_changes']==0
c=json.loads((O/'exact-comparison.json').read_bytes());assert len(c['headers'])==2 and len(c['compiler_results_independent_classification'])==8
assert all(x['forward_exact_raw_LF'] and x['reverse_exact_raw_LF'] and x['complete_named_rfl_exact'] for x in c['headers'])
print(json.dumps({'actual_readback_pid':os.getpid(),'qualified_original_snapshot_pairs':33,'all_hashes_read_back':True,'named_kernel_overlay_source_payload_sha256':sha(canon(p)),'verdict':r['verdict'],'new_compilers':0}))
