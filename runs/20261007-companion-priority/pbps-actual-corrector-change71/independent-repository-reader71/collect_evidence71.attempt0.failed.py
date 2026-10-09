import hashlib,json,os,pathlib,subprocess,difflib
from html.parser import HTMLParser
R=pathlib.Path('E:/Samplinglib');r=R/'runs/20261007-companion-priority/pbps-actual-corrector-change71';OWN=r/'independent-repository-reader71'
def get(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();return {'path':p.as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(b.replace(b'\r\n',b'\n')),'LF_sha256':sha(b.replace(b'\r\n',b'\n'))}
def dump(n,d):(OWN/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
p=get(r/'final-reader-repository-packet71.json');assert sha((r/'final-reader-repository-packet71.json').read_bytes())=='ce23377e2799a9617f19cf7bceefd69bc7b2078e47ad16a463a3950adb8cad06'
assert len(p['inputs'])==127 and len({x['path'] for x in p['inputs']})==127
for x in p['inputs']:
 a=pin(x['path']);assert all(a[k]==x[k] for k in ['RAW_bytes','RAW_sha256','LF_sha256']),x['path']
SCI=p['checked_science_commit'];assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==SCI
base=subprocess.check_output(['git','rev-parse','origin/main'],cwd=R).decode().strip()
extras=[];science=[]
paths=['AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean','website/content/publications/pbps-actual-corrector-change.json','website/content/declaration_lessons/pbps-actual-corrector-change.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualCorrectorChange.json']
for path in paths:
 frozen=subprocess.check_output(['git','show',SCI+':'+path],cwd=R);current=(R/path).read_bytes();assert current==frozen
 science.append({'path':path,'SCI_RAW_sha256':sha(frozen),'current_RAW_sha256':sha(current),'exact_RAW_equal':True})
rootgates=[]
for x in p['inputs']:
 if x['path'].endswith('/receipt.json') and '/generator-sideeffects/' not in x['path']:
  a=get(x['path']);assert a['exit_code']==0 and a['terminal_closed'] is True
  for k in ['stdout','stderr']:
   assert all(pin(a[k]['path'])[j]==a[k][j] for j in ['RAW_bytes','RAW_sha256','LF_sha256'])
  rootgates.append({'label':pathlib.Path(x['path']).parent.name,'receipt':pin(x['path']),'command':a['command'],'actual_foreground_PID':a['actual_foreground_PID'],'exit_code':0,'terminal_closed':True,'stdout':a['stdout'],'stderr':a['stderr']})
assert len(rootgates)==19
bounds=[]
for a in get(r/'integration71/owned-before.json')['owned']:
 path=R/a['exact_snapshot'];extras.append(pin(path));b=path.read_bytes();assert sha(b)==a['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==a['LF_sha256']
 old=b.decode();new=(R/a['path']).read_text(encoding='utf-8');lines=[z for z in difflib.unified_diff(old.splitlines(),new.splitlines(),n=0) if z[:1] in ['+','-'] and not z.startswith(('+++','---'))]
 bounds.append({'path':a['path'],'before':pin(path),'current':pin(R/a['path']),'changed_line_count':len(lines),'complete_changed_lines':lines})
for rel in ['integration71/cell.0.before-final-admin.exactraw.snapshot.json','independent-source71/complete-named-review-decision-input-payload.json']:
 extras.append(pin(r/rel))
source=get(r/'independent-source71/complete-named-review-decision-input-payload.json');assert source['native_run_complete']['actor']=='/root/independent_primary69'
reuse={}
for label in ['source','math','decoder','exact-verification']:
 a=get(r/('root.'+label+'71.adoption.json'))
 reuse[label]={'adoption':pin(r/('root.'+label+'71.adoption.json')),'status':a['status'],'native_whole_logical_run_sha256':a.get('native_whole_logical_run_sha256'),'native_owned_count':a.get('native_owned_files',a.get('native_files'))}
reuse['source']['sole_source_credit_actor']=source['native_run_complete']['actor'];reuse['source']['native_counts']=source['native_run_complete']['counts'];reuse['source']['no_new_source_verdict']=True
for rel,n in [('independent-source71/lease.final.json',277),('independent-math71/lease.final.json',95),('exact-science-verification71/lease.final.json',116),('anonymous-decoder/lease.closed.json',10)]:
 a=get(r/rel);assert a['status']=='CLOSED_LAST';print('reused-closed',rel,n)
reuse['science_exact_commit']=SCI
unit=get(R/paths[2])['units'][0];src=(R/paths[0]).read_bytes();text=src.decode();lines=src.splitlines(keepends=True);copy=get(r/'integration71/visual71/copy-unit0-copy-and-download.inspect.json')
assert len(lines)==528 and len(unit['steps'])==8 and len(copy['steps'])==8
body=[]
for i,step in enumerate(unit['steps']):
 a=step['lean_source_region'];b=b''.join(lines[a['start_line']-1:a['end_line']]);assert sha(b)==a['exact_code_raw_sha256'];assert a['source_raw_sha256']==sha(src);assert copy['steps'][i]['lean'] in text;assert copy['steps'][i]['initiallyFolded'] is True
 body.append({'ordinal':i+1,'title':step['title'],'formula':step['formula'],'region':a,'BODY_lines':a['end_line']-a['start_line']+1,'exact_source_bound':True,'initially_folded':True})
assert sum(a['BODY_lines'] for a in body)==377
assert len(copy['panels'])==3 and len(copy['downloads'])==3 and copy['initialFolded'] is True
for a in copy['panels']:assert a['callbackCalled'] and a['copiedExactly'] and a['code'] in text
for a in copy['downloads']:assert a['status']==200 and a['text'].encode()==src
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.depth=0;self.active=False;self.details=[];self.codes=[];self.current=None;self.links=[]
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='section':
   if d.get('id')=='pbps-actual-corrector-change':self.active=True
   if self.active:self.depth+=1
  if self.active:
   if t=='details':self.details.append(d)
   if t=='code':self.current=[]
   if t=='a':self.links.append(d)
 def handle_data(self,d):
  if self.active and self.current is not None:self.current.append(d)
 def handle_endtag(self,t):
  if self.active and t=='code' and self.current is not None:self.codes.append(''.join(self.current));self.current=None
  if self.active and t=='section':
   self.depth-=1
   if self.depth==0:self.active=False
h=Parser();h.feed((R/'_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html').read_text(encoding='utf-8'))
assert len(h.details)==14 and all('open' not in a for a in h.details)
assert len([a for a in h.details if 'data-lean-code-panel' in a])==3
for a in copy['panels']:assert a['code'] in h.codes
helper=copy['panels'][2]['code'];assert helper.startswith('private def actual_corrector_change_statement') and 'Prop :=' in helper and len(helper.splitlines())==121
assert len([a for a in h.links if 'download' in a])==3
for a in copy['steps']:assert a['lean'] in h.codes
download=R/'_site/downloads/lean/AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean';assert download.read_bytes()==src;extras.append(pin(download))
g=get(R/'_site/data/underlying-lean-graph.json');focus='decl:'+unit['declaration'];node=[a for a in g['nodes'] if a['id']==focus];assert len(node)==1 and node[0]['status']=='compiled'
edges=[a for a in g['edges'] if a['source']==focus or a['target']==focus];assert len(edges)==5
assert len([a for a in edges if a['relation']=='declares'])==1
assert len([a for a in edges if a['relation']=='source reference (scanner)'])==2
assert not any('Tests.' in str(a) or 'conceptual' in str(a).lower() for a in edges)
for path in ['tools/astis_publication.py','tools/astis_contributor_contract.py','website/scripts/check_site.py']:
 extras.append(pin(R/path))
verified=get(r/'verified.json');assert verified['status']=='VERIFIED'
evidence={'schema':'repository-reader71-bounded-independent-evidence-v1','actor':'/root/anonymous_decoder71','actual_collector_PID':os.getpid(),'checked_science_commit':SCI,'origin_main_readonly_base_commit':base,'reviewed_packet':pin(r/'final-reader-repository-packet71.json'),'all127_current_inputs_exact':True,'science_raw_unchanged':science,'reused_native_adoptions':reuse,'root19_terminal_gates':rootgates,'admin_differences':bounds,'admin_limit':'Registry/import/Test519, cell status/shared gate/visual/admin, handoff/execution/conversion/module graph only; no science publication/lesson/audit mutation. Generator receipt retains exact backups and irrelevant generated changes were restored by owner.','BODY_steps':body,'BODY_lines':377,'module_lines':528,'literal_private_Prop':{'full_helper_chars':len(helper),'UTF8_bytes':len(helper.encode()),'lines':len(helper.splitlines()),'exact_source_and_rendered':True,'initially_folded':True,'adjacent_proof_helper':True,'representation_not_proof_provider':True},'reader_DOM':{'section':'pbps-actual-corrector-change','closed_details':14,'source_code_panels':3,'source_step_panels':8,'all_initially_closed':True,'complete_statement_chars':len(unit['statement']),'complete_statement':unit['statement'],'formula':unit['formula'],'boundary':unit['boundary']},'copy_download':{'callbacks':3,'callbacks_exact':True,'RAW_downloads':3,'all_RAW_equal_current_module':True,'RAW_UTF8_bytes_each':26489,'JS_character_count_each':24587,'physical_OS_clipboard_test':False,'live_deployment':False},'actual_graph_branch':{'focus_node':node[0],'exact_incident_edges':edges,'formal_declares':1,'dashed_name_scan_reference_edges':2,'semantic_audit_edge':1,'source_correspondence_edge':1,'complete_theorem_dependency_export':False,'source_graph_is_not_proof_completion':True},'failure_retention':{'root_freeze_old_decoder_lease_filename_PID45100_EXIT1_retained':True,'root_freeze_corrected_actual_lease_closed_PID8452_EXIT0':True,'canonical_or_native_math_changed_by_correction':False,'nonowner_VERIFIED_transition_EXIT1_after_successful_append_retained':True},'exposures':{'original_blind71_closed':True,'source_first72_closed_source_visible':True,'this_role_is_source_exposed':True,'new_blind_or_source_fidelity_credit':False,'self_decoder_source_credit':False},'extra_finite_input_pins':extras,'no_historical_recursive_payload_copies':True,'no_build_or_canonical_Git_ledger_Goal_old_CLOSED_writes':True}
dump('evidence71.json',evidence)
print(json.dumps({'PID':os.getpid(),'inputs':127,'extra_finite_inputs':len(extras),'root_gates':19,'SCI_exact_RAW_unchanged':4,'BODY_lines':377,'closed_details':14,'copy_callbacks':3,'RAW_downloads':3,'graph_incident':5,'EXIT':0}))
