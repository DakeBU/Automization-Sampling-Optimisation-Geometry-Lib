import pathlib,json,hashlib,re,datetime
R=pathlib.Path('E:/Samplinglib')
B='runs/20261007-companion-priority/pbps-actual-phase-normalization103/'
S='runs/20261007-companion-priority/pbps-actual-weighted-sector102/next-primary103/'
P='runs/20261007-companion-priority/pbps-phase-normalization-preread103/'
D='runs/semantic-roundtrip/anonymous103/decoder-native/'
O=R/(B+'final-source103/')
def H(b):return hashlib.sha256(b).hexdigest()
inputs={}
def ref(p):
 p=p.replace('\\','/').replace('E:/Samplinglib/','')
 b=(R/p).read_bytes();v={'path':p,'raw_sha256':H(b),'bytes':len(b)};inputs[p]=v;return v
def read(p):ref(p);return json.loads((R/p).read_text(encoding='utf-8'))
def put(n,d):
 p=O/n;assert not p.exists();p.write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode());return ref(p.relative_to(R).as_posix())
first=read(B+'final-source103/primary-first103.native.json')
packet=read(B+'reviewer-packet103.json');pc=dict(packet);pc.pop('packet_sha256')
psha=H(json.dumps(pc,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
assert psha==packet['packet_sha256']=='c11373d3e8a67a275fe8bcaa6913d30dba5b55aa102ff34e8f63706b6b8d98b4'
pubsha=packet['publication_binding_sha256']
assert pubsha=='349f71636e82ddb57d97fb9e228a792f1d77f13dd232decdccff39c399cce8b7'
prod=ref(packet['lean']['file']);raw=(R/prod['path']).read_bytes();lines=raw.splitlines(keepends=True)
assert prod['raw_sha256']=='c7806ada54ca78514a75ea1d13ed4bf08e5af4e92546d9ba0165683d77b36af4' and len(lines)==149
assert H(packet['lean']['statement'].encode())==packet['lean']['statement_sha256']
assert H(packet['source']['original_text'].encode())==packet['source']['text_sha256']
lessonpath='website/content/declaration_lessons/pbps-actual-phase-normalization.json'
pubpath='website/content/publications/pbps-actual-phase-normalization.json'
lesson=read(lessonpath)['units'][0];pub=read(pubpath)['items'][0];ctx=packet['candidate_publication_context']
assert ctx['file']==prod['raw_sha256'] and ctx['current_lean_module']==raw.decode()
for k in ['source','statement','formulae','assumptions','obligations']:assert ctx[k]==pub[k]
for k,v in ctx['binding'].items():assert pub['bindings'][0][k]==v
for k,v in ctx['lesson'].items():assert lesson[k]==v
assert lesson['statement']==pub['statement']==packet['source']['original_text']
drun=read(D+'decoder-run.json');dt=(R/(D+'reconstruction.txt')).read_bytes()
ref(D+'reconstruction.txt');read(D+'reconstruction.json');read(D+'manifest.json')
assert H(dt)==packet['blind_reconstruction']['text_sha256'] and dt.decode()==packet['blind_reconstruction']['text']
assert ref(D+'decoder-run.json')['raw_sha256']==packet['blind_reconstruction']['decoder_run_sha256']
assert all(drun[k] is False for k in ['source_text_visible','source_identity_visible','prior_audit_visible','repair_proposals_visible'])
assert drun['canonical_supplied_packet_sha256']==packet['blind_reconstruction']['decoder_packet_sha256']
ref('runs/semantic-roundtrip/anonymous103/input.json')
assert all(v is False for v in packet['anti_anchoring'].values())
graph=read(S+'source-proof-graph-delta103.native.json')
overlay=read(S+'graph-normalization103/source-api-identity-normalization103.native.json')
top=read(P+'independent-header-math103/source-topology-admission103.native.json')
assert top['base_graph']==ref(S+'source-proof-graph-delta103.native.json')
assert top['overlay']==ref(S+'graph-normalization103/source-api-identity-normalization103.native.json')
assert top['effective_graph']['nodes_including_API_references']==51 and top['effective_graph']['edges']==79
cov=read(S+'source-coverage-delta103.native.json');primary=ref(cov['primary']['path'])
assert primary==cov['primary'];pr=(R/primary['path']).read_bytes()
for r in cov['regions']:assert H(pr[r['byte_start']:r['byte_end_exclusive']])==r['raw_sha256']
assert len(cov['regions'])==21
for k in ['base_effective102','inherited_delta','inherited_alias_overlay','inherited_independent_topology_admission']:assert ref(graph[k]['path'])==graph[k]
for leaf in graph['existing_compiled_leaves_referenced']:assert ref(leaf['artifact']['path'])==leaf['artifact']
mb=B+'independent-whole-math103/'
kernel=read(mb+'fresh-kernel-receipt103.native.json');axioms=read(mb+'fake-closure-and-axioms103.native.json')
math=read(mb+'whole-math-decision103.native.json');ref(mb+'closed-RAW-manifest103.native.json')
ref(mb+'fresh-kernel.stdout.log');ref(mb+'fresh-kernel.stderr.log')
assert kernel['production_raw_sha256']==prod['raw_sha256'] and kernel['exit_code']==0 and kernel['terminal_closed'] and kernel['target_module_not_imported'] and kernel['original_sealed_header_witness']
assert ref(kernel['kernel']['path'])==kernel['kernel'] and (R/kernel['kernel']['path']).read_bytes().startswith(raw)
assert not axioms['module_fake_closure_hits'] and axioms['both_public_theorem_and_original_header_witness_standard']
ref(P+'Header103.lean');ref(P+'root.statement-seal103.json');ref('lean-toolchain');ref('lake-manifest.json')
ref('.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Tilted.lean')
def span(a,b):
 rb=b''.join(lines[a-1:b]);lf=rb.replace(b'\r\n',b'\n')
 return {'path':prod['path'],'line_start':a,'line_end':b,'source_RAW_sha256':H(rb),'display_LF_RAW_sha256':H(lf),'bytes':len(rb)}
assert re.findall(r'^\s+let (\w+)\s*:',b''.join(lines[34:47]).decode(),re.M)==['d','Vy','U','w','ell','Zx','C','Zphase','piY','nu','gamma']
judgments=[
 'Actual lower Hessian half plus C2 gives strong convexity; positive alpha and differentiability discharge Gibbs-tail integrability. No minimizer or critical point is supplied.',
 'Continuity supplies measurability; eta positivity makes proximal quadratic nonnegative. Domination by exp(-V) proves integrability. Positive exponential and nonzero canonical volume give Zx>0, including rank0.',
 'Gaussian integral at a=1/2 yields exact ENNReal mass. Explicit rpow-to-sqrt natural-power conversion matches C, positive also at rank0. The real integral formula is conventional nonnegative-integral notation; the canonical Gaussian leaf supplies its finiteness.',
 'Actual target energy factors into position and momentum weights. Nonnegative product integration uses derived measurability. Actual position integrability permits real/ENNReal conversion, yielding position-first Zphase=ofReal(Zx*C).',
 'Derived positive Zx,C and finite ofReal give positive finite Zphase. Canonical Gibbs normalization consumes these facts and proves probability. Display formula abbreviates the positive exponential embedding; the full statement explicitly uses ofReal.',
 'Existing Gaussian density specialized to variance1 gives actual stdGaussian density C inverse times exp(-norm(p)^2/2). sqrt1 scaling is identity. No eta factor or positive-rank premise.',
 'Expand tilted and product-withDensity for derived measurable densities. Actual partition and energy identities, positivity and finite factors justify inverse/division algebra. Pointwise agreement gives exact measure equality via withDensity_congr_ae.']
regions=[]
for i,(step,j) in enumerate(zip(lesson['steps'],judgments),1):
 rg=step['lean_source_region'];a,b=rg['start_line'],rg['end_line'];rb=b''.join(lines[a-1:b]);code=step['lean'].encode()
 assert code==rb.replace(b'\r\n',b'\n') and H(code)==rg['exact_code_raw_sha256'] and rg['source_raw_sha256']==prod['raw_sha256']
 runs=[len(m.group()) for m in re.finditer(r'\\+',step['formula'])];assert all(x==1 for x in runs)
 regions.append({'step':i,'title':step['title'],'text':step['text'],'formula':step['formula'],'source_span':span(a,b),'display_code_RAW_sha256':H(code),'metadata_hash_semantics':'Exact UTF8 lesson code string; source span separately hashed.103 source is already LF, so hashes equal.','formula_escape_run_lengths':runs,'judgment':j,'accepted':True})
assert len(regions)==7
parts=[(1,6,'Canonical imports; no102 import.'),(7,22,'Bounded attribution, namespace and ambient conventions.'),(23,55,'Entire literal private Prop,6binders,11definitions,7conclusions,forall y.'),(56,69,'Public doc/interface, same six arguments; private Prop is conclusion.'),(70,85,'Definitional unfolding and actual local notation.'),(86,87,'Hessian and Gibbs-tail producer calls.'),(88,99,'Conditional continuity, domination, integrability and positive real mass.'),(100,113,'Positive exact Gaussian normalizer and scalar power conversion.'),(114,128,'Target factorization and nonnegative product integral.'),(129,133,'Positive finite mass and probability producer.'),(134,138,'Actual stdGaussian density from variance1.'),(139,145,'Tilted/product density calculation and measure equality.'),(146,149,'Axiom output and namespace closure.')]
whole=[dict(span(a,b),review=j) for a,b,j in parts]
assert [n for a,b,_ in parts for n in range(a,b+1)]==list(range(1,150))
L=graph['existing_compiled_leaves_referenced']
ids=[x['id'].replace('MeasureTheory.Measure.prod_withDensity','MeasureTheory.prod_withDensity') for x in L]
direct={'H99':[(25,32),(62,69),(86,99)],'DEFWEIGHT101':[(35,47),(73,80)],'VY-DOM103':[(88,99)],'PHASE-FACTOR103':[(100,130)],'NORM':[(49,55),(129,145)],ids[0]:[(86,86)],ids[1]:[(87,87)],ids[2]:[(102,113)],ids[3]:[(134,138)],ids[4]:[(131,132)],ids[5]:[(119,128)],ids[6]:[(139,145)]}
later={'SECTOR100','AVG100','INV100','L2A3','RESTART'};nodes=[]
for n in top['effective_graph']['topological_order']:
 role='current103-direct' if n in direct else 'later-excluded' if n in later else 'inherited-not-current-proof-dependency'
 note='Literal identity retained; no101 theorem invocation or premise.' if n=='DEFWEIGHT101' else 'Actual assumption, internal bridge or canonical producer; ingredients are discharged, not extra public premises.' if n in direct else 'Inherited node outside selected normalization; no103 credit or proof dependency on process/sector result.'
 nodes.append({'id':n,'role':role,'compiled_regions':[span(a,b) for a,b in direct.get(n,[])],'scope':note})
assert len(nodes)==len({n['id'] for n in nodes})==51
newedges=[{'source':a,'target':b,'role':'current-normalization-ingredient','target_compiled_regions':[span(x,y) for x,y in direct[b]],'proof_ingredient_not_public_premise':True} for a,b in top['effective_graph']['new_edges']]
assert len(newedges)==18
source_regions=[]
for r in cov['regions']:
 q={k:v for k,v in r.items() if k!='disposition103'};rid=q['id']
 q['compiled103_regions']=[span(25,32),span(62,69)] if rid in ['standing-curvature','standing-eta'] else [span(35,55),span(86,145)] if rid in ['target-position-energy','phase-gibbs-law'] else []
 q['disposition103']='Selected source assumptions/actual normalization, explicit ASTIS completion of proportionality.' if q['compiled103_regions'] else 'Source license retained; no primary archive.' if rid=='source-license' else 'Downstream averaging/invariance only; no current proof credit.' if rid in ['average','weight-matching-and-invariance'] else 'Inherited source region excluded from103; original process/flow/jump/survival/sector/L2 scope unchanged.'
 source_regions.append(q)
parents=[]
for id,line,why in [(ids[0],86,judgments[0]),(ids[1],87,'Positive alpha, C2-derived differentiability and produced hsc; no minimizing point.'),(ids[2],102,'Actual coefficient1/2 positive, momentum variance1.'),(ids[3],135,'Scale1, identity Gaussian map.'),(ids[4],132,'Actual ell,U and derived hpos.ne/hfin.ne; no mass premise.')]:
 leaf=next(l for l in L if l['id']==id);parents.append({'declaration':id,'artifact':leaf['artifact'],'invocation':span(line,line),'discharge':why})
coverage=put('compiled-source-coverage103.native.json',{'kind':'compiled-source-coverage103','reviewer':'/root/source_final96','reviewer_packet_sha256':psha,'publication_binding_sha256':pubsha,'production':prod,'primary':primary,'source_graph_delta':ref(S+'source-proof-graph-delta103.native.json'),'source_graph_overlay':ref(S+'graph-normalization103/source-api-identity-normalization103.native.json'),'independent_topology_admission':ref(P+'independent-header-math103/source-topology-admission103.native.json'),'source_inventory':ref(S+'source-coverage-delta103.native.json'),'source_regions':source_regions,'all21_RAW_slices_verified':True,'graph_nodes':nodes,'effective_node_count':51,'effective_edge_count':79,'edge_coverage':{'unchanged61':{'source':graph['inherited_independent_topology_admission'],'graph_input':graph['inherited_delta'],'overlay':graph['inherited_alias_overlay'],'disposition':'All61 inherited incidences retained by exact independent admission; every node disposed above. No new103 process credit. Existing NORM->SECTOR100 stays a future consumer edge.'},'new18':newedges},'no102_to_NORM_proof_dependency':True,'whole_module_regions':whole,'whole149_lines_reviewed':True,'actual_five_public_parents':parents,'exact_seven_exposition_regions':regions,'compile_receipt':ref(mb+'fresh-kernel-receipt103.native.json'),'axiom_receipt':ref(mb+'fake-closure-and-axioms103.native.json'),'compile_not_fidelity_shortcut':True,'graph_author':'/root/source_final96','topology_self_validated':False,'independently_owned_whole_module_and_private_helper_review':True,'unresolved_gaps_within_selected_boundary':[],'remaining_red_nodes':sorted(later),'full_paper_credit':False,'publication_pointer_followup':'Root should mechanically replace prospective coverage pointer/status with this compiled report after adoption; no shared metadata edited here.'})
exposition=put('exposition-review103.native.json',{'kind':'bounded-seven-step-exposition-review103','reviewer':'/root/source_final96','reviewer_packet_sha256':psha,'publication_binding_sha256':pubsha,'lesson':ref(lessonpath),'publication':ref(pubpath),'production':prod,'statement_and_source_boundary':'Complete attributed all-y statement gives11literal definitions,6hypotheses,7conclusions,position-first volume,real/ENNReal roles,rank0 and explicit ASTIS completion. No process-invariance/cost credit.','seven_regions':regions,'whole_private_Prop_and_public_interface':[span(23,55),span(61,85)],'canonical_producers':parents,'formula_rendering':'All decoded TeX command backslash runs length1; no matrix or newline commands. Mathematical formulas checked manually; no browser-render claim. Formula5 abbreviates positive density embedding, defined explicitly in the statement.','decision':'ACCEPT_BOUNDED_AUTHORED_SEVEN_STEP_EXPOSITION','bounded_exposition_seal':True,'full_Exposition_Seal':False,'browser_acceptance':False,'merged':False,'purified':False,'whole_paper_complete':False,'repairs_required':[]})
observations={
 'objects':('The decoder expands all11literal definitions, including actual tilted piY, product volume ell, real Zx, ENNReal Zphase, actual reciprocal withDensity nu and stdGaussian. The private Prop and public unfolding preserve these objects.','equivalent','Production35-47 and73-85; decoder definitions; actual target energy is V+proximal position quadratic+momentum norm squared/2. No arbitrary supplied measure or density.'),
 'domains':('Lean and decoder use any finite-dimensional real inner-product Borel E, including rank0, and ordered position-momentum E x E. Canonical volume and Gaussian match coordinate-free finite Euclidean source law.','explicit-elaboration','Production25-27,35,40,47; source Eq3.1 has R^d with position first. In rank0 C=1 and normalized singleton phase law is unit mass.'),
 'quantifiers':('Six source arguments precede11local definitions, then forall y:E. Seven assertions hold for every center without an existential chosen normalizer, critical point or finite-mass witness.','equivalent','Production28-55 and65-85; exact sealed-header witness compiles but source agreement is established by these literal quantifiers and the fresh decoder.'),
 'assumptions':('All six original assumptions are retained: positive alpha, alpha<=beta, genuine C2 V, paired Frechet Hessian bounds, positive eta and beta*eta<=1. No extra measurability/integrability/minimizer/normalizer premise.','equivalent','Production28-32 and65-69. Beta>0 follows from positive alpha and alpha<=beta, so beta*eta<=1 matches source eta<=1/beta. Canonical producers at86,87,102,132,135 receive derived facts rather than new source binders.'),
 'conclusion':('Decoder and Lean assert exactly the seven expected conclusions: position Gibbs integrability; positive real Zx; Zphase=ofReal(Zx*C); positive Zphase; finite Zphase; probability nu; exact nu=piY product stdGaussian.','explicit-elaboration','Production49-55,81-85,99,119-145. Source proportionality and product law in Eq3.1 are completed explicitly by the actual normalizer proof, accurately attributed as ASTIS elaboration.'),
 'scopes':('This is exact all-y phase-law normalization and measure identification. No evolution, invariant process, countable/signed averaging, Markov property, cost or whole-paper conclusion is present.','equivalent','Source Eq3.1 is the selected boundary; A7/A8 averaging is downstream. Publication supports only phase-gibbs-normalization and leaves weighted-invariance unresolved. No102 theorem is invoked by production.'),
 'constant_dependencies':('C=(sqrt(2*pi))^finrank(E) is a natural power; Zphase=ofReal(Zx*C). Momentum covariance is identity, without eta scaling. All other quantities depend only on E,V,eta,y; no n,T,r or unspecified constants.','equivalent','Production35-47,100-113,134-138; decoder constants agree. Rank0 uses power0=1. Actual positive finite masses prevent totalized real/ENNReal operations from hiding normalization assumptions.')
}
slots={k:{'original':first['expected_semantic_slots'][k],'reconstructed':v[0],'relation':v[1],'evidence':v[2]} for k,v in observations.items()}
deltas=[
 {'slot':'domains','severity':'informational','description':'Coordinate-free finite-dimensional Borel formulation explicitly includes rank zero.','source':'Finite Euclidean position-momentum space in Eq3.1.','lean':'Finite real inner-product Borel E and natural finrank exponent, with no positive-dimension binder.','evidence':'Production25-27,35,42,47; canonical Gaussian producer covers rank0; same law under orthonormal coordinates.','blocking':False},
 {'slot':'conclusion','severity':'informational','description':'Actual positive finite partitions and exact normalized representatives expand source proportionality.','source':'Eq3.1 defines conditional position Gibbs times standard Gaussian and gives its density up to normalization.','lean':'Seven assertions derive integrability, actual partition factorization, positivity/finiteness, probability and exact product equality.','evidence':'Production49-55 and86-145; all analytic facts derived under original binders. Publication explicitly attributes the proof as ASTIS completion, not a new quoted source theorem.','blocking':False},
 {'slot':'scopes','severity':'informational','description':'The selected normalization boundary supplies a later averaging ingredient; process invariance is excluded.','source':'Appendix A.1 subsequently averages A7 under nu and concludes invariance after further substitution/summation.','lean':'Actual phase normalization only; no time, process, signed integral, cost or invariant kernel conclusion.','evidence':'Public theorem expands only the private normalization Prop. Source coverage disposes all later regions explicitly; NORM is analytically independent of102.','blocking':False}
]
run=put('source-review-run103.native.json',{'kind':'independent-primary-first-final-source-run103','reviewer':'/root/source_final96','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer_packet':ref(B+'reviewer-packet103.json'),'reviewer_packet_sha256':psha,'publication_binding_sha256':pubsha,'primary_first':ref(B+'final-source103/primary-first103.native.json'),'primary_first_closed_before_current_packet_and_production':True,'prior_prospective_involvement_acknowledged':True,'earlier_final_semantic_verdicts_slots_deltas_repairs_used':False,'formalizer':packet['roles']['formalizer'],'decoder':packet['roles']['blind_decoder'],'decoder_native_run':ref(D+'decoder-run.json'),'decoder_visibility_flags_verified_false':True,'production':prod,'compiled_coverage':coverage,'exposition':exposition,'independently_owned_whole_private_Prop_public_proof_and_exposition_review':True,'whole149_lines_read':True,'source_region_count':21,'effective_graph_nodes':51,'effective_graph_edges':79,'topology_reused_from_independent_noncreator_admission':ref(P+'independent-header-math103/source-topology-admission103.native.json'),'self_topology_validation':False,'fresh_kernel_receipt':ref(mb+'fresh-kernel-receipt103.native.json'),'whole_math_evidence':ref(mb+'whole-math-decision103.native.json'),'Lean_evidence_not_semantic_verdict_shortcut':True,'diagnostics':'One malformed tool envelope was rejected before helper-file execution; no input or source artifact changed. Source reconstruction had already been frozen.','no_source_or_statement_repair_required':True,'no_shared_edit_or_VERIFIED':True,'no_full_primary_copy':True})
decision=put('source-review103.native.json',{'verdict':'equivalent-after-elaboration','semantic_slots':slots,'deltas':deltas,'repairs':[],'reviewer_packet_sha256':psha,'review_run_sha256':run['raw_sha256'],'publication_binding_sha256':pubsha,'reviewer':'/root/source_final96','independent_from_formalizer':True,'independent_from_decoder':True,'source_review':{'state':'accepted','reviewer':'/root/source_final96','independent_from_formalizer':True,'independent_from_decoder':True,'reviewer_packet_sha256':psha,'review_run_sha256':run['raw_sha256'],'publication_binding_sha256':pubsha,'run_artifact':run['path'],'evidence':'Fresh primary-first reconstruction preceded current packet/production/exposition. All7slots accepted; all21 source slices rehashed,51graph nodes/79edges covered by exact inherited graph plus current18ingredient edges, whole149line private Prop/public proof independently read,5actual canonical producer premises discharged,7exact formula/code regions accepted. No normalization/minimizer provider premise or process-invariance claim.','read_flags':{'primary_first_frozen_before_current_packet':True,'current_production_read':True,'current_decoder_read_after_source_freeze':True,'current_publication_and_lesson_read':True,'earlier_final_semantic_verdicts_slots_deltas_repairs_used':False,'prior_prospective_header_involvement':True,'unseen_inherited_context_claimed':False},'source_text_visible':True,'prior_final_verdict_used':False},'compiled_source_coverage':coverage,'bounded_exposition_review':exposition,'whole_module_review_owned_by':'/root/source_final96','remaining_scope':'Exact science-commit admission, generated/browser reader acceptance, main merge, postmerge purification and later normalized averaging/invariance remain separate. No full paper credit.'})
owned=[{'path':p.relative_to(R).as_posix(),'raw_sha256':H(p.read_bytes()),'bytes':p.stat().st_size} for p in sorted(O.iterdir()) if p.is_file()]
external=[v for p,v in inputs.items() if not p.startswith(B+'final-source103/')]
closure=put('closed-RAW-final-source103.native.json',{'kind':'closed-independent-final-source-exposition103','reviewer':'/root/source_final96','reviewer_packet_sha256':psha,'publication_binding_sha256':pubsha,'inputs':external,'owned_artifacts':owned,'self_hash_policy':'Manifest excludes itself; exact RAW reported separately.','no_shared_mutations':True,'no_full_primary_archive':True})
for v in external+owned:assert H((R/v['path']).read_bytes())==v['raw_sha256']
script=(O/'author_final_review103.py').read_bytes()
assert script.endswith(b'\n') and not script.endswith(b'\n\n') and b'\r' not in script and all(x==x.rstrip(b' \t') for x in script.split(b'\n'))
print(json.dumps({'decision':decision,'coverage':coverage,'exposition':exposition,'run':run,'closure':closure,'input_count':len(external),'owned_count':len(owned)},indent=2))
