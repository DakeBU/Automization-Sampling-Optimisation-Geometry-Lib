"""Verify immutable science and historical RAW closure; never modify shared state."""
from pathlib import Path
import hashlib,json,gzip,subprocess,sys,re
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent
C=sys.argv[1];BASE='45e1f1457b59446dc4d1774cea510775c331d590'
M='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhaseReversalVolume.lean'
L='website/content/declaration_lessons/pbps-actual-phase-reversal-volume.json'
P='website/content/publications/pbps-actual-phase-reversal-volume.json'
A='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualPhaseReversalVolume.json'
CELL='research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-phase-reversal-volume.json'
PRE=B.parent/'pbps-phase-reversal-volume-preread96';D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseReversalVolume.actual_phase_reversal_volume_laws'
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda v:json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def rel(p):
 s=str(p).replace('\\','/');return s[len('E:/Samplinglib/'):] if s.startswith('E:/Samplinglib/') else s
def path(p):return R/rel(p)
def load(p):return json.loads(path(p).read_bytes())
def info(p):
 b=path(p).read_bytes();return dict(path=rel(p),raw_sha256=sha(b),bytes=len(b))
def save(n,v):
 p=O/n;assert not p.exists(),str(p);p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
def git(*args):return subprocess.check_output(['git',*args],cwd=R,stderr=subprocess.PIPE)
assert re.fullmatch('[0-9a-f]{40}',C) and git('rev-parse','HEAD').decode().strip()==C
assert git('merge-base',BASE,C).decode().strip()==BASE
tree={line.split('\t',1)[1]:line.split()[2] for line in git('ls-tree','-r',C).decode().splitlines()};cache={}
def blob(p):
 p=rel(p)
 if p not in cache:cache[p]=git('cat-file','blob',tree[p])
 return cache[p]
stage=load(B/'science-staging96.json');assert blob(B/'science-staging96.json')==path(B/'science-staging96.json').read_bytes()
collab=load(B.parent/'pbps-actual-bounded-path-expansion95/exact-commit-verification95/closed-RAW-manifest95.json')['preserved_collaborator_inputs']
assert len(collab)==21 and collab==stage['preserved_collaborator_inputs']
for x in collab:assert info(x['path'])['raw_sha256']==x['raw_sha256'],x['path']
byhash={};archive_audit=[];matched={};local={};historical=[];unresolved=[]
archives={rel(x['raw_path']):x for x in stage['raw_archives']}
for p,x in archives.items():
 ab=blob(x['archive']);rb=gzip.decompress(ab)
 assert sha(ab)==x['archive_sha256'] and sha(rb)==x['raw_sha256'] and rb==path(p).read_bytes(),p
 if x.get('public_text_sha256'):assert sha(blob(p))==x['public_text_sha256'],p
 byhash.setdefault(sha(rb),dict(archive=x['archive'],archive_sha256=sha(ab)));archive_audit.append(x)
for p in stage['files']:
 assert p in tree,p
 if p.endswith('.gz'):
  rb=gzip.decompress(blob(p));byhash.setdefault(sha(rb),dict(archive=p,archive_sha256=sha(blob(p))))
 else:byhash.setdefault(sha(blob(p)),dict(snapshot=p))
scanned=False
def history():
 global scanned
 if scanned:return
 scanned=True
 candidates=[p for p in tree if p.endswith(('.gz','.RAW','.snapshot','.exactraw')) or '.exactraw.' in p]
 batch=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
 for p in candidates:
  batch.stdin.write((tree[p]+'\n').encode());batch.stdin.flush();head=batch.stdout.readline().split();bb=batch.stdout.read(int(head[2]));assert batch.stdout.read(1)==b'\n'
  if p.endswith('.gz'):rb=gzip.decompress(bb);byhash.setdefault(sha(rb),dict(archive=p,archive_sha256=sha(bb)))
  else:byhash.setdefault(sha(bb),dict(snapshot=p))
 batch.stdin.close();assert batch.wait()==0
collabpaths={rel(x['path']) for x in collab}
def exact(p):
 p=rel(p)
 if p in matched or p in local:return
 b=path(p).read_bytes();h=sha(b)
 if p in collabpaths or p.startswith(('.lake/','.astis/')) or h=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760':
  local[p]=dict(**info(p),reason='Pinned runtime/library, preserved collaborator, or exact local primary excluded from republication.');return
 if p in tree and blob(p)==b:matched[p]=dict(**info(p),binding='exact Git blob',git_blob=tree[p]);return
 if h not in byhash:history()
 if h in byhash:matched[p]=dict(**info(p),binding='exact preserved Git archive/snapshot',**byhash[h]);return
 if (p in ['lean-toolchain','lake-manifest.json'] or p.startswith('tools/')) and p in tree and blob(p).replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n'):
  matched[p]=dict(**info(p),binding='newline-equivalent fixed tool/config',git_blob_sha256=sha(blob(p)));return
 raise AssertionError('UNPRESERVED CURRENT RAW '+p)
def record(x):
 p=x.get('path');h=x.get('raw_sha256',x.get('sha256'))
 if not isinstance(p,str) or not isinstance(h,str) or not re.fullmatch('[0-9a-f]{64}',h):return
 if path(p).is_file() and sha(path(p).read_bytes())==h:
  if 'bytes' in x:assert path(p).stat().st_size==x['bytes'],p
  exact(p);return
 if h not in byhash:history()
 if h not in byhash:unresolved.append(x);return
 location=byhash[h];bb=gzip.decompress(blob(location['archive'])) if 'archive' in location else blob(location['snapshot'])
 assert sha(bb)==h
 if 'bytes' in x:assert len(bb)==x['bytes'],p
 historical.append(dict(reference=x,**location))
def records(v):
 if isinstance(v,dict):
  record(v)
  for x in v.values():records(x)
 elif isinstance(v,list):
  for x in v:records(x)
def manifest(p):exact(p);v=load(p);records(v);return v
for p in [M,L,P,A,CELL,'lean-toolchain','lake-manifest.json','runs/substantive_advances.jsonl']:exact(p)
assert info(M)['raw_sha256']=='4b144dfa25d9521803e37518b8a6386fff08396c5804e410e9be593d46833a7b'
assert info(L)['raw_sha256']=='af8129aeb3cad23e7a2c98284e986abb90fbeb1da5fb05e1c2e44c8dd56c0951'
assert info('lake-manifest.json')['raw_sha256']=='b1f16b43aaf4a886cfe0382d5e3ae63d6904281c00afd8f35af20f0270a747e2'
assert git('-C','.lake/packages/mathlib','rev-parse','HEAD').decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
seal=manifest(PRE/'root.statement-seal96.json');assert seal['proposed_public_theorem']==D
for p in stage['files']:
 if p.endswith('.json') and ('manifest' in p.lower() or 'freeze' in p.lower()):manifest(p)
whole=manifest(B/'independent-whole-math96/whole-math-decision96.native.json')
expo=manifest(B/'independent-whole-math96/exposition96/exposition-decision96.native.json')
assert whole['decision']=='ACCEPT_EXACT_PRODUCTION_AND_SEALED_STATEMENT'
assert expo['decision']=='ACCEPT_MATHEMATICAL_STATEMENT_AND_SEVEN_PROOF_EXPLANATIONS'
assert whole['production']['raw_sha256']==info(M)['raw_sha256']
assert expo['inputs'][0]['raw_sha256']==info(L)['raw_sha256']
dec=R/'runs/semantic-roundtrip/anonymous96/decoder';dm=manifest(dec/'raw-manifest.json');dr=manifest(dec/'decoder-report.json');dp=load(dec.parent/'input.json');audit=load(A)
for p in [dec.parent/'input.json',dec/'reconstructed-theorem.txt']:exact(p)
assert dp.pop('packet_sha256')==sha(canon(dp))==dm['packet_sha256']==audit['reconstruction']['decoder_packet_sha256']
assert sha(canon({k:v for k,v in dr.items() if k!='decoder_run_sha256'}))==dr['decoder_run_sha256']==dm['decoder_run_sha256']==audit['reconstruction']['decoder_run_sha256']
assert not dm['source_text_visible'] and not dr['source_text_visible'] and not audit['reconstruction']['source_text_visible']
assert dr['exact_lean_statement']==dp['lean']['statement']
assert sha(dp['lean']['statement'].encode())==audit['reconstruction']['lean_statement_sha256']
assert audit['reconstruction']['text']==dr['reconstructed_theorem_text']==(dec/'reconstructed-theorem.txt').read_text(encoding='utf8')
assert sha(dr['reconstructed_theorem_text'].encode())==dm['reconstructed_text_sha256']
assert dr['semantic_slots']==audit['reconstruction']['native_semantic_slots']
# Source acceptance is checked separately in verify_source96.py once its native schema exists.
assert audit['state']=='accepted' and audit['source_review']['state']=='accepted'
sys.path[:0]=[str(R),str(R/'tools')]
from tools import astis_publication as pub
item=load(P)['items'][0];binding=next(x for x in item['bindings'] if x['declaration']==D)
bd=pub.binding_digest(item,binding);assert bd==audit['publication_binding_sha256']
pub.check_advance([D],reviewed=True)
save('archive-audit96.json',dict(status='PASS',archives=archive_audit,historical_reference_resolutions=historical))
save('source-decoder-bindings96.json',dict(status='PASS',decoder_run_sha256=dr['decoder_run_sha256'],decoder_packet_sha256=dm['packet_sha256'],publication_binding_sha256=bd,source_native_verification='separate required verify_source96.py receipt'))
save('input-freeze96.json',dict(status='FAIL' if unresolved else 'PASS',verified_commit=C,baseline=BASE,unresolved=unresolved,exact_commit_matches=list(matched.values()),local_pinned_or_excluded_inputs=list(local.values()),preserved_collaborator_inputs=collab,historical_reference_resolutions=historical))
assert not unresolved,unresolved
assert git('rev-parse','HEAD').decode().strip()==C
print(json.dumps(dict(status='PASS',matched=len(matched),local=len(local),historical=len(historical),archives=len(archive_audit))))
