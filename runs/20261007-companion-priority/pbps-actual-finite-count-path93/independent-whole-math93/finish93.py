import pathlib,json,hashlib,re,subprocess,datetime
R=pathlib.Path('E:/Samplinglib'); O=pathlib.Path(__file__).parent
def raw(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def save(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteCountPath.lean'
s=p.read_text(encoding='utf-8'); inp=json.loads((O/'input-manifest93.native.json').read_text(encoding='utf-8'))
checks=json.loads((O/'kernel-receipt93.native.json').read_text(encoding='utf-8'))['checks']
assert all(c['exit_code']==0 for c in checks)
assert all(raw(R/x['path'])['raw_sha256']==x['raw_sha256'] for x in inp['inputs'])
helpers=re.findall(r'^private theorem (\w+)',s,re.M)
assert len(helpers)==25
scan=re.findall(r'\b(?:sorry|admit|axiom|unsafe)\b|Prop\s*:=\s*True|:=\s*trivial',s)
assert not scan
items=[
('statement','1851-2015','The private Prop definition is text-identical to the independently sealed Header93 literal Prop after declaration-name/visibility removal. A fresh kernel witness inhabits this independently defined Prop using the public theorem; no additional provider is introduced.'),
('assumptions','2005-2015','Six analytic hypotheses only: positive alpha, alpha <= beta, C2 potential, Hessian sandwich, positive eta, beta*eta <= 1. Remaining carriers/typeclasses are finite-dimensional real Hilbert/Borel structures. No Nontrivial/rank-positive assumption, integrability, nonexplosion, independence or path-law provider is added.'),
('history_interpolation_measurability','31-84,148-204','Finite fold is measurable by induction, record update by measurable sum elimination and a measurable time comparison. Coordinatewise measurable_pi_lambda establishes the product sigma-algebra result for arbitrary horizon-indexed path coordinates; no diagonal or Skorokhod structure is assumed.'),
('conditional_terminal_weight','206-400','Survival88 is applied at a measurable remaining duration T-liveTime(last). Its history-set identity is localized by measure extensionality. The stopped record has zero terminal weight and false survival. Arbitrary measurable ENNReal tests follow from the actual restricted history pushforward.'),
('prefix_weighted_joint_law','402-726','Prefix92 is applied to F(h,Psi(h))*W(h). This gives rho=q*W(K) and the history/interpolated-path joint law. Joint parameter measurability of Gamma and rho follows from joint K/q/Psi/hazard measurability. Measure equality uses measurable tests, not measurability of equality of paths. The F=1 test gives unnormalized mass and canonical product probability gives <=1.'),
('raw_path_identification','728-995','The greatest eligible finite record selects each path coordinate; its successor lies after that coordinate because either the index is terminal and terminal survival applies, or maximality excludes the successor. Thus the fold matches the actual process arc at every coordinate. Functional extensionality proves whole-path equality on every raw C event, including null clocks when C holds.'),
('total_count','997-1161','N is Nat.find of a measurable countable family of interval events with explicit zero fallback outside the union. Its joint measurability is proved; decidability witnesses are equated by subsingleton elimination. Monotone intervals guarantee uniqueness even when raw event times coincide.'),
('prescribed_path','1163-1249','Strict ordered prefix implies nonnegative times. The real-time fold lemma uses the last eligible index and NNReal subtraction under its guard, giving the exact harmonic arc formula with post-event state.'),
('endpoint_nullity','1251-1541','For each fixed finite T and positive index j, use prefix horizon T+1. On the canonical positive-clock AE event a live endpoint at T implies a strict prefix below T+1. The ordered density sends last-coordinate hyperplanes to null events; withDensity absolute continuity preserves nullity even without a bounded density. Countable intersection over j gives fixed-T endpoint avoidance. No exchange to AE(all T) occurs.'),
('count_event_and_cardinality','1543-1849','C_n is pointwise contained in interval I_n. Canonical positive clocks, physical-time coverage and fixed-T endpoint nullity yield I_n iff C_n simultaneously for all n almost surely. The selected interval and monotonicity identify the positive index sets at <T and <=T with Ioc 0 N, proving finiteness and ncard=N. Raw disjointness follows from the pointwise containment and monotonicity; union measure one uses AE coverage.'),
('final_actual_joint_law','2156-2209','The restriction to N=n is replaced by restriction to C_n only via AE equality. The pointwise-on-C identity Psi(H)=ZT gives equality of restricted joint pushforwards by map_congr and of tests by lintegral_congr_ae. Thus the actual coordinate-product path enters the law, rather than only a surrogate history interpolation.'),
('edge_cases','whole module','At n=0 the strict prefix carrier has its empty-time point, q is the empty product 1 and the history contains the initial record; the terminal survival factor remains. At T=0 positive-count prefix carriers are empty, endpoint nullity excludes positive-index zero events almost surely, and count 0 has full mass. Infinite waits remain top and are never replaced by a finite wait in a live recurrence; stopped later records remain top. Raw zero clocks may yield coincident events or uncovered fallback, so strict/count interpretation is only AE; raw statements require their written guards. Rank zero needs no exception or extra assumption.'),
]
report={
 'schema_version':1,'reviewer':'independent_whole_math93','role':'independent-whole-mathematical-and-kernel-verifier','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'decision':'ACCEPT_EXACT_SEALED_WHOLE_MODULE_MATHEMATICS_AND_KERNEL','failure_class':'NONE','necessary_fixes':[],
 'baseline_commit':inp['baseline'],'checked_commit_boundary':'Uncommitted production module over the named baseline; exact worktree RAW is the review identity. This does not certify a future commit without rehash.',
 'production':raw(p),'header':raw(R/'runs/20261007-companion-priority/pbps-finite-count-path-preread93/Header93.lean'),
 'statement_literal_equal':True,'fresh_kernel_witness':'IndependentWholeMath93.sealed_header_witness',
 'kernel_checks':checks,'axioms':['propext','Classical.choice','Quot.sound'],
 'fake_closure_scan':{'matches':scan,'new_private_theorem_count':len(helpers),'new_private_prop_count':1,'new_public_theorem_count':1},
 'private_helper_inventory':[{'name':n,'lexical_occurrences':len(re.findall(r'\b'+re.escape(n)+r'\b',s))} for n in helpers],
 'mathematical_audit':[{'topic':t,'production_lines':l,'finding':f,'decision':'accepted'} for t,l,f in items],
 'exposition_review':{'status':'pending-authored-input','scope':'No authored explanation supplied at decision time. Source fidelity, blind decoding and exposition acceptance are separate.'},
 'truth_boundary':['Exact finite-count history and actual coordinate-product path law for every finite count and NNReal horizon under six hypotheses.','This is not independent source-fidelity/decoder acceptance, aggregate repository gate, publication validation, graph/site review, merge/purification or whole-Goal completion.','Full countable A.7 expansion, hazard stitching, left limits, Skorokhod compatibility, restart/Markovness, invariance, hypocoercivity, implementation errors, costs and actual-input composition remain outside this review.'],
 'input_rehash':{'all_unchanged':True,'count':len(inp['inputs'])},
 'warnings':'Lean emits unused-variable linter warnings for the exact private proposition signature and generic helpers; these do not alter the public six-hypothesis type or kernel result.',
 'failed_trials':[],
}
save('whole-math-decision93.native.json',report)
artifacts=[]
for f in sorted(O.rglob('*')):
 if f.is_file() and f.name!='closed-RAW93.native.json':artifacts.append(raw(f))
save('closed-RAW93.native.json',{'schema_version':1,'closure':'All owned run files except this manifest; this manifest is hashed by the parent review receipt. External exact source inputs have local RAW snapshots.','artifacts':artifacts,'external_inputs':inp['inputs'],'runtime':[raw(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),raw(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe')]})
print(json.dumps({'decision':raw(O/'whole-math-decision93.native.json'),'manifest':raw(O/'closed-RAW93.native.json'),'artifacts':len(artifacts)},indent=2))
