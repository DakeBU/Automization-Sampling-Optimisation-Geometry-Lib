import json,hashlib,gzip,re,subprocess,datetime
from pathlib import Path
r=Path('E:/Samplinglib');run=r/'runs/20261007-companion-priority/pbps-conditional-gradient-variance';q=run/'site-ci-cardinality-repair48';out=run/'CI-repair-review48';base='79efd28ca8827742e690529f8c763a7bce9b054a'
def H(b):return hashlib.sha256(b).hexdigest()
def LF(b):return b.replace(b'\r\n',b'\n')
def bind(p):
 p=Path(p);b=p.read_bytes();return {'path':str(p.relative_to(r)).replace('\\','/'),'bytes':len(b),'raw_sha256':H(b),'lf_sha256':H(LF(b))}
def read(p):return json.loads(Path(p).read_text('utf-8'))
def dump(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n','utf-8')
def git(*args):return subprocess.check_output(['git',*args],cwd=r)
assert read(out/'reviewer.ci.whitespace.lease.json')['status']=='OPEN';assert git('rev-parse','HEAD').decode().strip()==base
assert bind(out/'review.json')['raw_sha256']=='27667e273a02c0396371d0a9d5eeba53d0a3fc0a221a83f3822986086d09f6dc'
assert bind(r/'tools/tests/test_samplewiki_companions.py')['raw_sha256']=='04c5683c4e1b057ee1a8080f10d897c642ff78480da8957c23912b1462cd539f'
diag=read(q/'staged.whitespace.diagnosis.json');excluded=[x['path']for x in diag['external_raw_logs']];expected=[str((q/n).relative_to(r)).replace('\\','/')for n in ['original.ci79-lean.failed.log','original.ci79-site.failed.log']];assert excluded==expected
assert diag['authored_check']['command']==['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check','--','.']+[':(exclude)'+x for x in expected]
rows=[]
for pin,name in zip(diag['external_raw_logs'],['ci79-lean.failed.log','ci79-site.failed.log']):
 p=r/pin['path'];b=p.read_bytes();assert H(b)==pin['raw_sha256'];assert b==(r/'.astis/pbps-gradient48'/name).read_bytes();assert git('show',':'+pin['path'])==b
 trailing=[i for i,line in enumerate(b.splitlines(),1)if line.endswith((b' ',b'\t'))];assert trailing==pin['trailing_space_rows']
 for i in trailing:assert re.fullmatch(rb'[^\t]+\t[^\t]+\t\d{4}-\d\d-\d\dT[0-9:.]+Z[ \t]+',b.splitlines()[i-1]),(name,i)
 rows.append({'rawLF_binding':bind(p),'actual_trailing_rows':trailing,'row_content_class':'Original GitHub timestamp/tab prefix followed only by blank-line trailing whitespace','staged_equals_raw_original':True})
assert [len(x['actual_trailing_rows'])for x in rows]==[24,5]
archive=read(q/'staged.whitespace.archive.json');raw=(r/archive['raw_local_only']).read_bytes();packed=(r/archive['gzip_path']).read_bytes();assert H(raw)==archive['raw_sha256'] and H(packed)==archive['gzip_sha256'];assert gzip.decompress(packed)==raw;assert int.from_bytes(packed[4:8],'little')==0 and not packed[3]&8
reported=re.findall(rb'^(.*):(\d+): trailing whitespace\.$',LF(raw),re.M);actualpairs=[(x['path'].encode(),str(i).encode())for x in diag['external_raw_logs']for i in x['trailing_space_rows']];assert reported==actualpairs
cached=git('diff','--cached','--name-only').decode().splitlines();assert 'tools/tests/test_samplewiki_companions.py' in cached
allowed=[str((run/x).relative_to(r)).replace('\\','/')+'/'for x in ['repository-seal48','exposition-seal48','CI-repair-review48','site-ci-cardinality-repair48']];assert all(p=='tools/tests/test_samplewiki_companions.py' or any(p.startswith(a)for a in allowed)for p in cached)
assert not any(p.endswith('staged.raw-ci-whitespace.negative.log')for p in cached)
# Fresh bounded staged check. Preserve newly generated negative losslessly as deterministic gzip, no new rawdiff transcript staging.
fresh=[]
for i,c in enumerate([diag['full_check']['command'],diag['authored_check']['command']]):
 started=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.Popen(c,cwd=r,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);pid=p.pid;data,_=p.communicate();expectedcode=2 if i==0 else 0;assert p.returncode==expectedcode
 if i==0:
  assert LF(data)==LF(raw);dest=out/'whitespace.fresh.full-negative.log.gz';dest.write_bytes(gzip.compress(data,mtime=0));preserved=bind(dest)
 else:
  assert data==b'';dest=out/'whitespace.fresh.authored.log';dest.write_bytes(data);preserved=bind(dest)
 s={'command':c,'process_id':pid,'foreground_process':True,'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':p.returncode,'actual_output_raw_sha256':H(data),'actual_output_lf_sha256':H(LF(data)),'preserved_output':preserved};dump(out/f'whitespace.check.{i}.status.json',s);fresh.append(s)
packet={'base_commit':base,'verdict':'ACCEPTED_NARROW_EXTERNAL_RAW_DIAGNOSTIC_EXCLUSION_ONLY','blocking':False,'external_raw_rows_total':29,'external_raw_rows_by_file':[24,5],'external_raw_files':rows,'original_diagnosis':bind(q/'staged.whitespace.diagnosis.json'),'root_full_negative_archive_contract':bind(q/'staged.whitespace.archive.json'),'root_lossless_deterministic_gzip':bind(r/archive['gzip_path']),'decompression_exact':True,'gzip_mtime':0,'gzip_embedded_filename':False,'fresh_actual_checks':fresh,'cached_paths':cached,'original_review_unchanged':bind(out/'review.json'),'original_candidate_unchanged':bind(r/'tools/tests/test_samplewiki_companions.py'),'scope':'Exactly two immutable GitHub original failed-log blobs excluded from authored staged whitespace; no production/source/Test/scientific or other authored bytes excluded. Full check remains actualexit2 and preserved; authored scoped check actualexit0.','root_guard_history':'Parent reports first guard matched immutable historical OPEN snapshots with no writes atfailure; explicit actualclosedpaths subsequently passed. This is reported roothistory, not synthetic independent timestamp evidence.','remaining':'No new compiler/theorem/VERIFIED/CI PASS/main/live/PURIFIED credit. Commit/push/freshremoteCI still pending. Original79 science and sealed Python repair admission reused immutable.','compiler':'NOT_STARTED_CLOSED'}
dump(out/'whitespace.review.json',packet);print(json.dumps({'verdict':packet['verdict'],'rows':[24,5],'fresh_codes':[x['exit_code']for x in fresh],'gzip_exact':True,'excluded_blobs':2,'new_Lean_runs':0}))
