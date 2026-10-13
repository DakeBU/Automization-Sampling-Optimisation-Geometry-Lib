import pathlib, json, hashlib, os, sys, subprocess, time, re, ctypes
from ctypes import wintypes
ROOT=pathlib.Path('E:/Samplinglib'); os.chdir(ROOT)
R=ROOT/'runs/20261007-companion-priority/pbps-centered-defect59'; D=R/'exact-science-verification'
COMMIT='2d6cd0167adc4fae1d8d166068a2eda51cd3c3ad'; BASE='ef0784198739f214b1d7bd5883b8f595179e5d04'
ACTOR='/root/whole_math52/exact-science59'; SAU='ASTIS-SA-20261008-PBPSCenteredDefectOperator'
def sha(b): return hashlib.sha256(b).hexdigest()
def canon(q): return json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def load(p): return json.loads(pathlib.Path(p).read_bytes())
def write(p,q): pathlib.Path(p).write_bytes((json.dumps(q,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
def path(s):
 s=str(s).replace('\\','/'); s=re.sub('/+','/',s)
 p=pathlib.Path(s); return p if p.is_absolute() else ROOT/p
def pin(p):
 p=path(p); b=p.read_bytes(); l=b.replace(b'\r\n',b'\n')
 return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def match(a,row):
 return a['raw_sha256']==row['raw_sha256'] and a['lf_sha256']==row['lf_sha256'] and a['bytes']==row.get('bytes',row.get('raw_bytes',a['bytes'])) and a['lf_bytes']==row.get('lf_bytes',a['lf_bytes'])
def git(*a): return subprocess.run(['git',*a],capture_output=True,check=True).stdout
def pins(q):
 if isinstance(q,dict):
  if {'path','raw_sha256','lf_sha256'}<=q.keys(): yield q
  for v in q.values(): yield from pins(v)
 elif isinstance(q,list):
  for v in q: yield from pins(v)
def check_self(q,field): assert sha(canon({k:v for k,v in q.items() if k!=field}))==q[field],field

assert git('rev-parse','HEAD').decode().strip()==COMMIT
assert git('rev-parse','HEAD^').decode().strip()==BASE
env=os.environ.copy(); inherited=env.pop('ELAN_TOOLCHAIN',None)
env.update(LEAN_NUM_THREADS='2',PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1')
write(D/'lease.open.json',dict(status='OPEN',actor=ACTOR,actual_Python_pid=os.getpid(),checked_commit=COMMIT,inherited_ELAN_TOOLCHAIN_removed=inherited,exclusive_focused_build=True))
freeze=load(R/'math-freeze.json'); assert len(freeze['inputs'])==27
frozen=[]
for row in freeze['inputs']:
 a=pin(row['path']); assert match(a,row),row['path']; frozen.append(a)
write(D/'math-inputs.json',dict(freeze=pin(R/'math-freeze.json'),inputs=frozen,count=27))

# Historical source-input resolution is exact qualified path AND original raw/LF identity.
source_manifest=load(R/'source-review59/input.manifest.json'); pairs=source_manifest['qualified_input_snapshot_pairs']
maps=[]
for x in pairs:
 assert match(pin(x['snapshot']['path']),x['original']),x
 current=pin(x['original']['path'])
 if not match(current,x['original']):
  assert 'research-wiki/semantic-roundtrip/audits/' in path(x['original']['path']).as_posix(),x
  maps.append(dict(original=x['original'],exact_snapshot=x['snapshot'],current=current,reason='Independent source review preceded canonical accepted audit admission'))
assert len(maps)==2
decoder_maps=load(R/'root.decoder59.adoption.json')['raw_snapshot_mappings']
def resolve(row):
 p=path(row['path'])
 if p.exists() and match(pin(p),row): return pin(p),'CURRENT_EXACT'
 for x in pairs:
  if path(x['original']['path'])==p and match(x['original'],row):
   a=pin(x['snapshot']['path']); assert match(a,row); return a,'EXACT_SOURCE_INPUT_SNAPSHOT'
 for x in decoder_maps:
  if path(x['original']['path'])==p and match(x['original'],row):
   a=pin(x['exact_raw_snapshot']['path']); assert match(a,row); return a,'EXACT_DECODER_ARCHIVE'
 raise AssertionError(('UNMAPPED_NATIVE_PIN',row))
native_files=[]
for folder, fs in [
 ('independent-math-review',['run.json','lease.json','receipt.json','outputs.final.json','readback.json','inputs.open.json','API.inputs.json']),
 ('source-review59',['run.json','lease.json','receipt.json','input.manifest.json','source.0.review.json','source.1.review.json','publication-exposition.review.json','foreground-final-readback.receipt.json']),
 ('anonymous-decoder',['decoder-run.json','lease.json','decoder-receipt.json','input-output-sha256.json','foreground-readback.json','packet0.json','packet1.json'])]:
 for f in fs: native_files.append(R/folder/f)
checks=[]; identities={}
for p in native_files:
 q=load(p)
 for row in pins(q):
  a,route=resolve(row); key=(path(row['path']).as_posix(),row['raw_sha256'],row['lf_sha256'])
  identities[key]=dict(original=row,resolved=a,route=route)
 checks.append(pin(p))
math=load(R/'independent-math-review/run.json'); check_self(math,'run_sha256')
assert sha(canon(math['mathematics_review_payload']))==math['mathematics_review_payload_sha256']
check_self(load(R/'independent-math-review/lease.json'),'lease_sha256')
check_self(load(R/'independent-math-review/outputs.final.json'),'outputs_sha256')
assert load(R/'independent-math-review/lease.json')['status']=='CLOSED'
source=load(R/'source-review59/run.json'); check_self(source,'run_sha256')
assert sha(canon(source['named_source_review_payload']))==source['named_source_review_payload_sha256']
assert load(R/'source-review59/named-source-review.payload.json')==source['named_source_review_payload']
for i,q in enumerate(source['named_source_review_payload']['reviews_before_native_run_binding']):
 actual=load(R/f'source-review59/source.{i}.review.json')
 assert actual==dict(q,review_run_sha256=source['run_sha256'])
 assert q['verdict']=='equivalent-after-elaboration' and len(q['semantic_slots'])==7 and not q['repairs']
 assert not any(x['blocking'] for x in q['deltas']) and q['independent_from_formalizer'] and q['independent_from_decoder']
assert source['decisions']['EXCESS']==source['decisions']['repairs']==source['decisions']['blocking_deltas']==0
assert load(R/'source-review59/lease.json')['status']=='CLOSEDLAST'
assert load(R/'source-review59/lease.json')['actual_final_readback_exit_code']==0
anon=load(R/'anonymous-decoder/decoder-run.json'); al=load(R/'anonymous-decoder/lease.json')
assert not anon['source_text_visible'] and not anon['source_identity_visible'] and not anon['compiler_started']
assert al['status']=='CLOSEDLAST' and al['authoritative_foreground_readback']['exit_code']==0
for i in range(2):
 q=load(R/f'anonymous-decoder/packet{i}.json')
 assert sha(canon({k:v for k,v in q.items() if k!='packet_sha256'}))==q['packet_sha256']
write(D/'native-checks.json',dict(native_object_inputs=checks,qualified_unique_pin_count=len(identities),pin_checks=list(identities.values()),historical_source_audit_mappings=maps,math_run_sha256=math['run_sha256'],math_payload_sha256=math['mathematics_review_payload_sha256'],source_run_sha256=source['run_sha256'],source_payload_sha256=source['named_source_review_payload_sha256'],decoder_run_raw_sha256=pin(R/'anonymous-decoder/decoder-run.json')['raw_sha256'],decoder_native_has_whole_self_digest=False,decoder_recipe_scope='Packet complete-object hash excluding packet_sha256 only; decoder run is raw/LF bound, not invented self field',whole_self_checks=4,distinct_payload_checks=2,packet_self_checks=2))

# Commit delta: every added/changed exact Git entry, binary-safe blob batch, no basename alias.
names=[x.decode() for x in git('diff','--name-only','-z',BASE,COMMIT).split(b'\0') if x]
entries={}
for row in git('ls-tree','-r','-z',COMMIT).split(b'\0'):
 if row:
  metadata,name=row.split(b'\t',1); mode,kind,oid=metadata.decode().split(); entries[name.decode()]=(mode,kind,oid)
ids=[entries[n][2] for n in names]
blob=subprocess.run(['git','cat-file','--batch'],input=('\n'.join(ids)+'\n').encode(),capture_output=True,check=True).stdout
offset=0; gitrows=[]
ledger=ROOT/'runs/substantive_advances.jsonl'
ledger_bytes=ledger.read_bytes(); (D/'ledger.before.exactraw.snapshot').write_bytes(ledger_bytes)
for n,oid in zip(names,ids):
 end=blob.index(b'\n',offset); h=blob[offset:end].decode().split(); size=int(h[2]); b=blob[end+1:end+1+size]; offset=end+size+2
 assert h[0]==oid and h[1]=='blob'
 a=pin(ROOT/n); assert sha(b.replace(b'\r\n',b'\n'))==a['lf_sha256'],n
 gitrows.append(dict(path=(ROOT/n).as_posix(),git_blob_oid=oid,git_bytes=len(b),git_raw_sha256=sha(b),git_lf_sha256=sha(b.replace(b'\r\n',b'\n')),working=a))
assert offset==len(blob)
write(D/'git-science-inputs.json',dict(checked_commit=COMMIT,parent=BASE,entry_count=len(gitrows),entries=gitrows,ledger_before=pin(D/'ledger.before.exactraw.snapshot')))
codepaths=[path(freeze['inputs'][i]['path']) for i in [0,1]]
headers=[]; scan=[]
for i,p in enumerate(codepaths):
 s=p.read_text(encoding='utf8'); h=s[s.index('theorem '):s.index(' := by\n')].rstrip()+'\n'
 expected=ROOT/f'runs/20261007-companion-priority/pbps-centered-defect-preproof59/independent-elab-type-second/header{i}.inline-kernel-proposed.lean'
 assert h.encode()==expected.read_bytes()
 assert not re.search(r'\b(sorry|admit|axiom)\b|Prop\s*:=\s*True|:=\s*trivial',s)
 assert len(re.findall(r'^theorem ',s,re.M))==1 and 'trace "' not in s
 headers.append(dict(source=pin(p),sealed_header=pin(expected),signature_sha256=sha(h.encode())))
 scan.append(dict(source=pin(p),authored_fake_closures=0,actual_named_theorems=1,private_provider_count=0))
for row in frozen[2:6]:
 s=path(row['path']).read_text(encoding='utf8')
 assert not re.search(r'\b(sorry|admit|axiom)\b|Prop\s*:=\s*True|:=\s*trivial',s)
 scan.append(dict(source=row,authored_fake_closures=0,role='Actual unchanged public parent'))
write(D/'headers-and-fake-scan.json',dict(headers=headers,authored_scan_rows=scan,early_failed_elaboration_sorryAx_credit=False))
assert (ROOT/'lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0'
assert next(x for x in load(ROOT/'lake-manifest.json')['packages'] if x['name']=='mathlib')['rev']=='db584cd6d46c92f209a44c0f1c829460d327499d'

class Entry(ctypes.Structure):
 _fields_=[('dwSize',wintypes.DWORD),('cntUsage',wintypes.DWORD),('th32ProcessID',wintypes.DWORD),('th32DefaultHeapID',ctypes.c_size_t),('th32ModuleID',wintypes.DWORD),('cntThreads',wintypes.DWORD),('th32ParentProcessID',wintypes.DWORD),('pcPriClassBase',ctypes.c_long),('dwFlags',wintypes.DWORD),('szExeFile',wintypes.WCHAR*260)]
k=ctypes.WinDLL('kernel32',use_last_error=True);k.CreateToolhelp32Snapshot.restype=wintypes.HANDLE;k.Process32FirstW.argtypes=[wintypes.HANDLE,ctypes.POINTER(Entry)];k.Process32NextW.argtypes=[wintypes.HANDLE,ctypes.POINTER(Entry)];k.CloseHandle.argtypes=[wintypes.HANDLE]
def processes():
 h=k.CreateToolhelp32Snapshot(2,0); e=Entry();e.dwSize=ctypes.sizeof(e); rows=[]
 if k.Process32FirstW(h,ctypes.byref(e)):
  while True:
   rows.append(dict(pid=e.th32ProcessID,parent_pid=e.th32ParentProcessID,exe=e.szExeFile))
   if not k.Process32NextW(h,ctypes.byref(e)):break
 k.CloseHandle(h); return rows
def tree(pid):
 rows=processes();ids={pid}
 for _ in range(12):
  added={r['pid'] for r in rows if r['parent_pid'] in ids}; old=len(ids);ids.update(added)
  if len(ids)==old:break
 return [r for r in rows if r['pid'] in ids]
gates=[]
def gate(name,cmd,compiler=False):
 observed={}
 with (D/(name+'.stdout.log')).open('wb') as out,(D/(name+'.stderr.log')).open('wb') as err:
  p=subprocess.Popen(cmd,env=env,stdout=out,stderr=err)
  while p.poll() is None:
   if compiler:
    for row in tree(p.pid):observed[row['pid']]=row
   time.sleep(.05)
  code=p.wait()
 q=dict(name=name,command=cmd,actual_pid=p.pid,actual_exit_code=code,observed_processes=list(observed.values()),stdout=pin(D/(name+'.stdout.log')),stderr=pin(D/(name+'.stderr.log')),closed=True)
 gates.append(q); write(D/(name+'.status.json'),q); assert code==0,(name,code)
 return q
gate('Lean.version',['lake','env','lean','--version'])
assert not [r for r in processes() if r['exe'].lower()=='lean.exe'],'Concurrent Lean compiler'
focused=gate('focused',['lake','build','Tests.ProximalBPSCenteredDefect'],True)
out=(D/'focused.stdout.log').read_text(encoding='utf8');assert 'Build completed successfully (3911 jobs)' in out and 'sorryAx' not in out
closures=[]
for n in freeze['mathematical_declarations']:
 m=re.search(re.escape(n)+r"' depends on axioms: \[([^]]*)\]",out,re.S);assert m,n
 ax=[x.strip() for x in m.group(1).replace('\n',' ').split(',')];assert set(ax)=={'propext','Classical.choice','Quot.sound'}
 closures.append(dict(declaration=n,axioms=ax))
write(D/'axiom-closures.json',dict(closures=closures,actual_stdout=pin(D/'focused.stdout.log'),nonforced=True,lean_child_observed=any(r['exe'].lower()=='lean.exe' for r in focused['observed_processes'])))
decls=freeze['mathematical_declarations']
gate('publication.reviewed',[sys.executable,'-B','-X','utf8','-c','from tools.astis_publication import check_advance; check_advance('+repr(decls)+',reviewed=True); print("reviewed publication PASS")'])
gate('publication.changed-module',[sys.executable,'-B','-X','utf8','tools/astis_publication.py','check','--base',BASE])
gate('semantic',[sys.executable,'-B','-X','utf8','tools/astis_semantic_roundtrip.py','check'])
gate('frontier',[sys.executable,'-B','-X','utf8','tools/astis_frontier_cells.py','check'])
gate('contributor',[sys.executable,'-B','-X','utf8','tools/astis_contributor_contract.py','check','--base','origin/main'])
write(D/'gates.json',dict(actual_foreground_gates=gates,count=len(gates),deferred=['Mandatory full ASTIS root build and root Tests','Registry/shared import integration','Generated official and cell graphs/site and browser acceptance'],no_full_aggregate_gate_claim=True))
for a in frozen: assert pin(a['path'])==a
for x in identities.values(): assert match(pin(x['resolved']['path']),x['resolved'])
for row in gitrows: assert pin(row['path'])==row['working']
write(D/'input-postcheck.json',dict(frozen27_unchanged=True,native_unique_pins=len(identities),science_entries=len(gitrows),all_exact=True,actual_Python_pid=os.getpid()))
print(json.dumps(dict(status='EXACT59_CHECKS_PASS_BEFORE_TRANSITION',checked_commit=COMMIT,science_entries=len(gitrows),frozen_math=27,native_unique_pins=len(identities),actual_lake_pid=focused['actual_pid'],actual_lake_exit=0,lean_children=[r for r in focused['observed_processes'] if r['exe'].lower()=='lean.exe'],actual_reader_pid=os.getpid(),gate_count=len(gates)),ensure_ascii=False),flush=True)
