import sys
sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib, json, hashlib, datetime, re, html, base64, os
O = pathlib.Path(__file__).resolve().parent
B = pathlib.Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-actual-projected-rotation-preproof70/independent-header-source70')
P = pathlib.Path('E:/Samplinglib/runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html')
H = lambda b: hashlib.sha256(b).hexdigest()
J = lambda p: json.loads(p.read_bytes())
def save(n,v):
 (O/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def input_snapshot(path, name):
 raw=path.read_bytes(); lf=raw.replace(b'\r\n',b'\n')
 (O/name).write_bytes(raw); (O/(name+'.LF')).write_bytes(lf)
 return {'original_path':str(path),'snapshot':name,'RAW_bytes':len(raw),'RAW_sha256':H(raw),'LF_snapshot':name+'.LF','LF_bytes':len(lf),'LF_sha256':H(lf),'LF_recipe':'replace only CRLF byte pairs (0D 0A) with LF (0A); preserve all other bytes','original_mtime_ns':path.stat().st_mtime_ns}
primary=P.read_bytes()
assert len(primary)==1482128 and H(primary)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
prior_manifest=J(B/'owned-manifest.json'); prior_lease=J(B/'lease.final.json')
assert H((B/'lease.final.json').read_bytes())=='0aba415246dd79cee1429a046c6a1d61ce9924bb32de50caeef60c0a8cf2f714'
assert H((B/'owned-manifest.json').read_bytes())=='875f0d90ddfc801b3bfb17928a5971f5d1fd1fb741c85196ebf782f117aa5084'
checked=[]
for e in prior_manifest['regular_file_entries']:
 p=B/e['name']; raw=p.read_bytes(); assert len(raw)==e['RAW_bytes'] and H(raw)==e['RAW_sha256']; assert H(raw.replace(b'\r\n',b'\n'))==e['LF_sha256']
 checked.append({'name':e['name'],'RAW_bytes':len(raw),'RAW_sha256':H(raw),'mtime_ns':p.stat().st_mtime_ns})
assert len(checked)==81
inputs=[input_snapshot(P,'primary-pbps.exactraw.snapshot.html')]
names=['lease.final.json','owned-manifest.json','source-expectations70.before-header.json','primary419-NODE-EXCLUDED70.json','finite-coverage-manifest70.json','source-before-header-order.json','parent69-retention-and-binder-audit.json','frozen-source.source-proof-graph.json','frozen-source.source-input-regions.json','frozen-source.source-expectations.json','frozen-source.source-coverage-inventory.json']
for n in names: inputs.append(input_snapshot(B/n,'prior83.'+n))
region_map=J(B/'frozen-source.source-input-regions.json')
items=[]; regions=[]
pat=re.compile(rb'<math\b[^>]*>.*?</math>',re.S)
for region in region_map['regions']:
 name='source.'+region['name']+'.RAW.html'; raw=(B/name).read_bytes(); a,z=region['source_RAW_range_end_exclusive']
 assert raw==primary[a:z] and H(raw)==region['RAW_sha256']
 inputs.append(input_snapshot(B/name,name))
 found=[]
 for m in pat.finditer(raw):
  tag=m.group(); idm=re.search(rb'\bid="([^"]+)"',tag); altm=re.search(rb'\balttext="([^"]*)"',tag)
  assert idm and altm
  anns=re.findall(rb'<annotation\b[^>]*encoding="application/x-tex"[^>]*>(.*?)</annotation>',tag,re.S)
  tex=html.unescape(altm.group(1).decode('utf-8')); ann=html.unescape(anns[0].decode('utf-8')) if anns else None
  assert tex==ann
  entry={'id':idm.group(1).decode(),'region':region['name'],'source_RAW_range_end_exclusive':[a+m.start(),a+m.end()],'region_RAW_range_end_exclusive':[m.start(),m.end()],'RAW_bytes':len(tag),'RAW_sha256':H(tag),'alttext':tex,'annotation_tex':ann}
  items.append(entry); found.append(entry)
 assert len(found)==region['math_count']
 regions.append({'name':region['name'],'RAW_range_end_exclusive':[a,z],'RAW_bytes':len(raw),'RAW_sha256':H(raw),'LF_sha256':H(raw.replace(b'\r\n',b'\n')),'math_count':len(found)})
assert len(items)==419 and len({e['id'] for e in items})==419
old=J(B/'frozen-source.source-coverage-inventory.json')['math_items']
for a,b in zip(items,old):
 for k in ['id','region','source_RAW_range_end_exclusive','RAW_sha256','alttext','annotation_tex']: assert a[k]==b[k],(k,a['id'])
save('stageA.primary419.reparsed-inventory.json',{'schema':'source70-stageA-independent-RAW-reparse-v1','actual_pid':os.getpid(),'count':419,'regions':regions,'math_items':items,'source_before_current70_BODY':True,'source_selection_finite_not_whole_paper':True})
save('stageA.prior83.integrity.json',{'actual_pid':os.getpid(),'prior_status':prior_lease['status'],'old_native_read_only':True,'regular_files_verified':checked,'regular_count':81,'total_closed_file_count':83,'lease_RAW_sha256':H((B/'lease.final.json').read_bytes()),'manifest_RAW_sha256':H((B/'owned-manifest.json').read_bytes()),'no_old_writes':True})
save('stageA.input-manifest.json',{'schema':'source70-stageA-exact-RAW-LF-inputs-v1','actual_pid':os.getpid(),'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inputs':inputs,'count':len(inputs),'LF_recipe':'CRLF-only; no Unicode normalization or JSON reserialization','current70_BODY_read':False,'current70_candidate_publication_read':False,'blind70_decoder_read':False})
save('stageA.open-lease.json',{'schema':'source70-stageA-open-lease-v1','owner':'/root/independent_primary69','owned_path':str(O),'status':'OPEN_STAGE_A_PRIMARY_ONLY_PENDING_OFFICIAL_PACKET','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_pid':os.getpid(),'source_verdict':None,'no_Lean_compile':True,'no_canonical_Git_ledger_Goal_Graph_edits':True,'no_old_closed_writes':True,'not_full_theorem_or_source_fidelity_credit':True})
print(json.dumps({'actual_pid':os.getpid(),'primary_RAW_sha256':H(primary),'prior83_regular_verified':81,'source_regions':len(regions),'independent_math_items':len(items),'input_count':len(inputs),'current70_BODY_read':False},ensure_ascii=True))
