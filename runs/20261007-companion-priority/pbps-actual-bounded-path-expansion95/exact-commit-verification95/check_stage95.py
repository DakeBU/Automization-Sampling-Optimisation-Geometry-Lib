import pathlib,json,gzip,subprocess,hashlib
R=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent;B=O.parent
C=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()
def sha(b):return hashlib.sha256(b).hexdigest()
def public(b):return b'\n'.join(x.rstrip(b' \t') for x in b.replace(b'\r\n',b'\n').split(b'\n')).rstrip(b'\n')+b'\n' if b else b''
def blob(p):return subprocess.check_output(['git','show',C+':'+p],cwd=R)
stage=json.loads((B/'science-staging95.json').read_bytes());archives={x['raw_path']:x for x in stage['raw_archives']};rows=[]
primary='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
for p in stage['files']:
 b=blob(p);local=(R/p).read_bytes()
 assert sha(b)!=primary and (not p.endswith('.gz') or sha(gzip.decompress(b))!=primary),'full primary republication'
 if p in archives:
  raw=gzip.decompress(blob(archives[p]['archive']));assert b==public(raw),p
  kind='exact declared RAW-to-public text normalization'
 else:assert b==local,p;kind='exact current local bytes'
 rows.append({'path':p,'git_blob_raw_sha256':sha(b),'bytes':len(b),'comparison':kind})
out={'status':'PASS','verified_commit':C,'stage_file_count':len(rows),'files':rows,'full_pinned_primary_added':False,'local_raw_primary_is_not_a_public_artifact':True,'normalization':'CRLF to LF, terminal spaces/tabs and extra final blank lines only, checked byte-for-byte against committed gzip.'}
(O/'all-staged-bytes95.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(len(rows))
