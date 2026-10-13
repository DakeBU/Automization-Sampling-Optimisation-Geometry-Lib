from pathlib import Path
import copy, hashlib, json, os, re, subprocess, sys, time
from datetime import datetime, timezone

ROOT = Path('E:/Samplinglib')
OWN = ROOT / 'runs/20261007-companion-priority/pbps-harmonic-flow-preproof73/independent-header-math73'
PRE = OWN.parent
PY = Path('C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe')
SELF = Path(__file__)
RECIPE = 'CRLF byte pair -> LF only; preserve bare CR and every other byte'

def now(): return datetime.now(timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def canon(x): return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
def write(name, x):
    p = OWN / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(json.dumps(x, ensure_ascii=False, sort_keys=True, indent=2).encode('utf-8') + b'\n')
def read(name): return json.loads((OWN / name).read_bytes())
def pin(p, locator=None):
    b = p.read_bytes()
    return dict(path=locator or p.relative_to(ROOT).as_posix(), RAW_bytes=len(b), RAW_sha256=sha(b),
                LF_sha256=sha(b.replace(b'\r\n', b'\n')), LF_recipe=RECIPE)
def snapshot(p, i, role):
    row = pin(p)
    dest = f'inputs/{i:03d}.exactraw.snapshot'
    (OWN / dest).parent.mkdir(parents=True, exist_ok=True)
    (OWN / dest).write_bytes(p.read_bytes())
    row.update(snapshot=dest, role=role)
    return row
def current_inputs():
    rows = read('inputs.manifest.json')['inputs']
    checked = []
    for row in rows:
        p = ROOT / row['path']
        cur = pin(p)
        assert cur['RAW_sha256'] == row['RAW_sha256'], row['path']
        assert cur['LF_sha256'] == row['LF_sha256'], row['path']
        assert pin(OWN / row['snapshot'])['RAW_sha256'] == row['RAW_sha256']
        checked.append(dict(path=row['path'], current_RAW_equal=True, snapshot_RAW_equal=True))
    return checked
def freeze():
    assert not (OWN / 'lease.final.json').exists()
    dispatch = json.loads((PRE / 'header-math73.dispatch.json').read_bytes())
    paths = [(ROOT / r['path'], 'dispatch exact prospective/source/API input') for r in dispatch['inputs']]
    for p, expected in zip((x[0] for x in paths), dispatch['inputs']):
        actual = pin(p)
        for k in ['RAW_bytes', 'RAW_sha256', 'LF_sha256']: assert actual[k] == expected[k], (p,k)
    extra = [
        (PRE / 'header-math73.dispatch.json', 'dispatch boundary; not source topology authority'),
        (ROOT / 'lean-toolchain', 'fixed Lean toolchain'),
        (ROOT / 'lake-manifest.json', 'fixed dependency manifest'),
        (ROOT / 'AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/Gradient.lean', 'existing C1 gradient continuity API'),
        (ROOT / '.lake/packages/mathlib/Mathlib/MeasureTheory/Constructions/BorelSpace/Basic.lean', 'continuous-to-measurable/product Borel APIs'),
        (ROOT / 'docs/proof-digestion-protocol.md', 'independent topology/source truth policy'),
    ]
    rows = [snapshot(p, i, role) for i, (p, role) in enumerate(paths + extra)]
    write('inputs.manifest.json', dict(input_count=len(rows), dispatch_input_count=12,
          inputs=rows, RAW_authoritative=True, LF_recipe=RECIPE, historical_fallback_used=False))
    head = subprocess.run(['git','rev-parse','HEAD'], cwd=ROOT, capture_output=True, check=True)
    write('lease.open.json', dict(status='OPEN_HEADER_ONLY', actor='/root/exact_science63', opened_utc=now(),
          actual_freezer_PID=os.getpid(), observed_HEAD=head.stdout.decode().strip(),
          commit_bound_verification=False, owned_scope=OWN.relative_to(ROOT).as_posix(),
          sourcegraph_extractor_exposure=True, topology_self_approval=False,
          distinct_topology_verdict_consumed=False, theorem_proof_search=False,
          canonical_Git_ledger_writes=False))
    print(json.dumps(dict(status='FROZEN', actual_PID=os.getpid(), input_count=len(rows),
          input_manifest=pin(OWN/'inputs.manifest.json'), observed_HEAD=head.stdout.decode().strip())))
def make_probe():
    header = (OWN / 'inputs/000.exactraw.snapshot').read_text(encoding='utf-8')
    prefix, public = header.split('theorem actual_harmonic_flow_laws', 1)
    assert public.endswith(' := by\n\n'), repr(public[-40:])
    signature, target = public[:-len(' := by\n\n')].rsplit(' :\n', 1)
    target = target.strip()
    assert target == 'actual_harmonic_flow_statement hα hαβ hV hH hη hβη'
    private_binders = prefix.split('private def actual_harmonic_flow_statement',1)[1].split(' : Prop :=\n',1)[0]
    assert signature == private_binders
    probe = prefix + '\ndef prospective_public_target' + signature + ' : Prop :=\n    ' + target + '\n'
    probe += '\n#check @actual_harmonic_flow_statement\n#check @prospective_public_target\n'
    probe += '#check @AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.continuous_gradient_of_contDiff_one\n'
    probe += '#check @Continuous.measurable\n#check @Real.hasDerivAt_sin\n#check @Real.hasDerivAt_cos\n'
    probe += '\nsection CarrierOnly\nvariable {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℝ F]\n'
    probe += '[FiniteDimensional ℝ F] [MeasurableSpace F] [BorelSpace F]\n'
    probe += '#synth CompleteSpace F\n#synth SecondCountableTopology F\n'
    probe += '#synth BorelSpace (F × F)\n#synth BorelSpace ((F × F) × ℝ × (F × F))\n'
    probe += 'end CarrierOnly\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow\n'
    assert not re.search(r'\b(sorry|admit|axiom|unknownTACTIC)\b|:=\s*by', probe)
    (OWN/'HeaderOnlyCheck73.lean').write_bytes(probe.encode('utf-8'))
    write('type-representation.map.json', dict(
        status='DEFINITIONS_AND_API_FORMATION_ONLY_NO_THEOREM_PROOF',
        candidate=pin(OWN/'inputs/000.exactraw.snapshot'), probe=pin(OWN/'HeaderOnlyCheck73.lean'),
        private_complete_Prop_body_exact_UTF8=True, public_private_binder_blocks_exact=True,
        public_theorem_replaced_with_Prop_valued_def=True, target_application_exact=target,
        no_proof_of_target=True, no_hole_or_axiom_or_tactic_skeleton=True,
        namespace_close_added=True, canonical_header_contains_only_unproved_terminal_by=True,
        canonical_header_not_compilation_certificate=True))
def check():
    before = current_inputs()
    make_probe()
    argv = ['lake','env','lean',str(OWN/'HeaderOnlyCheck73.lean')]
    start = now()
    with (OWN/'typecheck.stdout.log').open('wb') as out, (OWN/'typecheck.stderr.log').open('wb') as err:
        proc = subprocess.Popen(argv, cwd=ROOT, stdout=out, stderr=err)
        pid = proc.pid
        print(json.dumps(dict(status='RUNNING_TYPE_FORMATION_ONLY', actual_foreground_PID=pid, runner_PID=os.getpid())), flush=True)
        code = proc.wait()
    write('typecheck.receipt.json', dict(command=argv, actual_foreground_PID=pid, runner_PID=os.getpid(),
          started_utc=start, ended_utc=now(), exit_code=code, terminal_closed=True,
          fresh_Lean_process=True, Lake_build_cache_replay=False, target_theorem_proved=False,
          proof_search=False, output_olean_requested=False,
          before_inputs=before, after_inputs=current_inputs(), stdout=pin(OWN/'typecheck.stdout.log'),
          stderr=pin(OWN/'typecheck.stderr.log'), probe=pin(OWN/'HeaderOnlyCheck73.lean')))
    print(json.dumps(dict(status='TERMINAL_TYPE_FORMATION', actual_foreground_PID=pid, exit_code=code)))
    return code
def all_owned(exclude=()):
    return [pin(p) for p in sorted(OWN.rglob('*')) if p.is_file() and p.relative_to(OWN).as_posix() not in exclude]
def finalize():
    assert read('decision.json')['accepted_prospectively']
    assert read('typecheck.receipt.json')['exit_code'] == 0
    checks=current_inputs()
    write('final-core-readback.json',dict(status='ALL_FROZEN_CURRENT_INPUTS_EXACT',input_count=len(checks),rows=checks))
    outputs=all_owned(exclude=('outputs.manifest.json','run.json','complete-named-header-review.payload.json','lease.final.json'))
    write('outputs.manifest.json',dict(status='FINALIZATION_BASELINE_FINAL_LEASE_BINDS_ALL_LATER_SELF_TERMINALS',file_count=len(outputs),files=outputs))
    payload=dict(payload_name='COMPLETE_INDEPENDENT_PROSPECTIVE_HEADER_MATH73_REVIEW',
        actor='/root/exact_science63', input_manifest=read('inputs.manifest.json'),
        mathematical_review=read('mathematical-review.json'), decision=read('decision.json'),
        type_representation=read('type-representation.map.json'), typecheck=read('typecheck.receipt.json'),
        final_readback=read('final-core-readback.json'), outputs_manifest=read('outputs.manifest.json'),
        closure_policy='Final lease binds every owned file, including all self and actual terminal layers. No native scope reopened.')
    write('complete-named-header-review.payload.json',payload)
    run=dict(schema='independent-prospective-header-math73/v1',status='ACCEPTED_PROSPECTIVE_HEADER_ONLY',
        actor='/root/exact_science63',observed_HEAD=read('lease.open.json')['observed_HEAD'],
        commit_bound_verification=False,exact_header=pin(OWN/'inputs/000.exactraw.snapshot'),
        input_manifest=pin(OWN/'inputs.manifest.json'),complete_named_RAW_payload=pin(OWN/'complete-named-header-review.payload.json'),
        output_manifest=pin(OWN/'outputs.manifest.json'),decision=pin(OWN/'decision.json'),
        fresh_typecheck=read('typecheck.receipt.json'),
        hash_recipe='canonical UTF8 JSON ensure_ascii=false sort_keys=true separators comma/colon, delete ONLY top-level run_sha256',
        final_lease_binding='all owned files except lease itself; separate lease RAW hash returned externally',
        proof_source_topology_and_VERIFIED_credit=False)
    run['run_sha256']=sha(canon(run))
    write('run.json',run)
    print(json.dumps(dict(actual_PID=os.getpid(),run_sha256=run['run_sha256'],named_RAW=pin(OWN/'complete-named-header-review.payload.json'))))
def readback():
    run=read('run.json'); claimed=run.pop('run_sha256'); assert sha(canon(run))==claimed
    assert pin(OWN/'complete-named-header-review.payload.json')['RAW_sha256']==run['complete_named_RAW_payload']['RAW_sha256']
    current_inputs()
    print(json.dumps(dict(status='READBACK_PASS',actual_PID=os.getpid(),run_sha256=claimed,named_RAW_sha256=run['complete_named_RAW_payload']['RAW_sha256'])))
def close():
    assert not (OWN/'lease.final.json').exists()
    readback()
    # A separate actual foreground probe emits terminal evidence before the lease is written last.
    launch('close-probe')
    rows=all_owned(exclude=('lease.final.json',))
    write('lease.final.json',dict(status='CLOSED_LAST',actor='/root/exact_science63',closed_utc=now(),
        actual_close_writer_PID=os.getpid(),nonself_file_count=len(rows),file_count_including_lease=len(rows)+1,
        files=rows,all_nonself_logical_manifest_sha256=sha(canon(rows)),run_sha256=read('run.json')['run_sha256'],
        complete_named_RAW_payload=pin(OWN/'complete-named-header-review.payload.json'),
        final_owned_write=True,postclose_owned_writes_forbidden=True,all_prior_launched_sessions_closed_before_lease=True,
        close_writer_terminal_exit_observed_only_externally_after_lease=True))
    print(json.dumps(dict(status='CLOSED_LAST',actual_close_writer_PID=os.getpid(),lease=pin(OWN/'lease.final.json'),file_count=len(rows)+1)))
def postclose():
    lease=read('lease.final.json'); rows=all_owned(exclude=('lease.final.json',))
    assert rows==lease['files']; assert sha(canon(rows))==lease['all_nonself_logical_manifest_sha256']
    readback()
    print(json.dumps(dict(status='READ_ONLY_POSTCLOSE_PASS',actual_PID=os.getpid(),file_count=len(rows)+1,
         lease=pin(OWN/'lease.final.json'),closure_sha256=lease['all_nonself_logical_manifest_sha256'],owned_writes=False)))
def launch(action):
    assert not (OWN/'lease.final.json').exists()
    (OWN/f'{action}.executed-helper.RAW.py').write_bytes(SELF.read_bytes())
    argv=[str(PY),'-B','-X','utf8',str(SELF),'_child',action]
    started=now()
    with (OWN/f'{action}.stdout.log').open('wb') as out,(OWN/f'{action}.stderr.log').open('wb') as err:
        p=subprocess.Popen(argv,cwd=ROOT,stdout=out,stderr=err)
        print(json.dumps(dict(status='RUNNING',action=action,actual_PID=p.pid,runner_PID=os.getpid())),flush=True)
        code=p.wait()
    write(f'{action}.receipt.json',dict(action=action,command=argv,actual_PID=p.pid,runner_PID=os.getpid(),
        exit_code=code,terminal_closed=True,started_utc=started,ended_utc=now(),
        stdout=pin(OWN/f'{action}.stdout.log'),stderr=pin(OWN/f'{action}.stderr.log'),executed_helper=pin(OWN/f'{action}.executed-helper.RAW.py')))
    print(json.dumps(dict(status='TERMINAL',action=action,actual_PID=p.pid,exit_code=code)))
    return code

if __name__=='__main__':
    act=sys.argv[-1]
    if sys.argv[1]=='_child':
        if act=='close-probe':
            readback(); print(json.dumps(dict(status='CLOSE_PROBE_PASS',actual_PID=os.getpid())))
            sys.exit(0)
        result=globals()[act](); sys.exit(result or 0)
    elif act in ('close','postclose'): globals()[act]()
    else: sys.exit(launch(act))
