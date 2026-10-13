import json, hashlib, os, time, datetime, struct
from pathlib import Path
from urllib.parse import urlsplit,unquote
R=Path('E:/Samplinglib');T=R/'runs/20261007-companion-priority/pbps-macroscopic-centered-range58';B=T/'reader-controls58/independent-review';S=R/'_site';P=T/'reader-controls58';O=T/'exposition-seal58'
def h(b):return hashlib.sha256(b).hexdigest()
def can(o):return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def rec(p):
 b=Path(p).read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=str(p).replace('\\','/'),raw_bytes=len(b),raw_sha256=h(b),lf_bytes=len(l),lf_sha256=h(l))
def write(n,o):(B/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
oldscript=(O/'review_exposition.py').read_text();classes=oldscript[oldscript.index('class N:'):oldscript.index("ids=['l2-pullback-range'")];from html.parser import HTMLParser;exec(classes)
def structural(n):
 if isinstance(n,str):return n
 if 'lean-source-actions' in n.a.get('class','').split():return None
 attrs={k:v for k,v in n.a.items() if k!='data-lean-code-panel'}
 return [n.tag,attrs,[v for x in n.c for v in [structural(x)] if v is not None]]
def find(n,key,val):return next(x for x in n.all() if x.a.get(key)==val)
def direct(n,tag):return next(x for x in n.c if isinstance(x,N) and x.tag==tag)
start=time.monotonic();inputs=[]
def pin(p):
 p=Path(p);inputs.append(p);return rec(p)
rootexec=load(P/'root.execution.json');pin(P/'root.execution.json');behavior=load(P/'browser/results.json');pin(P/'browser/results.json');pin(P/'browser/closure.json');pin(P/'browser-pass4.executed.mjs')
for p in ['attempt0.status.json','attempt0.closure.json','attempt1.status.json','attempt1.closure.json','attempt2.closure.json','attempt3.closure.json','clipboard-newline.diagnosis.json']:
 if (P/p).is_file():pin(P/p)
renderer=[]
for r in rootexec['changed_files']:
 actual=pin(R/r['path']);assert actual['raw_bytes']==r['bytes'] and actual['raw_sha256']==r['raw_sha256'] and actual['lf_sha256']==r['lf_sha256'];renderer.append(actual)
pin(S/'assets/site.js');pin(S/'assets/site.css');pin(S/'assets/module-lean-tutor.js')
assert (S/'assets/site.js').read_bytes()==(R/'website/static/site.js').read_bytes();assert (S/'assets/site.css').read_bytes()==(R/'website/static/site.css').read_bytes()
oldman=load(O/'input.manifest.json');pin(O/'input.manifest.json');pin(O/'run.json');pin(O/'exposition.seal.json');pin(O/'lease.json');pin(O/'review_exposition.py')
oldmap={x['qualified_identity']:x for x in oldman['inputs']};oldrun=load(O/'run.json');ox=dict(oldrun);osh=ox.pop('run_sha256');assert h(can(ox))==osh;assert load(O/'lease.json')['status']=='CLOSED' and oldrun['full_reader_delivery_blockers']==1
comp=S/'example-cases/samplewiki/companions/proximal-bouncy-particle.html';pin(comp);current=parse(comp);oldcomp=Path(oldmap[str(comp.relative_to(R)).replace('\\','/')]['exactraw_snapshot']['path']);pin(oldcomp);prior=parse(oldcomp)
ids=['l2-pullback-range','pbps-macroscopic-centered-range','pbps-centered-macro-defect-gap'];codes=['AutoSamplingTheory/TechnicalLemmas/Measure/L2PullbackRange.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicRange.lean','Tests/ProximalBPSMacroscopicRange.lean'];mods=['autosamplingtheory-technicallemmas-measure-l2pullbackrange','autosamplingtheory-examplecases-proximalbps-macroscopicrange','tests-proximalbpsmacroscopicrange'];audits=['ASTIS-RT-20261008-L2PullbackRange','ASTIS-RT-20261008-PBPSMacroscopicCenteredRange','ASTIS-RT-20261008-PBPSCenteredMacroDefectGap']
records=behavior['records'];assert len(records)==9 and behavior['ownedBrowserExit']['code']==0;assert load(P/'browser/closure.json')['success']
unchanged=[];rows=[];controls=[];clipboard=[];downloads=[]
def inspect_panel(panel,page,source,label,record):
 assert 'open' not in panel.a and 'data-lean-code-panel' in panel.a
 actions=next(x for x in panel.c if isinstance(x,N) and x.a.get('class')=='lean-source-actions');button=direct(actions,'button');anchor=direct(actions,'a');status=direct(actions,'span');assert button.text()==label and 'data-lean-copy' in button.a and status.a['role']=='status' and status.a['aria-live']=='polite'
 u=urlsplit(anchor.a['href']);assert not u.scheme and not u.netloc;target=(page.parent/unquote(u.path)).resolve();assert S.resolve() in target.parents and target==S/'downloads/lean'/source;assert anchor.text()=='Download module (.lean)' and anchor.a['download']==Path(source).name
 code=direct(direct(panel,'pre'),'code').text().encode();lf=code.replace(b'\r\n',b'\n');native=lf.replace(b'\n',b'\r\n')
 assert record['copyStatus']=='Copied' and record['initiallyFolded'] and record['clipboardRestoredInMemory'];assert record['copiedLFSHA256']==h(lf) and record['copiedSHA256'] in [h(code),h(native)];assert record['CRLFpairNormalizationOnly']
 if 'copiedBytes' in record:assert record['copiedBytes'] in [len(code),len(native)]
 clipboard.append(dict(expected_code_LF_sha256=h(lf),observed_native_clipboard_sha256=record['copiedSHA256'],observed_native_clipboard_LF_sha256=record['copiedLFSHA256'],line_endings_only=True,observed_by='root actual foreground pass4; independently bound to exact current DOM/code bytes',reviewer_reclicked=False))
 controls.append(dict(page=str(page),label=label,download_href=anchor.a['href'],download_filename=anchor.a['download'],initially_folded=True,adjacent_direct_code=True,aria_live_status=True))
 pin(target);assert target.read_bytes()==(R/source).read_bytes()
 return code
for i,(slug,source,mod,audit) in enumerate(zip(ids,codes,mods,audits)):
 for path in [source,'website/content/publications/'+slug+'.json','website/content/declaration_lessons/'+slug+'.json','research-wiki/semantic-roundtrip/audits/'+audit+'.json']:
  actual=pin(R/path);baseline=oldmap[path]['actual_input'];assert all(actual[k]==baseline[k] for k in ['raw_bytes','raw_sha256','lf_bytes','lf_sha256']);unchanged.append(actual)
 item=find(current,'id',slug);olditem=find(prior,'id',slug);assert structural(item)==structural(olditem),'non-controls reader row delta '+slug
 declarations=[x for x in item.all() if 'data-authored-declaration' in x.a];assert len(declarations)==1;decl=declarations[0].a['data-authored-declaration'];panes=[x for x in item.all() if x.a.get('data-inline-lean')==decl];assert len(panes)==2
 for role,label in [('statement','Copy statement'),('proof','Copy declaration')]:
  pane=next(x for x in panes if 'inline-lean-'+role in x.a['class'].split());record=next(x for x in records if x.get('id')==slug and x.get('role')==role);assert record['actualNativeClipboardReadback'];code=inspect_panel(pane,comp,source,label,record);assert code.decode() in (R/source).read_text(encoding='utf-8')
 steps=[x for x in item.all() if x.a.get('class')=='proof-reader-step'];assert len(steps)==[3,4,4][i]
 module=S/'modules'/(mod+'.html');pin(module);oldmodule=Path(oldmap[str(module.relative_to(R)).replace('\\','/')]['exactraw_snapshot']['path']);pin(oldmodule);m=parse(module);om=parse(oldmodule);section=find(m,'id','complete-module-source');oldsection=find(om,'id','complete-module-source');assert structural(section)==structural(oldsection)
 panel=direct(section,'details');record=next(x for x in records if x.get('source')==source);code=inspect_panel(panel,module,source,'Copy complete module',record);assert code.replace(b'\r\n',b'\n')==(R/source).read_bytes().replace(b'\r\n',b'\n')
 downloaded=P/'browser/downloads'/Path(source).name;pin(downloaded);raw=downloaded.read_bytes();assert raw==(R/source).read_bytes() and record['downloadRawSHA256']==h(raw) and record['downloadBytes']==len(raw) and record['actualAnchorClicked'] and record['exactCheckoutRawBytes']
 downloads.append(dict(source=source,actual_export=rec(S/'downloads/lean'/source),actual_completed_download=rec(downloaded),raw_checkout_bytes_equal=True))
 rows.append(dict(id=slug,exact_controls_only_reader_structure_delta=True,unchanged_statement_formula_proof_source_and_audit=True,inline_control_count=2,module_control_count=1,proof_steps=len(steps)))
completed=[x for x in behavior['nativeDownloadEvents'] if x['method']=='Browser.downloadProgress' and x['params']['state']=='completed'];begins=[x for x in behavior['nativeDownloadEvents'] if x['method']=='Browser.downloadWillBegin'];assert len(completed)==len(begins)==3 and len({x['params']['guid'] for x in completed})==3
for source in codes:
 e=next(x for x in begins if x['params']['suggestedFilename']==Path(source).name);assert urlsplit(e['params']['url']).path=='/downloads/lean/'+source;done=next(x for x in completed if x['params']['guid']==e['params']['guid']);assert done['params']['receivedBytes']==done['params']['totalBytes']==(R/source).stat().st_size
js=(R/'website/static/site.js').read_text();assert 'panel?.querySelector(":scope > pre > code")' in js and 'await navigator.clipboard.writeText(code.textContent)' in js and 'document.execCommand("copy")' in js and 'Copy failed; select the Lean code below.' in js
implementation=dict(correct_direct_parent_code_selection=True,clipboard_primary_and_manual_selection_failure_status=True,insecure_clipboard_fallback_present_but_not_browser_tested=True,full_module_exports_write_bytes_read_bytes=True,download_separates_complete_module_from_partial_declaration=True)
for page in [comp]+[S/'modules'/(m+'.html') for m in mods]:
 p=parse(page);loaded=[n.a.get('src') for n in p.all() if n.tag=='script' and n.a.get('src')];assert any(x.endswith('assets/site.js') for x in loaded)
visuals=[]
for p,scope in [(B/'browser-corrected/companion-controls-corrected.png','reviewer corrected exact main statement controls'),(P/'browser/module-controls.png','root complete module controls')]:
 pin(p);raw=p.read_bytes();assert struct.unpack('>II',raw[16:24])==(1440,1800);visuals.append(dict(file=rec(p),actually_viewed_with_view_image=True,native_resolution=[1440,1800],scope=scope,observation='Copy and direct module download controls visibly adjacent to actual Lean code; fullreader readability debts remain'))
pin(P/'browser/companion-controls.png')
capture=load(B/'browser-corrected/results.json');assert capture['geometry']['layoutRechecked'] and capture['geometry']['actions']['y']>=0 and capture['ownedBrowserExit']['code']==0
for p in [R/'docs/proof-digestion-protocol.md',R/'docs/evidence-routed-memory-protocol.md']:pin(p)
unique=list(dict.fromkeys(inputs));(B/'inputs').mkdir();entries=[]
for index,p in enumerate(unique):
 identity=str(p.relative_to(R)).replace('\\','/');stem='%03d__%s__%s'%(index,h(identity.encode())[:16],p.name[:44]);raw=p.read_bytes();a=B/'inputs'/(stem+'.exactraw');l=B/'inputs'/(stem+'.lf');a.write_bytes(raw);l.write_bytes(raw.replace(b'\r\n',b'\n'));entries.append(dict(qualified_identity=identity,actual_input=rec(p),exactraw_snapshot=rec(a),crlf_to_lf_snapshot=rec(l)))
write('input.manifest.json',dict(schema_version=1,input_count=len(entries),qualified_unique_identity_count=len(entries),basename_aliases_used=False,inputs=entries))
payload=dict(schema_version=1,actor='/root/statement_topology58',status='ACCEPT_SCOPED_READER_CONTROLS_REPAIR',repair_classification='reader-delivery-missing-clipboard-and-direct-source-download',typed_prior_blocker_resolved_for_current_rendered_three_rows=True,original_exposition_run_sha256=osh,original_stage_immutable_and_not_retroaccepted=True,science_commit='8c8847715c1d4c3033224b069d8dd694f2a4bd30',integration_commit='a7cafde7957a8562bcd697d89c56b14768914c66',renderer_files=renderer,rows=rows,controls=controls,clipboard_readbacks=clipboard,downloads=downloads,completed_native_download_event_count=3,unchanged_canonical_code_publication_lesson_audit_receipts=unchanged,implementation=implementation,actual_visuals=visuals,root_companion_wrong_framing_retained_not_visual_evidence=True,root_actual_checks=rootexec,own_capture_actual_exit_code=0,own_capture_chunk='a169bb',own_browser_closure=load(B/'browser-corrected/closure.json'),retained_failures=[dict(path='browser-bootstrap-env-blocked.json',classification='ENV_BLOCKED_runtime_missing'),dict(path='retained-capture-failure.json',classification='visual-capture-framing-tooling')],blocking_repair_deltas=[],remaining_readability_debts=['dense inline notation and duplicate assumptions','horizontal assumption-table scroll','very tall companion','long graph labels'],full_reader_accepted=False,Chapter1_3_full_reader_acceptance=False,full_Exposition_Seal=False,PURIFIED=False,live_verified=False,math_source_acceptance_changed=False,canonical_Git_Lean_renderer_state_edits=False,compiler_started=False,remaining_boundary='Gamma/root/inverse/full weighted weak H1/C5-C7/half-turn/dynamics/main/errors/cost/actual-input composition/full paper/Goal remain open.')
write('repair-payload.json',payload);write('review.execution.json',dict(status='CONTENT_AND_VISUAL_REPAIR_REVIEW_PASS',actual_foreground_pid=os.getpid(),wall_seconds=time.monotonic()-start,cpu_user_seconds=os.times().user,cpu_system_seconds=os.times().system,input_count=len(entries),clipboard_readback_count=9,download_count=3,actually_viewed_png_count=2))
print(json.dumps(dict(status=payload['status'],input_count=len(entries),controls=len(controls),clipboard_readbacks=9,downloads=3,visuals=2,pid=os.getpid())))
