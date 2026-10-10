import json,os,sys
sys.dont_write_bytecode=True
from pathlib import Path
from review76 import OWN,HEADER,EXPECTED,NS,SPEC,PUBLIC,ENV,sha,pin,check,save,load,command
assert not (OWN/'lease.final.json').exists()
original=HEADER.read_bytes();assert sha(original)==EXPECTED
repairs=[
 ('((τ y xRef a.2 e).untopD 0 : ℝ)','(((τ y xRef a.2 e).untopD 0 : ℝ≥0) : ℝ)'),
 ('((τ y xRef a.2 (e n)).untopD 0 : ℝ)','(((τ y xRef a.2 (e n)).untopD 0 : ℝ≥0) : ℝ)')]
v3=original.decode()
for before,after in repairs:assert v3.count(before)==1;v3=v3.replace(before,after)
path=OWN/'header76.v3.proposed.lean';assert not path.exists();path.write_bytes(v3.encode())
start=v3.index('\ntheorem '+PUBLIC)+1;prefix=v3[:start];tail=v3[start:];assert tail.endswith(' := by\n')
pred=prefix+'\n#check @'+SPEC+'\n\nend\nend '+NS+'\n'
args,result=tail[len('theorem '+PUBLIC):].rsplit(' :\n',1);result=result[:-len(' := by\n')]
pub=prefix+'\n-- TYPE ONLY: the exact proposed public telescope as a proposition, with no proof.\ndef independent_public_telescope_TYPEONLY : Prop :=\n  ∀'+args+',\n'+result+'\n\n#print independent_public_telescope_TYPEONLY\n#check WithTop.measurable_untopD\n#check Measurable.sumElim\n#check measurable_fun_sum\n#check measurable_pi_apply\n#check Measurable.ite\n\nend\nend '+NS+'\n'
dp=OWN/'header76.v3.predicate.TYPEONLY.lean';du=OWN/'header76.v3.public-telescope.TYPEONLY.lean';dp.write_bytes(pred.encode());du.write_bytes(pub.encode())
save('exact-minimal-type-overlay.v3.proposal.json',dict(status='INDEPENDENT_MINIMAL_TYPE_REPAIR_PROPOSAL_NOT_ROOT_ADOPTED_NOT_SOURCE_ACCEPTED',original_header=pin(HEADER),proposed_header=pin(path),exact_replacements=[dict(before=b,after=a,occurrences=1) for b,a in repairs],original_lines=[53,68],mathematical_semantics_changed=False,public_binders_changed=False,reason='An inner NNReal ascription fixes the type of the complete untopD result before outer coercion to Real; annotating only the zero default is insufficient because Lean coerces that default under the outer expected type.',original_negative_typechecks=pin(OWN/'typechecks.json'),insufficient_v2_negative_typechecks=pin(OWN/'typechecks.v2.json'),full_target_proof=False,VERIFIED=False,actual_writer_PID=os.getpid()))
config=load(OWN/'typechecks.json');exe=Path(config['real_Lean_executable']['path']);check(config['real_Lean_executable']);env=dict(ENV,LEAN_PATH=config['LEAN_PATH'],LEAN_SRC_PATH=config['LEAN_SRC_PATH']);results=[]
for name,driver in [('predicate',dp),('public-telescope',du)]:
 _,rec=command('fresh-v3-'+name+'-TYPEONLY',[exe,driver],env);results.append(dict(kind=name,driver=pin(driver),receipt=pin(OWN/'terminals'/('fresh-v3-'+name+'-TYPEONLY.receipt.json')),PID=rec['actual_foreground_PID'],terminal_EXIT=rec['terminal_EXIT']))
status='PASS' if all(z['terminal_EXIT']==0 for z in results) else 'FAIL_TYPE_CONTRACT'
save('typechecks.v3.json',dict(status=status,results=results,fresh_direct_type_elaboration=True,Lake_build_cache_replay=False,full_target_proof=False,real_Lean_executable=config['real_Lean_executable'],LEAN_PATH=config['LEAN_PATH'],LEAN_SRC_PATH=config['LEAN_SRC_PATH'],no_canonical_output_written=True,driver_PID=os.getpid(),original_and_v2_failures_preserved=True,only_two_inner_type_annotations=True,proposed_header=pin(path)))
print(json.dumps(dict(status=status,PID=os.getpid(),proposed_header=pin(path),results=results)),flush=True)
if status!='PASS':sys.exit(1)
