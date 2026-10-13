from pathlib import Path
import json, hashlib, sys, copy
root=Path.cwd(); r=Path(__file__).parent; pre=r.parent/'pbps-phase-reversal-volume-preread96'
sys.path.insert(0,str(root/'tools'))
import astis_semantic_roundtrip as rt
import astis_publication as pub
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,x):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def fresh(p,x):
    assert not p.exists(),p
    save(p,x)
def pin(p):
    p=Path(p);b=p.read_bytes()
    return dict(path=p.as_posix(),raw_sha256=sha(b),bytes=len(b))
claim=load(r/'claim.json');decl=claim['target_declarations'][0];file=claim['proposed_files'][0];cid=claim['frontier_cell']
module=Path(file);s=module.read_text(encoding='utf8');raw=module.read_bytes()
assert sha(raw)=='4b144dfa25d9521803e37518b8a6386fff08396c5804e410e9be593d46833a7b'
receipt=r/'checks96/exact-sealed-kernel/receipt.json';assert load(receipt)['exit_code']==0
literal=s.split('private def actual_phase_reversal_volume_statement',1)[1].split('\nvariable {E :',1)[0].strip()
seal=load(pre/'root.statement-seal96.json');assert literal==seal['expanded_literal_Prop'].strip()
binders,body=literal.split(' : Prop :=\n',1);statement_lean=binders+' :\n'+body
restatement='''Let E be a finite-dimensional real inner-product space equipped with its Borel sigma algebra, including dimension zero. Let V:E->R, alpha,beta>=0 and eta in R. Assume alpha>0, alpha<=beta, V is C2, alpha||v||^2<=D2V(x)[v,v]<=beta||v||^2 for every x,v in E, eta>0 and beta*eta<=1. These are the six original analytic assumptions; there is no supplied volume, measurability, inverse-map or integral identity premise.
For every y,r in E put c(y,r)=y-eta grad V(r), h(r,x)=grad V(x)-grad V(r), B(n,p)=p-(2<p,n>/||n||^2)n and S_r(x,p)=(x,B(h(r,x),p)). Put R(x,p)=(x,-p) and
Phi_(y,r,u)(x,p)=(c+cos(u)(x-c)+sqrt(eta)sin(u)p, -sin(u)/sqrt(eta)(x-c)+cos(u)p),
lambda_r(x,p)=sqrt(eta)max(0,<p,h(r,x)>), ell=volume_E tensor volume_E.
Volume_E is the canonical Hilbert-space Lebesgue/Haar volume. Division by zero in B is totalized by zero, hence B(0,p)=p; no nonzero-normal hypothesis is imposed.
The map ((y,r),(u,z))->Phi_(y,r,u)(z) is jointly Borel measurable on (E x E) x R x (E x E); (r,z)->S_r(z) and (r,z)->lambda_r(z) are jointly Borel measurable. For every y,r,u, Phi_(y,r,u) preserves ell. For every r, S_r preserves ell, and R preserves ell. Preservation means a measurable map whose pushforward of ell equals ell.
For every y,r,u,z, both Phi_(y,r,-u)(Phi_(y,r,u)(z))=z and Phi_(y,r,u)(Phi_(y,r,-u)(z))=z. For every r,z, S_r(S_r(z))=z; for every z, R(R(z))=z. For every y,r,u,z, R(Phi_(y,r,u)(R(z)))=Phi_(y,r,-u)(z). For every r,z, R(S_r(z))=S_r(R(z)) and lambda_r(R(S_r(z)))=lambda_r(z).
Finally, for every r and real-valued F on E x E that is Bochner integrable with respect to ell, F composed with S_r is ell-integrable and integral F(S_r(z)) d ell(z)=integral F(z) d ell(z).
These assertions include all real times u, zero normals and rank zero. They assert phase product-volume preservation, not preservation of the unscaled phase-space norm. The real integrable-test clause is the A6 change-of-variables consequence. The elementary phase reversal laws supply dependencies for later prescribed-path reversal; they assert no pointwise reversal of a right-continuous path at its jumps, no stationary/Gibbs invariant law, Markov semigroup, hypocoercivity, implementation error, expected oracle cost, main sampling theorem or actual-input composition.'''
attribution='Chen, Chewi, Lu and Zhang, arXiv:2609.06905v1, Appendix A.1, harmonic flow, (A.5), (A.6) and elementary dependencies of (A.8); complete attributed mathematical restatement with explicit ASTIS Borel/product-volume and zero-case completion, not verbatim source text.'
context=[
 'The ambient norm and inner product are real; gradient and fderiv denote Hilbert gradient and Frechet derivative. The ambient measurable structure is its Borel sigma algebra.',
 'volume on a finite-dimensional real inner-product space is its canonical Hilbert-space Lebesgue measure, and Measure.prod is product measure. MeasurePreserving f mu nu means f is measurable and its pushforward sends mu to nu.',
 'Real division by zero equals zero. Smul denotes scalar multiplication. The real square root is the nonnegative one. Finite-dimensional spaces include dimension zero.',
 'Integrable is Bochner integrability; for real functions it includes absolute integrability and almost-everywhere strong measurability. All quantifiers have their displayed scope, and real time ranges over the whole real line.'
]
aid='ASTIS-RT-20261011-PBPSActualPhaseReversalVolume';slug='pbps-actual-phase-reversal-volume';title='Actual PBPS phase-volume preservation and reversal'
audit=dict(id=aid,state='draft',source=dict(source_id='companion-domain:'+slug,anchor=claim['source_anchor'],url='https://arxiv.org/html/2609.06905v1#A1.E6',original_text=restatement,text_sha256=sha(restatement.encode())),lean=dict(statement=statement_lean.strip(),statement_sha256=sha(statement_lean.strip().encode()),compiled=True,decoder_context=context,declaration=decl,file=file,formalizer='companion_root_20261005',compiler_evidence=receipt.as_posix()),source_review=dict(state='pending'),repairs=[])
ap=Path('research-wiki/semantic-roundtrip/audits')/f'{aid}.json';fresh(ap,audit)
packet=rt.decoder_packet(audit);out=Path('runs/semantic-roundtrip/anonymous96/input.json');fresh(out,packet)
fresh(r/'authored-statement96.json',dict(statement=restatement,attribution=attribution))
cp=Path('research-wiki/frontier-cells')/f'{cid}.json';cell=load(cp);parents=cell['parents']
cell['evidence']['whole_target_compiled']=pin(module);cell['evidence']['focused_checks']=[receipt.as_posix(),(r/'checks96/production-build/receipt.json').as_posix()]
cell['blocked']['reason']='Full frozen theorem and literal-kernel test passed; independent mathematics, blind decoding, source and exposition review pending.'
cell['purification']['dead_code_audit']='Eight private mathematical helpers are consumed by the public proof through reflection and harmonic affine volume preservation. Postmerge purification pending.'
mirror=dict(status='none-found',reason='Uses existing Haar translation, skew-product disintegration and isometry-volume mechanisms; no new cross-domain transport is introduced.')
cell['conceptual_mirror_audit']=mirror
save(cp,cell)
def step(title,text,formula,start,end):
    a=s.index(start);b=s.index(end,a);code=s[a:b]
    return dict(title=title,text=text,formula=formula,lean=code,detail='Exact compiled proof region; all private volume and algebra premises are discharged internally in the public theorem.',lean_source_region=dict(path=file,source_raw_sha256=sha(raw),start_line=s[:a].count('\n')+1,end_line=s[:b].count('\n'),exact_code_raw_sha256=sha(code.encode())))
steps=[
 step('Preserve product volume under elementary shears',
 'For L_a(x,p)=(x,p+a x), each fixed-x momentum map is a translation and preserves volume_E. Joint measurability and the skew-product theorem therefore preserve ell. Swapping coordinates before and after L_a gives U_a(x,p)=(x+a p,p), also volume preserving. Negation on both coordinates is a product of linear isometries, so it preserves ell as well. These are the elementary maps used below.',r'L_a(x,p)=(x,p+ax),\quad U_a(x,p)=(x+ap,p),\quad (L_a)_\#\ell=(U_a)_\#\ell=\ell.', 'private theorem lower_shear','private theorem reflect_fiber'),
 step('Identify every bounce fiber with an orthogonal reflection',
 'For fixed n, the literal formula B(n,p) equals reflection in the orthogonal complement of span(n). In finite dimension this reflection is a linear isometry equivalence, hence preserves canonical volume_E. If n=0, its orthogonal complement is all E and the formula is the identity, so this proof requires no division by a nonzero norm. This is a fiber statement; joint Borel measurability of the state-dependent bounce is supplied separately by the verified bounce theorem.',r'B(n,p)=\operatorname{refl}_{(\mathbb R n)^\perp}(p),\qquad B(n,\cdot)_\#\operatorname{vol}_E=\operatorname{vol}_E.', 'private theorem reflect_fiber','private theorem area_matrix'),
 step('Factor the linear harmonic matrix into three shears',
 'Suppose a^2-bc=1 and 1+a is nonzero. Set k=b/(1+a). The determinant identity gives ck=a-1, while k(1+a)=b. Expanding U_k composed with L_c composed with U_k gives diagonal coefficients 1+ck=a and upper-right coefficient 2k+k^2 c=k(1+a)=b; its lower-left coefficient is c. Composition of these three preserved-volume maps proves the matrix map preserves ell, without choosing coordinates or assuming positive dimension.',r'\begin{pmatrix}a&b\\c&a\end{pmatrix}=U_k L_c U_k,\quad k=\frac b{1+a},\quad ck=a-1.', 'private theorem area_matrix','private theorem harmonic_linear'),
 step('Cover every harmonic time and restore the center',
 'Use a=cos(u), b=sqrt(eta)sin(u), c=-sin(u)/sqrt(eta). Since eta>0, sqrt(eta) is nonzero, and sin^2(u)+cos^2(u)=1 gives a^2-bc=1. If 1+cos(u) is nonzero, apply the shear factorization. Otherwise cos(u)=-1 and the same trigonometric identity forces sin(u)=0, so the linear map is simultaneous negation. Finally translate x by minus the center, apply the linear map, and translate back. Position translations preserve ell, giving the exact affine Phi for all u.',r'\Phi_u=T_d\circ\begin{pmatrix}\cos u&\sqrt\eta\sin u\\-\sin u/\sqrt\eta&\cos u\end{pmatrix}\circ T_{-d},\qquad (\Phi_u)_\#\ell=\ell.', 'private theorem harmonic_linear','\ntheorem actual_phase_reversal_volume_laws'),
 step('Assemble actual joint Borel maps and phase-volume laws',
 'Reuse the verified actual harmonic-flow theorem for joint Borel measurability and both inverse-flow identities, and the actual bounce theorem for joint Borel rate/bounce maps and the bounce involution. For each fixed reference r, combine measurable S_r with volume preservation of its momentum reflection at every x through the skew-product theorem. This proves S_r preserves ell. Momentum reversal is identity on x times momentum negation and also preserves ell. The affine proof above supplies flow volume preservation.',r'(S_r)_\#\ell=R_\#\ell=(\Phi_{y,r,u})_\#\ell=\ell.', '  have hf :=','  · intro z\n    simp [R]'),
 step('Check reversal and rate pairing with the actual formulas',
 'Momentum negation is involutive. Substitute the flow formula and use cos(-u)=cos(u), sin(-u)=-sin(u) to obtain R Phi_u R=Phi_(-u). Reflection is linear in momentum, including n=0, so R S_r=S_r R. The verified reflection identity <B(n,p),n>=-<p,n> shows that the additional momentum negation in R S_r restores the inner product; applying the same positive-part rate formula gives lambda_r(R S_r z)=lambda_r(z). These are phase identities, not path reversal assertions at jump values.',r'R\Phi_u R=\Phi_{-u},\quad RS_r=S_rR,\quad \lambda_r(RS_r z)=\lambda_r(z).', '  · intro z\n    simp [R]','  · intro r F hF'),
 step('Derive the full real integrable-test identity',
 'Fix r and an ell-integrable real F. Measure preservation transports integrability to F composed with S_r. The measurable involution S_r is a measurable equivalence, and its pushforward identity supplies change of variables for the real integral. Thus both integrability and the exact A6 equality follow from the proved phase map. Integrability of F specifies the test class; volume preservation and invertibility are conclusions already proved inside this theorem.',r'F\in L^1(\ell)\Longrightarrow F\circ S_r\in L^1(\ell),\qquad\int F(S_rz)\,d\ell(z)=\int F(z)\,d\ell(z).', '  · intro r F hF','\nend\nend AutoSamplingTheory')
]
assumptions=['Finite-dimensional real inner-product Borel E, including rank zero.','alpha,beta>=0; alpha>0; alpha<=beta; V is C2; alpha||v||^2<=D2V(x)[v,v]<=beta||v||^2 for every x,v; eta>0; beta*eta<=1.','All y,r in E and all real times u; all phase points, including zero reflection normals.','A6 test class: each real F is Bochner integrable against the explicitly defined product volume ell.','Measurability, volume preservation, inverse identities and integrability after bounce are proved conclusions, not supplied provider assumptions.']
source=dict(url=audit['source']['url'],edition='arXiv2609.06905v1',anchor=claim['source_anchor'],wording_status='faithful paraphrase',attribution=attribution)
deltas=[dict(source='A6 bounce change of variables and harmonic flow/reversal mechanics.',lean='Explicit product-volume preservation, joint Borel maps, phase inverses and real integrable-test identity.',classification='source-implicit',reason='ASTIS expands implicit measurability and zero-case obligations; no additional provider assumption.'),dict(source='Finite-dimensional Euclidean phase calculations.',lean='Finite-dimensional real Hilbert Borel E, including rank zero; exact sqrt(eta) scaling and literal reflection.',classification='generalization',reason='Coordinate-free equivalent mechanism; rank zero and zero normals covered.'),dict(source='Original analytic assumptions for the sampler.',lean='All six assumptions retained; individual algebra/volume identities need fewer assumptions.',classification='same',reason='No assertion of necessity of every assumption; existing actual parents reused.'),dict(source='Later stationary path reversal and main sampling results.',lean='Only elementary phase-volume/reversal identities.',classification='unresolved',reason='Prescribed endpoint/time reversal, stationary averaging, invariance, Markovness, errors, costs and composition remain separate obligations.')]
item=dict(id=slug,library='pbps',chapter='pbps-01',chapter_path='example-cases/samplewiki/companions/proximal-bouncy-particle.html',title=title,source=source,statement=restatement,assumptions=assumptions,formulae=[dict(label='Phase product-volume and reversal',tex=steps[4]['formula']),dict(label='Bounce change of variables',tex=steps[-1]['formula'])],obligations=[dict(id='phase-volume-reversal',label='Actual phase-volume preservation and elementary reversal'),dict(id='stationary-path-reversal',label='A8 prescribed endpoint/time reversal and stationary averaging')],bindings=[dict(declaration=decl,cell=cid,role='proof-edge',supports=['phase-volume-reversal'],audit_id=aid,boundary=claim['truth_boundary'],assumption_deltas=deltas)])
for key in ['declaration_level','statement_seal','source_proof_coverage','proof_digestion','purification']:item[key]=copy.deepcopy(cell[key])
unit=dict(kind='theorem',declaration=decl,title=title,sources=[dict(url=source['url'],label=source['anchor'],scope=claim['truth_boundary'])],tests=claim['focused_checks'],assumptions=assumptions,statement=restatement,formula=steps[4]['formula'],boundary=claim['truth_boundary'],steps=steps,lean_statement=restatement,lean_proof='; '.join(x['title'] for x in steps),helpers=[decl.rsplit('.',1)[0]+'.actual_phase_reversal_volume_statement'],astis_dependencies=parents,mathlib_dependencies=['MeasurePreserving.skew_product','MeasurePreserving.prod','MeasurePreserving.comp','Measure.measurePreserving_swap','measurePreserving_add_left','measurePreserving_add_right','LinearIsometryEquiv.measurePreserving','Submodule.reflection_orthogonal_apply','Submodule.reflection_singleton_apply','MeasurePreserving.integrable_comp_of_integrable','MeasurableEquiv.ofInvolutive','MeasurePreserving.integral_comp'])
pp=Path('website/content/publications')/f'{slug}.json';lp=Path('website/content/declaration_lessons')/f'{slug}.json';fresh(pp,dict(schema_version=1,items=[item]));fresh(lp,dict(schema_version=1,units=[unit]))
pub.inputs.cache_clear();pub.load.cache_clear();audit['publication_binding_sha256']=pub.binding_digest(item,item['bindings'][0],pub.inputs());audit['publication_context']=pub.review_context(item,item['bindings'][0],pub.inputs())
start=s.index('theorem actual_phase_reversal_volume_laws');stop=s.index(':= by\n',start)
audit['lean']['statement_representation']=dict(kind='exact-literal-Prop-expansion',actual_header=s[start:stop],private_definition='def actual_phase_reversal_volume_statement'+literal,expanded_header='theorem actual_phase_reversal_volume_laws'+statement_lean,source_approved_overlay=(pre/'root.statement-seal96.json').as_posix(),kernel_header_and_literal_expansion_checked=True)
assert rt.decoder_packet(audit)==packet;save(ap,audit)
fresh(r/'publication-freeze96.json',dict(status='DRAFT_PENDING_INDEPENDENT_MATH_DECODER_SOURCE_EXPOSITION',module=pin(module),inputs=[pin(x) for x in [pp,lp,ap]],packet=pin(out),canonical_packet_sha256=packet['packet_sha256'],steps=len(steps),conceptual_mirror_audit=mirror,PROVED_LOCAL=False,VERIFIED=False))
pub.check_advance([decl],reviewed=False)
print(json.dumps(dict(packet=pin(out),steps=len(steps),publication_binding_sha256=audit['publication_binding_sha256'])))
