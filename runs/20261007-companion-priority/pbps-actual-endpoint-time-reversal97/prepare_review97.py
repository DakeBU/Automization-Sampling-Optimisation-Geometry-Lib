from pathlib import Path
import json, hashlib, sys, copy
root=Path.cwd(); r=Path(__file__).parent; pre=r.parent/'pbps-endpoint-time-reversal-preread97'
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
receipt=r/'focused97/production2/receipt.json';check=load(receipt)
assert check['exit_code']==0 and check['input_raw_sha256']==sha(raw)
literal=s.split('private def actual_endpoint_time_reversal_statement',1)[1].split('\n/-- Exact source-sealed',1)[0].strip()
seal=load(pre/'root.statement-seal97.json');assert literal==seal['expanded_literal_Prop'].strip()
binders,body=literal.split(' : Prop :=',1);statement_lean=binders+' :'+body
restatement='''Let E be a finite-dimensional real inner-product space with its Borel sigma algebra, including dimension zero. Let V:E->R, alpha,beta>=0 and eta in R. Assume alpha>0, alpha<=beta, V is C2, alpha||v||^2<=D2V(x)[v,v]<=beta||v||^2 for every x,v in E, eta>0 and beta*eta<=1.
For y,r in E put c=y-eta grad V(r), h_r(x)=grad V(x)-grad V(r), R(x,p)=(x,-p),
Phi_(y,r,u)(x,p)=(c+cos(u)(x-c)+sqrt(eta)sin(u)p, -sin(u)/sqrt(eta)(x-c)+cos(u)p),
S_r(x,p)=(x,p-(2<p,h_r(x)>/||h_r(x)||^2)h_r(x)). Real division by zero is zero, so a zero normal gives the identity bounce. Let ell=volume_E tensor volume_E, with canonical Hilbert-space Lebesgue measure.
For every integer n>=0 and horizon T>=0, let Delta_n(T) consist of real tuples 0<t_0<...<t_(n-1)<T. Equivalently, prepending 0 produces a strictly increasing tuple and every entry is less than T. Let Prefix_n(T) be this subtype and m_n,T the comap of Lebesgue measure on R^n under its inclusion. This is unnormalized simplex volume. For n=0 the tuple is empty and its zero-dimensional volume is one; for T=0 and n>0 the subtype is empty.
Write q_0=0 and q_(j+1)=t_j. Starting at z_0=z, define z_(j+1)=S_r(Phi_(y,r,t_j-q_j)(z_j)) for 0<=j<n. Define records K_j=(q_j,z_j), each embedded in the live branch of (R_nonnegative x (E x E)) plus a cemetery symbol. For a general history of n+1 such records, the path reconstruction Psi at s in [0,T] starts from z and visits records in increasing index order: a live record (a,w) replaces the accumulator by Phi_(y,r,s-a)(w) exactly when a<=s; future records and cemetery records leave it unchanged. Here s-a is nonnegative subtraction. Define Gamma_(y,r,z,t)=Psi(K), the actual finite prescribed path; thus its value at an event is the post-bounce value. Let A_(y,r)(z,t)=Gamma_(y,r,z,t)(T).
There exists rho:Prefix_n(T)->Prefix_n(T) with (rho t)_i=T-t_(n-1-i) for every i. It is Borel measurable, involutive, and preserves m_n,T. For all y,r,z,t, the terminal identity is A_(y,r)(z,t)=Phi_(y,r,T-q_n)(z_n). The map (y,r,z,t)->A_(y,r)(z,t) is jointly Borel measurable. For each y,r,t, z->A_(y,r)(z,t) preserves ell. The reversed endpoint satisfies A_(y,r)(R(A_(y,r)(z,t)),rho t)=R(z).
Define Theta_(y,r)(z,t)=(R(A_(y,r)(z,t)),rho t). The map (y,r,z,t)->Theta_(y,r)(z,t) is jointly Borel measurable. For each y,r, Theta_(y,r) is an involution and preserves ell tensor m_n,T, in phase-first order. Every measure-preservation assertion includes measurability and equality of pushforward measures. All conclusions include n=0, T=0, zero reflection normals and rank-zero E; measurability, inverses, sigma finiteness and volume identities are proved internally from the six analytic assumptions.
This is the finite prescribed endpoint/time change of variables used in the Appendix A.1 reversal argument. It does not assert pointwise time reversal of right-continuous paths at event times. Gibbs-weight balance, stationary averaging and invariant probability laws, Markov properties, hypocoercivity, implementation error, expected oracle costs, main sampling results and actual-input composition remain separate obligations.'''
attribution='Chen, Chewi, Lu and Zhang, arXiv:2609.06905v1, Appendix A.1, endpoint/time substitution surrounding (A.8). Complete attributed ASTIS mathematical restatement with explicit finite-word, Borel, simplex-comap and product-volume completion; not verbatim source text and not the full weighted stationary identity.'
context=[
 'The real Hilbert gradient and Frechet derivative are gradient and fderiv. All measurable spaces on the ambient finite-dimensional real inner-product space are its Borel structure.',
 'volume is canonical Hilbert-space Lebesgue measure. Measure.prod is product measure. Measure.comap under a measurable subtype inclusion gives the subtype measure. MeasurePreserving includes measurability and equality of pushforward measures.',
 'Fin n indexes n coordinates from zero. Fin.cons prepends a coordinate. Fin.rev reverses the index order. Fin.induction is recursion on this finite index, and Fin.foldl applies updates in increasing index order.',
 'Real division by zero equals zero. Real.toNNReal is the nonnegative part. Subtraction in the nonnegative reals is truncated at zero. Sum.inl is the live-record constructor; the other summand has one cemetery value.',
 'A function-valued path has the product measurable structure, and its argument subtype is the closed interval from zero to the displayed horizon. Function.Involutive means composing the map with itself gives the identity. The zero-coordinate tuple is unique.'
]
aid='ASTIS-RT-20261012-PBPSActualEndpointTimeReversal';slug='pbps-actual-endpoint-time-reversal';title='Actual PBPS finite endpoint and event-time reversal'
audit=dict(id=aid,state='draft',source=dict(source_id='companion-domain:'+slug,anchor=claim['source_anchor'],url='https://arxiv.org/html/2609.06905v1#A1.E8',original_text=restatement,text_sha256=sha(restatement.encode())),lean=dict(statement=statement_lean.strip(),statement_sha256=sha(statement_lean.strip().encode()),compiled=True,decoder_context=context,declaration=decl,file=file,formalizer='companion_root_20261005',compiler_evidence=receipt.as_posix()),source_review=dict(state='pending'),repairs=[])
ap=Path('research-wiki/semantic-roundtrip/audits')/f'{aid}.json';fresh(ap,audit)
packet=rt.decoder_packet(audit);out=Path('runs/semantic-roundtrip/anonymous97/input.json');fresh(out,packet)
fresh(r/'authored-statement97.json',dict(statement=restatement,attribution=attribution))
cp=Path('research-wiki/frontier-cells')/f'{cid}.json';cell=load(cp)
ordered='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOrderedPrefix.actual_ordered_prefix_law'
if ordered not in cell['parents']:cell['parents'].append(ordered)
parents=cell['parents'];cell['reuse_plan']['reused_declarations']=parents[:];cell['reuse_plan']['planned_dependencies']=[]
cell['proof_digestion']['existing_substrate']=parents[:]
cell['evidence']['whole_target_compiled']=pin(module);cell['evidence']['focused_checks']=[receipt.as_posix()]
cell['blocked']['reason']='Frozen full theorem compiled; independent whole mathematics, anonymous decoding, source and exposition reviews pending.'
cell['purification']['dead_code_audit']='Private simplex, finite-word and terminal-data helpers are consumed by the public theorem. Postmerge purification pending.'
cell['source_proof_coverage']['coverage_status']='Source-first graph and prospective coverage independently checked; compiled implementation awaits final source review.'
mirror=dict(status='none-found',reason='Finite-word cancellation and existing measure-preserving skew-product mechanisms are used within one actual PBPS endpoint construction. No new cross-domain transport with distinct consumers is claimed.')
cell['conceptual_mirror_audit']=mirror;save(cp,cell)
def step(title,text,formula,start,end):
    a=s.index(start);b=s.index(end,a);code=s[a:b]
    return dict(title=title,text=text,formula=formula,lean=code,detail='Exact compiled region. Generic internal premises are supplied by verified actual maps in the final assembly.',lean_source_region=dict(path=file,source_raw_sha256=sha(raw),start_line=s[:a].count('\n')+1,end_line=s[:b].count('\n'),exact_code_raw_sha256=sha(code.encode())))
steps=[
 step('Reverse the ordered time simplex',
 'Set rho(t)_i=T-t_(n-1-i). Reversal reverses index order and subtraction reverses inequalities, so strict ordering is preserved. The original upper bound gives positivity, and the original positivity gives the new upper bound T. Applying the formula twice restores every coordinate. On R^n this map is a coordinate permutation composed with coordinatewise reflection and translation, each preserving Lebesgue measure. Its invariant measurable simplex therefore inherits preservation of the exact comap measure m. This includes the unique empty tuple.',r'\rho(t)_i=T-t_{n-1-i},\quad \rho^2=\mathrm{id},\quad \rho_\#m_{n,T}=m_{n,T}.','private def delta','private theorem reverse_fold_cancel'),
 step('Cancel a finite reversed sequence',
 'For updates f_i and a map C satisfying f_i(C(f_i(x)))=C(x), process f_0 through f_(n-1), then apply C and process the updates in reverse order. Induction removes the outer matching pair and leaves C(x). A second finite induction identifies a fold with a prescribed sequence whenever its initial value and one-step recurrences agree. These algebraic statements will be applied to the actual flow and bounce.',r'f_i C f_i=C\ \Longrightarrow\ f_0\cdots f_{n-1}C f_{n-1}\cdots f_0=C.','private theorem reverse_fold_cancel','private def gaps'),
 step('Express the endpoint as a finite word of gaps',
 'Append T and prepend 0 to define gaps g_0=t_0, g_j=t_j-t_(j-1), g_n=T-t_(n-1). Reversing the tuple reverses the n+1 gaps exactly. The recursive post-bounce states give the terminal map Phi_(g_n) S Phi_(g_(n-1)) ... S Phi_(g_0). Equivalently start from S(z) and fold f_i=Phi_(g_i) composed with S through i=0,...,n. The first pair of bounces cancels because S is involutive. For n=0 this is just Phi_T(z).',r'g_i(\rho t)=g_{n-i}(t),\qquad A_t=\Phi_{g_n}S\Phi_{g_{n-1}}\cdots S\Phi_{g_0}.','private def gaps','private theorem endpoint_reversed'),
 step('Derive the inverse endpoint and its fiber volume',
 'Take C=S composed with R. The identities S^2=R^2=id, RS=SR and R Phi_u R=Phi_(-u), together with the inverse-flow law, imply f_i C f_i=C. Apply reversed-word cancellation and use the reversed-gap identity. The result is A_(rho t)(R A_t(z))=R(z). Separately, finite induction shows a composition of volume-preserving updates preserves volume; since S and each Phi_u preserve ell, so does A_t.',r'A_{\rho t}(R A_t(z))=Rz,\qquad (A_t)_\#\ell=\ell.','private theorem endpoint_reversed','private def endpoint_data_statement'),
 step('Connect the finite word to the actual path at T',
 'The verified ordered-prefix theorem supplies measurability of Delta. The verified finite-count path theorem supplies joint measurability of Gamma and its last-interval formula. Evaluating the measurable function-valued path at T preserves measurability. For n>0 the last event is strictly before T; for n=0 its grid point is zero and T>=0. There is no later record than the final index. Thus the interval formula yields Gamma(T)=Phi_(T-q_n)(z_n), exactly the finite word above. This connection uses the actual live/cemetery history and the original six analytic assumptions.',r'A_{y,r}(z,t)=\Gamma_{y,r,z,t}(T)=\Phi_{y,r,T-q_n}(z_n).','private def endpoint_data_statement','private def actual_endpoint_time_reversal_statement'),
 step('Assemble the jointly measurable preserving involution',
 'Reuse the actual phase-volume theorem for every flow, bounce and reversal identity; no such identity is an extra public premise. The terminal-data connection gives the measurable endpoint A and its fiber-volume and reversal laws. Hence Theta(z,t)=(R A_t(z),rho t) is jointly measurable and Theta^2(z,t)=(R R z,rho^2 t)=(z,t). The simplex inclusion pushes m to restricted ambient Lebesgue measure, establishing sigma finiteness. In time-first order, apply the measurable skew-product theorem to rho and the ell-preserving fibers z->R A_t(z); swap coordinates before and after to obtain preservation of ell tensor m in the stated phase-first order. This finishes the endpoint change of variables; weighting by Gibbs densities is a later edge.',r'\Theta^2=\mathrm{id},\qquad \Theta_\#(\ell\otimes m_{n,T})=\ell\otimes m_{n,T}.','theorem actual_endpoint_time_reversal_laws','\nend\nend AutoSamplingTheory')
]
assumptions=['Finite-dimensional real inner-product Borel E, including rank zero.','alpha,beta>=0; alpha>0; alpha<=beta; V is C2; alpha||v||^2<=D2V(x)[v,v]<=beta||v||^2 for all x,v; eta>0; beta*eta<=1.','All n>=0, T>=0, y,r,z and strictly ordered event tuples; zero events and zero normals are included.','The exact unnormalized simplex comap m and phase-first product ell tensor m are fixed definitions. Measurability, sigma finiteness, inverses and volume preservation are proved dependencies or conclusions.']
source=dict(url=audit['source']['url'],edition='arXiv2609.06905v1',anchor=claim['source_anchor'],wording_status='faithful paraphrase',attribution=attribution)
deltas=[dict(source='Endpoint/time substitution surrounding A8.',lean='Actual Gamma terminal evaluation and measurable preserving involution for exact simplex and phase volume.',classification='source-implicit',reason='Explicit ASTIS completion of finite-word cancellation, measurable maps and product-volume change of variables; no added premise.'),dict(source='Finite-dimensional Euclidean phase space.',lean='Finite-dimensional real Hilbert Borel space including rank zero.',classification='generalization',reason='Coordinate-free volume and inner-product formulation.'),dict(source='Original sampler assumptions.',lean='All six original analytic assumptions retained.',classification='same',reason='Actual verified parents discharge all internal provider premises.'),dict(source='Weighted stationary identity and subsequent invariance.',lean='Finite endpoint/time volume substitution only.',classification='unresolved',reason='Gibbs balance, stationary averaging and full invariant probability law remain separate obligations.')]
item=dict(id=slug,library='pbps',chapter='pbps-01',chapter_path='example-cases/samplewiki/companions/proximal-bouncy-particle.html',title=title,source=source,statement=restatement,assumptions=assumptions,formulae=[dict(label='Endpoint inverse',tex=steps[3]['formula']),dict(label='Joint change of variables',tex=steps[-1]['formula'])],obligations=[dict(id='endpoint-time-volume',label='Actual finite endpoint/time preserving involution'),dict(id='weighted-stationary-reversal',label='Gibbs-weighted sector reversal and stationary averaging')],bindings=[dict(declaration=decl,cell=cid,role='proof-edge',supports=['endpoint-time-volume'],audit_id=aid,boundary=claim['truth_boundary'],assumption_deltas=deltas)])
for key in ['declaration_level','statement_seal','source_proof_coverage','proof_digestion','purification']:item[key]=copy.deepcopy(cell[key])
unit=dict(kind='theorem',declaration=decl,title=title,sources=[dict(url=source['url'],label=source['anchor'],scope=claim['truth_boundary'])],tests=claim['focused_checks'],assumptions=assumptions,statement=restatement,formula=steps[-1]['formula'],boundary=claim['truth_boundary'],steps=steps,lean_statement=restatement,lean_proof='; '.join(x['title'] for x in steps),helpers=[decl.rsplit('.',1)[0]+'.actual_endpoint_time_reversal_statement'],astis_dependencies=parents,mathlib_dependencies=['MeasurePreserving.skew_product','MeasurePreserving.comp','MeasurePreserving.pi','Measure.measurePreserving_swap','MeasurableEquiv.piCongrLeft','map_comap_subtype_coe','measurePreserving_subtype_coe','SigmaFinite.of_map','Fin.foldl_rev','Fin.foldl_succ','Fin.foldr_succ'])
pp=Path('website/content/publications')/f'{slug}.json';lp=Path('website/content/declaration_lessons')/f'{slug}.json';fresh(pp,dict(schema_version=1,items=[item]));fresh(lp,dict(schema_version=1,units=[unit]))
pub.inputs.cache_clear();pub.load.cache_clear();audit['publication_binding_sha256']=pub.binding_digest(item,item['bindings'][0],pub.inputs());audit['publication_context']=pub.review_context(item,item['bindings'][0],pub.inputs())
start=s.index('theorem actual_endpoint_time_reversal_laws');stop=s.index(':= by\n',start)
audit['lean']['statement_representation']=dict(kind='exact-literal-Prop-expansion',actual_header=s[start:stop],private_definition='def actual_endpoint_time_reversal_statement'+literal,expanded_header='theorem actual_endpoint_time_reversal_laws'+statement_lean,source_approved_overlay=(pre/'root.statement-seal97.json').as_posix(),kernel_header_and_literal_expansion_checked=False)
assert rt.decoder_packet(audit)==packet;save(ap,audit)
fresh(r/'publication-freeze97.json',dict(status='DRAFT_PENDING_INDEPENDENT_MATH_DECODER_SOURCE_EXPOSITION',module=pin(module),inputs=[pin(x) for x in [pp,lp,ap]],packet=pin(out),canonical_packet_sha256=packet['packet_sha256'],steps=len(steps),conceptual_mirror_audit=mirror,PROVED_LOCAL=False,VERIFIED=False))
pub.check_advance([decl],reviewed=False)
print(json.dumps(dict(packet=pin(out),steps=len(steps),publication_binding_sha256=audit['publication_binding_sha256'])))
