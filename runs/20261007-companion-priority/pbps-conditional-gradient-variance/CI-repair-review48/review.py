import json,hashlib,subprocess,datetime,sys,os
from pathlib import Path
r=Path('E:/Samplinglib');run=r/'runs/20261007-companion-priority/pbps-conditional-gradient-variance';repairdir=run/'site-ci-cardinality-repair48';out=run/'CI-repair-review48';commit='79efd28ca8827742e690529f8c763a7bce9b054a';testpath='tools/tests/test_samplewiki_companions.py';os.environ['PYTHONUTF8']='1'
def H(b):return hashlib.sha256(b).hexdigest()
def LF(b):return b.replace(b'\r\n',b'\n')
def bind(p):
 p=Path(p);b=p.read_bytes();return {'path':str(p.relative_to(r)).replace('\\','/'),'bytes':len(b),'raw_sha256':H(b),'lf_sha256':H(LF(b)),'CRLF_count':b.count(b'\r\n'),'lone_CR_count':b.replace(b'\r\n',b'').count(b'\r')}
def read(p):return json.loads(Path(p).read_text('utf-8'))
def dump(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n','utf-8')
def git(*args):return subprocess.check_output(['git',*args],cwd=r)
assert read(out/'reviewer.ci.lease.json')['status']=='OPEN'
assert git('rev-parse','HEAD').decode().strip()==commit
assert git('diff','--name-only').decode().splitlines()==[testpath]
assert not git('diff','--cached','--name-only').strip()
repair=read(repairdir/'repair.json');before=(repairdir/'test.before.raw.snapshot.py').read_bytes();after=(r/testpath).read_bytes();oldgit=git('show',commit+':'+testpath)
assert H(before)==repair['before_raw_sha256'] and H(after)==repair['after_raw_sha256'];assert oldgit in (before,LF(before))
original=LF(before).decode('utf-8');expected=original
replacements=[('test_three_sources_keep_the_two_paper_composition_separate','test_four_sources_keep_the_two_paper_composition_separate'),("self.assertEqual(len(m['sources']),3)","self.assertEqual(len(m['sources']),4)"),("self.assertEqual(len(m['cases']),3)","self.assertEqual(len(m['cases']),4)"),("{'source_cases':3,'composition_views':1,'technology_candidates':12}","{'source_cases':4,'composition_views':1,'technology_candidates':12}"),('self.assertEqual(len(b.nodes),19)','self.assertEqual(len(b.nodes),20)')]
for a,b in replacements:assert expected.count(a)==1;expected=expected.replace(a,b)
newlines="        midpoint=next(row for row in m['cases'] if row['id']=='ASTIS-SW-MIDPOINT-2026')\n        self.assertEqual(midpoint['source_ids'],['midpoint-2026'])\n        self.assertEqual(midpoint['status'],'planned')\n        self.assertEqual(m['sources']['midpoint-2026']['version'],'2610.06308v1')\n"
anchor="        snapshot=json.loads((ROOT/'research-wiki/source-index/SampleWiki_cases.json').read_text(encoding='utf8'))\n";assert expected.count(anchor)==1;expected=expected.replace(anchor,newlines+anchor)
assert expected.encode()==LF(after),'additional changes beyond five replacements/fourlines'
# Bind real producer gate receipts unchanged; their schema lacks timestamps/root lease, no synthetic chronology.
producer=[]
for stem,check in zip(['focused','ci-contract-suite','formalization-ci-discover','whitespace'],repair['checks']):
 s=read(repairdir/(stem+'.status.json'));assert s==check and s['exit_code']==0;log=repairdir/(stem+'.log');assert H(log.read_bytes())==s['log_raw_sha256'];producer.append({'status':bind(repairdir/(stem+'.status.json')),'log':bind(log),'actual_status':s})
assert 'Ran 12 tests' in (repairdir/'focused.log').read_text('utf-8')
assert 'Ran 224 tests' in (repairdir/'ci-contract-suite.log').read_text('utf-8')
assert 'Ran 296 tests' in (repairdir/'formalization-ci-discover.log').read_text('utf-8')
for stem in ['focused','ci-contract-suite','formalization-ci-discover']:assert '\nOK' in (repairdir/(stem+'.log')).read_text('utf-8')
ci=read(run/'repository-seal48/CI79.negative.json');negative=[]
for item,stem in zip(ci['failures'],['original.ci79-site.failed.log','original.ci79-lean.failed.log']):
 p=repairdir/stem;d=bind(p);assert d['raw_sha256']==item['actual_failed_log']['raw_sha256'];assert p.read_bytes()==(r/item['actual_failed_log']['path']).read_bytes();negative.append(d)
# Original scientific/admin79 inputs, sealed raw/log/parent artifacts remain untouched.
proof=read(run/'repository-seal48/bindings.json');sealed=[]
for x in proof['Git_rawLF_checks']+proof['root12_gate_bindings']+proof['shared_currentGit_rawLF']:
 d=bind(r/x['path']);assert all(d[k]==x[k]for k in ['raw_sha256','lf_sha256','bytes']);sealed.append(d)
originalseals=[]
for folder in ['repository-seal48','exposition-seal48']:
 rr=read(run/folder/'run.json')
 for x in rr['outputs']:
  d=bind(r/x['path']);assert all(d[k]==x[k]for k in ['raw_sha256','lf_sha256','bytes']);originalseals.append(d)
 assert read(run/folder/'reviewer.seal.lease.json')['status']=='CLOSED'
# One independent meaningful focused suite and scoped whitespace check; own real process chronology.
fresh=[]
for i,c in enumerate([[sys.executable,'-m','unittest','tools.tests.test_samplewiki_companions'],['git','-c','core.whitespace=cr-at-eol','diff','--check','--',testpath]]):
 started=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.Popen(c,cwd=r,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);PID=p.pid;data,_=p.communicate();log=out/f'check.{i}.log';log.write_bytes(data);s={'command':c,'process_id':PID,'foreground_process':True,'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':p.returncode,'log':bind(log)};dump(out/f'check.{i}.status.json',s);fresh.append(s);print('independent',i,p.returncode,flush=True)
assert all(x['exit_code']==0 for x in fresh)
result={'base_commit':commit,'working_candidate_uncommitted_Test_py':bind(r/testpath),'base_before_snapshot':bind(repairdir/'test.before.raw.snapshot.py'),'baseGit_blob_sha256':H(oldgit),'logical_LF_delta':'EXACT_FIVE_COUNT_OR_NAME_REPLACEMENTS_PLUS_FOUR_MIDPOINT_PLANNED_FIXEDV1_LINES','five_replacements':replacements,'four_inserted_lines':newlines,'source_semantics':'Existing two-paper composition source_ids remains exactly PBPS/SPHMC; original34SampleWiki case snapshot/activecase assertions, technology12 and compositionview1 retained. No compiled nodes or formal imports/declares/depends-on/closes-leaf edges in source plan. Tests remain source/graph-contract checks, not mathematics.','root_actual4checks':producer,'root_process_provenance':'Parent reports actual foreground71931 exit0; actual receipts contain only command/exit/logsha, no timestamps or separate root Python repair lease. Review does not invent missing chronology/lease. Repair UTC is after all checks.','originalCI79_negatives_unchanged':negative,'sealed79science_gate_rawLF_inputs_unchanged_count':len(sealed),'original79seal_outputs_unchanged_count':len(originalseals),'independent_fresh_checks':fresh,'compiler':'NOT_STARTED_CLOSED','no_canonical_or_site_or_originalseal_mutations_by_reviewer':True,'no_newVERIFIED':True,'remoteCI':'OPEN_FOR_FUTURE_REPAIR_COMMIT; exact79 original remote failures remain unchanged; no new remotePASS or LeanBuildFailure inference','remaining':'Commit and push reviewed Python-only candidate, obtain actual fresh remote CI, no main/live/PURIFIED/fullreader/four-paper Goal closure.'}
dump(out/'bindings.json',result);print(json.dumps({'base':commit,'accepted_delta':'fiveplusfour','root_actual_tests':[12,224,296],'independent':[x['exit_code']for x in fresh],'unchanged79pins':len(sealed),'originalsealoutputs':len(originalseals),'compiler':'NOT_STARTED_CLOSED'}))
