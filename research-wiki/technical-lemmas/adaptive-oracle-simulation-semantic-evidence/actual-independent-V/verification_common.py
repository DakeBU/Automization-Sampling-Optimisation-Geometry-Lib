"""R18 independent verification guards. Import is inert; all full snapshots remain local-private."""
import ast,copy,datetime as dt,hashlib,json,os,stat,subprocess,sys,tarfile,time,traceback
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.dont_write_bytecode=True
OWN=Path(__file__).resolve().parent
REPO=OWN.parents[2]
PRIVATE=OWN/'local-private-guards'
ADV='ASTIS-SA-20261116-AdaptiveOracleSimulation'
OWNER='huanjian_20261116_adaptive_oracle_simulation'
VERIFIER='adaptive_oracle_native_61e4_independent_verifier'
P='AutoSamplingTheory.TechnicalLemmas.Probability.AdaptiveOracleSimulation.measurable_simulation_joint_law_and_cost'
MATH='57016008083947405bc7d430838537014a40f987'
BINDING=None
ADVPATH='runs/substantive_advances.jsonl'
DISCPATH='runs/substantive_discoveries.jsonl'
CELL='research-wiki/frontier-cells/ASTIS-SHARED-ADAPTIVE-ORACLE-SIMULATION.json'
VOUT_PUBLIC='research-wiki/technical-lemmas/adaptive-oracle-simulation-semantic-evidence/actual-independent-V/normal-V-outcome.public.json'
VAPP_PUBLIC='research-wiki/technical-lemmas/adaptive-oracle-simulation-semantic-evidence/actual-independent-V/normal-V-exact-append.jsonl'
PLSHA=None
PLAPPENDSHA=None
NATIVESHA='cdab11fcc8542e68123b16e3713e828ebbba7c3342e3dd59e7b7f28d7fe11dee'
READERSHA=None
READERMANIFESTSHA=None
PLCOUNT=None
SOURCES={'AutoSamplingTheory/TechnicalLemmas/Probability/AdaptiveOracleSimulation.lean':'9c0f0c9134aa4360f8bc8384d73f311826224dbe056adb56658d4c393cd33e25','Tests/GaussianComplexityAdaptiveFirstOrderSimulation.lean':'9c28703d8adcc9e33b187371b021c3d1cea902172ce7ba89f1d257d80f7ef6ae'}
SCRIPTS={'verification_common.py','verify_once.py','project_cell_once.py'}
def sha(b):return hashlib.sha256(b).hexdigest()
def file_sha(p):return sha(Path(p).read_bytes())
def read(p):return json.loads(Path(p).read_text())
def private_dir(p):
    p=Path(p);assert p.resolve().is_relative_to(PRIVATE.resolve())
    p.mkdir(parents=True,exist_ok=True,mode=0o700)
    for directory in [p,*p.parents]:
        if directory.resolve().is_relative_to(PRIVATE.resolve()):os.chmod(directory,0o700)
        else:break
def output_parent(p):
    p=Path(p)
    if p.resolve().is_relative_to(PRIVATE.resolve()):private_dir(p.parent);return 0o600
    p.parent.mkdir(parents=True,exist_ok=True);return 0o644
def write(p,x):
    p=Path(p);mode=output_parent(p)
    with p.open('x') as f:os.fchmod(f.fileno(),mode);json.dump(x,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
def exact(p,b):
    p=Path(p);mode=output_parent(p)
    with p.open('xb') as f:os.fchmod(f.fileno(),mode);f.write(b);f.flush();os.fsync(f.fileno())
def ident(p):
    p=Path(p);assert p.is_absolute() and p.resolve().is_relative_to(REPO.resolve());return {'file':str(p.relative_to(REPO)),'bytes':p.stat().st_size,'sha256':file_sha(p)}
def canonical(x):return sha(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def pin_bytes(row):
    p=REPO/row['file'];assert not Path(row['file']).is_absolute() and p.resolve().is_relative_to(REPO.resolve())
    assert not any(x in Path(row['file']).parts for x in ['local-private-guards','.atlas-upstream','.git'])
    raw=p.read_bytes();assert sha(raw)==row['sha256']
    if 'bytes' in row:assert len(raw)==row['bytes']
    if 'member' in row:
        with tarfile.open(p,'r:*') as archive:
            member=archive.getmember(row['member']);assert member.isfile();raw=archive.extractfile(member).read()
        assert sha(raw)==row['member_sha256']
        if 'member_bytes' in row:assert len(raw)==row['member_bytes']
    return raw
def git(label,*args,allow=(0,)):
    directory=PRIVATE/'read-only-git';private_dir(directory)
    out=directory/(label+'.stdout.raw');err=directory/(label+'.stderr.raw');argv=['/usr/bin/git','--no-optional-locks',*args]
    start=time.monotonic()
    with out.open('xb') as o,err.open('xb') as e:
        os.fchmod(o.fileno(),0o600);os.fchmod(e.fileno(),0o600)
        r=subprocess.run(argv,cwd=REPO,env={'PATH':'/usr/bin:/bin','LC_ALL':'C','GIT_OPTIONAL_LOCKS':'0'},stdin=subprocess.DEVNULL,stdout=o,stderr=e)
    write(directory/(label+'.receipt.json'),{'local_private_do_not_publish':True,'argv':argv,'actual_exit_code':r.returncode,'elapsed_seconds':time.monotonic()-start,'stdout_sha256':file_sha(out),'stderr_sha256':file_sha(err)})
    assert r.returncode in allow,(label,r.returncode)
    return out.read_bytes()
def replay(araw,draw):
    assert araw.endswith(b'\n') and draw.endswith(b'\n'),'Never permit API tail recovery/truncation'
    ar=[json.loads(x) for x in araw.splitlines() if x.strip()];dr=[json.loads(x) for x in draw.splitlines() if x.strip()]
    nodes=[n for n in ast.parse((REPO/'tools/astis_advance.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name in ['_replay_advances','_replay_discoveries']]
    assert len(nodes)==2
    ns={'Any':object,'Iterable':list,'NO_PROGRESS_FREEZE_AT':3};exec(compile(ast.Module(body=nodes,type_ignores=[]),'<pure-read-only-replay>','exec'),ns)
    return ar,dr,ns['_replay_advances'](copy.deepcopy(ar)),ns['_replay_discoveries'](copy.deepcopy(dr))
def filesystem_ident(p):
    p=Path(p)
    if p.is_symlink():return {'kind':'symlink','mode':stat.S_IMODE(p.lstat().st_mode),'link_sha256':sha(os.readlink(p).encode())}
    if not p.exists():return {'kind':'missing'}
    s=p.stat();h=file_sha(p);t=p.stat();assert (s.st_size,s.st_mtime_ns,s.st_mode)==(t.st_size,t.st_mtime_ns,t.st_mode)
    return {'kind':'file','mode':stat.S_IMODE(t.st_mode),'bytes':t.st_size,'sha256':h}
def snapshot(label,a):
    directory=PRIVATE/label;assert not directory.exists();private_dir(directory)
    head=git(label+'-HEAD','rev-parse','HEAD').decode().strip();branch=git(label+'-branch','symbolic-ref','HEAD').decode().strip()
    assert head==a['carrier_commit'] and branch==a['expected_branch']
    def gitpath(name):
        p=Path(git(label+'-gitpath-'+name.replace('/','_'),'rev-parse','--git-path',name).decode().strip());return p if p.is_absolute() else REPO/p
    index=gitpath('index');headpath=gitpath('HEAD');ref=gitpath(branch)
    idx=index.read_bytes();exact(directory/'index.exact',idx)
    paths=[x.decode() for x in git(label+'-tracked','ls-files','-z').split(b'\0') if x]
    assert len(paths)==len(set(paths))
    with ThreadPoolExecutor(max_workers=8) as pool:tracked=dict(zip(paths,pool.map(lambda n:filesystem_ident(REPO/n),paths)))
    araw=(REPO/ADVPATH).read_bytes();draw=(REPO/DISCPATH).read_bytes();ar,dr,adv,disc=replay(araw,draw)
    exact(directory/'advance-ledger.exact.jsonl',araw);exact(directory/'discovery-ledger.exact.jsonl',draw)
    frontiers={str(p.relative_to(REPO)):filesystem_ident(p) for p in (REPO/'research-wiki/frontier-cells').rglob('*.json')}
    state={'local_private_do_not_publish':True,'HEAD':head,'branch':branch,'HEAD_file':filesystem_ident(headpath),'branch_ref':filesystem_ident(ref),'index_mode':stat.S_IMODE(index.stat().st_mode),'index_sha256':sha(idx),'tracked':tracked,'frontiers':frontiers,'foreign_A_states':{k:canonical(v) for k,v in adv.items() if k!=ADV},'all_D_states':{k:canonical(v) for k,v in disc.items()},'A_ledger_sha256':sha(araw),'D_ledger_sha256':sha(draw),'view':'local worktree ledger replay only; no origin/main stabilizer release claim'}
    if not ref.exists():state['packed_refs']=filesystem_ident(gitpath('packed-refs'))
    write(directory/'full-guard-map.private.json',state)
    return {'state':state,'araw':araw,'draw':draw,'records':ar,'adv':adv,'disc':disc,'index':idx}
def postguards(before,after,a,allowed,cell_exception=None):
    x=before['state'];y=after['state']
    for k in ['HEAD','branch','HEAD_file','branch_ref','packed_refs','index_mode']:
        assert x.get(k)==y.get(k),k
    assert before['index']==after['index'] and set(x['tracked'])==set(y['tracked'])
    changed={k for k in x['tracked'] if x['tracked'][k]!=y['tracked'][k]};assert changed<=set(allowed),changed
    # Mode bits stay exact even for the one permitted content mutation.
    assert all(x['tracked'][k].get('mode')==y['tracked'][k].get('mode') for k in x['tracked'])
    assert x['foreign_A_states']==y['foreign_A_states'] and x['all_D_states']==y['all_D_states'] and before['draw']==after['draw']
    assert {k:v for k,v in x['frontiers'].items() if k!=cell_exception}=={k:v for k,v in y['frontiers'].items() if k!=cell_exception}
    return {'HEAD_branch_index_exact':True,'all_tracked_modes_exact':True,'all_other_tracked_bytes_exact':True,'all_foreign_A_and_all_D_states_exact':True,'D_ledger_exact':True,'all_frontiers_including_target_exact':cell_exception is None,'all_other_frontiers_exact':True,'only_changed_tracked_paths':sorted(changed),'tracked_paths_checked':len(x['tracked']),'frontiers_checked':len(x['frontiers']),'full_maps_private_only':True}

def validate_authorization(path,h,action):
    global BINDING,PLSHA,PLAPPENDSHA,READERSHA,READERMANIFESTSHA,PLCOUNT
    assert Path(path).is_absolute() and Path(path).resolve().is_relative_to(OWN.resolve()),'Exact absolute new-namespace authorization path required'
    assert file_sha(path)==h;a=read(path)
    assert a.get('preparation_only') is False
    BINDING=a['source_binding'];PLSHA=a['original_PL_sha256'];PLAPPENDSHA=a['original_PL_append_sha256']
    READERSHA=a['reader_report_sha256'];READERMANIFESTSHA=a['reader_manifest_sha256'];PLCOUNT=a['original_PL_field_count']
    assert all(isinstance(v,str) and len(v)==64 for v in [BINDING,PLSHA,PLAPPENDSHA,READERSHA,READERMANIFESTSHA])
    assert type(PLCOUNT) is int and PLCOUNT>0
    assert a['authorization_absolute_path']==str(Path(path))
    assert a['authorization']=='ROOT_EXPLICIT_SINGLE_WINDOW_AUTHORIZATION' and a['authorized_action']==action
    assert a['advance_id']==ADV and a['owner_id']==OWNER and a['worker_id']==a['verifier_id']==VERIFIER and VERIFIER!=OWNER
    assert a['math_commit']==MATH and a['source_binding']==BINDING
    assert a['normal_API_calls_authorized']==(1 if action=='NORMAL_PROOF_V_ONCE' else 0)
    assert a['expected_api_sha256']==file_sha(REPO/'tools/astis_advance.py')
    assert a['expected_cell_validator_sha256']==file_sha(REPO/'tools/astis_frontier_cells.py')
    assert set(a['scripts'])==SCRIPTS and all(file_sha(OWN/n)==h for n,h in a['scripts'].items())
    assert a['separate_window2_authorization_required'] is True
    return a

def inspect_target(s,pl,state):
    target=s['adv'][ADV];rows=[r for r in s['records'] if r.get('advance_id')==ADV]
    assert target['state']==state and target['owner_id']==OWNER
    assert target['target_declarations']==target['publication_declarations']==[P]
    assert sum(r.get('to_state')=='PROVED_LOCAL' for r in rows)==1
    assert sum(r.get('to_state')=='VERIFIED' for r in rows)==(0 if state=='PROVED_LOCAL' else 1)
    assert next(r['evidence'] for r in rows if r.get('to_state')=='PROVED_LOCAL')==pl
    assert any(sha(line+b'\n')==PLAPPENDSHA for line in s['araw'].splitlines())
    return target

def json_pointer(value,pointer):
    assert isinstance(pointer,str) and pointer.startswith('/')
    for token in pointer.split('/')[1:]:
        token=token.replace('~1','/').replace('~0','~')
        value=value[int(token)] if isinstance(value,list) else value[token]
    return value

def evidence_inputs(a):
    required={'PL','PL_append','native_original','native_carried','native_fake_scan','reader_original','reader_carried','reader_manifest_original','source_run','source_public','source_private','public_audit','private_audit'}
    assert set(a['evidence_pins'])==required
    data={k:pin_bytes(v) for k,v in a['evidence_pins'].items()}
    assert sha(data['PL'])==PLSHA and sha(data['PL_append'])==PLAPPENDSHA
    pl=json.loads(data['PL']);assert len(pl)==PLCOUNT and pl['lean_declarations']==pl['publication_declarations']==[P]
    assert json.loads(data['PL_append'])['evidence']==pl
    assert len(data['PL_append'].splitlines())==1 and data['PL_append'].endswith(b'\n')
    native=json.loads(data['native_original']);reader=json.loads(data['reader_original'])
    assert sha(data['native_original'])==NATIVESHA and data['native_original']==data['native_carried']
    assert native['candidate_commit']==MATH and native['independent_rebuild']['exact_ASTIS_modules']==6
    assert native['independent_rebuild']['all6_first_compiles_actual_exit0'] and not native['independent_rebuild']['old_ASTIS_olean_reused']
    assert native['unsafe_in_target_logical_closure']==native['partial_in_target_logical_closure']==0
    assert not native['sorryAx_or_unauthorized_axiom_in_target_closure'] and native['axioms']==['Classical.choice','Quot.sound','propext']
    assert native['complete_recursive_target_dependency_closure']['declarations']==34481
    partial=native['raw_type_value_Level_DAG']['compiler_partial_values_preserved_not_safely_kernel_checked']
    assert len(partial)==1 and partial[0]['partial'] and not partial[0]['kernel_value_checked']
    scan=json.loads(data['native_fake_scan']);assert scan['candidate_commit']==MATH and scan['passed'] and len(scan['modules'])==6 and all(not m['fake_closure_hits'] for m in scan['modules'])
    assert sha(data['reader_original'])==READERSHA and data['reader_original']==data['reader_carried'] and sha(data['reader_manifest_original'])==READERMANIFESTSHA
    # Exact future schemas/outcomes must be independently inspected before these conditions are filled and frozen.
    checks=a['independently_reviewed_evidence_checks']
    assert set(checks)=={'PL','reader_original','source_run','source_public','source_private','public_audit','private_audit'}
    for key,conditions in checks.items():
        assert isinstance(conditions,list) and conditions
        obj=json.loads(data[key])
        for row in conditions:
            assert set(row)=={'pointer','expected'} and row['expected'] is not None
            assert json_pointer(obj,row['pointer'])==row['expected'],(key,row['pointer'])
    assert a['source_reader_review_status']=='INDEPENDENTLY_INSPECTED_CURRENT_OUTCOMES_NOT_ROOT_VERDICT_INHERITANCE'
    assert file_sha(REPO/'lean-toolchain')=='302cd63c54178885b89e669f33b38f12f4dd7ae7e5cac537b3203e3768d8fb2b'
    assert file_sha(REPO/'lake-manifest.json')=='b83ca83b9cf7caa85fa8b023c2ff9a3fb7a7cce7e1c332e810c348535ec49c37'
    for path,h in SOURCES.items():assert file_sha(REPO/path)==h
    assert a['owned_metadata_pins']
    for row in a['owned_metadata_pins']:pin_bytes(row)
    gates=json.loads(pin_bytes(a['gate_summary']))
    assert gates['carrier']==a['carrier_commit'] and gates['original_math_identity']==MATH
    assert len(gates['records'])==6 and {r['gate'] for r in gates['records']}=={'publication','contributor','semantic','private-semantic','frontier','whitespace'}
    for row in gates['records']:
        assert row['checked_metadata_commit']==a['carrier_commit'] and row['actual_exit_code']==0
        receipt=REPO/row['receipt'];assert file_sha(receipt)==row['receipt_sha256'];r=read(receipt)
        assert r['exit_code']==0 and r['head_before']==r['head_after']==a['carrier_commit']
        assert file_sha(Path(r['log']))==r['log_sha256']
    return {'pl':pl,'pl_raw':data['PL'],'native':native,'reader':reader,'gates':gates,'pins':a['evidence_pins']}

def differences(a,b,p=''):
    if type(a) is not type(b):return [p]
    if isinstance(a,dict):return sum((differences(a[k],b[k],p+'/'+k) if k in a and k in b else [p+'/'+k] for k in sorted(set(a)|set(b))),[])
    if isinstance(a,list):return [] if a==b else [p]
    return [] if a==b else [p]

def public_selection(label,success):
    names=['verification_common.py','verify_once.py','project_cell_once.py',label+'-OS-receipt.public.json']
    if success:
        names+=['normal-V-outcome.public.json','normal-V-exact-append.jsonl','normal-V-evidence.full.json','PROVED_LOCAL-original.exact.json','window1-postguards.public.json']
        if label=='window2':names+=['target-cell-outcome.public.json','window2-postguards.public.json','window2-schema-precheck.public.json','target-cell-proposal.exact.json']
    else:names+=[label+'-stopped.public.json']
    files=[{'path':n,'bytes':(OWN/n).stat().st_size,'sha256':file_sha(OWN/n)} for n in names]
    write(OWN/(label+'-public-selected-originals.manifest.json'),{'schema':'R18-normal-verification-explicit-own-public-leaves-v1','advance_id':ADV,'window':label,'actual_success_with_postguards':success,'files':files,'full_guards_allstate_maps_raw_ledgers_index_git_output_API_and_raw_OS_streams_excluded':True,'public_OS_receipt_is_explicit_bounded_projection_of_private_actual_receipt':True,'no_raw_stream_payload_or_suffix_trim_normalize':True})

def run_captured(args,action,child_function):
    os.umask(0o077);a=validate_authorization(args.authorization,args.authorization_sha256,action)
    if args.child:child_function(a,args.authorization);return 0
    label='window1' if action=='NORMAL_PROOF_V_ONCE' else 'window2';d=PRIVATE/(label+'-OS-process');assert not d.exists();private_dir(d)
    out=d/'stdout.raw';err=d/'stderr.raw';argv=[sys.executable,str(Path(sys.argv[0]).resolve()),*sys.argv[1:],'--child']
    home=os.environ['HOME'];assert home=='/Users/zhouhuanjian'
    env={'HOME':home,'PATH':str(Path(sys.executable).parent)+':/usr/bin:/bin','LC_ALL':'C','PYTHONDONTWRITEBYTECODE':'1','PYTHONIOENCODING':'utf-8','GIT_OPTIONAL_LOCKS':'0','ASTIS_ATLAS_ROOT':str(REPO/'.atlas-upstream/v1')}
    utc=dt.datetime.now(dt.timezone.utc).isoformat();start=time.monotonic()
    with out.open('xb') as o,err.open('xb') as e:
        os.fchmod(o.fileno(),0o600);os.fchmod(e.fileno(),0o600)
        child=subprocess.Popen(argv,cwd=REPO,env=env,stdin=subprocess.DEVNULL,stdout=o,stderr=e);code=child.wait()
    receipt={'schema':'R18-independent-single-window-actual-OS-receipt-v1','window':action,'argv':argv,'cwd':str(REPO),'pid':child.pid,'parent_pid':os.getpid(),'started_utc':utc,'ended_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-start,'actual_exit_code':code,'stdout_sha256':file_sha(out),'stderr_sha256':file_sha(err),'stdout_bytes':out.stat().st_size,'stderr_bytes':err.stat().st_size,'raw_streams_local_private':True,'authorization_sha256':file_sha(args.authorization),'scripts':a['scripts'],'actual_OS_fd1_fd2_captured_separately':True,'no_automatic_retry_rollback_or_second_window':True}
    write(d/'receipt.private.json',{**receipt,'environment_explicit_whitelist':env,'ATLAS_path_reference_only_no_body_read':True})
    write(OWN/(label+'-OS-receipt.public.json'),{**receipt,'private_original_receipt_sha256':file_sha(d/'receipt.private.json'),'projection_omits_only_environment_explicit_whitelist_and_ATLAS_path_reference_flag':True})
    if code:
        marker=PRIVATE/('normal-V-attempted.once.json' if label=='window1' else 'target-cell-attempted.once.json')
        write(OWN/(label+'-stopped.public.json'),{'status':'ACTUAL_FAILURE_STOP_NO_RETRY_NO_ROLLBACK','advance_id':ADV,'window':action,'actual_exit_code':code,'this_window_attempt_marker_present':marker.exists(),'normal_API_calls_authorized_in_this_window':a['normal_API_calls_authorized'],'no_success_or_preservation_claim_without_actual_postguards':True,'actual_bytes_suffix_marker_private_streams_must_be_inspected_before_any_future_action':True})
        public_selection(label,False);return code
    guards=read(OWN/(label+'-postguards.public.json'));assert guards['all_postguards_passed']
    if label=='window1':
        write(OWN/'normal-V-outcome.public.json',{'schema':'R18-independent-normal-proof-V-actual-outcome-v1','status':'NORMAL_V_ACTUALLY_RECORDED_ALL_POSTGUARDS_PASSED','advance_id':ADV,'verified_commit':a['carrier_commit'],'verifier_id':VERIFIER,'normal_API_calls':1,'actual_exit_code':code,'original_PL_top_level_field_count':PLCOUNT,'all_original_PL_top_level_fields_unchanged':True,'exact_appended_record_sha256':guards['exact_appended_record_sha256'],'exact_appended_record_bytes':guards['exact_appended_record_bytes'],'actual_math_build_identity':MATH,'new_build_at_verified_carrier_claimed':False,'all_window1_postguards_passed':True,'all_frontiers_including_target_unchanged':True,'post_advance_ledger_sha256':guards['post_advance_ledger_sha256'],'post_discovery_ledger_sha256':guards['post_discovery_ledger_sha256'],'exact_append':ident(OWN/'normal-V-exact-append.jsonl'),'full_inline_payload':ident(OWN/'normal-V-evidence.full.json'),'actual_OS_receipt':ident(OWN/(label+'-OS-receipt.public.json')),'raw_API_OS_streams_full_guards_and_allstate_maps_private':True,'target_cell_projection_not_launched':True})
    else:write(OWN/'target-cell-outcome.public.json',{'schema':'R18-independent-target-cell-actual-outcome-v1',**guards,'actual_exit_code':code,'actual_OS_receipt':ident(OWN/(label+'-OS-receipt.public.json'))})
    public_selection(label,True);print(json.dumps({'window':action,'advance_id':ADV,'actual_exit_code':code,'all_postguards_passed':True,'next_window_automatically_launched':False}),flush=True);return 0
