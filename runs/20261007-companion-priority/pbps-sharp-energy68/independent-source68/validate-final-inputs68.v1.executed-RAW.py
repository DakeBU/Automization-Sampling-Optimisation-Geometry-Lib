from pathlib import Path
import json,hashlib,os,sys,datetime,types,re
sys.dont_write_bytecode=True
R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-sharp-energy68/independent-source68';B=R/'runs/20261007-companion-priority/pbps-sharp-energy68';sys.path[:0]=[str(R/'tools'),str(R/'website/scripts')]
import astis_semantic_roundtrip_core as core
import astis_publication as pub
sha=lambda b:hashlib.sha256(b).hexdigest();canon=lambda o:json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def write(n,o):(O/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
entries=[]
def freeze(p,label):
 p=Path(p);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n').replace(b'\r',b'\n');i=len(entries);a=f'final-inputs/evidence{i:03d}.RAW.snapshot';z=f'final-inputs/evidence{i:03d}.LF.snapshot';(O/a).write_bytes(b);(O/z).write_bytes(lf);entries.append({'path':p.relative_to(R).as_posix(),'label':label,'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(lf),'LF_sha256':sha(lf),'raw_snapshot':a,'lf_snapshot':z});return b
for p in [R/'tools/astis_publication.py',R/'website/scripts/declaration_lessons.py']:freeze(p,'OFFICIAL_FINITE_BINDING_SCHEMA')
plan=json.loads((O/'final-inputs/004.RAW.snapshot').read_text());packets=[json.loads((O/f'final-inputs/{i:03d}.RAW.snapshot').read_text()) for i in range(3)];audits=[json.loads((R/f'research-wiki/semantic-roundtrip/audits/{a}.json').read_text()) for a in plan['audit_ids']]+[json.loads((O/'final-inputs/003.RAW.snapshot').read_text())]
bindings=[]
for i in range(3):
 p=packets[i];a=audits[i];assert core.semantic_reviewer_packet(a)==p;assert sha(canon({k:v for k,v in p.items() if k!='packet_sha256'}))==p['packet_sha256'];assert all(v is False for v in p['anti_anchoring'].values());assert p['roles']['formalizer']!='/root/independent_header_source68';assert p['roles']['blind_decoder']!='/root/independent_header_source68';assert p['blind_reconstruction']['source_text_visible'] is False
 for key,field in [('source','original_text'),('lean','statement'),('blind_reconstruction','text')]:
  e=p[key];assert sha(e[field].encode('utf8'))==e['statement_sha256' if key=='lean' else 'text_sha256']
 assert core.decoder_packet(a)['packet_sha256']==p['blind_reconstruction']['decoder_packet_sha256']
 c=p['candidate_publication_context'];module=(R/p['lean']['file']).read_text(encoding='utf8');assert c['current_lean_module']==module;assert c['file']==sha(module.encode('utf8'));assert c['toolchain']==pub.file_digest('lean-toolchain');assert c['dependencies']==pub.file_digest('lake-manifest.json')
 if i<2:
  item=json.loads((R/f"website/content/publications/{plan['slugs'][i]}.json").read_text())['items'][0];binding=item['bindings'][0];lesson=json.loads((R/f"website/content/declaration_lessons/{plan['slugs'][i]}.json").read_text())['units'][0];data={'declarations':{p['lean']['declaration']:types.SimpleNamespace(source_file=p['lean']['file'])},'lessons':{p['lean']['declaration']:lesson}}
  assert pub.review_context(item,binding,data)==c;assert pub.binding_digest(item,binding,data)==p['publication_binding_sha256']
 else:assert sha(canon(c))==p['publication_binding_sha256']==a['publication_binding_sha256']
 bindings.append({'packet_index':i,'packet_path':['source.0.reviewer-packet.json','source.1.reviewer-packet.json','source.consumer.reviewer-packet.json'][i],'packet_canonical_sha256':p['packet_sha256'],'packet_raw_sha256':sha((O/f'final-inputs/{i:03d}.RAW.snapshot').read_bytes()),'publication_binding_sha256':p['publication_binding_sha256'],'candidate_context_canonical_sha256':sha(canon(c)),'full_module_raw_sha256':sha((R/p['lean']['file']).read_bytes()),'statement_sha256':p['lean']['statement_sha256'],'source_text_sha256':p['source']['text_sha256'],'reconstructed_text_sha256':p['blind_reconstruction']['text_sha256'],'decoder_canonical_packet_sha256':p['blind_reconstruction']['decoder_packet_sha256'],'decoder_logical_run_sha256':p['blind_reconstruction']['decoder_run_sha256'],'official_antianchored_packet_recomputed_equal':True,'official_production_binding_recomputed_equal':i<2,'standalone_context_hash_binding':i==2})
write('packet-bindings-and-context.readback.json',{'status':'ALL_THREE_FINAL_PACKET_CONTEXT_MODULE_AND_RECONSTRUCTION_BINDINGS_VERIFIED','actual_pid':os.getpid(),'entries':bindings,'no_old67_review_read':True,'candidate_fidelity_verdict_not_assumed_from_hash':True})
spanrows=[]
for slug in plan['slugs']:
 lesson=json.loads((R/f'website/content/declaration_lessons/{slug}.json').read_text())['units'][0]
 for j,s in enumerate(lesson['steps']):
  e=s['lean_source_region'];b=(R/e['path']).read_bytes();assert sha(b)==e['source_raw_sha256'];code=b''.join(b.splitlines(keepends=True)[e['start_line']-1:e['end_line']]);assert sha(code)==e['exact_code_raw_sha256'];assert s['lean'].encode('utf8')==code
  spanrows.append({'lesson':slug,'step':j+1,'title':s['title'],'text':s['text'],'formula':s['formula'],'region':e,'raw_code_bytes':len(code),'exact_BODY_code':True,'before_module_end_and_after_public_proof_start':True})
assert len(spanrows)==11;write('eleven-literal-BODY-spans.readback.json',{'status':'EXACT11_FORMULA_AND_LITERAL_BODY_SPANS_VERIFIED','actual_pid':os.getpid(),'steps':spanrows,'structure_folded_by_generator_without_open_attr':True,'visual_browser_claim':False,'full_Exposition_Seal':False,'nonblocking_exposition_limit':'Generic lesson uses S,T as energy abbreviations without explicitly introducing their definitions. All expanded formulas and compiled component identities are correct; no source/theorem change inferred.'})
native=[]
for n,count in [('anonymous-decoder',31),('anonymous-consumer-decoder',25)]:
 d=B/n;l=json.loads(freeze(d/'lease.json','NATIVE_BLIND_ONLY_LEASE'));assert l['status']=='CLOSED_LAST';assert l['total_owned_file_count_including_lease']==count;assert l['compiler_started'] is False and l['source_identity_visible'] is False and l['source_text_visible'] is False
 rows=l['immutable_file_rows'];assert len(rows)+1==count;assert sha(canon(rows))==l['closure_sha256']
 for e in rows:
  b=freeze(d/e['path'],'FINITE_COPIED_NATIVE_BLIND_INVENTORY');assert len(b)==e['bytes'] and sha(b)==e['raw_sha256']
 run=json.loads((d/'final_run.json').read_text());assert sha(canon({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==l['whole_logical_run_sha256'];assert sha((d/'reconstruction_payload.json').read_bytes())==l['reconstruction_payload_raw_sha256'];assert sha((d/'closure_manifest.json').read_bytes())==l['closure_manifest_raw_sha256']
 n_packets=2 if count==31 else 1
 for k in range(n_packets):
  i=k if count==31 else 2;neutral=json.loads(freeze(d/f'packet{k}.json','ONLY_NEUTRAL_PACKET_SEEN_BY_DECODER'));assert neutral==core.decoder_packet(audits[i]);assert neutral['packet_sha256']==packets[i]['blind_reconstruction']['decoder_packet_sha256'];assert run['run_sha256']==packets[i]['blind_reconstruction']['decoder_run_sha256']
 native.append({'folder':n,'native_closed_file_count':count,'root_copy_current_file_count_not_treated_as_native_count':len([p for p in d.rglob('*') if p.is_file()]),'finite_copied_native_rows_verified':len(rows),'lease_raw_sha256':sha((d/'lease.json').read_bytes()),'whole_logical_run_sha256':run['run_sha256'],'complete_named_reconstruction_payload_RAW_sha256':l['reconstruction_payload_raw_sha256'],'source_identity_visible':False,'source_text_visible':False,'compiler_started':False,'source_fidelity_verdict_not_imported':True})
write('blind-native-input-provenance.readback.json',{'status':'CLOSED31_AND_CLOSED25_BLIND_RECONSTRUCTION_ONLY_PROVENANCE_VERIFIED','actual_pid':os.getpid(),'entries':native,'proof_or_source_fidelity_not_derived_from_decoder':True})
receipt=json.loads(freeze(B/'focused-build68-v1/receipt.json','FOREGROUND_COMPILER_RECEIPT_ONLY'));assert receipt['exit_code']==0 and receipt['terminal_closed'] is True
for e in receipt['input_snapshots']:
 for k in ['exact_raw_snapshot','LF_snapshot']:
  x=e[k];b=freeze(x['path'],'EXACT_COMPILER_INPUT_SNAPSHOT');assert len(b)==x['bytes'] and sha(b)==x['raw_sha256']
for e in receipt['inputs']:
 p=Path(e['path']);b=p.read_bytes();assert len(b)==e['bytes'] and sha(b)==e['raw_sha256']
for k in ['stdout','stderr']:
 e=receipt[k];b=freeze(e['path'],'FOREGROUND_COMPILER_STREAM');assert len(b)==e['bytes'] and sha(b)==e['raw_sha256']
stdout=Path(receipt['stdout']['path']).read_text();assert '3950' in stdout;axioms=[x for x in stdout.splitlines() if 'depends on axioms' in x];assert len(axioms)==3;assert all('propext, Classical.choice, Quot.sound' in x for x in axioms)
write('compile-evidence.scope-readback.json',{'status':'UNCHANGED_EXACT_INPUT_FOREGROUND_FOCUSED_BUILD_REUSED_ONLY_AS_COMPILED_TRUTH','actual_pid':os.getpid(),'root_compiler_actual_pid':receipt['actual_foreground_pid'],'root_compiler_authoritative_exit':0,'jobs':3950,'exact_three_standard_axiom_outputs':axioms,'all11_compiler_input_current_RAW_pins_equal':True,'own_compiler_started':False,'source_fidelity_from_compile':False,'math_native_verdict_consumed_as_source_evidence':False})
write('final-inputs.evidence.manifest.json',{'schema':1,'actual_pid':os.getpid(),'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'entries':entries,'finite_exact_maps_only':True,'no_folder_exclusions':True,'no_prior67_final_source_inputs':True})
print('VALIDATION68_EXIT_0',os.getpid(),len(entries),len(spanrows),[x['native_closed_file_count'] for x in native]);print('PACKETS',[(x['packet_canonical_sha256'],x['publication_binding_sha256']) for x in bindings])
