from pathlib import Path
from html.parser import HTMLParser
import json
import hashlib
import datetime
import re
import subprocess

root=Path('E:/Samplinglib')
out=Path(__file__).resolve().parent
run=out.parent
pre=root/'runs/20261007-companion-priority/pbps-clock-tail-preread87'
packet_path=run/'source-review87.packet.json'
module_path=root/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryTailLaw.lean'
lesson_path=root/'website/content/declaration_lessons/pbps-actual-finite-history-tail-law.json'
publication_path=root/'website/content/publications/pbps-actual-finite-history-tail-law.json'
reader_path=run/'reader-candidate87.html'
def rawhash(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def jsonhash(value):return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def write(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def pin(path):return dict(path=str(path.resolve()),raw_sha256=rawhash(path),bytes=path.stat().st_size)
expected={packet_path:'e24b4fdcd7281c04a48793e76c62bf20034527f14db1cee0e02b411c399b76f3',module_path:'01fcff944f1dbd42be2af30063b9baf4e191e2cde959e008724387cadb4fc899',lesson_path:'e6ba01830259ed4d886647c062c6658e07bcd4711636a93354b158c0d12719d5',publication_path:'a8088607020c8685a5d675e7e5cce4de212aafb473e6a4877393d4da27c3a030',reader_path:'8831c856570333846dae05ac2670d7444c69eeee2f238c1dd1e5e1a86c5e8864'}
for path,value in expected.items():assert rawhash(path)==value,(str(path),rawhash(path))
packet=json.loads(packet_path.read_text(encoding='utf-8'))
assert jsonhash({k:v for k,v in packet.items() if k!='packet_sha256'})==packet['packet_sha256']
assert packet['packet_sha256']=='876795a8b0d8ee2e569bf89bde988cb05a0e2a67aa3e8f527450a36139cb91a8'
assert packet['publication_binding_sha256']=='aca18a420581e6d76f5404a9991db270c46f875aabf7672488ad4a3c8fe05f59'
module=module_path.read_text(encoding='utf-8')
lesson=json.loads(lesson_path.read_text(encoding='utf-8'))['units'][0]
pub=json.loads(publication_path.read_text(encoding='utf-8'))['items'][0]
context=packet['candidate_publication_context']
assert context['current_lean_module']==module
payload={**{k:context[k] for k in ['file','current_lean_module','toolchain','dependencies']},**{k:pub[k] for k in ['source','statement','formulae','assumptions','obligations']},'lesson':lesson,'binding':{k:v for k,v in pub['bindings'][0].items() if k not in ['audit_id','legacy_audit_debt']}}
assert jsonhash(payload)==packet['publication_binding_sha256']
for path,key in [(root/'lean-toolchain','toolchain'),(root/'lake-manifest.json','dependencies')]:assert hashlib.sha256(path.read_text(encoding='utf-8').encode()).hexdigest()==context[key]
for key,textkey,hashkey in [('source','original_text','text_sha256'),('lean','statement','statement_sha256'),('blind_reconstruction','text','text_sha256')]:assert hashlib.sha256(packet[key][textkey].encode()).hexdigest()==packet[key][hashkey]
assert packet['blind_reconstruction']['source_text_visible'] is False
assert len({packet['roles']['formalizer'],packet['roles']['blind_decoder'],'/root/fresh_source87'})==3
freeze_path=pre/'independent-source-first87/source-first.freeze.native.json'
assert rawhash(freeze_path)=='d8e37422b5597b0a5761282bcf88b94453a7b21a5176ef0cb71c2363f5ab87d7'
primary_manifest_path=pre/'independent-source-first87/primary-source.raw-manifest.native.json'
primary_manifest=json.loads(primary_manifest_path.read_text(encoding='utf-8'))
primary_path=Path(primary_manifest['source']['local_path']);primary=primary_path.read_bytes()
assert rawhash(primary_path)==primary_manifest['source']['raw_sha256']
for anchor in primary_manifest['anchors']:assert hashlib.sha256(primary[anchor['byte_start_zero_based']:anchor['byte_end_exclusive']]).hexdigest()==anchor['raw_span_sha256']
assert b'License: arXiv.org perpetual non-exclusive license' in primary
assert b'arXiv:2609.06905v1' in primary
assert len(re.findall(r'^private def ',module,re.M))==1
assert len(re.findall(r'^theorem ',module,re.M))==1
fake_patterns=[r'\bsorry\b',r'\badmit\b',r'\baxiom\b',r'Prop\s*:=\s*True',r':=\s*trivial',r'\bsorryAx\b']
assert not any(re.search(pattern,module) for pattern in fake_patterns)
region_checks=[]
raw_lines=module_path.read_bytes().splitlines(keepends=True)
mathematical_checks=[
 'All thirteen literal local definitions are repeated without semantic mutation; change unfolds the private proposition. Existing actual-recursion measurability and product-clock probability/mutual independence are consumed internally. The analytic hypotheses are supplied only to existing producers; no theorem-shaped caller certificate appears.',
 'Induction proves that record m consumes only coordinates below m. The successor uses e_m and the earlier record; Fin(n+1) then yields j<=n and pointwise causality of the history. Coordinate clipping and joint measurable recursion give ambient history measurability; coordinate reindexing gives ambient tail measurability.',
 'The proof-only truncated input keeps clipped coordinates below n and sets all others to zero. Each coordinate is measurable from past n by comap inclusion or constancy. It is a factorization tool, not a changed clock law or source algorithm.',
 'For j<=n, truncated and actual inputs agree below j, so causality identifies their records. Compose the joint measurable record map with deterministic parameters and the past-measurable truncated stream. This proves the smaller-domain F_n measurability rather than relying on ambient measurability.',
 'The future sigma algebra is generated by raw coordinates k>=n. Disjoint index ranges and mutual coordinate independence give independent generated sigma algebras. Measurability of H_n and Y_n in their respective blocks gives their independence. The imported generated-sigma-algebra theorem covers the complete countable tail, not only finite cylinders.',
 'The injective shift k->n+k preserves the identical-factor infinite product law. Independence plus ambient measurability gives the joint product law. For every measurable tail B, restricted pushforward evaluates to P(H_n in A and Y_n in B), factors, and uses unchanged tail law; measure extensionality yields the unnormalized identity, including zero-mass A.'
]
for i,step in enumerate(lesson['steps']):
 region=step['lean_source_region'];chunk=b''.join(raw_lines[region['start_line']-1:region['end_line']])
 assert hashlib.sha256(chunk).hexdigest()==region['exact_code_raw_sha256']
 assert chunk.decode()==step['lean']
 region_checks.append(dict(region_number=i+1,**region,mathematics='accepted',exposition='accepted',independent_reason=mathematical_checks[i],text_read=True,formula_read=True,exact_lean_read=True))
assert [(r['start_line'],r['end_line']) for r in region_checks]==[(87,147),(148,171),(172,186),(187,200),(201,218),(219,237)]

class DOM(HTMLParser):
 def __init__(self):super().__init__();self.stack=[];self.nodes=[];self.codes=[];self.code=None;self.order=0
 def handle_starttag(self,tag,attrs):
  self.order+=1
  node=dict(tag=tag,attrs=dict(attrs),parent=self.stack[-1] if self.stack else None,order=self.order)
  index=len(self.nodes);self.nodes.append(node)
  if tag not in ['meta','link','br','hr','input','img']:self.stack.append(index)
  if tag=='code':self.code=[]
 def handle_endtag(self,tag):
  if tag=='code' and self.code is not None:self.codes.append(''.join(self.code));self.code=None
  for i in range(len(self.stack)-1,-1,-1):
   if self.nodes[self.stack[i]]['tag']==tag:self.stack=self.stack[:i];break
 def handle_data(self,text):
  if self.code is not None:self.code.append(text)
dom=DOM();dom.feed(reader_path.read_text(encoding='utf-8'))
details=[n for n in dom.nodes if n['tag']=='details'];assert len(details)==12
assert not any('open' in n['attrs'] for n in details)
signature=[n for n in details if 'inline-lean-statement' in n['attrs'].get('class','')][0]
helper=[n for n in details if n['attrs'].get('data-inline-lean','').endswith('.actual_finite_history_tail_law_statement')][0]
roadmap=[n for n in dom.nodes if n['attrs'].get('class')=='proof-roadmap'][0]
assert signature['parent']==helper['parent']
assert signature['order']<helper['order']<roadmap['order']
for step in lesson['steps']:assert step['lean'] in dom.codes
reader_checks=dict(kind='DOM/content-only; not browser or layout verification',input=pin(reader_path),details=12,initially_open_details=0,
 exact_body_regions_present=6,public_signature_and_literal_prop_helper='Separate siblings before roadmap',
 full_prop_present=True,full_body_present=True,statement_and_all_six_authored_mathematical_explanations_read=True,
 informational_observation='The helper disclosure includes the trailing set_option maxHeartbeats 1600000 in scanner context preceding the theorem. This is extra source context, not an additional hypothesis or changed declaration; it does not alter the full proposition or any of the six exact proof regions.',
 browser_visual_credit=False,mobile_layout_credit=False,svg_visual_credit=False)
write(out/'reader-dom-source-check87.native.json',reader_checks)

def slot(original,reconstructed,evidence,relation='equivalent'):
 return dict(original=original,reconstructed=reconstructed,relation=relation,evidence=evidence)
slots={
 'objects':slot('The attributed source restatement fixes the authors actual harmonic flow, bounce/intensity, integrated-hazard stopped recursion, unit-exponential clock product, complete finite record history and unused infinite raw clock tail.',
 'The blind decoder reconstructs these same flow/bounce/hazard/hitting/record maps, product-clock space, clipped input, history, raw tail and past sigma algebra.',
 'Primary A1.SS1.p1/p2 and A1.E1/E2; current private proposition lines17-76 and public proof repeated lets; blind reconstruction expressly distinguishes tagged stopped states, clipped inputs and raw tail.'),
 'domains':slot('Finite-dimensional real inner-product Borel space, including dimension zero; V:E->R; nonnegative alpha,beta; eta real; fixed y,r,z0; nonnegative waits with infinity; countable real product clock space; history in a finite product of tagged live/stopped records.',
 'The decoder gives the same finite-dimensional/Borel setting, the same NNReal or extended waiting times, the same tagged record space and real clock product. Clipping is pointwise on all raw sequences, and raw tail is unclipped.',
 'Current c/Phi/S/rate/Lambda/tau/next/record/P/epsilon/history/tail definitions match the attributed statement. The representation extends positive-source-clock dynamics only on a P-null nonpositive-clock set. The Euclidean-to-finite-dimensional generalization is explicit and has no extra mathematical restriction.'),
 'quantifiers':slot('For every fixed analytic input satisfying the six premises and every deterministic y,r,z0,n, all conclusions hold; prefix equality is for all real w,w-prime; the last identity holds for every measurable history event A.',
 'The decoder gives universal deterministic parameters/depth, pointwise all-stream causality, and all measurable history events with no positive-mass requirement.',
 'Private proposition final universal binders and explicit forall w,w-prime,A; Fin(n+1) means depths0..n, each j<=n. The raw shift n+k starts at source E_(n+1), so the first n inputs only are consumed.'),
 'assumptions':slot('Positive alpha, alpha<=beta, C2 V, pointwise two-sided Hessian bounds, positive eta, beta*eta<=1, with finite-dimensional inner-product/Borel carrier data. The iid input model is defined, while measurability/causality/independence/laws are conclusions.',
 'The decoder lists exactly those analytic assumptions and carrier structures, defines the probability model, and does not request an external independence or regularity certificate.',
 'Expanded private Prop and theorem signatures retain exactly six analytic binders; hrec and hinput are internal compiled producers. No bundled assumption hides an independence conclusion or a random-history hypothesis.'),
 'conclusion':slot('Ambient measurability of H_n and Y_n, pointwise prefix causality, explicit F_n-measurability of H_n, unchanged full-tail law, independence, joint law and unnormalized restricted-tail pushforward identity.',
 'The decoder reconstructs every conclusion, including the whole-measure product and restriction identities; no regular conditional distribution or division by point-history probabilities is introduced.',
 'All eight final conjunction components are reproduced in the blind text; the current proof constructs hHmeas,hTmeas,hprefix,hHp,htailLaw,hindep,hjoint and proves the final identity by Measure.ext and event factorization.'),
 'scopes':slot('Only deterministic event depth; complete infinite raw tail independent of generated finite stopped history. Ambient measurability and measurability in the smaller past sigma algebra are distinct. Random-hazard integration, finite-event density/final survival/A.7 and physical-time residual memorylessness remain open.',
 'The decoder explicitly separates ambient history/tail measurability from F_n history measurability, gives the full infinite unclipped tail, retains stopped tags and excludes random indices, explosion, trajectory invariance and costs.',
 'Region3/4 factorization proves F_n scope; region5 generated-sigma-algebra independence covers the whole tail. The module and all reviewed prose scope this as an ASTIS source-implicit probability completion; accepted source-slice v2 marks only I1-I3 in scope, I4/I5 open.'),
 'constant_dependencies':slot('Rate-one exponential input distribution; fixed analytic alpha,beta,eta; arbitrary fixed y,r,z0,n; no failure budget, event-rate cap or cost constant is required for this local probability substrate.',
 'The decoder retains the same unit-rate product law and six parameter premises with no additional constant, horizon, random stopping parameter or running-cost assertion.',
 'P uses expMeasure 1 throughout; tail reindexing uses identical factors. The proof does not use or claim a bounded-rate/non-explosion estimate; those remain separate global consumers.')
}

definitions=[
 ('c','Source3.4 center y-eta*gradient(V,r); literal for all fixed parameters.'),
 ('Phi','Source harmonic flow with cos/sin and momentum coefficient -sin/sqrt(eta); eta>0 makes the formula source-equivalent.'),
 ('S','Reflection in gradient-difference normal. Total real division gives identity at zero normal, exactly R0=I; no nonzero-normal premise.'),
 ('rate','sqrt(eta)*max(0,inner(momentum,gradient difference)); source positive-part intensity.'),
 ('Lambda','Interval integral from0 to nonnegative t of literal intensity along literal flow; no rate surrogate or cap substituted.'),
 ('tau','hittingAfter of Lambda-e in Ici0 after time0; source first crossing with >= and empty-set infinity. This is a literal infimum, not a choice from an assumed existence theorem.'),
 ('next','Tagged stopped branch is absorbing; infinite crossing yields stop; only finite crossing branch uses untopD0, adds finite time and bounces flowed state. No phase at infinity is invented.'),
 ('record','Nat recursion initialized at live(0,z0); successor stage k consumes e_k. Finite full stopped history is a lossless tagged encoding of source termination.'),
 ('P','Countable infinite product of rate-one exponential measures on real raw coordinates; realizes the source mutual iid law without a caller provider.'),
 ('epsilon','Real.toNNReal pointwise clipping; literal on all raw streams of the explicitly extended carrier. Under P all clocks are positive almost surely, so this is source-equivalent with a declared null-set ambient extension.'),
 ('history','Fin(n+1) record evaluations0..n on clipped inputs, including stopped tags; no future/no-event physical-time information is inserted.'),
 ('tail','All raw real coordinates w(n+k), k>=0; not clipped, finite, normalized, stopped or adaptively reindexed.'),
 ('past','Supremum of coordinate-comap sigma algebras for k<n. It is the consumed-prefix sigma algebra; the tail is not asserted measurable in this smaller past sigma algebra.')
]
definition_audit=[dict(name=name,definition_kind='literal',verdict='accepted',evidence=evidence) for name,evidence in definitions]
binder_audit=[
 dict(name='hAlpha',classification='STANDING',source='S1.p1/S1.E1',meaning='0<alpha; source strongly convex parameter positivity.'),
 dict(name='hAlphaBeta',classification='STANDING',source='S1.p1/S1.E1',meaning='alpha<=beta, alpha/beta nonnegative carriers.'),
 dict(name='hV',classification='STANDING',source='S1.p1',meaning='V is C2 globally.'),
 dict(name='hH',classification='STANDING',source='S1.E1',meaning='For every x,v, alpha*norm(v)^2 <= D2V(x)[v,v] <= beta*norm(v)^2. This one binder contains both printed Hessian bounds, not a new proof conclusion.'),
 dict(name='hEta',classification='STANDING',source='S2.SS2.p1',meaning='eta>0.'),
 dict(name='hBetaEta',classification='STANDING',source='S2.SS2.p1',meaning='beta*eta<=1, equivalent to eta<=1/beta since beta>=alpha>0.')]
delta_rows=[
 dict(id='S87-D1',slot='conclusion',classification='source-implicit',blocking=False,description='The explicit finite-prefix/tail sigma-algebra argument, full-tail joint law and restriction identity are ASTIS completions of the source clock iteration, not a standalone theorem printed by the authors.'),
 dict(id='S87-D2',slot='domains',classification='generalization',blocking=False,description='The source Euclidean setting is expressed on any finite-dimensional real inner-product Borel space, explicitly including dimension zero; the local statement and recursion remain valid and no extra restriction is imposed.'),
 dict(id='S87-D3',slot='domains',classification='representation-elaboration',blocking=False,description='Raw real clocks are clipped into nonnegative inputs on the ambient sample carrier; the nonpositive-coordinate set is P-null. The tail remains the entire raw real sequence. The statement explicitly labels this extension and does not give negative clocks new source meaning.'),
 dict(id='S87-D4',slot='scopes',classification='endpoint-and-conditioning-elaboration',blocking=False,description='The stopped sum and guarded finite extraction preserve infinite-wait termination. The final identity is deliberately unnormalized and includes null history events, avoiding unsupported pointwise conditioning.'),
 dict(id='S87-D5',slot='scopes',classification='residual-boundary-retained',blocking=False,description='S87-I4/I5 and the remainder of G86-11 are open: random-hazard conditional survival/density, final survival/iteration, full A.7, physical-time residual memorylessness, Markovness/invariance/cost/main/composition are not conclusions here.')]

receipt_path=run/'independent-math87/fresh-focused-build.receipt.json'
receipt=json.loads(receipt_path.read_text(encoding='utf-8'))
assert receipt['exit_code']==0 and receipt['terminal_closed'] is True
assert receipt['source']['raw_sha256']==expected[module_path]
for stream in ['stdout','stderr']:
 p=root/receipt[stream]['path'];assert rawhash(p)==receipt[stream]['raw_sha256']
kernel_log=run/'independent-math87/fresh-whole-source-kernel.stdout.log'
kernel=kernel_log.read_text(encoding='utf-8')
assert "depends on axioms: [propext,\n Classical.choice,\n Quot.sound]" in kernel
assert 'sorryAx' not in kernel
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
assert head==receipt['observed_head']
compiler_evidence=dict(focused_receipt=pin(receipt_path),focused_exit_code=0,observed_head=head,checked_module_raw_sha256=rawhash(module_path),
 named_declaration=packet['lean']['declaration'],kernel_log=pin(kernel_log),kernel_axioms=['propext','Classical.choice','Quot.sound'],
 source_reviewer_reran_lean=False,evidence_scope='Fresh independent compiler receipt and whole-source kernel output read; no prior mathematical/source verdict read. Aggregate repository gates are not certified by this source review.')

chronology=[
 dict(sequence=1,event='Reused primary-first freeze and source RAW manifest after previous bytes-only unchanged check',source_raw_sha256=rawhash(primary_path),freeze_raw_sha256=rawhash(freeze_path)),
 dict(sequence=2,event='Fresh anti-anchored canonical source-review packet received and RAW/canonical hashes checked',packet_raw_sha256=rawhash(packet_path),packet_sha256=packet['packet_sha256']),
 dict(sequence=3,event='Read complete current module, private expanded proposition, fresh blind reconstruction, current lesson and publication; no old verdict/repair review read'),
 dict(sequence=4,event='Checked six contiguous exact BODY regions and read each new mathematical exposition/formula against the corresponding code'),
 dict(sequence=5,event='Independently checked current reader HTML DOM/content only; no browser or SVG/layout verification'),
 dict(sequence=6,event='Recomputed publication binding from current code/prose/binding; reviewed fresh compile/kernel evidence and ran whole-module fake-closure scan'),
 dict(sequence=7,event='Independent source-equivalence findings authored; no canonical writes, no VERIFIED transition and no repair self-approval')]
chronology_path=out/'chronology.source-review87.native.jsonl'
chronology_path.write_text(''.join(json.dumps(dict(e,recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),ensure_ascii=False)+'\n' for e in chronology),encoding='utf-8')
native_run=dict(schema=1,kind='assistant-authored-independent-source-review-native-run',reviewer='/root/fresh_source87',formalizer=packet['roles']['formalizer'],decoder=packet['roles']['blind_decoder'],
 scope='Exact current BODY/source/exposition semantic audit, not theorem completion or hidden reasoning trace',
 packet=pin(packet_path),reviewer_packet_sha256=packet['packet_sha256'],publication_binding_sha256=packet['publication_binding_sha256'],module=pin(module_path),lesson=pin(lesson_path),publication=pin(publication_path),
 checked_head=head,primary_source=pin(primary_path),primary_first_freeze=pin(freeze_path),primary_anchor_span_checks=len(primary_manifest['anchors']),
 definition_audit=definition_audit,binder_audit=binder_audit,whole_body_and_exposition=region_checks,
 proof_obligation_boundary=dict(closed_substrate=['S87-I1','S87-I2','S87-I3'],open=['S87-I4','S87-I5','conditional remainder of G86-11','G86-13','G86-14','G86-15','full A.7','physical-time residual memorylessness','random stopping/restart/Markovness','reversal/invariance/all-L2','cost/main/composition/whole paper/Goal']),
 edge_cases=dict(n_zero='H0 contains only deterministic live(0,z0), F0 is bottom and Y0 is identity; all identities reduce correctly.',stopped='Absorbing stop flag only uses consumed inputs; future clocks still exist under the original product P. Infinite wait is permitted, and no later phase value is claimed.',null_history_event='Restriction to a null preimage yields the zero measure; no positive mass or normalization is used.',zero_normal='Total division gives zero reflection correction, hence identity.',zero_rate='Positive clocks yield empty hazard crossings and a stop; zero clocks occur only in ambient/null extensions.',ambient_vs_past='H_n has both ambient and F_n measurability; Y_n ambient/future measurability is proved, not F_n measurability.',full_tail_vs_clipping='The probability law is always raw product P; only inputs to the literal recursion are clipped. Proof-only truncation affects no coordinate used by H_n.',random_stopping='No substitution of random n is authorized; N_t can reveal unused-clock survival. Residual memorylessness remains a separate argument.'),
 compiler_evidence=compiler_evidence,reader_dom_check=pin(out/'reader-dom-source-check87.native.json'),
 publication_audit=dict(source_attribution='The authors iid threshold construction/A.1-A.2 and explicit later Borel argument are separated from the attributed ASTIS prefix/tail completion.',source_version_and_license='Pinned raw v1 identifier and arXiv perpetual non-exclusive license checked locally; long primary extracts remain in excluded private source-first files.',support='The sole proof-edge supports actual-history-tail only. conditional-iteration has no binding and remains open.',metadata='Pending purification/dead_code_audit wording is process state, not a claim of reader purification; no whole-paper status credit is inferred.'),
 independence_attestation=dict(primary_first=True,prior_source_verdict_contents_read=False,prior_repair_review_contents_read=False,formalizer_and_decoder_distinct=True,canonical_writes=False,verified_transition=False),
 outcome='No blocking semantic/source/BODY/exposition delta. Accept equivalence after elaboration for this attributed deterministic-depth source-implicit substrate only.')
native_run_path=out/'source-review87.run.native.json';write(native_run_path,native_run)
decision=dict(semantic_slots=slots,deltas=delta_rows,verdict='equivalent-after-elaboration',repairs=[],reviewer='/root/fresh_source87',
 independent_from_formalizer=True,independent_from_decoder=True,
 review_evidence='Read pinned primary first before candidate exposure; reused unchanged independently validated local source graph. Fresh packet/current full module/private Prop, blind reconstruction, all six exact regions and new prose independently audited. All seven semantic slots agree after explicit finite-dimensional/representation/source-implicit elaboration; no blocking delta. Entire review is restricted to the deterministic-depth unused-tail substrate.',
 review_run_sha256=rawhash(native_run_path),reviewer_packet_sha256=packet['packet_sha256'],
 reviewer_packet_raw_sha256=rawhash(packet_path),review_run_artifact=str(native_run_path),publication_binding_sha256=packet['publication_binding_sha256'],
 lean_module_raw_sha256=rawhash(module_path),lesson_raw_sha256=rawhash(lesson_path),publication_raw_sha256=rawhash(publication_path),
 complete_definition_audit=definition_audit,complete_analytic_binder_audit=binder_audit,
 private_prop_audit='Expanded the one private Prop alias in full: thirteen literal let definitions and the eight genuine conclusion components; neither True nor an assumed result. The public proof unfolds/reconstructs this proposition and establishes every component.',
 exact_body_exposition_audit=region_checks,reader_dom_content_check=reader_checks,
 nonblocking_presentation_observations=[reader_checks['informational_observation']],
 accepted_truth_boundary=native_run['proof_obligation_boundary'],blocking_deltas=[],body_source_fidelity_acceptance=True,
 theorem_verified_transition=False,whole_paper_acceptance=False,browser_or_layout_acceptance=False)
decision_path=out/'source-review87.decision.native.json';write(decision_path,decision)
snapshot_path=out/'source-review87.packet.exactraw.snapshot.json';snapshot_path.write_bytes(packet_path.read_bytes())

direct_inputs=[packet_path,module_path,lesson_path,publication_path,reader_path,primary_path,freeze_path,primary_manifest_path,
 pre/'independent-source-first87/chronology.native.jsonl',pre/'source-slice87.v2.json',
 run/'header-source87/closed-raw-manifest.header-source87.native.json',root/'lean-toolchain',root/'lake-manifest.json',
 root/'website/scripts/declaration_lessons.py',receipt_path,kernel_log,
 root/receipt['stdout']['path'],root/receipt['stderr']['path']]
outputs=[p for p in sorted(out.iterdir()) if p.is_file() and p.name!='closed-raw-manifest.source-review87.native.json']
manifest=dict(schema=1,kind='closed-RAW-independent-BODY-source-review87-manifest',reviewer='/root/fresh_source87',
 reviewer_packet_sha256=packet['packet_sha256'],publication_binding_sha256=packet['publication_binding_sha256'],
 inputs=[pin(p) for p in direct_inputs],outputs=[pin(p) for p in outputs],
 exact_primary_spans=primary_manifest['anchors'],exact_six_body_regions=[{k:r[k] for k in ['path','source_raw_sha256','start_line','end_line','exact_code_raw_sha256']} for r in region_checks],
 inherited_evidence_handling='Primary freeze/RAW and independently validated v2 topology reused unchanged. Header manifest is byte-pinned only, not replayed as BODY acceptance. Old semantic verdict/repair content not read.',
 run_sha256=rawhash(native_run_path),decision_sha256=rawhash(decision_path),chronology_sha256=rawhash(chronology_path))
manifest_path=out/'closed-raw-manifest.source-review87.native.json';write(manifest_path,manifest)
for path in [decision_path,native_run_path,manifest_path,chronology_path,out/'reader-dom-source-check87.native.json']:
 print(path.name,rawhash(path))
