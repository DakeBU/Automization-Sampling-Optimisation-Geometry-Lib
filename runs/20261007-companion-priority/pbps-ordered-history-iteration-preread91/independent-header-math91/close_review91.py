import pathlib,json,hashlib,datetime,subprocess,re
R=pathlib.Path('E:/Samplinglib'); B=R/'runs/20261007-companion-priority/pbps-ordered-history-iteration-preread91';O=B/'independent-header-math91'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def desc(p):
 p=pathlib.Path(p);p=p if p.is_absolute() else R/p;b=p.read_bytes()
 return {'path':p.relative_to(R).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def read(p):return json.loads(pathlib.Path(p).read_text(encoding='utf8'))
def write(n,d):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
 return desc(O/n)
freeze=read(O/'input-freeze91.json');inputs=freeze['inputs'][:]
for d in inputs:assert desc(d['path'])['raw_sha256']==d['raw_sha256'],d
for n in ['independent-topology-repair91/decision91.native.json','independent-topology-repair91/closed-raw-manifest91.json']:
 inputs.append(dict(desc(B/n),read_scope='distinct exact route-overlay review binding only; own overlay not self-approved'))
repair=read(B/'independent-topology-repair91/decision91.native.json')
assert repair['reviewer_id']=='/root/exposition_repair89'
assert repair['decision']=='ACCEPT_EXACT_THREE_OPERATION_ROUTE_INDEXED_TOPOLOGY_OVERLAY91'
assert desc(B/'source-proof-graph91.accepted-successor.json')['raw_sha256']==repair['exact_accepted_successor']['sha256']
for n in ['header-original91.receipt.json','header-private-check91.receipt.json']:
 d=read(O/n);assert d['terminal_exit_code']==0
 for k in ['source','log']:assert desc(d[k]['path'])['raw_sha256']==d[k]['raw_sha256']
baseline=read(B/'pre-fetch91.workspace-RAW.json')['tracked_modified']
preservation=[]
for p,h in baseline.items():
 d=desc(p);assert d['raw_sha256']==h,p;preservation.append(d)
assert len(preservation)==21
write('collaborator-preservation91.json',{'utc':utc(),'status':'ALL_21_BYTE_IDENTICAL','baseline':desc(B/'pre-fetch91.workspace-RAW.json'),'files':preservation})
write('read-scope-clarification91.json',{'utc':utc(),'initial_freeze_scope_correction':{'actual90':'Tool read first125 lines, including introductory proof-local c/Phi lets after complete literal statement/public signature. No parent proof used as source-topology evidence.','actual89':'Tool read first121 lines, including introductory proof-local c/Phi lets after complete literal statement/public signature. No new91 BODY exists or was read.'},'earlier_read':'Read run90.json as receipt/schema reference; not mathematics or source acceptance evidence.','source_first':'Primary91 V2 and first-half closure were frozen before creator graph or header; reused exact. This review does not repeat primary-source extraction.','future_source_review':'Distinct87 whole-header/source review is not read or used.'})
inputs.append(dict(desc('runs/20261007-companion-priority/pbps-next-history-extension-preread90/independent-header-math90/run90.json'),read_scope='prior native receipt schema reference only'))
math={
 'reviewer_id':'/root/exact_verify77','scope':'Complete expanded private prospective Prop, independently assessed; no implementation or proof search',
 'whole_header':desc(B/'header91.proposed.lean'),
 'literal_prefix':'Six analytic binders/typeclasses and fourteen model definitions byte-identical to compiled actual90. Remaining lets are explicit packaging, not supplied model/law/regularity premises.',
 'clauses':[
  {'clause':'Borel H,Hnext,a,U,appendAbs,liftAbs and old-prefix preservation','finding':'Existing actual finite recursion/history measurability supplies H/Hnext. readTime is Borel on Sum, evaluation at last indices is measurable. Fin.snoc with raw real-time Phi and total bounce is Borel for all real differences and preserves all old coordinates. Finite-dimensional Borel Euclidean typing supplies countable-generation/sigma-finiteness required for parameter integrals.'},
  {'clause':'strict relative/absolute guard equality pointwise','finding':'On a live last record with time T and finite tau v, literal next produces live time T+v. Then T<T+v<b iff 0<v<max(b-T,0). On a stopped last record, waitObs=0 and next remains stopped, so both guards fail. Tau=top makes next stopped and fails finite Brel. Thus Brel=B for every raw sample, not merely AE. Zero tau never lies in either guard.'},
  {'clause':'actual observer and append identification','finding':'U reads Hnext lastNext, not an invented shifted observable. On B, tau is finite positive, U=T+v, timeObs=v, and U-a=v. Hence appendAbs reproduces literal next and all old history records. Off guard no actual identification is asserted.'},
  {'clause':'history-dependent Lebesgue coordinate transport','finding':'C(h,s)=(h,a(h)+s) is a Borel invertible shear with inverse(h,u-a(h)); each fiber preserves real volume by additive translation. Probability mu is finite and volume sigma-finite, so product shear invariance follows from MeasurePreserving.skew_product. This is coordinate invariance of reference measure, not PBPS phase invariance or temporal Markov property.'},
  {'clause':'strict density under shear','finding':'For d(h)=toNNReal(b(h)-a(h)), 0<s<d(h) is exactly a(h)<a(h)+s<b(h). Under inverse shear, relative density becomes the stated D. On positive support, toNNReal(u-a(h)) coerces back to u-a(h); negative auxiliary flow is masked to zero outside strict support. No open/closed endpoint mass equivalence or no-atom premise is used.'},
  {'clause':'all-history fiber and total bounds','finding':'Actual89 supplies finite strict relative density mass <=1 for every abstract last live phase and finite d, even unrealizable histories. Translation gives the stated integral bound. Dead density is identically zero. Since mu=map H P and P is internally normalized iid Exp1 probability, total nu mass <=1 follows. No pointwise D<=1 claim is made.'},
  {'clause':'joint/history/marginal pushforward laws','finding':'Actual90 restricted relative next-history law plus the shear, actual observer and append identities yields all three displayed map laws. Old history X law may be obtained from its relative parent89 or projection of90; no new supplied law binder. appendAbs and liftAbs preserve the whole prefix, so restrictions by Borel old-history A transport correctly.'},
  {'clause':'all nonnegative joint tests','finding':'Joint Borel G/F multiplied by joint Borel D gives measurable ENNReal parameter integrals by Tonelli. Map/restrict laws yield exactly the unnormalized displayed set-lintegrals, with no division by P(A) and no boundedness/integrability restriction on F/G. Values infinity and 0*infinity follow standard ENNReal integration.'}
 ],
 'edge_cases':{
  'n0':'Fin1 has initialized live record at time0; Fin2 appends coordinate0 jump. Definitions and cutoff do not require n>0.',
  'b_zero_or_b_le_a':'d=0 and strict absolute support empty for that history; no boundary event or negative elapsed wait is counted.',
  'stopped_history':'a=0 and d=b (not forced zero) in this literal header. waitObs=0, dead density=0 and actual next remains stopped; all restricted contributions are zero. This differs harmlessly from a source-proposal dead-duration convention; it is an auxiliary value not a source hypothesis.',
  'live_infinite_wait':'actual next stopped; U fallback0 cannot satisfy the live-next guard; Brel finite cutoff excludes top.',
  'zero_or_negative_exp_raw':'Real.toNNReal totalization may give tau0; strict positive guard excludes zero without demanding a universally positive raw input. Law remains under actual Exp product.',
  'rank0_or_flat_rate':'rate zero gives density zero; possible infinite wait and zero-threshold exceptional behavior do not enter strict finite guard.',
  'null_A':'unnormalized restriction identity yields zero without conditional representative or positive-mass condition.',
  'unbounded_Borel_cutoff':'b takes finite NNReal values at each history; no uniform bound or cap is required.',
  'off_support_append':'For live history T, appendAbs last time is T+max(u-T,0), not universally u. Phi receives raw u-T. On strict support u>T this equals u; off support no event/process interpretation is claimed.',
  'unrealizable_history':'Borel constructors and fiber bound are meaningful on all Hist; source path claims concern actual H only.'},
 'genuine_delta':'An explicit full-history absolute-event-time density and actual-record observer law obtained by measurable history-dependent Lebesgue transport of90; not merely relabelling relative wait. It supplies a next ordered coordinate at b=T. Finite-depth induction, terminal survival and count/path assembly remain separate OPEN targets.',
 'provider_binders_added':[], 'missing_hypotheses_found':[], 'counterexamples_found':[], 'required_mathematical_repairs':[],
 'feasibility_limit':'Mathematical derivation and API signatures inspected; no Lean implementation of shear/density lemmas or target proof was attempted. Typecheck does not certify these conclusions.',
 'dependency_plan':'Genuine probability parent actual90; actual89 has useful direct Borel/all-history-fiber facets and is already transitive. No actual88 survival AND, no optional typed kernel/Markov provider.'
}
write('whole-header-mathematics91.json',math)
write('API-review91.json',{'scope':'Signature feasibility only; no theorem proof/implementation','references':[{'file':'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Prod.lean','line':870,'name':'MeasureTheory.MeasurePreserving.skew_product','contract':'SFinite source and fiber measures, joint measurable fiber transform, AE fiber map equality.'},{'file':'.lake/packages/mathlib/Mathlib/MeasureTheory/Group/Measure.lean','line':80,'name':'MeasureTheory.measurePreserving_add_left','contract':'generated additive analogue of measurePreserving_mul_left for invariant measure'},{'file':'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryExtension.lean','line':109,'name':'actual_finite_history_extension','contract':'full private Prop read independently; original six analytic premises only'},{'file':'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualConditionalNextWaitDensity.lean','line':105,'name':'actual_conditional_next_wait_density','contract':'joint Borel density/all-history finite-kernel mass and restricted law supplied internally'}],'no_API_compilation_credit_except_whole_header':True})
decision=write('decision91.json',{'utc':utc(),'reviewer_id':'/root/exact_verify77','status':'ACCEPT_INDEPENDENT_WHOLE_HEADER_MATHEMATICS_AND_TYPE_ONLY','header':desc(B/'header91.proposed.lean'),'context_commit':freeze['context_commit'],'whole_private_Prop_checked':True,'native_typechecks_exit_codes':[0,0],'required_repairs':[],'mathematical_assessment':desc(O/'whole-header-mathematics91.json'),'definition_readback':desc(O/'definition-readback91.json'),'source_topology':{'own_prior_whole_graph_review':desc(B/'independent-topology91/source-topology91.decision.json'),'proposer_cannot_self_approve_overlay':True,'exact_route_residual_discharged_only_by_distinct_reviewer':desc(B/'independent-topology-repair91/decision91.native.json'),'accepted_graph':desc(B/'source-proof-graph91.accepted-successor.json')},'linter_warnings':'Expected unused proposition-parameter/n warnings only; six named analytic premises are retained in explicit checked type. No warning suppressed.','scope_limits':['No theorem BODY/proof has been created or reviewed for91.','No Seal/SAU claim/PROVED_LOCAL/VERIFIED or canonical mutation.','No finite ordered iteration/final survival/full A7/endpoint equivalence/restart/global theorem or Goal completion.','This is independent mathematical header acceptance; distinct source-header review remains separate.'],'collaborator_RAW':'21/21 unchanged'})
run=write('run91.json',{'utc':utc(),'status':'CLOSED_HEADER_REVIEW_ONLY','reviewer_id':'/root/exact_verify77','context_commit':freeze['context_commit'],'mathlib_commit':freeze['mathlib_commit'],'native_commands':[{'argv':['C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe','-X','utf8',str(O/'check_header91.py')],'foreground_child_receipts':[desc(O/'header-original91.receipt.json'),desc(O/'header-private-check91.receipt.json')]},{'argv':['C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe','-X','utf8',str(O/'close_review91.py')],'purpose':'immutable decision and noncircular RAW closure'}],'native_terminal':desc(O/'terminal91.json'),'decision':decision,'input_scope_corrections':desc(O/'read-scope-clarification91.json'),'no_proof_native_trajectory':True})
for d in inputs:assert desc(d['path'])['raw_sha256']==d['raw_sha256'],d
outputs=[desc(p) for p in sorted(O.iterdir()) if p.is_file()]
manifest=write('closed-RAW-manifest91.json',{'utc':utc(),'closed':True,'reviewer_id':'/root/exact_verify77','frozen_current_inputs':inputs,'owned_artifacts':outputs,'self_hash_excluded':True,'noncircular':'Manifest includes run/decision/scripts/logs/receipts/snapshots; no artifact embeds this manifest hash.','no_other_writes':True})
print(json.dumps({'decision':decision,'run':run,'closed_manifest':manifest,'header':desc(B/'header91.proposed.lean')},ensure_ascii=False))
