from pathlib import Path
from html.parser import HTMLParser
from types import SimpleNamespace
import ctypes, datetime, hashlib, json, os, subprocess, sys
ROOT=Path('E:/Samplinglib'); R=ROOT/'runs/20261007-companion-priority/pbps-actual-hazard-clock75'; O=R/'independent-repository-reader75'; DIS=R/'final-reader-repository-packet75.json'
ACTOR='/root/header_math72'; SCI='51d3a65f65b189b0afaaf91a248f8c2f58162ef2'; DECL='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHazardClock.actual_integrated_hazard_clock_laws'; MOD='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean'; SOURCE='fd93d01583eec206285573c1f1631b94739f95471c50e1ff940e66080238e23d'
PY=Path('C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'); ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1'); sys.dont_write_bytecode=True
sha=lambda b:hashlib.sha256(b).hexdigest(); can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode(); load=lambda p:json.loads(Path(p).read_bytes())
def resolve(p):
 p=Path(p); return p if p.is_absolute() else ROOT/p
def pin(p):
 p=resolve(p); b=p.read_bytes(); return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def check(z):
 p=resolve(z['path']); b=p.read_bytes(); n=z.get('RAW_bytes',z.get('raw_bytes',z.get('bytes'))); h=z.get('RAW_sha256',z.get('raw_sha256')); lf=z.get('LF_sha256',z.get('lf_sha256'))
 assert len(b)==n and sha(b)==h,p
 if lf is not None: assert sha(b.replace(b'\r\n',b'\n'))==lf,p
 return b
def save(n,j):
 assert not (O/'lease.final.json').exists(); p=O/n; p.parent.mkdir(parents=True,exist_ok=True); assert not p.exists(),p
 p.write_text(json.dumps(j,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf8',newline='\n')
def command(label,args):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat(); p=subprocess.Popen([str(x) for x in args],cwd=ROOT,env=ENV,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 print(json.dumps(dict(START=label,PID=p.pid,driver_PID=os.getpid())),flush=True); out,err=p.communicate(); d=O/'terminals'; d.mkdir(exist_ok=True)
 a=d/(label+'.stdout.RAW'); b=d/(label+'.stderr.RAW'); assert not a.exists() and not b.exists(); a.write_bytes(out); b.write_bytes(err)
 rec=dict(label=label,actual_foreground_PID=p.pid,actual_driver_PID=os.getpid(),command=[str(x) for x in args],terminal_closed=True,terminal_EXIT=p.returncode,started_UTC=start,finished_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),stdout=pin(a),stderr=pin(b)); save('terminals/'+label+'.receipt.json',rec)
 print(json.dumps(dict(END=label,PID=p.pid,EXIT=p.returncode)),flush=True); assert p.returncode==0,label; return out,rec
class Node:
 def __init__(self,tag='',attrs=None):self.tag=tag;self.attrs=dict(attrs or []);self.children=[]
 def all(self,tag=None):
  out=[self] if tag is None or self.tag==tag else []
  for n in self.children:
   if isinstance(n,Node):out+=n.all(tag)
  return out
 def text(self):return ''.join(x.text() if isinstance(x,Node) else x for x in self.children)
class Tree(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.root=Node();self.stack=[self.root]
 def handle_starttag(self,t,a):
  n=Node(t,a);self.stack[-1].children.append(n)
  if t not in ['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr']:self.stack.append(n)
 def handle_endtag(self,t):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i].tag==t:self.stack=self.stack[:i];break
 def handle_data(self,s):self.stack[-1].children.append(s)
def prepare():
 j=load(DIS); assert j['checked_science_commit']==SCI and len(j['inputs'])==131
 for z in j['inputs']:check(z)
 save('inputs.manifest.json',dict(dispatch=pin(DIS),input_count=131,inputs=j['inputs']))
 save('initial-frozen-input-check.json',dict(status='PASS',actual_PID=os.getpid(),current_RAW_and_CRLF_pairs_only_LF_checked=131,dispatch=pin(DIS),earlier_readonly_pin_check_PID=36144,earlier_readonly_pin_check_EXIT=0))
 save('inspection-setup-negative.json',dict(status='PRESERVED_READONLY_INSPECTION_SCHEMA_NEGATIVE',terminal_EXIT=1,actual_foreground_PID=None,PID_basis='Not printed by that ad hoc inspection; no PID is invented.',exact_stdout='',exact_stderr='Traceback (most recent call last):\n  File "<string>", line 1, in <module>\nKeyError: \'conditions\'\n',failed_expression='lesson["units"][0]["conditions"]',diagnosis='Current native lesson schema uses assumptions, not conditions. A read-only display query used an obsolete field name. No input or evidence changed.',corrected_readonly_inspection_PID=8228,corrected_readonly_inspection_EXIT=0,mathematical_or_gate_failure=False))
 observations=[]
 for z in j['inputs']:
  if z['path'].endswith('.png'):
   name=Path(z['path']).name
   if 'branch-' in name:note='Compiled actual first-clock node and three direct relationships visible; large-context graph labels remain dense. Legend distinguishes imports/ownership/reference signals and conceptual structure.'
   elif 'proof-' in name:note='Corresponding numbered formula and prose proof step visibly rendered with adjacent initially folded Lean. Long formula rows may require horizontal scrolling.'
   else:note='Attributed complete ten-group statement, six original analytic callers, extended-time and remaining-process boundary visible; full Lean panels initially folded. Plain compact full-statement notation remains a reader debt.'
   observations.append(dict(input_pin=z,actually_viewed_with='tools.view_image',independently_viewed=True,observation=note))
 assert len(observations)==12; save('independent-PNG-observations.json',dict(actor=ACTOR,independent_of_root_viewing=True,independently_viewed_PNGs=12,records=observations,physical_OS_clipboard_test=False))
 print(json.dumps(dict(status='PREPARED',actual_PID=os.getpid(),inputs=131,actual_independent_PNG_views=12)))
def finite_closed(lp,rows,extra=None,directory=None):
 lp=resolve(lp); directory=resolve(directory) if directory else lp.parent; extra={resolve(x).resolve() for x in (extra or [lp])}
 expected={resolve(z['path']).resolve() for z in rows}|extra; actual={p.resolve() for p in directory.rglob('*') if p.is_file()}; assert actual==expected,(directory,len(actual),len(expected))
 for z in rows:check(z);assert resolve(z['path']).stat().st_mtime_ns<=lp.stat().st_mtime_ns,z['path']
 return dict(lease=pin(lp),owned_files=len(actual),all_native_owned_RAW_LF_unchanged=True,mathematics_recertified=False,source_recertified=False)
def native_reuse():
 results=[]
 # Read finite native leases in their actual schemas, preserving all role distinctions.
 lp=R/'independent-math75/lease.final.json'; l=load(lp); assert l['status']=='CLOSED_LAST'; check(l['manifest']); m=load(resolve(l['manifest']['path'])); rows=m['entries']; assert len(rows)==m['entry_count'] and sha(can(rows))==m['logical_entries_sha256'] and len(rows)+2==l['owned_files']==46
 q=finite_closed(lp,rows,[lp,resolve(l['manifest']['path'])]);q['kind']='accepted-independent-math75';results.append(q)
 for name,count in [('independent-clean-source75',52),('independent-clean-source75-admission-overlay',19)]:
  lp=R/name/'CLOSED_LAST.json';l=load(lp);assert l['status']=='CLOSED_LAST' and l['actual_EXIT']==0;rows=l['complete_owned_prior_manifest'];assert len(rows)==l['complete_owned_prior_file_count'] and len(rows)+1==count;q=finite_closed(lp,rows);q['kind']=name;results.append(q)
 lp=R/'exact-science-verification75/lease.final.json';l=load(lp);rows=l['all_owned_outputs_except_only_self'];assert l['status']=='CLOSED_LAST' and l['VERIFIED'] and l['all_sessions_closed'] and l['verified_commit']==SCI and len(rows)+1==l['owned_count']==94 and sha(can(rows))==l['closure_logical_sha256'];q=finite_closed(lp,rows);q['kind']='prior-nonowner-exact-SCI75';results.append(q)
 lp=R/'independent-source75/lease.final.json';l=load(lp);assert l['status']=='CLOSED_LAST' and not l['source_admission_ready'] and l['source_status']=='SUPPLEMENTAL_SOURCE_REVIEW_NOT_ANTI_ANCHORED';assert len(l['files'])==l['file_count']==81;q=finite_closed(lp,l['files']);q['kind']='exposed-review-administrative-metadata-only-not-clean-source-admission';results.append(q)
 a=load(R/'root.decoder75.adoption.json');check(a['native_lease']);check(a['native_complete_payload']);native_lp=resolve(a['native_lease']['path']);l=load(native_lp);assert l['status']=='CLOSED' and native_lp.read_bytes()==(R/'anonymous-decoder/CLOSED_LAST.json').read_bytes();assert len(l['allowed_owned_files'])==4 and len(l['bound_prior_owned_files'])==3 and l['closed_exit_receipt']['exit_code']==0
 q=finite_closed(native_lp,l['bound_prior_owned_files']);q['kind']='strict-blind-decoder75-native-four-file-directory';results.append(q)
 for name,keys in [('root.math75.adoption.json',['native_lease','native_complete_named']),('root.source75.adoption.json',['native_whole_five_payload','native_lease','administrative_overlay_lease','administrative_overlay_complete_payload']),('root.exact-verification75.adoption.json',['native_complete_named','native_lease','unique_VERIFIED_append'])]:
  a=load(R/name)
  for key in keys:check(a[key])
 am=load(R/'root.math75.adoption.json');assert am['readonly_EXIT']==0 and am['fresh_compiler']['fresh_source_elaboration'] and not am['fresh_compiler']['Lake_build_cache_replay'] and am['fresh_compiler']['actual_foreground_Lean_PID']==18716 and am['fresh_compiler']['axiom_audit_PID']==21324 and len(am['fresh_compiler']['standard_axioms'])==3
 for key in ['compiler_receipt','axiom_audit_receipt']:
  check(am['fresh_compiler'][key]);rec=load(resolve(am['fresh_compiler'][key]['path']));assert rec['terminal_closed'] and rec['terminal_EXIT']==0
 ass=load(R/'root.source75.adoption.json');assert ass['native_readonly_EXIT']==ass['overlay_readonly_EXIT']==0 and ass['earlier_exposed_source_not_adopted'] and ass['coverage_counts']==dict(node_count=32,edge_count=67,item_count=137,NODE=77,EXCLUDED=60,internal_bridge_count=13)
 ae=load(R/'root.exact-verification75.adoption.json');assert ae['native_readonly_EXIT']==0 and ae['native_verified'] and ae['verified_commit']==SCI and not ae['full_RAW_whitespace_PASS'] and ae['authored_complement_PASS']
 return results
def check_child():
 im=load(O/'inputs.manifest.json');assert im['inputs']==load(DIS)['inputs'] and im['input_count']==131
 for z in im['inputs']:check(z)
 src=(ROOT/MOD).read_bytes();assert sha(src)==SOURCE and len(src)==21771;lines=src.splitlines(keepends=True);assert len(lines)==396
 u=load(ROOT/'website/content/declaration_lessons/pbps-actual-hazard-clock.json')['units'][0];pub=load(ROOT/'website/content/publications/pbps-actual-hazard-clock.json')['items'][0];a=load(ROOT/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualHazardClock.json');cell=load(ROOT/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-hazard-clock.json')
 assert len(u['steps'])==9 and u['declaration']==DECL and pub['bindings'][0]['declaration']==DECL
 spans=[]
 for i,s in enumerate(u['steps']):
  q=s['lean_source_region'];b=b''.join(lines[q['start_line']-1:q['end_line']]);assert b.decode()==s['lean'] and sha(b)==q['exact_code_raw_sha256'] and q['source_raw_sha256']==SOURCE and q['path']==MOD;assert s['formula'] and s['text'];spans.append(dict(step=i+1,title=s['title'],start_line=q['start_line'],end_line=q['end_line'],exact_BODY_RAW_sha256=sha(b)))
 assert [(z['start_line'],z['end_line']) for z in spans]==[(136,150),(151,169),(170,189),(251,291),(292,326),(327,341),(342,359),(360,368),(369,393)]
 assert all(t in u['statement'] for t in ['rank zero','C²','α≤β','βη≤1','η>0','τ_z(0)=0','∞','pushforward','Recursive paths','remain open'])
 assert 'six original analytic callers' in ' '.join(u['assumptions']) and 'never supplied as callers' in ' '.join(u['assumptions'])
 for h in ['hα','hαβ','hV','hH','hη','hβη']:assert '('+h+' :' in src.decode()
 sys.path.insert(0,str(ROOT/'tools'));import astis_publication as ap
 data=dict(declarations={DECL:SimpleNamespace(source_file=MOD)},lessons={DECL:u});binding=ap.binding_digest(pub,pub['bindings'][0],data);context=ap.review_context(pub,pub['bindings'][0],data)
 assert binding==a['publication_binding_sha256'] and context==a['publication_context'];assert a['state']=='accepted' and a['verdict']=='equivalent-after-elaboration';assert a['source_review']['reviewer']=='/root/independent_clean_source75' and a['source_review']['independent_from_formalizer'] and a['source_review']['independent_from_decoder']
 html=(ROOT/'_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html').read_text(encoding='utf8');start=html.index('<section id="pbps-actual-hazard-clock"');end=html.find('<section id=',start+1);fragment=html[start:end if end!=-1 else None];t=Tree();t.feed(fragment);article=next(n for n in t.root.all('article') if n.attrs.get('data-authored-declaration')==DECL);details=article.all('details');assert len(details)==16 and all('open' not in n.attrs for n in details);codes=[n.text() for n in article.all('code') if 'language-lean' in n.attrs.get('class','')];assert len(codes)==13
 for s in u['steps']:assert s['lean'] in codes and s['formula'] in fragment and s['text'] in article.text()
 assert u['statement'] in article.text() and 'private def actual_integrated_hazard_clock_statement' in article.text() and 'private theorem actual_hazard_primitive_laws' in article.text()
 vis=R/'integration75/visual75';copy=load(vis/'copy-unit0-copy-and-download.inspect.json');assert copy['initialFolded'] and copy['copyProbeUsesIsolatedPageClipboardCallback'] and not copy['physicalOSClipboardTest'] and copy['closedLeanDetails']==16;assert len(copy['panels'])==len(copy['downloads'])==4 and len(copy['steps'])==9
 panel_rows=[]
 for p in copy['panels']:
  assert p['callbackCalled'] and p['copiedExactly'] and p['status']=='Copied' and p['code'] in codes and p['code'] in src.decode();panel_rows.append(dict(code_UTF8_RAW_bytes=len(p['code'].encode()),code_RAW_sha256=sha(p['code'].encode()),exact_continuous_module_fragment=True,callbackCalled=True,copiedExactly=True))
 for d in copy['downloads']:assert d['status']==200 and d['text'].encode()==src and d['bytes']==len(d['text'])
 for s,ss in zip(u['steps'],copy['steps']):assert s['lean']==ss['lean'] and ss['initiallyFolded']
 render=load(vis/'render-capture.json');cc=load(vis/'copy-capture.json');assert render['ownedBrowserExit']['code']==cc['ownedBrowserExit']['code']==0 and len(render['records'])==11 and len(cc['records'])==1
 pngs=[z for z in im['inputs'] if z['path'].endswith('.png')];assert len(pngs)==12 and len(load(O/'independent-PNG-observations.json')['records'])==12
 sys.path.insert(0,str(ROOT/'website/scripts'));import publication_reader
 graph=load(ROOT/'_site/data/underlying-lean-graph.json');assert graph['publication_inputs_sha256']==publication_reader.graph_input_digest();mid='module:'+DECL.rsplit('.',1)[0];did='decl:'+DECL;nodes={n['id']:n for n in graph['nodes']};assert nodes[mid]['status']==nodes[did]['status']=='compiled';direct=[e for e in graph['edges'] if e['source']==did or e['target']==did];assert len(direct)==3 and any(e['source']==mid and e['relation']=='declares' for e in direct) and any(e['relation']=='source correspondence; not a Lean dependency' for e in direct) and any(e['relation']=='Lean target under audit' for e in direct)
 for parent in ['ActualHarmonicFlow','ActualBounceRate']:assert any(e['source']=='module:AutoSamplingTheory.ExampleCases.ProximalBPS.'+parent and e['target']==mid and e['relation']=='imports' for e in graph['edges'])
 assert cell['status']=='independently_verified'
 gates=[]
 for z in im['inputs']:
  if z['path'].endswith('/receipt.json') and '/integration75/' in z['path']:
   q=load(resolve(z['path']))
   if 'exit_code' in q:
    assert q['terminal_closed'] and q['exit_code']==0 and q['checked_parent']==SCI
    for key in ['stdout','stderr']:check(q[key])
    gates.append(dict(label=Path(z['path']).parent.name,actual_foreground_PID=q['actual_foreground_PID'],terminal_EXIT=0,terminal_closed=True,receipt=z))
 assert len(gates)==18
 logs=lambda name:(R/'integration75'/name/'stdout.log').read_text(encoding='utf8')
 assert all(x in logs('mandatory-astis-check-final') for x in ['ASTIS check passed','Build completed successfully (9186 jobs).','Build completed successfully (9486 jobs).']);assert '245 source items' in logs('publication-final') and '524 compiled local leaves' in logs('website-ci-build') and 'ASTIS site check passed' in logs('site-check-final') and '"omitted_connections": 0' in logs('graph-check-final')
 for name in ['reader-render-current','reader-copy-download']:assert 'CLOSED' in logs(name)
 notes=load(R/'integration.notes.json');assert notes['proof_commit']==SCI and notes['registry_count']==524 and notes['publication_units']==245 and notes['root_jobs']==9186 and notes['test_jobs']==9486 and len(notes['checks'])==17 and notes['publication_inputs_sha256']==graph['publication_inputs_sha256'];check(notes['current_graph'])
 affected=load(R/'integration75/affected-module-graph/affected-graph.receipt.json');assert affected['actual_root_PID']==51732 and len(affected['outputs'])==5 and not affected['canonical_tool_source_changed'] and not affected['official_whole_module_graph_refresh_command_run'] and affected['unrelated_cards_external_indexes_leaf_docs_and_manifest_untouched']
 before=load(R/'integration75/before-generator-state.json');protected={resolve(p).resolve() for p in before['preexisting_tracked_changes']+before['untracked_cards']};changed=set()
 for z in affected['outputs']:check(z);changed.add(resolve(z['path']).resolve())
 assert not (changed & protected) and changed <= {resolve(p).resolve() for p in before['keep']}
 diagnosis=load(R/'delivery-helper-panel-count75/diagnosis.json');assert diagnosis['negative_PID52936_EXIT1_preserved'] and not diagnosis['Lean_changed'] and not diagnosis['canonical_changed'] and not diagnosis['closed_evidence_changed']
 observer=[]
 for z in diagnosis['changes']:
  current=resolve(z['path']);old=R/'delivery-helper-panel-count75'/(current.name+'.before.exactraw.snapshot');assert sha(old.read_bytes())==z['before_RAW_sha256'] and sha(current.read_bytes())==z['after_RAW_sha256'];observer.append(dict(before=pin(old),current=pin(current)))
 old=(R/'delivery-helper-panel-count75/record-integration75.py.before.exactraw.snapshot').read_text(encoding='utf8');current=resolve(diagnosis['changes'][0]['path']).read_text(encoding='utf8');assert "==3" in old and "==4" in current
 inspection=load(R/'visual.inspection.json');assert inspection['copy_callbacks']==inspection['RAW_downloads']==4 and inspection['formula_BODY_steps']==9 and inspection['actual_root_PID']==7660
 reuse=load(R/'integration75/unchanged-regression-reuse.json');assert reuse['unchanged_Git_and_workspace'] and not reuse['fresh_full_suite_or_full_browser_for75'] and 'Historical executable RAW hashes were not recorded' in reuse['runtime_qualification'];prior=[]
 for x in reuse['records']:
  check(x['receipt']);check(x['stdout']);check(x['stderr']);q=load(resolve(x['receipt']['path']));assert q['exit_code']==0 and q['terminal_closed'] and not x['fresh_for75'];prior.append(dict(label=x['label'],receipt=x['receipt'],actual_foreground_PID=q['actual_foreground_PID'],terminal_EXIT=0))
 for x in reuse['current_runtime_pins']:check(x['current_pin']);assert x['mtime_predates_reused_runs'] and x['historical_RAW_hash_not_recorded']
 vf=load(R/'verified.json');assert vf['status']=='VERIFIED' and vf['verifier_id']=='/root/exact_science63' and vf['owner_id']!=vf['verifier_id'] and vf['verified_commit']==SCI and vf['transition_count']==1 and not vf['aggregate'] and not vf['current_reader'];assert vf['event']['from_state']=='PROVED_LOCAL' and vf['event']['to_state']=='VERIFIED' and vf['event']['worker_id']==vf['verifier_id'];append=check(vf['exact_append']);assert json.loads(append)==vf['event']
 ledger=(ROOT/'runs/substantive_advances.jsonl').read_bytes();before_n=vf['ledger_before']['RAW_bytes'];after_n=vf['ledger_after']['RAW_bytes'];assert sha(ledger[:before_n])==vf['ledger_before']['RAW_sha256'] and sha(ledger[:after_n])==vf['ledger_after']['RAW_sha256'] and ledger[before_n:after_n]==append
 transitions=[j for b in ledger.splitlines() if b.strip() for j in [json.loads(b)] if j.get('advance_id')==vf['advance_id'] and j.get('to_state')=='VERIFIED'];assert len(transitions)==1 and transitions[0]==vf['event']
 native=native_reuse()
 result=dict(status='PASS_SCOPED_CURRENT_READER_FINITE_CHECKS',actual_foreground_PID=os.getpid(),checked_science_commit=SCI,all_dispatch_RAW_LF_pins=131,source_module=pin(ROOT/MOD),complete_module_lines=396,formula_BODY_spans=spans,initially_closed_details=16,exact_Lean_code_panels=13,copy_panel_fragments=panel_rows,copy_callbacks=4,RAW_downloads=4,download_UTF8_RAW_bytes=len(src),download_Javascript_character_count=len(src.decode()),publication_binding_sha256=binding,publication_context_exact=True,source_binding_reused_unchanged=True,source_and_decoder_distinct=True,native_reviews_reused=native,current_gate_receipts=gates,current_graph_digest=graph['publication_inputs_sha256'],direct_graph_connections=direct,graph_labels_dense=True,graph_not_theorem_implication=True,affected_generator_outputs=affected['outputs'],no_preexisting_or_untracked_collaborator_path_overwritten=True,prior_full_regressions_reused=prior,runtime_qualification=reuse['runtime_qualification'],observer_count_failure_PID=52936,observer_count_failure_EXIT=1,observer_negative_basis='Frozen diagnosis, retained exact before-helper snapshots and explicit root terminal report; not invented independent receipt.',observer_repaired_admin_PID=7660,observer_repaired_admin_EXIT=0,observer_helper_pins=observer,physical_OS_clipboard_test=False,prior_unique_VERIFIED_transition_reused_only=True,new_VERIFIED_transition=False,new_independent_mathematics_certification=False)
 print(json.dumps(result,ensure_ascii=False))
def checks():
 out,headrec=command('checked-current-HEAD',['git','rev-parse','HEAD']);assert out.decode().strip()==SCI
 out,src=command('exact-SCI-module-Git-RAW',['git','show',SCI+':'+MOD]);assert out==(ROOT/MOD).read_bytes()
 regions=['tools','website/scripts','website/static','.github/workflows','lean-toolchain','lake-manifest.json']
 out,gitrec=command('unchanged-reused-helper-Git-diff',['git','diff','bc3dca8d76432f71e3abbfdbce2c3b2161ec8d19','HEAD','--']+regions);assert not out
 out,wrec=command('unchanged-reused-helper-workspace-diff',['git','diff','--']+regions);assert not out
 out,rec=command('independent-finite-reader-checks',[PY,'-B','-X','utf8',O/'review75.py','check-child']);result=json.loads(out);assert result['status'].startswith('PASS_');save('checks.json',dict(result=result,actual_terminal_receipts=[headrec,src,gitrec,wrec,rec]))
def close():
 assert not (O/'lease.final.json').exists();im=load(O/'inputs.manifest.json');checks=load(O/'checks.json');assert checks['result']['status']=='PASS_SCOPED_CURRENT_READER_FINITE_CHECKS';views=load(O/'independent-PNG-observations.json')
 for z in im['inputs']:check(z)
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==SCI
 debts=['The complete statement uses compact plain notation; long formula rows may require horizontal scrolling.','The selected graph branch is usable, but full-context labels remain dense; references and conceptual relations are not theorem implication.','Copy probes exercise isolated page callbacks only; physical OS clipboard and deployed/live-site behavior were not tested.','Full Chapter1.3/whole-paper Exposition Seal and postmerge purification remain open.','Recursive PDMP construction, iid sequence/SLLN/nonexplosion, Markov memorylessness, invariance/reversal and terminal sampling kernels remain open; main bounds, errors, expected-query costs and actual-input composition are not admitted.','The source-module prospective top comment is retained historical seal text and is stale process documentation; the proof and closed admissions are separately exact.','Earlier full Python/browser regression reuse has same-path/mtime continuity evidence only; historical executable RAW hashes were not recorded.']
 d=dict(status='ACCEPTED_SCOPED_AGGREGATE_CURRENT_READER75_WITH_READER_DEBT',accepted_scoped_aggregate=True,actor=ACTOR,checked_science_commit=SCI,independent_of_formalizer_stabilizer=True,new_VERIFIED_transition=False,new_independent_mathematics_certification=False,blockers=[],reader_debts=debts,Registry=524,publication_units=245,formula_BODY_steps=9,independently_viewed_PNGs=12,independently_viewed_PNG_records=views['records'],copy_callbacks=4,RAW_downloads=4,Goal_complete=False,PURIFIED=False,full_Exposition_Seal=False,main=False,live=False,whole_paper=False)
 save('decision.json',d)
 text='Independent scoped repository/current-reader review75\n\nACCEPTED for the exact frozen serialized aggregate at SCI '+SCI+'. All 131 dispatch RAW pins and CRLF-pairs-only LF pins were checked, and the complete 396-line source is byte-identical to Git at SCI. This is reader/aggregate acceptance, not a new proof, source verdict or VERIFIED transition.\n\nThe attributed complete ten-group statement retains the six analytic callers, actual flow/rate, weighted half-sum energy and actual exponential pushforward. Infinity, rank zero, zero energy and zero threshold remain legal. Nine formula/prose steps bind the exact contiguous compiled BODY spans, including three primitive-helper blocks. All 16 adjacent Lean/details start folded; the private literal and actual proved primitive are supplied next to the public statement/proof. Four distinct full-code copy callbacks succeed with exact continuous module fragments, and four HTTP200 downloads reproduce all 21771 source UTF8 bytes (19880 JavaScript characters). All twelve frozen PNGs were independently viewed; visual content agrees with the static/source and native browser evidence.\n\nThe accepted clean source review is distinct from the earlier exposed supplemental review and strict blind decoder; all finite native closed owned hashes remain unchanged. Accepted independent fresh-source Lean18716/0 and standard-axiom21324/0, clean-source/administrative overlay and nonowner exact SCI75 closures are reused unchanged. The already unique VERIFIED transition by /root/exact_science63 is read-only checked. No credit is created by this review.\n\nEighteen actual terminal-closed successful gate receipts bind the current SCI, including mandatory ASTIS root9186/Tests9486, Registry524, publication245, final source/semantic/frontier/contributor/site/graph and current scoped browsers. The current graph publication digest is independently recomputed, with compiled module/declaration, two actual formal-parent imports and three correctly typed direct declaration relations. The five narrow generated outputs are exact and disjoint from preexisting tracked/untracked collaborator paths. Full prior Python/browser regressions are reused under the explicit runtime qualification, never historical executable byte identity.\n\nThe original observer52936/1 is preserved by its frozen diagnosis and exact before-helper snapshots: the observer expected three panels although the already-successful browser recorded four. Repaired admin7660/0 counts four; Lean/source/native browser did not change. The read-only inspection KeyError conditions is retained separately and diagnosed against the native assumptions field.\n\nReader debts and retained boundaries:\n'+'\n'.join('- '+x for x in debts)+'\n'
 rp=O/'named-review75.txt';assert not rp.exists();rp.write_text(text,encoding='utf8',newline='\n')
 payload=dict(schema='independent-scoped-reader75-complete-named-RAW/v1',decision=d,inputs=im,named_review_UTF8=text,full_exact_module_UTF8=(ROOT/MOD).read_bytes().decode('utf8'),checks=checks,PNG_observations=views,inspection_setup_negative=load(O/'inspection-setup-negative.json'))
 save('complete.named.RAW-payload.json',payload)
 run=dict(schema='independent-scoped-repository-reader75/v1',actor=ACTOR,checked_science_commit=SCI,decision=pin(O/'decision.json'),inputs_manifest=pin(O/'inputs.manifest.json'),complete_named_RAW_payload=pin(O/'complete.named.RAW-payload.json'),named_review=pin(rp),checks=pin(O/'checks.json'),owned_script=pin(O/'review75.py'),independent_PNG_observations=pin(O/'independent-PNG-observations.json'),writer_PID=os.getpid(),prior_owned_writer_PID=load(O/'initial-frozen-input-check.json')['actual_PID'],writer_EXIT_contract='Immediate successful return after final lease write; actual terminal and standalone readonly observer confirm termination.',whole_logical_recipe='SHA256 canonical sorted compact UTF8 JSON; remove ONLY top-level run_sha256; LF pins replace CRLF byte pairs only.',new_independent_mathematics_certification=False,new_VERIFIED_transition=False)
 run['run_sha256']=sha(can(run));save('run.json',run)
 rows=[pin(p) for p in sorted(O.rglob('*'),key=lambda p:p.as_posix()) if p.is_file()];assert all(not z['path'].endswith('lease.final.json') for z in rows)
 lease=dict(schema='independent-scoped-reader75-CLOSED-LAST/v1',status='CLOSED_LAST',actor=ACTOR,checked_science_commit=SCI,writer_PID=os.getpid(),all_prior_child_sessions_terminal_closed=True,completed_check_receipts=checks['actual_terminal_receipts'],postclose_owned_writes_forbidden=True,final_owned_write=True,files=rows,file_count_including_lease=len(rows)+1,closure_logical_sha256=sha(can(rows)),run_sha256=run['run_sha256'],actual_writer_EXIT_observation='Lease is last write; writer terminal EXIT0 and external readonly are separately observed, not assumed.',new_VERIFIED_transition=False)
 save('lease.final.json',lease)
 print(json.dumps(dict(status='CLOSED_LAST',actual_writer_PID=os.getpid(),run_sha256=run['run_sha256'],lease_RAW_sha256=sha((O/'lease.final.json').read_bytes()),complete_named_RAW_payload=run['complete_named_RAW_payload'],owned_count=lease['file_count_including_lease'],closure_logical_sha256=lease['closure_logical_sha256'],inputs=131),ensure_ascii=False))
def postclose():
 lp=O/'lease.final.json';l=load(lp);assert l['status']=='CLOSED_LAST' and l['actor']==ACTOR and l['postclose_owned_writes_forbidden'] and l['final_owned_write'];rows=l['files'];assert l['file_count_including_lease']==len(rows)+1 and sha(can(rows))==l['closure_logical_sha256'];assert {p.resolve() for p in O.rglob('*') if p.is_file()}=={resolve(z['path']).resolve() for z in rows}|{lp.resolve()}
 for z in rows:check(z);assert resolve(z['path']).stat().st_mtime_ns<=lp.stat().st_mtime_ns
 run=load(O/'run.json');assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==l['run_sha256'];assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==run['checked_science_commit']==SCI
 for key in ['decision','inputs_manifest','complete_named_RAW_payload']:check(run[key])
 d=load(resolve(run['decision']['path']));im=load(resolve(run['inputs_manifest']['path']));p=load(resolve(run['complete_named_RAW_payload']['path']));assert p['decision']==d and p['inputs']==im and im['inputs']==load(DIS)['inputs'] and len(im['inputs'])==im['input_count']==131;check(im['dispatch'])
 for z in im['inputs']:check(z)
 assert d['accepted_scoped_aggregate'] and d['independent_of_formalizer_stabilizer'] and not d['blockers'] and d['copy_callbacks']==d['RAW_downloads']==4 and d['formula_BODY_steps']==9 and d['independently_viewed_PNGs']==12 and d['Registry']==524 and d['publication_units']==245
 assert all(not d[key] for key in ['new_VERIFIED_transition','new_independent_mathematics_certification','Goal_complete','PURIFIED','full_Exposition_Seal','main','live','whole_paper'])
 k=ctypes.WinDLL('kernel32',use_last_error=True);k.OpenProcess.restype=ctypes.c_void_p;h=k.OpenProcess(0x00100000,False,l['writer_PID'])
 if h:k.WaitForSingleObject.argtypes=[ctypes.c_void_p,ctypes.c_ulong];k.CloseHandle.argtypes=[ctypes.c_void_p];assert k.WaitForSingleObject(h,0)==0;k.CloseHandle(h)
 else:assert ctypes.get_last_error()==87
 print(json.dumps(dict(status='PASS',actual_external_readonly_PID=os.getpid(),writer_PID=l['writer_PID'],writer_terminated=True,owned_files=l['file_count_including_lease'],current_inputs=131,run_sha256=run['run_sha256'],lease_RAW_sha256=sha(lp.read_bytes()),complete_named_RAW_sha256=run['complete_named_RAW_payload']['RAW_sha256'],closure_logical_sha256=l['closure_logical_sha256'],no_owned_writes=True,new_VERIFIED_transition=False)))
if __name__=='__main__':{'prepare':prepare,'checks':checks,'check-child':check_child,'close':close,'postclose':postclose}[sys.argv[1]]()
