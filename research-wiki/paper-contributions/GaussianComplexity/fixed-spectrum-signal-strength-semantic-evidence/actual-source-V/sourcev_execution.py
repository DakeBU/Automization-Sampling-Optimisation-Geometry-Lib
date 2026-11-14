from pathlib import Path
import contextlib,copy,datetime,gzip,hashlib,io,json,os,subprocess,sys,tarfile,traceback
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC')
RUN=ROOT/'.astis/semantic-neutral-20261110/src_a83e10/sourcev_execution_20261110'
PUB=RUN/'public'; PRIVATE=RUN/'private'
E=ROOT/'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-signal-strength-semantic-evidence'
ADV='ASTIS-SA-20261110-GaussianComplexityFixedSpectrumSignalStrength'
VERIFIER='/root/source_reader_a83e10'
OWNER='huanjian_gc_20261110_fixed_spectrum_signal_strength'
FRONT=ROOT/'research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-signal-strength.json'
LEDGER=ROOT/'runs/substantive_advances.jsonl'
CANDIDATE='df64aaa6088b6ac88c35696acfed906031964d72'
CARRIER='cb761181b45a73fe884d9c7590a8710105a108e1'
DECL='AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSignalStrength.eventual_actual_gaussian_signal_strength'
def shab(b):return hashlib.sha256(b).hexdigest()
def sha(p):return shab(p.read_bytes())
def canon(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def digest(v):return shab(canon(v))
def load(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def ref(p):return {'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size}
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
sys.path.insert(0,str(ROOT/'tools'))
import astis_advance as advance
import astis_semantic_roundtrip as roundtrip

def head():
    g=ROOT/'.git'; h=(g/'HEAD').read_text().strip()
    if not h.startswith('ref: '):return h
    r=h[5:]; f=g/r
    if f.exists():return f.read_text().strip()
    for line in (g/'packed-refs').read_text().splitlines():
        if line.endswith(' '+r):return line.split()[0]
    raise ValueError('Unresolved filesystem HEAD')

def protected_snapshot():
    # Read-only Git index inventory; no index refresh, Git mutation or network.
    env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
    tracked=subprocess.check_output(['git','ls-files','-z','--cached'],cwd=ROOT,env=env).split(b'\0')
    untracked=subprocess.check_output(['git','ls-files','-z','--others','--exclude-standard'],cwd=ROOT,env=env).split(b'\0')
    paths={os.fsdecode(x) for x in tracked+untracked if x}
    paths|={str(p.relative_to(ROOT)) for p in (ROOT/'research-wiki/frontier-cells').rglob('*') if p.is_file()}
    paths|={'runs/substantive_discoveries.jsonl','.git/HEAD','.git/index','lean-toolchain','lakefile.lean','lake-manifest.json'}
    # Include the current ref bytes and package identity metadata, without package semantic work.
    h=(ROOT/'.git/HEAD').read_text().strip()
    if h.startswith('ref: '):paths.add('.git/'+h[5:])
    for package in (ROOT/'.lake/packages').iterdir():
        if not package.is_dir():continue
        g=package/'.git'
        if g.is_file():
            paths.add(str(g.relative_to(ROOT)))
            gd=Path(g.read_text().strip().removeprefix('gitdir: '))
            if not gd.is_absolute():gd=(package/gd).resolve()
        elif g.is_dir():gd=g
        else:continue
        for item in [gd/'HEAD',gd/'packed-refs']:
            if item.is_file():paths.add(str(item.relative_to(ROOT)))
        hh=(gd/'HEAD').read_text().strip()
        if hh.startswith('ref: ') and (gd/hh[5:]).is_file():paths.add(str((gd/hh[5:]).relative_to(ROOT)))
    ownrun=str(RUN.relative_to(ROOT))+'/'
    paths={p for p in paths if not p.startswith(ownrun) and p!=str(LEDGER.relative_to(ROOT)) and p!=str(FRONT.relative_to(ROOT))}
    values={p:(sha(ROOT/p) if (ROOT/p).is_file() else 'MISSING') for p in sorted(paths)}
    families={name:sum(name in p for p in values) for name in ['ProximalBPS','SmoothedPicardHMC','research-wiki/paper-contributions/PBPS']}
    assert all(families.values()),'Required actual protected families must be nonempty'
    return {'files':values,'families':families,'tracked_count':len([x for x in tracked if x]),'untracked_count':len([x for x in untracked if x])}

def verify_archive(manifest):
    archive=ROOT/manifest['archive']['path']
    assert sha(archive)==manifest['archive']['sha256']
    t=tarfile.open(archive)
    members={m.name:m for m in t.getmembers() if m.isfile()}
    for entry in manifest.get('files',[]):
        name=entry['path']; assert name in members,name
        b=t.extractfile(members[name]).read()
        assert shab(b)==entry['sha256'],name
        if 'bytes' in entry:assert len(b)==entry['bytes'],name
    return t,members

def preflight():
    assert not (PUB/'original-evidence.raw.json').exists(),'Preflight already created; inspect before repeating'
    assert head()==CARRIER
    applications={n:load(E/n) for n in ['exact-independent-source-review-application.json','independent-module-native-static-reader-6bc291-manifest.json','accepted-C7-locator-precision-application.json','accepted-review-checks/actual-working-layer-gates.json']}
    source=applications['exact-independent-source-review-application.json']
    native=applications['independent-module-native-static-reader-6bc291-manifest.json']
    overlay=applications['accepted-C7-locator-precision-application.json']
    gates=applications['accepted-review-checks/actual-working-layer-gates.json']
    assert source['proposal_sha256']=='f05c4af13db556783d31b1ffe49e1670073e9e8d2a6a88fd26f18d0a448bbcf7'
    assert source['source_freeze_sha256']=='70eb35cfe123ea3a4a7b6da8f5797824295461d634b116ca1a82e7e549a59c28'
    sa=ROOT/source['source_archive']['path']; assert sha(sa)==source['source_archive']['sha256']
    st=tarfile.open(sa)
    for n,h in [('phase3.freeze.json',source['source_freeze_sha256']),('phase3_canonical_five_field_proposal.json',source['proposal_sha256'])]:
        member=next(m for m in st.getmembers() if m.isfile() and (m.name==n or m.name.endswith('/'+n)))
        assert shab(st.extractfile(member).read())==h
    nt,members=verify_archive(native)
    assert shab(nt.extractfile('freeze.json').read())=='b03582c72b2c874bbbe2a2896a2dc9d70dbd60f920e435f74d171df277b52904'
    report=json.loads(nt.extractfile('check-report.json').read())
    assert report['candidate_commit']==CANDIDATE and report['local_mathematical_native_static_result']=='PASS'
    assert report['kernel']['owned_count']==13 and report['kernel']['handwritten_count']==4
    assert report['kernel']['reachable_generated_proof_count']==2 and report['kernel']['unused_generated_simp_count']==7
    assert report['kernel']['all_axioms_standard'] and report['kernel']['all_handwritten_reachable']
    assert report['environment']['reused_canonical_objects']==8 and report['environment']['fresh_parent_compilations']==0
    for name in ['isolated-producer','isolated-Test','isolated-kernel-audit','static-lesson-v2']:
        receipt=json.loads(nt.extractfile(name+'.receipt.json').read())
        assert receipt['exit_code']==0
        for stream in ['stdout','stderr']:
            assert shab(nt.extractfile(name+'.'+stream+'.log').read())==receipt[stream+'_sha256']
    reuse=json.loads(nt.extractfile('canonical-reuse.json').read())
    assert len(reuse['objects'])==8
    for r in reuse['objects']:
        assert sha(ROOT/r['source'])==r['source_sha256'] and r['exit_code']==0 and not r['fresh_parent_compilation_claim']
        op='oleans/'+r['source'].removesuffix('.lean')+'.olean'
        assert shab(nt.extractfile(op).read())==r['object_sha256']
        orig=next(v for k,v in members.items() if k.startswith('reused-native-evidence/') and shab(nt.extractfile(v).read())==r['receipt_sha256'])
        rr=json.loads(nt.extractfile(orig).read()); assert rr['exit_code']==0
    for which,expected in [('source_overlay','78990a241f6a7e1f9f75b519304c77b8da59d43671720a1cdf1b9d3c23003267'),('native_overlay','3468b9766b8171d1b98faa38aa336e15d961d145946aaa634eb8c247ddfad4da')]:
        t,_=verify_archive(overlay[which]); assert shab(t.extractfile('freeze.json').read())==expected
    assert sha(ROOT/overlay['current_successor']['path'])==overlay['current_successor']['sha256']
    gatebindings=[]
    for g in gates['checks']:
        rp=E/'accepted-review-checks'/g['receipt']; assert sha(rp)==g['receipt_sha256']
        r=load(rp); assert r['exit_code']==g['exit_code']==0
        assert r['head_before']==r['head_after']==CANDIDATE
        gz=rp.with_name(rp.name.removesuffix('.receipt.json')+'.log.gz')
        assert sha(gz)==g['lossless_gzip_sha256']
        assert shab(gzip.decompress(gz.read_bytes()))==g['original_log_sha256']==r['log_sha256']
        gatebindings.append({'receipt':ref(rp),'lossless_log':ref(gz),'original_log_sha256':g['original_log_sha256'],'command':g['command'],'exit_code':0,'actual_execution_HEAD':CANDIDATE})
    assert len([g for g in gatebindings if g['command'][1].startswith('tools/')])==4
    auditpath=ROOT/'research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-signal-strength.json'
    assert sha(auditpath)=='fa9654df283d41a2439550f6baed0312a4d0ef0c8cae4bb11039ec2dbb24ae62'
    audit=next(a for a in roundtrip.load_registry()['audits'] if a['id']=='ASTIS-RT-20261110-HuanjianFixedSpectrumSignalStrength')
    proposal=load(RUN.parent/'phase3_canonical_five_field_proposal.json')
    assert all(audit[k]==proposal[k] for k in proposal)
    assert audit['publication_binding_sha256']=='aa982161b75c7550ba8168b07d4c45218f497e7463c99e250d66012c622de195'
    state=advance.current_advances(); own=state[ADV]
    assert own['state']=='PROVED_LOCAL' and own['owner_id']==OWNER and own['publication_declarations']==[DECL]
    frontier=load(FRONT); assert frontier['status']=='proved_locally' and frontier['owner_id']==OWNER
    ledger=LEDGER.read_bytes(); assert ledger.endswith(b'\n')
    for line in ledger.splitlines():json.loads(line)
    (PRIVATE/'ledger.before.raw.jsonl').write_bytes(ledger)
    write(PRIVATE/'states.before.json',state)
    (PUB/'own-frontier.before.raw.json').write_bytes(FRONT.read_bytes())
    write(PUB/'own-sau.before.json',own)
    protected=protected_snapshot(); write(PRIVATE/'protected.before.json',protected)
    # Preserve foreign frontier bytes privately; do not publish foreign path inventories.
    with tarfile.open(PRIVATE/'foreign-frontiers.before.tar','w') as tf:
        for f in (ROOT/'research-wiki/frontier-cells').rglob('*'):
            if f.is_file() and f!=FRONT:tf.add(f,arcname=str(f.relative_to(ROOT)),recursive=False)
    checked=load(RUN.parent/'phase3_bound_inputs.json')['whitelisted_candidate_files']
    for f in checked:assert sha(ROOT/f['path'])==f['sha256']
    pre={'scope':'Bounded evidence preflight before exactly one normal local VERIFIED API; no repeated native/static/site gate.',
      'carrier_commit':CARRIER,'source_and_native_checked_candidate':CANDIDATE,
      'audit_raw_sha256':sha(auditpath),'audit_canonical_sha256':digest(audit),
      'exact_original_five_fields_equal':True,'applications':[ref(E/n) for n in applications],
      'native_archive_full_manifest_members_verified':len(native['files']),
      'native_freeze_sha256':native['independent_freeze_sha256'],
      'fresh_native_producer_Test_kernel':True,'reused_canonical_objects':8,'fresh_parent_compiles':0,
      'owned_inventory':{k:report['kernel'][k] for k in ['owned_count','handwritten_count','reachable_generated_proof_count','unused_generated_simp_count','all_handwritten_reachable','all_axioms_standard']},
      'C7_qualification_closed_by_separate_two_role_overlays_only':True,
      'four_actual_metadata_gates':gatebindings,'fresh_gate_or_native_at_carrier_claim':False,
      'protected_file_count':len(protected['files']),'protected_private_inventory_commitment':digest(protected),
      'actual_nonempty_family_counts':protected['families'],'foreign_raw_snapshots_public':False,
      'ledger_before_bytes':len(ledger),'ledger_before_sha256':shab(ledger),
      'SAU_before':'PROVED_LOCAL','frontier_before':'proved_locally','normal_API_calls_so_far':0}
    write(PUB/'evidence-preflight.json',pre)
    evidence={
      'verifier_id':VERIFIER,'verified_commit':CANDIDATE,'accepted_evidence_carrier_commit':CARRIER,
      'publication_declarations':[DECL],
      'gate':{'scope':'Actual accepted-review working-layer metadata gates on HEADdf64; no new gate/native claim at carrier cb761.',
        'manifest':ref(E/'accepted-review-checks/actual-working-layer-gates.json'),'checks':gatebindings},
      'source_audit':{'reviewer':VERIFIER,'independent_from_formalizer':True,'independent_from_decoder':True,
        'original_phase3_freeze_sha256':source['source_freeze_sha256'],'original_five_field_proposal_sha256':source['proposal_sha256'],
        'review_run_sha256':source['source_review_run_sha256'],'application':ref(E/'exact-independent-source-review-application.json'),
        'audit':ref(auditpath),'audit_canonical_sha256':digest(audit),'reviewer_packet_sha256':audit['source_review']['reviewer_packet_sha256'],
        'scope':'Public selected actual-Gaussian norm/SNR and private diagonal-law zero-event only; full module,providers,Test and six-step exposition reviewed.'},
      'fake_closure_scan':{'actor':'/root/module_reader_f35b7d','manifest':ref(E/'independent-module-native-static-reader-6bc291-manifest.json'),
        'freeze_sha256':native['independent_freeze_sha256'],'owned_inventory':pre['owned_inventory'],
        'axioms':['propext','Classical.choice','Quot.sound'],'complete_provider_and_root_kernel_types_checked':True,
        'scope':'Fresh producer/fullTest/kernel at df64;13owned=4handwritten+2reachable generated proofs+7unused compiler simp; no fake closure.'},
      'native_verification':{'checked_commit':CANDIDATE,'actor':'/root/module_reader_f35b7d',
        'archive':native['archive'],'new_native_compilations':2,'new_kernel_audit':1,
        'canonical_object_reuse':reuse,'fresh_parent_compilation_claim':False,
        'receipt_names':['isolated-producer.receipt.json','isolated-Test.receipt.json','isolated-kernel-audit.receipt.json'],
        'local_static_reader_only':True,'public_browser_or_site_acceptance':False},
      'locator_precision_overlay':{'application':ref(E/'accepted-C7-locator-precision-application.json'),
        'source_freeze_sha256':overlay['source_overlay']['independent_freeze_sha256'],
        'native_freeze_sha256':overlay['native_overlay']['independent_freeze_sha256'],
        'current_map':overlay['current_successor'],'field_changes':10,
        'changes_mathematics_or_original_reviews':False},
      'publication_binding_sha256':audit['publication_binding_sha256'],
      'checked_input_files':checked,
      'preflight':ref(PUB/'evidence-preflight.json'),
      'original_proved_local_history':'Retained unchanged; earlier pre-review publication/contributor failures remain preserved and are discharged only by the actual later accepted-source successful metadata receipts.',
      'source_provenance_limits':'Phase1 incidental older filename-only exposure remains disclosed; scope HTML extractions are derived and original full raw HTML is source authority. No prior freeze or original review rewritten.',
      'truth_boundary':'LOCAL verification only. No full tau/tau-over-beta, shifted/rotated detector or Ex26, algorithm/oracle/TV/precision/cost, main bounds, STAB/integration/Registry/import/site/browser/publication/purification/Exposition Seal/whole-Goal completion.',
      'execution_authority':'Original independent source verifier explicitly authorized one normal PROVED_LOCAL->VERIFIED API, then separate own-frontier status/evidence string closeout only; no post_integration release.'}
    write(PUB/'original-evidence.raw.json',evidence)
    (PUB/'original-evidence.canonical.json').write_bytes(canon(evidence))
    write(PUB/'all-original-keys-retention-contract.json',{
      'scope':'This complete original evidence object and every original nested value must survive any future release unchanged.',
      'original_keys':list(evidence),'original_key_count_observed_not_fixed':len(evidence),
      'original_evidence_raw_sha256':sha(PUB/'original-evidence.raw.json'),
      'original_evidence_canonical_sha256':digest(evidence),
      'original_value_canonical_hashes':{k:digest(v) for k,v in evidence.items()},
      'complete_original_evidence':evidence,
      'future_change_contract':'Only this original verifier may later add post_integration. Preserve every original key and recursively every original value exactly; no compact replacement, key deletion, nesting rewrite or fixed-count simplification.',
      'post_integration_added_now':False})
    for n in ['original-evidence.raw.json','original-evidence.canonical.json','all-original-keys-retention-contract.json','evidence-preflight.json']:(PUB/n).chmod(0o444)
    print(json.dumps({'preflight':'PASS','actual_API_calls':0,'evidence_raw_sha256':sha(PUB/'original-evidence.raw.json'),'evidence_canonical_sha256':digest(evidence),'original_keys':list(evidence),'protected_file_count':len(protected['files']),'actual_nonempty_family_counts':protected['families']},indent=2))

def execute_once():
    assert not (PRIVATE/'normal-api-attempt-started.json').exists(),'An attempt may already have occurred; inspect ledger, never repeat automatically'
    evidence=load(PUB/'original-evidence.raw.json'); pre=load(PUB/'evidence-preflight.json')
    before=(PRIVATE/'ledger.before.raw.jsonl').read_bytes()
    assert LEDGER.read_bytes()==before and head()==CARRIER
    assert advance.current_advances()[ADV]['state']=='PROVED_LOCAL'
    assert load(FRONT)==load(PUB/'own-frontier.before.raw.json')
    assert protected_snapshot()==load(PRIVATE/'protected.before.json')
    write(PRIVATE/'normal-api-attempt-started.json',{'started':now(),'API':'astis_advance.transition_advance','actual_calls_before':0})
    actual_calls=0; out=io.StringIO(); err=io.StringIO(); error=None
    try:
        with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
            actual_calls+=1
            advance.transition_advance(ADV,'VERIFIED',worker_id=VERIFIER,modes=('independent-source-review','independent-native-evidence-preflight'),evidence=evidence)
    except BaseException:
        error=traceback.format_exc()
    (PRIVATE/'api.stdout.txt').write_text(out.getvalue());(PRIVATE/'api.stderr.txt').write_text(err.getvalue())
    if error:(PRIVATE/'api.error.txt').write_text(error)
    after=LEDGER.read_bytes(); assert after.startswith(before),'Prior ledger bytes changed'
    append=after[len(before):]
    (PRIVATE/'ledger.after.raw.jsonl').write_bytes(after)
    write(PRIVATE/'states.after-api.json',advance.current_advances())
    write(PUB/'normal-api-receipt.json',{'API':'tools.astis_advance.transition_advance','advance_id':ADV,'worker_id':VERIFIER,
      'from_state':'PROVED_LOCAL','to_state':'VERIFIED','actual_API_calls':actual_calls,'success':error is None,
      'ledger_prefix_unchanged':True,'append_bytes':len(append),'append_sha256':shab(append),
      'stdout_sha256':shab(out.getvalue().encode()),'stderr_sha256':shab(err.getvalue().encode()),
      'error_preserved_privately':error is not None,'finished':now()})
    if error:raise RuntimeError('API failed; actual count and ledger inspected/preserved; no automatic retry')
    events=append.splitlines();assert len(events)==1
    event=json.loads(events[0]);assert event['advance_id']==ADV and event['event']=='transition' and event['from_state']=='PROVED_LOCAL' and event['to_state']=='VERIFIED'
    assert event['worker_id']==VERIFIER and event['evidence']==evidence and canon(event['evidence'])==canon(evidence)
    (PUB/'exact-one-appended-ledger-event.raw.jsonl').write_bytes(append)
    (PUB/'exact-one-appended-ledger-event.canonical.json').write_bytes(canon(event))
    beforestates=load(PRIVATE/'states.before.json');afterstates=advance.current_advances()
    assert {k:v for k,v in beforestates.items() if k!=ADV}=={k:v for k,v in afterstates.items() if k!=ADV}
    assert afterstates[ADV]['state']=='VERIFIED' and afterstates[ADV]['owner_id']==OWNER
    # Normal API inspected: only ledger append occurred; frontier stays untouched until separate closeout.
    oldfront=(PUB/'own-frontier.before.raw.json').read_bytes()
    assert FRONT.read_bytes()==oldfront
    write(PUB/'frontier-closeout.authorization-and-api-observation.json',{
      'normal_API_changed_frontier':False,'separate_closeout_authorized':True,
      'allowed_paths':['/status','/evidence/independent_verification'],'owner_unchanged':OWNER,
      'normal_API_already_succeeded':True,'second_API_or_post_integration_authorized':False})
    f=json.loads(oldfront)
    newtext='Original independent source verifier /root/source_reader_a83e10 completed one normal local PROVED_LOCAL->VERIFIED API after bounded evidence preflight. Source/full-module/provider/private-Test/exposition reviewed at df64aaa6088b6ac88c35696acfed906031964d72; fresh independent producer/fullTest/kernel native and isolated static evidence at df64, eight canonical objects explicitly reused. Accepted-review working-layer four metadata gates ran at HEADdf64 and were carried unchanged at cb761181b45a73fe884d9c7590a8710105a108e1; no fresh gate/native run at carrier claimed. Separate two-role exact-C7 locator overlays preserve original math reviews. Local selected actual-Gaussian norm/SNR and private zero-event scope only; no full tau/shifted/rotated detector/main/oracle/TV/cost/integration/site/browser/publication/purification/whole-Goal credit. Exact original evidence and single ledger event are frozen by this verifier; no post_integration release.'
    oldstatus=f['status'];oldverify=f['evidence']['independent_verification']
    assert oldstatus=='proved_locally' and isinstance(oldverify,str)
    f['status']='independently_verified';f['evidence']['independent_verification']=newtext
    # Text-local replacement preserves all unrelated bytes, ordering and formatting.
    text=oldfront.decode(); a='"status": '+json.dumps(oldstatus);b='"status": '+json.dumps(f['status'])
    assert text.count(a)==1;text=text.replace(a,b,1)
    a='"independent_verification": '+json.dumps(oldverify,ensure_ascii=False);b='"independent_verification": '+json.dumps(newtext,ensure_ascii=False)
    assert text.count(a)==1;text=text.replace(a,b,1)
    assert json.loads(text)==f
    FRONT.write_text(text)
    (PUB/'own-frontier.after.raw.json').write_bytes(FRONT.read_bytes())
    write(PUB/'frontier-closeout.exact-two-field-diff.json',[
      {'path':'/status','before':oldstatus,'after':f['status']},
      {'path':'/evidence/independent_verification','before':oldverify,'after':newtext}])
    restored=copy.deepcopy(f);restored['status']=oldstatus;restored['evidence']['independent_verification']=oldverify
    assert restored==json.loads(oldfront)
    assert f['owner_id']==OWNER
    protectedafter=protected_snapshot();write(PRIVATE/'protected.after.json',protectedafter)
    assert protectedafter==load(PRIVATE/'protected.before.json'),'Protected files changed'
    write(PUB/'own-sau.after.json',afterstates[ADV])
    write(PUB/'preservation-and-scope.json',{
      'actual_API_calls':1,'one_own_ledger_event_appended':True,'exact_before_ledger_is_byte_prefix':True,
      'foreign_SAU_states_unchanged':True,'foreign_frontier_and_tracked_inventory_bytes_unchanged':True,
      'protected_file_count':len(protectedafter['files']),'private_protected_inventory_commitment':digest(protectedafter),
      'actual_nonempty_family_counts':protectedafter['families'],
      'discoveries_unchanged':True,'all_other_frontier_fields_values_and_owner_unchanged':True,
      'own_frontier_only_two_field_closeout':True,'normal_API_auto_frontier_change':False,
      'original_evidence_all_keys_and_nested_values_equal_appended':True,
      'original_evidence_raw_sha256':sha(PUB/'original-evidence.raw.json'),'original_evidence_canonical_sha256':digest(evidence),
      'appended_event_raw_sha256':shab(append),'appended_event_canonical_sha256':digest(event),
      'no_post_integration':True,'no_second_API':True,'no_STAB_global_site_browser_or_Goal_claim':True,
      'private_foreign_raw_snapshots_or_path_inventory_published':False})
    for p in PUB.iterdir():
        if p.is_file():p.chmod(0o444)
    print(json.dumps({'state':'VERIFIED','actual_API_calls':1,'frontier':'independently_verified','frontier_fields_changed':2,'append_sha256':shab(append),'evidence_raw_sha256':sha(PUB/'original-evidence.raw.json'),'evidence_canonical_sha256':digest(evidence),'foreign_and_protected_unchanged':True},indent=2))

if __name__=='__main__':
    try:
        {'preflight':preflight,'execute-once':execute_once}[sys.argv[1]]()
    except BaseException:
        mode=sys.argv[1] if len(sys.argv)>1 else 'launcher'
        (PRIVATE/(mode+'.failure.txt')).write_text(traceback.format_exc())
        raise
