from pathlib import Path
import json, hashlib, re, datetime, shutil

root=Path('E:/Samplinglib')
out=Path(__file__).resolve().parent
r89=out.parent
pre=root/'runs/20261007-companion-priority/pbps-conditional-next-wait-density-preread89'
sf=pre/'independent-source-first89'
def sha(b): return hashlib.sha256(b).hexdigest()
def raw(p): return sha(p.read_bytes())
def pin(p): return dict(path=str(p.resolve()),raw_sha256=raw(p),bytes=p.stat().st_size,hash_mode='exact-raw-file-bytes')
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def canon(v): return sha(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def write(n,v):
 p=out/n; assert not p.exists(),n
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');return p
def copy(p,n):
 q=out/n;assert not q.exists();shutil.copyfile(p,q);assert raw(p)==raw(q);return q

packet_path=r89/'source-review89.packet.json';packet=read(packet_path)
assert raw(packet_path)=='c2f73e5ef620c8056a35213a614724c0917ae5569d8113279fdf9c6cd15e30e0'
packet_canonical=canon({k:v for k,v in packet.items() if k!='packet_sha256'})
assert packet_canonical==packet['packet_sha256']=='2c336852a39e280610628e129e2f29b8edd1c77a1468bb943ae4d81501392f2f'
module=root/packet['lean']['file'];lesson_path=root/'website/content/declaration_lessons/pbps-actual-conditional-next-wait-density.json';pub_path=root/'website/content/publications/pbps-actual-conditional-next-wait-density.json'
assert raw(module)=='36813b659cbdbb4b31c6300abd1300858d42afe683046b8c06ff9c22806e8e37'
assert raw(lesson_path)=='e79d7ece6c0ef61a19caa473448b14d0b5e5001ae756cb394f4281514f1bb1c4'
lesson=read(lesson_path)['units'][0];pub=read(pub_path)['items'][0];binding=pub['bindings'][0];ctx=packet['candidate_publication_context']
assert ctx['current_lean_module']==module.read_text(encoding='utf-8')
assert ctx['lesson']=={k:v for k,v in lesson.items() if k not in ['boundary','source_history_boundary']}
for k in ['source','statement','formulae','assumptions','obligations']:assert ctx[k]==pub[k]
payload={k:ctx[k] for k in ['file','current_lean_module','toolchain','dependencies','source','statement','formulae','assumptions','obligations']}
payload.update(lesson=lesson,binding={k:v for k,v in binding.items() if k not in ['audit_id','legacy_audit_debt']})
assert canon(payload)==packet['publication_binding_sha256']=='4da0587d22739a11e111fc835b19408cd722d156f6876a03b84ef1c2673e2ade'
for k,p in [('toolchain',root/'lean-toolchain'),('dependencies',root/'lake-manifest.json')]:assert sha(p.read_text(encoding='utf-8').encode())==ctx[k]
for k,field in [('source','original_text'),('lean','statement')]:assert sha(packet[k][field].encode())==packet[k]['text_sha256' if k=='source' else 'statement_sha256']

preread=out/'closed-raw-manifest.final-preread89.native.json'
assert raw(preread)=='8e880bc194cf9a425b807d5485bf0bb15e02508797ce70a4b023fafd22efc97c'
for section in ['inputs','outputs']:
 for e in read(preread)[section]:
  p=Path(e['path']);assert raw(p)==e['raw_sha256'] and p.stat().st_size==e['bytes']
inventory=read(out/'final-primary-source-math-inventory89.native.json')
primary=root/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
assert raw(primary)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
for a in inventory['anchors']:assert sha(primary.read_bytes()[a['byte_start_zero_based']:a['byte_end_exclusive']])==a['raw_span_sha256']

decdir=root/'runs/semantic-decoder-outputs/round89';decpath=decdir/'reconstruction.json';dec=read(decpath);decrun=decdir/'decoder-run.json';decmanifest=decdir/'manifest.json';neutral=root/'runs/semantic-decoder-inputs/round89/packet.json'
assert dec['decoder_run_sha256']==raw(decrun)==packet['blind_reconstruction']['decoder_run_sha256']
assert dec['reconstructed_theorem_text']==packet['blind_reconstruction']['text']
assert sha(dec['reconstructed_theorem_text'].encode())==dec['reconstructed_text_sha256']==packet['blind_reconstruction']['text_sha256']
assert raw(neutral)==dec['decoder']['input_raw_sha256']
for section in ['inputs','outputs']:
 for e in read(decmanifest)[section]:
  p=Path(e['path']);assert raw(p)==e['sha256'] and p.stat().st_size==e['bytes']
neutral_obj=read(neutral)
assert canon({k:v for k,v in neutral_obj.items() if k!='packet_sha256'})==packet['blind_reconstruction']['decoder_packet_sha256']

model_text=packet['lean']['statement'];text=module.read_text(encoding='utf-8');lines=module.read_bytes().splitlines(keepends=True)
private=text.split('private def actual_conditional_next_wait_density_statement',1)[1].split('set_option maxHeartbeats',1)[0]
expanded=private.replace(': Prop :=',':',1).strip()
assert re.sub(r'\s+',' ',expanded)==re.sub(r'\s+',' ',model_text.strip())
names=re.findall(r'^\s+let ([^\s:]+)',model_text,re.M)
assert names==['c','Φ','S','rate','Λ','τ','next','record','P','ε','history','waitObs','timeObs','density','Hist','last','H','μ','D','K','B','X','ν']
semantics=[
 'c(y,r)=y-eta gradient V(r), source proximal-reference center.',
 'Literal harmonic flow with cos/sin and sqrt eta scaling, for every real time; no time rescaling.',
 'Literal gradient-difference reflection with coefficient2; total real division gives identity at gradient difference0.',
 'sqrt eta times positive part of velocity-gradient inner product; not absolute value or an assumed hazard.',
 'Real interval integral from0 to finite NNReal time of actual rate along actual flow.',
 'hittingAfter closed nonnegative target for Lambda-e from0; infimum empty is top; e0 may produce wait0.',
 'Absorbing stopped update, live no-hit becomes stopped, otherwise append actual finite time and reflected flowed state.',
 'Nat recursion initial live(0,z0), update k uses e_k, no sampled-time or random-index recurrence.',
 'Countable product of rate-one real exponential measures, supplied literally as a definition.',
 'Real.toNNReal on each raw coordinate; explicit ambient extension outside positive source-clock support.',
 'Complete record tuple indices0..n, fixed deterministic n, including absorbing stopped records.',
 'Live tau using clipped real threshold; stopped0; absolute accumulated time ignored for this relative wait.',
 'Real extraction untopD0: correct finite wait on B, auxiliary0 at top/stopped; not a replacement dynamics.',
 'Live ofReal(rate at raw real s times exp(-Lambda(toNNReal s))); stopped0; nonpositive-time extension killed by D.',
 'Full Borel product of tagged records Fin(n+1), includes inconsistent/unrealizable histories.',
 'Deterministic last index n with proof n<n+1.',
 'Actual deterministic-depth history map with same y,r,z0,n as actual recursion.',
 'Actual history pushforward H_*P, no external history law provider.',
 'Strict guard 0<s<d(h) multiplying literal density; d finite NNReal at every h.',
 'Mathlib const real-volume kernel.withDensity D; joint measurability and explicit fiber identity rule out fallback0.',
 'Actual strict positive extended wait below finite d(H), using record n and raw w_n; infinity/stopped/zero excluded.',
 'Actual joint (H,total-real-wait) observation; only restricted to B in its density law.',
 'Joint history-law times real-volume measure.withDensity uncurry D, unnormalized finite submeasure.'
]
matches=list(re.finditer(r'^\s+let ([^\s:]+)',model_text,re.M));defs=[]
for i,(name,meaning) in enumerate(zip(names,semantics)):
 start=matches[i].start();end=matches[i+1].start() if i+1<len(matches) else model_text.index('        Measurable (Function.uncurry D)',start)
 snippet=model_text[start:end]
 # Density is followed by the main quantifiers before the next nested let: retain the exact scope as part of its literal evidence.
 defs.append(dict(name=name,classification='literal-source-definition' if i<11 else 'source-implicit-observable-or-measure-packaging',literal_lean=snippet,literal_utf8_sha256=sha(snippet.encode()),meaning=meaning,accepted=True))

region_math=[
 'Expand the complete public private Prop without a provider. ActualHazardClock supplies Borel hitting/hazard; actual harmonic flow/rate continuity gives Borel finite density, including all live states. Sum-product equivalence handles tagged records. UnitExponentialProduct proves P probability. The total wait projection is Borel. Density is finite pointwise; this is not density<=1. Six analytic binders are unchanged.',
 'Use actual87 to derive measurable H,Y and (H,Y)_*P=mu prod P, with Y_k=w_(n+k). Define B as pullback of product event Q, X via G. The last-record and tail0 projections identify actual raw coordinate n. Joint strict guard plus Borel density gives measurable uncurry D. Kernel.withDensity_apply hD proves every fiber identity, excluding the nonmeasurable fallback. This region sets up kernel; it does not yet prove its mass bound.',
 'Prove each fixed-history strict fiber law. Stopped fiber and D are zero. In live case actual86 gives the real finite-event Ioc law. Restrict its event/image measures by Iio(dh), prove positive finite extended-wait guard equals the restricted real-extraction event, and rewrite Ioc intersect Iio as Ioo. withDensity_indicator gives exactly D. No no-atom, open/closed total mass equality, or exact strict-mass formula is used.',
 'Rewrite each K(h) as the restricted wait pushforward proved above. Its univ mass is at most P(univ)=1, for every abstract history. Supply uniform bound1 to IsFiniteKernel. This does not assert D<=1 or weighted integrals finite.',
 'For arbitrary Borel joint set C, L=G^-1(C) intersect Q is Borel. Pull actual restricted X law to (H,Y), replace by actual87 product law, use product sections and each-h strict fiber identity, then Tonelli/withDensity. Extensional equality gives map X(P restricted B)=nu, hence nu mass<=1 internally. Conditioning remains unnormalized.',
 'For every joint Borel ENNReal F, prove parameter-integral measurability by joint measurability of F*D and nonnegative product integration. For every Borel A, indicator on first-coordinate A identifies both restricted integrals; map law, withDensity and Tonelli give exact nested identity. F may be unbounded/infinite, A null, d variable and unbounded across histories. No integrability/positive-probability premise appears.'
]
regions=[];previous=114
for step,math in zip(lesson['steps'],region_math):
 a=step['lean_source_region'];assert a['start_line']==previous+1;previous=a['end_line']
 b=b''.join(lines[a['start_line']-1:a['end_line']]);assert sha(b)==a['exact_code_raw_sha256'];assert b.decode()==step['lean'];assert a['source_raw_sha256']==raw(module)
 regions.append(dict(**a,title=step['title'],text=step['text'],formula=step['formula'],text_utf8_sha256=sha(step['text'].encode()),formula_utf8_sha256=sha(step['formula'].encode()),exact_code_matches=True,mathematics=math,exposition='Independently read current text/formula/Lean; faithful to the displayed mathematical region and bounded source graph, with derivation sequencing aligned.',source_boundary='Only density component S87-I5/G86-11',verdict='accepted'))
assert previous==436 and len(regions)==6
assert not re.search(r'\b(sorry|admit|axiom)\b|Prop\s*:=\s*True|:=\s*trivial',text)

original_lesson=r89/'independent-math89/lesson89.original.exactraw.json';old=read(original_lesson)['units'][0]
diff=[]
def differences(a,b,p=''):
 if type(a)!=type(b):diff.append(p);return
 if isinstance(a,dict):
  for k in sorted(set(a)|set(b)):
   if k not in a or k not in b:diff.append(p+'/'+k)
   else:differences(a[k],b[k],p+'/'+k)
 elif isinstance(a,list):
  if len(a)!=len(b):diff.append(p)
  else:
   for i,(x,y) in enumerate(zip(a,b)):differences(x,y,p+'/'+str(i))
 elif a!=b:diff.append(p)
differences(old,lesson);assert diff==['/steps/1/text'],diff

mathdir=r89/'independent-math89';focused=mathdir/'fresh-focused-build.receipt.json';kernelrec=mathdir/'fresh-whole-source-kernel.receipt.json';kr=read(kernelrec);fr=read(focused)
for rec in [kr,fr]:
 assert rec['exit_code']==0 and rec['terminal_closed'] and rec['source']['raw_sha256']==raw(module)
 for k in ['source','probe','stdout','stderr']:
  if rec.get(k):
   e=rec[k];p=root/e['path'];assert raw(p)==e['raw_sha256'] and p.stat().st_size==e['bytes']
kernel_log=root/kr['stdout']['path'];log=kernel_log.read_text(encoding='utf-8');probe=root/kr['probe']['path'];probe_text=probe.read_text(encoding='utf-8')
assert text.strip() in probe_text
axiom=re.search(r'depends on axioms:\s*\[([^\]]+)\]',log,re.S).group(1)
assert {x.strip() for x in axiom.split(',')}=={'propext','Classical.choice','Quot.sound'}
external=[x.split(' ',1)[1] for x in log.splitlines() if x.startswith('EXTERNAL_ASTIS_DEPENDENCY ')]
public=[x for x in external if not x.startswith('_private.')]
assert len(public)==6
assert any(x.endswith('ActualFiniteHistoryTailLaw.actual_finite_history_tail_law') for x in public)
assert any(x.endswith('ActualFiniteFirstEventLaw.actual_finite_first_event_law') for x in public)
assert any(x.endswith('UnitExponentialProduct.unit_exponential_product_laws') for x in public)
assert not any('ActualConditionalNextWaitSurvival' in x for x in external)
assert 'LOCAL_PROOF_CONSTANT_COUNT 18' in log and 'TRANSITIVE_ASTIS_CONSTANT_COUNT 77' in log
assert 'LOCAL_NO_VALUE' not in log and 'PROJECT_NO_VALUE' not in log and 'sorryAx' not in log

snapshots=[copy(packet_path,'source-review89.packet.exactraw.json'),copy(module,'module89.exactraw.lean'),copy(lesson_path,'lesson89.exactraw.json'),copy(pub_path,'publication89.exactraw.json'),copy(decpath,'decoder89.reconstruction.exactraw.json'),copy(decrun,'decoder89.run.exactraw.json'),copy(decmanifest,'decoder89.manifest.exactraw.json'),copy(neutral,'decoder89.input.exactraw.json')]
uncertainties=write('decoder89.uncertainties.native.json',dict(source=pin(decpath),semantic_uncertainties_verbatim=dec['semantic_uncertainties'],native_output_modified=False,assessment=[
 'The exact hittingAfter semantics agree with frozen source infimum/empty-infinity convention. No attainment, infinite process or global consequence is imported from the decoder.',
 'Compilation is not decoder evidence. Separate exact-module focused and complete-source native receipts both have terminal exit0; independently read proof code and source anchors establish this review boundary.',
 'RAW and canonical JSON hashes have distinct declared meanings. Independently recomputed both neutral input RAW and canonical excluding packet_sha256, and bound reconstructed text/run RAW. This resolves the serialization uncertainty without modifying native reconstruction.'
],blocking=False))
kernel_audit=write('source-review89.kernel-evidence.native.json',dict(kind='independent reading of underlying exact-source native kernel evidence',focused_receipt=pin(focused),kernel_receipt=pin(kernelrec),probe=pin(probe),native_log=pin(kernel_log),source_text_occurs_exactly_in_probe=True,standard_axioms=sorted(x.strip() for x in axiom.split(',')),owned_constant_count=18,transitive_ASTIS_count=77,immediate_public_producers=public,immediate_private_generated_count=len(external)-len(public),all_owned_generated_constants_traversed=True,provider_binders=False,survival88_false_dependency=False,producer_consumption='Immediate kernel constants agree with independently read BODY calls: actual87 product-history law, actual86 finite-event density, actual75 hazard, harmonic flow/rate and unit-exponential77. No import-only claim is substituted for usage.',scope='Evidence supports exact current declaration; independent source fidelity is decided separately from compiler/kernel status. No other reviewer decision is adopted. Kernel-dependency89 metadata status was visible during data inspection and is not used as a source verdict.'))

slot_original={
 'objects':'Printed source actual harmonic flow, reflection, intensity and iid integrated-hazard hitting recursion; frozen ASTIS completion forms full finite stopped history, actual unused raw threshold, strict finite relative waiting-time density and history-time submeasure.',
 'domains':'Source Euclidean phase space realized explicitly as arbitrary finite-dimensional real inner-product Borel space, including rank0. Full tagged record histories, real product thresholds, NNReal finite durations, WithTop NNReal waits, real Lebesgue relative time, ENNReal nonnegative tests.',
 'quantifiers':'All fixed deterministic y,r,z0,n; all fixed Borel d:Hist->NNReal, joint Borel nonnegative extended F, and Borel A. Conclusions include every abstract history, not merely realized/almost-everywhere histories.',
 'assumptions':'Six standing analytic hypotheses only: positive alpha, alpha<=beta, global C2 V, two Hessian inequalities all x,v, eta>0, beta eta<=1. Borel d,F,A specify admissible tests; independence/measurability/density/kernel laws are derived.',
 'conclusion':'Borel finite density and wait observables, measurable strict guarded density, genuine every-history finite subprobability kernel, actual restricted joint pushforward equality and arbitrary joint-test/history-event unnormalized integral identity.',
 'scopes':'Only the finite-density component of S87-I5/G86-11 at deterministic depth. Stopped/zero/infinite waits excluded from this finite guard; absent mass not normalized away. Strict source A7 endpoint is realized by restriction. Ordered iteration/final factor and global results remain open.',
 'constant_dependencies':'Exp rate1, reflection coefficient2, same sqrt eta harmonic scaling, beta eta<=1 and total-mass bound1. No new clock/measure scaling, positive event-mass bound, dimension bound or density<=1 assumption.'
}
evidence={
 'objects':'Primary A1.SS1.p1/p2,A1.E1/E2 and independent preimplementation inventory; exact private Prop and all23 literal lets. Actual history[last]=record n and Y0=w_n.',
 'domains':'Current literal instances/typing, source-first rank0 and real-volume elaboration, all-history strict fiber BODY region3. Negative-time density extension is explicitly killed by guard.',
 'quantifiers':'Exact expanded private Prop equals packet statement; public theorem/change retains all quantifiers. n fixed externally, d deterministic function though d(H) random; F jointly Borel and may be infinity.',
 'assumptions':'Source standing S1 and etaS2 spans; exact6 binders; actual producer calls, no theorem-valued/provider assumptions. Product law and measurability proved internally.',
 'conclusion':'Whole BODY six contiguous regions prove each stated conjunction/test identity; source graph paths D1,A1,A2,I3,P1,P2 to target. Product law avoids substitution into exceptional conditional representatives.',
 'scopes':'Native decoder scopes/branches and public source attribution agree with frozen boundary; all six code/text/formula regions. Distinct77 topology review is separate from graph creator, and not copied here.',
 'constant_dependencies':'Literal Phi,S,rate,P,density, measure reference and hmass/hfinite evidence. Kernel total-mass bound1 does not constrain pointwise rho.'
}
slots={k:dict(original=slot_original[k],reconstructed=dec[k],evidence=evidence[k],relation='explicit-elaboration' if k in ['objects','domains','assumptions','conclusion','scopes'] else 'equivalent') for k in slot_original}
deltas=[
 dict(id='D89-1',classification='source-implicit',blocking=False,source='A1.E1/E2 and strict next jump factor implicit in A1.E7',lean='Explicit complete-history conditional finite density/kernel and arbitrary joint-test identity',reason='Faithful necessary measurable iid disintegration completion; not a printed standalone theorem. Attribution and bounded claim are explicit.'),
 dict(id='D89-2',classification='domain-clarification',blocking=False,source='Euclidean source phase space',lean='Any finite-dimensional real inner-product Borel realization including rank0',reason='Coordinate-free formulas/proof retain source geometry; zero rank is benign and disclosed.'),
 dict(id='D89-3',classification='notation-resolution',blocking=False,source='Positive iid Exp1 thresholds and possible infinite wait/stopping',lean='Raw real product plus toNNReal null extension, tagged stopped records, total untopD0 time observable',reason='Source-support dynamics retained; restricted strict finite event kills stopped/zero/top and out-of-support auxiliary defaults.'),
 dict(id='D89-4',classification='source-implicit',blocking=False,source='Strict ordered simplex0<t1<...<tn<T',lean='Ioc deterministic density restricted by Iio cutoff to Ioo',reason='Both sides genuinely restricted; no asserted equality of endpoint masses and no additional no-atom premise.'),
 dict(id='D89-5',classification='quantifier-clarification',blocking=False,source='History-dependent finite next-event horizon and path tests',lean='All fixed Borel d on full history and jointly Borel ENNReal F; all Borel A',reason='Admissible test domains, not new analytic regularity assumptions. d(H) random but no random unconditioned d, future-tail inspection or random-depth claim.'),
 dict(id='D89-6',classification='source-implicit',blocking=False,source='Nonnegative finite-jump factor can lose mass to infinity/no event',lean='Every-history kernel and joint submeasure mass<=1 unnormalized',reason='Derived from restricted probability, not provider or pointwise density bound; does not assert exact strict mass/survival consistency.'),
 dict(id='D89-7',classification='unresolved',blocking=False,source='Full A7 and global G86-11',lean='Only conditional finite density component',reason='Intentional explicit bounded target. Iteration/final factor/full source result remain open and are not represented as proved.'),
 dict(id='D89-8',classification='notation-resolution',blocking=False,source='Native decoder RAW/canonical hash uncertainty',lean='RAW pin and canonical excluding self field both independently verified',reason='Native uncertainty retained verbatim; no mathematical or textual repair required.')
]
binders=[dict(name=n,source_anchor=a,meaning=m,classification='standing-source-hypothesis',extra_provider=False) for n,a,m in [
 ('hα','S1.E1','0<alpha'),('hαβ','S1.E1','alpha<=beta'),('hV','S1.p1','ContDiff R2 V globally'),('hH','S1.E1','Both Hessian quadratic-form bounds for every x,v'),('hη','S2.SS2.p1','0<eta'),('hβη','S2.SS2.p1','beta eta<=1')]]
boundary=dict(target='density component of S87-I5 / G86-11 only',source_graph=pin(sf/'source-proof-graph89.native.json'),source_coverage=pin(sf/'source-coverage89.native.json'),creator_self_independent_topology_approval=False,open=['remaining S87-I5 assembly','ordered-time density iteration','finite count partition/path-functional identification','final survival factor assembly','full A.7','whole G86-11','finite-mass/survival consistency and exact strict mass formula','physical-time residual memorylessness/random restart/Markovness','global nonexplosion/process path construction','invariance/hypocoercivity','implementation/errors/unbounded expected costs/main','actual-input composition/whole paper/Goal'])

inputs=[packet_path,module,lesson_path,pub_path,primary,preread,out/'final-primary-first89.freeze.native.json',out/'final-primary-source-math-inventory89.native.json',out/'chronology.final-source89.native.jsonl',sf/'source-first89.native.json',sf/'source-proof-graph89.native.json',sf/'source-coverage89.native.json',sf/'closed-raw-manifest.source-first89.native.json',pre/'header-source89/header89.source-decision.native.json',neutral,decpath,decrun,decmanifest,focused,kernelrec,probe,kernel_log,root/fr['stdout']['path'],root/fr['stderr']['path'],root/kr['stderr']['path'],original_lesson,r89/'publication-freeze89.after-exposition.json',root/'lean-toolchain',root/'lake-manifest.json',root/'tools/astis_publication.py',root/'.lake/packages/mathlib/Mathlib/Probability/Kernel/WithDensity.lean']
# Pin observed kernel data without adopting its status or other review conclusions.
inputs.append(mathdir/'kernel-dependency89.json')
producer_modules=[root/'AutoSamplingTheory/ExampleCases/ProximalBPS'/x for x in ['ActualFiniteHistoryTailLaw.lean','ActualFiniteFirstEventLaw.lean','ActualHazardClock.lean','ActualHarmonicFlow.lean','ActualBounceRate.lean']]+[root/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean']
inputs+=producer_modules
chron=out/'chronology.source-review89.native.jsonl'
events=[
 dict(event='PRIMARY_FIRST_SEQUENCE_INHERITED_IMMUTABLE',preread_manifest=pin(preread),primary_math_inventory=pin(out/'final-primary-source-math-inventory89.native.json'),direct_primary_read_before_current_BODY_decoder_packet=True,prospective_headerV2_known=True,prospective_header_is_not_BODY_acceptance=True),
 dict(event='FRESH_PACKET_AND_ALL_NEW_CODE_PROSE_INDEPENDENTLY_READ',packet=pin(packet_path),module=pin(module),lesson=pin(lesson_path),publication=pin(pub_path),all23defs=True,six_contiguous_BODY_regions=True,prior_current89_source_fidelity_or_math_decision_read=False),
 dict(event='NATIVE_BLIND_DECODER_READ_AND_UNCERTAINTIES_PRESERVED',decoder=pin(decpath),uncertainties=pin(uncertainties),note='Initial filename lookup used nonexistent reconstructed-theorem.json/decoder.run.json; corrected to actual native filenames, with no altered native input.'),
 dict(event='EXACT_BINDINGS_AND_UNDERLYING_KERNEL_READ',packet_canonical=packet_canonical,publication_binding=canon(payload),kernel_evidence=pin(kernel_audit),other_review_decision_not_adopted=True,prior88_output_read_as_requested_format_only=True),
 dict(event='SOURCE_COMPARISON_COMPLETED',verdict='equivalent-after-elaboration',repairs=[],accepted_target=boundary['target'],canonical_writes=False,VERIFIED=False)
]
assert not chron.exists();chron.write_text(''.join(json.dumps(dict(sequence=i+1,recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),**e),ensure_ascii=False)+'\n' for i,e in enumerate(events)),encoding='utf-8',newline='\n')
run=write('source-review89.run.native.json',dict(schema_version=1,kind='independent anti-anchored primary-first source89 review run',reviewer='/root/fresh_source87',formalizer=packet['roles']['formalizer'],decoder=packet['roles']['blind_decoder'],independent_from_formalizer=True,independent_from_decoder=True,chronology=pin(chron),inputs=[pin(p) for p in inputs],anti_anchoring=dict(primary_first_final_reconstruction_closed_before_current_packet_BODY_decoder=True,preimplementation_graph_reused_unchanged=True,prospective_header_familiarity_disclosed=True,no_prior89_source_verdict_or_math_decision_imported=True,underlying_kernel_data_metadata_status_observed_not_adopted=True,prior88_native_decision_used_as_format_only=True),checks=dict(packet_raw_and_canonical=True,source_statement_hash=True,privateProp_complete_expansion=True,all23defs=True,six_analytics=True,wholeBODY_all6exact_regions=True,all_current_exposition_read=True,publication_binding_recomputed=True,native_decoder_manifest_rehashed=True,native_uncertainties_preserved=True,underlying_kernel_receipts_terminal0=True),canonical_mutations=False,source_only=True,new_proof_or_VERIFIED=False))
decision=write('source-review89.decision.native.json',dict(schema_version=1,semantic_slots=slots,deltas=deltas,verdict='equivalent-after-elaboration',repairs=[],reviewer='/root/fresh_source87',independent_from_formalizer=True,independent_from_decoder=True,review_evidence='Immutable primary-first source reconstruction plus exact current privateProp/BODY/prose, fresh source-blind reconstruction and underlying exact-source kernel data. Native original files and all uncertainties retained. Only bounded density component accepted.',review_run_sha256=raw(run),reviewer_packet_sha256=packet_canonical,reviewer_packet_raw_sha256=raw(packet_path),publication_binding_sha256=canon(payload),module=pin(module),lesson=pin(lesson_path),publication=pin(pub_path),primary_version_license=dict(version='arXiv2609.06905v1',date='07 Sep 2026',license='arXiv.org perpetual non-exclusive license',primary=pin(primary),anchors=inventory['anchors'],long_source_extracts='Only inherited *.private.json; no new public verbatim primary extracts.'),literal_definition_audit=defs,analytic_binder_audit=binders,admissible_tests=dict(d='Fixed Borel Hist->NNReal, finite pointwise and unbounded across histories permitted; d(H) random by composition. No tail/external random argument.',F='Joint Borel Hist x R->ENNReal, nonnegative possibly infinite; no bound/integrability premise.',A='Any Borel history event, null events allowed.',classification='Admissible measurable test class, not added source analytic/regularity/provider hypotheses.'),privateProp_audit=dict(literal_complete_expansion_matches_packet=True,public_theorem_targets_complete_privateProp=True,all14outer_and9nested_definitions_expanded=True,public_BODY_change_same_fullProp=True,hidden_provider=False),body_audit=regions,whole_body_audit=dict(start_line=115,end_line=436,regions=6,exhaustive_contiguous=True,mathematics_and_exposition='All six exact code regions plus statement/assumptions/formula proofs independently read and compared to immutable source graph.',step2_successor_overlay=dict(original=pin(original_lesson),current=pin(lesson_path),independently_verified_changed_paths=diff,source_verdict_not_inherited=True)),boundary_cases=dec['scopes']['branches'],conditioning_audit='Unnormalized restriction over B intersect H^-1 A equals history-law iterated integral; equivalent to frozen P-space formulation by pushforward. Null A valid without division. No pointwise conditioned representative, provider law or arbitrary random-history independence.',endpoint_audit='Both measures restricted from actual86 Ioc(0,d) by Iio(d). Strict positive finite wait and Ioo support coincide after finite extraction; live infinity/stopped zero fail guard. No open/closed total-mass equivalence, no no-atom premise and no exact strict mass formula.',kernel_evidence=pin(kernel_audit),decoder_uncertainties=pin(uncertainties),accepted_truth_boundary=boundary,blocking_deltas=[],body_source_fidelity_acceptance=True,topology_creator_self_independent_acceptance=False,theorem_verified_transition=False,whole_paper_acceptance=False,browser_or_layout_acceptance=False,reader_content='Current canonical lesson text/formula and exact6 initially foldable Lean-region metadata checked. No rendered DOM/browser/SVG/layout/deployment validation is claimed.'))
terminal=write('terminal-completion.source-review89.native.json',dict(schema_version=1,kind='native source-review89 terminal completion',terminal_closed=True,status='source-review-closed',verdict='equivalent-after-elaboration',decision=pin(decision),run=pin(run),chronology=pin(chron),accepted_target=boundary['target'],blocking_deltas=0,canonical_mutations=False,VERIFIED=False))
outputs=[Path(__file__).resolve(),*snapshots,uncertainties,kernel_audit,chron,run,decision,terminal]
manifest=write('closed-raw-manifest.source-review89.native.json',dict(schema_version=1,kind='closed exact RAW independent-source89 BODY/source review manifest',closed=True,input_set_closed=True,output_set_closed=True,inputs=[pin(p) for p in inputs],outputs=[pin(p) for p in outputs],inherited_preread_manifest=pin(preread),root_policy='Manifest excludes itself to avoid circular RAW hashing; root RAW identity reported externally.',private_extract_policy='Long primary text exists only in inherited *.private.json and is excluded from reader publication.',canonical_mutations=False,theorem_VERIFIED=False))
for section in ['inputs','outputs']:
 for e in read(manifest)[section]:
  p=Path(e['path']);assert raw(p)==e['raw_sha256'] and p.stat().st_size==e['bytes']
print(json.dumps(dict(status='CLOSED',decision=pin(decision),run=pin(run),manifest=pin(manifest),terminal=pin(terminal),chronology=pin(chron),inputs=len(inputs),outputs=len(outputs),verdict='equivalent-after-elaboration',accepted_target=boundary['target']),ensure_ascii=False,indent=2))
