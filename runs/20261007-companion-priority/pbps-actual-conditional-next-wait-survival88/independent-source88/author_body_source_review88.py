from pathlib import Path
from html.parser import HTMLParser
import json, hashlib, datetime, re, subprocess

root = Path('E:/Samplinglib')
out = Path(__file__).resolve().parent
run = out.parent
pre = root/'runs/20261007-companion-priority/pbps-conditional-next-wait-preread88'
packet_path = run/'source-review88.packet.json'
module_path = root/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualConditionalNextWaitSurvival.lean'
lesson_path = root/'website/content/declaration_lessons/pbps-actual-conditional-next-wait-survival.json'
pub_path = root/'website/content/publications/pbps-actual-conditional-next-wait-survival.json'
reader_path = run/'reader-candidate88.html'
primary_path = root/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
chronology_path = out/'chronology.source-review88.native.jsonl'
def raw(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def canon(x): return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def pin(p): return dict(path=str(p.resolve()),raw_sha256=raw(p),bytes=p.stat().st_size)
def write(p,x):
    assert not p.exists(), str(p)
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def append(event,**kwargs):
    with chronology_path.open('a',encoding='utf-8',newline='\n') as f:
        f.write(json.dumps(dict(event=event,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),**kwargs),ensure_ascii=False)+'\n')

expected = {
    packet_path:'a82bcfa6e81385cd86ec20cd850a27d27a75b10835553352bc121bc9ca1cbc34',
    module_path:'2f509ce49343d349f7a9fb21d2f7b1697c1a6de942353f6cd8ff16d522911569',
    lesson_path:'30935077e0f7457da469f1ce18fc2bae4e2b598b80fb085af929229c56ee5796',
    pub_path:'4636be49eb4a8793b8d44c2ccf91f2f3884c2b6ab8afa505f540abbed9ed99fd',
    reader_path:'0cbbbbe903c24979d02c38ed79e3607f571a65abd9da9aee3d661c05fdfe0aa2',
    primary_path:'d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760',
    pre/'independent-source-first88/source-first88.freeze.native.json':'9b3dc106bb0bd83bf846af82aef051c7af5c6c0e2142b33d6834bc89777011da',
    pre/'independent-source-first88/source-proof-slice88.native.json':'7fe781cc3ab8092faf0c9970787c459f662a2e52585c4d637e57c0a328895726',
    pre/'independent-source-first88/source-coverage88.native.json':'6e88954e891eac264d81416f5661e3726c6db3a39c4e38915c38d2f8617b2e92',
    pre/'independent-source-first88/primary-source88.raw-manifest.native.json':'1c5977ef4f0a115811e10d53be294b37287e07d2c664f176e030c94483d49b37',
    pre/'independent-source-first88/closed-raw-manifest.source-first88.native.json':'fedbc429c2e3cc01aa92a2b5dd94a0f5c4c431f005564bcb50631822681432f5',
    pre/'header-source88/header88.source-decision.native.json':'38a95c5cd4c34d1861fdce32ec3c506afd41a58abef7430fe3815b10e30dc228',
    pre/'header-source88/closed-raw-manifest.header-source88.native.json':'2f2c49e16104d098e24fb99c5ff45db849245cf26e0008407bd8193a7d1b80fa',
    pre/'header-math88/topology-review88.json':'e455f3843056e3638b84589f137da0fd5b374b00e0b972e62e3d04aca2f200c2',
    pre/'header88.proposed.lean':'89890948b0716e9e8a0a4e4d5c634aa166361b7fb1575f57e751d49e024aeed3'
}
for p,h in expected.items(): assert raw(p)==h,(str(p),raw(p))
first=json.loads(chronology_path.read_text(encoding='utf-8').splitlines()[0])
assert first['event']=='DIRECT_PRIMARY_REREAD_BEFORE_BODY_PACKET_OR_DECODER'
assert all(first[k] is False for k in ['candidate_BODY_packet_read','decoder88_read','production88_read'])
assert raw(Path(first['private_extract_path']))==first['private_extract_raw_sha256']
packet=json.loads(packet_path.read_text(encoding='utf-8'))
assert canon({k:v for k,v in packet.items() if k!='packet_sha256'})==packet['packet_sha256']=='f9ddb7330489311cdb9471319785d4f369a9744eb1d0cbbdf441780a78fa9d1a'
assert packet['publication_binding_sha256']=='01f6aaf74fd89229d665d649fbe18d0769a8253b9c2e717d56772bb9678344bb'
assert not any(packet['anti_anchoring'].values())
assert len({packet['roles']['formalizer'],packet['roles']['blind_decoder'],'/root/fresh_source87'})==3
module=module_path.read_text(encoding='utf-8')
lesson=json.loads(lesson_path.read_text(encoding='utf-8'))['units'][0]
pub=json.loads(pub_path.read_text(encoding='utf-8'))['items'][0]
context=packet['candidate_publication_context']
assert context['current_lean_module']==module
assert context['lesson']=={k:v for k,v in lesson.items() if k!='boundary'}
for k in ['source','statement','formulae','assumptions','obligations']: assert context[k]==pub[k]
assert hashlib.sha256(module.encode()).hexdigest()==context['file']
for p,k in [(root/'lean-toolchain','toolchain'),(root/'lake-manifest.json','dependencies')]:
    assert hashlib.sha256(p.read_text(encoding='utf-8').encode()).hexdigest()==context[k]
payload={**{k:context[k] for k in ['file','current_lean_module','toolchain','dependencies']},**{k:pub[k] for k in ['source','statement','formulae','assumptions','obligations']},'lesson':lesson,'binding':{k:v for k,v in pub['bindings'][0].items() if k not in ['audit_id','legacy_audit_debt']}}
assert canon(payload)==packet['publication_binding_sha256']
for k,t,h in [('source','original_text','text_sha256'),('lean','statement','statement_sha256'),('blind_reconstruction','text','text_sha256')]:
    assert hashlib.sha256(packet[k][t].encode()).hexdigest()==packet[k][h]
assert packet['blind_reconstruction']['source_text_visible'] is False
pm_path=pre/'independent-source-first88/primary-source88.raw-manifest.native.json'
pm=json.loads(pm_path.read_text(encoding='utf-8'))
pb=primary_path.read_bytes()
for a in pm['anchors']:
    assert hashlib.sha256(pb[a['byte_start_zero_based']:a['byte_end_exclusive']]).hexdigest()==a['raw_span_sha256']
assert b'arXiv:2609.06905v1' in pb and b'07 Sep 2026' in pb
assert b'License: arXiv.org perpetual non-exclusive license' in pb
sf_manifest=json.loads((pre/'independent-source-first88/closed-raw-manifest.source-first88.native.json').read_text(encoding='utf-8'))
for section in ['inputs','outputs']:
    for p in sf_manifest[section]:
        q=Path(p['path']); assert raw(q)==p['raw_sha256'] and q.stat().st_size==p['bytes']
append('FRESH_PACKET_AND_CURRENT_BODY_READ_AFTER_PRIMARY',packet=pin(packet_path),canonical_packet_sha256=packet['packet_sha256'],publication_binding_sha256=packet['publication_binding_sha256'],prior_source_verdict_used_as_anchor=False,prior_math_verdict_read=False,format_only_reference='87 native writer script was inspected solely for requested output-field compatibility; 87 conclusions were not used to decide 88.')

decoder_dir=run/'anonymous-decoder'
decoder=json.loads((decoder_dir/'reconstructed-theorem.json').read_text(encoding='utf-8'))
assert decoder['reconstructed_theorem_text']==packet['blind_reconstruction']['text']
assert raw(decoder_dir/'decoder.run.json')==packet['blind_reconstruction']['decoder_run_sha256']
decoder_manifest=json.loads((decoder_dir/'closed-RAW-manifest.json').read_text(encoding='utf-8'))
decoder_clarification=dict(
    original_native_assumptions_sentence='In particular, d need not be bounded, positive, deterministic, or restricted to histories that the recursion attains.',
    original_artifact=pin(decoder_dir/'reconstructed-theorem.json'),
    assessment='The word deterministic is imprecise in isolation. The quantified d is a fixed Borel function on Hist_n, with no omega or tail argument. Its value d(H_n) may be random and need not be a constant duration. An arbitrary random unconditioned function d is not quantified or permitted.',
    internal_evidence='The same untouched native reconstruction explicitly quantifies every Borel function on the history space and explicitly excludes w_n/future-threshold durations in Scopes and Limits. The literal Lean and current public prose agree with these precise paragraphs.',
    classification='notation-resolution',blocking=False,
    native_output_modified=False,canonical_overlay_required=False,
    interpretation_accepted='d is deterministic as a function; d(H_n) may vary randomly with H_n. No extra randomization or future inspection is admitted.')
write(out/'decoder-wording-clarification88.native.json',decoder_clarification)

def slot(original,reconstructed,evidence,relation='equivalent'):
    return dict(original=original,reconstructed=reconstructed,relation=relation,evidence=evidence)
slots={
 'objects':slot('The source fixed-reference PBPS harmonic flow, gradient reflection and positive-part intensity define integrated-hazard crossings with iid Exp(1) thresholds. The frozen completion uses their actual finite tagged stopped record history, its next unused raw threshold, and the live-guarded survival observable and exponential weight.',
 'The blind reconstruction gives the same thirteen literal objects c,Phi,S,rate,Lambda,tau,next,record,P,epsilon,history,L,W, including the strict crossing event and separate stopped tag.',
 'Direct primary A1.SS1.p1/p2, A1.E1/E2; source-first88 freeze; current private Prop lines16-82 and all repeated BODY definitions. The current record is H_n[last] definitionally and the unused source E_(n+1) is raw w_n.'),
 'domains':slot('Finite-dimensional real inner-product Borel carrier, including rank zero; V:E->R; alpha,beta nonnegative, eta real; fixed y,r,z0; nonnegative finite durations and extended waiting times. Hist_n is the full finite product of tagged records, and raw inputs lie in R^N. d:Hist_n->NNReal is Borel and need not be bounded; A is any Borel history set.',
 'The decoder retains the carrier structures, all parameter types, full arbitrary history domain, finite-valued duration function, extended wait and raw exponential product. It separates raw clocks from their clipped recursion inputs.',
 'Finite-dimensional generalization of the source Euclidean formulas is explicitly attributed. All-history Borel event/weight claims include unrealizable tuples; the final law is integrated against the actual history pushforward. No dimension-positive, finite-wait or duration-bound restriction appears.'),
 'quantifiers':slot('For every fixed deterministic y,r,z0 and event depth n, every fixed Borel function d on the complete history and every Borel A, prove joint-event measurability, all-history measurable bounded weight and the exact unnormalized survival identity.',
 'The precise native quantifier paragraph reconstructs forall y,r,z0,n,d followed by Measurable d and forall A with MeasurableSet A. Its scopes exclude future-dependent duration and random indices. The assumptions paragraph contains an imprecise deterministic phrase assessed separately.',
 'Current private Prop and public change expand the identical quantified four-part conjunction. d(H_n) can be random; d itself is a fixed map, not an arbitrary random family. No interchange of separate fixed-time almost-everywhere identities occurs.', 'explicit-elaboration'),
 'assumptions':slot('Exactly the six standing analytic hypotheses: alpha>0, alpha<=beta, global C2 V, both Hessian bounds for all x,v, eta>0, beta*eta<=1, with finite-dimensional real inner-product/Borel carrier data. Measurable d and Borel A delimit admissible tests rather than supplying algorithm regularity or independence.',
 'The decoder lists those six hypotheses and defines the product law and algorithm literally. Its d-not-deterministic wording is accepted only as history-dependent random duration d(H_n), consistently with its own function type and explicit exclusions.',
 'No history measurability, product law, survival identity, regular conditional distribution, integrability or independence provider is a binder. Actual75/87 and unit-exponential77 are called internally with exactly the original analytic inputs. Native wording is preserved and clarified in a separate exact-input-bound record.', 'explicit-elaboration'),
 'conclusion':slot('B_d={(h,v):L(h_last,d(h),v_0)} is Borel; W_d is Borel and at most one on every abstract history; for every Borel A, P{H_n in A,L(R_n,d(H_n),w_n)}=integral_A W_d d((H_n)_*P). This is the history-law form of the frozen unnormalized P-space integral.',
 'The decoder reconstructs all four components, distinguishes the auxiliary coordinate0 event from the actual next coordinate n, and identifies an extended nonnegative restricted integral without normalization.',
 'BODY regions2/3 prove measurability and boundedness; region4 proves every fixed-history fiber, region5 pulls back C under (H_n,Y_n), uses the actual87 joint law, applies Measure.prod_apply and lintegral_indicator. History pushforward translates exactly to the frozen P-space formula; it adds no source premise.'),
 'scopes':slot('Only S87-I4, a source-implicit history-dependent conditional-survival ingredient at deterministic event depth. Live infinite waits survive every finite duration. Stopped histories have event false and weight zero; null A is allowed. Density, ordered-time iteration, final factor assembly/full A.7, physical-time restart and all global results remain open.',
 'The native reconstruction correctly excludes random-depth stopping, enlarged/future-informed histories, infinite duration, finite-wait guarantees, path process/nonexplosion/Markov/invariance/cost consequences. The public exposition attributes the completion and retains I5/global boundaries.',
 'The fixed-T consumer may use Borel d_T(live(t,z))=max(T-t,0), stopped0, together with a live t<=T history guard. This theorem admits that choice but does not perform final no-event factor assembly, density multiplication, sum/integration iteration or path-law derivation.'),
 'constant_dependencies':slot('Exp rate is exactly one. Objects depend on V,eta and fixed y,r/states; alpha,beta occur in the standing hypotheses. No rate lower bound, positive event mass, finite wait, horizon budget, integrability constant or cost constant is required.',
 'The decoder records unit-rate P independent of all algorithm parameters and makes no dimension lower bound or unspecified constant claim. d can use every history entry; its finite pointwise values may be unbounded across histories.',
 'P=Measure.infinitePi(expMeasure 1), Y_n(w)_k=w_(n+k). Boundedness of W_d follows internally from Lambda>=0, not a caller domination certificate; all probabilities and restricted lintegrals include null A.')
}

defrows=[
 ('c','y-eta*gradient V r','S3.E4','Literal source center.'),
 ('Phi','(c+cos(t)*(x-c)+sqrt(eta)*sin(t)*p, -sin(t)/sqrt(eta)*(x-c)+cos(t)*p)','A1.SS1.p1','Literal harmonic flow; eta>0 ensures source scaling.'),
 ('S','(x,p-(2*inner(p,g)/norm(g)^2)*g), g=gradient V x-gradient V r','A1.SS1.p1','Total division makes the correction zero when g=0, exactly R0=I.'),
 ('rate','sqrt(eta)*max(0,inner(p,g))','A1.SS1.p1','Literal nonnegative source intensity, no surrogate cap.'),
 ('Lambda','integral from0 to finite NNReal u of rate(Phi_s z)','A1.E1','Actual interval integral, finite and jointly Borel from actual75.'),
 ('tau','hittingAfter (Lambda-e) Ici0 after0, valued WithTop NNReal','A1.E1','First >= crossing; inf empty infinity; tau0=0 and strict-survival endpoint retained.'),
 ('next','stopped stays stopped; live goes stopped at tau=infinity, otherwise live(T+tau,S(Phi_tau z))','A1.E2','untopD0 only used after infinity excluded, no fictitious infinite-time phase.'),
 ('record','Nat.rec live(0,z0), successor k consumes e_k','A1.E1/E2','Source E_(k+1) reindexed to zero-based coordinate k; record n consumes only k<n.'),
 ('P','infinitePi of expMeasure1 on R^N','A1.SS1.p2','Literal mutual iid rate-one threshold model, a definition rather than independence premise.'),
 ('epsilon','Real.toNNReal(w_k)','A1.SS1.p2','Ambient nonnegative extension; all clocks positive P-a.s. and clipping then equals raw. Does not modify full raw tail law.'),
 ('history','Fin(n+1) evaluations of record at j.val on epsilon w','A1.E1/E2 and A.2','Complete deterministic-depth stopped history, not random event count at physical time.'),
 ('liveSurvival','live(T,z): u<tau_z(toNNReal e); stopped: False','A1.E1/E7 source-implicit','Finite duration strict survival includes infinite next wait; no stopped phase/wait interpretation.'),
 ('survivalWeight','live(T,z): ENNReal.ofReal(exp(-Lambda_z u)); stopped:0','A1.E7 source-implicit','Borel bounded weight on every history, including unrealizable histories; ofReal does not change positive exp.')]
definitions=[dict(name=n,definition_kind='literal',formula=f,source_anchor=a,verdict='accepted',evidence=e) for n,f,a,e in defrows]
binders=[
 dict(name='hAlpha',literal='0 < (alpha : R)',classification='STANDING',source='S1.p1/S1.E1',evidence='Positive strongly convex parameter.'),
 dict(name='hAlphaBeta',literal='alpha <= beta',classification='STANDING',source='S1.E1',evidence='Source ordered nonnegative parameters.'),
 dict(name='hV',literal='ContDiff R 2 V',classification='STANDING',source='S1.p1',evidence='Source global twice continuously differentiable V.'),
 dict(name='hH',literal='forall x v, alpha*norm(v)^2 <= D2V(x)[v,v] and D2V(x)[v,v] <= beta*norm(v)^2',classification='STANDING',source='S1.E1',evidence='One binder contains both exact Hessian bounds, no algorithm-law premise.'),
 dict(name='hEta',literal='0 < eta',classification='STANDING',source='S2.SS2.p1',evidence='Positive source scale.'),
 dict(name='hBetaEta',literal='beta*eta <= 1',classification='STANDING',source='S2.SS2.p1',evidence='Equivalent to eta<=1/beta since beta>=alpha>0.')]
tests=dict(d='A fixed deterministic Borel map Hist_n -> NNReal; all entries accessible, no tail argument, pointwise finite and globally possibly unbounded. d(H_n) is the permitted random duration.',A='Any Borel subset of Hist_n, including zero history-law mass. An admissible deterministic test event, not a seventh analytic assumption.',classification='source-implicit measurable test interface',not_pure_typing=True,not_provider_hypotheses=True,consumer='For deterministic T>=0 use d_T(h)=max(T-t,0) on last live(t,z), stopped0, with the history event also restricted to live and t<=T. Its Borel property follows from the sum cases/projections and continuous positive-part map. This permits the duration required in A.7; I5 must still assemble the final factor.')

math_checks=[
 'The proof repeats all13 literal definitions and change unfolds the private Prop without adding a premise. actual75 is destructured into joint Borel Lambda/tau, Lambda nonnegativity and deterministic-state survival. actual87 gives measurable H/Y and their actual product law; unit-exponential77 gives probability and coordinate0 Exp1 law. The proof does not assume a conditional law.',
 'Borel sum-product distribution makes waitObs measurable on all records/raw clocks. Its proof-only stopped value0 gives u<0 false for u>=0, exactly the public stopped False semantics. Last projection, Borel d and coordinate0 compose into the actual joint event, then measurableSet_lt proves Borelness. No unsupported hitting-time projection is assumed.',
 'The analogous sum-product weightObs is measurable through joint Lambda, negation, exp and ofReal. Composing with last and d proves weight measurability on all histories. Case-splitting the last tag proves weight<=1 everywhere: stopped0 or exp(-Lambda)<=1 by internal Lambda>=0. No realizability or bounded-d hypothesis enters.',
 'For every fixed history h, the stopped fiber is empty. In the live branch, coordinate0 has Exp1 law and the measurable pushforward through clipped tau has exact Ioi(dh) real mass exp(-Lambda(dh)); its probability instance makes ofReal_measureReal valid. This derives the ENNReal fiber equality for every h, including arbitrary/unrealizable ones. Ioi in WithTop includes infinity. No random-u substitution into conditional representatives is used.',
 'C=(A x tailspace) intersect B is Borel. Map_apply identifies its pullback with the literal actual event because H[last]=record n and Y[0]=w_n. The exact actual87 joint law replaces this by historylaw prod P. Measure.prod_apply, the pointwise fiber identity and the indicator identity yield the restricted history lintegral. There is no division by historylaw(A), point-history conditioning or invocation of full A.7.'
]
exposition_checks=[
 'Text and displayed product-law formula name each consumed producer and distinguish raw shifted tail from clipped input. All declared dependencies actually appear in the BODY.',
 'Text explicitly limits the artificial stopped waitObs0 to a proof observable under strict comparison, so it cannot be read as new dynamics. Formula is valid in both sum branches.',
 'Text/formula correctly derive Borel weight and its bound from nonnegative hazard, including unbounded duration functions and all abstract histories.',
 'Text/formula accurately describe fixed-history fiber integration, probability-to-ENNReal conversion and the pointwise-for-every-h strength. Infinite-wait mass is not discarded.',
 'Text/formula correctly use the actual history law, product sections and indicator; the result remains unnormalized. No full path-law or restart claim is introduced.'
]
raw_lines=module_path.read_bytes().splitlines(keepends=True)
regions=[]
assert len(lesson['steps'])==5
for i,s in enumerate(lesson['steps']):
    r=s['lean_source_region']; chunk=b''.join(raw_lines[r['start_line']-1:r['end_line']])
    assert r['source_raw_sha256']==raw(module_path)
    assert hashlib.sha256(chunk).hexdigest()==r['exact_code_raw_sha256']
    assert chunk.decode()==s['lean']
    if i: assert lesson['steps'][i-1]['lean_source_region']['end_line']+1==r['start_line']
    regions.append(dict(**r,title=s['title'],text_sha256=hashlib.sha256(s['text'].encode()).hexdigest(),formula_sha256=hashlib.sha256(s['formula'].encode()).hexdigest(),exact_code_matches=True,mathematics=math_checks[i],exposition=exposition_checks[i],source_boundary='S87-I4 only; no I5/global closure',verdict='accepted'))
assert regions[0]['start_line']==97 and regions[-1]['end_line']==302
body=b''.join(raw_lines[96:302]).decode()
assert body.startswith('  classical\n') and body.rstrip().endswith('lintegral_indicator hA weight')
assert len(re.findall(r'^private def ',module,re.M))==1 and len(re.findall(r'^theorem ',module,re.M))==1
private_text=module[module.index('private def '):module.index('\n\n\nset_option')]
expanded='\n'.join(private_text.splitlines()[1:]).replace(' : Prop :=',' :',1)
assert re.sub(r'\s+',' ',expanded).strip()==re.sub(r'\s+',' ',packet['lean']['statement']).strip()
assert len(re.findall(r'^    let ',private_text,re.M))==13
assert not any(re.search(p,module) for p in [r'\bsorry\b',r'\badmit\b',r'\baxiom\b',r'Prop\s*:=\s*True',r':=\s*trivial',r'\bsorryAx\b'])
write(out/'private-proposition-expansion88.native.json',dict(kind='literal public alias expansion audit',declaration=packet['lean']['declaration'],private_definition='actual_conditional_next_wait_survival_statement',private_definition_exact_text=private_text,packet_statement_exact_text=packet['lean']['statement'],packet_statement_sha256=packet['lean']['statement_sha256'],tokens_match_exact_private_expansion=True,literal_definitions=13,analytic_binders=6,admissible_tests=tests,conclusion_components=['Borel joint liveSurvival event','Borel survivalWeight on all histories','survivalWeight <=1 on all histories','unnormalized actual history-conditioned survival for every Borel A'],proof_body_lines=[97,302],alias_hides_extra_premise=False))
append('SEVEN_SLOT_DEFINITION_BINDER_AND_EXACT_FIVE_REGION_AUDIT_COMPLETED',region_count=5,literal_definitions=13,standing_analytic_binders=6,native_decoder_phrase_explicitly_clarified=True,prior_source_header_decision_contents_replayed_as_BODY_acceptance=False)

class Inspect(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.details=[]; self.code=None; self.codes=[]; self.events=[]; self.steps=0; self.text=[]
    def handle_starttag(self,t,a):
        a=dict(a)
        if t=='details':
            self.details.append(a)
            if a.get('data-inline-lean'): self.events.append(('lean',a['data-inline-lean'],a.get('class','')))
        if 'proof-roadmap' in a.get('class','').split(): self.events.append(('roadmap','',''))
        if 'proof-reader-step' in a.get('class','').split(): self.steps+=1
        if t=='code': self.code=[]
    def handle_data(self,d):
        self.text.append(d)
        if self.code is not None: self.code.append(d)
    def handle_endtag(self,t):
        if t=='code' and self.code is not None: self.codes.append(''.join(self.code)); self.code=None
dom=Inspect(); dom.feed(reader_path.read_text(encoding='utf-8'))
decl=lesson['declaration']; helper=decl+'_statement'
assert len(dom.details)==11 and dom.steps==5 and all('open' not in a for a in dom.details)
assert dom.events[:3]==[('lean',decl,'inline-lean inline-lean-statement'),('lean',helper,'inline-lean inline-lean-proof'),('roadmap','','')]
for s in lesson['steps']: assert any(s['lean'].strip()==c.strip() for c in dom.codes)
helper_code=[c for c in dom.codes if 'private def actual_conditional_next_wait_survival_statement' in c]
assert len(helper_code)==1 and private_text in helper_code[0]
domcheck=dict(kind='independent local HTML DOM/content source check',candidate=pin(reader_path),initially_folded_details=11,steps=5,exact_body_regions_present=5,full_private_proposition_present=True,public_signature_then_private_helper_siblings_before_roadmap=True,informational_observation='The scanner helper disclosure includes trailing set_option maxHeartbeats 1000000 in context after the complete private definition. It adds no source premise and does not affect the complete Prop or any of the five exact BODY regions.',browser_visual_credit=False,interactive_browser_credit=False,svg_or_layout_credit=False,site_build_or_deployment_credit=False)
write(out/'reader-dom-source-check88.native.json',domcheck)
append('LOCAL_HTML_DOM_CONTENT_CHECK_COMPLETED',initially_folded_details=11,exact_BODY_regions=5,browser_or_visual_validation=False)

receipt_path=run/'focused/production6-sum-observable-equality/receipt.json'
receipt=json.loads(receipt_path.read_text(encoding='utf-8'))
assert receipt['exit_code']==0 and receipt['terminal_closed'] is True and receipt['module_RAW']==raw(module_path)
kernel_receipt_path=run/'independent-math88/fresh-whole-source-kernel.receipt.json'
kr=json.loads(kernel_receipt_path.read_text(encoding='utf-8'))
assert kr['exit_code']==0 and kr['terminal_closed'] is True and kr['source']['raw_sha256']==raw(module_path)
for k in ['probe','stdout','stderr']:
    p=root/kr[k]['path']; assert raw(p)==kr[k]['raw_sha256'] and p.stat().st_size==kr[k]['bytes']
kernel_path=root/kr['stdout']['path']; kernel=kernel_path.read_text(encoding='utf-8')
assert 'depends on axioms: [propext,\n Classical.choice,\n Quot.sound]' in kernel and 'sorryAx' not in kernel
producer_paths=[root/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryTailLaw.lean',root/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean',root/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean']
for name in lesson['astis_dependencies']: assert name in kernel
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
compiler=dict(focused_receipt=pin(receipt_path),focused_exit_code=0,checked_module_raw_sha256=raw(module_path),kernel_receipt=pin(kernel_receipt_path),kernel_output=pin(kernel_path),kernel_axioms=['propext','Classical.choice','Quot.sound'],checked_compiler_head=kr['observed_head'],current_head_at_review=head,producer_modules=[pin(p) for p in producer_paths],producer_consumption='actual87 H/Y measurability and joint law; actual75 Lambda/tau measurability, nonnegative Lambda and exact deterministic-state survival; actual77 probability and coordinate0 law. All three named constants occur in the kernel transitive output.',source_reviewer_reran_lean=False,independent_math_verdict_read=False,aggregate_gate_credit=False)

delta_rows=[
 dict(id='S88-D1',slot='conclusion',classification='source-implicit',blocking=False,description='Explicit history-parametric product integration, measurable guarded event/weight and unnormalized survival identity complete a dependency implicit in the authors A.7 iteration. The authors did not print this as a standalone theorem; current prose attributes the ASTIS completion.'),
 dict(id='S88-D2',slot='domains',classification='generalization',blocking=False,description='Source Euclidean formulas are expressed on a finite-dimensional real inner-product Borel space, including rank zero. No new restriction is introduced.'),
 dict(id='S88-D3',slot='domains',classification='representation-elaboration',blocking=False,description='The real product input is clipped into NNReal only for the actual recursion. Nonpositive clocks are P-null; the complete raw tail and Exp1 law are unchanged. The stopped sum encodes source termination without a phase at infinity.'),
 dict(id='S88-D4',slot='assumptions',classification='admissible-test-interface',blocking=False,description='Borel d and A are explicit source-implicit test-class restrictions, not pure typing and not extra analytic hypotheses or providers. All internal measurability, independence and survival conclusions are proved from unchanged six standing analytic binders.'),
 dict(id='S88-D5',slot='quantifiers',classification='notation-resolution',blocking=False,description='Native decoder assumptions say d need not be deterministic. Its exact function quantifier and explicit scopes exclude random unconditioned/future-dependent d; the precise reading is that fixed Borel d may give random d(H_n), not merely a constant duration. Native output remains unchanged; this clarification is separately recorded.'),
 dict(id='S88-D6',slot='scopes',classification='endpoint-and-conditioning-elaboration',blocking=False,description='Strict finite-duration survival, live infinity inclusion, stopped False/zero and unnormalized null-event law preserve source endpoints. A history-law restricted integral equals the frozen P-space formula by measurable pushforward.'),
 dict(id='S88-D7',slot='scopes',classification='residual-boundary-retained',blocking=False,description='Only S87-I4 is supplied. S87-I5 conditional density, ordered-time iteration, final factor assembly/full A.7 and physical-time residual memorylessness/restart/Markovness and all global claims remain open.')
]
boundary=dict(target_source_node='S87-I4',already_verified_parent_substrate=['S87-I1','S87-I2','S87-I3'],local_ingredients_internally_consumed_or_discharged=['S88-A1','S88-A2 via actual75 deterministic survival','S88-P1','S88-P2'],open=['S87-I5','conditional finite-wait density','ordered-time disintegration and iteration','final no-event factor assembly','full A.7','global G86-11 iteration','physical-time residual memorylessness','random stopping/restart/Markovness','nonexplosion/process path construction','reversal/invariance/all-L2 contraction','implementation error/cost/main','actual-input composition/whole paper/Goal'])
edge_cases=dict(
    n_zero='H0 is the singleton deterministic live(0,z0) history; w0 is unused. Arbitrary Borel d restricts to its finite value at that history; the identity is deterministic-state survival or zero when A excludes that history.',
    stopped='For a last stopped tag L=false and W=0. waitObs0 is proof-only under u<0 and introduces no next phase or actual wait. Absorbing tagged recursion consumes no new physical event after termination.',
    live_infinity='A currently live state can have next tau=infinity; Ioi(finite u) in WithTop includes infinity. That survival mass is retained. A subsequent record becomes stopped, with no infinite timestamp/phase.',
    null_A='Historylaw(A)=0 gives zero on both sides via the product/restricted-integral argument. No division, positive event premise or point-history conditional probability is used.',
    zero_duration='Lambda0=0, tau0=0 and positive clocks have tau>0. Live W0=1, stopped W0=0. Equality at the zero raw threshold is excluded and occurs only on a P-null set.',
    strict_endpoint='tau is first >= hazard crossing; for finite u, u<tau(e) iff Lambda(u)<e. A hit exactly at u is excluded, including flat hazard cases. Equality under an independent continuous Exp1 clock has zero mass but definitions retain exact strictness.',
    zero_normal_rate='Total division gives identity bounce at zero gradient difference. Vanishing hazard throughout an orbit permits infinity for every positive threshold; vanishing initial rate alone does not imply this. No rate positivity/strict hazard growth is assumed.',
    rank_zero='The sole phase has zero rate and hazard. Under positive raw clocks H0 is live and histories n>=1 have stopped last tag; W is respectively1 and0 for every finite duration.',
    unrealizable_histories='B_d, W measurability, the bound and fixed-history fiber equality are proved on the whole abstract history space. No earlier-record consistency premise is introduced; only the final law uses the realized pushforward.',
    finite_d_unbounded_function='Every d(h) is finite NNReal, with no global upper bound. W<=1 follows from Lambda>=0. Infinity-valued duration and arbitrary real/negative durations are excluded.',
    fixed_depth_vs_physical_time='n is a fixed natural number. A random physical-time count can reveal the next clock survival and is not substituted here. Raw threshold truncation/residual memorylessness at physical time requires a separate argument.',
    ambient_vs_past='The current theorem needs ambient joint Borel event/weight and H/Y maps. actual87 internally derives the smaller consumed-prefix sigma-algebra measurability and whole-tail independence; these are not assumed of arbitrary histories.',
    final_factor_consumer=tests['consumer'])

snapshots={
 'packet88.exactraw.snapshot.json':packet_path,
 'module88.exactraw.snapshot.lean':module_path,
 'lesson88.exactraw.snapshot.json':lesson_path,
 'publication88.exactraw.snapshot.json':pub_path,
 'decoder88.reconstruction.exactraw.snapshot.json':decoder_dir/'reconstructed-theorem.json',
 'decoder88.run.exactraw.snapshot.json':decoder_dir/'decoder.run.json'
}
for n,p in snapshots.items():
    q=out/n; assert not q.exists(); q.write_bytes(p.read_bytes()); assert raw(q)==raw(p)
append('SOURCE_EQUIVALENCE_DECISION_READY',publication_binding_recomputed=True,complete_primary_spans_rechecked=len(pm['anchors']),whole_module_fake_closure_scan='clear',focused_compile_terminal0=True,sourcegraph_creator_self_independent_validation=False,distinct_topology_evidence_byte_pin=pin(pre/'header-math88/topology-review88.json'),canonical_writes=False,VERIFIED_transition=False)

native_run=dict(schema=1,kind='assistant-authored-independent-BODY-source-review-native-run',reviewer='/root/fresh_source87',formalizer=packet['roles']['formalizer'],decoder=packet['roles']['blind_decoder'],scope='Current complete88 BODY/source/exposition audit, not hidden reasoning trace or theorem-completion transition',packet=pin(packet_path),reviewer_packet_sha256=packet['packet_sha256'],publication_binding_sha256=packet['publication_binding_sha256'],module=pin(module_path),lesson=pin(lesson_path),publication=pin(pub_path),primary=pin(primary_path),primary_first_freeze=pin(pre/'independent-source-first88/source-first88.freeze.native.json'),primary_exact_anchor_span_checks=len(pm['anchors']),sourcegraph=pin(pre/'independent-source-first88/source-proof-slice88.native.json'),sourcecoverage=pin(pre/'independent-source-first88/source-coverage88.native.json'),separate_distinct_topology_review=pin(pre/'header-math88/topology-review88.json'),topology_independence='Source graph was reconstructed before implementation and is unchanged. As its creator, this reviewer does not self-certify independent topology approval; the separately owned distinct77 topology review is byte-bound, not used to infer source topology from Lean or to anchor BODY acceptance.',definition_audit=definitions,binder_audit=binders,admissible_test_class=tests,private_prop_audit=pin(out/'private-proposition-expansion88.native.json'),whole_body_and_exposition=regions,whole_body_summary='All four expanded Prop conclusions are established in five exhaustive contiguous exact proof regions. New text/formula and complete declaration statement agree with the literal definitions and proof mechanism.',decoder_wording_clarification=decoder_clarification,edge_cases=edge_cases,proof_obligation_boundary=boundary,compiler_evidence=compiler,reader_DOM_content=domcheck,publication_audit=dict(source_attribution='Source A.1 iid threshold construction and A.2 measurable recursion are distinguished from attributed ASTIS random-history/duration product integration implicit in A.7.',fixed_source_version='arXiv2609.06905v1, 07 Sep 2026',local_license='arXiv.org perpetual non-exclusive license; long primary extracts remain private and excluded from publication.',binding_scope='Only conditional-survival has the proof-edge; conditional-density-iteration has no binding and remains open.',purification_status='Current metadata remains pending, with inherited Proof pending wording. This review does not grant purification, deployment, whole-paper completion or visual credit.'),independence_attestation=dict(primary_reread_before_fresh_packet=True,preimplementation_freeze_unchanged=True,prior_source_verdict_used_as_anchor=False,prior_independent_math_verdict_read=False,prior_repair_verdict_read=False,formalizer_and_decoder_distinct=True,format_only87_script_read=True,canonical_writes=False,verified_transition=False),outcome='No blocking source/semantic/BODY/exposition delta. Equivalent after explicit elaboration for the one deterministic-depth live-guarded conditional-survival edge only.',chronology=pin(chronology_path))
run_path=out/'source-review88.run.native.json'; write(run_path,native_run)
decision=dict(semantic_slots=slots,deltas=delta_rows,verdict='equivalent-after-elaboration',repairs=[],reviewer='/root/fresh_source87',independent_from_formalizer=True,independent_from_decoder=True,review_evidence='Pinned primary A1.E1/E2/E7 and A.2 reread directly before candidate packet/decoder/production. Unchanged preimplementation freeze and local source graph retained; separate distinct topology evidence byte-bound without self-validation. Fresh exact module, fully expanded private Prop, blind reconstruction, complete public statement and five text/formula/exact Lean regions audited independently. All seven slots agree after explicit source-implicit, representation and native decoder notation elaboration. No blocking repair.',review_run_sha256=raw(run_path),reviewer_packet_sha256=packet['packet_sha256'],reviewer_packet_raw_sha256=raw(packet_path),review_run_artifact=str(run_path),publication_binding_sha256=packet['publication_binding_sha256'],lean_module_raw_sha256=raw(module_path),lesson_raw_sha256=raw(lesson_path),publication_raw_sha256=raw(pub_path),complete_definition_audit=definitions,complete_analytic_binder_audit=binders,admissible_test_class=tests,private_prop_audit='The public alias expands to exactly13 literal lets and four genuine quantified conclusion components; no True or caller certificate. The whole BODY proves each component.',exact_body_exposition_audit=regions,decoder_wording_clarification=decoder_clarification,reader_dom_content_check=domcheck,nonblocking_presentation_observations=[domcheck['informational_observation']],accepted_truth_boundary=boundary,blocking_deltas=[],body_source_fidelity_acceptance=True,topology_creator_self_independent_acceptance=False,theorem_verified_transition=False,whole_paper_acceptance=False,browser_or_layout_acceptance=False)
decision_path=out/'source-review88.decision.native.json'; write(decision_path,decision)
terminal_path=out/'terminal-completion.source-review88.native.json'
write(terminal_path,dict(kind='native independent source review terminal completion',terminal_closed=True,completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),reviewer='/root/fresh_source87',decision=pin(decision_path),review_run=pin(run_path),verdict=decision['verdict'],blocking_delta_count=0,repair_count=0,scope='S87-I4 only',canonical_writes=False,verified_transition=False))
direct_inputs=list(expected)+[root/'lean-toolchain',root/'lake-manifest.json',root/'website/scripts/declaration_lessons.py',receipt_path,kernel_receipt_path,root/kr['probe']['path'],kernel_path,root/kr['stderr']['path'],decoder_dir/'reconstructed-theorem.json',decoder_dir/'reconstructed-theorem.txt',decoder_dir/'decoder.run.json',decoder_dir/'closed-RAW-manifest.json',decoder_dir/'input.packet.RAW.json',decoder_dir/'lean-statement.RAW.txt',decoder_dir/'approved-definition-context.json']+producer_paths
outputs=[p for p in sorted(out.iterdir()) if p.is_file() and not p.name.startswith('closed-raw-manifest')]
manifest=dict(schema=1,kind='closed-RAW-independent-BODY-source-review88-manifest',reviewer='/root/fresh_source87',inputs=[pin(p) for p in direct_inputs],outputs=[pin(p) for p in outputs],reviewer_packet_sha256=packet['packet_sha256'],publication_binding_sha256=packet['publication_binding_sha256'],exact_primary_spans=pm['anchors'],exact_five_body_regions=[{k:r[k] for k in ['path','source_raw_sha256','start_line','end_line','exact_code_raw_sha256']} for r in regions],primary_first_chronology=pin(chronology_path),review_run_sha256=raw(run_path),decision_sha256=raw(decision_path),terminal_completion_sha256=raw(terminal_path),inherited_evidence_handling='Unchanged preimplementation source-first88 and header-source88 bytes are preserved; header decision is byte-pinned only, never substituted for current BODY acceptance. Sourcegraph creator does not self-independentvalidate topology. Separate distinct77 review bytes retained. No independent mathematical verdict or older source verdict was used as a BODY anchor.',privacy='Long pinned-primary reread text exists only in primary88.reread-before-BODY.private.json, excluded from publication. Other outputs use attributed restatement/anchors and exact Lean/public prose.',closure_rule='All inputs and outputs pinned with RAW SHA256 and byte count. This manifest excludes itself to avoid a hash cycle. Native decision/run/chronology are complete, no shared/canonical writes or VERIFIED transition.')
manifest_path=out/'closed-raw-manifest.source-review88.native.json'; write(manifest_path,manifest)
for section in ['inputs','outputs']:
    for p in manifest[section]:
        q=Path(p['path']); assert raw(q)==p['raw_sha256'] and q.stat().st_size==p['bytes']
for p in [decision_path,run_path,manifest_path,chronology_path,terminal_path]: print(p.name,raw(p))
print('CLOSED',len(manifest['inputs']),'inputs',len(manifest['outputs']),'outputs',len(regions),'exact BODY regions',len(pm['anchors']),'primary spans')
