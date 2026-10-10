from pathlib import Path
import ctypes, datetime, hashlib, json, os, re, subprocess, sys, traceback

ROOT=Path('E:/Samplinglib')
R72=ROOT/'runs/20261007-companion-priority/pbps-b4-corrector-perturbation72'
OWN=R72/'exact-science-verification72'
COMMIT='18183c58eee62145b6059ded11c7be05a4cb82de'
PARENT='1e9d2feb727919ebaa17ee1a67b629a0b85b0ba9'
SAU='ASTIS-SA-20261010-PBPSActualCorrectorPerturbation'
ACTOR='/root/header_math72'
PY=Path('C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe')
sys.path[:0]=[str(ROOT),str(ROOT/'tools')]
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1')

def sha(b): return hashlib.sha256(b).hexdigest()
def canon(j): return json.dumps(j,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')
def load(p): return json.loads(Path(p).read_bytes())
def save(n,j):
    p=OWN/n;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_bytes((json.dumps(j,ensure_ascii=False,indent=2,sort_keys=True,allow_nan=False)+'\n').encode('utf-8'))
def pin(p):
    p=Path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n')
    return {'path':p.as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(l),'LF_sha256':sha(l)}
def command(label,args,env=None,stdout_snapshot=None):
    assert not (OWN/'terminals'/str(label+'.receipt.json')).exists(),'receipt label already exists; preserve history'
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    proc=subprocess.Popen([str(x) for x in args],cwd=ROOT,env=env or ENV,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    print(json.dumps({'START':label,'actual_PID':proc.pid,'driver_PID':os.getpid()}),flush=True)
    out,err=proc.communicate()
    on=stdout_snapshot or ('terminals/'+label+'.stdout.RAW')
    op=OWN/on;op.parent.mkdir(parents=True,exist_ok=True);op.write_bytes(out)
    ep=OWN/'terminals'/str(label+'.stderr.RAW');ep.parent.mkdir(parents=True,exist_ok=True);ep.write_bytes(err)
    receipt={'label':label,'command':[str(x) for x in args],'actual_PID':proc.pid,'driver_PID':os.getpid(),
             'terminal_EXIT':proc.returncode,'started_UTC':start,'finished_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'stdout':pin(op),'stderr':pin(ep),'terminal_closed':True}
    save('terminals/'+label+'.receipt.json',receipt)
    print(json.dumps({'END':label,'actual_PID':proc.pid,'terminal_EXIT':proc.returncode}),flush=True)
    if proc.returncode: raise RuntimeError(label+' failed; retained exact output, no retry or ledger append')
    return out,receipt
def git(label,*args,**kw): return command(label,['git',*args],**kw)
def ledger_rows():
    return [j for line in (ROOT/'runs/substantive_advances.jsonl').read_bytes().splitlines()
            if line.strip() and (j:=json.loads(line)).get('advance_id')==SAU]
def state(rows):
    s=None
    for r in rows:
        if r.get('event')=='propose': s='PROPOSED'
        if r.get('event')=='transition': s=r['to_state']
    return s
def verify_hash(p,raw_hash,raw_size=None,lf_hash=None):
    b=Path(p).read_bytes();assert sha(b)==raw_hash,str(p)
    if raw_size is not None: assert len(b)==raw_size,str(p)
    if lf_hash is not None: assert sha(b.replace(b'\r\n',b'\n'))==lf_hash,str(p)

def freeze():
    OWN.mkdir(parents=True,exist_ok=True)
    save('retained-discovery-errors.json',{'not_gate_failures':True,'not_transition_failures':True,'events':[
        {'command_scope':'initial schema discovery','terminal_EXIT':1,'exact_error':'rg: tools/astis_advance_schema.py: The system cannot find the file specified. (os error 2)','resolution':'read actual tools/astis_advance.py schema; no nonexistent schema used'},
        {'command_scope':'initial gate filename discovery','rg_error':'tools/astis_frontier.py; tools/astis_source_contract.py; tools/astis_contributors.py: The system cannot find the file specified. (os error 2)','enclosing_terminal_EXIT':0,'resolution':'rg --files tools supplied real astis_frontier_cells.py, astis_source.py, astis_contributor_contract.py'}]})
    d=load(R72/'exact-verification.dispatch72.json')
    assert d['checked_commit']==COMMIT and d['parent']==PARENT and d['advance_id']==SAU and d['verifier']==ACTOR
    assert d['unique_VERIFIED_transition_authorized_after_independent_checks'] is True
    assert len(d['inputs'])==21
    (OWN/'dispatch.exactRAW.json').write_bytes((R72/'exact-verification.dispatch72.json').read_bytes())
    head,_=git('head-before','rev-parse','HEAD');assert head.decode().strip()==COMMIT
    par,_=git('parent-before','rev-parse',COMMIT+'^');assert par.decode().strip()==PARENT
    records=[]
    for i,item in enumerate(d['inputs']):
        path=ROOT/item['path'];raw=path.read_bytes()
        verify_hash(path,item['RAW_sha256'],item['RAW_bytes'],item['LF_sha256'])
        blob,receipt=git('git-show-'+str(i).zfill(2),'show',COMMIT+':'+item['path'],stdout_snapshot='inputs/'+str(i).zfill(2)+'.git-exactRAW.snapshot')
        exact=raw==blob;lf_only=raw.replace(b'\r\n',b'\n')==blob.replace(b'\r\n',b'\n')
        assert exact or (item['path'] in ['lean-toolchain','lake-manifest.json'] and lf_only),item['path']
        records.append({'input':item,'git_blob':pin(OWN/('inputs/'+str(i).zfill(2)+'.git-exactRAW.snapshot')),
                        'git_show_PID':receipt['actual_PID'],'git_show_terminal_EXIT':receipt['terminal_EXIT'],
                        'workspace_git_RAW_equal':exact,'CRLF_to_LF_only_equal':lf_only,
                        'allowed_nonRAW_equivalence':not exact and item['path'] in ['lean-toolchain','lake-manifest.json']})
    parentfile='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean'
    b,receipt=git('parent71-exact-source','show',PARENT+':'+parentfile,stdout_snapshot='inputs/parent71.git-exactRAW.lean')
    assert b==(ROOT/parentfile).read_bytes()
    rows=ledger_rows();assert state(rows)=='PROVED_LOCAL'
    assert not any(r.get('to_state')=='VERIFIED' for r in rows)
    save('ledger-before.target-only.json',{'rows':rows,'state':'PROVED_LOCAL','global_ledger':pin(ROOT/'runs/substantive_advances.jsonl')})
    save('inputs21.git-workspace.manifest.json',{'checked_commit':COMMIT,'parent':PARENT,'exact_git_show':True,'records':records,
         'parent71_reuse':{'path':parentfile,'commit':PARENT,'pin':pin(OWN/'inputs/parent71.git-exactRAW.lean'),'workspace_RAW_equal':True},
         'dispatch':pin(R72/'exact-verification.dispatch72.json'),'normalization':'ONLY bytewise CRLF -> LF; no other changes permitted'})
    print(json.dumps({'phase':'freeze','inputs':len(records),'status':'PASS'}))

def native():
    records=[]
    mdir=R72/'independent-math72';ml=load(mdir/'lease.final.json');ma=load(R72/'root.math72.adoption.json')
    verify_hash(mdir/'lease.final.json',ma['native_lease_RAW_sha256'])
    ents=ml['all_owned_outputs_except_only_self'];assert len(ents)+1==ma['native_files']==82
    for e in ents: verify_hash(e['path'],e['RAW_sha256'],e['RAW_bytes'],e['LF_sha256'])
    actual={p.resolve().as_posix() for p in mdir.rglob('*') if p.is_file()}
    expect={Path(e['path']).resolve().as_posix() for e in ents}|{(mdir/'lease.final.json').resolve().as_posix()}
    assert actual==expect
    mr=load(mdir/'run.json');mh=mr.pop('run_sha256');assert sha(canon(mr))==mh==ma['native_whole_logical_run_sha256']
    for e in ma['fresh_compilers']:
        assert e['exit_code']==0 and e['fresh_source_elaboration'] and not e['Lake_cache_replay']
        assert set(e['standard_axioms'])=={'propext','Classical.choice','Quot.sound'}
        verify_hash(e['receipt']['path'],e['receipt']['RAW_sha256'],e['receipt']['RAW_bytes'],e['receipt']['LF_sha256'])
    records.append({'kind':'math','owned_files':82,'native_lease':pin(mdir/'lease.final.json'),'native_wholelogical_run_sha256':mh,
                    'fresh_Lean_PID_EXIT':[(e['actual_foreground_PID'],e['exit_code']) for e in ma['fresh_compilers']],
                    'unchanged':True,'proof_review_repeated':False})
    sdir=R72/'independent-source72';sl=load(sdir/'lease.final.json');sa=load(R72/'root.source72.adoption.json')
    verify_hash(ROOT/sa['native_lease']['path'],sa['native_lease']['RAW_sha256'],sa['native_lease']['RAW_bytes'],sa['native_lease']['LF_sha256'])
    sm=load(sdir/sl['manifest_path']);verify_hash(sdir/sl['manifest_path'],sl['manifest_RAW_sha256'])
    assert sha(canon(sm['entries']))==sl['manifest_logical_entries_sha256']==sm['logical_manifest_sha256']
    for e in sm['entries']: verify_hash(sdir/e['path'],e['raw_sha256'],e['raw_bytes'],e['lf_sha256'])
    actual={p.relative_to(sdir).as_posix() for p in sdir.rglob('*') if p.is_file()}
    expect={e['path'] for e in sm['entries']}|{sl['manifest_path'],'lease.final.json'}
    assert actual==expect and len(actual)==sa['native_owned_files']==258
    sr=load(sdir/'source72.run.json');sh=sr.pop('run_sha256');assert sha(canon(sr))==sh==sa['native_whole_logical_run_sha256']
    assert sl['blocking_deltas']==[0,0] and sl['verdicts']==['equivalent-after-elaboration']*2
    verify_hash(ROOT/sa['native_complete_named_RAW']['path'],sa['native_complete_named_RAW']['RAW_sha256'],sa['native_complete_named_RAW']['RAW_bytes'])
    for i in [0,1]:
        decision=load(sdir/f'source.{i}.decision.json')
        assert decision['verdict']=='equivalent-after-elaboration'
    records.append({'kind':'source','owned_files':258,'native_lease':pin(sdir/'lease.final.json'),
                    'native_wholelogical_run_sha256':sh,'blocking_deltas':[0,0],'unchanged':True,'source_review_repeated':False,
                    'complete_named':pin(ROOT/sa['native_complete_named_RAW']['path']),'root_adoption':pin(R72/'root.source72.adoption.json')})
    bdir=ROOT/'.astis/decoder-72/independent';bl=load(bdir/'CLOSED_LAST.json');ba=load(R72/'root.decoder72.adoption.json')
    verify_hash(ba['native_lease']['path'],ba['native_lease']['RAW_sha256'],ba['native_lease']['RAW_bytes'])
    assert {p.name for p in bdir.iterdir() if p.is_file()}==set(bl['owned_files']) and len(bl['owned_files'])==5
    for e in bl['sealed_files_except_self']: verify_hash(bdir/e['path'],e['raw_sha256'],e['bytes'],e['lf_sha256'])
    br=load(bdir/'run.json');bh=br.pop('run_sha256');assert sha(canon(br))==bh==ba['native_whole_logical_run_sha256']
    records.append({'kind':'strictblind','owned_files':5,'native_lease':pin(bdir/'CLOSED_LAST.json'),
                    'native_wholelogical_run_sha256':bh,'unchanged':True,'decoder_repeated':False,
                    'original_writer_PID_EXIT':[ba['reported_native_writer_PID'],ba['reported_native_writer_EXIT']],
                    'original_external_readonly_PID_EXIT':[ba['reported_native_external_readonly_PID'],ba['reported_native_external_readonly_EXIT']]})
    save('native-evidence-reuse.json',{'records':records,'status':'PASS','no_native_owned_writes':True})
    print(json.dumps({'phase':'native','counts':[82,258,5],'status':'PASS'}))

def lean():
    envout,_=command('lake-selected-env',['lake','env',str(PY),'-B','-X','utf8','-c',
        "import os,json;print(json.dumps({k:os.environ.get(k,'') for k in ['LEAN_PATH','LEAN_SRC_PATH']}))"])
    prefix,_=command('lean-print-prefix',['lake','env','lean','--print-prefix'])
    exe=Path(prefix.decode().strip())/'bin/lean.exe';assert exe.exists()
    e=dict(ENV,**json.loads(envout));build=OWN/'lean-build';build.mkdir(parents=True,exist_ok=True)
    e['LEAN_PATH']=str(build)+';'+e['LEAN_PATH']
    ver,_=command('pinned-lean-version',[exe,'--version'],env=e)
    assert '4.33.0' in ver.decode()
    plan=load(R72/'publication-plan.json');receipts=[]
    for i,module in enumerate(load(R72/'proved-local.json')['lean_files']):
        dest=build/Path(module).with_suffix('.olean');dest.parent.mkdir(parents=True,exist_ok=True)
        out,rec=command('fresh-lean'+str(i),[exe,'-o',dest,ROOT/module],env=e)
        txt=out.decode('utf-8');decl=plan['mathematical_declarations'][i]
        lines=[line for line in txt.splitlines() if 'depends on axioms:' in line]
        assert len(lines)==1 and decl in lines[0]
        axioms=re.search(r'depends on axioms:\s*\[([^]]*)\]',txt,re.S)
        assert axioms and {x.strip() for x in axioms.group(1).split(',')}=={'propext','Classical.choice','Quot.sound'}
        receipts.append({'declaration':decl,'file':module,'actual_lean_PID':rec['actual_PID'],'terminal_EXIT':0,
                         'fresh_source_elaboration':True,'cache_replay':False,'standard_axioms_only':True,
                         'owned_output_olean':pin(dest),'receipt':pin(OWN/('terminals/fresh-lean'+str(i)+'.receipt.json'))})
    save('fresh-lean-exact72.json',{'checked_commit':COMMIT,'toolchain':pin(ROOT/'lean-toolchain'),'manifest':pin(ROOT/'lake-manifest.json'),
          'real_lean_executable':exe.as_posix(),'compiler_binary':pin(exe),'generic_olean_consumed_from_own_fresh_build':True,
          'LEAN_PATH':e['LEAN_PATH'],'results':receipts})
    print(json.dumps({'phase':'lean','status':'PASS','PIDs':[x['actual_lean_PID'] for x in receipts]}))

def metadata():
    plan=load(R72/'publication-plan.json')
    for i,c in enumerate(plan['active_cells']): command('bounded-packet'+str(i),[PY,'-B','-X','utf8','tools/astis_publication.py','packet','--cell',c])
    command('publication-diff-private-inventory',[PY,'-B','-X','utf8','tools/astis_publication.py','check','--base',PARENT])
    command('semantic-roundtrip',[PY,'-B','-X','utf8','tools/astis_semantic_roundtrip.py','check'])
    command('contributor-base',[PY,'-B','-X','utf8','tools/astis_contributor_contract.py','check','--base',PARENT])
    command('focused-source-frontier-fakeclosure',[PY,'-B','-X','utf8',Path(__file__),'focused'])
    command('git-diff-check',['git','diff','--check',PARENT,COMMIT])
    save('metadata-gates.json',{'checked_commit':COMMIT,'status':'PASS','aggregate_root_Tests_site_not_run':True,
          'focused_gates':['two publication packets','publication check --base exact INT71 with private inventory',
          'semantic roundtrip native gate','contributor check --base exact INT71','two exact frontier/source/binding and native fakeclosure APIs','git diff --check parent SCI72']})
    print(json.dumps({'phase':'metadata','status':'PASS'}))

def lean_actual():
    # Diagnosed recovery only. Do not repeat successful generic compilation.
    selected=json.loads((OWN/'terminals/lake-selected-env.stdout.RAW').read_bytes())
    prefix=(OWN/'terminals/lean-print-prefix.stdout.RAW').read_bytes().decode().strip()
    exe=Path(prefix)/'bin/lean.exe';env=dict(ENV,**selected)
    plan=load(R72/'publication-plan.json');modules=load(R72/'proved-local.json')['lean_files']
    oldrec=load(OWN/'terminals/fresh-lean0.receipt.json');assert oldrec['terminal_EXIT']==0
    oldout=(OWN/'terminals/fresh-lean0.stdout.RAW').read_text(encoding='utf-8')
    assert plan['mathematical_declarations'][0] in oldout
    ax=re.search(r'depends on axioms:\s*\[([^]]*)\]',oldout,re.S)
    assert ax and {x.strip() for x in ax.group(1).split(',')}=={'propext','Classical.choice','Quot.sound'}
    native_math=load(R72/'independent-math72/run.json')
    native_source=load(R72/'independent-source72/StageB.current-inputs.manifest.json')
    binds=[]
    for module in modules:
        m=next(x for x in native_math['candidate_files'] if Path(x['path']).resolve()==(ROOT/module).resolve())
        verify_hash(ROOT/module,m['RAW_sha256'],m['RAW_bytes'],m['LF_sha256'])
        s=next(x for x in native_source['inputs'] if x['path']==module)
        verify_hash(ROOT/module,s['raw_sha256'],s['raw_bytes'],s['lf_sha256'])
        binds.append({'module':module,'current':pin(ROOT/module),'closed_math':m,'closed_source':s})
    save('source-code-review-bindings.json',{'status':'PASS','module_bindings':binds,'reviews_not_repeated':True})
    imported=ROOT/'.lake/build/lib/lean'/Path(modules[0]).with_suffix('.olean')
    cache_before=pin(imported)
    dest=OWN/'lean-build'/Path(modules[1]).with_suffix('.olean');dest.parent.mkdir(parents=True,exist_ok=True)
    out,rec=command('fresh-lean1.fixed-searchroots',[exe,'-o',dest,ROOT/modules[1]],env=env)
    assert pin(imported)==cache_before,'canonical imported generic olean changed during fresh actual check'
    txt=out.decode('utf-8');decl=plan['mathematical_declarations'][1]
    assert len([l for l in txt.splitlines() if 'depends on axioms:' in l])==1 and decl in txt
    ax=re.search(r'depends on axioms:\s*\[([^]]*)\]',txt,re.S)
    assert ax and {x.strip() for x in ax.group(1).split(',')}=={'propext','Classical.choice','Quot.sound'}
    generic_dest=OWN/'lean-build'/Path(modules[0]).with_suffix('.olean')
    results=[{'declaration':plan['mathematical_declarations'][0],'file':modules[0],'actual_lean_PID':oldrec['actual_PID'],
              'terminal_EXIT':0,'fresh_source_elaboration':True,'cache_replay':False,'standard_axioms_only':True,
              'owned_output_olean':pin(generic_dest),'receipt':pin(OWN/'terminals/fresh-lean0.receipt.json')},
             {'declaration':decl,'file':modules[1],'actual_lean_PID':rec['actual_PID'],'terminal_EXIT':0,
              'fresh_source_elaboration':True,'cache_replay':False,'standard_axioms_only':True,
              'owned_output_olean':pin(dest),'receipt':pin(OWN/'terminals/fresh-lean1.fixed-searchroots.receipt.json')}]
    save('fresh-lean-exact72.json',{'checked_commit':COMMIT,'toolchain':pin(ROOT/'lean-toolchain'),'manifest':pin(ROOT/'lake-manifest.json'),
          'real_lean_executable':exe.as_posix(),'compiler_binary':pin(exe),'results':results,
          'actual_LEAN_PATH':env['LEAN_PATH'],'generic_current_source':pin(ROOT/modules[0]),
          'actual_imported_canonical_generic_olean':cache_before,'imported_cache_unchanged_during_check':True,
          'fresh_generic_compilation_is_separate':True,'source_code_closed_reviews_binding':pin(OWN/'source-code-review-bindings.json'),
          'diagnosed_failed_setup':{'PID':50632,'EXIT':1,'cause':'sparse top-level namespace search root omitted parent olean',
             'no_mathematical_change':True,'no_successful_gate_repeated':True}})
    print(json.dumps({'phase':'lean_actual','status':'PASS','PIDs':[x['actual_lean_PID'] for x in results]}))

def metadata_finish():
    # Reuse all successful metadata gates; repair only the observer schema lookup.
    command('focused-source-frontier-fakeclosure.fixed-schema',[PY,'-B','-X','utf8',Path(__file__),'focused'])
    command('git-diff-check',['git','diff','--check',PARENT,COMMIT])
    labels=['bounded-packet0','bounded-packet1','publication-diff-private-inventory','semantic-roundtrip','contributor-base',
            'focused-source-frontier-fakeclosure.fixed-schema','git-diff-check']
    for label in labels:assert load(OWN/'terminals'/str(label+'.receipt.json'))['terminal_EXIT']==0
    save('metadata-gates.json',{'checked_commit':COMMIT,'status':'PASS','aggregate_root_Tests_site_not_run':True,
          'accepted_receipt_labels':labels,'accepted_terminal_EXITs':[0]*len(labels),
          'successful_previous_gates_reused_unchanged':True,
          'retained_failed_setup':{'PID':3952,'EXIT':1,'cause':'source review verdict is audit top-level, not inside source_review'},
          'focused_gates':['two publication packets','publication check --base exact INT71 with private inventory',
             'semantic roundtrip native gate','contributor check --base exact INT71','two exact frontier/source/binding and native fakeclosure APIs',
             'git diff --check parent SCI72']})
    print(json.dumps({'phase':'metadata_finish','status':'PASS'}))

def metadata_admit():
    # Frozen exact-RAW evidence has its own pre-existing whitespace exception ledger.
    dp=R72/'whitespace-diagnosis72/diagnosis.json';d=load(dp)
    if (OWN/'terminals/whitespace-diagnosis-exact-git.receipt.json').exists():
        rec=load(OWN/'terminals/whitespace-diagnosis-exact-git.receipt.json')
        assert rec['terminal_EXIT']==0
        raw=(OWN/'terminals/whitespace-diagnosis-exact-git.stdout.RAW').read_bytes()
    else:
        raw,rec=git('whitespace-diagnosis-exact-git','show',COMMIT+':'+dp.relative_to(ROOT).as_posix())
    assert raw==dp.read_bytes()
    lines=(OWN/'terminals/git-diff-check.stdout.RAW').read_bytes().split(b'\n')
    substantive=[];CRonly=0
    for i,line in enumerate(lines):
        m=re.match(rb'(.+):(\d+): (.+)\.$',line)
        if not m:continue
        kind=m.group(3).decode();following=lines[i+1][1:] if i+1<len(lines) and lines[i+1].startswith(b'+') else b''
        if kind=='trailing whitespace' and following.endswith(b'\r') and following[:-1]==following[:-1].rstrip(b' \t'):
            CRonly+=1
        else:substantive.append({'path':m.group(1).decode(),'line':int(m.group(2)),'kind':kind})
    assert substantive==d['findings'] and len(substantive)==335
    allowed={e['path'] for e in d['immutable_native_exceptions']}
    assert {e['path'] for e in substantive}==allowed and len(allowed)==13
    exception_pins=[]
    for i,e in enumerate(d['immutable_native_exceptions']):
        immutable_prefixes=[R72.relative_to(ROOT).as_posix()+'/',
           'runs/20261007-companion-priority/pbps-b4-perturbation-preproof72/independent-header-source72/']
        assert any(e['path'].startswith(p) for p in immutable_prefixes)
        # Hash exact Git bytes in memory: no second copy of large native inputs.
        prior=OWN/'terminals'/str('immutable-exception-'+str(i)+'.receipt.json')
        if prior.exists():
            receipt=load(prior);assert receipt['terminal_EXIT']==0
            assert receipt['stdout_inline_pin']['RAW_sha256']==e['RAW_sha256']
            verify_hash(ROOT/e['path'],e['RAW_sha256'],receipt['stdout_inline_pin']['RAW_bytes'])
            exception_pins.append({'path':e['path'],'RAW_sha256':e['RAW_sha256'],
                'RAW_bytes':receipt['stdout_inline_pin']['RAW_bytes'],'git_PID':receipt['actual_PID'],'git_terminal_EXIT':0,
                'workspace_exact_git_RAW':True,'frozen_native_exception':True,'successful_git_pin_reused':True})
            continue
        start=datetime.datetime.now(datetime.timezone.utc).isoformat()
        proc=subprocess.Popen(['git','show',COMMIT+':'+e['path']],cwd=ROOT,env=ENV,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        b,err=proc.communicate();assert proc.returncode==0
        assert sha(b)==e['RAW_sha256'] and b==(ROOT/e['path']).read_bytes()
        receipt={'label':'immutable-exception-'+str(i),'actual_PID':proc.pid,'terminal_EXIT':proc.returncode,
          'terminal_closed':True,'command':['git','show',COMMIT+':'+e['path']],'started_UTC':start,
          'stdout_inline_pin':{'RAW_sha256':sha(b),'RAW_bytes':len(b)},'stderr_inline_pin':{'RAW_sha256':sha(err),'RAW_bytes':len(err)},
          'reason_no_RAW_copy':'exact original already in native immutable evidence; only finite hash metadata retained'}
        save('terminals/immutable-exception-'+str(i)+'.receipt.json',receipt)
        exception_pins.append({'path':e['path'],'RAW_sha256':sha(b),'RAW_bytes':len(b),'git_PID':proc.pid,'git_terminal_EXIT':0,
          'workspace_exact_git_RAW':True,'frozen_native_exception':True})
    args=['git','-c','core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol','diff','--check',PARENT,COMMIT,'--','.']
    args+=[':(exclude)'+p for p in sorted(allowed)]
    command('git-authored-complement-cr-at-eol',args)
    save('whitespace-exact-native-exception-audit.json',{'status':'PASS_SCOPED_AUTHORED_COMPLEMENT_ONLY','diagnosis':pin(dp),
      'diagnosis_git_show_PID':rec['actual_PID'],'diagnosis_git_RAW_equal':True,'default_full_diff_terminal_EXIT':2,
      'default_raw_negative':pin(OWN/'terminals/git-diff-check.stdout.RAW'),'CR_only_noise_count':CRonly,
      'substantive_findings':substantive,'substantive_count':335,'exact_frozen_exception_files':exception_pins,
      'scoped_authored_terminal_EXIT':0,'full_diff_whitespace_PASS_claimed':False,'no_evidence_normalization':True})
    labels=['bounded-packet0','bounded-packet1','publication-diff-private-inventory','semantic-roundtrip','contributor-base',
            'focused-source-frontier-fakeclosure.fixed-schema','git-authored-complement-cr-at-eol']
    for label in labels:assert load(OWN/'terminals'/str(label+'.receipt.json'))['terminal_EXIT']==0
    save('metadata-gates.json',{'checked_commit':COMMIT,'status':'PASS','aggregate_root_Tests_site_not_run':True,
       'accepted_receipt_labels':labels,'accepted_terminal_EXITs':[0]*len(labels),
       'successful_previous_gates_reused_unchanged':True,'whitespace_exception_audit':pin(OWN/'whitespace-exact-native-exception-audit.json'),
       'full_diff_whitespace_PASS_claimed':False,'default_full_whitespace_negative_retained':True,
       'retained_failed_setup':[{'PID':3952,'EXIT':1,'cause':'audit verdict is top-level'},
                               {'PID':50632,'EXIT':1,'cause':'sparse namespace omitted parent olean'}],
       'focused_gates':['two bounded publication packets','publication --base INT71 private inventory','semantic native gate',
         'contributor --base INT71','two exact source/frontier/fakeclosure checks','authored diff complement with frozen13 exactRAW exceptions']})
    print(json.dumps({'phase':'metadata_admit','status':'PASS','native_whitespace_findings':335,'exceptions':13,'full_diff_PASS':False}))

def focused():
    import astis, astis_publication as pub, astis_frontier_cells as fc, astis_semantic_roundtrip as rt
    plan=load(R72/'publication-plan.json');data=pub.inputs();items=pub.load();decls=plan['mathematical_declarations']
    cells=[load(ROOT/'research-wiki/frontier-cells'/str(c+'.json')) for c in plan['active_cells']]
    errors=fc.validate_cells(cells);assert not errors,errors
    fake=[]
    for path in load(R72/'proved-local.json')['lean_files']:
        clean=astis.strip_lean_comments_and_strings((ROOT/path).read_text(encoding='utf-8'))
        for n,line in enumerate(clean.splitlines(),1):
            if astis.FORBIDDEN_REGEX.search(line):fake.append({'path':path,'line':n,'text':line})
    assert not fake,fake
    source=[]
    registry=rt.load_registry();audits={a['id']:a for a in registry['audits']}
    for i,name in enumerate(decls):
        audit=audits[plan['audit_ids'][i]];assert audit['state']=='source-reviewed'
        item=next(it for it in items if any(b['declaration']==name for b in it['bindings']))
        binding=next(b for b in item['bindings'] if b['declaration']==name)
        digest=pub.binding_digest(item,binding);assert digest==audit['publication_binding_sha256']
        assert audit['verdict']=='equivalent-after-elaboration' and audit['source_review']['state']=='accepted'
        source.append({'declaration':name,'audit_id':audit['id'],'audit_state':audit['state'],'publication_binding_sha256':digest,
                       'reviewer_id':audit['source_review']['reviewer'],'verdict':audit['verdict'],
                       'review_run_sha256':audit['source_review']['review_run_sha256']})
    pub.check_advance(decls,reviewed=True)
    inventory=pub.changed_declarations(PARENT)
    assert set(inventory)==set(decls),list(inventory)
    save('focused-source-frontier-fakeclosure.json',{'status':'PASS','checked_commit':COMMIT,'frontier_cells':plan['active_cells'],
       'source_admissions':source,'fake_closure_hits':fake,'changed_public_declarations':sorted(inventory),
       'private_implementation_inventory':pub.PRIVATE_IMPLEMENTATION_COVERAGE,'source_review_repeated':False,
       'truth_boundary':plan['remaining_boundary']})
    print(json.dumps({'status':'PASS','exact_cells':2,'exact_declarations':2,'source_reviewed_audits':2,'fake_closures':0,
                      'private_inventory':pub.PRIVATE_IMPLEMENTATION_COVERAGE},ensure_ascii=False))

def transition():
    from tools.astis_advance import transition_advance
    assert not (R72/'verified.json').exists(),'verified.json exists: inspect; never append again'
    for n in ['inputs21.git-workspace.manifest.json','native-evidence-reuse.json','fresh-lean-exact72.json','metadata-gates.json','focused-source-frontier-fakeclosure.json']:
        assert (OWN/n).exists(),n
    rows=ledger_rows();assert state(rows)=='PROVED_LOCAL' and not any(r.get('to_state')=='VERIFIED' for r in rows)
    head,_=git('head-before-transition','rev-parse','HEAD');assert head.decode().strip()==COMMIT
    for item in load(R72/'exact-verification.dispatch72.json')['inputs']:verify_hash(ROOT/item['path'],item['RAW_sha256'],item['RAW_bytes'],item['LF_sha256'])
    proof=load(OWN/'fresh-lean-exact72.json');native_reuse=load(OWN/'native-evidence-reuse.json')
    evidence={'verifier_id':ACTOR,'verified_commit':COMMIT,'native_verified':True,
      'gate':{'scope':'two exact SCI72 declarations, source/publication/semantic/frontier/contributor/private inventory; serialized aggregate deferred',
              'metadata':pin(OWN/'metadata-gates.json'),'fresh_Lean':proof['results']},
      'source_audit':{'status':'source-reviewed','root_adoption':pin(R72/'root.source72.adoption.json'),
                      'native_lease':native_reuse['records'][1]['native_lease'],'checked':pin(OWN/'focused-source-frontier-fakeclosure.json')},
      'native_lease':native_reuse['records'][1]['native_lease'],
      'semantic_roundtrip_audit':load(R72/'publication-plan.json')['audit_ids'],
      'fake_closure_scan':{'hits':0,'evidence':pin(OWN/'focused-source-frontier-fakeclosure.json')},
      'publication_declarations':load(R72/'publication-plan.json')['mathematical_declarations'],
      'truth_boundary':load(R72/'publication-plan.json')['remaining_boundary'],
      'native_evidence_reuse':pin(OWN/'native-evidence-reuse.json'),
      'independent_verification_owned_scope':OWN.relative_to(ROOT).as_posix(),
      'proving_owner':'companion_root_20261005','no_owner_self_verification':True}
    save('decision.before-transition.json',{'decision':'ACCEPT_EXACT_SCI72_FOR_UNIQUE_VERIFIED_TRANSITION',
        'checked_commit':COMMIT,'evidence':evidence,'wholepaper_Goal_Purified_credit':False,'actual_verifier_PID':os.getpid()})
    before=(ROOT/'runs/substantive_advances.jsonl').read_bytes()
    save('ledger-before-transition.meta.json',{'RAW_sha256':sha(before),'RAW_bytes':len(before),'target_rows':rows,
         'global_history_not_copied':True})
    try:
        transition_advance(SAU,'VERIFIED',worker_id=ACTOR,modes=['independent-exact-commit-verification'],evidence=evidence)
    except BaseException:
        after=(ROOT/'runs/substantive_advances.jsonl').read_bytes()
        save('transition.failed-readonly-confirmation.json',{'ledger_changed':after!=before,'target_rows':ledger_rows(),
            'global_ledger_after':pin(ROOT/'runs/substantive_advances.jsonl'),'no_retry_permitted':True,'traceback':traceback.format_exc()})
        raise
    after=(ROOT/'runs/substantive_advances.jsonl').read_bytes();assert after.startswith(before)
    delta=after[len(before):];newrows=[json.loads(l) for l in delta.splitlines() if l.strip()]
    assert len(newrows)==1 and newrows[0]['to_state']=='VERIFIED' and newrows[0]['advance_id']==SAU and newrows[0]['worker_id']==ACTOR
    assert state(ledger_rows())=='VERIFIED'
    save('transition.exact-append.json',{'actual_verifier_PID':os.getpid(),'append_count':1,'event':newrows[0],
           'before_bytes':len(before),'after_bytes':len(after),'before_RAW_sha256':sha(before),'after_RAW_sha256':sha(after),
           'appended_RAW_sha256':sha(delta),'to_state_used':True,'global_ledger_after':pin(ROOT/'runs/substantive_advances.jsonl')})
    verified={'native_verified':True,'verified_commit':COMMIT,'verifier_id':ACTOR,'advance_id':SAU,
              'status':'VERIFIED_EXACT_SCI72_TWO_CONNECTED_IDENTITIES_ONLY','native_lease':native_reuse['records'][1]['native_lease'],
              'gate':evidence['gate'],'source_audit':evidence['source_audit'],'fake_closure_scan':evidence['fake_closure_scan'],
              'semantic_roundtrip_audit':evidence['semantic_roundtrip_audit'],'publication_declarations':evidence['publication_declarations'],
              'actual_verifier_PID':os.getpid(),'unique_transition':pin(OWN/'transition.exact-append.json'),
              'remaining_boundary':evidence['truth_boundary'],'root_site_aggregate':'deferred to sole serialized root owner',
              'PURIFIED':False,'full_paper':False,'Goal_complete':False}
    (R72/'verified.json').write_bytes((json.dumps(verified,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode('utf-8'))
    save('verified.external-owned-copy.json',verified)
    print(json.dumps({'phase':'transition','status':'VERIFIED','actual_verifier_PID':os.getpid(),'append_count':1,'checked_commit':COMMIT}))

def seal():
    assert load(R72/'verified.json')['verified_commit']==COMMIT
    assert state(ledger_rows())=='VERIFIED'
    assert sum(r.get('to_state')=='VERIFIED' for r in ledger_rows())==1
    receipts=[load(p) for p in sorted((OWN/'terminals').glob('*.receipt.json'))]
    assert all(r['terminal_closed'] for r in receipts)
    for label in load(OWN/'metadata-gates.json')['accepted_receipt_labels']:
        assert load(OWN/'terminals'/str(label+'.receipt.json'))['terminal_EXIT']==0
    assert all(r['terminal_EXIT']==0 for r in load(OWN/'fresh-lean-exact72.json')['results'])
    review=('Independent exact SCI72 verification by '+ACTOR+'\n\n'
      'Checked commit '+COMMIT+'; parent '+PARENT+'. The two connected perturbation identities pass exact Git RAW/workspace pins (only the toolchain/manifest CRLF→LF equivalence is permitted), fresh source elaboration in the pinned Lean4.33.0 runtime, standard-axiom output, native fake-closure scan, publication diff/private-implementation inventory, source/publication bindings, semantic review, two Frontier Cells and contributor contract. The actual consumer uses the original fixed Lake import roots; its imported current generic source/olean are pinned, and the exact generic source is separately freshly compiled.\n\n'
      'Independent closed mathematics (82 files; prior fresh Lean22524/41536), strict blind reconstruction (5), and independent primary-source review (258) are byte-verified and reused without repeating their reviews. No source or proof implementation was edited.\n\n'
      'The proving owner is companion_root_20261005; verifier is '+ACTOR+'. Exactly one authorized PROVED_LOCAL→VERIFIED event was appended using the real to_state schema. verified.json records native_lease, native_verified and verified_commit.\n\n'
      'Actual conditional half-turn H, K/B7, actual r/r_rho/B27, B4/B28 dynamics, H1/B2, invariance/nonexplosion, full PBPS/SPHMC results, errors/caps, expected-query costs and actual-input composition remain OPEN. No PURIFIED, Exposition Seal, main/live, whole-paper or Goal completion is claimed. Root/Tests/site aggregate and graph delivery belong to subsequent serialized stabilization.\n\n'
      'Preliminary nonexistent tooling-name discovery errors and two diagnosed verifier setup failures are retained. The failed actual import used a sparse top-level namespace search root (PID50632 EXIT1); the failed focused observer queried a nonexistent nested verdict field (PID3952 EXIT1). Corrected checks use the original fixed Lake roots and the real top-level audit verdict. No successful check was repeated. All accepted final verification gates have real PID and terminal EXIT0 receipts; failed setup receipts remain visible. No state-transition failure occurred.\n\n'
      'The added full-archive default git whitespace check returned EXIT2. Its 335 substantive findings exactly match the SCI72 frozen diagnosis and all 13 immutable native exception files are bound to exact git-show RAW bytes. The authored complement under explicit cr-at-eol rules passes EXIT0. Full-diff whitespace PASS is expressly not claimed; no immutable evidence was normalized.\n')
    (OWN/'complete-named-review.md').write_bytes(review.encode('utf-8'))
    payload={'schema':1,'reviewer':ACTOR,'checked_commit':COMMIT,'parent':PARENT,'named_review':review,
       'decision':load(OWN/'decision.before-transition.json'),'inputs':load(OWN/'inputs21.git-workspace.manifest.json'),
       'native_evidence_reuse':load(OWN/'native-evidence-reuse.json'),'fresh_compilers':load(OWN/'fresh-lean-exact72.json'),
       'metadata':load(OWN/'metadata-gates.json'),'focused':load(OWN/'focused-source-frontier-fakeclosure.json'),
       'transition':load(OWN/'transition.exact-append.json'),'verified':load(R72/'verified.json'),
       'retained_errors':load(OWN/'retained-discovery-errors.json'),'terminal_receipts':receipts,
       'source_code_review_bindings':load(OWN/'source-code-review-bindings.json'),
       'whitespace_exception_audit':load(OWN/'whitespace-exact-native-exception-audit.json'),
       'retained_phase_failures':[load(p) for p in sorted(OWN.glob('failure.*.json'))]}
    save('complete-named-review-decision-input-payload.json',payload)
    run={'schema':1,'reviewer':ACTOR,'checked_commit':COMMIT,'parent':PARENT,'native_verified':True,
       'verified_commit':COMMIT,'status':'ACCEPTED_EXACT_SCI72_TWO_CONNECTED_IDENTITIES_ONLY','actual_last_writer_PID':os.getpid(),
       'complete_named':pin(OWN/'complete-named-review-decision-input-payload.json'),
       'inputs':load(OWN/'inputs21.git-workspace.manifest.json'),'native_evidence':load(OWN/'native-evidence-reuse.json'),
       'terminal_receipts':receipts,'unique_transition':load(OWN/'transition.exact-append.json'),
       'verified_json':pin(R72/'verified.json'),'truth_boundary':load(R72/'publication-plan.json')['remaining_boundary'],
       'wholelogical_recipe':'delete ONLY top-level run_sha256; sorted UTF8 JSON ensure_ascii=False separators comma colon allow_nan=False',
       'no_more_owned_writes_after_final_lease':True}
    run['run_sha256']=sha(canon(run));save('run.json',run)
    entries=[pin(p) for p in sorted(OWN.rglob('*')) if p.is_file() and p.name not in ['owned.manifest.json','lease.final.json']]
    save('owned.manifest.json',{'entries':entries,'entry_count':len(entries),'logical_entries_sha256':sha(canon(entries)),
           'excludes_only_self_and_final_lease':True})
    save('lease.final.json',{'status':'CLOSED_LAST','owner':ACTOR,'checked_commit':COMMIT,'native_verified':True,'verified_commit':COMMIT,
         'actual_last_writer_PID':os.getpid(),'run_sha256':run['run_sha256'],'manifest':pin(OWN/'owned.manifest.json'),
         'complete_named':pin(OWN/'complete-named-review-decision-input-payload.json'),'owned_files':len(entries)+2,
         'last_write_contract':'THIS lease.final.json is CLOSED_LAST and the final owned write. External process read-only only.',
         'writer_terminal_EXIT_contract':'return EXIT0 immediately; observed separately by caller'})
    print(json.dumps({'phase':'seal','status':'CLOSED_LAST','actual_last_writer_PID':os.getpid(),'run_sha256':run['run_sha256'],'owned_files':len(entries)+2}))

def readonly():
    lease=load(OWN/'lease.final.json');manifest=load(OWN/'owned.manifest.json')
    verify_hash(OWN/'owned.manifest.json',lease['manifest']['RAW_sha256'],lease['manifest']['RAW_bytes'])
    assert sha(canon(manifest['entries']))==manifest['logical_entries_sha256']
    for e in manifest['entries']:verify_hash(e['path'],e['RAW_sha256'],e['RAW_bytes'],e['LF_sha256'])
    files=[p for p in OWN.rglob('*') if p.is_file()]
    assert len(files)==lease['owned_files']
    expected={e['path'] for e in manifest['entries']}|{(OWN/'owned.manifest.json').as_posix(),(OWN/'lease.final.json').as_posix()}
    assert {p.as_posix() for p in files}==expected
    run=load(OWN/'run.json');r=run.pop('run_sha256');assert sha(canon(run))==r==lease['run_sha256']
    assert all(p.stat().st_mtime_ns<=(OWN/'lease.final.json').stat().st_mtime_ns for p in files)
    kernel=ctypes.WinDLL('kernel32',use_last_error=True);kernel.OpenProcess.argtypes=[ctypes.c_uint32,ctypes.c_int,ctypes.c_uint32];kernel.OpenProcess.restype=ctypes.c_void_p
    h=kernel.OpenProcess(0x1000,False,lease['actual_last_writer_PID']);assert not h,'writer PID still exists; inspect read-only'
    assert state(ledger_rows())=='VERIFIED' and sum(r.get('to_state')=='VERIFIED' for r in ledger_rows())==1
    assert load(R72/'verified.json')['verified_commit']==COMMIT
    print(json.dumps({'status':'PASS','external_readonly_PID':os.getpid(),'writer_PID':lease['actual_last_writer_PID'],
       'writer_terminated':True,'owned_files':len(files),'run_sha256':r,'unique_transition':True,'terminal_EXIT_contract':0}))

if __name__=='__main__':
    phase=sys.argv[1];assert phase in ['freeze','native','lean','lean_actual','metadata','metadata_finish','metadata_admit','focused','transition','seal','readonly']
    if phase!='readonly':assert not (OWN/'lease.final.json').exists(),'CLOSED: no write permitted'
    print(json.dumps({'driver_PID':os.getpid(),'phase':phase}),flush=True)
    try: globals()[phase]()
    except BaseException:
        if phase not in ['readonly','seal'] and not (OWN/'lease.final.json').exists():
            save('failure.'+phase+'.'+str(os.getpid())+'.json',{'phase':phase,'actual_PID':os.getpid(),'traceback':traceback.format_exc(),
                        'ledger_state_readonly':state(ledger_rows()),'no_second_transition_attempt':True})
        raise
