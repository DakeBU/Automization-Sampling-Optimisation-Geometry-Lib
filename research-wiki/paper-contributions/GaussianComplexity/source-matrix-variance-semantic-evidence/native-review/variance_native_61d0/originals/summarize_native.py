from runner import *
import gzip,re,shutil,collections
RAW=OUT/'commands/inventory-kernel-v4/stdout';GZ=OUT/'local-only/inventory-kernel-v4.stdout.gz'
GZ.parent.mkdir(exist_ok=True)
# Streaming lossless compression and independent streaming decompression hash.
h=hashlib.sha256();n=0
with RAW.open('rb') as src,GZ.open('wb') as dst,gzip.GzipFile(fileobj=dst,mode='wb',mtime=0) as z:
 while b:=src.read(1024*1024):h.update(b);n+=len(b);z.write(b)
zsha=hashlib.sha256();zn=0
with GZ.open('rb') as f:
 while b:=f.read(1024*1024):zsha.update(b);zn+=len(b)
back=hashlib.sha256();bn=0
with gzip.open(GZ,'rb') as f:
 while b:=f.read(1024*1024):back.update(b);bn+=len(b)
assert n==bn and h.digest()==back.digest()
receipt=json.loads((OUT/'commands/inventory-kernel-v4/result.json').read_text());assert h.hexdigest()==receipt['stdout']['sha256']
compressed={'raw_path':str(RAW),'raw_bytes':n,'raw_sha256':h.hexdigest(),'gzip_path':str(GZ),'gzip_bytes':zn,'gzip_sha256':zsha.hexdigest(),'streaming_roundtrip_bytes':bn,'streaming_roundtrip_sha256':back.hexdigest(),'export':False}
(OUT/'proofdump-local-only.json').write_text(json.dumps(compressed,indent=2))
# Stream out just metadata; typeExpr/valueExpr remain complete in the local lossless dump.
marker=re.compile(rb'"(typeExpr|valueExpr)":')
closing=re.compile(rb'(?<!\\)(?:\\\\)*"')
buf=b'';state='normal';field=None;records=[];token_hash=None;token_n=0
with RAW.open('rb') as src,(OUT/'inventory-metadata.raw.jsonl').open('wb') as dst:
 eof=False
 while not eof or buf:
  if not eof and (len(buf)<128 or state=='skip'):
   new=src.read(1024*1024);eof=not new;buf+=new
  if state=='normal':
   m=marker.search(buf)
   if m:
    dst.write(buf[:m.end()]);field=m[1].decode();buf=buf[m.end():];state='expect'
   else:
    limit=len(buf) if eof else max(0,len(buf)-64)
    dst.write(buf[:limit]);buf=buf[limit:]
  elif state=='expect':
   if buf.startswith(b'null'):dst.write(b'null');buf=buf[4:];state='normal'
   elif buf.startswith(b'"'):
    dst.write(b'"[complete expression retained in local-only gzip]"')
    token_hash=hashlib.sha256();token_hash.update(b'"');token_n=1;buf=buf[1:];state='skip'
   else:raise RuntimeError(('unexpected expression value',buf[:40]))
  else:
   m=closing.search(buf)
   if m:
    end=m.end();token_hash.update(buf[:end]);token_n+=end
    records.append({'field':field,'serialized_json_token_bytes':token_n,'serialized_json_token_sha256':token_hash.hexdigest()})
    buf=buf[end:];state='normal'
   else:
    # Retain a possible trailing escape sequence across chunk boundaries.
    end=len(buf)
    while end and buf[end-1]==92:end-=1
    assert not eof,'unterminated expression string'
    token_hash.update(buf[:end]);token_n+=end;buf=buf[end:]
(OUT/'expression-token-hashes.json').write_text(json.dumps(records,indent=2))
decls=[];rootchecks=[];other=[]
with (OUT/'inventory-metadata.raw.jsonl').open() as f:
 for line in f:
  if line.startswith('{'):
   d=json.loads(line)
   if d.get('record')=='declaration':decls.append(d)
   elif d.get('record')=='literal-root-value-check':rootchecks.append(d)
  elif 'error:' in line:other.append(line)
assert not other and len(rootchecks)==2
assert all(d['closed'] and d['kernel_actual_typed_let_checked'] and set(d['axioms'])<={'propext','Classical.choice','Quot.sound'} for d in decls)
assert len(records)==2*len(decls),(len(records),len(decls))
for i,d in enumerate(decls):
 d['type_expression_token']=records[2*i];d['value_expression_token']=records[2*i+1]
by={d['name']:d for d in decls};roots={('P' if 'truncated_matrix_second_moments' in d['actual_name'] else 'T'):d['actual_name'] for d in rootchecks}
for d in decls:
 d['direct_ASTIS_type_parents']=[x for x in d['typeConstants'] if x in by]
 d['direct_ASTIS_body_parents']=[x for x in d['valueConstants'] if x in by]
def reachable(n):
 visited=set();todo=[n]
 while todo:
  k=todo.pop()
  if k in visited:continue
  visited.add(k);d=by[k];todo.extend(d['direct_ASTIS_type_parents']+d['direct_ASTIS_body_parents'])
 return sorted(visited)
reach={tag:reachable(n) for tag,n in roots.items()}
Pmod='AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixVariance';Tmod='Tests.GaussianComplexityFixedSpectrumSourceMatrixVariance'
p=json.loads((OUT/'preparation.json').read_text());sys.path[:0]=[str(OUT/'candidate/tools')]
import astis_site as base
modules,hand=base.scan_project_sources();handnames={d.full_name for d in hand}
for d in decls:
 # Private mangling prefix comes from the fresh environment; compare suffix to independently scanned source names.
 d['classification']='handwritten' if d['name'] in handnames or any(d['name'].endswith('.'+x) for x in handnames) else 'generated'
owned={tag:[{'name':d['name'],'classification':d['classification'],'root_reachable':d['name'] in reach[tag]} for d in decls if d['module']==m] for tag,m in [('P',Pmod),('T',Tmod)]}
full_reach=set(reach['P'])|set(reach['T'])
unused=[d['name'] for d in decls if d['module'] not in {Pmod,Tmod} and d['name'] not in full_reach]
summary={'actual_math_compiled_commit':COMMIT,'kernel_exit':receipt['exit'],'module_count':len(p['order']),'declaration_count':len(decls),'all_actual_types_and_bodies_closed':True,'actual_typed_let_kernel_checked_count':sum(d['kernel_actual_typed_let_checked'] for d in decls),'standard_axioms_only':True,'roots':roots,'root_checks':rootchecks,'direct_parents':{tag:{'type':by[n]['direct_ASTIS_type_parents'],'body':by[n]['direct_ASTIS_body_parents']} for tag,n in roots.items()},'root_reachability':reach,'owned':owned,'old_imported_unused_inventory':unused,'all_modules':dict(collections.Counter(d['module'] for d in decls)),'shared_S_is_preexisting_provider_not_R9_new_node':True,'private_T_is_material_consumer_not_public_API':True,'full_expr_evidence':'local-only gzip and expression-token-hashes; not portable export','fake_closure_scan':'pending below'}
bad=[];patterns={'placeholder':r'\b(sorry|admit|axiom|constant|postulate)\b','fake_true':r'\bProp\s*:=\s*True\b','fake_trivial':r':=\s*trivial\b'}
for row in p['sources']:
 clean=base.sanitize_lean((OUT/'candidate'/row['path']).read_text())
 for kind,pat in patterns.items():
  for m in re.finditer(pat,clean):bad.append({'file':row['path'],'kind':kind,'line':clean[:m.start()].count('\n')+1,'token':m.group()})
assert not bad,bad
summary['fake_closure_scan']={'sanitizer':'fixed e654 tools/astis_site.py sanitize_lean','files':len(p['sources']),'findings':bad,'patterns':patterns}
(OUT/'declaration-inventory.json').write_text(json.dumps(decls,indent=2))
(OUT/'native-summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps({k:summary[k] for k in ['declaration_count','roots','direct_parents','owned']},indent=2))
