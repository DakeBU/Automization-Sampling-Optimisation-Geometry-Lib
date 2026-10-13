from pathlib import Path
import hashlib,json,sys
ROOT=Path('E:/Samplinglib');RUN=Path(__file__).parent
sys.path.insert(0,str(ROOT/'tools'))
import astis_semantic_roundtrip as rt
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
def fresh(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
out=ROOT/'runs/semantic-roundtrip/anonymous91/decoder-output'
expected={'reconstruction.json':'8ca96b1f7990d59bf7859c4db2325b465f41c123063a78577d407729c53b815d',
          'run.json':'2a35e174d0ae1b44c50a86c5efa0ebeeb9bdaba2e3b3f7968f24f86659a55621',
          'raw-manifest.json':'11c68218192db678a36c147fd675921620d7b85d3557553ec1acdfb043e473bd'}
for f,h in expected.items():assert sha((out/f).read_bytes())==h
m=load(out/'raw-manifest.json');n=load(out/'reconstruction.json');run=load(out/'run.json')
assert m['closed'] and not n['source_text_visible'] and not run['other_mathematical_inputs_read']
for x in m['inputs']+m['outputs']:
    b=Path(x['path']).read_bytes();assert sha(b)==x['sha256']
    if 'bytes' in x:assert len(b)==x['bytes']
packet=load(ROOT/'runs/semantic-roundtrip/anonymous91/input.json')
assert packet['packet_sha256']==rt.sha256_json({k:v for k,v in packet.items() if k!='packet_sha256'})
assert n['decoder_run_sha256']==expected['run.json']
text=n['reconstructed_theorem_text']
assert sha(text.encode())==n['reconstructed_text_sha256']==run['reconstructed_text_sha256']
ap=ROOT/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualAbsoluteNextEventTime.json'
a=load(ap);assert a['state']=='draft' and rt.decoder_packet(a)==packet
(RUN/'audit.before-decoder91.json').write_bytes(ap.read_bytes())
a.update(state='blind-reconstructed',reconstruction=dict(text=text,text_sha256=n['reconstructed_text_sha256'],
    decoder='/root/blind_decoder91',decoder_run_sha256=expected['run.json'],decoder_packet_sha256=packet['packet_sha256'],
    source_text_visible=False,lean_statement_sha256=a['lean']['statement_sha256'],input_artifacts=packet['input_artifacts'],
    observed_input_artifacts=[dict(path=m['inputs'][0]['path'],raw_sha256=m['inputs'][0]['sha256'])],
    run_artifact=(out/'run.json').relative_to(ROOT).as_posix(),native_named_payload_sha256=expected['reconstruction.json'],
    native_run_manifest_RAW_sha256=expected['raw-manifest.json'],unresolved_semantics=[],
    native_semantic_uncertainties=n['important_uncertainties'],
    native_structured_payload=(out/'reconstruction.json').relative_to(ROOT).as_posix(),
    run_hash_recipe='Exact native run bytes. Source-blind decoder reports compilation only from packet; independent mathematics/kernel review supplies compiler evidence. Root independently verifies canonical packet hash; original decoder uncertainty retained.'))
ap.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
fresh(RUN/'root.decoder91.adoption.json',dict(status='BLIND_RECONSTRUCTION_ONLY',native_hashes=expected,
    canonical_packet_hash_verified=True,canonical_packet_sha256=packet['packet_sha256'],
    semantic_uncertainties_retained=n['important_uncertainties'],source_verdict=False,VERIFIED=False))
fresh(RUN/'anti-anchored.review91.json',rt.semantic_reviewer_packet(a))
print('Blind reconstruction adopted; canonical anti-anchored packet written. No source verdict.')
