from pathlib import Path
import json,os,hashlib,subprocess,sys,datetime
O=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-sharp-energy68/independent-source68');s=(O/'validate-final-inputs68.v2.py').read_text(encoding='utf8');old="stdout=Path(receipt['stdout']['path']).read_text();assert '3950' in stdout;axioms=[x for x in stdout.splitlines() if 'depends on axioms' in x];assert len(axioms)==3;assert all('propext, Classical.choice, Quot.sound' in x for x in axioms)"
new="""stdout=Path(receipt['stdout']['path']).read_text();assert '3950' in stdout
all_axiom_matches=re.findall(r\"'([^']+)' depends on axioms:\\s*\\[([^\\]]*)\\]\",stdout,re.S)
targets=[p['lean']['declaration'] for p in packets];axioms=[]
for name in targets:
 reports=[a for n,a in all_axiom_matches if n==name];assert reports
 parsed=[[v.strip() for v in a.split(',')] for a in reports];assert all(set(a)=={'propext','Classical.choice','Quot.sound'} for a in parsed)
 axioms.append({'declaration':name,'all_targeted_occurrences':len(reports),'axioms':parsed[0]})
assert len(axioms)==3"""
assert old in s;s=s.replace(old,new);(O/'validate-final-inputs68.v3.py').write_text(s,encoding='utf8',newline='\n')
(O/'negative.compiler-axiom-output-shape-v2.json').write_text(json.dumps({'kind':'OBSERVER_AXIOM_REPORT_COUNT_AND_LINE_SHAPE_WRONG','actual_diagnosis_pid':os.getpid(),'actual_failed_run_receipt':'validation68.v2.terminal.json','error':'Observer assumed total stdout had exactly3 single-line axiom reports. Full Lake log includes ancestor reports and producer/Test repeats; each targeted report is multiline.','resolution':'Parse complete bracketed multiline reports; select exact three current declaration names; require every occurrence of each to have precisely propext/Classical.choice/Quot.sound. Retain duplicates and full RAW stdout.','Lean_or_source_defect':False},indent=2)+'\n',encoding='utf8',newline='\n')
a=[sys.executable,'-X','utf8',str(O/'validate-final-inputs68.v3.py')];p=subprocess.Popen(a,cwd='E:/Samplinglib',stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate();(O/'validation68.v3.stdout.RAW.txt').write_bytes(out);(O/'validation68.v3.stderr.RAW.txt').write_bytes(err);(O/'validation68.v3.terminal.json').write_text(json.dumps({'foreground':True,'detached':False,'wrapper_actual_pid':os.getpid(),'actual_child_pid':p.pid,'actual_exit_code':p.returncode,'command':a,'stdout_raw_sha256':hashlib.sha256(out).hexdigest(),'stderr_raw_sha256':hashlib.sha256(err).hexdigest(),'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2)+'\n',encoding='utf8',newline='\n');print(out.decode('utf8'));print(err.decode('utf8'));sys.exit(p.returncode)
