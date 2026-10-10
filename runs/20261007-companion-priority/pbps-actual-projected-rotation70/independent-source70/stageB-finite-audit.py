import sys
sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os
O=pathlib.Path(__file__).resolve().parent
R=O.parent
def sha(b): return hashlib.sha256(b).hexdigest()
def load(n): return json.loads((O/n).read_bytes())
def save(n,x): (O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def logical(x): return sha(json.dumps({k:v for k,v in x.items() if k!='run_sha256'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
module=(O/'current70.source_body.exactraw.lean').read_bytes()
lines=module.splitlines(keepends=True)
old=(O/'original-source-reviewed70.header.exactraw.lean').read_bytes().splitlines(keepends=True)
assert len(lines)==544 and b''.join(lines[26:133])==b''.join(old[9:116])
assert lines[18:25]==old[1:8]
unit=load('current70.lesson.exactraw.json')['units'][0]
regions=[]
for i,s in enumerate(unit['steps']):
 d=s['lean_source_region']; a,z=d['start_line'],d['end_line']; raw=b''.join(lines[a-1:z])
 assert d['source_raw_sha256']==sha(module) and d['exact_code_raw_sha256']==sha(raw)
 assert s['lean'].encode()==raw.rstrip(b'\n')
 regions.append({'step':i+1,'start_line':a,'end_line':z,'RAW_bytes':len(raw),'RAW_sha256':sha(raw),'exact_lesson_code':True})
assert len(regions)==8 and regions[0]['start_line']==144 and regions[-1]['end_line']==539
assert all(a['end_line']+1==b['start_line'] for a,b in zip(regions,regions[1:]))
save('stageB.exact-header-and-eight-BODY-audit.json',{'schema':'independent-source70-finite-literal-and-code-v1','actual_pid':os.getpid(),'source_module_RAW_sha256':sha(module),'module_lines':544,'sealed_result_lines':[10,116],'current_literal_value_lines':[27,133],'literal_value_exact_byte_equal':True,'six_binders_exact_byte_equal':True,'representation':'private exact literal definition, public theorem asserts its value; definition is not proof provider','common_witnesses':['S','e','U','T','Γ','q','ΓP0','Inv','A0','B0','V0','R'],'body_lines':396,'body_range':[144,539],'eight_steps_exact_contiguous':True,'regions':regions,'compile_run_performed_by_reviewer':False})

# Exact bounded proposals: metadata only. No canonical writes.
pub=load('current70.publication.exactraw.json'); frontier=load('current70.frontier.exactraw.json')
oldword=pub['purification']['dead_code_audit'] if 'purification' in pub else pub['items'][0]['purification']['dead_code_audit']
newword='One public production theorem with an exact private literal statement definition; no proof provider or wrapper Test.'
formula_changes=[]
for i,s in enumerate(unit['steps']):
 before=s['formula']; after=before.replace('\\\\','\\')
 assert before!=after and '\\\\' not in after
 formula_changes.append({'json_pointer':'/units/0/steps/'+str(i)+'/formula','before':before,'after':after,'before_utf8_sha256':sha(before.encode()),'after_utf8_sha256':sha(after.encode())})
save('stageB.reader-metadata-overlay.proposal.json',{'schema':'independent-source70-reader-only-overlay-v1','scope':'No Lean, binder, definition, BODY, dependency or mathematical change. Reader metadata only. Root must apply only after separate review.','stale_dead_code_audit':{'publication_before':oldword,'recommended_after':newword,'fields':'publication and cell purification.dead_code_audit only','justification':'Complete actual statement is a private literal def at module18-133; no proof provider.'},'eight_formula_changes':formula_changes,'evidence':'website/scripts/declaration_lessons.py:159 places the unnormalized formula directly inside MathJax display delimiters via base.esc; main formula uses single TeX backslashes, eight step formulas incorrectly contain double literal backslashes.','decision':'recommend both reader corrections; no mathematical statement repair','applied_by_reviewer':False})

# Native blind closure is independently checked without importing mathematical verdicts.
D=R/'anonymous-decoder'; nm=json.loads((D/'native-manifest.json').read_bytes()); lease=json.loads((D/'lease.json').read_bytes())
checks=[]; snapshots=[]
for f in nm['files']:
 b=(D/f['path']).read_bytes(); assert len(b)==f['bytes'] and sha(b)==f['raw_sha256']
 checks.append({'path':f['path'],'bytes':len(b),'RAW_sha256':sha(b),'valid':True})
 for suffix in ('', '.LF'):
  n='blind70.native.'+f['path']+suffix; content=b if not suffix else b.replace(b'\r\n',b'\n'); dest=O/n
  if dest.exists(): assert dest.read_bytes()==content
  else: dest.write_bytes(content)
 snapshots.append({'source_path':str(D/f['path']),'RAW_snapshot':'blind70.native.'+f['path'],'LF_snapshot':'blind70.native.'+f['path']+'.LF','RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(b.replace(b'\r\n',b'\n')),'LF_sha256':sha(b.replace(b'\r\n',b'\n')),'LF_recipe':'replace only CRLF bytes with LF; no other transformation'})
assert len(checks)==10 and nm['file_count']==10 and lease['status']=='CLOSED_LAST'
for f in lease['bindings']:
 b=(D/f['path']).read_bytes(); assert sha(b)==f['raw_sha256'] and len(b)==f['bytes']
br=json.loads((D/'review-run.json').read_bytes()); assert logical(br)==br['run_sha256']==nm['whole_logical_run_sha256']==lease['whole_logical_run_sha256']
packet=load('current70.official-source-review.packet.0.exactraw.json')
assert br['lean_statement_sha256']=='27d7f794916d9bb2f1636b04fc7e71c702ad5248327d3df2af7d9d4a62b8a257'
save('stageB.blind-native-integrity.json',{'schema':'independent-source70-blind-native-integrity-v1','native_files':checks,'file_count':10,'native_manifest_RAW_sha256':sha((D/'native-manifest.json').read_bytes()),'lease_RAW_sha256':sha((D/'lease.json').read_bytes()),'native_lease_binding_count':len(lease['bindings']),'CLOSED_LAST':True,'whole_logical_sha256':br['run_sha256'],'whole_logical_recipe':'delete ONLY top-level run_sha256; sorted compact ensure_ascii=False UTF-8 JSON','neutral_packet_sha256':br['decoder_packet_sha256'],'seven_reconstruction_fields':list(load('blind70.slot-decisions.json')['reconstruction_fields']),'seal_actual_python_pid':lease['seal_python_pid'],'seal_parent_terminal_pid':lease['seal_parent_terminal_pid'],'native_seal_exit_not_present_not_invented':True,'native_files_unchanged':True})
save('stageB.blind-complete-input-manifest.json',{'schema':'exact-RAW-and-CRLF-only-LF-inputs-v1','inputs':snapshots})
print(json.dumps({'actual_pid':os.getpid(),'module_lines':len(lines),'literal_exact':True,'eight_BODY_steps_exact':True,'blind_native_files':len(checks),'reader_formula_repairs':8,'canonical_writes':False},ensure_ascii=False))
