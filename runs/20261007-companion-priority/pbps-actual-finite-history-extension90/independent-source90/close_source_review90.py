from pathlib import Path
import json,hashlib,re,datetime,shutil
root=Path('E:/Samplinglib');out=Path(__file__).resolve().parent;r90=out.parent
pre=root/'runs/20261007-companion-priority/pbps-next-history-extension-preread90';sf=pre/'independent-source-first90'
def sha(b):return hashlib.sha256(b).hexdigest()
def raw(p):return sha(p.read_bytes())
def pin(p):return dict(path=str(p.resolve()),raw_sha256=raw(p),bytes=p.stat().st_size,hash_mode='exact-raw-file-bytes')
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def canon(v):return sha(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def write(n,v):
 p=out/n;assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');return p
def snap(p,n):
 q=out/n;assert not q.exists();shutil.copyfile(p,q);assert raw(p)==raw(q);return q

packet_path=r90/'source-review90.packet.json';packet=load(packet_path)
assert raw(packet_path)=='7c2b4f8846e12b6899820df1b0502283243b47f1ae489ecf64ff98186fb41148' and packet_path.stat().st_size==83791
packet_canonical=canon({k:v for k,v in packet.items() if k!='packet_sha256'});assert packet_canonical==packet['packet_sha256']=='e05eb6e6f0301337eb17e14396af2577aeb852a022557b036c3e536735906000'
module=root/packet['lean']['file'];lesson_path=root/'website/content/declaration_lessons/pbps-actual-finite-history-extension.json';pub_path=root/'website/content/publications/pbps-actual-finite-history-extension.json'
assert raw(module)=='6cdc14328be5ec3ece3f028e6e1dd0185ee4031a8e651956ee0f55d4beebf029'
assert raw(lesson_path)=='f8e3db3c9cffc10938fc6350ec16a589eeb43dc2130c48f0f41544511a56b905'
assert raw(pub_path)=='908c65e23b7608a2609a515da742a1db378f087c3143807cf1ed21a5f8728022'
lesson=load(lesson_path)['units'][0];pub=load(pub_path)['items'][0];binding=pub['bindings'][0];ctx=packet['candidate_publication_context']
assert ctx['current_lean_module']==module.read_text(encoding='utf-8')
assert ctx['lesson']=={k:v for k,v in lesson.items() if k not in ['boundary','source_history_boundary']}
for k in ['source','statement','formulae','assumptions','obligations']:assert ctx[k]==pub[k]
payload={k:ctx[k] for k in ['file','current_lean_module','toolchain','dependencies','source','statement','formulae','assumptions','obligations']}
payload.update(lesson=lesson,binding={k:v for k,v in binding.items() if k not in ['audit_id','legacy_audit_debt']})
assert canon(payload)==packet['publication_binding_sha256']=='b3a9241d785c8132839c366f260d5fbc3dcaa40aba8566560ec814e6c5716472'
for k,p in [('toolchain',root/'lean-toolchain'),('dependencies',root/'lake-manifest.json')]:assert sha(p.read_text(encoding='utf-8').encode())==ctx[k]
assert sha(packet['source']['original_text'].encode())==packet['source']['text_sha256']
assert sha(packet['lean']['statement'].encode())==packet['lean']['statement_sha256']

preread=out/'closed-raw-manifest.final-preread90.native.json'
assert raw(preread)=='9d5408793d72a93c5ad4497e4a3f267a22305ba7c2cc6a898ac0078815ebc256'
for section in ['inputs','outputs']:
 for e in load(preread)[section]:
  p=Path(e['path']);assert raw(p)==e['raw_sha256'] and p.stat().st_size==e['bytes']
inventory=load(out/'final-primary-source-math-inventory90.native.json');primary=Path(inventory['primary']['path']);assert raw(primary)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
for a in inventory['anchors']:assert sha(primary.read_bytes()[a['byte_start_zero_based']:a['byte_end_exclusive']])==a['raw_span_sha256']

decdir=root/'runs/semantic-decoder-outputs/round90';decpath=decdir/'reconstruction.json';decrun=decdir/'decoder-run.json';decmanifest=decdir/'manifest.json';neutral=root/'runs/semantic-decoder-inputs/round90/packet.json';dec=load(decpath)
assert raw(decpath)=='4ebb21a3620b4ccc2326771f4b1f26da5a87092e46eff283520718560e696df9'
assert raw(decrun)==dec['decoder_run_sha256']==packet['blind_reconstruction']['decoder_run_sha256']=='b4134e2f1891da784d224913c4e66ffe1bcbfd1c25386bb599102b8064070c98'
assert raw(decmanifest)=='eeacc7307084efcfc31f50eea30fefc721badf929752a55b5baf353e55c0febb'
assert dec['reconstructed_theorem_text']==packet['blind_reconstruction']['text']
assert sha(dec['reconstructed_theorem_text'].encode())==dec['reconstructed_text_sha256']==packet['blind_reconstruction']['text_sha256']
for section in ['inputs','outputs']:
 for e in load(decmanifest)[section]:
  p=Path(e['path']);assert raw(p)==e['raw_sha256'] and p.stat().st_size==e['bytes']
assert canon({k:v for k,v in load(neutral).items() if k!='packet_sha256'})==packet['blind_reconstruction']['decoder_packet_sha256']=='49d6f3dadb0397f915fadaf4b73c95e22edf4440a92e3f5921cb37616ce44687'
assert dec['semantic_uncertainties']==load(decrun)['semantic_uncertainties']

# Mutable canonical semantic audit/cell are evidence only through exact immutable snapshots.
mutable_index=out/'mutable-input-snapshots90.native.json';mutable=load(mutable_index);mutable_paths=[]
for e in mutable['snapshots']:
 p=Path(e['snapshot_path']);assert raw(p)==e['raw_sha256'] and p.stat().st_size==e['bytes'];assert e['contents_parsed'] is False;mutable_paths.append(p)
assert len(mutable_paths)==2

text=module.read_text(encoding='utf-8');model=packet['lean']['statement'];lines=module.read_bytes().splitlines(keepends=True)
private=text.split('private def actual_finite_history_extension_statement',1)[1].split('set_option maxHeartbeats',1)[0]
expanded=private.replace(': Prop :=',':',1).strip();assert re.sub(r'\s+',' ',expanded)==re.sub(r'\s+',' ',model.strip())
names=re.findall(r'^\s+let ([^\s:]+)',model,re.M)
assert names==['c','Φ','S','rate','Λ','τ','next','record','P','ε','history','waitObs','timeObs','density','Rec','Hist','HistNext','last','H','Hnext','append','lift','μ','D','B','X','Y','ν']
meanings=[
 'Source proximal-reference center y-eta gradient V(reference).','Literal harmonic flow at raw real time, with same sqrt eta normalization.','Gradient-difference velocity reflection coefficient2; total division implements R0=I.','sqrt eta times positive part of the inner product, no alternative rate.','Actual rate integrated along actual flow from0 to NNReal horizon as a real interval integral.','Closed-target integrated-hazard hittingAfter infimum, empty entry set top; no attainment assumption added.','Absorbing stopped update; live top->stopped; live finite extraction adds time and performs actual flow/reflection.','Actual finite Nat recursion, initial live(0,z0), kth update uses e_k.','Countable real-product Exp1 measure, fixed literally.','Coordinatewise toNNReal, ambient null-support extension only.','Complete actual history tuple from index0 through n.','Live actual extended wait at clipped raw threshold; stopped0.','Real finite projection untopD0, defaults0 at top/stopped outside the positive finite guard.','Finite nonnegative real-time rate*exp(-hazard(toNNReal time)) embedded by ofReal; stopped0, auxiliary nonpositive-time extension.',
 'Tagged finite accumulated time/phase or stopped record carrier.','Complete full product of n+1 records, including unrealizable tuples.','Complete full product of n+2 records for the next history.','Deterministic old last index n.','Actual old H_n with same fixed parameters and raw clock input.','Literal actual H_(n+1), not an arbitrary supplied history map.','Fin.snoc retains full old prefix and appends live(T+toNNReal(s),S(Phi_s z)), or stopped. Raw negative flow/clipped increment is auxiliary and killed by strict density support.','Pair of complete append and unchanged prospective real relative wait.','Actual old history pushforward mu=map H P.','Strict0<s<d(h) density with finite Borel d.','Actual strict positive extended wait below finite d(H), from record n and raw coordinate n.','Actual old history and total finite-extracted wait.','Actual NEW history and the same relative waiting observation.','Actual89 strict old-history/real-time density submeasure, unnormalized.'
]
positions=list(re.finditer(r'^\s+let ([^\s:]+)',model,re.M));defs=[]
for i,(name,meaning) in enumerate(zip(names,meanings)):
 start=positions[i].start();end=positions[i+1].start() if i+1<len(positions) else model.index('        MeasurableSet B',start);snippet=model[start:end]
 defs.append(dict(name=name,literal_lean=snippet,literal_utf8_sha256=sha(snippet.encode()),meaning=meaning,classification='literal inherited actual model/observer' if i<14 else 'explicit source-implicit actual history transport packaging',accepted=True))
assert not re.search(r'\b(sorry|admit|axiom)\b|Prop\s*:=\s*True|:=\s*trivial',text)

maths=[
 'Repeat every actual model/input/observer let, change to the full expanded private Prop and consume density89, actual history87, actual harmonic flow and bounce-rate/reflection producers with the original six hypotheses. Define fixed-depth old and next COMPLETE histories and literal Fin.snoc append/lift. The append supports every abstract history and real prospective time; raw negative flow with clipped increment is auxiliary, not source finite-event dynamics.',
 'Actual87 gives measurable H and Hnext at n and n+1, including finite hazard/threshold/recursion measurability already proved there. Derive update measurability by sumProdDistrib: real-time flow is jointly measurable, zero-safe reflection is Borel, clipped time addition is Borel and stopped branch constant. Fin.lastCases/coordinate projections give Borel append; pairing gives Borel lift. Fin.snoc_castSucc proves all-prefix equality for every abstract history/time, not merely almost surely.',
 'Fix Borel finite-valued d on full old history. Define the same mu,D,B,X,Y,nu as89. Consume exact89 Borel B/X, actual restricted joint law, nu mass<=1 and all old-history joint tests. Y measurability follows actual Hnext and time projection of X. No density/independence/finite-wait/measurability provider becomes a premise.',
 'For each actual w in B, split the literal current record. Stopped contradicts positive wait. In live case top contradicts finite upper bound; then Fin.lastCases separates all preserved old entries and the new entry. Unfold actual record successor and the non-top next branch. toNNReal(real finite wait)=finite wait makes cumulative time and raw real flow agree with append. This is pointwise actual full Hnext equality, not an assumed constructor identity. Pair equality Y=lift(X) follows; no hitting attainment, no atom equality or restart is used.',
 'On Borel B the derived equality is valid almost everywhere for P restricted B. Measure.map_congr and map_map with Borel append/lift transport89 exact joint law to actual Y and Hnext laws. Measurable lift preserves nu total mass, hence<=1. Both are strict finite-component laws; missing stopped/top/outside-cutoff mass is neither discarded by normalization nor claimed as an unrestricted next-history distribution.',
 'Every joint Borel ENNReal F on HistNext x real yields admissible old-history/time test F composed with lift, whose parameter-integral measurability89 already proves. For any Borel old event A, replace actual integrand pointwise on B intersect H^-1 A using Y=lift(X), then apply89 test identity. Unbounded/infinite F, null A, unbounded finite-valued d are valid without integrability or positivity premises. This is one history extension step; ordered-time/final-survival/fullA7 assembly remains open.'
]
regions=[];previous=119
for step,math in zip(lesson['steps'],maths):
 a=step['lean_source_region'];assert a['start_line']==previous+1;previous=a['end_line'];chunk=b''.join(lines[a['start_line']-1:a['end_line']]);assert sha(chunk)==a['exact_code_raw_sha256'] and chunk.decode()==step['lean'];assert a['source_raw_sha256']==raw(module)
 regions.append(dict(**a,title=step['title'],text=step['text'],formula=step['formula'],text_utf8_sha256=sha(step['text'].encode()),formula_utf8_sha256=sha(step['formula'].encode()),exact_code_matches=True,mathematics=math,exposition='Current text/formula and exact Lean independently read; source boundary and proof sequencing match this mathematical region.',source_boundary='One actual complete next-history strict finite transport within remaining S87-I5/G86-11.',verdict='accepted'))
assert previous==340 and len(regions)==6

mathdir=r90/'independent-math90';original_lesson=mathdir/'lesson90.original.exactraw.json';original_pub=mathdir/'publication90.original.exactraw.json';diff=[]
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
differences(load(original_lesson),load(lesson_path),'lesson');differences(load(original_pub),load(pub_path),'publication')
assert diff==['lesson/units/0/steps/0/formula','publication/items/0/formulae/0/tex'],diff
assert lesson['steps'][0]['formula']==pub['formulae'][0]['tex']
assert '\\max\\{s,0\\}' in lesson['steps'][0]['formula'] and '\\mathrm{stopped}' in lesson['steps'][0]['formula']

focused=mathdir/'fresh-focused-build.receipt.json';kernelrec=mathdir/'fresh-whole-source-kernel.receipt.json';fr=load(focused);kr=load(kernelrec)
for rec in [fr,kr]:
 assert rec['exit_code']==0 and rec['terminal_closed'] and rec['source']['raw_sha256']==raw(module)
 for k in ['source','probe','stdout','stderr']:
  if rec.get(k):
   e=rec[k];p=root/e['path'];assert raw(p)==e['raw_sha256'] and p.stat().st_size==e['bytes']
probe=root/kr['probe']['path'];kernel_log=root/kr['stdout']['path'];log=kernel_log.read_text(encoding='utf-8');assert text.strip() in probe.read_text(encoding='utf-8')
axioms={x.strip() for x in re.search(r'depends on axioms:\s*\[([^\]]+)\]',log,re.S).group(1).split(',')};assert axioms=={'propext','Classical.choice','Quot.sound'}
external=[x.split(' ',1)[1] for x in log.splitlines() if x.startswith('EXTERNAL_ASTIS_DEPENDENCY ')];public=[x for x in external if not x.startswith('_private.')]
assert len(public)==4 and any(x.endswith('ActualConditionalNextWaitDensity.actual_conditional_next_wait_density') for x in public) and any(x.endswith('ActualFiniteHistoryTailLaw.actual_finite_history_tail_law') for x in public)
assert not any('ActualConditionalNextWaitSurvival' in x for x in external)
assert 'LOCAL_PROOF_CONSTANT_COUNT 11' in log and 'TRANSITIVE_ASTIS_CONSTANT_COUNT 95' in log
assert 'LOCAL_NO_VALUE' not in log and 'PROJECT_NO_VALUE' not in log and 'sorryAx' not in log

snapshots=[snap(packet_path,'source-review90.packet.exactraw.json'),snap(module,'module90.exactraw.lean'),snap(lesson_path,'lesson90.exactraw.json'),snap(pub_path,'publication90.exactraw.json'),snap(decpath,'decoder90.reconstruction.exactraw.json'),snap(decrun,'decoder90.run.exactraw.json'),snap(decmanifest,'decoder90.manifest.exactraw.json'),snap(neutral,'decoder90.input.exactraw.json')]
uncertainties=write('decoder90.uncertainties.native.json',dict(schema_version=1,source=pin(decpath),semantic_uncertainties_verbatim=dec['semantic_uncertainties'],native_output_modified=False,assessments=[
 'Infimum semantics and empty-set top are retained. This90 pointwise constructor proof uses only a finite literal wait and actual recursion definition, not an inferred hitting attainment theorem. Existing89 density/hazard regularity is consumed internally.',
 'Blind decoder correctly supplies reconstruction only, not source fidelity. Current source decision is independently compared with direct primary and preimplementation source inventory; no decoder source verdict is inferred.',
 'Infinite-event nonexplosion, unrestricted normalization/zero-infinity law are outside the exact proposition and remain open. This agrees with primary-first frozen boundary.'
],blocking=False))
kernel_audit=write('source-review90.kernel-evidence.native.json',dict(schema_version=1,kind='independent read of underlying exact-source compiler/kernel evidence, no other mathematical decision adopted',focused_receipt=pin(focused),whole_source_kernel_receipt=pin(kernelrec),probe=pin(probe),native_log=pin(kernel_log),exact_current_whole_source_occurs_in_probe=True,standard_axioms=sorted(axioms),owned_constant_count=11,transitive_ASTIS_count=95,immediate_public_producers=public,immediate_private_generated_count=len(external)-len(public),producer_use='Density89 supplies strict X law/mass/tests. Actual87 is separately used for actual H and Hnext Borel maps, not redundantly to reprove89 probability factorization. Flow and bounce/reflection producers derive append measurability. No survival88 parent or new provider assumption.',all_owned_generated_constants_traversed=True,whole_math_verdict_read=False,source_fidelity_not_inferred_from_compilation=True))
originals={
 'objects':'Printed actual integrated-hazard clock/finite bounce recursion and complete history; frozen ASTIS completion constructs Borel whole append/lift, derives guarded actual H_(n+1) identity, then transports89 strict finite submeasure.',
 'domains':'Finite-dimensional real inner-product Borel realization of source Euclidean space including rank0; tagged records, full Hist_n and Hist_(n+1), raw real clock product, finite NNReal cutoff, extended wait and real prospective time.',
 'quantifiers':'Every fixed deterministic y,r,z0,n; every fixed Borel full-old-history d with finite values; every jointly Borel ENNReal F on new history/time; every Borel old-history A including null events. All abstract-history append/prefix properties hold everywhere.',
 'assumptions':'Exactly six original analytic hypotheses: alpha>0,alpha<=beta,globalC2V,two Hessian bounds all x,v,eta>0,beta eta<=1; carrier typing plus admissible Borel d/F/A tests. Append measurability/actual identity/density laws remain internal proof dependencies.',
 'conclusion':'Derived Borel Hnext/append/lift, universal complete-prefix preservation, pointwise actual finite-guard equality, restricted actual joint and next-history marginal pushforward laws, lifted mass<=1, parameter test-integral measurability and unnormalized old-event identity.',
 'scopes':'Only actual complete n+1 history under a strict finite-event restricted submeasure. Infinite/stopped/zero/outside-cutoff mass remains absent and unnormalized. Auxiliary real totalization is not source dynamics. Full ordered-time/final survival/A7 and global restart/results stay open.',
 'constant_dependencies':'Original Exp1, coefficient2 reflection, sqrt eta harmonic scaling, beta eta<=1 and mass bound1; same actual history-law product real-volume density. No new rescaling, positive event mass, density<=1 or new-history Lebesgue reference is asserted.'}
evidence={
 'objects':'Primary A1.E1/E2 and A.2; exact current full private Prop/28 literal definitions; BODY regions1-4 prove complete constructor semantics and actual recursion rather than assuming them.',
 'domains':'All literal carrier/function types and Fin.snoc preservation; raw negative Phi with clipped cumulative increment is explicit total extension, killed by D on nonpositive times. Rank0/unrealizable histories retained.',
 'quantifiers':'Exact private Prop equals packet statement, public theorem targets full private Prop and BODY change retains all scopes. Fixed d may be nonconstant; d(H) random, no independent random family or future-input argument.',
 'assumptions':'Direct standing/eta source spans; all6 binder types unchanged, actual producer calls receive those6. No regularity/constructor/finite-wait/independence/conditional-law hypothesis added.',
 'conclusion':'All6 exact contiguous BODY regions120-340 independently read with text/formulas. Actual identity pointwise on B then measure-map congruence/composition and89 tests give all conclusions; no normalization.',
 'scopes':'Fresh native decoder reconstruction and all current exposition preserve strict finite restricted scope and explicit ASTIS attribution. No hitting attainment or global implication is imported.',
 'constant_dependencies':'Literal c/Phi/S/rate/P/D/append/lift and map mass proof; standard kernel log and actual producer usage support the same constants and measures.'}
slots={k:dict(original=originals[k],reconstructed=json.dumps(dec[k],ensure_ascii=False,sort_keys=True,indent=2),evidence=evidence[k],relation='explicit-elaboration' if k in ['objects','domains','conclusion','scopes'] else 'equivalent') for k in originals}
delta_specs=[
 ('D90-1','objects','source-implicit','Author finite update and Borel finite recursion','Explicit Borel complete-history append and actual guarded equality','Necessary ASTIS iteration ingredient; constructor identity/measurability are conclusions, not providers.'),
 ('D90-2','domains','domain-clarification','Source Euclidean phase space','Finite-dimensional real inner-product Borel realization incl rank0','Coordinate-free exact formulas; rank0 is benign and explicitly disclosed.'),
 ('D90-3','objects','notation-resolution','Source positive finite actual jump','Total append uses raw-negative Phi, clipped cumulative increment and absorbing stopped branch','These are auxiliary Borel totalizations, accurately shown in repaired current formulas and eliminated by strict density support.'),
 ('D90-4','quantifiers','quantifier-clarification','History-dependent cutoff and measurable path factors','Every fixed Borel full-history d, joint ENNReal F and Borel old-history A','Admissible tests, not added analytic premises; d(H) random by composition, fixed deterministic n retained.'),
 ('D90-5','conclusion','source-implicit','A7 iteration needs actual updated complete history','Actual restricted joint/marginal H_(n+1) laws and all nonnegative tests by89 transport','New actual recursion bridge distinguishes this from an assumed constructor wrapper; mass stays unnormalized and<=1.'),
 ('D90-6','scopes','unresolved','Full ordered-time/path A7 assembly and global G86-11','Only one strict actual next-history extension step','Remaining ordered density iteration, final survival/count/path factors and all global/main/composition/Goal remain explicitly open.'),
 ('D90-7','scopes','notation-resolution','Native decoder hitting-infimum uncertainty','No hitting attainment inferred in finite-recursion transport','Exact native uncertainties preserved verbatim; source completion uses existing89 only within its reviewed boundary.')]
deltas=[dict(id=i,slot=s,source=a,lean=b,classification=c,reason=j,blocking=False,severity='informational',description=a+' → '+b+'. '+j,evidence=evidence[s]) for i,s,c,a,b,j in delta_specs]
binders=[dict(**x,header_and_public_and_BODY_present=True,extra_provider=False) for x in load(sf/'source-first90.native.json')['source_hypotheses']]
assert len(binders)==6
boundary=dict(target='One actual complete next-history strict finite transport step within remaining S87-I5/G86-11.',source_graph=pin(pre/'source-proof-graph90.accepted-successor.json'),unchanged_source_coverage=pin(sf/'source-coverage90.native.json'),graph_creator_self_independent_approval=False,open=load(out/'final-primary-first90.freeze.native.json')['truth_boundary_open'])
inputs=[packet_path,module,lesson_path,pub_path,primary,preread,out/'final-primary-first90.freeze.native.json',out/'final-primary-source-math-inventory90.native.json',out/'chronology.final-source90.native.jsonl',sf/'source-first90.native.json',sf/'source-proof-graph90.native.json',sf/'source-coverage90.native.json',pre/'source-proof-graph90.accepted-successor.json',pre/'independent-header-source90/closed-raw-manifest.header-source90.v2.native.json',neutral,decpath,decrun,decmanifest,focused,kernelrec,probe,kernel_log,root/fr['stdout']['path'],root/fr['stderr']['path'],root/kr['stderr']['path'],original_lesson,original_pub,r90/'publication-freeze90.after-exposition.json',root/'lean-toolchain',root/'lake-manifest.json',mutable_index,*mutable_paths]
inputs += [root/'AutoSamplingTheory/ExampleCases/ProximalBPS'/n for n in ['ActualConditionalNextWaitDensity.lean','ActualFiniteHistoryTailLaw.lean','ActualHarmonicFlow.lean','ActualBounceRate.lean']]
chron=out/'chronology.source-review90.native.jsonl';assert not chron.exists()
events=[dict(event='INHERIT_CLOSED_PRIMARY_FIRST_FINAL90_PREREAD',manifest=pin(preread),direct_primary_before_current_BODY_lesson_decoder_packet=True,prospective89_90_header_familiarity_disclosed=True,prospective_header_not_BODY_acceptance=True),dict(event='FRESH_CURRENT90_INPUTS_READ_AND_MUTABLE_CANONICAL_BYTES_SNAPSHOTTED',packet=pin(packet_path),module=pin(module),lesson=pin(lesson_path),publication=pin(pub_path),mutable_snapshot_index=pin(mutable_index),mutable_audit_cell_contents_not_parsed=True),dict(event='NATIVE_DECODER_READ_AND_UNCERTAINTIES_PRESERVED',decoder=pin(decpath),uncertainties=pin(uncertainties),other_math_source_verdict_not_read=True),dict(event='ALL_DEFINITIONS_BINDERS_BODY_PROSE_AND_KERNEL_EVIDENCE_COMPARED',literal_definitions=28,analytic_binders=6,exact_exhaustive_contiguous_BODY_regions=6,BODY_start=120,BODY_end=340,publication_binding=canon(payload),exact_two_field_formula_overlay_diff=diff,kernel=pin(kernel_audit)),dict(event='FINAL90_SOURCE_COMPARISON_CLOSED',verdict='equivalent-after-elaboration',repairs=[],accepted_target=boundary['target'],canonical_mutations=False,VERIFIED=False)]
chron.write_text(''.join(json.dumps(dict(sequence=i+1,recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),**e),ensure_ascii=False)+'\n' for i,e in enumerate(events)),encoding='utf-8',newline='\n')
run=write('source-review90.run.native.json',dict(schema_version=1,kind='independent primary-first anti-anchored final90 source review run',reviewer='/root/fresh_source87',formalizer=packet['roles']['formalizer'],decoder=packet['roles']['blind_decoder'],independent_from_formalizer=True,independent_from_decoder=True,chronology=pin(chron),inputs=[pin(p) for p in inputs],anti_anchoring=dict(primary_first_closed_before_current_BODY_lesson_decoder_packet=True,prospective_header89_90_familiarity_disclosed=True,no_whole_math_verdict_as_fidelity=True,no_prior90_source_fidelity_verdict_read=True,mutable_semantic_audit_snapshot_not_parsed=True,own_graph_not_self_independently_approved=True),checks=dict(packet_RAW_canonical_and_publication_binding=True,complete_privateProp_expansion=True,all28defs_and6analytics=True,all6BODY_regions_exhaustive_exact=True,current_source_prose_formulae_independently_read=True,native_decoder_inputs_outputs_RAW_reverified=True,uncertainties_verbatim=True,underlying_whole_source_kernel_receipts_terminal0=True,mutable_audit_cell_bound_to_immutable_snapshots=True),canonical_mutations=False,VERIFIED=False))
decision=write('source-review90.decision.native.json',dict(schema_version=1,semantic_slots=slots,deltas=deltas,verdict='equivalent-after-elaboration',repairs=[],reviewer='/root/fresh_source87',independent_from_formalizer=True,independent_from_decoder=True,review_evidence='Direct fixed primary and immutable source-first/final preread inventory compared with fresh exact current privateProp/BODY/text/formulas and source-blind reconstruction. Underlying kernel evidence checked independently of mathematical verdict. Only bounded actual strict next-history transport accepted.',review_run_sha256=raw(run),reviewer_packet_sha256=packet_canonical,reviewer_packet_raw_sha256=raw(packet_path),publication_binding_sha256=canon(payload),module=pin(module),lesson=pin(lesson_path),publication=pin(pub_path),primary_version_license=dict(version='arXiv2609.06905v1',date='07 Sep 2026',license='arXiv.org perpetual non-exclusive license',primary=pin(primary),anchors=inventory['anchors'],long_primary_extracts='Only inherited *.private.json, excluded publication; no full primary copy created.'),literal_definition_audit=defs,literal_definition_count=28,analytic_binder_audit=binders,analytic_binder_count=6,privateProp_audit=dict(fully_expanded_literal_privateProp_matches_packet=True,public_theorem_targets_complete_privateProp=True,BODY_change_retains_same_fullProp=True,all14inherited_8history_6cutoff_lets=True,no_hidden_provider=True),admissible_tests=dict(d='Every fixed Borel complete old-history->NNReal cutoff, finite pointwise, possibly unbounded across histories. d(H) random by composition; no external random d or future raw input.',F='Every jointly Borel next-history x real->ENNReal; unbounded/infinity allowed, no integrability premise.',A='Every Borel old-history set, including null A; no division or positive-mass premise.',classification='Admissible measurable tests, not extra source analytic/independence/constructor premises.'),body_audit=regions,whole_body_audit=dict(start_line=120,end_line=340,regions=6,exhaustive_contiguous=True,all_current_statement_assumptions_text_formulas_Lean_independently_read=True),exact_successor_exposition_check=dict(original_lesson=pin(original_lesson),original_publication=pin(original_pub),independently_verified_changed_paths=diff,current_total_append_formula_matches_literal_Lean=True,other_reviewer_repair_verdict_not_imported=True),boundary_cases=dict(negative_time='Raw Phi_s, clipped time increment; explicit Borel auxiliary extension outside D support.',stopped='Append stopped preserves old prefix; W0 and rho0 make strict finite event/density zero.',live_infinity='Extended W top fails finite d upper guard; untopD0 only auxiliary offguard, no phase at infinity.',zero_wait_d0='Strict positivity/cutoff excludes zero; zero kernel/submeasure; no no-atom/equal-endpoint assertion.',n0='Singleton initial history extends to actual two-record H1 using raww0.',rank0='Allowed; zero hazard and strict finite submeasure zero.',unrealizable='Every-history append/lift/prefix/integrand measurability, actual equality only for actual H_n on B.',nullA='Unnormalized restricted extended integral identity valid without positive mu(A).',deterministic_n='Fixed event depth, no random stopping-index or physical-time restart conclusion.',full_history='Every old record retained; new record identified with literal actual recursion, not merely last-state summary.',reference='Old-history product real-volume density pushed forward; no unsupported new-history Lebesgue density or normalization.'),kernel_evidence=pin(kernel_audit),decoder_uncertainties=pin(uncertainties),native_structured_reconstruction={k:dec[k] for k in slots},mutable_canonical_snapshot_evidence=dict(index=pin(mutable_index),immutable_inputs=[pin(p) for p in mutable_paths],live_original_paths_are_provenance_only=True,prior_verdict_contents_not_parsed=True),accepted_truth_boundary=boundary,blocking_deltas=[],body_source_fidelity_acceptance=True,topology_creator_self_independent_acceptance=False,theorem_VERIFIED_transition=False,wholepaper_or_Goal_acceptance=False,browser_or_layout_acceptance=False,reader_validation='Current canonical authored statement/formulas/steps and six exact initially-foldable source-region metadata checked. No DOM/browser/SVG/layout/deployment validation is claimed.',delta_slots={x['id']:x['slot'] for x in deltas}))
for s in slots.values():
 for k in ['original','reconstructed','evidence']:assert isinstance(s[k],str) and s[k].strip()
terminal=write('terminal-completion.source-review90.native.json',dict(schema_version=1,kind='native final source-review90 terminal completion',terminal_closed=True,status='SOURCE_REVIEW_CLOSED',verdict='equivalent-after-elaboration',decision=pin(decision),run=pin(run),chronology=pin(chron),accepted_target=boundary['target'],repairs=[],blocking_deltas=0,canonical_mutations=False,VERIFIED=False))
outputs=[Path(__file__).resolve(),*snapshots,mutable_index,*mutable_paths,uncertainties,kernel_audit,chron,run,decision,terminal]
manifest=write('closed-raw-manifest.source-review90.native.json',dict(schema_version=1,kind='closed exact RAW independent final source90 BODY/source review manifest',closed=True,input_set_closed=True,output_set_closed=True,inputs=[pin(p) for p in inputs],outputs=[pin(p) for p in outputs],inherited_primary_first_preread_manifest=pin(preread),mutable_canonical_artifact_policy='The audit/cell inputs bind only immutable exactraw snapshots. Original live paths in snapshot index are attribution coordinates, not mutable manifest inputs.',manifest_root_excluded_from_self_hash=True,private_source_extracts_excluded_publication=True,canonical_mutations=False,VERIFIED=False))
for section in ['inputs','outputs']:
 for e in load(manifest)[section]:
  p=Path(e['path']);assert raw(p)==e['raw_sha256'] and p.stat().st_size==e['bytes']
print(json.dumps(dict(status='CLOSED',decision=pin(decision),run=pin(run),manifest=pin(manifest),chronology=pin(chron),terminal=pin(terminal),verdict='equivalent-after-elaboration',repairs=[],inputs=len(inputs),outputs=len(outputs),accepted_target=boundary['target']),ensure_ascii=False,indent=2))
