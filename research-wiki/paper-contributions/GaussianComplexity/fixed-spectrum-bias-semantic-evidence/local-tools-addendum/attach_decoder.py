from pathlib import Path
import json, hashlib, sys
sys.dont_write_bytecode=True;sys.path.insert(0,'tools')
import astis_semantic_roundtrip as rt
W=Path('.astis/huanjian-gc-fixed-spectrum-bias-20261110')
E=Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-bias-semantic-evidence')
D=Path('.astis/semantic-neutral-20261110/b7e604')
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda x:(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def put(p,b):
    assert not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
assert sha((D/'frozen-sha256-manifest.json').read_bytes())=='66150144b53bd264cef81d36988ba3b766257fb1182a191f0dc2256aab4bebda'
f=json.loads((D/'frozen-sha256-manifest.json').read_bytes())
for rel,r in f['files'].items():assert sha((D/rel).read_bytes())==r['sha256']
r=json.loads((D/'decoder-run.json').read_bytes())
assert r['actor_identity']=='/root/decoder_b7e604' and r['source_text_visible'] is False
assert sha((D/'decoder-run.json').read_bytes())=='b30fe6fa600e6b5725d13f42cce2777d59616b9de56d5f1a3e783c2e8efc650c'
rec=json.loads((D/'reconstruction.json').read_bytes());text=rec['reconstructed_theorem_text']
assert sha(text.encode())==r['reconstructed_text_sha256']==rec['reconstructed_text_sha256']
p=Path('research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-bias.json')
old=p.read_bytes();a=json.loads(old);assert a['state']=='draft' and a['reconstruction']=={}
packet=rt.decoder_packet(a)
assert packet['packet_sha256']==r['packet_sha256'] and sha((D/'input.json').read_bytes())==r['input_raw_sha256']
a['state']='blind-reconstructed'
a['reconstruction']={'text':text,'text_sha256':sha(text.encode()),'decoder':r['actor_identity'],'source_text_visible':False,'lean_statement_sha256':a['lean']['statement_sha256'],'decoder_packet_sha256':packet['packet_sha256'],'decoder_run_sha256':sha((D/'decoder-run.json').read_bytes()),'input_artifacts':packet['input_artifacts'],'ambient_cues_disclosed':r['ambient_exposure'],'zero_ambient_cues_claimed':False}
for x in sorted(D.iterdir()):
    if x.is_file():put(E/'independent-decoder-b7e604'/x.name,x.read_bytes())
put(E/'audit-before-independent-reconstruction.raw.json',old);p.write_bytes(dump(a))
full=rt.semantic_reviewer_packet(a)
assert all(x is False for x in full['anti_anchoring'].values())
put(E/'fresh-source-reviewer-packet.json',dump(full))
s=json.loads((W/'statement-seal-v1.json').read_bytes())
head,body=s['actual_private_consumer']['signature'].split(' :\n',1)
consumer='∀'+head.removeprefix('private theorem actual_gaussian_zero_threshold_probability_le')+',\n'+body
white={'schema_version':1,'task':'selective-source-statement-reconstruction-comparison','parent_canonical_packet_sha256':full['packet_sha256'],'source':{k:full['source'][k] for k in ['source_id','anchor','original_text','text_sha256']},'lean_statement':{k:full['lean'][k] for k in ['statement','statement_sha256']},'approved_definition_context':a['lean']['decoder_context'],'blind_reconstruction':{k:full['blind_reconstruction'][k] for k in ['text','text_sha256','decoder','decoder_packet_sha256','decoder_run_sha256','source_text_visible']},'private_consumer_statement':consumer}
assert b' := by' not in dump(white)
put(W/'strict-selective-phase2-input.json',dump(white));put(E/'strict-selective-phase2-input.json',dump(white))
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-bias.json')
c=json.loads(C.read_bytes());c['parents']=['ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-exact-means','ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-variances']
c['reuse_plan']['reused_declarations'] += ['Real.hasDerivAt_half_log_one_add_div_one_sub_sub_sum_range','intervalIntegral.integral_eq_sub_of_hasDerivAt','intervalIntegral.integral_mono_on','meas_ge_le_variance_div_sq']
C.write_bytes(dump(c))
print(json.dumps({'state':'blind-reconstructed','full_reviewer_packet_canonical_sha256':full['packet_sha256'],'strict_whitelist_raw_sha256':sha(dump(white)),'source_review_or_sourceV':False}))
