from bindings64 import *
def main():
 assert load(OUT/'bindings.result.json')['status']=='PASS' and load(OUT/'gates.result.json')['status']=='PASS'
 paths={}
 for name in ['independent-math64','independent-source64','independent-auxiliary-overlay64','anonymous-decoder']:
  d=BASE/name
  if name=='independent-math64':rows=load(d/'lease.json')['complete_owned_output_manifest_after_readback'];ps=[pth(x['path']) for x in rows]+[d/'lease.json']
  elif name=='anonymous-decoder':ps=[d/x['path'] for x in load(d/'closure_manifest.json')['artifacts']]+[d/'closure_manifest.json',d/'lease.json']
  else:ps=[d/x['relative_path'] for x in load(d/'full-owned-manifest.json')['files']]+[d/'full-owned-manifest.json']
  for p in ps:paths[p.relative_to(ROOT).as_posix()]=p
 for x in load(OUT/'input.manifest.json')['inputs']:paths[pth(x['path']).relative_to(ROOT).as_posix()]=pth(x['path'])
 roots=[(BASE/n).relative_to(ROOT).as_posix() for n in ['independent-math64','independent-source64','independent-auxiliary-overlay64','anonymous-decoder']]
 raw=subprocess.check_output(['git','ls-tree','-rz',COMMIT,'--',*roots,*[p for p in paths if not any(p.startswith(r+'/') for r in roots)]],cwd=ROOT)
 tree={}
 for rec in raw.split(b'\0'):
  if rec:
   lhs,p=rec.split(b'\t',1);mode,typ,oid=lhs.decode().split();assert typ=='blob';tree[p.decode()]=oid
 committed=[]
 for rel,p in paths.items():
  assert rel in tree,('missing exact-commit native/input artifact',rel)
  b=p.read_bytes();oid=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
  if oid==tree[rel]:style='RAW-exact'
  else:
   gb=blob(COMMIT,rel);assert gb.replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n'),rel;style='RAW-distinct-LF-equal';assert rel not in {v['path'] for v in load(OUT/'mathematics-reuse.json')['three_exact_SOURCE_files']}
  committed.append({'path':rel,'committed_Git_blob_oid':tree[rel],'working_RAW_sha256':sha(b),'Git_working_byte_relation':style})
 # Overlay inputs: validate the eighteen RAW/LF snapshots and literal slices of the COMPLETE named RAW INPUT.
 overlay=BASE/'independent-auxiliary-overlay64';ov=load(overlay/'finite-diff-checks.json');pay=(overlay/'complete-inputs.named.raw.payload').read_bytes();assert sha(pay)=='29bd9f9678d49046e20969b7be6a93d4aa6a4a46fb4a6a48004627846f8ebaaa'
 for x in ov['input_maps']:
  b=(overlay/x['raw_snapshot']).read_bytes();lf=(overlay/x['lf_snapshot']).read_bytes();assert len(b)==x['raw_bytes'] and sha(b)==x['raw_sha256'] and b.replace(b'\r\n',b'\n')==lf and sha(lf)==x['lf_sha256'];assert pay[x['payload_byte_start']:x['payload_byte_end_exclusive']]==b
 assert len(ov['input_maps'])==18
 # Current step texts are precisely the accepted native statements/formulas, not only matching Lean fragments.
 source=BASE/'independent-source64';sr=load(source/'candidate-input-binding-and-span-checks.json');proof_text=[]
 for slug in ['real-l2-positive-square-order','pbps-centered-root-order-inverse']:
  current=load(ROOT/f'website/content/declaration_lessons/{slug}.json')['units'][0]
  row=next(x for x in sr['records'] if norm(x['source_path'])==norm(ROOT/f'website/content/declaration_lessons/{slug}.json'))
  old=load(source/row['raw_snapshot'])['units'][0]
  for k in ['statement','formula','assumptions','lean_statement','lean_proof','steps']:assert old[k]==current[k],(slug,k)
  proof_text.append({'lesson':slug,'mathematical_statement_assumptions_formula_and_all_steps_native_exact':True,'step_count':len(current['steps'])})
 terminal=[]
 for folder in ['independent-source64','independent-auxiliary-overlay64']:
  d=BASE/folder
  for n in ['foreground-finalizer.receipt.json','foreground-readback.receipt.json']:
   r=load(d/n);assert r['exit_code']==0 and r['terminal_closed'] and r['actual_foreground_pid']>0
   for k in ['stdout','stderr']:validate(r[k],d/r[k]['relative_path'])
   terminal.append({'folder':folder,'phase':n,'actual_pid':r['actual_foreground_pid'],'exit_code':r['exit_code'],'terminal_closed':True,'receipt':rawpin(d/n)})
 repairs=[]
 for x in load(BASE/'frontier-process-repair64/repair.json')['finite_historical_maps']:
  before=load(x['explicit_exact_raw_snapshot']['path']);after=load(x['current']['path'])
  if 'reuse_plan' in x['only_changed_field']:
   a=before['reuse_plan']['reused_declarations'];b=after['reuse_plan']['reused_declarations'];assert [v for v in b if v not in a]==[DECLS[0]] and [v for v in a if v not in b]==[]
  else:a=before['graph_contribution']['lean_view'];b=after['graph_contribution']['lean_view'];assert (a,b)==('reusable-interface','new-node')
  repairs.append({'only_field':x['only_changed_field'],'before':a,'after':b})
 changed=[p for p in subprocess.check_output(['git','diff','--name-only',PARENT,COMMIT,'--','AutoSamplingTheory','Tests','AutoSamplingTheory.lean','Tests.lean'],cwd=ROOT).decode().splitlines() if p.endswith('.lean')];expected=[x['path'] for x in load(OUT/'mathematics-reuse.json')['three_exact_SOURCE_files']];assert set(changed)==set(expected)
 write('supplemental-bindings.result.json',{'status':'PASS','checked_commit':COMMIT,'actual_pid':os.getpid(),'complete_closed_native_and_frozen_input_commit_bindings':committed,'bound_file_count':len(committed),'closed_native_folders_unchanged':True,'overlay_RAW_LF_and_complete_payload_slices':18,'accepted_formula_texts_and_statement_bindings':proof_text,'native_source_actual_terminal_evidence':terminal,'original_source_close_PID_debt':None,'only_process_field_values':repairs,'only_three_changed_Lean_files':changed,'mathematics_exact_Git_RAW_reuse':True,'no_source_statement_assumption_or_proof_change':True})
 print(json.dumps({'status':'SUPPLEMENTAL_BINDINGS_PASS','actual_pid':os.getpid(),'exact_committed_artifacts_and_inputs':len(committed),'overlay_RAW_LF_pairs':18,'current_formula_texts':12,'only_changed_Lean_files':len(changed)}))
if __name__=='__main__':main()
