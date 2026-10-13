from pathlib import Path
import copy, hashlib, json, os, sys

root = Path.cwd(); sys.path.insert(0, str(root / 'tools'))
import astis_publication as pub, astis_semantic_roundtrip as rt, astis_advance as adv
r = Path('runs/20261007-companion-priority/pbps-actual-harmonic-flow73')
pre = Path('runs/20261007-companion-priority/pbps-harmonic-flow-preproof73')
load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
def save(p, x):
    Path(p).write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
def new(p, x):
    p = Path(p); assert not p.exists(), p; save(p, x)
def pin(p):
    p = Path(p); b = p.read_bytes()
    return dict(path=p.resolve().as_posix(), RAW_bytes=len(b), RAW_sha256=sha(b), LF_sha256=sha(b.replace(b'\r\n', b'\n')))

freeze = load(r / 'mathematics-freeze73.json')
for z in freeze['inputs']:
    assert sha(Path(z['path']).read_bytes()) == z['RAW_sha256'], z['path']
claim = load(r / 'claim.json'); decl = claim['target_declarations'][0]; file = claim['proposed_files'][0]
cid = claim['frontier_cell']; cp = Path('research-wiki/frontier-cells') / (cid + '.json')
c = load(cp); assert c['status'] == 'claimed'; new(r / 'cell.before-publication73.json', c)
boundary = 'Only the actual deterministic harmonic segment and its nine stated laws are focused-compiled. The measurable stochastic bounce/rate/clock recursion, nonexplosion, actual half-turn H_y and terminal Markov kernel, reversal, invariance, same-J lift, actual K/r_rho/B27/B28, full PBPS/SPHMC main results, implementation errors/caps, expected-query costs and actual-input composition remain open. Independent review, serialized integration, full Exposition Seal, PURIFIED, main/live and whole-Goal completion are separate admissions.'
c['evidence']['focused_checks'] = [dict(command=claim['focused_checks'][0], result='PASS2523; standard three axioms only; exact sealed six callers and nine conclusions.', evidence=freeze['compiled'][0]['focused_receipt']['path'])]
c['evidence']['truth_boundary'] = boundary
c['blocked']['reason'] = 'Frozen focused-compiled deterministic result; independent mathematics, blind reconstruction, whole implementation/source and publication review pending.'
c['source_detail_audit']['fidelity_boundary'] = boundary
c['source_detail_audit']['gap'] = 'Seven omitted deterministic source bridges are implemented internally and await independent full-body review; stochastic construction remains open.'
c['conceptual_mirror_audit'] = load(r / 'conceptual-mirror-audit73.json')
c['learning_contract']['failure_class'] = 'IMPLEMENTATION_FAILED'
c['learning_contract']['salvage'].update(required=True, status='completed', reason='Two distinct compiler diagnostics repaired without changing sealed mathematics; see compiler-diagnoses73.json. All nine clauses now compile.', promoted_fragments=[decl], discarded_fragments=[])
c['purification']['scope'] = boundary
save(cp, c)

assumptions = [
    'E is a finite-dimensional real inner-product space with its norm and a measurable structure equal to its Borel structure. Rank zero is allowed; the product space uses its usual product structures.',
    'V:E→ℝ is twice continuously Frechet differentiable on all E. The nonnegative moduli α,β satisfy 0<α and α≤β, and α‖v‖²≤D²V(x)[v,v]≤β‖v‖² for every x,v∈E.',
    'The real step η satisfies η>0 and βη≤1. The endpoint αη=1 is allowed. The original six analytic callers are retained; only C² for gradient continuity and η>0 are invoked in this deterministic proof.',
    'The parameters y,xRef range independently over E, the time variable over all real numbers, and z=(x,p) over E×E. The gradient is the Hilbert gradient of V; c,Φ,H are the exact displayed definitions.',
    'H is a weighted SUM of the two individual squared vector norms, not the square of a product-space max norm. No nonzero energy, positive dimension, stochastic kernel, supplied flow certificate or higher derivative bound is assumed.'
]
statement = '''Let E be a finite-dimensional real inner-product Borel space, including rank zero. Let V:E→ℝ be C² on all E, let α,β≥0 satisfy 0<α≤β and α‖v‖²≤D²V(x)[v,v]≤β‖v‖² for all x,v∈E, and assume η>0 and βη≤1. For every y,xRef∈E set c=y−η∇V(xRef), and for t∈ℝ, z=(x,p)∈E×E define Φ_t(z)=(c+cos(t)(x−c)+√η sin(t)p,−sin(t)(x−c)/√η+cos(t)p) and H(z)=(η⁻¹‖x−c‖²+‖p‖²)/2. Then (1) the map (y,xRef,t,z)↦Φ_t(z) is jointly continuous on (E×E)×ℝ×(E×E); (2) it is jointly Borel measurable; (3) Φ_0(z)=z; (4) Φ_{s+t}(z)=Φ_s(Φ_t(z)) for all real s,t; (5) Φ_{−t}(Φ_t(z))=Φ_t(Φ_{−t}(z))=z; (6) writing (X_t,P_t)=Φ_t(z), both time derivatives exist at every real t and satisfy dX_t/dt=√η P_t and dP_t/dt=−(X_t−y)/√η−√η∇V(xRef); (7) H(z)≥0; (8) H(Φ_t(z))=H(z); and (9) Φ_π(z)=(2c−x,−p). These conclusions quantify every displayed parameter and state. The original six source-standing callers persist; the deterministic calculation invokes C² through gradient continuity and η>0, while the two Hessian bounds, positive lower modulus and step cap are retained rather than used in its BODY. No energy positivity, positive dimension, strict endpoint or higher derivative assumption is added. This is the actual deterministic arc ingredient of the cited algorithm, with ASTIS supplying the omitted elementary continuity, group, differentiation and norm-cancellation bridges. It does not construct the stochastic trajectory, prove nonexplosion or identify an invariant/terminal sampling law.'''
formulas = [
    r'c=y-\eta\nabla V(x_{\rm ref}),\quad\Phi_t(x,p)=\left(c+\cos t\,(x-c)+\sqrt\eta\sin t\,p,\,-\frac{\sin t}{\sqrt\eta}(x-c)+\cos t\,p\right).',
    r'\Phi_0=\mathrm{id},\quad\Phi_{s+t}=\Phi_s\circ\Phi_t,\quad\Phi_{-t}=\Phi_t^{-1},\qquad\dot X_t=\sqrt\eta P_t,\quad\dot P_t=-\frac{X_t-y}{\sqrt\eta}-\sqrt\eta\nabla V(x_{\rm ref}).',
    r'H(x,p)=\frac{\eta^{-1}\|x-c\|^2+\|p\|^2}{2}\ge0,\quad H(\Phi_tz)=H(z),\qquad\Phi_\pi(x,p)=(2c-x,-p).'
]
s = Path(file).read_text(encoding='utf8'); body = s.index(':= by\n', s.index('theorem actual_harmonic_flow_laws'))
def step(title, text, formula, start, end):
    assert s.count(start, body) == 1, start
    a = s.index(start, body); b = s.index(end, a); code = s[a:b].rstrip() + '\n'
    return dict(title=title, text=text, formula=formula, lean=code,
        detail='Exact compiled contiguous proof BODY; local literal c,Φ,H and preceding facts remain in scope.',
        lean_source_region=dict(path=file, source_raw_sha256=sha(Path(file).read_bytes()),
            start_line=s[:a].count('\n') + 1, end_line=s[:a+len(code)].count('\n'), exact_code_raw_sha256=sha(code.encode())))
steps = [
    step('Establish the scale and joint continuity', 'Since η>0, r=√η is positive, nonzero and r²=η. The canonical ASTIS gradient-continuity theorem applies to V∈C² after lowering its differentiability order to one. Hence c depends continuously on (y,xRef), and the displayed trigonometric and scalar operations make Φ jointly continuous in all four inputs. Joint Borel measurability follows for the actual product Borel spaces; it is used when reassembling the conclusions.', r'r=\sqrt\eta>0,\quad r^2=\eta,\quad c(y,x_{\rm ref})=y-\eta\nabla V(x_{\rm ref})\ \text{is continuous}.', '  have hr :', '  have hzero'),
    step('Verify identity, group composition and inverse', 'At time zero the sine vanishes and cosine is one. Expanding Φ_s(Φ_tz), the cosine and sine addition formulas identify both coordinates with Φ_{s+t}z; division is legitimate because √η≠0. Taking s=−t or t=−s yields both inverse identities. All times are real, with no domain restriction.', r'\cos(s+t)=\cos s\cos t-\sin s\sin t,\quad\sin(s+t)=\sin s\cos t+\cos s\sin t,\quad\Phi_{-t}\Phi_t=\Phi_t\Phi_{-t}=\mathrm{id}.', '  have hzero', '  have hode'),
    step('Differentiate the two actual coordinates', 'Differentiate the sine and cosine expressions while fixing y,xRef and the initial state. The position derivative is −sin(t)(x−c)+r cos(t)p=rP_t. For momentum, −cos(t)(x−c)/r−sin(t)p equals −(X_t−y)/r−r∇V(xRef), using c=y−η∇V(xRef) and r²=η. HasDerivAt.congr_deriv changes only the vector derivative expression; it supplies no ODE hypothesis.', r'\dot X_t=-\sin t\,(x-c)+r\cos t\,p=rP_t,\quad\dot P_t=-\frac{\cos t}{r}(x-c)-\sin t\,p=-\frac{X_t-y}{r}-r\nabla V(x_{\rm ref}).', '  have hode', '  have hnonneg'),
    step('Keep the weighted energy nonnegative', 'Both squared norms are nonnegative. Since η>0, its inverse is nonnegative, and dividing their weighted sum by two preserves nonnegativity. Zero initial energy is included.', r'H(z)=\tfrac12(\eta^{-1}\|x-c\|^2+\|p\|^2)\ge0.', '  have hnonneg', '  have henergy'),
    step('Cancel the mixed terms in the conserved energy', 'Put q=x−c, C=cos t and S=sin t. Translate the first coordinate back by c and expand each individual squared norm. The mixed terms are +2CS⟨q,p⟩/r and −2CS⟨q,p⟩/r, which cancel. The remaining sum is (C²+S²)(r⁻²‖q‖²+‖p‖²). Using C²+S²=1 and r²=η gives H(Φ_tz)=H(z), with the exact factor one half retained.', r'r^{-2}\|Cq+rSp\|^2+\|-S q/r+Cp\|^2=(C^2+S^2)(r^{-2}\|q\|^2+\|p\|^2)=r^{-2}\|q\|^2+\|p\|^2.', '  have henergy', '  have hpi'),
    step('Evaluate the half-turn and collect the nine laws', 'At t=π, sin π=0 and cos π=−1, so X_π=c−(x−c)=2c−x and P_π=−p. Collect the continuity/Borel, initial, group, two inverse, ODE, nonnegative-energy, conservation and half-turn conclusions. This endpoint belongs to a deterministic arc only; stochastic bounces may change the eventual terminal law.', r'\Phi_\pi(x,p)=(c-(x-c),-p)=(2c-x,-p).', '  have hpi', '\nend\n')
]
source = dict(url='https://arxiv.org/html/2609.06905v1#A1', edition=load(pre / 'root.statement-seal73.json')['source_revision'],
    anchor=claim['source_anchor'], wording_status='faithful paraphrase',
    attribution='Fan Chen, Sinho Chewi, Jianfeng Lu and Matthew S. Zhang, arXiv:2609.06905v1, Algorithm1, Section3 and AppendixA.1. ASTIS completes the deterministic explicit-flow/weighted-energy details; stochastic Proposition3.1 is a separate consumer, not a theorem proved here.')
deltas = [dict(source='Finite-dimensional Euclidean state with source C² potential, 0<α≤β, both global Hessian bounds, η>0 and βη≤1.',
    lean=assumptions[0]+' '+assumptions[1]+' '+assumptions[2], classification='same', reason='Retain the original six source-standing analytic conditions. Inner-product-coordinate presentation and Borel typing do not add regularity. Rank-zero degenerate extension is explicit and checked.'),
    dict(source='Printed deterministic harmonic arc and preserved weighted energy; elementary continuity/group/differentiation details are implicit.', lean=statement, classification='source-implicit', reason='The literal coordinates and weighted sum are unchanged. Missing deterministic bridges are proved internally using the canonical gradient producer and fixed Mathlib; no proof certificate is a caller premise.'),
    dict(source='Stochastic trajectory/nonexplosion/invariance/actual terminal kernel and sampling complexity.', lean=boundary, classification='unresolved', reason='Deterministic harmonic laws alone do not produce clocks, bounce recursion, invariant laws, costs or the full paper.')]
slug='pbps-actual-harmonic-flow'; aid='ASTIS-RT-20261010-PBPSActualHarmonicFlow'; title='Actual PBPS harmonic flow and conserved weighted energy'
item=dict(id=slug, library='pbps', chapter='pbps-01', chapter_path='example-cases/samplewiki/companions/proximal-bouncy-particle.html',
    title=title, source=source, statement=statement, assumptions=assumptions,
    formulae=[dict(label=x, tex=y) for x,y in zip(['Actual arc','Group and ODE','Energy and half-turn'],formulas)],
    obligations=[dict(id='actual-harmonic-flow',label='Actual deterministic harmonic laws with internal omitted bridges'),dict(id='stochastic-and-paper',label='Stochastic construction and full sampling/cost/composition')],
    bindings=[dict(declaration=decl,cell=cid,role='proof-edge',supports=['actual-harmonic-flow'],audit_id=aid,boundary=boundary,assumption_deltas=deltas)])
for k in ['declaration_level','statement_seal','source_proof_coverage','proof_digestion','purification']:
    item[k]=copy.deepcopy(c[k])
unit=dict(kind='theorem',declaration=decl,title=title,sources=[dict(url=source['url'],label=source['anchor'],scope=boundary)],
    tests=claim['focused_checks'],assumptions=assumptions,statement=statement,formula=formulas[0]+'\quad '+formulas[2],boundary=boundary,steps=steps,
    lean_statement=statement,lean_proof='; '.join(z['title'] for z in steps),
    helpers=[decl.rsplit('.',1)[0]+'.actual_harmonic_flow_statement'],
    astis_dependencies=c['proof_digestion']['existing_substrate'],
    mathlib_dependencies=['Real.sqrt_pos','Real.sq_sqrt','Real.cos_add','Real.sin_add','Real.hasDerivAt_cos','Real.hasDerivAt_sin','HasDerivAt.smul_const','HasDerivAt.congr_deriv','norm_add_sq_real','norm_smul','real_inner_smul_left','real_inner_smul_right','Real.sin_sq_add_cos_sq','Continuous.measurable','Real.sin_pi','Real.cos_pi'])
pp=Path('website/content/publications')/(slug+'.json');lp=Path('website/content/declaration_lessons')/(slug+'.json')
new(pp,dict(schema_version=1,items=[item]));new(lp,dict(schema_version=1,units=[unit]))
pub.inputs.cache_clear();pub.load.cache_clear()
lean=load(r/'anonymous.lean-context73.json')
lean.update(declaration=decl,file=file,formalizer='root-samplinglib-writer',compiler_evidence=freeze['compiled'][0]['focused_receipt']['path'])
lean['statement_representation']=dict(kind='exact-literal-private-Prop-expansion',
    actual_header=s[s.index('theorem actual_harmonic_flow_laws'):body].rstrip()+'\n',
    private_definition=s[s.index('private def actual_harmonic_flow_statement'):s.index('theorem actual_harmonic_flow_laws')].rstrip()+'\n',
    expanded_header=(r/'expanded73.frozen.header.lean').read_text(encoding='utf8'),
    source_approved_overlay=(pre/'root.statement-seal73.json').as_posix(),kernel_header_and_literal_expansion_checked=True)
original=source['attribution']+'\n'+statement+'\n'+source['anchor']
audit=dict(id=aid,state='draft',source=dict(source_id='companion-domain:'+slug,anchor=source['anchor'],url=source['url'],original_text=original,text_sha256=sha(original.encode())),
    lean=lean,source_review=dict(state='pending'),repairs=[],publication_binding_sha256=pub.binding_digest(item,item['bindings'][0],pub.inputs()),publication_context=pub.review_context(item,item['bindings'][0],pub.inputs()))
assert rt.decoder_packet(audit)==load(r/'anonymous.decoder.json')
ap=Path('research-wiki/semantic-roundtrip/audits')/(aid+'.json');new(ap,audit)
new(r/'publication-plan.json',dict(slugs=[slug],audit_ids=[aid],mathematical_declarations=[decl],active_cells=[cid],remaining_boundary=boundary,literal_statement_helpers=unit['helpers'],formula_proof_steps=[len(steps)],source_graph_and_lean_graph_distinct=True,no_fake_consumer=True))
new(r/'publication-freeze73.json',dict(status='DRAFT_BEFORE_WHOLE_INDEPENDENT_SOURCE_REVIEW',actual_root_PID=os.getpid(),
    mathematics_freeze=pin(r/'mathematics-freeze73.json'),inputs=[pin(x) for x in [pp,lp,ap,cp]],source_review=False,VERIFIED=False,PROVED_LOCAL=False))
adv.checkpoint_advance(claim['advance_id'],worker_id=claim['created_by'],route_fingerprint='literal-harmonic/gradient-continuity/trig-group-deriv/weighted-sum',progress_signature='178lines-2523jobs-EXIT0-standard3-sixBODYformulaSteps',mathematical_delta=claim['theorem_delta'],exact_residual=boundary)
pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance([decl],reviewed=False)
print('PASS draft73:one actual deterministic theorem,unchanged anonymous packet,six exact formula/BODY steps; no PROVED_LOCAL or VERIFIED.')
