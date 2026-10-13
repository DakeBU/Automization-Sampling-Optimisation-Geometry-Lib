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
def make_probe(probe_name='HeaderOnlyCheck73.lean'):
    header = (OWN / 'inputs/000.exactraw.snapshot').read_text(encoding='utf-8')
    prefix, public = header.split('theorem actual_harmonic_flow_laws', 1)
    assert public.endswith(' := by\n'), repr(public[-40:])
    signature, target = public[:-len(' := by\n')].rsplit(' :\n', 1)
    target = target.strip()
    assert target == 'actual_harmonic_flow_statement hα hαβ hV hH hη hβη'
    private_binders = prefix.split('private def actual_harmonic_flow_statement',1)[1].split(' : Prop :=\n',1)[0]
    assert signature == private_binders
    probe = prefix + '\ndef prospective_public_target' + signature + ' : Prop :=\n    ' + target + '\n'
    probe += '\n#check @actual_harmonic_flow_statement\n#check @prospective_public_target\n'
    probe += '#check @AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.continuous_gradient_of_contDiff_one\n'
    probe += '#check @Continuous.measurable\n#check @Real.hasDerivAt_sin\n#check @Real.hasDerivAt_cos\n'
    probe += '\nsection CarrierOnly\nvariable {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℝ F]\n'
    probe += '    [FiniteDimensional ℝ F] [MeasurableSpace F] [BorelSpace F]\n'
    probe += '#synth CompleteSpace F\n#synth SecondCountableTopology F\n'
    probe += '#synth BorelSpace (F × F)\n#synth BorelSpace ((F × F) × ℝ × (F × F))\n'
    probe += 'end CarrierOnly\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow\n'
    assert not re.search(r'\b(sorry|admit|axiom|unknownTACTIC)\b|:=\s*by', probe)
    (OWN/probe_name).write_bytes(probe.encode('utf-8'))
    write('type-representation.map.json', dict(
        status='DEFINITIONS_AND_API_FORMATION_ONLY_NO_THEOREM_PROOF',
        candidate=pin(OWN/'inputs/000.exactraw.snapshot'), probe=pin(OWN/probe_name),
        private_complete_Prop_body_exact_UTF8=True, public_private_binder_blocks_exact=True,
        public_theorem_replaced_with_Prop_valued_def=True, target_application_exact=target,
        no_proof_of_target=True, no_hole_or_axiom_or_tactic_skeleton=True,
        namespace_close_added=True, canonical_header_contains_only_unproved_terminal_by=True,
        canonical_header_not_compilation_certificate=True))
def check(tag='typecheck', probe_name='HeaderOnlyCheck73.lean'):
    before = current_inputs()
    make_probe(probe_name)
    argv = ['lake','env','lean',str(OWN/probe_name)]
    start = now()
    with (OWN/f'{tag}.stdout.log').open('wb') as out, (OWN/f'{tag}.stderr.log').open('wb') as err:
        proc = subprocess.Popen(argv, cwd=ROOT, stdout=out, stderr=err)
        pid = proc.pid
        print(json.dumps(dict(status='RUNNING_TYPE_FORMATION_ONLY', actual_foreground_PID=pid, runner_PID=os.getpid())), flush=True)
        code = proc.wait()
    write(f'{tag}.receipt.json', dict(command=argv, actual_foreground_PID=pid, runner_PID=os.getpid(),
          started_utc=start, ended_utc=now(), exit_code=code, terminal_closed=True,
          fresh_Lean_process=True, Lake_build_cache_replay=False, target_theorem_proved=False,
          proof_search=False, output_olean_requested=False,
          before_inputs=before, after_inputs=current_inputs(), stdout=pin(OWN/f'{tag}.stdout.log'),
          stderr=pin(OWN/f'{tag}.stderr.log'), probe=pin(OWN/probe_name)))
    print(json.dumps(dict(status='TERMINAL_TYPE_FORMATION', actual_foreground_PID=pid, exit_code=code)))
    return code
def check2():
    write('observer-negative.json',dict(status='RETAINED_HELPER_PARSE_ASSERTION_ONLY',
          actual_PID=read('check.receipt.json')['actual_PID'],exit_code=1,
          compiler_started=False,canonical_header_changed=False,
          diagnosis='Helper expected two final LF characters; actual exact candidate has one final LF. Corrected only local slicing assertion.',
          failed_executed_helper=pin(OWN/'check.executed-helper.RAW.py'),stderr=pin(OWN/'check.stderr.log')))
    return check()
def check3():
    (OWN/'type-representation.v1.map.json').write_bytes((OWN/'type-representation.map.json').read_bytes())
    write('probe-syntax-negative.json',dict(status='RETAINED_EXTRA_API_PROBE_SYNTAX_FAILURE',
        actual_foreground_PID=read('typecheck.receipt.json')['actual_foreground_PID'],exit_code=1,
        target_Prop_and_public_type_formation_reported_before_error=True,
        target_theorem_not_proved=True,canonical_header_changed=False,
        diagnosis='Own appended variable command continuation needed indentation and candidate noncomputable section needed a separate closing end.',
        failed_probe=pin(OWN/'HeaderOnlyCheck73.lean'),failed_receipt=pin(OWN/'typecheck.receipt.json'),
        stdout=pin(OWN/'typecheck.stdout.log'),stderr=pin(OWN/'typecheck.stderr.log')))
    return check('v2.typecheck','HeaderOnlyCheck73V2.lean')
def synthesis():
    assert read('v2.typecheck.receipt.json')['exit_code']==0
    header=(OWN/'inputs/000.exactraw.snapshot').read_bytes()
    text=header.decode('utf-8')
    prefix=text.split('theorem actual_harmonic_flow_laws',1)[0]
    matches=list(re.finditer(r'^    (?:Continuous|Measurable|\(∀)',prefix,re.M))
    assert len(matches)==9
    clauses=[]
    labels=['joint continuity','joint measurability','time zero','composition s after t',
            'two-sided inverse','both actual ODE derivatives','energy nonnegative','energy invariant','pi endpoint']
    for i,m in enumerate(matches):
        end=matches[i+1].start() if i+1<len(matches) else len(prefix.rstrip())
        b0=len(prefix[:m.start()].encode('utf-8')); b1=len(prefix[:end].encode('utf-8'))
        raw=header[b0:b1]
        clauses.append(dict(index=i+1,label=labels[i],RAW_byte_start_inclusive=b0,RAW_byte_end_exclusive=b1,
             literal_span_RAW_sha256=sha(raw),literal_UTF8=raw.decode('utf-8')))
    write('header.structural-audit.json',dict(status='EXACT_FULL_PRIVATE_LITERAL_PUBLIC_APPLICATION_CHECKED',
        header=pin(OWN/'inputs/000.exactraw.snapshot'),conjunct_count=9,clauses=clauses,
        let_definitions=['c(y,xRef)=y-η•gradient V xRef','literal Φ with actual same c and η','weighted sum H'],
        six_callers=['hα','hαβ','hV','hH','hη','hβη'],extra_public_logical_premises=0,
        complete_private_public_binder_blocks_exact=True,no_target_proof_present=True))
    review=dict(status='PROSPECTIVELY_SOUND_CONTRACT_TYPE_FORMATION_ONLY',
        reviewed_header=pin(OWN/'inputs/000.exactraw.snapshot'),
        reviewer_exposure=dict(actor='/root/exact_science63',prior_sourcegraph_extractor=True,
             self_topology_coverage_approval=False,distinct_primary73_verdict_consumed=False,
             header_first_consumed_after_sourcegraph_CLOSED49=True),
        representation=dict(kind='complete literal private Prop specification',
             public_application='actual_harmonic_flow_statement hα hαβ hV hH hη hβη',
             exact_same_binders=True,provider_or_extra_premise=False,
             proof_formation_probe='private Prop plus same-binder Prop-valued public type; no theorem or tactic body',
             initial_root_typing_different_RAW='9762ae48420d4ed39bdba3b439b1a07216e7661d459b277c167fd0d2244b95eb',
             root_old_comment_equivalence_claim_not_needed_for_fresh_current_check=True),
        actual_objects=dict(center='c=y−η•gradient V xRef',
             position='c+cos(t)•(x−c)+(sqrtη*sin(t))•p',
             momentum='(−sin(t)/sqrtη)•(x−c)+cos(t)•p',
             energy='(η⁻¹*‖x−c‖²+‖p‖²)/2',
             same_reference_and_potential_in_both_components=True,
             pair_norm='coordinate product only; H uses literal sum of E-norm squares, never product max norm'),
        quantifiers=dict(y_xRef='arbitrary E values in every clause; not sampled or constrained by a mean premise',
             phase='every z:E×E; its actual position and momentum are used',
             time='all s,t:ℝ; deterministic explicit-flow extension includes negative times, no backwards PDMP claim',
             joint_domain='(E×E)×(ℝ×(E×E)); a.1=(y,xRef),a.2=(t,z)',
             fixed_parameters='V,η fixed; no joint continuity in η at0 asserted'),
        nine_conjunct_review=[
          dict(index=1,verdict='sound',reason='Original hV:C² internally lowers to C¹; existing Gradient.continuous_gradient_of_contDiff_one applies after finite dimension supplies completeness. Scalar trigonometric and vector operations give the required fixed-η joint continuity; no continuity binder added.'),
          dict(index=2,verdict='sound',reason='Finite-dimensional real E is second countable. Fresh instance synthesis produced both product BorelSpace instances. Existing Continuous.measurable needs OpensMeasurableSpace on this domain and BorelSpace on E×E; those are inherited, so measurability is a conclusion, not a premise.'),
          dict(index=3,verdict='sound',reason='sin0=0,cos0=1 leaves exact actual x,p; no chosen flow witness or fallback semantics.'),
          dict(index=4,verdict='sound',reason='With r=sqrtη>0 and a=(x−c)/r, normalized state is (cos(t)a+sin(t)p,−sin(t)a+cos(t)p). Trigonometric addition gives R(s+t)=R(s)R(t), matching Φ(s)(Φ(t)z), all real times.'),
          dict(index=5,verdict='sound',reason='Both orders Φ(−t)Φ(t) and Φ(t)Φ(−t) reduce via the stated group law and zero. This is finite-dimensional literal flow invertibility, no onto polar/L2 assumption.'),
          dict(index=6,verdict='sound',reason='Position derivative equals r times current momentum. Momentum derivative equals −r⁻¹ times current (x−c). Since c=y−r² gradient V xRef, this is exactly −r⁻¹•(current x−y)−r•gradient V xRef. Parentheses and negative sign are correct; derivative evaluated at arbitrary t, reference gradient fixed.'),
          dict(index=7,verdict='sound',reason='η>0 supplies η⁻¹≥0; both squared E norms are nonnegative. This conclusion uses no curvature coercivity or positive energy division.'),
          dict(index=8,verdict='sound',reason='After the same scaling a=(x−c)/r, 2H=‖a‖²+‖p‖². Expanding the two rotated squared norms cancels the mixed inner terms and sin²+cos²=1 leaves the same sum. This describes feasibility only; no future Lean proof is credited.'),
          dict(index=9,verdict='sound',reason='sinπ=0,cosπ=−1 gives exact position 2•c−x and momentum −p; same actual c, no stochastic half-turn kernel concluded.')],
        binders=dict(original_standing_count=6,hessian_expanded_fields=['global lower','global upper'],
             source_internal_quantifiers=['y','xRef','z.1=x','z.2=p'],typing=['E','NormedAddCommGroup E','InnerProductSpace ℝ E','FiniteDimensional ℝ E','MeasurableSpace E','BorelSpace E','V:E→ℝ','α β:NNReal','η:ℝ','s t:ℝ'],
             convenience_or_provider_callers=[],EXCESS_count=0,RULED_count=0,
             unused_standing_parameters_retained='Type expression does not depend on proof terms, so six unused-variable warnings in private Prop are expected; do not remove source standing binders.'),
        boundary_cases=dict(rank0='Legal; all vectors and gradients zero, Φ=id,H=0; no Nontrivial or positive finrank.',
             alpha_eta_one='Legal; no division by1−αη and no strict cap.',
             eta='Source η>0 required; sqrt nonzero follows internally; no η=0 extension.',
             zero_energy='(c,0) fixed; no division by energy.',zero_normal='No normal or bounce in target; future R0=id convention receives no new proof credit.'),
        feasibility_plan_not_proof=['derive sqrtη>0,sqrtη²=η internally','reuse C²→C¹→gradient continuity',
             'apply product Borel and Continuous.measurable','use trigonometric addition for zero/group/inverses',
             'differentiate literal components and substitute actual c','expand weighted sum and cancel inner cross terms','evaluate sinπ/cosπ'],
        mathematical_repair_required=False,minimal_repair_proposal=None,
        excluded_credit=['source topology coverage acceptance','Statement Seal','73 theorem proof or compiled target','SAU claim or VERIFIED',
             'bounce/rate/hazard/clock/path/nonexplosion','Markov/invariance/terminal H kernel or L2 H','B4/main/composition/cost','reader Exposition/PURIFIED/whole paper/Goal'],
        compiler=dict(fresh_receipt=pin(OWN/'v2.typecheck.receipt.json'),actual_foreground_PID=read('v2.typecheck.receipt.json')['actual_foreground_PID'],
             EXIT=0,scope='complete named Prop/public type/API and four carrier instance formation checks only',
             retained_negatives=['helper final-newline assertion PID42676 EXIT1 before compiler',
                  'own appended API probe syntax PID35624 EXIT1; complete target Prop had formed before unrelated probe errors'],
             warnings='six unused proof-parameter warnings; zero errors in repaired probe',
             theorem_axiom_cleanliness_certificate=False))
    write('mathematical-review.json',review)
    decision=dict(status='ACCEPTED_PROSPECTIVE_HEADER_MATH_TYPE_ONLY',accepted_prospectively=True,
         exact_header=pin(OWN/'inputs/000.exactraw.snapshot'),complete_nine_conjuncts=True,
         same_six_original_callers=True,extra_public_premises=0,mathematical_repair_required=False,
         fresh_typecheck_PID=read('v2.typecheck.receipt.json')['actual_foreground_PID'],fresh_typecheck_EXIT=0,
         proof_credit=False,source_topology_self_approval=False,distinct_topology_verdict_consumed=False,
         sourcegraph_extractor_exposure=True,header_sealed=False,SAU_claimed=False,VERIFIED=False,
         header_decision_frozen_before_any_distinct_overlay_review=True,
         review=pin(OWN/'mathematical-review.json'),structural_audit=pin(OWN/'header.structural-audit.json'),
         own_negative_attempts_retained=2,remaining_boundary='actual proof/source-topology/source-fidelity/reader and exact-commit admission remain separate')
    write('header.decision.json',decision)
    print(json.dumps(dict(status=decision['status'],actual_PID=os.getpid(),header_decision=pin(OWN/'header.decision.json'),
          mathematical_review=pin(OWN/'mathematical-review.json'),typecheck_PID=decision['fresh_typecheck_PID'])))
def overlay():
    frozen_header_decision=pin(OWN/'header.decision.json')
    assert frozen_header_decision['RAW_sha256']=='3e283359671467f7e9b8beded781c20f539f1d590953a59f74a7d2691bb51c89'
    proposal_path=PRE/'independent-header-source73/sourcegraph-edge-overlay73/proposal.json'
    assert pin(proposal_path)['RAW_sha256']=='7aa8520d3ee96ee04757f73ef606c5b677eb9819775bc738203469b6aa56f939'
    proposal=json.loads(proposal_path.read_bytes())
    assert proposal['proposal_author']=='independent_primary69'
    primary_path=ROOT/proposal['primary']['path']; primary=primary_path.read_bytes()
    for authority in ('source_graph_input','source_graph_lease','primary'):
        actual=pin(ROOT/proposal[authority]['path'])
        for k in ('RAW_bytes','RAW_sha256','LF_sha256'): assert actual[k]==proposal[authority][k],(authority,k)
    graph=json.loads((ROOT/proposal['source_graph_input']['path']).read_bytes())
    nodes={n['id']:n for n in graph['nodes']}
    assert len(nodes)==23 and len(graph['edges'])==35
    for n in proposal['original_nodes']: assert n==nodes[n['id']]
    assert len(proposal['original_nodes'])==4
    assert [(e['producer'],e['consumer']) for e in proposal['add_only_edges']]==[('SCALE','GROUP'),('ENERGY','ENERGY-NONNEG')]
    oldpairs={(e['producer'],e['consumer']) for e in graph['edges']}
    assert not oldpairs.intersection({('SCALE','GROUP'),('ENERGY','ENERGY-NONNEG')})
    inputs=[snapshot(proposal_path,18,'separately authored frozen two-edge proposal only'),
            snapshot(ROOT/proposal['source_graph_lease']['path'],19,'old CLOSED49 lease read-only identity')]
    ref=pin(primary_path);ref.update(role='immutable exact whole primary reference; only three bounded literal regions copied',
                                   snapshot=None,storage='READ_ONLY_IMMUTABLE_REFERENCE_NO_WHOLE_SOURCE_COPY')
    inputs.append(ref)
    source_checks=[]
    for i,row in enumerate(proposal['exact_source_fragments']):
        start=row['primary_RAW_start_inclusive']; end=row['primary_RAW_end_exclusive']; raw=primary[start:end]
        rp=ROOT/row['RAW']['path']; lp=ROOT/row['LF']['path']
        assert rp.read_bytes()==raw;assert lp.read_bytes()==raw.replace(b'\r\n',b'\n')
        for kind,p in [('RAW',rp),('LF',lp)]:
            actual=pin(p)
            for k in ('RAW_bytes','RAW_sha256','LF_sha256'):assert actual[k]==row[kind][k]
            inputs.append(snapshot(p,20+2*i+(kind=='LF'),'exact bounded source region '+row['source_anchor']+' '+kind))
        assert ('id="'+row['source_anchor']+'"').encode() in raw
        source_checks.append(dict(anchor=row['source_anchor'],RAW_start_inclusive=start,RAW_end_exclusive=end,
             literal_span_RAW_sha256=sha(raw),RAW_exact_primary_slice=True,LF_exact_CRLF_only_recipe=True))
    write('overlay.inputs.manifest.json',dict(input_count=len(inputs),inputs=inputs,LF_recipe=RECIPE,
           no_distinct_author_other_verdict_or_coverage_consumed=True))
    newgraph=copy.deepcopy(graph);newgraph['edges']+=copy.deepcopy(proposal['add_only_edges']);newgraph['edge_count']=37
    unchanged=[k for k in graph if k not in ('edges','edge_count')]
    assert all(newgraph[k]==graph[k] for k in unchanged)
    adjacency={n:[] for n in nodes}; degree={n:0 for n in nodes}
    for e in newgraph['edges']:
        adjacency[e['producer']].append(e['consumer']);degree[e['consumer']]+=1
    queue=[n for n in nodes if degree[n]==0];seen=[]
    while queue:
        n=queue.pop();seen.append(n)
        for child in adjacency[n]:
            degree[child]-=1
            if degree[child]==0:queue.append(child)
    assert len(seen)==23
    repair=dict(status='ACCEPTED_DISTINCT_AUTHOR_TWO_EDGE_OVERLAY_ONLY',accepted=True,
        proposal=pin(proposal_path),proposal_author=proposal['proposal_author'],reviewer='/root/exact_science63',
        original_graph_extractor_exposure=True,reviewer_distinct_from_overlay_author=True,
        header_math_decision_frozen_before_overlay=frozen_header_decision,
        original_graph_coverage_self_approved=False,distinct_source_topology_full_verdict_consumed=False,
        actual_review_PID=os.getpid(),canonical_or_old_closed_graph_modified=False,
        checked_four_original_nodes_exact=True,source_checks=source_checks,
        two_edges=[
          dict(producer='SCALE',consumer='GROUP',accepted=True,source_use_site='S4.E5.m1',
               rationale='The literal restart formula uses sqrtη and η^(-1/2); group composition requires their reciprocal products to be1. The already-present η>0 SCALE bridge supplies this internally. It is missing as an explicit ingredient edge in the original graph, not a new public premise. The proposal’s η=0 real counterexample is valid but outside source and merely explains necessity.',
               anchor_indices=[0,2]),
          dict(producer='ENERGY',consumer='ENERGY-NONNEG',accepted=True,source_use_site='A1.Ex4',
               rationale='Nonnegativity applies to SAME printed H=(η⁻¹‖x−c‖²+‖p‖²)/2, so both its literal definition and positive-η weight are required. Existing STAND-STEP→ENERGY-NONNEG does not replace the ENERGY definition edge. Exact SUM and half coefficient preserved.',
               anchor_indices=[1,2])],
        prospective_patch=dict(added_edges=2,original_edges_retained_exact=True,
             derived_counter_update='/edge_count:35→37 only',other_fields_unchanged=unchanged,
             nodes=23,source_gaps=7,source_coverage_items=79,binder_items=20,
             structural_DAG_check=True,full_topology_coverage_acceptance=False),
        no_new_formula_binder_Lean_provider_or_proof=True,
        credit='Separately authored narrow graph-repair approval only; no approval of original extractor coverage, no theorem proof/source seal/VERIFIED credit')
    write('repair-decision.json',repair)
    assert pin(OWN/'header.decision.json')==frozen_header_decision
    original=read('inputs.manifest.json')['inputs'];union={r['path']:r for r in original+inputs}
    write('inputs.complete-union.manifest.json',dict(input_count=len(union),original_frozen_inputs=18,
          separately_frozen_overlay_inputs=9,inputs=list(union.values()),LF_recipe=RECIPE,
          version_map='All finite current RAW identities exact; no historical fallback or normalization used'))
    write('decision.json',dict(status='ACCEPTED_PROSPECTIVE_HEADER_AND_DISTINCT_TWO_EDGE_REPAIR_ONLY',
          accepted_prospectively=True,header_decision=frozen_header_decision,repair_decision=pin(OWN/'repair-decision.json'),
          target_proof=False,source_topology_full_coverage_approval=False,sourcegraph_extractor_exposure=True,
          canonical_Git_ledger_changes=False,SAU_claimed=False,VERIFIED=False,Goal_complete=False))
    print(json.dumps(dict(status=repair['status'],actual_PID=os.getpid(),repair_decision=pin(OWN/'repair-decision.json'),
          complete_input_count=len(union),header_decision_still_exact=True)))
def complete_current_inputs():
    checks=[]
    for row in read('inputs.complete-union.manifest.json')['inputs']:
        cur=pin(ROOT/row['path'])
        for k in ('RAW_bytes','RAW_sha256','LF_sha256'):assert cur[k]==row[k],(row['path'],k)
        if row.get('snapshot'):assert pin(OWN/row['snapshot'])['RAW_sha256']==row['RAW_sha256']
        checks.append(dict(path=row['path'],current_RAW_LF_exact=True,snapshot_or_immutable_reference_exact=True))
    return checks
def all_owned(exclude=()):
    return [pin(p) for p in sorted(OWN.rglob('*')) if p.is_file() and p.relative_to(OWN).as_posix() not in exclude]
def finalize():
    assert read('decision.json')['accepted_prospectively']
    assert read('v2.typecheck.receipt.json')['exit_code'] == 0
    checks=complete_current_inputs()
    probe=(OWN/'HeaderOnlyCheck73V2.lean').read_text(encoding='utf-8')
    forbidden={pattern:re.findall(pattern,probe) for pattern in
          [r'\bsorry\b',r'\badmit\b',r'\baxiom\b',r'\bunknownTACTIC\b',r'Prop\s*:=\s*True',r':=\s*trivial',r'\btheorem\b',r':=\s*by']}
    assert all(not hits for hits in forbidden.values())
    write('fake-closure-scan.json',dict(status='NO_TARGET_PROOF_OR_PROVIDER_IN_FORMATION_PROBE',
          probe=pin(OWN/'HeaderOnlyCheck73V2.lean'),patterns=forbidden,match_count=0,
          canonical_candidate='unsealed header ending with empty := by; never compiled as a theorem and never treated as closure',
          private_Prop_definition_is_specification_only=True,axiom_clean_theorem_credit=False,
          old_failed_probe_diagnostics_retained=True))
    write('final-core-readback.json',dict(status='ALL_FROZEN_CURRENT_INPUTS_EXACT',input_count=len(checks),rows=checks))
    outputs=all_owned(exclude=('outputs.manifest.json','run.json','complete-named-header-review.payload.json','lease.final.json'))
    write('outputs.manifest.json',dict(status='FINALIZATION_BASELINE_FINAL_LEASE_BINDS_ALL_LATER_SELF_TERMINALS',file_count=len(outputs),files=outputs))
    payload=dict(payload_name='COMPLETE_INDEPENDENT_PROSPECTIVE_HEADER_MATH73_REVIEW',
        actor='/root/exact_science63', input_manifest=read('inputs.complete-union.manifest.json'),
        original_frozen_header_inputs=read('inputs.manifest.json'),overlay_inputs=read('overlay.inputs.manifest.json'),
        frozen_header_decision=read('header.decision.json'),separate_two_edge_repair_decision=read('repair-decision.json'),
        mathematical_review=read('mathematical-review.json'), decision=read('decision.json'),
        type_representation=read('type-representation.map.json'), typecheck=read('v2.typecheck.receipt.json'),
        fake_closure_scan=read('fake-closure-scan.json'),
        final_readback=read('final-core-readback.json'), outputs_manifest=read('outputs.manifest.json'),
        closure_policy='Final lease binds every owned file, including all self and actual terminal layers. No native scope reopened.')
    write('complete-named-header-review.payload.json',payload)
    run=dict(schema='independent-prospective-header-math73/v1',status='ACCEPTED_PROSPECTIVE_HEADER_ONLY',
        actor='/root/exact_science63',observed_HEAD=read('lease.open.json')['observed_HEAD'],
        commit_bound_verification=False,exact_header=pin(OWN/'inputs/000.exactraw.snapshot'),
        input_manifest=pin(OWN/'inputs.complete-union.manifest.json'),complete_named_RAW_payload=pin(OWN/'complete-named-header-review.payload.json'),
        output_manifest=pin(OWN/'outputs.manifest.json'),decision=pin(OWN/'decision.json'),
        fresh_typecheck=read('v2.typecheck.receipt.json'),
        hash_recipe='canonical UTF8 JSON ensure_ascii=false sort_keys=true separators comma/colon, delete ONLY top-level run_sha256',
        final_lease_binding='all owned files except lease itself; separate lease RAW hash returned externally',
        proof_source_topology_and_VERIFIED_credit=False)
    run['run_sha256']=sha(canon(run))
    write('run.json',run)
    print(json.dumps(dict(actual_PID=os.getpid(),run_sha256=run['run_sha256'],named_RAW=pin(OWN/'complete-named-header-review.payload.json'))))
def readback():
    run=read('run.json'); claimed=run.pop('run_sha256'); assert sha(canon(run))==claimed
    assert pin(OWN/'complete-named-header-review.payload.json')['RAW_sha256']==run['complete_named_RAW_payload']['RAW_sha256']
    complete_current_inputs()
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
