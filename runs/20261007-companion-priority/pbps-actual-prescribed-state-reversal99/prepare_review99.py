from pathlib import Path
import copy,hashlib,json,sys
root=Path.cwd();r=Path(__file__).resolve().parent.relative_to(root.resolve());pre=r.parent/'pbps-finite-state-reversal-preread99'
sys.path.insert(0,str(root/'tools'))
import astis_semantic_roundtrip as rt
import astis_publication as pub
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,v):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def fresh(p,v):
 assert not p.exists(),p
 save(p,v)
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),raw_sha256=sha(b),bytes=len(b))
claim=load(r/'claim.json');decl=claim['target_declarations'][0];file=claim['proposed_files'][0];cid=claim['frontier_cell']
module=Path(file);s=module.read_text(encoding='utf8');raw=module.read_bytes();receipt=r/'focused99/production1/receipt.json'
check=load(receipt);assert check['exit_code']==0 and check['input_raw_sha256']==sha(raw)
literal=s.split('private def actual_prescribed_state_reversal_statement',1)[1].split('\ntheorem actual_prescribed_state_reversal_and_rate_product',1)[0].strip()
seal=load(pre/'root.statement-seal99.json');assert literal==seal['expanded_literal_Prop'].strip()
binders,body=literal.split(' : Prop :=',1);body=body.removeprefix(' by\n  classical\n  exact\n');statement_lean=binders+' :\n'+body
old=load(r.parent/'pbps-actual-endpoint-time-reversal97/authored-statement97.json')['statement']
restatement=old.split('There exists rho:')[0]+'''Define lambda_r(x,p)=sqrt(eta) max(0,<p,grad V(x)-grad V(r)>). For every finite n>=0 and T>=0 there exists rho:Prefix(n,T)->Prefix(n,T) with (rho(t))_i=T-t_(n-1-i). This witness is produced, not assumed. For every y,r,z and t in Prefix(n,T), form the grid a=(0,t_0,...,t_(n-1),T), indexed from0 through n+1. Set post_j=zAt(y,r,z,n,T,t,j) and arrive_j=Phi_(a_(j+1)-a_j)(post_j) for j=0,...,n. Set A=Gamma(y,r,z,n,T,t)(T), the actual terminal state. Form the reversed grid abar=(0,rho(t)_0,...,rho(t)_(n-1),T), set barPost_j=zAt(y,r,R(A),n,T,rho(t),j), and barArrive_j=Phi_(abar_(j+1)-abar_j)(barPost_j).
For every j=0,...,n, barPost_j=R(arrive_(n-j)) and barArrive_j=R(post_(n-j)). Moreover product over i=0,...,n-1 of lambda_r(barArrive_i) equals product over i=0,...,n-1 of lambda_r(arrive_i). The last arrival arrive_n is the actual terminal state and is not one of the n event-rate factors. Reversal on the n+1 arcs is j->n-j; reversal on the n events is i->n-1-i. Per-event rate equality is proved internally; the public conclusion exports the paired states and product equality.
The theorem covers n=0 (one flow arc and empty products equal1), T=0, rank-zero spaces, zero reflection normals and zero rates. No division by a rate or positivity of a prescribed event rate is assumed. The original six analytic assumptions are the only analytic premises; reversal identities, inverse maps, terminal identification and incoming-rate matching are derived from actual producers. The exact unnormalized simplex measure m is retained in the literal interface but is unused in these pointwise deterministic conclusions.
This is the finite-state and incoming-rate component of the Appendix A.1 reversal proof. At a genuine event the right-continuous post-event value reverses to the original incoming value, not the original post-event value. No equality of the two right-continuous trajectories at all times is claimed. Survival time substitution, weighted density equality, stationary invariance, restart/Markovness, hypocoercivity, implementation errors, actual expected costs, main results and PBPS/SPHMC composition remain separate.'''
attribution='Chen, Chewi, Lu and Zhang, arXiv:2609.06905v1, Appendix A.1 event convention, reversal algebra, (A.5) and (A.8). Complete attributed ASTIS mathematical restatement with explicit finite-state indexing; not verbatim text or a full invariance theorem.'
context=['The carrier is a finite-dimensional real inner-product space with Borel measurable structure; gradient and fderiv are the real Hilbert gradient and Frechet derivative.', 'Fin n indexes n coordinates from zero, and Fin.rev sends i to n-1-i. Fin.cons prepends and Fin.snoc appends; Fin.induction is finite recursion; Fin.foldl visits indices in increasing order.', 'Division by zero in the reals is zero. Real.toNNReal is the nonnegative part, and subtraction in nonnegative reals is truncated at zero. Sum.inl denotes a live record; Unit is a cemetery branch.', 'The path domain is the nonnegative closed-interval subtype. Measure.comap is the exact unnormalized subtype measure. Unused let definitions are not hypotheses.', 'Products over Fin0 are1. castSucc embeds Fin n in Fin(n+1) without changing the value; succ increases the value by one. The theorem uses both Fin n and Fin(n+1), with distinct reversal indices.']
aid='ASTIS-RT-20261012-PBPSActualPrescribedStateReversal';slug='pbps-actual-prescribed-state-reversal';title='Actual PBPS finite-state reversal and incoming-rate product'
audit=dict(id=aid,state='draft',source=dict(source_id='companion-domain:'+slug,anchor=claim['source_anchor'],url='https://arxiv.org/html/2609.06905v1#A1.E8',original_text=restatement,text_sha256=sha(restatement.encode())),lean=dict(statement=statement_lean.strip(),statement_sha256=sha(statement_lean.strip().encode()),compiled=True,decoder_context=context,declaration=decl,file=file,formalizer='companion_root_20261005',compiler_evidence=receipt.as_posix()),source_review=dict(state='pending'),repairs=[])
ap=Path('research-wiki/semantic-roundtrip/audits')/f'{aid}.json';fresh(ap,audit)
packet=rt.decoder_packet(audit);out=Path('runs/semantic-roundtrip/anonymous99/input.json');fresh(out,packet)
fresh(r/'authored-statement99.json',dict(statement=restatement,attribution=attribution))
cp=Path('research-wiki/frontier-cells')/f'{cid}.json';cell=load(cp);parents=cell['parents']
cell['evidence']['whole_target_compiled']=pin(module);cell['evidence']['focused_checks']=[receipt.as_posix()]
cell['blocked']['reason']='Full sealed actual target compiles; independent whole math, anonymous decoding and source/exposition reviews pending.'
cell['purification']['dead_code_audit']='Three private helpers are consumed: finite state induction, incoming-rate product and actual grid coordinate adapter. Public97 terminal/time and96 reversal/rate projections discharge the helper premises. No mangled private API used.'
save(cp,cell)
def step(title,text,formula,start,end):
 a=s.index(start);b=s.index(end,a);code=s[a:b]
 return dict(title=title,text=text,formula=formula,lean=code,detail='Exact compiled region; private helper premises are discharged by actual96/97 and literal recursion in the public proof.',lean_source_region=dict(path=file,source_raw_sha256=sha(raw),start_line=s[:a].count('\n')+1,end_line=s[:b].count('\n'),exact_code_raw_sha256=sha(code.encode())))
steps=[
 step('Reverse each finite incoming and post-event state',
 'The private finite-array lemma first combines momentum reversal with the inverse flow to obtain Phi_u(R(Phi_u q))=R q. The reversed initial state is the reversal of the final arrival. Induct over reversed events. The flow identity turns the paired reversed post-state into the reversal of the original post-state. The next reversed bounce is S R S applied to the original arrival, which equals R because S is involutive and commutes with R. The Fin casts convert arc reversal into event reversal exactly. These algebraic premises are internal and are supplied by actual PBPS laws below.',
 r'\bar z_j=R w_{n-j}\quad\Longrightarrow\quad\bar w_j=R z_{n-j},\qquad SRS=R.',
 'private theorem finite_state_reversal','private theorem incoming_rate_product'),
 step('Pair incoming event rates and permute the finite product',
 'At reversed event i, the state identity gives barArrive_i=R(post_(n-i))=R(S(arrive_(n-1-i))). The actual rate identity lambda(R S q)=lambda(q) pairs the corresponding incoming rates. Apply the permutation Fin.rev to reindex the product. No factor is cancelled, so zero rates are included; with no events both products are1. The individual rate pairing is an internal step, while the public result exposes the product.',
 r'\lambda_r(\bar w_i)=\lambda_r(RS_r w_{n-1-i})=\lambda_r(w_{n-1-i}),\qquad\prod_{i<n}\lambda_r(\bar w_i)=\prod_{i<n}\lambda_r(w_i).',
 'private theorem incoming_rate_product','private theorem reversed_grid_gaps'),
 step('Match the lengths of reversed flow arcs',
 'Prepend zero and append T to both event tuples. The coordinate equation rho(t)_i=T-t_(n-1-i) gives abar_j=T-a_(n+1-j) and abar_(j+1)=T-a_(n-j). Subtract to obtain the original arc length at index n-j. The first and last grid entries are checked separately by finite cases, so the one-arc n=0 case remains valid. This is an adapter for the actual grid representation; it invokes no private declaration from another module.',
 r'\bar a_{j+1}-\bar a_j=a_{n+1-j}-a_{n-j}.',
 'private theorem reversed_grid_gaps','set_option linter.unusedVariables false in'),
 step('Obtain actual reversal maps and the actual terminal state',
 'Apply the verified actual endpoint/time theorem to obtain rho, its coordinate formula and A=Phi_(T-a_n)(z_n). Apply the actual phase-reversal theorem to obtain both flow inverses, the involutions S and R, their commutation and lambda(R S q)=lambda(q). Introduce the literal actual post/arrival arrays and use the grid adapter to identify every reverse arc length. Nothing is supplied as an extra theorem hypothesis.',
 r'\rho(t)_i=T-t_{n-1-i},\qquad A=\Gamma(T)=\Phi_{T-a_n}(z_n).',
 'theorem actual_prescribed_state_reversal_and_rate_product','  have hp ('),
 step('Discharge every finite-array premise from the actual recursion',
 'Unfold the actual finite state recursion at successor indices. It gives post_(i+1)=S(arrive_i) and barPost_(i+1)=S(barArrive_i). Replace the reversed arc length by the matched original length. The actual terminal formula identifies the reversed initial state R(A) with R(arrive_n). Thus the private induction receives proved actual recurrences and endpoint data, including all zero cases.',
 r'z_{i+1}=S_r w_i,\quad\bar z_{i+1}=S_r\bar w_i,\quad\bar z_0=R A=R w_n.',
 '  have hp (','  have hstates :='),
 step('Assemble the actual state and incoming-product conclusions',
 'Invoke finite state reversal with the actual harmonic flow, bounce, momentum reversal and proved recurrences. Re-express its reversed-length flow as the literal barArrive array using the grid identity. This proves both state equalities. Supply the actual rate identity and state equalities to the finite-product lemma to obtain the product conclusion. The proof keeps incoming and post-event states separate; path reversal away from events and survival-integral substitution are later dependencies.',
 r'\bar z_j=R w_{n-j},\qquad\bar w_j=R z_{n-j},\qquad\prod_{i<n}\lambda_r(\bar w_i)=\prod_{i<n}\lambda_r(w_i).',
 '  have hstates :=','\n#print axioms')]
assumptions=['Finite-dimensional real inner-product Borel E, including rank zero.','alpha,beta>=0; alpha>0; alpha<=beta; V is C2; alpha||v||^2<=D2V(x)[v,v]<=beta||v||^2 for every x,v; eta>0; beta*eta<=1.','Every finite n>=0 and T>=0; rho is produced on the strict prescribed-event subtype, then every y,r,z,t is quantified. No positive rate or nonzero-normal condition.','Literal actual flow, zero-safe reflection, finite recursion, interpolated path, endpoint, momentum reversal and rate; no supplied reversal or inverse-map premise.']
source=dict(url=audit['source']['url'],edition='arXiv2609.06905v1',anchor=claim['source_anchor'],wording_status='faithful paraphrase',attribution=attribution)
deltas=[dict(source='A5/A8 finite incoming-state reversal.',lean='Both actual intermediate post/arrival equalities and incoming-rate product.',classification='source-implicit',reason='Explicit finite grid/recursion proof discharges actual producer conditions.'),dict(source='Finite Euclidean phase.',lean='Finite real Hilbert Borel E, including rank zero.',classification='generalization',reason='Coordinate-free source formulation.'),dict(source='Original sampler assumptions.',lean='All six analytic assumptions retained with no excess binder.',classification='same',reason='Flow inverses, reflection laws and terminal data are internal proved dependencies.'),dict(source='Printed path reversal notation at jumps and full invariant law.',lean='Separate incoming/post arrays; no all-time right-continuous equality or full invariance.',classification='unresolved',reason=claim['truth_boundary'])]
item=dict(id=slug,library='pbps',chapter='pbps-01',chapter_path='example-cases/samplewiki/companions/proximal-bouncy-particle.html',title=title,source=source,statement=restatement,assumptions=assumptions,formulae=[dict(label='Actual state reversal and incoming-rate product',tex=steps[-1]['formula'])],obligations=[dict(id='finite-state-rate-reversal',label='Actual intermediate state reversal and rate-product equality'),dict(id='weighted-invariance',label='Survival time substitution, weighted reversal and invariant probability')],bindings=[dict(declaration=decl,cell=cid,role='proof-edge',supports=['finite-state-rate-reversal'],audit_id=aid,boundary=claim['truth_boundary'],assumption_deltas=deltas)])
for key in ['declaration_level','statement_seal','source_proof_coverage','proof_digestion','purification']:item[key]=copy.deepcopy(cell[key])
unit=dict(kind='theorem',declaration=decl,title=title,sources=[dict(url=source['url'],label=source['anchor'],scope=claim['truth_boundary'])],tests=claim['focused_checks'],assumptions=assumptions,statement=restatement,formula=steps[-1]['formula'],boundary=claim['truth_boundary'],steps=steps,lean_statement=restatement,lean_proof='; '.join(x['title'] for x in steps),helpers=[decl.rsplit('.',1)[0]+'.actual_prescribed_state_reversal_statement'],astis_dependencies=parents,mathlib_dependencies=['Fin.induction','Fin.induction_succ','Fin.rev_castSucc','Fin.rev_succ','Fin.snoc_castSucc','Fin.cons_succ','Fin.revPerm','Equiv.prod_comp'])
pp=Path('website/content/publications')/f'{slug}.json';lp=Path('website/content/declaration_lessons')/f'{slug}.json';fresh(pp,dict(schema_version=1,items=[item]));fresh(lp,dict(schema_version=1,units=[unit]))
pub.inputs.cache_clear();pub.load.cache_clear();audit['publication_binding_sha256']=pub.binding_digest(item,item['bindings'][0],pub.inputs());audit['publication_context']=pub.review_context(item,item['bindings'][0],pub.inputs())
start=s.index('theorem actual_prescribed_state_reversal_and_rate_product');stop=s.index(':= by\n',start)
audit['lean']['statement_representation']=dict(kind='exact-literal-Prop-expansion',actual_header=s[start:stop],private_definition='def actual_prescribed_state_reversal_statement'+literal,expanded_header='theorem actual_prescribed_state_reversal_and_rate_product'+statement_lean,source_approved_overlay=(pre/'root.statement-seal99.json').as_posix(),kernel_header_and_literal_expansion_checked=False)
assert rt.decoder_packet(audit)==packet;save(ap,audit)
fresh(r/'publication-freeze99.json',dict(status='DRAFT_PENDING_INDEPENDENT_MATH_DECODER_SOURCE_EXPOSITION',module=pin(module),inputs=[pin(x) for x in [pp,lp,ap]],packet=pin(out),canonical_packet_sha256=packet['packet_sha256'],steps=len(steps),conceptual_mirror_audit=cell['conceptual_mirror_audit'],PROVED_LOCAL=False,VERIFIED=False))
pub.check_advance([decl],reviewed=False)
print(json.dumps(dict(packet=pin(out),steps=len(steps),publication_binding_sha256=audit['publication_binding_sha256'])))
