from verify63 import *

history={}; history_rows=[]; checked=[]; failures=[]
def absolute(s):
    p=Path(s); return p if p.is_absolute() else ROOT/p
def add(original,snapshot,authority):
    if isinstance(snapshot,dict): snapshot=snapshot['path']
    p=absolute(snapshot); b=p.read_bytes(); assert sha(b)==original['raw_sha256'],(authority,original,p)
    if 'lf_sha256' in original: assert sha(b.replace(b'\r\n',b'\n'))==original['lf_sha256']
    key=(str(absolute(original['path']).resolve()).lower(),original['raw_sha256'])
    if key in history: assert history[key].read_bytes()==b
    history[key]=p;history_rows.append({'original':original,'explicit_raw_snapshot':p.as_posix(),'authority':authority})

for fn,key,skey in [
    ('root.math63.adoption.json','exact_historical_negative_resolutions','exact_recorded_raw_snapshot'),
    ('root.decoder63.adoption.json','raw_snapshot_mappings','exact_raw_snapshot'),
    ('root.source63.adoption.json','qualified_historical_resolutions','exact_snapshot'),
    ('math-freeze.presentation-supplement-v2.json','qualified_original58_history','exact_raw_snapshot'),
    ('presentation-step3-repair63/root.presentation-repair63.json','raw_snapshot_mappings','exact_raw_snapshot'),
    ('preproof-admission.json','effective_negative_history_resolutions','exact_historical_snapshot')]:
    for row in read(RUN/fn)[key]:add(row['original'],row[skey],fn+':'+key)
for original,snapshot in [
    ('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSUniquePositiveMacroscopicDefectRoot.json','audit.0.before-source-admission.raw.snapshot.json'),
    ('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSUniquePositiveMacroscopicDefectRoot.json','audit.0.before-decoder.raw.snapshot.json'),
    ('research-wiki/frontier-cells/ASTIS-SW-PBPS-unique-macroscopic-defect-root.json','cell.0.before-proved.raw.snapshot.json')]:
    p=RUN/snapshot;row=pin(p);row['path']=(ROOT/original).as_posix();add(row,p.as_posix(),'explicit lifecycle snapshot '+snapshot)

seen=set()
def check_pin(row,authority):
    p=absolute(row['path']); span='start_line' in row and 'end_line' in row
    key=(str(p.resolve()).lower(),row.get('start_line'),row.get('end_line'),row['raw_sha256'])
    if key in seen:return
    effective=history.get((str(p.resolve()).lower(),row['raw_sha256']),p)
    try:
        whole=effective.read_bytes();b=b''.join(whole.splitlines(keepends=True)[row['start_line']-1:row['end_line']]) if span else whole
        assert sha(b)==row['raw_sha256'],f'digest mismatch {p}'
        lf=b.replace(b'\r\n',b'\n')
        if 'lf_sha256' in row: assert sha(lf)==row['lf_sha256'],f'LF mismatch {p}'
        for k,n in [('bytes',len(b)),('raw_bytes',len(b)),('lf_bytes',len(lf))]:
            if k in row:assert row[k]==n,f'length mismatch {p}'
        checked.append({'authority':authority,'original':row,'effective_exact_bytes':effective.as_posix(),'mode':'literal-line-span' if span else 'whole-file','historical_explicit_mapping':effective!=p});seen.add(key)
    except Exception as e:failures.append({'authority':authority,'pin':row,'error':str(e)})
def walk(x,authority):
    if isinstance(x,dict):
        if {'path','raw_sha256'}<=x.keys():check_pin(x,authority)
        for v in x.values():walk(v,authority)
    elif isinstance(x,list):
        for v in x:walk(v,authority)

natives=[('independent-math63','run.json','named-mathematics.payload.json','f8ea8bdcb3455d251047f5a24c608a700b25bdfc9190ac82148a8de92c594be6','1eca96b379d0da483409e761e7c4a86b71524ed1585db566d45c7a66b8e82d64'),('independent-source63','run.json','review.payload.json','32b39c9148d59120ba67a632e836ea203a7d8c8477703c27a9c774886857b2e5','ab7dea212533a86af87d609044db50c7ef14366cce652963aa262c2936fa2a01'),('anonymous-decoder','native.run.json','decoded.payload.json','3b1928ff12fd5ab82215efd237c8144b032e46dcf07b4fe35cf8b002cdf0ecce','78d9c4093240fd7dc550f8bb262da49d751b5f3fc31999e07187147850099710')]
native_results=[]
for sub,runfn,payloadfn,runhash,payloadhash in natives:
    d=RUN/sub;x=read(d/runfn);assert x['run_sha256']==runhash
    whole={k:v for k,v in x.items() if k!='run_sha256'};assert sha(compact(whole))==runhash
    assert sha((d/payloadfn).read_bytes())==payloadhash and payloadhash!=runhash
    lease=read(d/'lease.json');assert lease.get('status') in ['CLOSED','CLOSED_LAST']
    output_count=0
    for key in ['complete_owned_outputs','owned_artifacts']:
        for name,digest in lease.get(key,{}).items():assert sha((d/name).read_bytes())==digest;output_count+=1
    if (d/'output.manifest.json').exists():
        manifest=read(d/'output.manifest.json')
        for row in manifest.get('artifacts',[]):check_pin(row,sub+'/output.manifest.json');output_count+=1
        for name,digest in manifest.get('owned_outputs',{}).items():assert sha((d/name).read_bytes())==digest;output_count+=1
    if (d/'proposed-lease.closed.json').exists():assert (d/'lease.json').read_bytes()==(d/'proposed-lease.closed.json').read_bytes()
    for p in d.rglob('*.json'):walk(read(p),p.relative_to(ROOT).as_posix())
    native_results.append({'actor':lease.get('owner',lease.get('reviewer',sub)),'native_directory':sub,'whole_logical_run_sha256':runhash,'distinct_complete_named_RAW_payload_sha256':payloadhash,'bound_output_pin_count':output_count,'closed_status':lease['status']})
for name in ['math-freeze.json','math-freeze.presentation-supplement-v2.json','root.math63.adoption.json','root.decoder63.adoption.json','root.source63.adoption.json','source.0.review.root-adapter.json','proved-local.json','preproof-admission.json']:
    walk(read(RUN/name),name)

primary=read(RUN/'independent-source63/primary-only.input.manifest.json');source=absolute(primary['source_primary']['path']).read_bytes();assert sha(source)==primary['source_primary']['raw_sha256']
for row in primary['primary_regions']:
    a,b=row['byte_range'];data=source[a:b];assert data==Path(row['raw_path']).read_bytes() and sha(data)==row['raw_sha256'];assert data.replace(b'\r\n',b'\n')==Path(row['lf_path']).read_bytes()
assert len(primary['primary_regions'])==24
headers=[]
for path,headername in [(ROOT/MAIN,'header0.lean'),(ROOT/TEST,'header1.lean')]:
    b=path.read_bytes();start=b.index(b'theorem ');end=b.index(b':= by',start)
    delimiter_space_excluded=b[end-1:end]==b' '
    if delimiter_space_excluded:end-=1
    actual=b[start:end].rstrip(b'\n');sealed=(RUN.parent/'pbps-macro-root-preproof63'/headername).read_bytes().rstrip(b'\n')
    assert actual==sealed,(path,'sealed header mismatch')
    headers.append({'source':pin(path),'sealed_header':pin(RUN.parent/'pbps-macro-root-preproof63'/headername),'body_delimiter_single_space_excluded':delimiter_space_excluded,'literal_equal_ignoring_only_trailing_LF':True})

lesson=read(ROOT/'website/content/declaration_lessons/pbps-unique-positive-macroscopic-defect-root.json')
steps=[]
def stepwalk(x):
    if isinstance(x,dict):
        if 'lean_source_region' in x and 'lean' in x:
            row=x['lean_source_region'];p=absolute(row['path']);b=p.read_bytes();span=b''.join(b.splitlines(keepends=True)[row['start_line']-1:row['end_line']]);assert sha(b)==row['source_raw_sha256'];assert sha(span)==row['exact_code_raw_sha256'];assert span==x['lean'].encode();steps.append({'title':x['title'],'region':row,'literal_match':True})
        for v in x.values():stepwalk(v)
    elif isinstance(x,list):
        for v in x:stepwalk(v)
stepwalk(lesson);assert len(steps)==8
result={'status':'PASS' if not failures else 'BLOCKED_BINDING','exact_commit':SCI,'native_runs':native_results,'qualified_pin_readbacks':len(checked),'finite_explicit_history_maps':history_rows,'checked_pins':checked,'unresolved':failures,'source_raw_regions':24,'sealed_headers':headers,'eight_literal_formula_steps':steps,'arbitrary_fallback_used':False,'native_CLOSED_artifacts_written':False}
write('bindings.result.json',result)
print(json.dumps({'status':result['status'],'qualified_pin_readbacks':len(checked),'finite_maps':len(history_rows),'unresolved':failures[:10],'native_runs':native_results},ensure_ascii=False))
assert not failures,'exact artifact binding failures'
