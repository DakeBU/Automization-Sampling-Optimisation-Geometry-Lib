import json,os,sys
sys.dont_write_bytecode=True
from pathlib import Path
from review76 import OWN,HEADER,EXPECTED,NS,SPEC,PUBLIC,ENV,sha,pin,check,save,load,command

assert not (OWN/'lease.final.json').exists()
original=HEADER.read_bytes();assert sha(original)==EXPECTED
old=b'untopD 0 : '+ '\u211d'.encode('utf8')+b')'
new=b'untopD (0 : '+ '\u211d\u22650'.encode('utf8')+b') : '+ '\u211d'.encode('utf8')+b')'
assert original.count(old)==2
v2=original.replace(old,new);path=OWN/'header76.v2.proposed.lean';assert not path.exists();path.write_bytes(v2)
source=v2.decode();start=source.index('\ntheorem '+PUBLIC)+1;prefix=source[:start];tail=source[start:];assert tail.endswith(' := by\n')
pred=prefix+'\n#check @'+SPEC+'\n\nend\nend '+NS+'\n'
args,result=tail[len('theorem '+PUBLIC):].rsplit(' :\n',1);result=result[:-len(' := by\n')]
pub=prefix+'\n-- TYPE ONLY: the exact proposed public telescope as a proposition, with no proof.\ndef independent_public_telescope_TYPEONLY : Prop :=\n  \u2200'+args+',\n'+result+'\n\n#print independent_public_telescope_TYPEONLY\n#check WithTop.measurable_untopD\n#check Measurable.sumElim\n#check measurable_fun_sum\n#check measurable_pi_apply\n#check Measurable.ite\n\nend\nend '+NS+'\n'
dp=OWN/'header76.v2.predicate.TYPEONLY.lean';du=OWN/'header76.v2.public-telescope.TYPEONLY.lean';dp.write_bytes(pred.encode());du.write_bytes(pub.encode())
save('exact-minimal-type-overlay.proposal.json',dict(status='INDEPENDENT_MINIMAL_TYPE_REPAIR_PROPOSAL_NOT_ROOT_ADOPTED_NOT_SOURCE_ACCEPTED',original_header=pin(HEADER),proposed_header=pin(path),replacement_RAW_UTF8_before=old.decode(),replacement_RAW_UTF8_after=new.decode(),exact_occurrences=2,original_lines=[53,68],mathematical_semantics_changed=False,public_binders_changed=False,definitions_changed='Only default-value type annotations at the two finite NNReal-to-Real coercion sites; no function/formula changed.',reason='Expected-type elaboration of outer real ascription inferred WithTop Real for untopD; annotate the existing zero default as NNReal before the coercion.',original_negative_typechecks=pin(OWN/'typechecks.json'),full_target_proof=False,VERIFIED=False,actual_writer_PID=os.getpid()))
config=load(OWN/'typechecks.json');exe=Path(config['real_Lean_executable']['path']);check(config['real_Lean_executable']);env=dict(ENV,LEAN_PATH=config['LEAN_PATH'],LEAN_SRC_PATH=config['LEAN_SRC_PATH']);results=[]
for name,driver in [('predicate',dp),('public-telescope',du)]:
 _,rec=command('fresh-v2-'+name+'-TYPEONLY',[exe,driver],env);results.append(dict(kind=name,driver=pin(driver),receipt=pin(OWN/'terminals'/('fresh-v2-'+name+'-TYPEONLY.receipt.json')),PID=rec['actual_foreground_PID'],terminal_EXIT=rec['terminal_EXIT']))
status='PASS' if all(z['terminal_EXIT']==0 for z in results) else 'FAIL_TYPE_CONTRACT'
save('typechecks.v2.json',dict(status=status,results=results,fresh_direct_type_elaboration=True,Lake_build_cache_replay=False,full_target_proof=False,real_Lean_executable=config['real_Lean_executable'],LEAN_PATH=config['LEAN_PATH'],LEAN_SRC_PATH=config['LEAN_SRC_PATH'],no_canonical_output_written=True,driver_PID=os.getpid(),original_failure_preserved=True,only_two_default_value_type_annotations=True,proposed_header=pin(path)))
print(json.dumps(dict(status=status,PID=os.getpid(),proposed_header=pin(path),results=results)),flush=True)
if status!='PASS':sys.exit(1)
