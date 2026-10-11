from pathlib import Path
import datetime, hashlib, json, re, subprocess

R=Path('E:/Samplinglib'); O=Path(__file__).parent; B=O.parent
def raw(p):
    p=Path(p); p=p if p.is_absolute() else R/p
    b=p.read_bytes()
    return {'path':p.relative_to(R).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def load(p): return json.loads(Path(p).read_text(encoding='utf8'))
def put(n,v):
    with (O/n).open('x',encoding='utf8',newline='\n') as f: json.dump(v,f,ensure_ascii=False,indent=2); f.write('\n')
inputs={}
def inp(p,scope):
    d=raw(p);d['read_scope']=scope;inputs[d['path']]=d;return d
def validate_manifest(p):
    j=load(p); rows=[]
    def walk(v):
        if isinstance(v,dict):
            expected=v.get('raw_sha256',v.get('sha256'))
            if expected and v.get('path'):
                q=Path(v.get('closed_snapshot',v['path']));q=q if q.is_absolute() else R/q
                got=raw(q);assert got['raw_sha256']==expected,(str(q),expected,got)
                if 'bytes' in v:assert got['bytes']==v['bytes'],str(q)
                rows.append(got)
            for x in v.values():walk(x)
        elif isinstance(v,list):
            for x in v:walk(x)
    walk(j);inp(p,'manifest content and recursively exact RAW validation; private extracts/scripts hash-only')
    return {'manifest':raw(p),'matching_descriptors':rows,'all_match':True}

v1=inp(B/'header90.proposed.lean','complete private prospective Prop; original syntax failure retained')
v2=inp(B/'header90.v2.proposed.lean','complete private prospective Prop; mathematical and type review')
assert v1['raw_sha256']=='1262c82138eb3a7cc502fe4eb6182c10e4e33168a734333ffaec580585935750'
assert v2['raw_sha256']=='5c976dcfe91fe074db71ddbf13385086735c41c273e937b0c6ef432b7dba9037'
old=(B/'header90.proposed.lean').read_bytes();new=(B/'header90.v2.proposed.lean').read_bytes()
closing=b'end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryExtension\n'
assert new==old[:-len(closing)]+b'end\n'+closing
h=new.decode('utf8')
parents={}
for fn in ['ActualConditionalNextWaitDensity','ActualFiniteHistoryTailLaw','ActualFiniteJumpRecursion']:
    p=R/f'AutoSamplingTheory/ExampleCases/ProximalBPS/{fn}.lean'
    parents[fn]=inp(p,'private literal statement and public producer signature only; no parent proof used for source topology')
p89=(R/parents['ActualConditionalNextWaitDensity']['path']).read_text(encoding='utf8')
def binders(s):return s[s.index('    {E : Type*}'):s.index('    let c :')]
def model(s):return s[s.index('    let c :'):s.index('    ∀ y xRef : E, ∀ z₀ : E × E, ∀ n : ℕ,')]
assert binders(h)==binders(p89) and model(h)==model(p89)
model_names=re.findall(r'^    let ([^ :\n]+)',model(h),re.M)
assert model_names==['c','Φ','S','rate','Λ','τ','next','record','P','ε','history','waitObs','timeObs','density']
all_names=re.findall(r'^    +let ([^ :\n]+)',h,re.M);assert len(all_names)==28
for name,sha in [('lean-toolchain','b2b5068d5a4835675e651ce83b29c0ddb308d28b80076e7c007aef4630af0477'),('lake-manifest.json','b1f16b43aaf4a886cfe0382d5e3ae63d6904281c00afd8f35af20f0270a747e2')]:
    assert inp(R/name,'pinned configuration exact bytes')['raw_sha256']==sha
mathlib=subprocess.check_output(['git','-C',str(R/'.lake/packages/mathlib'),'rev-parse','HEAD'],cwd=R,text=True).strip()
assert mathlib=='db584cd6d46c92f209a44c0f1c829460d327499d'
inp(R/'.lake/packages/mathlib/Mathlib/Data/Fin/Tuple/Basic.lean','Fin.snoc signature and castSucc/last API names; no implementation proof search')
for exe in ['lean','lake']:inp(R/f'.astis/toolchain/lean-4.33.0-windows/bin/{exe}.exe','exact foreground executable hash only')
for n in ['header90.scope-diagnosis.json','header-review90.v2.packet.json','root.source90.adoption.json']:
    inp(B/n,'root version/adoption binding only; not independent mathematical evidence')

validation=[]
for n in ['independent-topology90/primary-reconstruction90.closed-RAW-manifest.json','independent-topology90/closed-RAW-manifest90.json','independent-topology-repair90/closed-raw-manifest90.json']:
    validation.append(validate_manifest(B/n))
for n in ['independent-topology90/independent-primary-math-reconstruction90.json','independent-topology90/primary-first90.chronology.json','independent-topology90/coverage90.independent-audit.json','independent-topology90/decision90.json','independent-topology-repair90/decision90.native.json','source-proof-graph90.accepted-successor.json','independent-source-first90/source-proof-graph90.native.json','independent-source-first90/source-coverage90.native.json']:
    inp(B/n,'prior independent source-first evidence, distinct repair acceptance, or exact accepted/original graph binding')
repair=load(B/'independent-topology-repair90/decision90.native.json')
assert raw(B/'independent-topology-repair90/decision90.native.json')['raw_sha256']=='5df52ecc5f45d77de1540066f0718a17af590feaea40539af9a681eed016c0df'
assert raw(B/'source-proof-graph90.accepted-successor.json')['raw_sha256']=='b39b8b3c26758d0787ded303c14c3c927c95033d3ff75bdc1a534431bf1fa8b7'
assert (B/'source-proof-graph90.accepted-successor.json').read_bytes()==(B/'independent-topology90/source-proof-graph90.proposed-measurability-scope-overlay.json').read_bytes()
assert raw(B/'independent-source-first90/source-proof-graph90.native.json')['raw_sha256']=='d55dc5ebc98cde129607e173801c39b0571a83383f75d03b1bdcc12ef7af3d36'
assert raw(B/'independent-source-first90/source-coverage90.native.json')['raw_sha256']=='a8e026e8cea330e34ca620561fe1208e219ad810e565d5757b2e8e913cd2e2de'
put('recursive-RAW-validation90.json',{'all_match':True,'validations':validation,'private_scripts_and_extracts_content_not_consulted':True})
baseline=R/'runs/20261007-companion-priority/pbps-conditional-next-wait-density-preread89/pre-fetch89.workspace-RAW.json'
inp(baseline,'original21 collaborator RAW baseline only')
collab=load(baseline)['tracked_modified'];assert len(collab)==21
rows=[]
for name,sha in collab.items():
    d=raw(R/name);assert d['raw_sha256']==sha;rows.append(d)
put('collaborator-preservation90.json',{'baseline':raw(baseline),'all_21_match':True,'files':rows})
receipts=[load(O/f'{x}.receipt.json') for x in ['header-original90','header-v2-exact90','header-v2-private-check90']]
assert [x['exit_code'] for x in receipts]==[1,0,0]
for q in receipts:
    assert q['terminal_closed']
    for name in ['source','stdout','stderr']:
        d=q[name];assert raw(R/d['path'])['raw_sha256']==d['raw_sha256']
assert not re.search(r'\b(sorry|admit|axiom|theorem)\b',h)
put('definition-readback90.json',{
    'reviewer_id':'/root/exact_verify77','header':v2,'parent89':parents['ActualConditionalNextWaitDensity'],
    'six_source_analytic_binders':['hα','hαβ','hV','hH','hη','hβη'],
    'binder_block_exact_text_equal_parent89':True,'model_block_exact_text_equal_parent89':True,
    'literal_model_definitions':model_names,'all_28_let_definitions':all_names,
    'fixed_parameters':'Every y,xRef,z0 and deterministic natural depth n; finite full tagged history includes record indices0..n.',
    'test_classes':'d is any Borel Hist→NNReal, finite at every history but need not have a global bound. F is any jointly Borel nonnegative ENNReal test; A any Borel old-history set. These are test classes, not new analytic or producer hypotheses.',
    'association':'Rec=(NNReal×(E×E))⊕Unit; Hist=Fin(n+1)→Rec; HistNext=Fin(n+2)→Rec. append preserves castSucc coordinates, then updates exactly the last record. lift=(append,relative real wait).',
    'totalization':'For negative real s, append uses literal Phi_s and toNNReal s in time. Stopped last record appends stopped. Guarded actual equality is claimed only on positive finite wait B, and D vanishes outside0<s<d(h), including all stopped histories.',
    'strict_guard':'B uses strict WithTop inequalities0<wait<finite d(H). Hence a live finite positive wait; timeObs then equals its real coercion. No equality of open/closed endpoint masses is used.',
    'quantifiers_and_measures':'mu=map H P; nu=(mu×real Lebesgue).withDensity D. Joint and marginal laws are unnormalized restrictions of actual P, not conditional-probability normalization.',
    'no_provider_premises':True,'no_new_analytic_hypotheses':True,
    'root_syntax_successor':'Only standalone end closes anonymous noncomputable section. Full private Prop and all other bytes unchanged. Root independently proposed V2; no reviewer-authored canonical change.'})
put('topology-admission90.json',{
    'status':'ACCEPT_PROSPECTIVE_SOURCE_TOPOLOGY_WITH_DISTINCTLY_REVIEWED_EXACT_SCOPE_REPAIR',
    'reviewer_id':'/root/exact_verify77','original_independent_source_reconstruction':raw(B/'independent-topology90/independent-primary-math-reconstruction90.json'),
    'chronology':raw(B/'independent-topology90/primary-first90.chronology.json'),
    'original_conditional_decision':raw(B/'independent-topology90/decision90.json'),
    'distinct_repair_decision':raw(B/'independent-topology-repair90/decision90.native.json'),
    'distinct_repair_reviewer':'/root/exposition_repair89',
    'repair_proposer_self_review_excluded':True,
    'admission_basis':'Own primary-first audit independently covers unchanged construction, strict guarded identity, transport,22dispositions,3AND and preserved OR/global exclusions. The two-field missing A2 Borel-recursion scope repair is admitted solely on distinct exact-proposal review; this proposer does not self-approve it.',
    'accepted_graph':raw(B/'source-proof-graph90.accepted-successor.json'),
    'original_graph_unchanged':True,'coverage_unchanged':True,
    'counts':{'nodes':7,'edges':8,'AND_junctions':3,'coverage_items':22,'NODE':14,'EXCLUDED':8},
    'dependencies':'Borel harmonic flow/reflection AND hazard/crossing/finite stopped recursion supply internal append/Hnext measurability. Actual89 strict density AND actual append AND guarded identification supply transport. Alternative direct87/86 route stays OR; actual88 survival and noatom are not AND prerequisites.',
    'remaining_OPEN':['Ordered absolute-time iteration','final survival/path/count assembly','full I5/G86-11/A7','random stopping/physical-time restart/Markov','global invariance/all-L2/cost/main/composition/fullpaper/Goal'],
    'not_final_BODY_or_source_acceptance':True})
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
put('decision90.json',{
    'status':'ACCEPT_PROSPECTIVE_WHOLE_HEADER_V2_MATHEMATICS_TYPE_AND_SOURCE_TOPOLOGY_ONLY',
    'reviewer_id':'/root/exact_verify77','header':v2,'context_commit':head,
    'mathematics':'No mathematical counterexample or missing hypothesis identified within the bounded statement. Actual constructor/recursion identification is a new substantive finite-history assembly interface beyond89, not a supplied measurable-map wrapper.',
    'whole_statement_audit':[
        'All six source analytic binders and14 literal model definitions are exactly unchanged from verified89; all14 packaging definitions and every conclusion inspected.',
        'Hnext measurability is supplied internally by verified87 at depth n+1, or actual76 finite-record measurability. Borel append/lift follows finite tuple coordinate construction, actual flow/reflection and time addition.',
        'Strict positive finite guard makes actual tau.untopD equal real observed wait; old record coordinates agree and final coordinate equals literal next. Guard excludes infinity,zero and cutoff endpoint without an atom assertion.',
        'Actual89 map X(P|B)=nu together with Y=lift∘X onB transports joint law. First projection yields next-history marginal; measurable lift preserves subprobability mass≤1.',
        'For every Borel ENNReal F, F∘lift is an admissible89 joint test, yielding Borel history integral and every Borel old-history restriction identity. No L1 requirement or normalization is imposed.',
        'Negative-time/unrealizable histories are auxiliary totalizations; density support eliminates them from positive finite update claims. No unrestricted next-history or physical-time restart law follows.'
    ],
    'case_audit':{
        'n0':'Fin1 old history, Fin2 updated history; last and castSucc remain valid.',
        'd0_zero_wait_cutoff_endpoint':'Strict B and strict D support exclude these exactly; both transported restrictions have zero mass there.',
        'stopped_and_top':'Stopped waitObs0 cannot enter B; live infinite wait cannot be below finite d. Default extraction0 is not asserted actual finite jump.',
        'rank0_flat_hazard_zero_normal':'Literal total reflection remains Borel; zero/flat hazard can yield infinite waits; strict guard handles them without a finite-wait premise.',
        'nullA':'Unnormalized set-lintegral identity remains meaningful and zero on null old-history events; no conditioning by positive mass.',
        'F_infinity':'Nonnegative extended integrals remain defined; no subtraction or0/0.',
        'unbounded_finite_cutoff':'No uniform bound is needed; every d(h) finite and Borel.',
        'off_support':'No source claim for negative update times or impossible histories; all such cases totalized and guard/disclosed support maintained.'
    },
    'typecheck_receipts':[raw(O/f'{x}.receipt.json') for x in ['header-original90','header-v2-exact90','header-v2-private-check90']],
    'original_negative':'V1 EXIT1 missing anonymous section end only; original snapshot/logs retained. Root V2 inserts end and exact full header EXIT0; local private #check complete-header overlay also EXIT0.',
    'required_repairs':[],'syntax_repair_already_root_proposed_and_independently_checked':True,
    'source_topology_admission':raw(O/'topology-admission90.json'),
    'no_theorem_BODY_proof_credit':True,'no_StatementSeal_or_claim_created':True,'no_VERIFIED_or_canonical_writes':True,
    'remaining_OPEN':['Actual90 theorem implementation and kernel/fakeclosure audit','independent blind decoder/final source/exposition/exact-science admission','ordered event density/final survival/fullA7','global/Markov/restart/invariance/L2/cost/main/fullpaper/Goal']})
put('run90.json',{
    'reviewer_id':'/root/exact_verify77','closed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status':'CLOSED_PROSPECTIVE_REVIEW_ONLY','context_commit':head,'mathlib_commit':mathlib,
    'foreground_checks':[{'receipt':raw(O/f'{x}.receipt.json'),'native_exit':q['exit_code'],'actual_PID':q['actual_foreground_PID']} for x,q in zip(['header-original90','header-v2-exact90','header-v2-private-check90'],receipts)],
    'inputs':list(inputs.values()),'recursive_RAW_validation':raw(O/'recursive-RAW-validation90.json'),
    'all_21_collaborator_RAW_preserved':True,'no_new_SOURCE_BODY_or_parent_PROOF_search':True,
    'scope':'Complete header mathematics/type; unchanged own primary-first source coverage plus distinct acceptance of reviewer-proposed scope repair. No forthcoming source-header verdict used as mathematics evidence.',
    'negative_preservation':'Original V1 compiler diagnostic retained. No own syntax candidate or canonical edit. Prior source topology residual remains in original native packet, not overwritten.'})
artifacts=[raw(p) for p in sorted(O.iterdir()) if p.is_file() and p.name!='closed-RAW-manifest90.json']
put('closed-RAW-manifest90.json',{
    'status':'CLOSED_NONCIRCULAR_PROSPECTIVE_HEADER_V2_REVIEW','reviewer_id':'/root/exact_verify77',
    'algorithm':'SHA256 exact raw bytes','frozen_inputs':list(inputs.values()),'owned_artifacts':artifacts,
    'decision':raw(O/'decision90.json'),'run':raw(O/'run90.json'),
    'closure':'All directly consulted input files and all reviewer-owned artifacts are pinned. Prior source manifests are recursively checked and retained as explicit input evidence; private script/extract contents not consulted. Self digest is returned externally, never embedded.',
    'self_hash_intentionally_omitted':True,'no_canonical_state_mutation':True})
print(json.dumps({'decision':raw(O/'decision90.json'),'manifest':raw(O/'closed-RAW-manifest90.json'),'header':v2,'exits':[q['exit_code'] for q in receipts]},indent=2))
