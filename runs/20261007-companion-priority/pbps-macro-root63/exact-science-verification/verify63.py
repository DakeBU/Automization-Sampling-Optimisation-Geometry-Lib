from pathlib import Path
import hashlib, json, os, re, subprocess, sys, time, shutil

ROOT = Path('E:/Samplinglib')
RUN = ROOT / 'runs/20261007-companion-priority/pbps-macro-root63'
OUT = RUN / 'exact-science-verification'
SCI = '4d02622332d02d0bd6c977d3cee48fd535ebf203'
PARENT = '44dc6d6f744e76b86df88cfde1926552dff12cf5'
ACTOR = '/root/exact_science63'
PY = 'C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
MAIN = 'AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicDefectRoot.lean'
TEST = 'Tests/ProximalBPSMacroscopicDefectRoot.lean'
DECL = 'AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicDefectRoot.actual_unique_positive_macroscopic_defect_root'
CELL = 'ASTIS-SW-PBPS-unique-macroscopic-defect-root'
ADV = 'ASTIS-SA-20261009-PBPSUniqueMacroscopicDefectRoot'

def sha(b): return hashlib.sha256(b).hexdigest()
def compact(x): return json.dumps(x, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()
def read(p): return json.loads(Path(p).read_bytes().decode('utf-8-sig'))
def write(name,x):
    p=OUT/name; p.parent.mkdir(parents=True,exist_ok=True)
    p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()); return p
def pin(p):
    p=Path(p); b=p.read_bytes(); lf=b.replace(b'\r\n',b'\n')
    return {'path':p.as_posix(),'raw_bytes':len(b),'raw_sha256':sha(b),'lf_bytes':len(lf),'lf_sha256':sha(lf)}
def git(*args): return subprocess.check_output(['git',*args],cwd=ROOT).decode().strip()
def strings(x):
    if isinstance(x,str): yield x
    elif isinstance(x,list):
        for v in x: yield from strings(v)
    elif isinstance(x,dict):
        for v in x.values(): yield from strings(v)
def aspath(s):
    if not isinstance(s,str) or '\n' in s or len(s)>500: return None
    s=s.replace('\\','/')
    if ':' in s[3:] or s.startswith(('_site/', 'http')): return None
    if s.startswith('E:/Samplinglib/'): p=Path(s)
    elif s.startswith(('runs/','research-wiki/','AutoSamplingTheory/','Tests/','website/','proof-obligations/','Libraries/','.astis/','docs/','tools/')) or s in ('lean-toolchain','lake-manifest.json','lakefile.lean','AGENTS.md'): p=ROOT/s
    else: return None
    return p if p.is_file() else None
def freeze():
    OUT.mkdir(parents=True,exist_ok=True)
    assert git('rev-parse','HEAD')==SCI
    assert git('rev-parse',SCI+'^')==PARENT
    write('lease.json',{'schema_version':1,'actor_id':ACTOR,'state':'OPEN','exact_commit':SCI,'opened_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'actual_pid':os.getpid(),'owned_prefix':OUT.as_posix(),'authorized_shared_write':'independent VERIFIED transition only'})
    paths={ROOT/p for p in [MAIN,TEST,'lean-toolchain','lake-manifest.json','lakefile.lean','AGENTS.md','docs/contributor-codex-contract.md','docs/theorem-publication-protocol.md','docs/proof-digestion-protocol.md','docs/evidence-routed-memory-protocol.md','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','runs/substantive_advances.jsonl','runs/substantive_discoveries.jsonl','tools/astis_advance.py','tools/astis_publication.py','tools/astis_contributor_contract.py','tools/astis_semantic_roundtrip.py','tools/astis_frontier_cells.py','tools/astis.py']}
    for p in RUN.rglob('*'):
        if p.is_file() and OUT not in p.parents and not any(v.startswith(('push-science','pr315-update','commit-science','remote-int62')) for v in p.relative_to(RUN).parts): paths.add(p)
    for p in git('diff','--name-only',PARENT,SCI).splitlines():
        q=ROOT/p
        if q.is_file(): paths.add(q)
    todo=list(paths); visited=set()
    while todo:
        p=todo.pop()
        if p in visited: continue
        visited.add(p)
        if p.suffix=='.json' and ('pbps-macro-root63' in p.parts or 'pbps-macro-root-preproof63' in p.parts):
            try: refs=list(strings(read(p)))
            except Exception: refs=[]
            for s in refs:
                q=aspath(s)
                if q and OUT not in q.parents and '_site' not in q.parts and q not in paths: paths.add(q); todo.append(q)
        if p.suffix=='.lean' and ('AutoSamplingTheory' in p.parts or p==ROOT/TEST):
            for mod in re.findall(r'^import\s+(\S+)',p.read_text(encoding='utf-8'),re.M):
                q=ROOT/(mod.replace('.','/')+'.lean')
                if q.is_file() and q not in paths: paths.add(q); todo.append(q)
    trees={}
    for line in git('ls-tree','-r',SCI).splitlines():
        info,name=line.split('\t',1); trees[name]=info.split()[2]
    rows=[]
    for i,p in enumerate(sorted(paths)):
        row=pin(p); snap=OUT/'inputs.v2'/f'{i:04}.exactraw.snapshot'; snap.parent.mkdir(exist_ok=True)
        snap.write_bytes(p.read_bytes()); assert sha(snap.read_bytes())==row['raw_sha256']
        row['exact_raw_snapshot']=snap.as_posix()
        rel=p.relative_to(ROOT).as_posix()
        row['git_blob_at_science']=trees.get(rel)
        rows.append(row)
    write('input.manifest.json',{'actor_id':ACTOR,'actual_pid':os.getpid(),'exact_commit':SCI,'actual_parent':PARENT,'git_tree':git('rev-parse',SCI+'^{tree}'),'git_status':git('status','--porcelain'),'frozen_before_own_compiler':True,'input_artifacts':rows})
    print(json.dumps({'status':'INPUTS_FROZEN_BEFORE_OWN_COMPILER','actual_pid':os.getpid(),'files':len(rows),'bytes':sum(r['raw_bytes'] for r in rows),'commit':SCI,'parent':PARENT}))
def summarize():
    for name in ['math-freeze.json','math-freeze.presentation-supplement-v2.json','preproof-admission.json','proved-local.json','exposition.draft.json','source.0.review.root-adapter.json']:
        x=read(RUN/name); print(name, list(x.keys()))
    for sub,name in [('independent-math63','run.json'),('independent-source63','run.json'),('anonymous-decoder','native.run.json')]:
        x=read(RUN/sub/name); print(sub,list(x.keys()))
    print('tracked_changed_production',[p for p in git('diff','--name-only',PARENT,SCI).splitlines() if not p.startswith('runs/')])
def assert_frozen():
    rows=read(OUT/'input.manifest.json')['input_artifacts']; changes=[]
    for row in rows:
        p=Path(row['path'])
        expected=row['raw_sha256']
        if p==ROOT/'runs/substantive_advances.jsonl' and (OUT/'transition.result.json').exists():expected=read(OUT/'transition.result.json')['after_ledger_pin']['raw_sha256']
        if sha(p.read_bytes())!=expected: changes.append(row['path'])
    assert not changes,changes
    assert git('rev-parse','HEAD')==SCI
    return {'exact_commit':SCI,'checked_input_artifacts':len(rows),'all_raw_bytes_unchanged':True,'actual_pid':os.getpid()}
def capture(label,args):
    write(label+'.pre.json',assert_frozen())
    started=time.time()
    with (OUT/(label+'.stdout.log')).open('wb') as stdout, (OUT/(label+'.stderr.log')).open('wb') as stderr:
        p=subprocess.Popen(args,cwd=ROOT,stdout=stdout,stderr=stderr)
        print(json.dumps({'foreground_command':args,'actual_pid':p.pid}),flush=True)
        rc=p.wait()
    post=assert_frozen()
    result={'actor_id':ACTOR,'parent_pid':os.getpid(),'actual_pid':p.pid,'argv':args,'cwd':ROOT.as_posix(),'started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(started)),'finished_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'elapsed_seconds':time.time()-started,'exit_code':rc,'foreground':True,'nonforced':True,'exact_commit':SCI,'post_pin':post,'stdout':pin(OUT/(label+'.stdout.log')),'stderr':pin(OUT/(label+'.stderr.log'))}
    write(label+'.receipt.json',result)
    print(json.dumps({'label':label,'exit_code':rc,'actual_pid':p.pid,'elapsed_seconds':result['elapsed_seconds']}),flush=True)
    return result
def compiler():
    assert not (OUT/'focused.receipt.json').exists(),'one build only'
    assert (ROOT/'lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0'
    mf=read(ROOT/'lake-manifest.json'); mathlib=next(p for p in mf['packages'] if p['name']=='mathlib')
    actual=subprocess.check_output(['git','-C',str(ROOT/'.lake/packages/mathlib'),'rev-parse','HEAD']).decode().strip()
    assert actual==mathlib['rev']
    write('runtime.pin.json',{'lean_toolchain':pin(ROOT/'lean-toolchain'),'lake_manifest':pin(ROOT/'lake-manifest.json'),'mathlib_manifest_rev':mathlib['rev'],'mathlib_actual_rev':actual,'lake_executable':shutil.which('lake'),'python_executable':sys.executable,'actual_pid':os.getpid()})
    r=capture('focused',[shutil.which('lake'),'build','Tests.ProximalBPSMacroscopicDefectRoot'])
    assert r['exit_code']==0
    out=(OUT/'focused.stdout.log').read_text(encoding='utf-8')
    ax=re.findall(r"'([^']+)' depends on axioms: \[([^\]]+)\]",out)
    standard={'propext','Classical.choice','Quot.sound'}
    required={DECL,'Tests.ProximalBPSMacroscopicDefectRoot.genuine_actual_macroscopic_root_consumer'}
    found={name:set(v.strip() for v in v.split(',')) for name,v in ax}
    assert required<=found.keys(),found.keys()
    assert all(found[n]==standard for n in required),found
    jobs=re.findall(r'Build completed successfully \((\d+) jobs\)',out)
    assert jobs==['3920'],jobs
    write('focused.result.json',{'status':'PASS','exact_commit':SCI,'jobs':3920,'target_axioms':{n:sorted(found[n]) for n in required},'zero_private_providers':True,'nonforced_build_count':1,'compiler_actual_pid':r['actual_pid']})
    print('PASS exact SCI63 focused3920 both targets standard3')
def gates():
    specs=[('publication.packet',[PY,'-X','utf8','tools/astis_publication.py','packet','--cell',CELL]),('publication.diff',[PY,'-X','utf8','tools/astis_publication.py','check','--base',PARENT]),('contributor.diff',[PY,'-X','utf8','tools/astis_contributor_contract.py','check','--base',PARENT]),('semantic',[PY,'-X','utf8','tools/astis_semantic_roundtrip.py','check']),('frontier.metadata',[PY,'-X','utf8','tools/astis_frontier_cells.py','check'])]
    results=[capture(label,args) for label,args in specs]
    finishgates()
def finishgates():
    results=[read(OUT/(label+'.receipt.json')) for label in ['publication.packet','publication.diff','contributor.diff','semantic','frontier.metadata']]
    sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tools'))
    from tools import astis,astis_publication as pub
    scan=astis.forbidden_pattern_hits()
    write('fakeclosure.result.json',{'exact_commit':SCI,'repository_forbidden_pattern_hits':scan,'focused_files':[pin(ROOT/MAIN),pin(ROOT/TEST)],'private_provider_inventory':[],'standard_axioms_evidence':'focused.result.json','status':'PASS' if not scan else 'FAIL'})
    pub.check_advance([DECL],reviewed=True)
    write('publication.reviewed.result.json',{'status':'PASS','exact_commit':SCI,'declarations':[DECL],'reviewed':True,'function':'tools.astis_publication.check_advance'})
    write('gates.result.json',{'exact_commit':SCI,'results':[{k:r[k] for k in ['argv','exit_code','actual_pid']} for r in results],'fakeclosure_status':'PASS' if not scan else 'FAIL','reviewed_publication_status':'PASS','full_repository_gate_run':False,'site_rebuild_run':False})
    print('Scoped gates captured; read exact exit codes in gates.result.json')
def drift():
    rows=read(OUT/'input.manifest.json')['input_artifacts']
    print(json.dumps([{'original':r,'current':pin(Path(r['path']))} for r in rows if sha(Path(r['path']).read_bytes())!=r['raw_sha256']],ensure_ascii=False))
if __name__=='__main__':
    {'freeze':freeze,'summarize':summarize,'compiler':compiler,'gates':gates,'finishgates':finishgates,'drift':drift}[sys.argv[1]]()
