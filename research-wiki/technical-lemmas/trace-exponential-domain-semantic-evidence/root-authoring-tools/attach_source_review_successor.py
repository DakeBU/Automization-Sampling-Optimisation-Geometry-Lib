from pathlib import Path
import json,hashlib,copy
r=Path.cwd();w=r/'.astis/huanjian-gc-trace-mgf-domain-20261115'
e=r/'research-wiki/technical-lemmas/trace-exponential-domain-semantic-evidence'
s=r/'.astis/semantic-neutral-20261115/trace_exp_fresh_source_51c8'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected={'phase1_public_leaf_manifest.json':'18cdaa53c656a27d1eeb986780843a0b91bf2cd8fc4c41794318f9db7915f870',
 'phase2_public_leaf_manifest.json':'b8b31c57b46cfd02030359979366a8843f2cd1fd6653502ad3c5f0e46c539720',
 'phase3_public_leaf_manifest.json':'c4fc2608cb0247dbb490796cd4280aa1b6b6ba33123dfea26d889a77296987dc'}
dest=e/'source-review/trace_exp_fresh_source_51c8/originals';assert not dest.exists();dest.mkdir(parents=True)
selected={}
for name,h in expected.items():
    p=s/name;assert sha(p)==h
    for x in json.loads(p.read_text())['public_leaves']:
        q=r/x['path'];assert q.is_relative_to(s) and sha(q)==x['sha256']
        assert q.name not in selected or selected[q.name]==q
        selected[q.name]=q
    selected[name]=p
for name,p in selected.items():(dest/name).write_bytes(p.read_bytes())
rows=[{'original':str(p.relative_to(r)),'public_byte_exact_copy':str((dest/n).relative_to(r)),
    'bytes':p.stat().st_size,'sha256':sha(p)} for n,p in sorted(selected.items())]
(dest.parent/'ROOT-byte-exact-reference-resolution.v1.json').write_text(json.dumps({
    'kind':'ROOT-later-byte-exact-explicit-source-review-copy',
    'scope':'Only three independent allowlists and their explicit public leaves; raw full sources/images/scripts/guards/registry/index/cache excluded. Original actor files unchanged; no new verdict emitted.',
    'files':rows},ensure_ascii=False,indent=2)+'\n')
pack=e/'semantic-packets-originals';assert not pack.exists();pack.mkdir()
for name in ['P.reviewer-packet.v1.json','T.reviewer-packet.v1.json','P.reviewer-packet.v2.json','T.reviewer-packet.v2.json',
 'publication-context.authored-v3.original.json','publication-context.authored-v4.original.json']:
    (pack/name).write_bytes((w/name).read_bytes())
ap=r/'research-wiki/semantic-roundtrip/audits/huanjian-trace-exponential-domain.json'
rp=w/'private-consumer-audit.registry.json'
pa=json.loads(ap.read_text());reg=json.loads(rp.read_text());ta=reg['audits'][0]
for a,k,resultsha in [(pa,'P','aa3f55d76f8e5b2293f5422595096b3ce2653f7c2c41bd6bf4047e115055ef1b'),
    (ta,'T','e24f30c0afeefa77e24c419aa07c996fb461b38bccacd8e1e893537115359af3')]:
    p=dest/f'phase3_{k}_successor_raw_review_result.json';assert sha(p)==resultsha
    v=json.loads(p.read_text());packet=json.loads((w/f'{k}.reviewer-packet.v2.json').read_text())
    assert v['reviewer_packet_sha256']==packet['packet_sha256']
    assert v['publication_binding_sha256']==a['publication_binding_sha256']=='e44190bca918ce5a1e8f4ff5fc942c56ea400deb7a10af9929a698ef22a9d45c'
    assert v['verdict']=='equivalent-after-elaboration' and v['independent_from_formalizer'] is True and v['independent_from_decoder'] is True
    assert v['reviewer'] not in [a['lean']['formalizer'],a['reconstruction']['decoder']]
    assert not v['deltas'] and not v['repairs'] and a['state']=='draft'
    a['state']='source-reviewed';a['semantic_slots']=v['semantic_slots'];a['deltas']=v['deltas'];a['verdict']=v['verdict'];a['repairs']=v['repairs']
    a['source_review']={'state':'accepted','reviewer':v['reviewer'],
        'independent_from_formalizer':True,'independent_from_decoder':True,
        'reviewer_packet_sha256':v['reviewer_packet_sha256'],'evidence':v['review_evidence'],
        'review_run_sha256':v['review_run_sha256'],'run_artifact':str(p.relative_to(r)),
        'original_full_review_run_sha256':'f5cbc9dac309eda9127f3551b368c6bd2d2765e5793947f7e59d7d44a1cd212c',
        'successor_scope':'Independent exact six citation-scope additions only; original full source/wholemodule/seven-slot review unchanged and retained.'}
    a['binding_status']='CURRENT_SOURCE_REVIEW_ACCEPTED; READER_RUNTIME_AND_NORMAL_PL_V_PENDING'
    a['lean']['compiler_evidence']=str((e/'local-mathematics-checkpoint.v1.json').relative_to(r))
    a['lean']['independent_native_evidence']['file']=str((e/'independent-native-and-preproof-originals/readable-native-originals/native-mathematics-report.v1.json').relative_to(r))
ap.write_text(json.dumps(pa,ensure_ascii=False,indent=2)+'\n');reg['audits']=[ta]
rp.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
(e/'private-consumer-audit.source-reviewed.v2.json').write_text(json.dumps(ta,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'current_binding':pa['publication_binding_sha256'],'public_and_private':'source-reviewed',
    'copied_explicit_original_leaves':len(rows),'normal_PL_calls':0,'normal_V_calls':0,
    'reader_runtime':'pending','normal_Conceptual_Discovery':'raw'}))
