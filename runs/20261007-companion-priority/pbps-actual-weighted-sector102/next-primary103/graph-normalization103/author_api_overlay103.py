import pathlib,json,hashlib,datetime,copy
R=pathlib.Path('E:/Samplinglib');B='runs/20261007-companion-priority/pbps-actual-weighted-sector102/next-primary103/';O=R/(B+'graph-normalization103/')
def ref(p):
 b=(R/p).read_bytes();return {'path':p,'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def put(n,d):
 p=O/n;assert not p.exists();p.write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf-8'));return ref(p.relative_to(R).as_posix())
def read(p):return json.loads((R/p).read_text(encoding='utf-8'))
g=ref(B+'source-proof-graph-delta103.native.json');r=ref(B+'retrieval103.native.json')
assert g['raw_sha256']=='13a69ec13506897d6946fd6c91a4b4bad0719aea3aa486492a92a789ca47a041'
assert r['raw_sha256']=='2db57ab6f91afda56b14b8686524eb5da192339726f5c1218fdfbab95e7028ef'
math=ref('.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/WithDensity.lean');ls=(R/math['path']).read_bytes().splitlines(keepends=True)
def span(a,b):
 v=b''.join(ls[a-1:b]);return {'line_start':a,'line_end':b,'raw_sha256':hashlib.sha256(v).hexdigest(),'bytes':len(v)}
changes=[(g,'/existing_compiled_leaves_referenced/6/id','MeasureTheory.Measure.prod_withDensity','MeasureTheory.prod_withDensity'),(g,'/AND_dependency_groups/4/sources/6','MeasureTheory.Measure.prod_withDensity','MeasureTheory.prod_withDensity'),(r,'/APIs/5','MeasureTheory.Measure.prod_withDensity','MeasureTheory.prod_withDensity'),(r,'/APIs/6','MeasureTheory.Measure.prod_withDensity_left','MeasureTheory.prod_withDensity_left')]
normalized={g['path']:read(g['path']),r['path']:read(r['path'])}
for f,pointer,old,new in changes:
 obj=normalized[f['path']];parts=pointer.split('/')[1:]
 for key in parts[:-1]:obj=obj[int(key)] if isinstance(obj,list) else obj[key]
 key=int(parts[-1]) if isinstance(obj,list) else parts[-1];assert obj[key]==old;obj[key]=new
# Verify only the four explicitly named strings differ; this is mechanical scope checking, not topology admission.
def diffs(a,b,path=''):
 if type(a)!=type(b):return [path]
 if isinstance(a,dict):
  assert a.keys()==b.keys();return sum((diffs(a[k],b[k],path+'/'+k) for k in a),[])
 if isinstance(a,list):
  assert len(a)==len(b);return sum((diffs(x,y,path+'/'+str(i)) for i,(x,y) in enumerate(zip(a,b))),[])
 return [] if a==b else [path]
for f in [g,r]:assert sorted(diffs(read(f['path']),normalized[f['path']]))==sorted(p for ff,p,_,_ in changes if ff['path']==f['path'])
for x in read(B+'closed-RAW-manifest103.native.json')['owned_artifacts']:assert ref(x['path'])==x
H='runs/20261007-companion-priority/pbps-phase-normalization-preread103/independent-header-source103/'
for x in read(H+'closed-RAW-manifest103.native.json')['owned_artifacts']:assert ref(x['path'])==x
ov=put('source-api-identity-normalization103.native.json',{'kind':'append-only-prospective103-source-API-identity-overlay','author':'/root/source_final96','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_graph':g,'original_retrieval':r,'reason':'Independent math reviewer identified creator namespace transcription error; pinned Mathlib verifies both declarations belong directly to MeasureTheory, not MeasureTheory.Measure.','pinned_API_source':math,'namespace_evidence':{'open_namespace':span(32,32),'prod_withDensity_left':span(701,703),'prod_withDensity':span(726,728),'closing_namespace':span(794,794)},'corrections':[{'input':f,'json_pointer':p,'old':old,'new':new,'operation':'replace-exact-string-only'} for f,p,old,new in changes],'effective_document_canonical_sha256':{p:hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest() for p,v in normalized.items()},'correction_scope':'Exactly four occurrences of two namespace strings in original graph/retrieval; no semantic statement, binder, conclusion, graph incidence, source region, producer requirement, or future consumer change. Graph API identity is corrected consistently at leaf id and its edge source.','original_native_files_unchanged':True,'header_review_unchanged':True,'header_unchanged':ref('runs/20261007-companion-priority/pbps-phase-normalization-preread103/Header103.lean'),'source_creator_acknowledgment':'The extra Measure namespace was my retrieval/graph transcription error. This append-only overlay corrects it without rewriting the closed source packet.','independent_admission':'Pending exact_verifier96; creator performs no topology self-validation.','self_topology_validation':False,'proof_credit':False,'no_claim_seal_or_shared_edit':True})
inputs=[g,r,math,ref(B+'closed-RAW-manifest103.native.json'),ref(H+'header-source-decision103.native.json'),ref(H+'closed-RAW-manifest103.native.json'),ref('runs/20261007-companion-priority/pbps-phase-normalization-preread103/Header103.lean')]
owned=[ref(p.relative_to(R).as_posix()) for p in sorted(O.iterdir()) if p.is_file()]
cl=put('closed-RAW-manifest103.native.json',{'kind':'closed-API-identity-overlay103','inputs':inputs,'owned_artifacts':owned,'self_hash_policy':'Manifest excludes itself; exact RAW reported separately.','topology_self_validated':False})
for f in inputs+owned:assert ref(f['path'])==f
print(json.dumps({'overlay':ov,'closure':cl},indent=2))
