from pathlib import Path
import json,hashlib,os,sys,subprocess,datetime,importlib.util,re
ROOT=Path('E:/Samplinglib')
OWN=ROOT/'runs/20261007-companion-priority/pbps-harmonic-flow-sourcegraph73'
OLD=ROOT/'runs/20261007-companion-priority/pbps-half-turn-construction-preread73'
PY='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
def sha(b): return hashlib.sha256(b).hexdigest()
def canonical(j): return json.dumps(j,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def write(n,j):
    assert not (OWN/'lease.final.json').exists(),'CLOSED_LAST'
    (OWN/n).write_bytes(j if isinstance(j,bytes) else (json.dumps(j,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode('utf-8'))
def read(p): return json.loads(p.read_text('utf-8'))
def pin(p):
    b=p.read_bytes(); return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n')),'lf_recipe':'CRLF byte pair -> LF only; preserve bare CR/every other byte'}
def compatible(row,now): return all(row[k]==now[k] for k in ['path','bytes','raw_sha256','lf_sha256'])
def parse():
    sp=importlib.util.spec_from_file_location('closed_source_parser73',OLD/'preread73.py'); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    return m.tree()
def text(n): return re.sub(r'\s+',' ',n.text()).strip()
def freeze():
    lease=read(OLD/'lease.final.json'); assert lease['state']=='CLOSED_LAST' and lease['owned_count_including_lease']==103
    for r in lease['all_files_except_self']: assert compatible(r,pin(ROOT/r['path'])),r['path']
    assert sha(canonical(lease['all_files_except_self']))==lease['closure_sha256']
    run=read(OLD/'run.json'); rh=run.pop('run_sha256'); assert sha(canonical(run))==rh
    assert compatible(run['complete_named_payload'],pin(ROOT/run['complete_named_payload']['path']))
    originals=read(OLD/'inputs.manifest.json')['inputs']; maps=[]
    for i,r in enumerate(originals):
        now=pin(ROOT/r['path']); assert compatible(r,now),r['path']
        maps.append({'index':i,'original_authority':pin(OLD/'inputs.manifest.json'),'original_input_reference':r,'current_input':now,'resolution':'EXACT_CURRENT_RAW_AND_CRLF_ONLY_LF_EQUALITY','historical_fallback':False})
    assert len(maps)==21
    names=['lease.final.json','run.json','complete-named-source-first-review.payload.json','inputs.manifest.json','selected-contract.json','source-expectations.json','source.regions.json','construction.formula-spans.json','api.regions.json','api.statement-regions.json','api.retrieval.json','preread73.py']
    inputs=[pin(OLD/n) for n in names]
    write('inputs.manifest.json',{'input_count':len(inputs),'inputs':inputs,'referenced_old_input_count':21,'old_input_version_map':'old21.version-map.json','no_recursive_package_or_source_snapshot_copy':True})
    write('old21.version-map.json',{'row_count':21,'rows':maps,'recipe':'finite exact current vs frozen RAW/LF check for EACH old input; no wildcard/exclusion or current-only fallback'})
    write('closed103.reference-validation.json',{'pid':os.getpid(),'source_scope':OLD.relative_to(ROOT).as_posix(),'state':'CLOSED_LAST','old_owned_count':103,'verified_native_nonself_rows':len(lease['all_files_except_self']),'closure_sha256':lease['closure_sha256'],'lease':pin(OLD/'lease.final.json'),'whole_logical_run_sha256':rh,'complete_named_payload':pin(OLD/'complete-named-source-first-review.payload.json'),'all_native_files_exact':True,'all21_old_inputs_exact_current':True,'old_native_byte_writes':0,'old_scope_has_complete_spg':False,'qualification':'CLOSED103 was planning only; this separate StageA completes the selected-edge source proof graph uncertainty.'})
    write('lease.open.json',{'state':'OPEN','actor':'/root/exact_science63','scope':OWN.relative_to(ROOT).as_posix(),'task':'independent source-first StageA73, selected actual_harmonic_flow_laws graph and binders only','owner_header_or_implementation_consumed':False,'proof_search':False,'compiler_run':False,'canonical_git_ledger_goal_writes':False})
    b,s,t=parse(); roots=read(OLD/'source.regions.json')['regions']; out=[]
    byid={n.a.get('id'):n for n in t.nodes if n.a.get('id')}
    def atoms(n):
        if n.tag=='math' or n.tag in ['p','table','figcaption','h6'] or 'ltx_listingline' in n.a.get('class',''): return [n]
        children=[c for c in n.children if not isinstance(c,str)]
        if not children: return [n] if text(n) else []
        return [v for c in children for v in atoms(c)]
    for region in roots:
        n=byid[region['source_id']]
        blocks=[]
        for k,a in enumerate(atoms(n)):
            if not text(a): continue
            lo=len(s[:a.start].encode('utf-8')); hi=len(s[:a.end].encode('utf-8')); q=b[lo:hi]
            blocks.append({'block_id':a.a.get('id') or region['source_id']+f'::block{k}','tag':a.tag,'raw_byte_start_inclusive':lo,'raw_byte_end_exclusive':hi,'literal_span_raw_sha256':sha(q),'bytes':len(q),'readview':text(a)})
        out.append({'source_id':region['source_id'],'whole_region_raw_sha256':region['literal_span_raw_sha256'],'raw_byte_start_inclusive':region['raw_byte_start_inclusive'],'raw_byte_end_exclusive':region['raw_byte_end_exclusive'],'blocks':blocks})
    write('source.blocks.json',{'source_primary':maps[0]['current_input'],'interval_recipe':'0-based RAW UTF8 bytes, inclusive start/exclusive end; block hashes are literal source bytes','region_count':len(out),'block_count':sum(len(x['blocks']) for x in out),'regions':out,'no_duplicate_source_snapshot_copy':'source bytes remain in fixed primary and CLOSED103 exact region snapshots; direct finite interval pins are sufficient'})
    for r in out:
        print('REGION',r['source_id'])
        for v in r['blocks']: print(v['block_id'],v['tag'],v['readview'])
    print(json.dumps({'pid':os.getpid(),'old_native_rows_verified':102,'old_inputs':21,'new_authority_inputs':len(inputs),'regions':len(out),'blocks':sum(len(x['blocks']) for x in out)}))
def runner(label,mode):
    assert not (OWN/'lease.final.json').exists()
    write(label+'.executed-helper.RAW.py',(OWN/'stageA73.py').read_bytes())
    cmd=[PY,'-B','-X','utf8',str(OWN/'stageA73.py'),mode]; start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    with (OWN/(label+'.stdout.log')).open('wb') as out,(OWN/(label+'.stderr.log')).open('wb') as err:
        p=subprocess.Popen(cmd,cwd=ROOT,stdout=out,stderr=err); print(json.dumps({'runner_pid':os.getpid(),'pid':p.pid,'command':cmd}),flush=True); ec=p.wait()
    receipt={'runner_pid':os.getpid(),'pid':p.pid,'exit_code':ec,'terminal_closed':True,'started_utc':start,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'stdout':pin(OWN/(label+'.stdout.log')),'stderr':pin(OWN/(label+'.stderr.log'))}
    write(label+'.receipt.json',receipt); print(json.dumps(receipt),flush=True); sys.exit(ec)
if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='run': runner(sys.argv[2],sys.argv[3])
    elif mode=='freeze': freeze()
