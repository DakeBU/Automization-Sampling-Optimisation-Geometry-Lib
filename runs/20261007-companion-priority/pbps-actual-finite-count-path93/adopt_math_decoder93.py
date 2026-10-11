from pathlib import Path
import hashlib,json,sys
root=Path(__file__).resolve().parents[3];run=Path(__file__).resolve().parent
sys.path.insert(0,str(root/'tools'));import astis_semantic_roundtrip as rt
load=lambda p:json.loads(p.read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def fresh(p,x):assert not p.exists(),p;save(p,x)
math=run/'independent-whole-math93';manifest=math/'closed-RAW93.native.json'
assert sha(manifest.read_bytes())=='33bd0320a4606db9df17ae8f0746a26c9939625dc86faa51ea3d8828871f191c'
for x in load(manifest)['artifacts']:
    p=root/x['path'];assert sha(p.read_bytes())==x['raw_sha256'] and p.stat().st_size==x['bytes'],x['path']
decision=load(math/'whole-math-decision93.native.json')
assert decision['decision']=='ACCEPT_EXACT_SEALED_WHOLE_MODULE_MATHEMATICS_AND_KERNEL'
assert sha((math/'exposition-supplement93.native.json').read_bytes())=='82d2033a4f27a71e9c0e05fa8a4522f0757570c800609bf1f44c8a3d02ac8ea0'
out=root/'runs/semantic-roundtrip/anonymous93/v2/decoder';closed=out/'raw-manifest.json'
assert sha(closed.read_bytes())=='a702b1c574d2b39e80e40c498105261cb1b217b60bb7ac1937b71cf269b6c5e9'
dm=load(closed);n=load(out/'decoder-report.json')
for x in dm['inputs']+dm['artifacts']:assert sha(Path(x['path']).read_bytes())==x['sha256'],x['path']
assert not dm['source_text_visible'] and not n['source_text_visible']
runhash=rt.sha256_json({k:v for k,v in n.items() if k!='decoder_run_sha256'})
assert runhash==n['decoder_run_sha256']==dm['decoder_run_sha256']
packet_path=out.parent/'input.json';packet=load(packet_path)
assert packet['packet_sha256']==rt.sha256_json({k:v for k,v in packet.items() if k!='packet_sha256'})==n['packet_sha256']
text=(out/'reconstructed-theorem.txt').read_text(encoding='utf8');assert sha(text.encode())==n['reconstructed_text_sha256']==dm['reconstructed_text_sha256']
ap=root/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualFiniteCountPath.json';a=load(ap)
assert a['state']=='draft' and rt.decoder_packet(a)==packet
fresh(run/'audit.before-adoption93.json',a)
a['lean']['statement_representation'].update(kernel_header_and_literal_expansion_checked=True,independent_kernel_evidence=(math/'whole-math-decision93.native.json').relative_to(root).as_posix())
a.update(state='blind-reconstructed',reconstruction=dict(text=text,text_sha256=n['reconstructed_text_sha256'],decoder=n['decoder'],decoder_run_sha256=runhash,decoder_packet_sha256=packet['packet_sha256'],source_text_visible=False,lean_statement_sha256=a['lean']['statement_sha256'],input_artifacts=packet['input_artifacts'],observed_input_artifacts=[dict(path=packet_path.relative_to(root).as_posix(),raw_sha256=sha(packet_path.read_bytes()))],run_artifact=(out/'decoder-report.json').relative_to(root).as_posix(),native_named_payload_sha256=sha((out/'decoder-report.json').read_bytes()),native_run_manifest_RAW_sha256=sha(closed.read_bytes()),native_structured_payload=(out/'decoder-report.json').relative_to(root).as_posix(),native_semantic_slots={k:n[k] for k in ['objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies']},run_hash_recipe=dm['decoder_run_hash_rule']))
assert rt.decoder_packet(a)==packet
review=rt.semantic_reviewer_packet(a);save(ap,a)
fresh(run/'root.math93.adoption.json',dict(status='INDEPENDENT_WHOLE_MATH_KERNEL_EXPOSITION_ONLY',manifest_raw_sha256=sha(manifest.read_bytes()),decision_raw_sha256=sha((math/'whole-math-decision93.native.json').read_bytes()),exposition_raw_sha256=sha((math/'exposition-supplement93.native.json').read_bytes()),source_verdict=False,exact_commit_verified=False,VERIFIED=False))
fresh(run/'root.decoder93.adoption.json',dict(status='BLIND_RECONSTRUCTION_ONLY',native_manifest_raw_sha256=sha(closed.read_bytes()),canonical_packet_sha256=packet['packet_sha256'],decoder_run_sha256=runhash,context_correction_only=True,old_packet_and_report_retained=True,source_verdict=False,VERIFIED=False))
fresh(run/'anti-anchored.review93.json',review)
print(json.dumps(dict(status='adopted independent math and blind reconstruction only',review_packet=review['packet_sha256'],review_raw=sha((run/'anti-anchored.review93.json').read_bytes()))))
