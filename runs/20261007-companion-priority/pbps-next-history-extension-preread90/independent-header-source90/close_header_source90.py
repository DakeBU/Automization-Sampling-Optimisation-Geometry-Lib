from pathlib import Path
import json,hashlib,re,datetime,shutil

root=Path('E:/Samplinglib');out=Path(__file__).resolve().parent;pre=out.parent;sf=pre/'independent-source-first90'
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p):return dict(path=str(p.resolve()),raw_sha256=raw(p),bytes=p.stat().st_size,hash_mode='exact-raw-file-bytes')
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def write(n,v):
 p=out/n;assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');return p
def snap(p,n):
 q=out/n;assert not q.exists();shutil.copyfile(p,q);assert raw(p)==raw(q);return q
primary=root/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
assert raw(primary)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
private=out/'primary90.header-preread.private.json';spans=load(private)['spans'];anchors=[]
for s in spans:
 assert hashlib.sha256(primary.read_bytes()[s['byte_start_zero_based']:s['byte_end_exclusive']]).hexdigest()==s['raw_span_sha256']
 anchors.append({k:v for k,v in s.items() if k not in ['raw_html','readable_text']})
header=pre/'header90.proposed.lean';packet_path=pre/'header-review90.packet.json';graph_path=pre/'source-proof-graph90.accepted-successor.json';adoption_path=pre/'root.source90.adoption.json';frozen_manifest=sf/'closed-raw-manifest.source-first90.native.json'
assert raw(header)=='1262c82138eb3a7cc502fe4eb6182c10e4e33168a734333ffaec580585935750' and header.stat().st_size==6439
assert raw(packet_path)=='df4185f503cd972d873af7c542247061b4fdd4814f82192bc68da4aaf2fd19d7'
assert raw(graph_path)=='b39b8b3c26758d0787ded303c14c3c927c95033d3ff75bdc1a534431bf1fa8b7'
assert raw(adoption_path)=='578af72921c3a18e582816581d91f5edc436b390cdfe4205aa273d9f6b251f09'
assert raw(frozen_manifest)=='82eed8395f4ddcbeb984847a31e277c8980c171fd6a42c69a0ee9608ef6b845c'
for section in ['inputs','outputs']:
 for e in load(frozen_manifest)[section]:
  p=Path(e['path']);assert raw(p)==e['raw_sha256'] and p.stat().st_size==e['bytes']
packet=load(packet_path)
for k in ['header','accepted_source_graph','source_adoption','unchanged_coverage','copied_literal_definitions_from']:
 e=packet[k];p=Path(e['path']);assert raw(p)==e['raw_sha256'] and p.stat().st_size==e['bytes']
# Read adoption's exact RAW descriptors as provenance, not its independent-review verdict.
adopt=load(adoption_path);descriptor_count=0
for e in adopt['checked_RAW_descriptors']:
 p=Path(e['path']);assert raw(p)==e['raw_sha256'] and p.stat().st_size==e['bytes'];descriptor_count+=1
assert descriptor_count==82
oldgraph=load(sf/'source-proof-graph90.native.json');newgraph=load(graph_path);diff=[]
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
differences(oldgraph,newgraph);assert diff==['/edges/1/justification','/nodes/1/claim'],diff
freeze=load(sf/'source-first90.native.json');coverage=load(sf/'source-coverage90.native.json')
h=header.read_text(encoding='utf-8');names=re.findall(r'^\s+let ([^\s:]+)',h,re.M)
assert names==['c','Φ','S','rate','Λ','τ','next','record','P','ε','history','waitObs','timeObs','density','Rec','Hist','HistNext','last','H','Hnext','append','lift','μ','D','B','X','Y','ν']
assert not re.search(r'\b(sorry|admit|axiom)\b|Prop\s*:=\s*True|:=\s*trivial|:= by',h)
assert packet['SAU_claimed'] is False and packet['statement_sealed'] is False and packet['Lean_BODY_started'] is False
semantics=[
 'Source center y-eta gradient V(reference).','Actual harmonic flow, same sqrt eta/time scaling for every real t.','Actual gradient-difference reflection with coefficient2, total division implements R0=I.','sqrt eta positive-part velocity/gradient-difference inner product.','Actual real interval integral of rate along flow on nonnegative finite time.','Original closed-target integrated-hazard infimum, empty set gives top.','Actual finite update, live top leads stopped, stopped absorbing; finite extraction only in non-top branch.','Actual Nat recursion initially live(0,z0), kth update uses e_k.','Literal real-sequence countable product of rate-one exponential law.','Coordinatewise toNNReal ambient extension, raw exponential inputs retained separately.','Complete actual records0..n, no last-state-only surrogate.','Live actual wait using clipped real threshold, stopped0.','Total real finite extraction, top/stopped0 outside the strict event is auxiliary.','Live real-time rate*exp(-hazard(toNNReal time)), stopped0; nonpositive-time extension eliminated by D.',
 'Tagged live finite accumulated time/phase or stopped record carrier.','Full finite product with n+1 old entries, all abstract histories.','Full finite product with n+2 entries, the complete next history.','Old last index n in Fin(n+1).','Actual H_n(w) from literal recursion and same fixed parameters.','Actual H_(n+1)(w) with Fin(n+2), not a freely supplied map.','Fin.snoc preserves entire old prefix; new live(T+toNNReal(s),S(Phi_s z)) or stopped. Raw negative-time flow plus clipped cumulative increment is a disclosed auxiliary convention.','Pair of the complete appended history and same prospective real relative wait.','Actual history pushforward mu=map H P.','Strict positive finite cutoff density, no endpoint change.','Actual 0<W_n<finite d(H), excludes stopped/zero/infinite waits.','Actual old-history/finite-extracted-wait pair with raw coordinate n.','Actual NEW complete-history/same next-relative-wait pair.','Unnormalized strict joint history/real-time density measure from89.'
]
positions=list(re.finditer(r'^\s+let ([^\s:]+)',h,re.M));defs=[]
for i,(name,meaning) in enumerate(zip(names,semantics)):
 start=positions[i].start();end=positions[i+1].start() if i+1<len(positions) else h.index('        MeasurableSet B',start)
 excerpt=h[start:end]
 defs.append(dict(name=name,literal_lean=excerpt,literal_utf8_sha256=hashlib.sha256(excerpt.encode()).hexdigest(),meaning=meaning,source_relation='literal model' if i<14 else 'explicit ASTIS measurable finite-history transport packaging',accepted_source_boundary=True))
slots={
 'objects':dict(original='Source actual clock/flow/bounce recursion appends each finite next post-bounce event to the complete finite history. Frozen completion transports89 strict joint density through the derived full append.',reconstructed='Exact28 lets preserve14 inherited actual model/observables,8 record/history/append/lift objects and6 cutoff/measure/actual-pair objects. Fin.snoc retains all n+1 old records and adds the actual finite update.',relation='explicit-elaboration',evidence='Primary A1.E1/E2 and independent source-first90; literal header definitions and prefix/guarded recursion conclusions.'),
 'domains':dict(original='Finite-dimensional real inner-product Borel source realization incl rank0; Hist_n tagged records^(n+1), Hist_(n+1) tagged records^(n+2), fixed finite n; real prospective time and finite nonnegative history-dependent cutoff.',reconstructed='Header has exactly these carriers, complete actual H/Hnext and same raw real product clocks. Append/lift are total on all Hist x real, including unrealizable histories and negative prospective arguments.',relation='explicit-elaboration',evidence='Literal Rec/Hist/HistNext, Fin.snoc, real-volume density and Borel sum/product structures. Extra total-domain cases are auxiliary, not author positive-event dynamics.'),
 'quantifiers':dict(original='All deterministic y,r,z0,n; every fixed Borel finite-valued d on complete old history; all joint Borel nonnegative extended F on new history x real; all Borel old-history A including null events.',reconstructed='Header quantifies forall y,xRef,z0,n, derives Hnext/append/lift measurability and every-prefix identity before d, then forall d Measurable d, forall F Measurable F, forall A MeasurableSet A.',relation='equivalent',evidence='All d/F/A are fixed maps/sets with no external random/tail argument. d(H) can be random and unbounded across histories; no random event-depth substitution.'),
 'assumptions':dict(original='Exactly six standing analytic source hypotheses, with carrier data. Measurable d/F and Borel A delimit admissible tests. Constructor measurability/actual identity/density/independence are proof obligations, never supplied premises.',reconstructed='Six binders hα,hαβ,hV,hH,hη,hβη unchanged. Every Hnext/append/lift measurability and actual equality is a conclusion. No additional provider, finite-wait, positive probability, normalization or independence premise.',relation='equivalent',evidence='Direct primary standing/eta spans and complete private Prop binder audit; no source hypothesis is replaced by a producer assumption.'),
 'conclusion':dict(original='Derived Borel prefix-preserving append, guarded pointwise equality to actual H_(n+1), actual restricted new-history/wait joint law and marginal pushforward of89 density, subprobability mass and arbitrary nonnegative joint-test/old-event identity.',reconstructed='All are explicit header conjunctions: Hnext/append/lift Borel, prefix equality forall p,j, actual Hnext=append(X) forall w in B, map Y(P|B)=map lift nu and map Hnext(P|B)=map append nu, lifted mass<=1, measurable iterated test integral and final unnormalized identity.',relation='explicit-elaboration',evidence='Matches source-first90 target formula. Joint lifted mass bound implies finite marginal mass under projection; omission of a redundant separate marginal bound is not a weakening of the substantive boundary.'),
 'scopes':dict(original='Only actual complete next-history law restricted to strict positive finite cutoff event. Stopped/infinite/outside-cutoff mass remains absent and unnormalized; next ordered-time/path assembly/fullA7 remain open.',reconstructed='Header says only strict finite event transported, derives actual equality on B only, and includes no unrestricted next-history probability, conditional representative, full trajectory/restart/Markov/global/Goal assertion.',relation='equivalent',evidence='Source A1 stop convention and A1.E7 strict simplex; packet explicit exclusions and header module comment, all exact conclusions.'),
 'constant_dependencies':dict(original='Same Exp1 clocks, reflection coefficient2, sqrt eta harmonic flow, beta eta<=1, strict guard and mass bound1. No new density/reference scaling.',reconstructed='Literal models retain these constants. Real Lebesgue is unchanged89 reference; append uses actual cumulative time addition and same bounce map. No pointwise density<=1 or new-history Lebesgue density is claimed.',relation='equivalent',evidence='Literal P/Phi/S/rate/D/nu and mass-bound conjunction; no Jacobian, new reference density or endpoint-mass equivalence appears.')
}
binders=[]
for x in freeze['source_hypotheses']:binders.append(dict(**x,header_present=True,extra_provider=False))
assert [x['id'] for x in binders]==packet['six_analytic_source_binders']
deltas=[
 dict(id='H90-1',slot='objects',classification='source-implicit',blocking=False,description='Explicit Borel full append and actual Hnext transport elaborate the finite recursion/A7 iteration ingredient rather than a printed standalone theorem.',evidence='Source-first90 frozen construction and primary A1.E2/A.2.'),
 dict(id='H90-2',slot='domains',classification='domain-clarification',blocking=False,description='Append is total for real negative arguments using raw negative Phi and clipped cumulative increment; stopped appends stopped. This agrees on strict positive finite support, which alone contributes to nu.',evidence='Exact append/D/B lets and packet auxiliary-totalizations disclosure; source-first90 expressly permits any Borel out-of-support totalization.'),
 dict(id='H90-3',slot='conclusion',classification='source-implicit',blocking=False,description='Every-prefix equality and pointwise actual Hnext=append(X) are conclusions. This meets the substantive actual-recursion bridge rather than assuming it.',evidence='Literal universal prefix equality and guarded actual equality before the map laws.'),
 dict(id='H90-4',slot='quantifiers',classification='quantifier-clarification',blocking=False,description='Fixed Borel d can depend on the entire old history, F is jointly Borel on new history/time and may be infinite; A may be null. These are admissible tests, not analytic/provider hypotheses.',evidence='Exact forall scopes and final restricted lintegral, no normalization denominator.'),
 dict(id='H90-5',slot='scopes',classification='unresolved',blocking=False,description='Only the actual strict finite component is transported. Unrestricted next-history mass, ordered-time density iteration, final factor, fullA7 and global conclusions remain open.',evidence='Frozen boundary and exact header/packet exclusions.')
]
cases=dict(
 negative_time='append live uses T+toNNReal(s) and S(Phi_s z); auxiliary when s<0, D=0. Does not contradict source positive finite update.',
 stopped='Absorbing appended stopped with old prefix retained; waitObs stopped0 fails B and D stopped0. No stopped-probability atom is recovered by this finite component.',
 live_infinity='waitObs retains top; t_n defaults0 offguard; finite d makes B false. No flow/bounce at infinity.',
 zero_wait_or_cap='Strict positivity excludes zero waits; d0 gives zero D and empty B. No no-atom premise or endpoint equality is imported.',
 n0='One old initial record, two next entries; fresh raw w0 supplies first update.',
 rank0='Allowed; zero-hazard positive clocks yield no strict finite event and zero transported submeasure.',
 unrealizable_history='All abstract histories receive Borel append/lift and parameter integrals; actual pointwise recursion equality is claimed only on realized H_n and B.',
 null_history_A='Final identity is unnormalized; no division by mu(A), positive mass or conditional-density representative.',
 strict_endpoint='0<W<d(H) and0<s<d(h) remain strict. This transport adds no < versus <= equivalence or exact strict mass formula.',
 whole_history='All old coordinates retained by forall p,j prefix equality; actual Hnext is literal history at n+1, not just final state.',
 random_duration='d is fixed Borel map, d(H_n) random by composition. n fixed deterministic; no raw/future clock argument in d/F.',
 measure_reference='Only old-history product real-volume has explicit density. New-history law is a measurable image; no unsupported Lebesgue density on its carrier.')
graph_audit=write('header90.graph-binding.native.json',dict(schema_version=1,original=pin(sf/'source-proof-graph90.native.json'),accepted_successor=pin(graph_path),root_adoption=pin(adoption_path),exact_changed_paths=diff,adoption_RAW_descriptors_reverified=descriptor_count,primary_compatibility='The expanded A1 measurability claim and edge justification mention hazard/threshold/finite recursion Borelness printed in the same direct A.2 paragraph. This header source audit does not independently approve the topology of its own graph.',creator_self_independent_topology_approval=False,prior_distinct_review_provenance_pinned_not_reissued=True,coverage_reused_unchanged=pin(sf/'source-coverage90.native.json'),no_survival88_AND=True,no_direct87_86_extra_AND_when89_consumed=True,no_noatom_AND=True))
snapshots=[snap(header,'header90.exactraw.lean'),snap(packet_path,'header-review90.packet.exactraw.json')]
chron=out/'chronology.header-source90.native.jsonl';first=json.loads(chron.read_text(encoding='utf-8').splitlines()[0]);assert first['header90_read'] is False and first['packet90_read'] is False
with chron.open('a',encoding='utf-8',newline='\n') as f:
 for e in [dict(event='EXACT90_PROSPECTIVE_HEADER_PACKET_READ_AFTER_PRIMARY',header=pin(header),packet=pin(packet_path),no_BODY_read=True),dict(event='IMMUTABLE_FREEZE_AND_ACCEPTED_GRAPH_BINDING_REVERIFIED',source_first_manifest=pin(frozen_manifest),graph_binding=pin(graph_audit),creator_topology_self_approval=False),dict(event='HEADER_SOURCE_COMPARISON_CLOSED',verdict='equivalent-after-elaboration',repairs=[],all28_literal_definitions=True,six_source_analytics=True,no_Seal_claim_BODY_or_proof_credit=True)]:
  f.write(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),**e),ensure_ascii=False)+'\n')
inputs=[primary,header,packet_path,graph_path,adoption_path,frozen_manifest,sf/'source-first90.native.json',sf/'source-proof-graph90.native.json',sf/'source-coverage90.native.json',sf/'primary-source90.raw-manifest.native.json',sf/'chronology.source-first90.native.jsonl',root/'lean-toolchain',root/'lake-manifest.json',Path(packet['copied_literal_definitions_from']['path'])]
run=write('header90.source-run.native.json',dict(schema_version=1,kind='prospective exact90 source-header audit; no BODY acceptance',reviewer='/root/fresh_source87',formalizer='/root',distinct_from_formalizer=True,distinct_from_math_verifier77=True,inputs=[pin(p) for p in inputs],chronology=pin(chron),direct_primary_before_header=True,prior_source_first90_and89_familiarity_disclosed=True,source_first_original_manifest_unchanged=True,accepted_graph_successor_exact_two_field_diff=True,root82_RAW_descriptors_reverified=True,no_graph_creator_self_approval=True,no_BODY_proof_or_Seal_review=True,canonical_mutations=False,VERIFIED=False))
decision=write('header90.source-decision.native.json',dict(schema_version=1,kind='independent prospective exact-header source-boundary decision',verdict='equivalent-after-elaboration',header_source_acceptance=True,repairs=[],blocking_deltas=[],reviewer='/root/fresh_source87',independent_from_formalizer=True,independent_from_math_verifier=True,header=pin(header),packet=pin(packet_path),review_run_sha256=raw(run),primary_version='arXiv2609.06905v1',primary_date='07 Sep 2026',license='arXiv.org perpetual non-exclusive license',primary_anchors=anchors,source_first_freeze=pin(sf/'source-first90.native.json'),source_first_manifest=pin(frozen_manifest),graph_binding=pin(graph_audit),semantic_slots=slots,deltas=deltas,literal_definitions=defs,literal_definition_count=28,analytic_binders=binders,analytic_binder_count=6,admissible_tests=dict(d='Every fixed Borel full old-history->NNReal function, finite pointwise but not uniformly bounded; no future/raw-clock argument.',F='Every joint Borel new-history x real->ENNReal, may be unbounded or infinity; no integrability premise.',A='Every Borel old-history event including null events.'),all_history_and_default_cases=cases,source_vs_ASTIS='Explicit Borel complete-history append, actual finite-recursion identity and unnormalized measure/test transport are ASTIS implicit completion of A.1/A.2/A7/A.2. Exact negative-time totalization and Fin.snoc API are implementation conventions, never new printed source truth.',substantive_delta='Actual whole H_(n+1) and its restricted joint/marginal law are conclusions; constructor measurability and equality are internally derived obligations. This header is not a wrapper assuming those obligations.',accepted_truth_boundary='One actual strict finite-history-extension transport step inside remaining S87-I5/G86-11.',truth_boundary_open=freeze['truth_boundary_open']+['unrestricted actual next-history probability law/stopped defect atom'],topology_creator_self_independent_acceptance=False,completed_semantic_BODY_review=False,Lean_compilation_claimed=False,statement_Seal_or_SAU_claim=False,theorem_VERIFIED=False,canonical_mutations=False,wholepaper_or_Goal_credit=False))
terminal=write('terminal-completion.header-source90.native.json',dict(schema_version=1,kind='native exact prospective source-header90 terminal completion',terminal_closed=True,status='HEADER_SOURCE_AUDIT_CLOSED',verdict='equivalent-after-elaboration',decision=pin(decision),run=pin(run),chronology=pin(chron),no_Seal_claim_BODY_or_proof_acceptance=True,canonical_mutations=False,VERIFIED=False))
outputs=[Path(__file__).resolve(),private,graph_audit,*snapshots,chron,run,decision,terminal]
manifest=write('closed-raw-manifest.header-source90.native.json',dict(schema_version=1,kind='closed exact RAW independent prospective source-header90 manifest',closed=True,input_set_closed=True,output_set_closed=True,inputs=[pin(p) for p in inputs],outputs=[pin(p) for p in outputs],adoption82_descriptors_checked=True,source_first_manifest_unchanged=True,manifest_root_excluded_from_self_hash=True,private_primary_extract_excluded_publication=True,canonical_mutations=False,header_ONLY_not_BODY_VERIFIED=True))
for section in ['inputs','outputs']:
 for e in load(manifest)[section]:
  p=Path(e['path']);assert raw(p)==e['raw_sha256'] and p.stat().st_size==e['bytes']
print(json.dumps(dict(status='CLOSED',decision=pin(decision),run=pin(run),manifest=pin(manifest),chronology=pin(chron),terminal=pin(terminal),verdict='equivalent-after-elaboration',repairs=[],inputs=len(inputs),outputs=len(outputs),literal_defs=len(defs),analytic_binders=len(binders),graph_creator_self_approval=False),ensure_ascii=False,indent=2))
