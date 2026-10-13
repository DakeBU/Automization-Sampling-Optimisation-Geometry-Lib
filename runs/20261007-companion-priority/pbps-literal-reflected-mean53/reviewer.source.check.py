from pathlib import Path
import json, hashlib, datetime
root=Path('E:/Samplinglib');p=Path(__file__).parent
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def J(path):return json.loads(Path(path).read_bytes())
def abs_path(x):
    z=Path(x);return z if z.is_absolute() else root/z
def fp(path):
    z=abs_path(path);b=z.read_bytes();return dict(path=str(z),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')),bytes=len(b))
lease=J(p/'source.review.lease.json');packet=J(p/'source.0.reviewer-packet.json');errors=[]
for x in lease['input_artifacts']:
    z=fp(x['path'])
    for k in ['raw_sha256','lf_sha256','bytes']:
        if k in x and z[k]!=x[k]:errors.append([x['path'],k])
assert not errors,errors
z=dict(packet);z.pop('packet_sha256');assert sha(canon(z))==packet['packet_sha256']==lease['reviewer_packet_sha256']
prod=abs_path(packet['lean']['file']);text=prod.read_text(encoding='utf-8')
assert text==packet['candidate_publication_context']['current_lean_module']
header=text[text.index('theorem reflected_gibbs_mean_c1'):text.index('\n := by')].rstrip()+'\n'
seal=(root/'runs/20261007-companion-priority/pbps-reflected-density-preproof53/prospective-statement.txt').read_text(encoding='utf-8')
assert header==seal and sha(header.encode())=='43d2831fa373729dc44cfd575fa4e1b68b2462688db8445320f13e433ddbe23e'
statement=header[header.index('\n'):].rstrip()
assert statement==packet['lean']['statement']
assert sha(statement.encode())==packet['lean']['statement_sha256']
lesson=J(root/'website/content/declaration_lessons/pbps-literal-reflected-mean.json')['units'][0]
pub=J(root/'website/content/publications/pbps-literal-reflected-mean.json')['items'][0]
binding=next(x for x in pub['bindings'] if x['declaration']==packet['lean']['declaration'])
payload=dict(file=sha(text.encode()),current_lean_module=text,toolchain=sha((root/'lean-toolchain').read_text(encoding='utf-8').encode()),dependencies=sha((root/'lake-manifest.json').read_text(encoding='utf-8').encode()),source=pub['source'],statement=pub['statement'],formulae=pub['formulae'],assumptions=pub['assumptions'],obligations=pub['obligations'],lesson=lesson,binding={k:v for k,v in binding.items() if k not in ['audit_id','legacy_audit_debt']})
binding_sha=sha(canon(payload));assert binding_sha==packet['publication_binding_sha256']
ctx=dict(payload);ctx['binding']={k:payload['binding'][k] for k in ['declaration','role','supports']};ctx['lesson']={k:v for k,v in lesson.items() if k not in ['boundary','source_history_boundary']};ctx['candidate_assumptions']=[{k:x[k] for k in ['source','lean']} for x in binding.get('assumption_deltas',[])]
assert ctx==packet['candidate_publication_context']
audit=J(root/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261008-PBPSLiteralReflectedMean.json')
assert audit['publication_context']==ctx and audit['publication_binding_sha256']==binding_sha
result=J(p/'anonymous-decoder/result0.json');run=J(p/'anonymous-decoder/run.json');bp=J(p/'anonymous-decoder/packet0.json');rec=audit['reconstruction']
z=dict(run);z.pop('run_sha256');assert sha(canon(z))==run['run_sha256']
assert sha(canon(run['run_binding_payload']))==run['decoder_run_sha256']==result['decoder_run_sha256']==packet['blind_reconstruction']['decoder_run_sha256']
assert result['reconstructed_theorem_text']==packet['blind_reconstruction']['text']==rec['text']
assert sha(result['reconstructed_theorem_text'].encode())==rec['text_sha256']==result['reconstructed_text_sha256']
assert result['decoder']==rec['decoder']==packet['roles']['blind_decoder']
assert rec['input_artifacts']==['lean-statement','approved-definition-context']
assert run['exposures']['source_text_visible'] is False and run['exposures']['strict_source_identity_blindness'] is False
for x in run['input_artifacts']+run['output_artifacts']:
    neutral=Path(x['path']).name;z=fp(p/'anonymous-decoder'/neutral)
    for k in ['raw_sha256','lf_sha256','bytes']:assert z[k]==x[k]
assert (p/'source.review.primary-first.contract.json').read_bytes()==(root/'runs/20261007-companion-priority/phase-pbps-primary-preread53/primary.contract.json').read_bytes()
assert len(lesson['steps'])==6
assert all('\\\\' not in x['formula'] for x in lesson['steps'])
checks=dict(schema='native-source53-byte-binding-checks/v1',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),strict_initial_inputs=506,all_raw_LF_match=True,exact758_LF_statement_match=True,statement_sha256=packet['lean']['statement_sha256'],reviewer_packet_sha256_recomputed=packet['packet_sha256'],publication_binding_sha256_recomputed=binding_sha,full_publication_payload_recipe='Authorized tools/astis_publication.py47-115; normalized UTF8 wholemodule/toolchain/manifest, full unprojected lesson and all binding keys except audit_id/legacy_audit_debt; sorted compact ensure_ascii=False.',projection_exact=True,whole_module_LF_sha256=sha(text.encode()),decoder_complete_run_logical_sha256_recomputed=run['run_sha256'],decoder_binding_payload_sha256_recomputed=run['decoder_run_sha256'],decoder_source_text_visible=False,decoder_strict_source_identity_blindness=False,decoder_native_text_verbatim=True,decoder_observations_and_portable_bytes_match=True,formula_steps=6,errors=[],compiler_invocations=0)
(p/'reviewer.source.checks.json').write_bytes((json.dumps(checks,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps(checks,ensure_ascii=False))
