from context109 import *
import gzip
assert head()==C
PRIMARY='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
if __name__=='__main__':
 assert head()==C and git('rev-parse',C+'^').decode().strip()==BASE
 tree={line.split('\t',1)[1]:line.split()[2] for line in git('ls-tree','-r',C).decode().splitlines()};cache={}
 def blob(p):
  p=rel(p)
  if p not in cache:cache[p]=git('cat-file','blob',tree[p])
  return cache[p]
 stage=load(B/'science-staging109.json');assert blob(B/'science-staging109.json')==(B/'science-staging109.json').read_bytes()
 scoped=list(dict.fromkeys(stage['files']+[rel(B/'science-staging109.json')]))
 changed=git('diff','--name-only',BASE,C).decode().splitlines();assert set(changed)<=set(scoped)
 assert len(stage['files'])==254 and len(scoped)==255,(len(scoped),len(stage['files']))
 assert not any('next-primary110' in p or 'exact-commit-verification109' in p for p in scoped)
 collab=load(B.parent/'pbps-actual-l2-flip-duality108/exact-commit-verification108/closed-RAW-manifest108.json')['preserved_collaborator_inputs']
 assert len(collab)==21 and collab==stage['preserved_collaborator_inputs']
 for x in collab:assert info(x['path'])['raw_sha256']==x['raw_sha256'],x['path']
 def batch_read(paths):
  batch=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
  for path in paths:
   if path in cache:continue
   batch.stdin.write((tree[path]+'\n').encode());batch.stdin.flush();hh=batch.stdout.readline().split();cache[path]=batch.stdout.read(int(hh[2]));assert batch.stdout.read(1)==b'\n'
  batch.stdin.close();assert batch.wait()==0
 batch_read(scoped)
 byhash={};archive_rows=[];matched={};local={};history_rows=[];span_rows=[];unresolved=[];scope=[]
 for x in stage['raw_archives']:
  ab=blob(x['archive']);rb=gzip.decompress(ab);assert sha(ab)==x['archive_sha256'] and sha(rb)==x['raw_sha256'] and rb==(R/x['raw_path']).read_bytes(),x['raw_path']
  assert sha(rb)!=PRIMARY
  if x.get('public_text_sha256'):assert sha(blob(x['raw_path']))==x['public_text_sha256']
  byhash[sha(rb)]=dict(archive=x['archive'],archive_sha256=sha(ab));archive_rows.append(x)
 for p in scoped:
  bb=blob(p)
  if p.endswith('.gz'):
   assert bb==(R/p).read_bytes(),p;rb=gzip.decompress(bb);assert sha(rb)!=PRIMARY;byhash.setdefault(sha(rb),dict(archive=p,archive_sha256=sha(bb)))
  else:
   rb=(R/p).read_bytes();nb=rb.replace(b'\r\n',b'\n')
   if p.startswith('runs/') and nb:nb=b'\n'.join(x.rstrip(b' \t') for x in nb.split(b'\n')).rstrip(b'\n')+b'\n'
   assert bb==nb,p;assert sha(bb)!=PRIMARY;byhash.setdefault(sha(bb),dict(snapshot=p))
  scope.append(dict(path=p,git_blob=tree[p],git_raw_sha256=sha(bb)))
 scanned=False
 def history():
  global scanned
  if scanned:return
  scanned=True
  candidates=[p for p in tree if p.endswith(('.gz','.RAW','.snapshot','.exactraw')) or '.exactraw.' in p]
  batch_read(candidates)
  for p in candidates:
   bb=blob(p);rb=gzip.decompress(bb) if p.endswith('.gz') else bb
   byhash.setdefault(sha(rb),dict(archive=p,archive_sha256=sha(bb)) if p.endswith('.gz') else dict(snapshot=p))
 def exact(p):
  p=rel(p)
  if p in matched or p in local:return
  b=(R/p).read_bytes();h=sha(b)
  if p in {rel(x['path']) for x in collab} or p.startswith(('.lake/','.astis/')) or h==PRIMARY:
   local[p]=dict(**info(p),reason='Pinned library/runtime, preserved collaborator or fixed original primary excluded from republication');return
  if p in tree and blob(p)==b:matched[p]=dict(**info(p),binding='exact Git blob',git_blob=tree[p]);return
  if h not in byhash:history()
  if h in byhash:matched[p]=dict(**info(p),binding='exact committed lossless archive/snapshot',**byhash[h]);return
  if (p in ['lean-toolchain','lake-manifest.json'] or p.startswith('tools/')) and p in tree and blob(p).replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n'):
   matched[p]=dict(**info(p),binding='fixed tool/config newline equivalence',git_blob_sha256=sha(blob(p)));return
  unresolved.append(dict(**info(p),reason='Original RAW not resolved in scoped or historical committed archives'))
 def records(v):
  if isinstance(v,dict):
   if 'source_RAW_sha256' in v:
    sp=rel(v['path']);sb=b''.join((R/sp).read_bytes().splitlines(keepends=True)[v['line_start']-1:v['line_end']]);assert sha(sb)==v['source_RAW_sha256'];assert sha(sb.replace(b'\r\n',b'\n'))==v['display_LF_RAW_sha256'];exact(sp);span_rows.append(v)
   if 'source_CRLF_span_RAW_sha256' in v:
    sp=rel(v['path']);sb=b''.join((R/sp).read_bytes().splitlines(keepends=True)[v['line_start']-1:v['line_end']]);assert sha(sb)==v['source_CRLF_span_RAW_sha256'];assert sha(sb.replace(b'\r\n',b'\n'))==v['display_LF_code_RAW_sha256'];exact(sp);span_rows.append(v)
   p=v.get('path');h=v.get('raw_sha256',v.get('sha256_raw',v.get('sha256')))
   if isinstance(p,str) and '/' in p.replace('\\','/') and isinstance(h,str) and re.fullmatch('[0-9a-f]{64}',h):
    p=rel(p)
    if (R/p).is_file() and 'line_start' in v and 'line_end' in v:
     rawlines=(R/p).read_bytes().splitlines(keepends=True);segment=b''.join(rawlines[v['line_start']-1:v['line_end']])
     assert sha(segment)==v.get('raw_span_sha256',h),('source span RAW mismatch',v)
     if 'raw_span_sha256' in v:assert sha((R/p).read_bytes())==h
     exact(p);span_rows.append(v)
    elif (R/p).is_file() and 'byte_start' in v and 'byte_end_exclusive' in v:
     segment=(R/p).read_bytes()[v['byte_start']:v['byte_end_exclusive']];assert sha(segment)==h;exact(p);span_rows.append(v)
    elif (R/p).is_file() and sha((R/p).read_bytes())==h:exact(p)
    else:
     if h not in byhash:history()
     if h not in byhash:unresolved.append(v)
     else:
      loc=byhash[h];bb=gzip.decompress(blob(loc['archive'])) if 'archive' in loc else blob(loc['snapshot']);assert sha(bb)==h
      if 'bytes' in v:assert len(bb)==v['bytes']
      if 'size_bytes' in v:assert len(bb)==v['size_bytes']
      history_rows.append(dict(reference=v,**loc))
   for q in v.values():records(q)
  elif isinstance(v,list):
   for q in v:records(q)
 def manifest(p):exact(p);v=load(p);records(v);return v
 for p in [M,L,P,A,CELL,'lean-toolchain','lake-manifest.json','runs/substantive_advances.jsonl']:exact(p)
 assert info(M)['raw_sha256']=='21c6b4e95b729b41f555eecf6a42185ab2f63bff7bcab3f6dc2ab82da171e85e'
 assert git('-C','.lake/packages/mathlib','rev-parse','HEAD').decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
 seal=manifest(PRE/'root.statement-seal109.json');assert info(PRE/'root.statement-seal109.json')['raw_sha256']=='d17001eb1349c6cd4c8711e8c729816570c88811f60a7bb2007ad0985680f8e9'
 for p in scoped:
  if p.endswith('.json') and ('manifest' in p.lower() or 'freeze' in p.lower()):manifest(p)

 for p in scoped:
  if p.endswith('.json'):records(load(p))
 save('science-scope109.json',dict(status='PASS',verified_commit=C,baseline=BASE,changed_files=changed,scoped_git_blobs=scope))
 save('archive-audit109.json',dict(status='PASS' if not unresolved else 'FAIL',verified_commit=C,archives=archive_rows,historical_reference_resolutions=history_rows,verified_code_spans=span_rows,unresolved=unresolved))
 save('input-freeze109.json',dict(status='FAIL' if unresolved else 'PASS',verified_commit=C,unresolved=unresolved,exact_commit_matches=list(matched.values()),local_pinned_or_excluded_inputs=list(local.values()),preserved_collaborator_inputs=collab,historical_reference_resolutions=history_rows))
 assert not unresolved,unresolved
 save('primary-scope109.native.json',dict(status='PASS',verified_commit=C,no_new_full_primary_RAW_or_gzip=True,all_scoped_blobs_and_gzip_contents_checked=True,baseline_historical_primary_files_unchanged=True))
 print('PASS_STORAGE',len(scope),len(matched),len(history_rows),len(archive_rows))
