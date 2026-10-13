"""Record the independent full-proof mathematics verdict without admission writes."""
from pathlib import Path
import datetime, hashlib, json, re
ROOT=Path('E:/Samplinglib');BASE=ROOT/'runs/20261007-companion-priority/pbps-actual-nonaccumulation78';OUT=BASE/'independent-math78'
MODULE=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualNonaccumulation.lean'
def info(p):
    b=Path(p).read_bytes();return {'path':str(p),'RAW_bytes':len(b),'RAW_sha256':hashlib.sha256(b).hexdigest()}
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def save(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=load(OUT/'fresh-compiler-summary78.json');assert summary['status']=='PASS_FULL_SOURCE_STANDARD_THREE'
assert summary['module']==info(MODULE)
lines=MODULE.read_text(encoding='utf-8').splitlines()
def line(needle):return next(i for i,s in enumerate(lines,1) if needle in s)
proof=[
 {'id':'M01','claim':'Exact source-standing target and actual objects','lines':[15,60],
  'argument':'Private Prop is byte-identical to the sealed private header. The public theorem repeats exactly its six source analytic arguments, plus only the standard finite-dimensional real inner-product/Borel typing context. There is no cap, probability, iid, positive-energy/dimension, continuation, crossing or divergent-sum caller. P and epsilon are canonical literal inputs; the nine recurrence definitions are exact to parent76. The body H and C are the same source initial-energy cap definitions as parent76, not arbitrary witnesses.'},
 {'id':'M02','claim':'Parent integration supplies all certificates internally','lines':[line('  -- Reuse the actual'),line('  intro y xRef z₀')],
  'argument':'Parent76 is applied to the six actual source arguments. Its initial-record, initial-time, absorbing-stop and cap/increment/zero-cap clauses are extracted. Product77 supplies simultaneous raw-coordinate positivity and divergence of the actual clamped input sums. Definitional equality matches the local P, epsilon(sample)(k), record and eventTime to both parent interfaces. No parent conclusion is moved into a public assumption.'},
 {'id':'M03','claim':'One actual full-measure input event suffices','lines':[line('  filter_upwards [hgood'),line('  obtain ⟨hC, hinc, hzero⟩')],
  'argument':'Intersect the product positivity and divergence events once. For each k, Real.toNNReal_pos converts the actual raw coordinate positivity to epsilon(sample)(k)>0. hsum is the exact real sum over range n of these epsilon values. y,xRef,z0 are fixed before AE quantification; all horizons are handled pathwise after selecting a sample. No uncountable intersection or joint process measurability is assumed.'},
 {'id':'M04','claim':'Zero cap, including rank0/zero energy, stops immediately','lines':[line('    by_cases hC0'),line('      exact WithTop.coe_lt_top t')],
  'argument':'The internal C>=0 cap splits at C=0. Parent zero-cap clause at n=0 consumes the actual initial active record and epsilon0>0, yielding record1=stopped. For n>=1, write n=1+k and use parent absorption. The eventTime definition sends stopped to top, which is strictly above every finite NNReal horizon. Thus rank0/zero-energy/cap0 cases are retained and require neither division by zero nor a phase at infinity.'},
 {'id':'M05','claim':'Positive cap has exact real/nonnegative representation','lines':[line('    · have hCp'),line('      have hcapPos')],
  'argument':'C>=0 and C!=0 imply C>0. cap=toNNReal C has real coercion exactly C. Every threshold is nonnegative, so toNNReal(e_n/C)=e_n/cap by the pinned quotient lemma. This is representation bookkeeping, not a change of the source cap or a cap-positivity premise.'},
 {'id':'M06','claim':'Actual clock scaled-sum lower bound includes all stopped prefixes','lines':[line('      have hbound'),line('            _ ≤ eventTime y xRef z₀ (ε sample) (n + 1) := hi')],
  'argument':'At n=0, the empty sum is0 and actual eventTime0=0. At successor, divide the finite NNReal sum identity by cap and coerce addition into WithTop. Add the new nonnegative quotient to the induction bound and use parent one-step actual event-time increment. The inequality is in WithTop NNReal, so an already-stopped top value remains top under finite addition. No continuing-path hypothesis or unsafe untopD applied to a stopped event time is introduced.'},
 {'id':'M07','claim':'Divergent actual sums imply escape beyond every finite horizon','lines':[line('      have hs : ∀ᶠ'),line('      exact lt_of_lt_of_le')],
  'argument':'For fixed finite t and positive finite C, real sum divergence gives eventually t*C<sum epsilon. Since C>0, this is t<sum epsilon/C. The NNReal-to-real coercions preserve the exact quotient and finite sum; coe_lt_coe lifts the strict inequality to WithTop and the actual clock lower bound completes it. Never-stopped paths may have arbitrarily large finite times; the proof never asserts Tendsto to the order atTop filter on WithTop, which would force eventual top.'},
 {'id':'M08','claim':'Finite bounded-horizon index sets follow without hidden monotonicity','lines':[line('  refine ⟨hescape'),line('  exact lt_of_not_ge')],
  'argument':'For each finite t, eventual escape yields an index N such that all n>=N have t<T_n. Any n with T_n<=t must therefore satisfy n<N. The displayed index set is a subset of finite Iio N. This argument includes initialization index0 and all stopped paths. It does not count top sentinels, identify the set cardinality with physical bounce count, assert injectivity, or prove an expected-count bound.'},
 {'id':'M09','claim':'Exact truth boundary is narrower than a global process theorem','lines':[15,len(lines)],
  'argument':'The two conclusions are actual finite-horizon event-time escape and finite sublevel index sets for every fixed deterministic initial phase/reference data, AE under the actual product. Global physical-time trajectory existence/uniqueness/measurability, Markov/invariance/kernel semantics, main accuracy, expected query cost and PBPS-SPHMC composition are absent. Divergence is consumed from the verified indicator-SLLN alternative; no direct Exp first-moment calculation or author mean-one-SLLN proof is claimed.'}
]
save('whole-proof-mathematics78.json',{'reviewer':'/root/exact_verify77','status':'ACCEPTED_WHOLE_IMPLEMENTATION_MATHEMATICS_ONLY',
    'module':info(MODULE),'proof_checks':proof,'new_provider_premises':0,'source_analytic_premises':6,
    'literal_statement_objects':11,'public_theorems':1,'private_specification_definitions':1,
    'mathematical_repairs_required':[],'strict_blockers':[],
    'nonblocking_followup':['Module overview comment still says prospective statement only despite the compiled proof; reader/publication debt, not a mathematical premise or proof defect.',
        'Local hcapPos is derived but unused; a later purification may remove it without changing the sealed target. No cleanup was performed during this independent read.'],
    'not_source_blind_decoder':True,'not_final_source_review':True,'VERIFIED':False,'Goal_complete':False})
verdict={'status':'ACCEPTED_INDEPENDENT_WHOLE_MATHEMATICS78_ONLY','reviewer':'/root/exact_verify77',
    'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'module':info(MODULE),
    'full_fresh_source_elaboration':True,'axioms':['propext','Classical.choice','Quot.sound'],
    'compiler_summary':info(OUT/'fresh-compiler-summary78.json'),'terminal_receipt':info(OUT/'fresh-whole-module-axioms.receipt.json'),
    'statement_definition_audit':info(OUT/'statement-and-definition-audit78.json'),
    'whole_proof_mathematics':info(OUT/'whole-proof-mathematics78.json'),'input_freeze':info(OUT/'input-freeze78.json'),
    'scope':'Independent complete mathematical/proof/definition/binder readback and fresh full-source compiler/axiom evidence only.',
    'no_mathematical_repair_required':True,'source_review':False,'decoder_verdict':False,'exact_commit_verification':False,
    'VERIFIED_transition':False,'canonical_Lean_shared_cell_ledger_edits':False,'stabilized':False,'PURIFIED':False,'Goal_complete':False,
    'provenance':'Honest named source snapshots, explicit mathematical checks and real foreground terminal receipts. No fabricated native reasoning trajectory.'}
save('decision78.json',verdict)
files=[info(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='closed-manifest78.json']
save('closed-manifest78.json',{'reviewer':'/root/exact_verify77','status':'CLOSED_INDEPENDENT_MATH78_EVIDENCE',
    'files':files,'whole_module_unchanged':info(MODULE),'proof_writing':False,'production_edits':False,
    'source_or_Verified_admission':False})
print('INDEPENDENT WHOLE MATH78 ACCEPTED',info(OUT/'decision78.json'))
