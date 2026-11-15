from pathlib import Path
import hashlib,json,subprocess
r=Path.cwd();w=r/'.astis/huanjian-gc-trace-mgf-domain-20261115'
s=r/'.astis/semantic-neutral-20261115/blind_decoder_8a39'
e=r/'research-wiki/technical-lemmas/trace-exponential-domain-semantic-evidence/decoder-originals/blind_decoder_8a39'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(s/'packet-a.decoder-result.v1.json')=='711e3be4861f66da173a698cf5c88bb483c213e2a3fcdb428de878daf3a391f9'
assert sha(s/'packet-b.decoder-result.v1.json')=='e0b7872c90fb8f217e6d31e211b2e452b0538bb5297be3c80c722245348f8879'
names=['independent_decode.v1.py','verification-receipt.v1.json']
for k in ['a','b']:
    names += [f'packet-{k}.{tail}' for tail in ['decoder-result.v1.json','decoder-run.v1.json','reconstructed-theorem.v1.txt','translation-notes.v1.txt']]
assert not e.exists();e.mkdir(parents=True)
for name in names:(e/name).write_bytes((s/name).read_bytes())
for k in ['a','b']:(e/f'packet-{k}.anonymous.v1.json').write_bytes((w/f'packet-{k}.anonymous.v1.json').read_bytes())
def attach(a,k):
    p=e/f'packet-{k}.decoder-result.v1.json';v=json.loads(p.read_text())
    pkt=json.loads((w/f'packet-{k}.anonymous.v1.json').read_text())
    assert v['source_text_visible'] is False and v['decoder']=='trace_domain_blind_decoder_8a39'
    assert v['reconstructed_text_sha256']==hashlib.sha256(v['reconstructed_theorem_text'].encode()).hexdigest()
    assert v['packet_sha256']==pkt['packet_sha256'] and v['input_artifacts']==pkt['input_artifacts']
    assert v['decoder_run_sha256']==sha(e/f'packet-{k}.decoder-run.v1.json')
    assert a['state']=='draft' and not a['reconstruction']
    a['reconstruction']={'text':v['reconstructed_theorem_text'],'text_sha256':v['reconstructed_text_sha256'],
        'decoder':v['decoder'],'decoder_run_sha256':v['decoder_run_sha256'],
        'decoder_packet_sha256':v['packet_sha256'],'source_text_visible':False,
        'lean_statement_sha256':a['lean']['statement_sha256'],'input_artifacts':v['input_artifacts'],
        'run_artifact':str(p.relative_to(r))}
    return a
ap=r/'research-wiki/semantic-roundtrip/audits/huanjian-trace-exponential-domain.json'
a=attach(json.loads(ap.read_text()),'a');ap.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
rp=w/'private-consumer-audit.registry.json';reg=json.loads(rp.read_text());reg['audits'][0]=attach(reg['audits'][0],'b')
rp.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
subprocess.run(['python3','tools/astis_semantic_roundtrip.py','reviewer-packet','--audit-id',a['id'],'--output',str(w/'P.reviewer-packet.v1.json')],check=True)
subprocess.run(['python3','tools/astis_semantic_roundtrip.py','--registry',str(rp),'reviewer-packet','--audit-id',reg['audits'][0]['id'],'--output',str(w/'T.reviewer-packet.v1.json')],check=True)
print(json.dumps({'independent_decodes_preserved_byte_exact':True,'source_review_still_pending':True,
    'P_reviewer_packet_file_sha256':sha(w/'P.reviewer-packet.v1.json'),
    'T_reviewer_packet_file_sha256':sha(w/'T.reviewer-packet.v1.json')}))
