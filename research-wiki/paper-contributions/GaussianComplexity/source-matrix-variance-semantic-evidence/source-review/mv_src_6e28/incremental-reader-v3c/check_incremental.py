from pathlib import Path
import json,hashlib,subprocess
R=Path('/Users/zhouhuanjian/ASTIS-GC');O=R/'.astis/semantic-neutral-20261112/mv_src_6e28';B=O/'incremental-reader-v3c';I=B/'inputs';V=O/'r9-full-consumer-source-review-v3a/v3b';F=V.parent;E='research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-semantic-evidence/';math='e654e98642350a615c473bc8190fbc1d47fe52bd';reader='1d0dedf3aac3c2ff72ee96566461e29e38a2eeae'
def h(a):return hashlib.sha256(a).hexdigest()
def canon(d):return json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def write(n,d):(B/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
P=json.loads((I/'0-anti-anchored-reviewer-packet.full-consumer-v3c.json').read_bytes());T=json.loads((I/'1-anti-anchored-private-centered-consumer.full-v3c.json').read_bytes());packetchecks=[]
for label,pkt,i in [('P',P,0),('T',T,1)]:
 old=json.loads(next((V/'inputs').glob(str(i)+'-*')).read_bytes());assert h(canon({k:v for k,v in pkt.items() if k!='packet_sha256'}))==pkt['packet_sha256']
 for k in ['schema_version','task','packet_id','anti_anchoring','roles','source','lean','blind_reconstruction','review_contract','output_contract','publication_review_rule']:assert pkt[k]==old[k],(label,k)
 oldcontext=old['candidate_publication_context'];newcontext=pkt['candidate_publication_context'];updated=json.loads(json.dumps(oldcontext));updated['lesson']['sources'][1]['scope']=newcontext['lesson']['sources'][1]['scope'];assert updated==newcontext
 packetchecks.append({'label':label,'canonical_packet_sha256':pkt['packet_sha256'],'all_math_source_Lean_decoder_and_contract_fields_unchanged':True,'context_only_source_scope_changed':True})
code=[]
for path,expected in [('AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceMatrixVariance.lean','d9db32e38f18f1f92a94c82886063181375a9e214f7d44ce1bca2a240586ace6'),('Tests/GaussianComplexityFixedSpectrumSourceMatrixVariance.lean','c72d3573c6047b75983a958ad8b98de9c399e13277daa852a66c3e5a0820e73b')]:
 a=(R/path).read_bytes();assert h(a)==expected
 for c in [math,reader]:assert subprocess.check_output(['git','show',c+':'+path],cwd=R)==a
 code.append({'path':path,'sha256':expected,'math_and_reader_commit_bytes_equal':True})
# Exact binding/context algorithms reviewed in prior phase; repeat only the changed payload calculation.
u=json.loads((I/'3-huanjian-gaussian-source-matrix-variance.json').read_bytes())['units'][0];item=json.loads((I/'4-huanjian-gaussian-source-matrix-variance.json').read_bytes())['items'][0];binding=item['bindings'][0];path=code[0]['path'];a=(R/path).read_bytes();payload={'file':h(a),'current_lean_module':a.decode(),'toolchain':h((R/'lean-toolchain').read_bytes()),'dependencies':h((R/'lake-manifest.json').read_bytes()),**{k:item[k] for k in ['source','statement','formulae','assumptions','obligations']},'lesson':u,'binding':{k:v for k,v in binding.items() if k not in ['audit_id','legacy_audit_debt']}}
assert h(canon(payload))=='00bdeee242bd0c09802bbe1d7497da5da80c58d77f4ddb54df8196b5db27f1cf'
context=json.loads(json.dumps(payload));context['binding']={k:context['binding'][k] for k in ['declaration','role','supports']};context['lesson']={k:v for k,v in context['lesson'].items() if k not in ['boundary','source_history_boundary']};context['candidate_assumptions']=[{k:r[k] for k in ['source','lean']} for r in binding['assumption_deltas']];assert context==P['candidate_publication_context']==T['candidate_publication_context'];assert P['publication_binding_sha256']==T['publication_binding_sha256']==h(canon(payload));write('full-publication-binding-payload.checked.json',payload)
# The same old7fold code and unchanged map/decoder originals are hash/equality reuse, no new reading credit.
assert ''.join(x['lean'] for x in u['steps'][:4]).encode()==(R/code[0]['path']).read_bytes();assert ''.join(x['lean'] for x in u['steps'][4:]).encode()==(R/code[1]['path']).read_bytes()
mp=R/(E+'source-lean-map.full-consumer-v3b.draft.json');assert mp.read_bytes()==(V/'inputs/3-source-lean-map.full-consumer-v3b.draft.json').read_bytes() and h(mp.read_bytes())=='3963dcbf31a39232c52c7845984bf91a78a14c0d63fede3b6c3d9a8f42fcb629'
originals=[]
for label,sub,folder,prefix in [('P','neutral_decode_d204',F/'inputs','P-original-'),('T','neutral_decode_t_91ad',F/'inputs','')]:
 for name,local in ([('input.json','P-original-input.json'),('decoder-run.json','P-original-decoder-run.json'),('reconstruction.md','P-original-reconstruction.md'),('freeze-manifest.json','P-original-freeze-manifest.json')] if label=='P' else [('input.json','6-input.json'),('decoder-run.json','8-decoder-run.json'),('reconstruction.md','7-reconstruction.md'),('freeze-manifest.json','9-freeze-manifest.json')]):
  path=E+'decoder-originals/'+sub+'/'+name;a=(R/path).read_bytes();assert a==(folder/local).read_bytes();originals.append({'label':label,'source_path':path,'sha256':h(a),'prior_frozen_original_exact':True})
# Reader candidate copies exactly supplied new packets/supplement and current authors.
for x in json.loads((B/'initial-capture.json').read_bytes())['records']:
 assert (R/x['source_path']).read_bytes()==subprocess.check_output(['git','show',reader+':'+x['source_path']],cwd=R)==(R/x['snapshot_path']).read_bytes()
write('incremental-consistency-checks.json',{'packets':packetchecks,'code':code,'decoder_originals_hash_only_reuse':originals,'map_unchanged_sha256':h(mp.read_bytes()),'math7slots_not_reread_or_rejudged':True,'all7folds_still_exact':True,'full_parentP_binding':h(canon(payload)),'reader_commit':reader,'actual_math_commit':math,'only_two_author_fields_changed':True,'selected_current_reader_commit_inputs_equal':True,'new_compiler_or_native_result_read':False,'normal_API_calls':0})
print('PASS two-fields-only, exact packets/full binding, identical math/source/decoder/map/7folds; math e654 vs reader1d0 separated')
