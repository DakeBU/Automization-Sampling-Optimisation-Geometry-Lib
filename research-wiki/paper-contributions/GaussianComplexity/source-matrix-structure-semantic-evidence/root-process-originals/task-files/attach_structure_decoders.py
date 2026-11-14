from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,'tools')
import astis_semantic_roundtrip as rt
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-structure-semantic-evidence')
A=Path('research-wiki/semantic-roundtrip/audits/huanjian-gaussian-source-matrix-structure.json')
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
def create(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b)
audits=[json.loads(A.read_bytes()),json.loads((W/'private-consumer-audit.bound.v1.json').read_bytes())]
records=[]
for a,n in zip(audits,['anon_328a','anon_96ec']):
 root=Path('.astis/semantic-neutral-20261113')/n
 out=json.loads((root/'result.json').read_bytes());packet=json.loads((root/'input.json').read_bytes())
 assert out['source_text_visible'] is False
 assert out['packet_sha256']==packet['packet_sha256']==rt.decoder_packet(a)['packet_sha256']
 assert out['reconstructed_text_sha256']==rt.sha256_text(out['reconstructed_theorem_text'])
 assert out['decoder_run_sha256']==sha((root/'reconstruction.md').read_bytes())
 for p in sorted(root.iterdir()):
  assert p.is_file();create(E/'decoder-originals'/n/p.name,p.read_bytes())
 a['reconstruction']={'text':out['reconstructed_theorem_text'],'text_sha256':out['reconstructed_text_sha256'],'decoder':out['decoder'],'decoder_run_sha256':out['decoder_run_sha256'],'decoder_packet_sha256':out['packet_sha256'],'source_text_visible':False,'lean_statement_sha256':a['lean']['statement_sha256'],'input_artifacts':out['input_artifacts'],'run_artifact':str(E/'decoder-originals'/n/'result.json')}
 a['state']='blind-reconstructed'
 records.append({'role':out['decoder'],'packet_sha256':out['packet_sha256'],'result_sha256':sha((root/'result.json').read_bytes()),'run_sha256':out['decoder_run_sha256'],'source_text_visible':False})
A.write_bytes(dump(audits[0]))
create(W/'private-consumer-audit.reconstructed.v1.json',dump(audits[1]));create(W/'private-consumer-registry.reconstructed.v1.json',dump({'schema_version':1,'audits':[audits[1]]}))
create(E/'decoder-originals/custody.json',dump({'original_decoder_artifacts_verified':records,'ROOT_semantic_verdicts':0}))
print(json.dumps(records))
