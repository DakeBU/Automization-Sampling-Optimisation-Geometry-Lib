from pathlib import Path
import ctypes,datetime,hashlib,json,os,re,subprocess,sys
ROOT=Path('E:/Samplinglib');PRE=ROOT/'runs/20261007-companion-priority/pbps-clock-preproof75';OWN=PRE/'independent-header-math75';PLAN=ROOT/'runs/20261007-companion-priority/pbps-clock-construction-preread75'
ACTOR='/root/header_math72';PY=Path('C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe');ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1');sys.dont_write_bytecode=True
sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda j:json.dumps(j,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf8');load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_bytes=len(lf),LF_sha256=sha(lf))
def check(z):
 b=Path(z['path']).read_bytes();lf=b.replace(b'\r\n',b'\n');assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'] and len(lf)==z['LF_bytes'] and sha(lf)==z['LF_sha256'];return b
def save(n,j):
 assert not (OWN/'lease.final.json').exists();p=OWN/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(j,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf8',newline='\n')
def command(label,args,expected=0,env=None):
 d=OWN/'terminals';d.mkdir(parents=True,exist_ok=True);assert not (d/(label+'.receipt.json')).exists()
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.Popen([str(x) for x in args],cwd=ROOT,env=env or ENV,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 print(json.dumps(dict(START=label,PID=p.pid,driver_PID=os.getpid())),flush=True);out,err=p.communicate();(d/(label+'.stdout.RAW')).write_bytes(out);(d/(label+'.stderr.RAW')).write_bytes(err)
 rec=dict(label=label,actual_foreground_PID=p.pid,actual_driver_PID=os.getpid(),command=[str(x) for x in args],terminal_closed=True,terminal_EXIT=p.returncode,expected_EXIT=expected,started_UTC=start,finished_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),stdout=pin(d/(label+'.stdout.RAW')),stderr=pin(d/(label+'.stderr.RAW')));save('terminals/'+label+'.receipt.json',rec)
 print(json.dumps(dict(END=label,PID=p.pid,EXIT=p.returncode)),flush=True);assert p.returncode==expected,label;return out,rec
def prepare():
 assert not (OWN/'inputs.manifest.json').exists();proposal=load(PRE/'header75.proposal.json');h=PRE/'header75.proposed.lean';assert pin(h)['RAW_sha256']==proposal['RAW_sha256']=='05ffee849dcf32541a948c1e9539550f122db34274e69d5b64397003de914263'
 files=[h,PRE/'header75.proposal.json',ROOT/'lean-toolchain',ROOT/'lake-manifest.json',ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean',ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBounceRate.lean',PLAN/'selected.contract.json',PLAN/'named.source-first-dependency-audit75.md',PLAN/'decision.json',PLAN/'lease.final.json',ROOT/'.lake/packages/mathlib/Mathlib/Probability/Process/HittingTime.lean',ROOT/'.lake/packages/mathlib/Mathlib/Probability/Distributions/Exponential.lean',ROOT/'.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/DominatedConvergence.lean',ROOT/'.lake/packages/mathlib/Mathlib/MeasureTheory/Constructions/BorelSpace/Order.lean']
 rows=[];(OWN/'inputs').mkdir(parents=True,exist_ok=True)
 for i,p in enumerate(files):
  q=OWN/'inputs'/f'{i:02d}.exactRAW.snapshot';q.write_bytes(p.read_bytes());rows.append(dict(original=pin(p),snapshot=pin(q)))
 save('inputs.manifest.json',dict(input_count=len(rows),inputs=rows,actual_prepare_PID=os.getpid(),LF_recipe='CRLF byte pairs -> LF only; preserve every other byte.',primary_source_or_other_reviewer_evolving_packet_read=False))
 raw=h.read_bytes();old=b'ProbabilityTheory.expMeasure1';new='(ProbabilityTheory.expMeasure (1 : ℝ))'.encode('utf8');assert raw.count(old)==1
 repaired=raw.replace(old,new);v2=OWN/'header75.v2.minimal-overlay.proposed.lean';v2.write_bytes(repaired)
 save('minimal-overlay.proposal.json',dict(status='REVIEWER_PROPOSED_TYPE_REPAIR_ONLY_NOT_SOURCE_ACCEPTED',original=pin(h),proposed=pin(v2),occurrences=1,exact_old_UTF8=old.decode(),exact_new_UTF8=new.decode(),only_change='Replace nonexistent expMeasure1 constant with the existing expMeasure at real rate1; outer parentheses are required for the Measure.map argument.',new_callers=[],mathematical_definition_change=False,proof_search=False))
 for tag,b in [('original',raw),('v2',repaired)]:
  text=b.decode('utf8');ix=text.index('\ntheorem actual_integrated_hazard_clock_laws');predicate=text[:ix]+'\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHazardClock\n';(OWN/(tag+'.predicate-only.lean')).write_text(predicate,encoding='utf8',newline='\n')
  public=text[ix+1:];assert public.endswith(' := by\n');tel=public.removeprefix('theorem actual_integrated_hazard_clock_laws\n').removesuffix(' := by\n');sep=tel.rfind(' :\n');assert sep!=-1;forall=tel[:sep]+',\n'+tel[sep+3:];driver=text[:ix]+'\n#check (∀\n'+forall+')\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHazardClock\n';(OWN/(tag+'.full-telescope-type-only.lean')).write_text(driver,encoding='utf8',newline='\n')
 print(json.dumps(dict(status='PREPARED',PID=os.getpid(),input_count=len(rows),v2=pin(v2)),ensure_ascii=False))
def probes():
 envout,_=command('fixed-lake-env',['lake','env',PY,'-B','-X','utf8','-c',"import os,json;print(json.dumps({k:os.environ.get(k,'') for k in ['LEAN_PATH','LEAN_SRC_PATH']}))"]);prefix,_=command('fixed-lean-prefix',['lake','env','lean','--print-prefix']);exe=Path(prefix.decode().strip())/'bin/lean.exe';env=dict(ENV,**json.loads(envout))
 version,_=command('fixed-lean-version',[exe,'--version'],env=env);assert '4.33.0' in version.decode()
 neg,nrec=command('original-predicate-typecheck',[exe,OWN/'original.predicate-only.lean'],expected=1,env=env);assert 'expMeasure1' in neg.decode('utf8')
 _,vrec=command('v2-predicate-typecheck',[exe,OWN/'v2.predicate-only.lean'],env=env)
 _,trec=command('v2-full-telescope-typecheck',[exe,OWN/'v2.full-telescope-type-only.lean'],env=env)
 save('typecheck-summary.json',dict(status='ORIGINAL_TYPE_REPAIR_REQUIRED_V2_TYPECHECK_PASS_ONLY',actual_probe_driver_PID=os.getpid(),original_negative=nrec,v2_predicate=vrec,v2_full_telescope=trec,original_fixed_Lake_search_roots=True,LEAN_PATH=env['LEAN_PATH'],LEAN_SRC_PATH=env['LEAN_SRC_PATH'],Lean_executable=pin(exe),no_theorem_BODY_or_proof_implementation=True,no_theorem_proved=True))

def structural():
 original=(OWN/'inputs/00.exactRAW.snapshot').read_bytes();v2=(OWN/'header75.v2.minimal-overlay.proposed.lean').read_bytes();old=b'ProbabilityTheory.expMeasure1';new='(ProbabilityTheory.expMeasure (1 : ℝ))'.encode();assert original.count(old)==1 and v2==original.replace(old,new)
 text=v2.decode();private=text[text.index('private def '):text.index('\ntheorem ')];public=text[text.index('\ntheorem ')+1:]
 pb=private[private.index('    {E :'):private.index(' : Prop :=')];tb=public[public.index('    {E :'):public.rindex(' :\n')];assert pb==tb
 callers=re.findall(r'\((h[^ :]+)\s*:',pb);assert callers==['hα','hαβ','hV','hH','hη','hβη'];assert public.endswith('actual_integrated_hazard_clock_statement hα hαβ hV hH hη hβη := by\n')
 flat=lambda t:' '.join(t.split())
 def local(src,name):
  start=src.index('    let '+name+' :');end=re.search(r'\n    (?:let |Continuous |Measurable )',src[start+1:]);assert end;return src[start:start+1+end.start()]
 p73=(OWN/'inputs/04.exactRAW.snapshot').read_text(encoding='utf8');p74=(OWN/'inputs/05.exactRAW.snapshot').read_text(encoding='utf8')
 for name in ['c','Φ','H']:assert flat(local(private,name))==flat(local(p73,name))
 for name in ['c','H']:assert flat(local(private,name))==flat(local(p74,name))
 assert flat(local(private,'rate'))==flat(local(p74,'rate').replace('(h xRef z.1)','(gradient V z.1 - gradient V xRef)'))
 cap=local(private,'C').split('fun y xRef z =>\n',1)[1];oldcap=p74[p74.index('        rate xRef z ≤ '):p74.index('\ntheorem ')].split('        rate xRef z ≤ ',1)[1].rstrip().removesuffix(')');assert flat(cap)==flat(oldcap.replace('z₀','z'))
 conclusion=private[private.index('\n    Continuous ')+1:];depth=0;chunks=[];start=0
 for i,c in enumerate(conclusion):
  if c in '([{':depth+=1
  elif c in ')]}':depth-=1;assert depth>=0
  elif c=='∧' and depth==0:chunks.append(conclusion[start:i].strip());start=i+1
 assert depth==0;chunks.append(conclusion[start:].strip());assert len(chunks)==10
 assert not re.search(r'\b(?:axiom|sorry|admit)\b|Prop\s*:=\s*True|:=\s*trivial',text)
 report=dict(status='PASS_EXACT_SINGLE_EXPRESSION_OVERLAY_AND_FULL_TELESCOPE',actual_foreground_PID=os.getpid(),original=pin(OWN/'inputs/00.exactRAW.snapshot'),v2=pin(OWN/'header75.v2.minimal-overlay.proposed.lean'),only_expression_replacement=dict(old=old.decode(),new=new.decode(),occurrences=1),private_public_binders_exactly_identical=True,full_binder_UTF8=pb,original_named_analytic_callers=callers,new_analytic_callers=[],same_parent73_c_Phi_H=True,same_parent74_c_rate_expanding_h_H_and_cap=True,conclusion_group_count=len(chunks),full_conclusion_groups_UTF8=chunks,fake_mathematical_closure_markers=0,full_candidate_has_unimplemented_by_stub=True,proof_search=False,no_EXCESS_new_premises=True,standing_callers_retained_even_if_unneeded=['hα','hαβ','hβη'])
 print(json.dumps(report,ensure_ascii=False))

def audit():
 out,rec=command('exact-header-structural-audit',[PY,'-B','-X','utf8',OWN/'math75.py','structural']);report=json.loads(out);assert report['status'].startswith('PASS_');save('binder-definition-audit.json',dict(audit=report,actual_terminal_receipt=rec))

def close():
 assert not (OWN/'lease.final.json').exists();im=load(OWN/'inputs.manifest.json');tc=load(OWN/'typecheck-summary.json');ba=load(OWN/'binder-definition-audit.json');ov=load(OWN/'minimal-overlay.proposal.json');review=(OWN/'named.prospective-header-mathematics75.md').read_text(encoding='utf8')
 for row in im['inputs']:assert check(row['original'])==check(row['snapshot'])
 assert tc['original_negative']['terminal_EXIT']==1 and tc['v2_predicate']['terminal_EXIT']==tc['v2_full_telescope']['terminal_EXIT']==0
 assert ba['actual_terminal_receipt']['terminal_EXIT']==0 and ba['audit']['conclusion_group_count']==10
 decision=dict(status='ACCEPT_V2_PROSPECTIVE_MATHEMATICAL_TYPE_CONTRACT_ONLY',actor=ACTOR,independent_of_root_canonical_writer=True,checked_proposal_parent=load(OWN/'inputs/01.exactRAW.snapshot')['head'],original_header=ov['original'],proposed_v2_header=ov['proposed'],original_type_status='REPAIR_REQUIRED_UNKNOWN_expMeasure1',ten_conclusion_groups_mathematically_correct_after_exact_repair=True,minimum_concrete_repair=[ov['exact_old_UTF8']+' -> '+ov['exact_new_UTF8']],further_mathematical_repair=[],original_six_callers_preserved=True,new_callers=[],no_EXCESS_new_premises=True,no_assumed_clock_law=True,actual_Exp1_first_clock_measure_not_terminal_kernel=True,continuous_time_NNReal_hittingAfter=True,top_allowed=True,e_zero_allowed=True,zero_energy_allowed=True,rank_zero_allowed=True,alpha_eta_one_allowed=True,almost_sure_finite_wait_assumed=False,definition_scalar_sign_and_product_orientation_audit='PASS',typecheck_only=True,actual_theorem_BODY_proved=False,full_candidate_compiled=False,proof_search=False,new_SAU=False,VERIFIED=False,source_final_acceptance=False,repair_source_accepted=False,reader_acceptance=False,PURIFIED=False,full_Exposition_Seal=False,Goal_complete=False,requires_distinct_source_review_and_root_adoption_before_seal=True,requires_parent74_admission_integration_before75_claim=True,remaining_boundaries=['recursive random path and state/time measurability','common-cap induction across actual jumps','iid exponential clock construction and summation/nonexplosion','Markov property and memorylessness','stochastic invariance','actual terminal kernels','expected costs','Proposition3.1/full paper/composition/Goal'],negative_evidence_preserved=['Original predicate Lean17592 EXIT1, unknown ProbabilityTheory.expMeasure1; exact stdout retained.'],tooling_lookup_clarification='Exact metadata filename is header75.proposal.json, not absent proposal.json; initial lookup gave a nonterminating PowerShell path error, no capture of its shell PID, no mathematical or canonical mutation.',actual_original_negative_PID=tc['original_negative']['actual_foreground_PID'],actual_v2_predicate_PID=tc['v2_predicate']['actual_foreground_PID'],actual_v2_telescope_PID=tc['v2_full_telescope']['actual_foreground_PID'])
 save('decision.json',decision)
 payload=dict(name='Complete independent prospective-header mathematics75 RAW payload',actor=ACTOR,decision=decision,input_manifest=im,exact_original_header_UTF8=check(ov['original']).decode('utf8'),exact_v2_header_UTF8=check(ov['proposed']).decode('utf8'),exact_minimal_overlay_proposal=ov,full_binder_and_definition_audit=ba,rigorous_named_review_UTF8=review,actual_typecheck_receipts=tc,source_acceptance=False,actual_theorem_proof=False)
 save('complete.named.RAW.payload75.json',payload)
 run=dict(name='Independent prospective-header mathematics75',actor=ACTOR,status=decision['status'],checked_proposal_parent=decision['checked_proposal_parent'],decision=decision,decision_file=pin(OWN/'decision.json'),input_manifest=im,inputs_manifest=pin(OWN/'inputs.manifest.json'),complete_named=pin(OWN/'complete.named.RAW.payload75.json'),named_review=pin(OWN/'named.prospective-header-mathematics75.md'),minimal_overlay_proposal=pin(OWN/'minimal-overlay.proposal.json'),binder_definition_audit=pin(OWN/'binder-definition-audit.json'),typecheck_summary=pin(OWN/'typecheck-summary.json'),wholelogical_recipe='sha256 UTF8 JSON sorted keys compact separators ensure_ascii=False allow_nan=False; remove ONLY top-level run_sha256',actual_close_writer_PID=os.getpid(),VERIFIED=False,proof_search=False)
 run['run_sha256']=sha(can(run));save('run.json',run)
 rows=[pin(p) for p in sorted(OWN.rglob('*')) if p.is_file() and p.name not in ['native.manifest.json','lease.final.json']];m=dict(entries=rows,entry_count=len(rows),logical_entries_sha256=sha(can(rows)),RAW_pin_recipe='Exact bytes.',LF_pin_recipe='Replace CRLF byte pairs only; retain every other byte.');save('native.manifest.json',m)
 lease=dict(status='CLOSED_LAST',actor=ACTOR,reviewer=ACTOR,VERIFIED=False,manifest=pin(OWN/'native.manifest.json'),owned_files=len(rows)+2,file_count_including_lease=len(rows)+2,closure_logical_sha256=m['logical_entries_sha256'],run_sha256=run['run_sha256'],writer_PID=os.getpid(),writer_terminal_EXIT_expected=0,postclose_owned_writes_forbidden=True,final_owned_write=True,closed_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat());save('lease.final.json',lease)
 print(json.dumps(dict(status='CLOSED_LAST',actual_writer_PID=os.getpid(),writer_terminal_EXIT_expected=0,owned_files=len(rows)+2,run_sha256=run['run_sha256'],lease=pin(OWN/'lease.final.json'),complete_named=run['complete_named'],v2=ov['proposed']),ensure_ascii=False),flush=True)
def readonly():
 lp=OWN/'lease.final.json';l=load(lp);assert l['status']=='CLOSED_LAST' and l['actor']==ACTOR and not l['VERIFIED'];m=load(OWN/'native.manifest.json');check(l['manifest']);rows=m['entries'];assert len(rows)==m['entry_count'] and len(rows)+2==l['owned_files'] and sha(can(rows))==m['logical_entries_sha256']
 assert {p.resolve() for p in OWN.rglob('*') if p.is_file()}=={Path(z['path']).resolve() for z in rows}|{lp.resolve(),(OWN/'native.manifest.json').resolve()}
 for z in rows:check(z);assert Path(z['path']).stat().st_mtime_ns<=lp.stat().st_mtime_ns
 run=load(OWN/'run.json');assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==l['run_sha256'];check(run['complete_named']);p=load(run['complete_named']['path']);assert p['decision']==run['decision'] and p['input_manifest']==run['input_manifest']
 for z in run['input_manifest']['inputs']:assert check(z['original'])==check(z['snapshot'])
 k=ctypes.WinDLL('kernel32',use_last_error=True);k.OpenProcess.restype=ctypes.c_void_p;handle=k.OpenProcess(0x00100000,False,l['writer_PID'])
 if handle:
  k.WaitForSingleObject.argtypes=[ctypes.c_void_p,ctypes.c_ulong];k.CloseHandle.argtypes=[ctypes.c_void_p];assert k.WaitForSingleObject(handle,0)==0;k.CloseHandle(handle)
 else:assert ctypes.get_last_error()==87
 print(json.dumps(dict(status='PASS',external_readonly_PID=os.getpid(),writer_PID=l['writer_PID'],writer_terminated=True,owned_files=l['owned_files'],inputs=run['input_manifest']['input_count'],run_sha256=run['run_sha256'],no_owned_writes=True,VERIFIED=False,terminal_EXIT_contract=0)))
if __name__=='__main__':{'prepare':prepare,'probes':probes,'structural':structural,'audit':audit,'close':close,'readonly':readonly}[sys.argv[1]]()
