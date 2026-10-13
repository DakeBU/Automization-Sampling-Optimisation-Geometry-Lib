from pathlib import Path
import json,hashlib,sys,copy
root=Path.cwd();r=Path(__file__).parent;pre=r.parent/'pbps-prescribed-gibbs-survival-preread98'
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
module=Path(file);s=module.read_text(encoding='utf8');raw=module.read_bytes();receipt=r/'checks98/production1/receipt.json'
check=load(receipt);assert check['exit_code']==0 and check['target_raw_sha256']==sha(raw)
literal=s.split('private def actual_prescribed_gibbs_survival_statement',1)[1].split('\n/-- Actual finite prescribed',1)[0].strip()
seal=load(pre/'root.statement-seal98.json');assert literal==seal['expanded_literal_Prop'].strip()
binders,body=literal.split(' : Prop :=',1)
# Preserve the complete let-definition expansion, eliminating only the def's proof-style Prop construction.
body=body.removeprefix(' by\n  classical\n  exact\n')
statement_lean=binders+' :\n'+body
oldstatement=load(r.parent/'pbps-actual-endpoint-time-reversal97/authored-statement97.json')['statement']
restatement=oldstatement.split('There exists rho:')[0]+'''Define the actual positive-part event rate lambda_r(x,p)=sqrt(eta) max(0,<p,grad V(x)-grad V(r)>), and the target energy U_y(x,p)=V(x)+||x-y||^2/(2 eta)+||p||^2/2. The rate after momentum reversal is lambda_r(R(x,p)); it is evaluated on the same trajectory, not on a reversed-time trajectory.
For every y,r,z,n,T,t as above, extend the actual prescribed path to real s by gamma(s)=Gamma(min(max(s,0),T)), with the argument understood as the nonnegative closed-interval subtype. Put A=Gamma(T), Iplus=integral from 0 to T of lambda_r(gamma(s)) ds, and Iminus=integral from 0 to T of lambda_r(R(gamma(s))) ds, both with real Lebesgue measure. Both integrands are interval integrable. The exact identities are
U_y(A)-U_y(z)=Iplus-Iminus,
exp(-U_y(z)) exp(-Iplus)=exp(-U_y(A)) exp(-Iminus).
All finite event counts n>=0, horizons T>=0, rank-zero spaces and zero reflection normals are included. No positive jump-rate condition is imposed on the prescribed tuple. No measurability, integrability, energy identity or normalizing-constant premise is added to the six source assumptions. The simplex measure m is retained to preserve the existing path interface but is not used by these two scalar identities. The weights here are unnormalized; a common Gibbs normalizer would cancel but existence of the normalized stationary law is a separate obligation.
This is the actual finite prescribed-path energy and Gibbs/survival identity in the Appendix A.1 reversal proof. It does not assert reversed-event density matching, pointwise time reversal at right-continuous jump values, weighted sector preservation, stationary averaging or invariant probability laws, restart/Markovness, hypocoercivity, implementation errors, expected oracle cost, main sampling results or actual-input composition.'''
attribution='Chen, Chewi, Lu and Zhang, arXiv:2609.06905v1, Appendix A.1 (A.4) and its integrated Gibbs/survival identity before the weighted reversal conclusion. Complete attributed ASTIS mathematical restatement and explicit finite-arc integration; not verbatim source text or a full invariance theorem.'
context=[
 'gradient and fderiv denote real Hilbert gradient and Frechet derivative; the space is finite-dimensional with Borel structure.',
 'Fin n indexes n coordinates from zero. Fin.cons prepends, Fin.induction is finite recursion, and Fin.foldl visits records in increasing index order.',
 'Real division by zero equals zero. Real.toNNReal is the nonnegative part. Subtraction in the nonnegative reals is truncated at zero. Sum.inl is the live-record constructor; Unit is the cemetery branch.',
 'The path domain is the nonnegative closed-interval subtype. Measure.comap uses the exact unnormalized subtype measure. volume on the real line is Lebesgue measure.',
 'IntervalIntegrable f volume a b states integrability on both oriented interval restrictions; the interval integral uses the standard signed orientation. Real.exp is the real exponential. Unused let definitions do not introduce theorem hypotheses.'
]
aid='ASTIS-RT-20261012-PBPSActualPrescribedGibbsSurvival';slug='pbps-actual-prescribed-gibbs-survival';title='Actual PBPS finite-path energy and Gibbs/survival balance'
audit=dict(id=aid,state='draft',source=dict(source_id='companion-domain:'+slug,anchor=claim['source_anchor'],url='https://arxiv.org/html/2609.06905v1#A1.E4',original_text=restatement,text_sha256=sha(restatement.encode())),lean=dict(statement=statement_lean.strip(),statement_sha256=sha(statement_lean.strip().encode()),compiled=True,decoder_context=context,declaration=decl,file=file,formalizer='companion_root_20261005',compiler_evidence=receipt.as_posix()),source_review=dict(state='pending'),repairs=[])
ap=Path('research-wiki/semantic-roundtrip/audits')/f'{aid}.json';fresh(ap,audit)
packet=rt.decoder_packet(audit);out=Path('runs/semantic-roundtrip/anonymous98/input.json');fresh(out,packet)
fresh(r/'authored-statement98.json',dict(statement=restatement,attribution=attribution))
cp=Path('research-wiki/frontier-cells')/f'{cid}.json';cell=load(cp)
parents=[x for x in cell['parents'] if '.ActualPrescribedPathDensity.' not in x]
cell['parents']=parents;cell['reuse_plan']['reused_declarations']=parents[:];cell['reuse_plan']['planned_dependencies']=[]
cell['proof_digestion']['existing_substrate']=parents[:]
cell['evidence']['whole_target_compiled']=pin(module);cell['evidence']['focused_checks']=[receipt.as_posix()]
cell['blocked']['reason']='Full sealed target compiles; independent whole mathematics, anonymous decoding and source/exposition reviews pending.'
cell['purification']['dead_code_audit']='Both private calculus and finite-energy helpers are consumed. Existing94 private integrator is not duplicated or called through a private name; new two-rate telescoping discharges actual energy-grid conditions. Postmerge review pending.'
cell['source_proof_coverage']['coverage_status']='Source-first graph and exact prospective statement reviewed; final compiled source coverage pending.'
mirror=dict(status='none-found',reason='This actual finite-path energy/compensator cancellation is the local PBPS source mechanism. No new cross-domain transport or claimed external consumer.')
cell['conceptual_mirror_audit']=mirror;save(cp,cell)
def step(title,text,formula,start,end):
 a=s.index(start);b=s.index(end,a);code=s[a:b]
 return dict(title=title,text=text,formula=formula,lean=code,detail='Exact compiled region. Generic private-helper assumptions are discharged by the actual path in the public proof.',lean_source_region=dict(path=file,source_raw_sha256=sha(raw),start_line=s[:a].count('\n')+1,end_line=s[:b].count('\n'),exact_code_raw_sha256=sha(code.encode())))
steps=[
 step('Differentiate the actual target energy along a flow arc',
 'Use the already proved actual ODE xdot=sqrt(eta)p and pdot=-(x-y)/sqrt(eta)-sqrt(eta)grad V(r). The chain rule gives sqrt(eta)<grad V(x),p>+<x-y,p>/sqrt(eta)-<p,x-y>/sqrt(eta)-sqrt(eta)<p,grad V(r)>. The quadratic-force terms cancel exactly. Since max(0,a)-max(0,-a)=a, this derivative equals lambda_r(x,p)-lambda_r(x,-p). Both rates are continuous along every harmonic arc, hence integrable on every finite real interval, and FTC gives the energy increment. The proof includes either orientation and equal interval endpoints.',
 r'\frac{d}{ds}U_y(\Phi_s z)=\sqrt\eta\langle p_s,\nabla V(x_s)-\nabla V(r)\rangle=\lambda_r(\Phi_s z)-\lambda_r(R\Phi_s z).',
 'private theorem actual_arc_energy','/-- Integrable adjacent differences'),
 step('Telescope the finite energy grid',
 'For each adjacent grid interval assume, only inside this private lemma, that f and g are integrable and their integral difference is u_(j+1)-u_j. The empty grid has zero integral and zero energy increment. Append one interval: oriented interval additivity gives both integrals on the enlarged interval, and the intermediate energy cancels. Induction therefore yields the endpoint energy difference. The public proof below supplies all these local facts from the actual trajectory; this helper introduces no public premise.',
 r'\sum_j\left(\int_{a_j}^{a_{j+1}}f-\int_{a_j}^{a_{j+1}}g\right)=\sum_j(u_{j+1}-u_j)=u_N-u_0.',
 'private theorem finite_energy_balance','open Set'),
 step('Preserve target energy at every actual bounce',
 'The actual reflection preserves position and momentum norm, including a zero normal. Thus V(x), the quadratic position term and the kinetic term are all unchanged by S_r. Reuse the actual flow initial identity and the continuity of the actual rate and flow. The energy grid consists of U evaluated at the post-bounce states, with the final entry U(A). These are literal actual states, not supplied witnesses.',
 r'U_y(S_r(x,p))=V(x)+\frac{\|x-y\|^2}{2\eta}+\frac{\|p\|^2}{2}=U_y(x,p).',
 'theorem actual_prescribed_gibbs_survival_balance','  have ham :'),
 step('Identify each open arc of the actual clamped path',
 'Prepend zero to the strictly ordered event times and append T to form a monotone grid. On the open jth interval, the real-time clamp equals s. Earlier history records have already occurred and later records are strictly in the future. Apply the verified actual finite-count path law to obtain gamma(s)=Phi_(s-a_j)(z_j). Only open-interval equality is used, so right-continuous values at event times are not confused with incoming states; a finite set of endpoints does not affect the Lebesgue integrals.',
 r'a_j<s<a_{j+1}\Longrightarrow\gamma(s)=\Phi_{s-a_j}(z_j).',
 '  have ham :','  obtain ⟨rho,'),
 step('Match the energies at the ends of all arcs',
 'At an internal grid point, finite recursion defines the next post-bounce state as S_r applied to the outgoing arc endpoint. Bounce energy preservation identifies the next grid energy. On the last interval, the independently verified actual terminal formula A=Phi_(T-a_n)(z_n) supplies the same identity. This handles zero events and zero horizon without adding a positive event rate or a nonzero normal assumption.',
 r'U_y(\Phi_{a_{j+1}-a_j}(z_j))=u_{j+1},\qquad U_y(\Phi_0(z_j))=u_j.',
 '  obtain ⟨rho,','  have hstep ('),
 step('Integrate the actual trajectory and exponentiate the balance',
 'Continuous arc rates transfer their integrability to the actual path through equality on open intervals. Compose the proved arc derivative with s-a_j, apply FTC on each interval and use the endpoint energy identities. The finite telescoping lemma now proves both whole-path integrabilities and U(A)-U(z)=Iplus-Iminus. Rearranging gives -U(z)-Iplus=-U(A)-Iminus; exponentiating and exp(a+b)=exp(a)exp(b) yields the Gibbs/survival equality. Iminus uses momentum reversal along the same path. Reverse-event matching and invariant-probability averaging remain separate.',
 r'U_y(A)-U_y(z)=I_+-I_-,\qquad e^{-U_y(z)}e^{-I_+}=e^{-U_y(A)}e^{-I_-}.',
 '  have hstep (','\nend\nend AutoSamplingTheory')
]
assumptions=['Finite-dimensional real inner-product Borel E, including rank zero.','alpha,beta>=0; alpha>0; alpha<=beta; V is C2; alpha||v||^2<=D2V(x)[v,v]<=beta||v||^2 for all x,v; eta>0; beta*eta<=1.','Every y,r,z,n>=0,T>=0 and strictly ordered prescribed event tuple; no positive rate or nonzero-normal condition.','Actual Gamma, clamped real-time extension, momentum reversal, positive-part rate and exact U definitions are fixed; both integral finiteness assertions are conclusions.']
source=dict(url=audit['source']['url'],edition='arXiv2609.06905v1',anchor=claim['source_anchor'],wording_status='faithful paraphrase',attribution=attribution)
deltas=[dict(source='A4 and its finite-path integrated identity.',lean='Both rate integrabilities, actual terminal energy increment and unnormalized Gibbs/survival equality.',classification='source-implicit',reason='Explicit chain rule, finite endpoint exclusion and telescoping; all producer premises discharged.'),dict(source='Finite Euclidean phase space.',lean='Finite real Hilbert Borel E includes rank zero.',classification='generalization',reason='Coordinate-free source formulation.'),dict(source='Original sampler assumptions.',lean='All six analytic assumptions retained with no excess binder.',classification='same',reason='Actual parents close internal proof ingredients.'),dict(source='Full weighted reversal and invariant law.',lean='Actual prescribed-path energy/survival identity only.',classification='unresolved',reason=claim['truth_boundary'])]
item=dict(id=slug,library='pbps',chapter='pbps-01',chapter_path='example-cases/samplewiki/companions/proximal-bouncy-particle.html',title=title,source=source,statement=restatement,assumptions=assumptions,formulae=[dict(label='Actual energy and survival balance',tex=steps[-1]['formula'])],obligations=[dict(id='finite-gibbs-survival',label='Actual finite prescribed energy and survival equality'),dict(id='weighted-invariance',label='Weighted reversal and stationary invariant probability')],bindings=[dict(declaration=decl,cell=cid,role='proof-edge',supports=['finite-gibbs-survival'],audit_id=aid,boundary=claim['truth_boundary'],assumption_deltas=deltas)])
for key in ['declaration_level','statement_seal','source_proof_coverage','proof_digestion','purification']:item[key]=copy.deepcopy(cell[key])
unit=dict(kind='theorem',declaration=decl,title=title,sources=[dict(url=source['url'],label=source['anchor'],scope=claim['truth_boundary'])],tests=claim['focused_checks'],assumptions=assumptions,statement=restatement,formula=steps[-1]['formula'],boundary=claim['truth_boundary'],steps=steps,lean_statement=restatement,lean_proof='; '.join(x['title'] for x in steps),helpers=[decl.rsplit('.',1)[0]+'.actual_prescribed_gibbs_survival_statement'],astis_dependencies=parents,mathlib_dependencies=['HasDerivAt.norm_sq','HasFDerivAt.comp_hasDerivAt','HasDerivAt.scomp','Continuous.intervalIntegrable','IntervalIntegrable.congr_uIoo','IntervalIntegrable.trans','intervalIntegral.integral_congr_Ioo_of_le','intervalIntegral.integral_eq_sub_of_hasDerivAt','intervalIntegral.integral_add_adjacent_intervals','intervalIntegral.integral_sub','Real.exp_add'])
pp=Path('website/content/publications')/f'{slug}.json';lp=Path('website/content/declaration_lessons')/f'{slug}.json';fresh(pp,dict(schema_version=1,items=[item]));fresh(lp,dict(schema_version=1,units=[unit]))
pub.inputs.cache_clear();pub.load.cache_clear();audit['publication_binding_sha256']=pub.binding_digest(item,item['bindings'][0],pub.inputs());audit['publication_context']=pub.review_context(item,item['bindings'][0],pub.inputs())
start=s.index('theorem actual_prescribed_gibbs_survival_balance');stop=s.index(':= by\n',start)
audit['lean']['statement_representation']=dict(kind='exact-literal-Prop-expansion',actual_header=s[start:stop],private_definition='def actual_prescribed_gibbs_survival_statement'+literal,expanded_header='theorem actual_prescribed_gibbs_survival_balance'+statement_lean,source_approved_overlay=(pre/'root.statement-seal98.json').as_posix(),kernel_header_and_literal_expansion_checked=False)
assert rt.decoder_packet(audit)==packet;save(ap,audit)
fresh(r/'publication-freeze98.json',dict(status='DRAFT_PENDING_INDEPENDENT_MATH_DECODER_SOURCE_EXPOSITION',module=pin(module),inputs=[pin(x) for x in [pp,lp,ap]],packet=pin(out),canonical_packet_sha256=packet['packet_sha256'],steps=len(steps),conceptual_mirror_audit=mirror,PROVED_LOCAL=False,VERIFIED=False))
pub.check_advance([decl],reviewed=False)
print(json.dumps(dict(packet=pin(out),steps=len(steps),publication_binding_sha256=audit['publication_binding_sha256'])))
