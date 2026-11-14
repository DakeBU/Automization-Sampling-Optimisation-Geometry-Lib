from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,'tools')
import astis_semantic_roundtrip as rt
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-radius-semantic-evidence')
A=Path('research-wiki/semantic-roundtrip/audits/huanjian-gaussian-source-matrix-radius.json')
base=Path('.astis/semantic-neutral-20261113')
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
def create(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b)
audits=[json.loads(A.read_bytes()),json.loads((W/'private-consumer-audit.bound.v2.json').read_bytes())]
receipts=[]
for a,(d,m,packet) in zip(audits,[('out_8d49','manifest.json','anonymous-P.json'),('out_47a2','output_manifest.json','anonymous-T.json')]):
    root=base/d;mf=json.loads((root/m).read_bytes())
    rows=mf.get('artifacts') or [{'path':k,**v} for k,v in mf['payload_artifacts'].items()]
    for row in rows:
        b=(root/row['path']).read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256']
    out=json.loads((root/'result.json').read_bytes());anon=json.loads((W/packet).read_bytes())
    assert out['source_text_visible'] is False
    assert out['canonical_packet_sha256']==anon['packet_sha256']==rt.decoder_packet(a)['packet_sha256']
    assert out['reconstructed_text_sha256']==rt.sha256_text(out['reconstructed_theorem_text'])
    assert out['input_artifacts']==anon['input_artifacts']
    assert sha((root/'decoder_run.json').read_bytes())==out['decoder_run_sha256']
    dest=E/'decoder-originals'/d
    for p in sorted(root.iterdir()):
        assert p.is_file();create(dest/p.name,p.read_bytes())
    a['reconstruction']={'text':out['reconstructed_theorem_text'],'text_sha256':out['reconstructed_text_sha256'],'decoder':out['decoder'],'decoder_run_sha256':out['decoder_run_sha256'],'decoder_packet_sha256':out['canonical_packet_sha256'],'source_text_visible':False,'lean_statement_sha256':a['lean']['statement_sha256'],'input_artifacts':out['input_artifacts'],'run_artifact':str(dest/'result.json')}
    a['state']='blind-reconstructed'
    receipts.append({'role':d,'input_packet_sha256':out['canonical_packet_sha256'],'reconstruction_sha256':out['reconstructed_text_sha256'],'decoder_run_sha256':out['decoder_run_sha256'],'original_files':len(list(root.iterdir()))})
A.write_bytes(dump(audits[0]))
create(W/'private-consumer-audit.reconstructed.v1.json',dump(audits[1]))
create(W/'private-consumer-registry.reconstructed.v1.json',dump({'schema_version':1,'audits':[audits[1]]}))
create(E/'decoder-originals/custody.json',dump({'byte_exact_inputs_and_outputs_verified':receipts,'source_text_visible':False,'fidelity_verdict':'not supplied by decoder or ROOT'}))
print(json.dumps(receipts))
