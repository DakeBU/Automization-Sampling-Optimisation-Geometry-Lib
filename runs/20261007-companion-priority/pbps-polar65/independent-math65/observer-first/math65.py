import datetime, hashlib, json, os, pathlib, re, subprocess, sys, traceback
R=pathlib.Path('E:/Samplinglib')
O=pathlib.Path(__file__).resolve().parent
D=R/'runs/20261007-companion-priority/pbps-polar65'
P=R/'runs/20261007-companion-priority/pbps-polar-preproof65'
BASE='0aef19ca2711159eeaec86d42c9be142a94fa402'
ACTOR='/root/exact_science63'
TARGETS=['AutoSamplingTheory/ExampleCases/ProximalBPS/PolarIsometry.lean','Tests/ProximalBPSPolarIsometry.lean']
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def canonical(o): return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def write(name,obj):
    p=O/name; p.parent.mkdir(parents=True,exist_ok=True)
    p.write_bytes((json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode('utf-8'))
def read(p): return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))
def pin(p):
    p=pathlib.Path(p); b=p.read_bytes(); l=b.replace(b'\r\n',b'\n')
    return {'path':p.as_posix(),'raw_bytes':len(b),'raw_sha256':sha(b),'lf_bytes':len(l),'lf_sha256':sha(l)}
def matching(actual,expected):
    assert actual['raw_sha256']==expected['raw_sha256'],(actual['path'],'RAW',actual['raw_sha256'],expected['raw_sha256'])
    assert actual['raw_bytes']==expected.get('raw_bytes',expected.get('bytes',actual['raw_bytes']))
    if 'lf_sha256' in expected: assert actual['lf_sha256']==expected['lf_sha256']
def git(*args):
    q=subprocess.run(['git',*args],cwd=R,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
    return q.stdout
def inputs_current():
    m=read(O/'inputs.manifest.json')
    result=[]
    for item in m['inputs']:
        actual=pin(item['resolved_path']); matching(actual,item)
        result.append(actual)
    assert git('rev-parse','HEAD').decode().strip()==BASE
    return result
def freeze():
    assert not (O/'lease.open.json').exists(),'new owned scope must be empty except helper'
    write('lease.open.json',{'schema':'independent-math65-lease-v1','status':'OPEN','actor':ACTOR,'owned_prefix':O.as_posix(),'opened_utc':now(),'actual_pid':os.getpid(),'checked_base_commit':BASE,'phase':'PRECOMMIT','canonical_Git_ledger_writes':False})
    head=git('rev-parse','HEAD').decode().strip(); assert head==BASE
    frozen=read(D/'math-freeze.json'); assert frozen['checked_base_commit']==BASE
    hist=D/'audit.0.before-decoder.exactraw.snapshot.json'
    rows=[]; seen=set(); maps=[]
    def add(path,expected=None,role='scoped-current'):
        path=pathlib.Path(path)
        if path.as_posix() in seen:return
        v=pin(path)
        if expected:matching(v,expected)
        v.update(resolved_path=path.as_posix(),role=role); rows.append(v);seen.add(path.as_posix())
    for f in frozen['inputs']:
        p=pathlib.Path(f['path'])
        if pin(p)['raw_sha256']!=f['raw_sha256']:
            assert p.name=='ASTIS-RT-20261009-PBPSActualPolarIsometry.json','no arbitrary historical fallback'
            add(hist,f,'finite-explicit-original-draft-audit-snapshot')
            maps.append({'claimed_original_path':p.as_posix(),'claimed_RAW_sha256':f['raw_sha256'],'resolved_exact_RAW_snapshot':pin(hist),'current_audit_not_consumed_as_math_or_source_verdict':True,'authority':'parent explicit draft-before-decoder snapshot mapping'})
        else:add(p,f,'root-math-freeze-input')
    add(D/'math-freeze.json')
    for f in ['AGENTS.md','CONTRIBUTING.md','docs/theorem-publication-protocol.md','docs/proof-digestion-protocol.md','docs/evidence-routed-memory-protocol.md','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','.agents/skills/astis-substantive-advance/SKILL.md','.agents/skills/astis-semantic-roundtrip/SKILL.md','tools/astis.py']:
        if (R/f).is_file():add(R/f,role='protocol-or-scanner')
    parent=R/'runs/20261007-companion-priority/pbps-centered-root64'
    for f in ['root.exact-verification64.adoption.json','verified.json','exact-science-verification/lease.json','exact-science-verification/verdict.json','repository-exposition64/lease.json']:
        add(parent/f,role='accepted64-bounded-parent-capsule')
    for folder in ['independent-primary65','independent-header65']:
        for name in ['owned-manifest.json','lease.final.json','raw-review-binding.json','source-inputs.json','review-run.json']:
            if (P/folder/name).is_file():add(P/folder/name,role='closed-source-first-seal-native-binding')
    primary=P/'independent-primary65'
    sin=read(primary/'source-inputs.json')
    add(sin['primary_path'],{'raw_bytes':sin['primary_raw_bytes'],'raw_sha256':sin['primary_raw_sha256']},'exact-primary-HTML')
    for s in sin['named_raw_input_payload']['segment_map']:
        for key in ['raw_snapshot','lf_snapshot','rendered_snapshot']:add(primary/s[key],role='finite-primary-region')
    add(primary/sin['named_raw_input_payload']['filename'],role='complete-named-RAW-primary-input')
    negatives=[]
    for n in range(1,6):
        p=D/f'focused65-v{n}'/'receipt.json'
        v=read(p);negatives.append({'version':n,'receipt':pin(p),'actual_pid':v.get('actual_foreground_pid'),'exit_code':v.get('exit_code'),'terminal_closed':v.get('terminal_closed'),'proof_credit':False})
        for name in ['receipt.json','stdout.log','stderr.log']:add(p.parent/name,role='retained-root-negative-no-proof-credit')
    for name in ['adjoint-typed-congruence65.diagnosis.json','ext-depth65.diagnosis.json','residual-map-sub65.diagnosis.json','test-local-types65.diagnosis.json','focused65-v1.failed-production.exactraw.snapshot']:
        add(D/name,role='retained-root-negative-diagnosis')
    local={};todo=TARGETS.copy()
    while todo:
        f=todo.pop()
        if f in local:continue
        b=(R/f).read_text(encoding='utf-8-sig');im=re.findall(r'^import\s+(\S+)',b,re.M);local[f]=im
        add(R/f,role='candidate-or-local-transitive-Lean-import')
        for x in im:
            q=x.replace('.','/')+'.lean'
            if q.startswith(('AutoSamplingTheory/','Tests/')):todo.append(q)
    for f in ['Analysis/InnerProductSpace/Adjoint.lean','Analysis/Normed/Operator/Basic.lean','Topology/Algebra/Module/ContinuousLinearMap/Restrict.lean','Topology/Algebra/Module/ContinuousLinearMap/Basic.lean','Analysis/InnerProductSpace/Positive.lean']:
        add(R/'.lake/packages/mathlib/Mathlib'/f,role='actual-used-Mathlib-API')
    parentpath='AutoSamplingTheory/ExampleCases/ProximalBPS/CenteredRootOrderInverse.lean'
    blob=git('show',BASE+':'+parentpath);current=(R/parentpath).read_bytes()
    assert blob==current,'actual64 parent exact Git RAW equality'
    assert sha(current)=='3c4f72ef44868fe2ebca6842192ee4a9cea1db4527ae29dccdec691004e6daa6'
    for f in TARGETS:
        result=subprocess.run(['git','cat-file','-e',BASE+':'+f],cwd=R,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        assert result.returncode!=0,'precommit files unexpectedly in checked base'
    for i,f in enumerate(TARGETS):
        b=(R/f).read_bytes();(O/f'candidate{i}.exactraw.snapshot').write_bytes(b)
    write('inputs.manifest.json',{'schema':'math65-bounded-inputs-v1','checked_BASE':BASE,'phase':'PRECOMMIT_UNCOMMITTED_CANDIDATES','candidate_files':TARGETS,'candidate_not_in_base':True,'inputs':rows,'input_count':len(rows),'finite_historical_resolutions':maps,'no_blanket_snapshot_fallback':True,'no_ledger_or_historical_review_copies':True,'actual64_Git_RAW_equality':{'path':parentpath,'base_blob_RAW_sha256':sha(blob),'current_RAW_sha256':sha(current),'equal':True},'local_Lean_import_graph':local,'root_negative_runs_retained':negatives,'source65_decoder_and_anti_anchored_source_verdicts_not_consumed':True,'actual_freezer_pid':os.getpid()})
    print(json.dumps({'status':'FROZEN','actual_pid':os.getpid(),'input_count':len(rows),'historical_maps':len(maps),'local_import_files':len(local),'BASE':BASE}),flush=True)
def build():
    pre=inputs_current();started=now()
    write('focused.pre.json',{'actual_runner_pid':os.getpid(),'started_utc':started,'input_pins':pre,'checked_BASE':BASE})
    env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
    with (O/'focused.stdout.log').open('wb') as out,(O/'focused.stderr.log').open('wb') as err:
        proc=subprocess.Popen(['lake','build','Tests.ProximalBPSPolarIsometry'],cwd=R,stdout=out,stderr=err,env=env)
        print(json.dumps({'event':'START','actual_lake_pid':proc.pid,'actual_runner_pid':os.getpid(),'command':['lake','build','Tests.ProximalBPSPolarIsometry']}),flush=True)
        code=proc.wait()
    post=inputs_current();txt=(O/'focused.stdout.log').read_text(encoding='utf-8-sig')
    declarations=re.findall(r"info: (AutoSamplingTheory/ExampleCases/ProximalBPS/PolarIsometry\.lean|Tests/ProximalBPSPolarIsometry\.lean):.*?\n([^\n]+).*?depends on axioms: \[([^\]]+)\]",txt,re.S)
    # Lake replay info may print the declaration and axiom array on one or multiple lines.
    axiom_lines=[l for l in txt.splitlines() if 'depends on axioms' in l and ('actual_centered_polar_isometry' in l or 'genuine_actual_polar_corrector_consumer' in l)]
    standard="[propext, Classical.choice, Quot.sound]"
    expected=['AutoSamplingTheory.ExampleCases.ProximalBPS.PolarIsometry.actual_centered_polar_isometry','Tests.ProximalBPSPolarIsometry.genuine_actual_polar_corrector_consumer']
    for d in expected:assert re.search(re.escape(d)+r"'? depends on axioms: \[propext, Classical.choice, Quot.sound\]",txt),('missing standard3',d)
    jobs=re.findall(r'Build completed successfully \((\d+) jobs\)',txt)
    assert code==0 and jobs==['3945'],(code,jobs)
    receipt={'schema':'independent-math65-focused-v1','command':['lake','build','Tests.ProximalBPSPolarIsometry'],'nonforced_invocations':1,'actual_runner_pid':os.getpid(),'actual_foreground_lake_pid':proc.pid,'exit_code':code,'terminal_closed':True,'started_utc':started,'finished_utc':now(),'checked_BASE':BASE,'candidate_commit':None,'phase':'PRECOMMIT','jobs':int(jobs[0]),'standard3_declarations':expected,'axiom_evidence_lines':axiom_lines,'pre_pins':pre,'post_pins':post,'all_inputs_RAW_LF_unchanged':pre==post,'stdout':pin(O/'focused.stdout.log'),'stderr':pin(O/'focused.stderr.log')}
    assert pre==post
    write('focused.result.json',receipt)
    print(json.dumps({'event':'TERMINAL','actual_lake_pid':proc.pid,'exit_code':code,'jobs':3945,'standard3':2,'all_inputs_unchanged':True}),flush=True)
def verify_run(p):
    j=read(p);h=j.pop('run_sha256');assert sha(canonical(j))==h,(str(p),'logical run');return h
def native(folder):
    man=read(folder/'owned-manifest.json');entries=man['all_preclosure_owned_files']+man['closure_files'];checked=[]
    for x in entries:
        assert isinstance(x,dict),(folder,'closure entry shape')
        q=folder/x['filename'];matching(pin(q),x);checked.append(x['filename'])
    lease=read(folder/'lease.final.json');assert lease['status']=='CLOSED_LAST'
    binding=read(folder/'raw-review-binding.json');matching(pin(folder/binding['filename']),binding)
    whole=verify_run(folder/'review-run.json')
    assert whole==lease['run_sha256']
    return {'folder':folder.as_posix(),'checked_native_files':len(checked),'native_owned_file_count':man['final_owned_file_count'],'owned_manifest':pin(folder/'owned-manifest.json'),'lease':pin(folder/'lease.final.json'),'status':'CLOSED_LAST','whole_logical_run_sha256':whole,'complete_named_RAW_REVIEW':pin(folder/binding['filename']),'all_manifest_RAW_LF_bindings_valid':True}
def check():
    inputs_current();native_results=[native(P/x) for x in ['independent-primary65','independent-header65']]
    sin=read(P/'independent-primary65/source-inputs.json');full=pathlib.Path(sin['primary_path']).read_bytes();payload=(P/'independent-primary65'/sin['named_raw_input_payload']['filename']).read_bytes();segments=[]
    assert sha(payload)==sin['named_raw_input_payload']['sha256']
    for s in sin['named_raw_input_payload']['segment_map']:
        a,z=s['source_byte_range'];region=full[a:z];raw=(P/'independent-primary65'/s['raw_snapshot']).read_bytes();lf=(P/'independent-primary65'/s['lf_snapshot']).read_bytes()
        assert region==raw and raw.replace(b'\r\n',b'\n')==lf
        assert sha(raw)==s['raw_sha256'] and sha(lf)==s['lf_sha256']
        assert payload[s['body_byte_start']:s['body_byte_end_exclusive']]==raw
        segments.append({'name':s['name'],'source_byte_range':s['source_byte_range'],'raw_bytes':len(raw),'raw_sha256':sha(raw),'lf_sha256':sha(lf),'complete_payload_body_exact':True})
    seals=[]
    for i,f in enumerate(TARGETS):
        b=(R/f).read_bytes();header=b[b.index(b'theorem '):b.index(b':= by')].rstrip(b'\r\n ')
        sealed=(P/f'header{i}.lean').read_bytes().rstrip(b'\r\n ')
        assert header==sealed,('header mismatch',i)
        seals.append({'candidate':f,'sealed_header':pin(P/f'header{i}.lean'),'candidate_header_bytes':len(header),'candidate_header_RAW_sha256':sha(header),'exact_header_equality_after_only_trailing_delimiter_whitespace':True})
    exp=read(D/'exposition.draft.json');steps=[s for u in exp['units'] for s in u['steps']];assert len(steps)==5;matches=[]
    for i,s in enumerate(steps):
        x=s['lean_source_region'];p=R/x['path'];b=p.read_bytes();assert sha(b)==x['source_raw_sha256']
        raw=b''.join(b.splitlines(keepends=True)[x['start_line']-1:x['end_line']]);assert sha(raw)==x['exact_code_raw_sha256'],('span digest',i)
        assert raw.decode('utf-8')==s['lean'],('literal span',i)
        bodystart=b[:b.index(b':= by')].count(b'\n')+1;assert x['start_line']>bodystart
        assert b[b.index(b':= by')+len(b':= by'):].find(raw)>=0
        matches.append({'step':i+1,'title':s['title'],'whole_source_RAW_sha256':sha(b),'start_line':x['start_line'],'end_line':x['end_line'],'literal_BODY_span_RAW_sha256':sha(raw),'literal_BODY_bytes':len(raw),'literal_exact':True,'after_theorem_BODY':True,'digest_scope':'line span; distinct from whole source RAW'})
    sys.path.insert(0,str(R/'tools'));import astis
    hits=astis.forbidden_pattern_hits();focus=[x for x in hits if any(f in str(x).replace('\\','/') for f in TARGETS)]
    assert not focus,focus
    scans=[]
    for f in TARGETS:
        t=(R/f).read_text(encoding='utf-8');assert not re.search(r'(?m)^\s*(?:private\s+)?(?:axiom|opaque|unsafe|def|abbrev|instance|lemma)\s',t)
        assert not re.search(r'\b(sorry|admit)\b|Prop\s*:=\s*True|:=\s*trivial|\b(?:native_decide|run_tac|elab|macro)\b',t)
        imports=re.findall(r'^import\s+(\S+)',t,re.M);decl=re.findall(r'^theorem\s+(\S+)',t,re.M);assert len(imports)==1 and len(decl)==1
        scans.append({'path':f,'imports':imports,'theorems':decl,'private_providers':0,'fake_closure_hits':[],'new_declarations':1})
    write('checks.result.json',{'status':'PASS','actual_checker_pid':os.getpid(),'inputs_unchanged':True,'native_source_first_initial_seal_bindings':native_results,'primary_regions_exact_RAW_LF':segments,'primary_complete_named_RAW_INPUT_payload':pin(P/'independent-primary65'/sin['named_raw_input_payload']['filename']),'header_seals':seals,'literal_BODY_steps':matches,'all5_literal_BODY_matches':True,'focused_scans':scans,'astis_global_forbidden_pattern_hit_count':len(hits),'new_files_forbidden_hits':focus,'source65_independent_verdicts_not_consumed':True,'actual64_parent_reused_by_exact_Git_RAW_pin':True})
    print(json.dumps({'status':'PASS','actual_pid':os.getpid(),'literal_BODY_matches':len(matches),'native_initial_reviews':len(native_results),'new_declarations':2,'private_providers':0}),flush=True)
if __name__=='__main__':
    mode=sys.argv[1]
    try:globals()[mode]()
    except Exception as e:
        write(mode+'.failure.json',{'status':'FAIL','stage':mode,'actual_pid':os.getpid(),'utc':now(),'exception':repr(e),'traceback':traceback.format_exc(),'no_proof_credit':True})
        raise
