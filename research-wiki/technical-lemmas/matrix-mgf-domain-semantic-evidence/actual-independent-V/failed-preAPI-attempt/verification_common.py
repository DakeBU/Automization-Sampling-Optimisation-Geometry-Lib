"""R17 independent verification guards. Import is inert; all full snapshots remain local-private."""
import ast,copy,datetime as dt,hashlib,json,os,stat,subprocess,sys,tarfile,time,traceback
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.dont_write_bytecode=True
OWN=Path(__file__).resolve().parent
REPO=OWN.parents[2]
PRIVATE=OWN/'local-private-guards'
ADV='ASTIS-SA-20261115-MatrixExponentialDomain'
OWNER='huanjian_20261115_matrix_exponential_domain'
VERIFIER='matrix_domain_native_61e4_independent_verifier'
P='AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveDefIntegral.integral_posDef'
MATH='a8bb8ea5b4474be5214bd83ae380a612e2cecb78'
BINDING='5e79fa3d4390c4d1e689174b0c014d67fb8dbfb550f986b4af7d8474ef644691'
ADVPATH='runs/substantive_advances.jsonl'
DISCPATH='runs/substantive_discoveries.jsonl'
CELL='research-wiki/frontier-cells/ASTIS-SHARED-REAL-MATRIX-EXPONENTIAL-DOMAIN.json'
VOUT_PUBLIC='research-wiki/technical-lemmas/matrix-mgf-domain-semantic-evidence/actual-independent-V/normal-V-outcome.public.json'
VAPP_PUBLIC='research-wiki/technical-lemmas/matrix-mgf-domain-semantic-evidence/actual-independent-V/normal-V-exact-append.jsonl'
PLSHA='4e1ae70212a5c951239de161597d0ebf816632c70762305d8c22a7841ea1e520'
PLAPPENDSHA='e52aabd14d64df55826a435023e2a6a117179b405704f85dd59318f9ee8180cc'
NATIVESHA='b9d494dc7402ec65930714729534ee69e3dd1ba52b85a16d9544691f5c4b73ee'
READERSHA='8be01dcb356632540df08a5c592c8b6496e442d180a9f743b20c50dac4a1e33c'
READERMANIFESTSHA='4cfcc33fda763638b257723060649578718d4c4bf327430df962fa18bc8ec2b1'
SOURCES={'AutoSamplingTheory/TechnicalLemmas/Probability/RealMatrixPositiveDefIntegral.lean':'d3c6e5a194fecf1ae1abe45c70310f4f47d66e903b098019c326ee0d3018b024','Tests/GaussianComplexityMatrixMgfDomain.lean':'60e9f7b928ebc1b8a0d9efad93f39f1b172fe0a871893d67eb1015582c5d5c61'}
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
    p=Path(p);return {'file':str(p.relative_to(REPO)),'bytes':p.stat().st_size,'sha256':file_sha(p)}
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
    assert file_sha(path)==h;a=read(path)
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

def evidence_inputs(a):
    data={k:pin_bytes(v) for k,v in a['evidence_pins'].items()}
    assert sha(data['PL'])==PLSHA and sha(data['PL_append'])==PLAPPENDSHA
    pl=json.loads(data['PL']);assert len(pl)==25 and pl['lean_declarations']==pl['publication_declarations']==[P]
    assert pl['actual_native_rebuilt_math_commit']==MATH and json.loads(data['PL_append'])['evidence']==pl
    assert len(data['PL_append'].splitlines())==1 and data['PL_append'].endswith(b'\n')
    native=json.loads(data['native_original']);reader=json.loads(data['reader_original'])
    assert sha(data['native_original'])==NATIVESHA and data['native_original']==data['native_carried']
    assert native['candidate_commit']==MATH and native['independent_rebuild']['exact_ASTIS_modules']==13
    assert native['independent_rebuild']['all13_modules_freshly_recompiled_actual_exit0'] and not native['independent_rebuild']['prior_ASTIS_olean_reused']
    assert native['unsafe_in_complete_actual_target_closure']==0 and not native['sorryAx_or_unauthorized_axiom']
    scan=json.loads(data['native_fake_scan']);assert scan['candidate_commit']==MATH and scan['passed'] and len(scan['modules'])==13 and all(not m['fake_closure_hits'] for m in scan['modules'])
    assert sha(data['reader_original'])==READERSHA and data['reader_original']==data['reader_carried'] and sha(data['reader_manifest_original'])==READERMANIFESTSHA
    assert reader['status']=='PASS_BOUNDED_ISOLATED_READER' and reader['necessary_reader_residual_count']==0
    assert reader['actual_run']['OS_exit_code']==0 and reader['actual_run']['runtime_checks']==523 and reader['actual_run']['runtime_false_checks']==0 and reader['actual_run']['actual_original_PNGs']==50
    assert reader['exact_binding']['source_reviewed_publication_binding_sha256']==BINDING
    assert sha(data['source_run'])=='1b2e4964109b4ca0c495f9ad2ecf50ed7f1508adfe38370487a182ad5fc9466a'
    sr=json.loads(data['source_run']);assert sr['candidate_commit']==MATH and sr['publication_binding_sha256']==BINDING and sr['roles']['all_distinct']
    slots={'objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies'}
    for key,h in [('source_public','480ecf75d0e6f373a030e36ed0e4a0a90dea0728a243f1ad033d360187dc1693'),('source_private','d79ffed0cc5981bddbecb4fce0fea2f9023d56b4ca425bf3736ee53ebef802a9')]:
        v=json.loads(data[key]);assert sha(data[key])==h and v['verdict']=='equivalent-after-elaboration' and not v['deltas'] and not v['repairs'] and set(v['semantic_slots'])==slots and v['independent_from_formalizer'] and v['independent_from_decoder']
    for key in ['public_audit','private_audit']:
        v=json.loads(data[key]);assert v['state']=='source-reviewed' and v['publication_binding_sha256']==BINDING
    assert file_sha(REPO/'lean-toolchain')=='302cd63c54178885b89e669f33b38f12f4dd7ae7e5cac537b3203e3768d8fb2b'
    assert file_sha(REPO/'lake-manifest.json')=='b83ca83b9cf7caa85fa8b023c2ff9a3fb7a7cce7e1c332e810c348535ec49c37'
    for path,h in SOURCES.items():assert file_sha(REPO/path)==h
    assert file_sha(REPO/'website/content/declaration_lessons/huanjian-matrix-mgf-domain.json')=='62bb756e1a030d7f7444a5571cb2008663ccedcda39f9782bdecf641fa9fa08d'
    assert file_sha(REPO/'website/content/publications/huanjian-matrix-mgf-domain.json')=='d2b60c1a9e827f7c6fb81c648930183b77015950de0d97a3acf4d7adb6574f1a'
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
        names+=['normal-V-outcome.public.json','normal-V-exact-append.jsonl','normal-V-evidence.full.json','PROVED_LOCAL-original25.exact.json','window1-postguards.public.json']
        if label=='window2':names+=['target-cell-outcome.public.json','window2-postguards.public.json','window2-schema-precheck.public.json','target-cell-proposal.exact.json']
    else:names+=[label+'-stopped.public.json']
    files=[{'path':n,'bytes':(OWN/n).stat().st_size,'sha256':file_sha(OWN/n)} for n in names]
    write(OWN/(label+'-public-selected-originals.manifest.json'),{'schema':'R17-normal-verification-explicit-own-public-leaves-v1','advance_id':ADV,'window':label,'actual_success_with_postguards':success,'files':files,'full_guards_allstate_maps_raw_ledgers_index_git_output_API_and_raw_OS_streams_excluded':True,'public_OS_receipt_is_explicit_bounded_projection_of_private_actual_receipt':True,'no_raw_stream_payload_or_suffix_trim_normalize':True})

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
    receipt={'schema':'R17-independent-single-window-actual-OS-receipt-v1','window':action,'argv':argv,'cwd':str(REPO),'pid':child.pid,'parent_pid':os.getpid(),'started_utc':utc,'ended_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-start,'actual_exit_code':code,'stdout_sha256':file_sha(out),'stderr_sha256':file_sha(err),'stdout_bytes':out.stat().st_size,'stderr_bytes':err.stat().st_size,'raw_streams_local_private':True,'authorization_sha256':file_sha(args.authorization),'scripts':a['scripts'],'actual_OS_fd1_fd2_captured_separately':True,'no_automatic_retry_rollback_or_second_window':True}
    write(d/'receipt.private.json',{**receipt,'environment_explicit_whitelist':env,'ATLAS_path_reference_only_no_body_read':True})
    write(OWN/(label+'-OS-receipt.public.json'),{**receipt,'private_original_receipt_sha256':file_sha(d/'receipt.private.json'),'projection_omits_only_environment_explicit_whitelist_and_ATLAS_path_reference_flag':True})
    if code:
        marker=PRIVATE/('normal-V-attempted.once.json' if label=='window1' else 'target-cell-attempted.once.json')
        write(OWN/(label+'-stopped.public.json'),{'status':'ACTUAL_FAILURE_STOP_NO_RETRY_NO_ROLLBACK','advance_id':ADV,'window':action,'actual_exit_code':code,'this_window_attempt_marker_present':marker.exists(),'normal_API_calls_authorized_in_this_window':a['normal_API_calls_authorized'],'no_success_or_preservation_claim_without_actual_postguards':True,'actual_bytes_suffix_marker_private_streams_must_be_inspected_before_any_future_action':True})
        public_selection(label,False);return code
    guards=read(OWN/(label+'-postguards.public.json'));assert guards['all_postguards_passed']
    if label=='window1':
        write(OWN/'normal-V-outcome.public.json',{'schema':'R17-independent-normal-proof-V-actual-outcome-v1','status':'NORMAL_V_ACTUALLY_RECORDED_ALL_POSTGUARDS_PASSED','advance_id':ADV,'verified_commit':a['carrier_commit'],'verifier_id':VERIFIER,'normal_API_calls':1,'actual_exit_code':code,'original_PL_top_level_field_count':25,'all_original_PL_top_level_fields_unchanged':True,'exact_appended_record_sha256':guards['exact_appended_record_sha256'],'exact_appended_record_bytes':guards['exact_appended_record_bytes'],'actual_math_build_identity':MATH,'new_build_at_verified_carrier_claimed':False,'all_window1_postguards_passed':True,'all_frontiers_including_target_unchanged':True,'post_advance_ledger_sha256':guards['post_advance_ledger_sha256'],'post_discovery_ledger_sha256':guards['post_discovery_ledger_sha256'],'exact_append':ident(OWN/'normal-V-exact-append.jsonl'),'full_inline_payload':ident(OWN/'normal-V-evidence.full.json'),'actual_OS_receipt':ident(OWN/(label+'-OS-receipt.public.json')),'raw_API_OS_streams_full_guards_and_allstate_maps_private':True,'target_cell_projection_not_launched':True})
    else:write(OWN/'target-cell-outcome.public.json',{'schema':'R17-independent-target-cell-actual-outcome-v1',**guards,'actual_exit_code':code,'actual_OS_receipt':ident(OWN/(label+'-OS-receipt.public.json'))})
    public_selection(label,True);print(json.dumps({'window':action,'advance_id':ADV,'actual_exit_code':code,'all_postguards_passed':True,'next_window_automatically_launched':False}),flush=True);return 0
