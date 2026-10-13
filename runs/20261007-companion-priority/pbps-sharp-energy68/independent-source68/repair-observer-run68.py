from pathlib import Path
import json,hashlib,os,subprocess,sys,datetime
O=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-sharp-energy68/independent-source68')
s=(O/'validate-final-inputs68.v1.executed-RAW.py').read_text(encoding='utf-8-sig')
s=s.replace("for e in receipt['inputs']:\n p=Path(e['path']);b=p.read_bytes();assert len(b)==e['bytes'] and sha(b)==e['raw_sha256']", """compiler_rows=[];cell_maps=[]
def diff(a,b,p=''):
 if type(a)!=type(b):return [{'pointer':p,'before':a,'after':b}]
 if isinstance(a,dict):
  z=[]
  for k in sorted(set(a)|set(b)):
   if k not in a or k not in b:z.append({'pointer':p+'/'+k,'before':a.get(k,'__ABSENT__'),'after':b.get(k,'__ABSENT__')})
   else:z.extend(diff(a[k],b[k],p+'/'+k))
  return z
 return [] if a==b else [{'pointer':p,'before':a,'after':b}]
allowed_cell_paths={str(R/'research-wiki/frontier-cells/ASTIS-SHARED-hilbert-corrector-square-bound.json'),str(R/'research-wiki/frontier-cells/ASTIS-SW-PBPS-sharp-corrector-energy.json')}
for e in receipt['inputs']:
 p=Path(e['path']);b=p.read_bytes();equal=len(b)==e['bytes'] and sha(b)==e['raw_sha256'];compiler_rows.append({'path':e['path'],'at_compile_RAW_sha256':e['raw_sha256'],'current_RAW_sha256':sha(b),'equal':equal})
 if not equal:
  assert str(p) in allowed_cell_paths
  snap=next(x['exact_raw_snapshot'] for x in receipt['input_snapshots'] if x['original']['path']==e['path']);before=Path(snap['path']).read_bytes();assert sha(before)==e['raw_sha256'];changes=diff(json.loads(before),json.loads(b));cell_maps.append({'path':p.relative_to(R).as_posix(),'at_compile_RAW_sha256':sha(before),'current_RAW_sha256':sha(b),'exact_before_snapshot':snap['path'],'changes':changes,'meaning':'Post-compile focused-check/source-cell/ownership metadata enrichment, not Lean/source-statement change.'})
assert len(cell_maps)==2 and sum(x['equal'] for x in compiler_rows)==9
write('compiler-current-two-cell-maps.json',{'status':'EXACT_NINE_MATCHING_INPUTS_AND_TWO_FINITE_POSTCOMPILE_CELL_MAPS','actual_pid':os.getpid(),'rows':compiler_rows,'cell_maps':cell_maps,'source_Lean_toolchain_and_dependencies_unchanged':True,'broad_exclusions':False})""")
s=s.replace("'all11_compiler_input_current_RAW_pins_equal':True", "'all11_compiler_input_current_RAW_pins_equal':False,'matching_current_RAW_inputs':9,'exact_two_current_cell_metadata_maps':'compiler-current-two-cell-maps.json','all3_final_Lean_plus_fixed_toolchain_manifest_RAW_pins_equal':True")
(O/'validate-final-inputs68.v2.py').write_text(s,encoding='utf8',newline='\n')
for n in ['packet-bindings-and-context.readback.json','eleven-literal-BODY-spans.readback.json','blind-native-input-provenance.readback.json']:
 p=O/n
 if p.exists():(O/(n+'.v1.before-observer-fix')).write_bytes(p.read_bytes())
(O/'negative.compiler-drift.actual-diagnosis.json').write_text(json.dumps({'kind':'OBSERVER_ALL11_EQUAL_ASSERTION_TOO_STRONG','diagnosis_actual_pid':os.getpid(),'original_failure_tool_chunk':'eabf1d','original_tool_exit':1,'actual_drift':'Exactly two frontier-cell metadata files were enriched after compile; all3 Lean files and fixed toolchain/dependency manifest are RAW-identical. This is distinct from V2 lesson overlay.','resolution':'Explicit finite before/current maps; retain old compiler snapshots. Never claim all11 current pins equal.','source_fidelity_not_derived_from_control_plane_metadata':True},indent=2)+'\n',encoding='utf8',newline='\n')
a=[sys.executable,'-X','utf8',str(O/'validate-final-inputs68.v2.py')];p=subprocess.Popen(a,cwd='E:/Samplinglib',stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate();(O/'validation68.v2.stdout.RAW.txt').write_bytes(out);(O/'validation68.v2.stderr.RAW.txt').write_bytes(err);(O/'validation68.v2.terminal.json').write_text(json.dumps({'foreground':True,'detached':False,'wrapper_actual_pid':os.getpid(),'actual_child_pid':p.pid,'actual_exit_code':p.returncode,'command':a,'stdout_raw_sha256':hashlib.sha256(out).hexdigest(),'stderr_raw_sha256':hashlib.sha256(err).hexdigest(),'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2)+'\n',encoding='utf8',newline='\n');print(out.decode('utf8'));print(err.decode('utf8'));sys.exit(p.returncode)
