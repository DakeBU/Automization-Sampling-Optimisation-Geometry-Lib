from pathlib import Path
import json,hashlib,subprocess,os,sys,time,re,shutil
ROOT=Path('E:/Samplinglib');BASE=ROOT/'runs/20261007-companion-priority/pbps-centered-root64';OUT=BASE/'exact-science-verification';ACTOR='/root/exact_science63';COMMIT='59fff63d320aa5e3dc4b45e81e40e2029ce42734';PARENT='ee6bdf211d0ef8c9db63ecd199a52fa8cbbb81c4';SAU='ASTIS-SA-20261009-PBPSCenteredRootOrderInverse';PY='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
DECLS=['AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareOrder.positive_square_order','AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredRootOrderInverse.actual_centered_root_order_inverse'];TEST='Tests.ProximalBPSCenteredRootOrderInverse.genuine_actual_centered_inverse_consumer'
def sha(b):return hashlib.sha256(b).hexdigest()
def compact(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def load(p):return json.loads(Path(p).read_bytes().decode('utf-8-sig'))
def write(n,x):p=OUT/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode());return p
def rawpin(p):p=Path(p);b=p.read_bytes();return {'path':p.as_posix(),'raw_bytes':len(b),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n'))}
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT,stderr=subprocess.DEVNULL).decode().strip()
def blob(c,p):return subprocess.check_output(['git','show',c+':'+p],cwd=ROOT,stderr=subprocess.DEVNULL)
def checkpins(rows):
 for x in rows:assert rawpin(Path(x['path']))=={k:x[k] for k in ['path','raw_bytes','raw_sha256','lf_sha256']},x['path']
def command(label,args):
 d=OUT/label;d.mkdir(exist_ok=True);pre=[rawpin(Path(x['path'])) for x in load(OUT/'input.manifest.json')['inputs']];start=time.time()
 with (d/'stdout.log').open('wb') as out,(d/'stderr.log').open('wb') as err:
  p=subprocess.Popen(args,cwd=ROOT,stdout=out,stderr=err);code=p.wait()
 post=[rawpin(Path(x['path'])) for x in pre];r={'command':args,'cwd':ROOT.as_posix(),'checked_commit':COMMIT,'actual_foreground_pid':p.pid,'observer_pid':os.getpid(),'started_unix':start,'finished_unix':time.time(),'exit_code':code,'terminal_closed':True,'pre':pre,'post':post,'pre_post_equal':pre==post,'stdout':rawpin(d/'stdout.log'),'stderr':rawpin(d/'stderr.log')};write(label+'/receipt.json',r);assert pre==post;return r
def compile():
 assert git('rev-parse','HEAD')==COMMIT and git('rev-parse',COMMIT+'^')==PARENT
 old=load(BASE/'independent-math64/mathematical-review.json');rows=[]
 for x in old['candidate_headers_exact_sealed']:
  pin=x['candidate'];p=Path(pin['path']);rel=p.relative_to(ROOT).as_posix();assert sha(blob(COMMIT,rel))==sha(p.read_bytes())==pin['raw_sha256'];rows.append({'path':rel,'Git_RAW_sha256':sha(blob(COMMIT,rel)),'closed_mathematical_review_RAW':pin,'exact_RAW_equal':True})
 write('mathematics-reuse.json',{'status':'EXACT_GIT_RAW_EQUALITY_REUSES_CLOSED_INDEPENDENT_MATHEMATICS','checked_commit':COMMIT,'closed_math_review':rawpin(BASE/'independent-math64/mathematical-review.json'),'closed_math_lease':rawpin(BASE/'independent-math64/lease.json'),'three_exact_SOURCE_files':rows,'mathematical_delta':'Same actual63Gamma/e/U/T, sameG/C4, Q positive-square order, exactHP0/operator inequality/derived unit/bothinverse/norm and genuine Test consumer previously independently proved; no broad63 transcripts replayed.','precommit_publication_blocker':'Original step6 issue retained in CLOSED math record; current all12BODY literal spans require fresh independent check.'})
 r=command('focused',[shutil.which('lake'),'build','Tests.ProximalBPSCenteredRootOrderInverse']);assert r['exit_code']==0
 s=(OUT/'focused/stdout.log').read_text(encoding='utf-8');assert 'Build completed successfully (3944 jobs).' in s
 axioms=[]
 for n in DECLS+[TEST]:
  m=re.search(re.escape("'"+n+"' depends on axioms: [")+r'([^\]]+)\]',s,re.S);assert m,n;a={v.strip() for v in m.group(1).split(',')};assert a=={'propext','Classical.choice','Quot.sound'};axioms.append({'declaration':n,'axioms':sorted(a)})
 write('focused.result.json',{'status':'PASS','checked_commit':COMMIT,'actual_compiler_pid':r['actual_foreground_pid'],'exit_code':0,'terminal_closed':True,'jobs':3944,'pre_post_pin_count':len(r['pre']),'axioms':axioms});print(json.dumps({'status':'EXACT_COMMIT_COMPILE_PASS','actual_pid':r['actual_foreground_pid'],'jobs':3944,'standard3_declarations':3,'stable_pre_post_pins':len(r['pre'])}))
if __name__=='__main__':{'compile':compile}[sys.argv[1]]()
