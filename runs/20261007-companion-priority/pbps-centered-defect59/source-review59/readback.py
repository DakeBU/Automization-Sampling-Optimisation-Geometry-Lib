from pathlib import Path
import hashlib,json,os,sys
sys.stdout.reconfigure(encoding='utf8')
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def vp(x):
 b=(R/x['path']).read_bytes();lf=b.replace(b'\r\n',b'\n');assert (len(b),len(lf),sha(b),sha(lf))==(x['bytes'],x['lf_bytes'],x['raw_sha256'],x['lf_sha256'])
m=json.loads((O/'input.manifest.json').read_bytes())
for x in m['qualified_input_snapshot_pairs']:vp(x['original']);vp(x['snapshot']);assert (R/x['original']['path']).read_bytes()==(R/x['snapshot']['path']).read_bytes()
for x in m['support_exact_LF_spans']:
 vp(x['original_file']);vp(x['snapshot']);p=R/x['original_file']['path'];s=''.join(p.read_text(encoding='utf8').splitlines(keepends=True)[x['start_line']-1:x['end_line']]).encode();assert sha(s)==x['LF_slice_sha256'];assert s==(R/x['snapshot']['path']).read_bytes()
vp(m['primary_verified_without_huge_copy']['original'])
p=json.loads((O/'named-source-review.payload.json').read_bytes())
for k in ('inputs','publication_exposition_review','primary_boundary_before_packets'):vp(p[k])
for review in p['reviews_before_native_run_binding']:
 assert set(review['semantic_slots'])=={'objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies'}
 assert all(x['relation']!='not-audited' and x['evidence'] for x in review['semantic_slots'].values())
 assert not any(x['blocking'] for x in review['deltas']) and review['repairs']==[]
if sys.argv[1:] == ['final']:
 run=json.loads((O/'run.json').read_bytes());h=run.pop('run_sha256');assert sha(canon(run))==h;assert sha(canon(run['named_source_review_payload']))==run['named_source_review_payload_sha256']==sha(canon(p))
 for x in run['output_pins_before_run']:vp(x)
 for i,sealed in enumerate(p['reviews_before_native_run_binding']):
  review=json.loads((O/f'source.{i}.review.json').read_bytes());expected=dict(sealed);expected['review_run_sha256']=h;assert review==expected
 print(json.dumps({'stage':'final','actual_readback_pid':os.getpid(),'native_run_sha256_checked':h,'exact_complete_review_run_bindings':2,'qualified_original_snapshot_pairs':len(m['qualified_input_snapshot_pairs']),'support_spans':len(m['support_exact_LF_spans']),'all_raw_LF_and_native_payload_readbacks':True,'new_compilers':0}))
else:
 print(json.dumps({'stage':'pre-native','actual_readback_pid':os.getpid(),'qualified_original_snapshot_pairs':len(m['qualified_input_snapshot_pairs']),'support_spans':len(m['support_exact_LF_spans']),'named_source_review_payload_sha256':sha(canon(p)),'all_raw_LF_readbacks':True,'new_compilers':0}))
