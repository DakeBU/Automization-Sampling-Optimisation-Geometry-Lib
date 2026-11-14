from pathlib import Path
import json,hashlib,shutil,subprocess
r=Path.cwd();w=r/'.astis/huanjian-gc-matrix-laplace-20261114'
anon=r/'.astis/semantic-neutral-20261114/anon_6f91'
e=r/'research-wiki/technical-lemmas/matrix-laplace-tail-semantic-evidence/decoder-originals/anon_6f91'
assert not e.exists()
for name in ['input','output']:
    shutil.copytree(anon/name,e/name)
def attach(a,n):
    p=e/'output'/str(n)/'result.json';v=json.loads(p.read_text())
    pkt=json.loads((e/'input'/(str(n)+'.json')).read_text())
    assert v['source_text_visible'] is False
    assert v['reconstructed_text_sha256']==hashlib.sha256(v['reconstructed_theorem_text'].encode()).hexdigest()
    assert v['packet_sha256']==pkt['packet_sha256']
    a['reconstruction']={'text':v['reconstructed_theorem_text'],
      'text_sha256':v['reconstructed_text_sha256'],'decoder':v['decoder'],
      'decoder_run_sha256':v['decoder_run_sha256'],'decoder_packet_sha256':v['packet_sha256'],
      'source_text_visible':False,'lean_statement_sha256':a['lean']['statement_sha256'],
      'input_artifacts':v['input_artifacts'],'run_artifact':str(p.relative_to(r))}
    return a
p=r/'research-wiki/semantic-roundtrip/audits/huanjian-matrix-laplace-tail.json'
a=attach(json.loads(p.read_text()),1);p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
p=w/'private-consumer-audit.registry.json';reg=json.loads(p.read_text());reg['audits'][0]=attach(reg['audits'][0],2)
p.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
subprocess.run(['python3','tools/astis_semantic_roundtrip.py','reviewer-packet','--audit-id',a['id'],'--output',str(w/'P.reviewer-packet.v1.json')],check=True)
subprocess.run(['python3','tools/astis_semantic_roundtrip.py','--registry',str(p),'reviewer-packet','--audit-id',reg['audits'][0]['id'],'--output',str(w/'T.reviewer-packet.v1.json')],check=True)
print(json.dumps({'independent_decodes_copied_byte_exact':True,'source_verdict_still_pending':True}))
