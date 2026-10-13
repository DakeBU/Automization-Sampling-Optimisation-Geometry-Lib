import copy,datetime,hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent;run=out.parent;repo=pathlib.Path(r'E:\Samplinglib')
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def put(n,d):(out/n).write_text(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
m=json.loads((out/'current-input-manifest.json').read_bytes())
def pin(n,p,role):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');(out/n).write_bytes(b);(out/(n+'.LF')).write_bytes(lf)
 m['inputs'].append(dict(name=n,original_path=str(p),role=role,RAW_bytes=len(b),RAW_sha256=sha(b),LF_bytes=len(lf),LF_sha256=sha(lf)));return b
for n,rel in [('schema.astis_semantic_roundtrip_core.RAW.py','tools/astis_semantic_roundtrip_core.py'),('schema.astis_publication.RAW.py','tools/astis_publication.py')]:
 pin(n,repo/rel,'only-canonical-schema-hash-and-binding-contract-reviewed; no-audit-registry-or-prior-verdict-read')
d=json.loads((out/'official.source.0.reviewer-packet.RAW.json').read_bytes());core=copy.deepcopy(d);del core['packet_sha256']
assert d['packet_sha256']==sha(canon(core))=='98e9a39c9f7eafea5a7a6660c162631fed010e9533ef2ab6debbdcdcd6405fc6'
assert all(x is False for x in d['anti_anchoring'].values())
assert d['roles']['formalizer']!='/root/independent_primary69'!=d['roles']['blind_decoder']
assert sha(d['source']['original_text'].encode('utf-8'))==d['source']['text_sha256']
assert sha(d['lean']['statement'].encode('utf-8'))==d['lean']['statement_sha256']
assert sha(d['blind_reconstruction']['text'].encode('utf-8'))==d['blind_reconstruction']['text_sha256']
assert d['blind_reconstruction']['source_text_visible'] is False
assert d['lean']['statement']==(out/'sealed.header0-expanded.lean').read_text(encoding='utf-8')[len('theorem actual_reflection_intertwining'):].rstrip('\r\n')
pub=json.loads((out/'final.publication.RAW.json').read_bytes())['items'][0];lesson=json.loads((out/'final.lesson.RAW.json').read_bytes())['units'][0]
old=json.loads((out/'current.lesson.RAW.json').read_bytes());restored=copy.deepcopy(lesson)
assert restored['helpers']==['AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionIntertwining.actual_reflection_intertwining_statement']
del restored['helpers'];restored['mathlib_dependencies'][-1]='Submodule.isSelfAdjoint_starProjection'
assert restored==old['units'][0]
binding={k:v for k,v in pub['bindings'][0].items() if k not in {'audit_id','legacy_audit_debt'}}
payload=dict(file=sha((out/'current.ReflectionIntertwining.RAW.lean').read_bytes()),current_lean_module=(out/'current.ReflectionIntertwining.RAW.lean').read_text(encoding='utf-8'),toolchain=sha((out/'current.lean-toolchain.RAW.LF').read_bytes()),dependencies=sha((out/'current.lake-manifest.RAW.json.LF').read_bytes()),source=pub['source'],statement=pub['statement'],formulae=pub['formulae'],assumptions=pub['assumptions'],obligations=pub['obligations'],lesson=lesson,binding=binding)
assert sha(canon(payload))==d['publication_binding_sha256']=='571c2916738f1981c5074a9a5f4e1cdf3efce3f94fafd26670566c70c3b25152'
context=copy.deepcopy(payload);context['binding']={k:context['binding'][k] for k in ['declaration','role','supports']}
context['lesson']={k:v for k,v in context['lesson'].items() if k not in ['boundary','source_history_boundary']}
context['candidate_assumptions']=[{k:row[k] for k in ['source','lean']} for row in binding['assumption_deltas']]
assert context==d['candidate_publication_context']
put('publication-binding.exact-payload.json',payload)
native=run/'anonymous-decoder';manifest=json.loads((native/'manifest.json').read_bytes());lease=json.loads((native/'lease.json').read_bytes())
assert lease['status']=='CLOSED_LAST' and lease['owned_regular_file_count']==17
assert sha((native/'manifest.json').read_bytes())==lease['manifest_raw_sha256']
verified=[]
for e in manifest['entries']:
 b=(native/e['path']).read_bytes();assert len(b)==e['raw_bytes'] and sha(b)==e['raw_sha256']
 verified.append(dict(path=e['path'],RAW_bytes=len(b),RAW_sha256=sha(b)))
assert len(verified)==15 and len(manifest['all_owned_files'])==17
for name in manifest['all_owned_files']:
 pin('decoder.native.'+name.replace('/','.')+'.RAW',native/name,'current-source-blind-native-CLOSED17-input-or-provenance; old-reviews-not-included')
pin('official.root.decoder69.adoption.RAW.json',run/'root.decoder69.adoption.json','root-copy-provenance-only; not-a-source-fidelity-verdict')
dr=json.loads((native/'review-run.json').read_bytes());dr_core=copy.deepcopy(dr);del dr_core['run_sha256']
assert sha(canon(dr_core))==dr['run_sha256']==lease['whole_logical_sha256']==d['blind_reconstruction']['decoder_run_sha256']=='e660f49813646393e7ccc2c927545e0ad62ef84f63cd10e0874c0adf00f2d05b'
nr=json.loads((native/'anonymous_reconstruction_69.json').read_bytes());assert nr['text']==d['blind_reconstruction']['text']
assert sha((native/'anonymous_reconstruction_69.json').read_bytes())=='95f81b646e7cdbecb588f14acd070caa65394cde323028a3b8291b408fbc8700'
neutral=json.loads((native/'inputs/packet0.raw.json').read_bytes());np=copy.deepcopy(neutral);del np['packet_sha256']
assert sha(canon(np))==neutral['packet_sha256']==d['blind_reconstruction']['decoder_packet_sha256']=='7c02491643e907ca8ea4af2ab9186d988ec9e83a13e3f4873e224a9e0840b93c'
assert neutral['statement']==d['lean']['statement']
assert set(nr)&set(d['review_contract']['semantic_slots'])==set(d['review_contract']['semantic_slots'])
m['count']=len(m['inputs']);put('current-input-manifest.json',m)
put('official-packet-binding-and-decoder-provenance.json',dict(schema='source69-official-packet-binding-validation-v1',actual_pid=os.getpid(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),reviewer_packet_canonical_sha256=d['packet_sha256'],reviewer_packet_RAW_sha256=sha((out/'official.source.0.reviewer-packet.RAW.json').read_bytes()),publication_binding_sha256=d['publication_binding_sha256'],full_current_module_context_exact=True,full_post_overlay_lesson_context_exact=True,only_two_approved_lesson_fields_changed=True,source_restated_text_sha256=d['source']['text_sha256'],expanded_Lean_statement_sha256=d['lean']['statement_sha256'],blind_reconstruction_text_sha256=d['blind_reconstruction']['text_sha256'],decoder_packet_canonical_sha256=neutral['packet_sha256'],decoder_whole_logical_sha256=dr['run_sha256'],decoder_native_named_RAW_sha256=sha((native/'anonymous_reconstruction_69.json').read_bytes()),decoder_native_manifest_RAW_sha256=sha((native/'manifest.json').read_bytes()),decoder_native_lease_RAW_sha256=sha((native/'lease.json').read_bytes()),decoder_native_closure_count=17,decoder_native_hashed_files=verified,decoder_role_independent=True,decoder_source_text_visible=False,anti_anchoring_flags_all_false=True,no_prior_source_semantic_decisions_in_packet=True,input_count=m['count']))
print(json.dumps(dict(actual_pid=os.getpid(),packet_sha256=d['packet_sha256'],publication_binding_sha256=d['publication_binding_sha256'],decoder_native_count=17,input_count=m['count']),sort_keys=True))
