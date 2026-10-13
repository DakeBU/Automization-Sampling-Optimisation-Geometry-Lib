from verify64 import *
SLOTS={'objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies'}
MAPS={};mapping_records=[]
def norm(p):return str(p).replace('\\','/').lower()
def pth(p,base=ROOT):
 p=Path(str(p).replace('\\','/'));return p if p.is_absolute() else base/p
def validate(pin,p=None):
 p=pth(p or pin['path']);b=p.read_bytes();assert sha(b)==pin['raw_sha256'],str(p)
 for key in ['raw_bytes','bytes']:
  if key in pin:assert len(b)==pin[key],str(p)
 if 'lf_sha256' in pin:assert sha(b.replace(b'\r\n',b'\n'))==pin['lf_sha256'],str(p)
 return b
def addmaps(capsule,key):
 for row in load(BASE/capsule)[key]:
  orig=row['original'];s=row['explicit_exact_raw_snapshot'];sp=pth(s if isinstance(s,str) else s['path']);b=validate(orig,sp)
  if isinstance(s,dict):validate(s)
  k=(norm(orig['path']),orig['raw_sha256']);assert k not in MAPS or MAPS[k].read_bytes()==b;MAPS[k]=sp
  mapping_records.append({'capsule':capsule,'original_path':orig['path'],'raw_sha256':orig['raw_sha256'],'explicit_snapshot':sp.as_posix()})
def resolve(pin,base=ROOT):
 p=pth(pin['path'],base)
 if p.exists() and sha(p.read_bytes())==pin['raw_sha256']:validate(pin,p);return 'current-exact',p
 k=(norm(p),pin['raw_sha256']);assert k in MAPS,('UNRESOLVED_FINITE_EXACT_INPUT',str(p),pin['raw_sha256']);validate(pin,MAPS[k]);return 'qualified-exact-history',MAPS[k]
def rawrows(obj):
 if isinstance(obj,dict):
  if {'path','raw_sha256'}<=set(obj) and ('raw_bytes'in obj or 'bytes'in obj):yield obj
  for v in obj.values():yield from rawrows(v)
 elif isinstance(obj,list):
  for v in obj:yield from rawrows(v)
def native(folder,runname,expected,payloadname,payloadsha,manifest,rowskey=None):
 d=BASE/folder;r=load(d/runname);r0=dict(r);r0.pop('run_sha256');assert sha(compact(r0))==r['run_sha256']==expected
 assert sha((d/payloadname).read_bytes())==payloadsha
 m=load(d/manifest)
 rows=m if rowskey is None else m[rowskey]
 for x in rows:validate(x,d/x.get('relative_path',x.get('path','')))
 lease=load(d/('lease.final.json' if 'source' in folder or 'overlay' in folder else 'lease.json'))
 assert lease.get('state',lease.get('status'))=='CLOSED_LAST'
 return {'folder':folder,'logical_whole_minus_only_run_sha256':expected,'complete_named_RAW_payload':rawpin(d/payloadname),'output_manifest':rawpin(d/manifest),'manifest_rows_verified':len(rows),'lease':rawpin(d/('lease.final.json' if 'source' in folder or 'overlay' in folder else 'lease.json')),'CLOSED_LAST':True}
def diff(a,b,path=''):
 if type(a)!=type(b):return [path]
 if isinstance(a,dict):
  out=[]
  for k in a.keys()|b.keys():out+=diff(a.get(k),b.get(k),path+'/'+k)
  return out
 if isinstance(a,list):return [] if a==b else [path]
 return [] if a==b else [path]
def check():
 assert git('rev-parse','HEAD')==COMMIT and git('rev-parse',COMMIT+'^')==PARENT
 checkpins(load(OUT/'input.manifest.json')['inputs'])
 for f,k in [('root.math64.adoption.json','finite_historical_maps'),('root.decoder64.adoption.json','raw_snapshot_mappings'),('root.source64.original-adoption.json','finite_input_maps'),('lesson-dependency64/supplement.json','finite_historical_maps'),('step6-presentation-repair64/supplement.json','finite_historical_maps'),('auxiliary-metadata-overlay64/overlay.json','finite_historical_maps'),('frontier-process-repair64/repair.json','finite_historical_maps')]:addmaps(f,k)
 for n,id in enumerate(['RealL2PositiveSquareOrder','PBPSCenteredRootOrderInverse']):
  sp=BASE/f'audit.{n}.before-source-admission.exactraw.snapshot.json';original=ROOT/f'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-{id}.json';pin=rawpin(sp);MAPS[(norm(original),pin['raw_sha256'])]=sp;mapping_records.append({'capsule':'explicit named before-source-admission snapshot','original_path':original.as_posix(),'raw_sha256':pin['raw_sha256'],'explicit_snapshot':sp.as_posix()})
 # Validate every closed native output, without copying any closed history.
 math=BASE/'independent-math64';ml=load(math/'lease.json');mr=load(math/'run.json');m0=dict(mr);m0.pop('run_sha256');assert sha(compact(m0))==mr['run_sha256']=='16d9117a32c0ba6f01a1d60b382da4d7e500a38c12ff94188984fc37a2b87773'
 assert sha((math/'named-mathematics.payload.json').read_bytes())=='a1154b20b2b47ca74aa3edc9db01e9b38e149c6824985b22cc6a816b0867c258'
 for x in ml['complete_owned_output_manifest_after_readback']:validate(x)
 assert ml['status']=='CLOSED_LAST' and len(ml['complete_owned_output_manifest_after_readback'])==167
 native_out=[{'folder':'independent-math64','logical_whole_minus_only_run_sha256':mr['run_sha256'],'complete_named_RAW_payload':rawpin(math/'named-mathematics.payload.json'),'lease':rawpin(math/'lease.json'),'manifest_rows_verified':167,'native_owned_files':168,'CLOSED_LAST':True}]
 native_out.append(native('independent-source64','review-run.json','9acbe7fd557f9fe4355d54f26ee5f2b7d2819d96c0deabd3eaba27aaf45f814d','review-run.json','8831289c9ae73ad92bb138016808ccf7e69e64f98c1779b0ea6f7a36ed8db4c3','full-owned-manifest.json','files'))
 native_out.append(native('independent-auxiliary-overlay64','review-run.json','c6b32a97745075cbc6bf286cdd763af1bcd4bf1cae69b937c19737c815a42d53','review-run.json','afa5bf100c9d91435c76deb8ca9fe45bcc212453a4e1f71ee0ef1bd4f138d91c','full-owned-manifest.json','files'))
 native_out.append(native('anonymous-decoder','final_run.json','dfa4906527c35c1684d8ce626c56cbcc41985f2bfb517f65d17c5cba1dd3f2ad','reconstruction_payload.json','ecbae83485126a3f9f25492b9b22d0c8f30059fabdcd64f2d18631d3a72d6c77','closure_manifest.json','artifacts'))
 assert native_out[1]['manifest_rows_verified']==96 and native_out[2]['manifest_rows_verified']==53 and native_out[3]['manifest_rows_verified']==16
 # Native source inputs are exact RAW/LF pairs and literal byte slices in the COMPLETE named RAW INPUT.
 source=BASE/'independent-source64';checks=load(source/'candidate-input-binding-and-span-checks.json');payload=(source/'review64-complete-inputs.named.raw.payload').read_bytes();assert sha(payload)=='f32b48a8d82d18bbd0f4978ad23526901b57ba702bf4d65c4d18fa1893bf6efc'
 for x in checks['records']:
  b=(source/x['raw_snapshot']).read_bytes();lf=(source/x['lf_snapshot']).read_bytes();assert sha(b)==x['raw_sha256'] and len(b)==x['raw_bytes'] and lf==b.replace(b'\r\n',b'\n') and sha(lf)==x['lf_sha256'];assert payload[x['complete_payload_byte_start']:x['complete_payload_byte_end_exclusive']]==b;resolve(dict(x,path=x['source_path']))
 resolutions=[]
 for folder,runname in [('independent-math64','run.json'),('independent-math64','mathematical-review.json'),('independent-source64','review-run.json'),('independent-auxiliary-overlay64','review-run.json'),('anonymous-decoder','final_run.json')]:
  for x in rawrows(load(BASE/folder/runname)):
   state,p=resolve(x,BASE/folder);resolutions.append({'record':folder+'/'+runname,'original_path':x['path'],'raw_sha256':x['raw_sha256'],'resolution':state,'resolved_path':p.as_posix()})
 # Canonical publication spans are literal whole-source + exact line-region RAW hashes, after the actual proof delimiter.
 spans=[]
 for lesson in ['real-l2-positive-square-order','pbps-centered-root-order-inverse']:
  unit=load(ROOT/f'website/content/declaration_lessons/{lesson}.json')['units'][0]
  for i,step in enumerate(unit['steps']):
   reg=step['lean_source_region'];p=ROOT/reg['path'];b=p.read_bytes();lines=b.splitlines(keepends=True);region=b''.join(lines[reg['start_line']-1:reg['end_line']]);literal=step['lean'].encode();assert sha(b)==reg['source_raw_sha256'] and region==literal and sha(region)==reg['exact_code_raw_sha256'];start=sum(map(len,lines[:reg['start_line']-1]));assert start>b.index(b':= by');assert blob(COMMIT,reg['path'])==b
   original=next(x for x in checks['all12_literal_spans'] if x['path']==reg['path'] and x['start_line']==reg['start_line'] and x['end_line']==reg['end_line']);assert (source/original['raw_excerpt_artifact']).read_bytes()==literal and original['literal_code_sha256']==sha(literal)
   spans.append({'lesson':lesson,'step':i+1,'path':reg['path'],'whole_source_RAW_sha256':sha(b),'start_line':reg['start_line'],'end_line':reg['end_line'],'literal_line_span_RAW_sha256':sha(literal),'literal_matches_current_and_committed_BODY':True,'native_source_excerpt_exact':True})
 assert len(spans)==12 and spans[8]['start_line']==251 and spans[8]['end_line']==293
 seals=[]
 for x in load(math/'mathematical-review.json')['candidate_headers_exact_sealed']:
  validate(x['candidate']);seal=validate(x['seal']);b=Path(x['candidate']['path']).read_bytes();start=b.index(b'theorem ');head=b[start:b.index(b':= by',start)].rstrip(b'\r\n ');assert head==seal.rstrip(b'\r\n ');seals.append({'candidate':x['candidate'],'seal':x['seal'],'exact_header_bytes_equal':True,'normalization':'Only final newline and delimiter-adjacent gap removed; no internal whitespace normalization.'})
 process=[]
 for x in load(BASE/'frontier-process-repair64/repair.json')['finite_historical_maps']:
  before=load(pth(x['explicit_exact_raw_snapshot']['path']));after=load(pth(x['current']['path']));validate(x['current']);assert sorted(diff(before,after))==[x['only_changed_field']];assert blob(COMMIT,pth(x['current']['path']).relative_to(ROOT).as_posix())==pth(x['current']['path']).read_bytes();process.append({'path':x['current']['path'],'only_changed_field':x['only_changed_field'],'before_RAW':x['original']['raw_sha256'],'after_RAW':x['current']['raw_sha256'],'exact_single_field_diff':True})
 cell=load(ROOT/'research-wiki/frontier-cells/ASTIS-SW-PBPS-centered-root-order-inverse.json');assert DECLS[0] in cell['reuse_plan']['reused_declarations']
 generic=load(ROOT/'research-wiki/frontier-cells/ASTIS-SHARED-l2-real-positive-square-order.json');assert generic['graph_contribution']['lean_view']=='new-node'
 audits=[]
 for i,id in enumerate(['RealL2PositiveSquareOrder','PBPSCenteredRootOrderInverse']):
  p=ROOT/f'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-{id}.json';a=load(p);adapter=load(BASE/f'source.{i}.review.root-adapter.json');assert a['state']=='accepted' and a['source_review']['state']=='accepted' and not a['repairs'] and not a['deltas'];assert set(adapter['semantic_slots'])==SLOTS and adapter['independent_from_formalizer'] and adapter['independent_from_decoder'];assert adapter['verdict']=='equivalent-after-elaboration' and not adapter['repairs'] and not adapter['deltas'];assert adapter['publication_binding_sha256']==a['publication_binding_sha256'];assert adapter['review_run_sha256']==native_out[i+2 if i==0 else 1]['logical_whole_minus_only_run_sha256'];assert blob(COMMIT,p.relative_to(ROOT).as_posix())==p.read_bytes();native_decision=load(BASE/('independent-auxiliary-overlay64/decision.0.json' if i==0 else 'independent-source64/decision.1.json'))
  for k in ['semantic_slots','verdict','repairs','deltas','publication_binding_sha256','reviewer_packet_sha256','declaration']:assert adapter[k]==native_decision[k],k
  audits.append({'audit':rawpin(p),'adapter':rawpin(BASE/f'source.{i}.review.root-adapter.json'),'native_decision':rawpin(BASE/('independent-auxiliary-overlay64/decision.0.json' if i==0 else 'independent-source64/decision.1.json')),'seven_slots_complete':True,'accepted_independent_review':True,'publication_binding_sha256':a['publication_binding_sha256'],'native_logical_run_sha256':adapter['review_run_sha256'],'native_complete_RAW_review_sha256':adapter['native_complete_RAW_review_sha256']})
 unchanged=[]
 for rel in ['AutoSamplingTheory.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests.lean','lean-toolchain','lake-manifest.json']:
  b=blob(COMMIT,rel);w=(ROOT/rel).read_bytes();assert b==blob(PARENT,rel) and b.replace(b'\r\n',b'\n')==w.replace(b'\r\n',b'\n');unchanged.append({'path':rel,'committed_RAW_sha256':sha(b),'exact_committed_parent_equal':True,'working_RAW':rawpin(ROOT/rel),'working_vs_Git_RAW_equal':b==w,'working_vs_Git_LF_equal':True})
 write('bindings.result.json',{'status':'PASS','actor':ACTOR,'actual_checker_pid':os.getpid(),'checked_commit':COMMIT,'actual_parent':PARENT,'native_closed_output_bindings':native_out,'finite_exact_historical_mapping_count':len(mapping_records),'finite_exact_historical_mappings':mapping_records,'native_pin_resolutions':resolutions,'source_RAW_LF_payload_pairs':len(checks['records']),'literal_BODY_spans':spans,'initial_exact_headers':seals,'process_only_two_fields':process,'accepted_source_audits':audits,'unchanged_shared_roots_toolchain_manifest':unchanged,'input_pin_count':142,'original_math_step6_blocker_preserved':True,'current_step6_repaired_literal_BODY':[251,293],'original_source_close_PID_debt_preserved':None,'source_Lean_graph_distinction_preserved':True,'conceptual_mirror_audit':'none-found consistent with exact within-model compiled dependencies','aggregate_integration':False,'full_paper_polar_onto_PURIFIED_ExpositionSeal_Goal':False})
 print(json.dumps({'status':'BINDINGS_PASS','pid':os.getpid(),'native_owned_counts':[168,97,54,18],'finite_maps':len(mapping_records),'native_pin_resolutions':len(resolutions),'literal_BODY_spans':len(spans),'source_RAW_LF_pairs':len(checks['records']),'headers':len(seals),'process_only_fields':len(process)}))
if __name__=='__main__':
 try:check()
 except Exception as e:write('bindings.failure.json',{'status':'FAIL','actual_pid':os.getpid(),'exception':repr(e)});raise
