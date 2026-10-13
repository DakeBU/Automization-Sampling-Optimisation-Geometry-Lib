import datetime,hashlib,json,os,pathlib,subprocess,sys,traceback
R=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent;D=O.parent;H=D.parent/'pbps-ambient-adjoint-preproof66';BASE='31ce36e7ca01b203696918672c33d29a337550c3';ACTOR='/root/exact_science63';PY='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(j):return json.dumps(j,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def read(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))
def write(f,j):
 assert not (O/'lease.final.json').exists();p=O/f;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(j,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();return {'path':p.as_posix(),'raw_bytes':len(b),'lf_bytes':len(b.replace(b'\r\n',b'\n')),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n'))}
def check(x):
 p=pin(x['path']);assert p['raw_sha256']==x['raw_sha256'] and p['lf_sha256']==x['lf_sha256'];assert p['raw_bytes']==x.get('raw_bytes',x.get('bytes'))
def frozen(rel):
 j=read(O/'inputs.manifest.json');full=(R/rel).as_posix();x=next(x for x in j['inputs'] if x['original']['path']==full);check(x['RAW_snapshot']);return pathlib.Path(x['RAW_snapshot']['path']).read_bytes()
def freeze():
 assert not (O/'lease.open.json').exists();write('lease.open.json',{'schema':'independent-precommit-math66-OPEN-v1','status':'OPEN','actor':ACTOR,'checked_base':BASE,'owned_prefix':O.as_posix(),'actual_open_pid':os.getpid(),'utc':now(),'no_SCI66_commit_or_VERIFIED':True,'source_review_separate':True,'canonical_source_Lean_Git_ledger_writes':False})
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==BASE
 m=read(D/'math-freeze.json');rows=[]
 for n,x in enumerate([pin(D/'math-freeze.json')]+m['inputs']):
  check(x);b=pathlib.Path(x['path']).read_bytes();raw=O/'inputs'/f'{n:03}.RAW.snapshot';lf=O/'inputs'/f'{n:03}.LF.snapshot';raw.parent.mkdir(exist_ok=True);raw.write_bytes(b);lf.write_bytes(b.replace(b'\r\n',b'\n'));rows.append({'original':x,'RAW_snapshot':pin(raw),'LF_snapshot':pin(lf),'initial_resolution':'Exact current frozen RAW equality; future current draft metadata changes must use this finite named original→frozen mapping, never a blanket fallback.'})
 write('inputs.manifest.json',{'schema':'independent-math66-frozen-RAW-LF-inputs-v1','checked_base':BASE,'candidate_commit':'UNCOMMITTED','actual_freezer_pid':os.getpid(),'utc':now(),'inputs':rows,'scope':'Bounded frozen target/headers/source ingredient inventory/representation closure and original math-freeze only. No ledger/history/native directory recursion.','audit_frozen_before_decoder_source_advances':next(x for x in rows if '/semantic-roundtrip/audits/' in x['original']['path']),'anti_anchoring':'No future source66 decision used for mathematical acceptance.'})
 print(json.dumps({'status':'FROZEN','actual_pid':os.getpid(),'inputs':len(rows),'base':BASE,'audit_RAW':next(x for x in rows if '/semantic-roundtrip/audits/' in x['original']['path'])['original']['raw_sha256']}),flush=True)
if __name__=='__main__':
 mode=sys.argv[1]
 try:globals()[mode]()
 except Exception as e:
  if not (O/'lease.final.json').exists():write(mode+'.failure.json',{'status':'FAIL','actual_pid':os.getpid(),'exception':repr(e),'traceback':traceback.format_exc(),'utc':now()})
  raise
