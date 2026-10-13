from pathlib import Path
import json,hashlib,sys,copy,re,datetime
root=Path(__file__).resolve().parents[3];run=Path(__file__).resolve().parent
sys.path.insert(0,str(root/'tools'))
import astis_publication as pub
import astis_semantic_roundtrip as rt
load=lambda p:json.loads(p.read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,x):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def pin(p):return dict(path=p.relative_to(root).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
claim=load(run/'claim.json');decl=claim['target_declarations'][0];file=claim['proposed_files'][0];cid=claim['frontier_cell']
module=root/file;s=module.read_text(encoding='utf-8');raw=module.read_bytes()
aid='ASTIS-RT-20261011-PBPSActualPrescribedPathDensity';slug='pbps-actual-prescribed-path-density';title='Actual PBPS prescribed-path hazard and density identity'
ap=root/'research-wiki/semantic-roundtrip/audits'/f'{aid}.json';audit=load(ap)
authored=load(run/'authored-statement94.json');statement=authored['statement'];attribution=authored['attribution']
cp=root/'research-wiki/frontier-cells'/f'{cid}.json';cell=load(cp)
parents=sorted(set(re.findall(r'AutoSamplingTheory\.(?:ExampleCases|TechnicalLemmas)\.[A-Za-z0-9_.]+',s)))
parents=[x for x in parents if x not in [decl.rsplit('.',1)[0],'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteCountPath']]
cell['parents']=parents;cell['reuse_plan']['reused_declarations']=parents;cell['proof_digestion']['existing_substrate']=parents
cell['blocked']['reason']='Exact sealed production theorem compiled; independent whole math, source-blind decoding, source/exposition review and publication admission pending.'
cell['evidence']['focused_checks']=['runs/20261007-companion-priority/pbps-actual-prescribed-path-density94/checks94/production1/receipt.json','runs/20261007-companion-priority/pbps-actual-prescribed-path-density94/checks94/exact-sealed-kernel1/receipt.json']
cell['evidence']['whole_target_compiled']=pin(module)
cell['purification']['dead_code_audit']='Production compiled; postmerge purification remains pending. Six private mathematical helpers each have a real local consumer.'
cell['learning_contract']['salvage']['reason']='API-only failed trials retained; no mathematical route discarded, exact Statement Seal unchanged.'
save(cp,cell)
assumptions=[
 'Finite-dimensional real inner-product Borel E, including rank zero; alpha,beta are nonnegative.',
 'Six original analytic assumptions: alpha>0, alpha<=beta, V is C2, alpha||v||^2<=D2V(x)[v,v]<=beta||v||^2 for all x,v, eta>0, beta*eta<=1.',
 'All y,r,z0, finite n and T>=0, and all strictly ordered prescribed event tuples are universally quantified.',
 'Flow, reflection, rate, integrated arc hazard, tagged histories, finite interpolation and density are explicit definitions inherited literally from the actual finite-count law.',
 'Integrability and incoming left limits are conclusions. No continuity of the reflection at a vanishing normal, positive density, supplied path law or stochastic independence premise is added.'
]
formulae=[
 r'0=a_0<a_1<\cdots<a_n<T=a_{n+1},\qquad z_i=S_r\Phi_{a_i-a_{i-1}}z_{i-1}.',
 r'\gamma(s)=\Gamma_n(t)(\min\{\max\{s,0\},T\}),\quad \gamma(s)=\Phi_{s-a_j}z_j\quad(a_j<s<a_{j+1}).',
 r'\int_0^T\lambda_r(\gamma(s))\,ds=\sum_{j=0}^{n}\Lambda_{z_j}(a_{j+1}-a_j).',
 r'\lim_{s\uparrow a_i}\gamma(s)=\Phi_{a_i-a_{i-1}}z_{i-1},\qquad\lim_{s\uparrow a_i}\lambda_r(\gamma(s))=\lambda_r(\Phi_{a_i-a_{i-1}}z_{i-1}).',
 r'\rho_n(T,t)=\operatorname{ofReal}\!\left[e^{-\int_0^T\lambda_r(\gamma(s))\,ds}\prod_{i=1}^{n}\lambda_r(\Phi_{a_i-a_{i-1}}z_{i-1})\right].'
]
# The first display needs a separate zero-event reading: n=0 allows T=0.
formulae[0]=r'a_0=0,\quad a_i=t_i\ (1\le i\le n),\quad a_{n+1}=T;\qquad 0<t_1<\cdots<t_n<T\ (n>0),\quad z_i=S_r\Phi_{a_i-a_{i-1}}z_{i-1}.'
def step(title,text,formula,start,end):
 a=s.index(start);b=s.index(end,a);code=s[a:b]
 return dict(title=title,text=text,formula=formula,lean=code,detail='Exact compiled proof region. Helper assumptions are discharged by the actual flow/rate/path producers in this module.',lean_source_region=dict(path=file,source_raw_sha256=sha(raw),start_line=s[:a].count('\n')+1,end_line=s[:b].count('\n'),exact_code_raw_sha256=sha(code.encode())))
steps=[
 step('Identify the actual prescribed open arcs',
 'Append T to the strictly increasing list beginning at0. The resulting grid is nondecreasing, also when n=0 and T=0. For a_j<s<a_(j+1), monotonicity gives0<=s<=T, so the clamp equals s. Every later record has time greater than s. Apply the already proved last-eligible-record formula of the actual finite-count path law to obtain gamma(s)=Phi_(s-a_j)(z_j). This uses the existing interpolation rather than a newly postulated path.',formulae[1],'private theorem actual_arc','private theorem actual_analysis'),
 step('Ignore endpoint values only for integration',
 'Assume a<=b. A continuous comparison function g is integrable on every finite interval. If f=g on the open interval(a,b), changing the two endpoint values does not change Lebesgue interval integrability or its integral. Transfer integrability with congr_uIoo and the integral with integral_congr_Ioo_of_le. The a=b case is included; no equality or continuity at a jump is required.',r'a\le b,\quad f=g\text{ on }(a,b),\quad g\in C^0\Longrightarrow\int_a^b f=\int_a^b g.', 'private theorem arc_integral','/-- Agreement with the incoming'),
 step('Sum the finite adjacent integrals',
 'Let the grid be nondecreasing; for every j assume g_j is continuous and f=g_j on(a_j,a_(j+1)). Induct on the number of grid intervals. The zero-interval integral and empty sum vanish. At the successor step, integrability of the prefix and last arc gives integrability of their union. The adjacent-interval identity adds the last integral, and the finite sum splits into its prefix and last index. This proves the exact sum for any nondecreasing finite grid without requiring positive lengths.',r'\int_{a_0}^{a_m}f(s)\,ds=\sum_{j=0}^{m-1}\int_{a_j}^{a_{j+1}}g_j(s)\,ds.', 'private theorem finite_arc_integral','private theorem actual_arc'),
 step('Determine an incoming limit from the preceding arc',
 'If a<b, the interval(a,b) is eventually visited by the left-neighborhood filter at b. On that interval the function equals its continuous incoming comparison arc. Restrict the continuous limit to the left filter and transfer it through eventual equality. The value assigned at b itself has no role; in particular a post-bounce value at b does not replace the incoming limit.',r'a\le b,\quad f=g\text{ on }(a,b),\ a<b,\ g\in C^0\Longrightarrow\lim_{s\uparrow b}f(s)=g(b).','private theorem incoming_left_limit','/-- Finite adjacent arcs'),
 step('Apply arc calculus to the actual phase and rate',
 'The actual harmonic-flow theorem supplies joint flow continuity, and the actual bounce-rate theorem supplies rate continuity. Compose them with s->s-a_j to obtain continuous incoming phase and rate arcs. The open-arc identity supplies the comparison equalities. Apply finite integration and translate each interval by a_j; its nonnegative length is exactly the argument of Lambda_(z_j). For each strict interior event a_i, the predecessor gap is positive. Apply the left-limit lemma to that phase arc, then compose with the continuous rate. Clamping is only an auxiliary real-time extension and is inactive on these open arcs.',formulae[2]+formulae[3], 'private theorem actual_analysis','private theorem product_survival'),
 step('Combine all exponential survival factors',
 'Distribute the finite product into rate factors and exponential factors. The product of exponentials is the exponential of the sum. Multiply by the terminal survival exponential and append the final hazard term to the finite sum. This is a real algebraic identity for arbitrary rates and hazards, so zero rates and the empty product do not require division or positivity.',r'\left(\prod_{i=0}^{n-1}r_i e^{-h_i}\right)e^{-h_n}=e^{-\sum_{j=0}^{n}h_j}\prod_{i=0}^{n-1}r_i.', 'private theorem product_survival','theorem actual_prescribed_path_density_rewrite'),
 step('Rewrite the original finite-count density',
 'Retain the exact twenty inherited definitions and six analytic assumptions. The simplex shows0<=a_n<=T, so the truncated terminal duration T-toNNReal(a_n) equals toNNReal(T-a_n). Thus the original tagged terminal weight is precisely ofReal(exp(-h_n)). The prefix density is the product of the n incoming rates and their arc survivals. Since the terminal exponential is nonnegative, ofReal transports multiplication exactly. Apply the product identity and substitute the proved integrated-hazard sum. Together with integrability and both incoming limits this closes the full frozen proposition. No normalization, all-count summation or signed-observable convergence is asserted.',formulae[4], 'theorem actual_prescribed_path_density_rewrite','\n#print axioms')
]
source=dict(url=audit['source']['url'],edition='arXiv2609.06905v1',anchor=claim['source_anchor'],wording_status='faithful paraphrase',attribution=attribution)
deltas=[dict(source='Prescribed trajectory density around Appendix A.1(A.7).',lean='The six analytic conditions and literal finite interpolation are retained; integrability, incoming limits and hazard stitching are derived.',classification='source-implicit',reason='ASTIS supplies the finite-arc analysis omitted from the printed expression.'),dict(source='Positive-dimensional phase trajectories on the finite physical interval.',lean='Rank-zero and zero-event/zero-horizon cases included; auxiliary real-time clamp disclosed.',classification='generalization',reason='Clamping agrees on the physical interval and locally before every strict interior jump; no function-space topology is inferred.'),dict(source='Complete(A.7) path expectation expansion.',lean='Deterministic prescribed-sector density rewrite only; composition with actual finite-count measures and countable/signed sums remain open.',classification='unresolved',reason='The finite density ingredient does not establish the full expansion or main theorem.')]
item=dict(id=slug,library='pbps',chapter='pbps-01',chapter_path='example-cases/samplewiki/companions/proximal-bouncy-particle.html',title=title,source=source,statement=statement,assumptions=assumptions,formulae=[dict(label='Prescribed path identity '+str(i+1),tex=f) for i,f in enumerate(formulae)],obligations=[dict(id='prescribed-path-density',label='Actual prescribed-path hazard and density identity'),dict(id='full-path-a7',label='Actual finite-count composition and countable full A7 assembly')],bindings=[dict(declaration=decl,cell=cid,role='proof-edge',supports=['prescribed-path-density'],audit_id=aid,boundary=claim['truth_boundary'],assumption_deltas=deltas)])
for key in ['declaration_level','statement_seal','source_proof_coverage','proof_digestion','purification']:item[key]=copy.deepcopy(cell[key])
unit=dict(kind='theorem',declaration=decl,title=title,sources=[dict(url=source['url'],label=source['anchor'],scope=claim['truth_boundary'])],tests=claim['focused_checks'],assumptions=assumptions,statement=statement,formula=formulae[4],boundary=claim['truth_boundary'],steps=steps,lean_statement=statement,lean_proof='; '.join(x['title'] for x in steps),helpers=[],astis_dependencies=parents,mathlib_dependencies=['IntervalIntegrable.congr_uIoo','intervalIntegral.integral_congr_Ioo_of_le','intervalIntegral.integral_add_adjacent_intervals','intervalIntegral.integral_comp_sub_right','Ioo_mem_nhdsLT','Real.exp_sum','Real.exp_add',"ENNReal.ofReal_mul'"])
pp=root/'website/content/publications'/f'{slug}.json';lp=root/'website/content/declaration_lessons'/f'{slug}.json'
assert not pp.exists() and not lp.exists();save(pp,dict(schema_version=1,items=[item]));save(lp,dict(schema_version=1,units=[unit]))
pub.inputs.cache_clear();pub.load.cache_clear()
audit['publication_binding_sha256']=pub.binding_digest(item,item['bindings'][0],pub.inputs());audit['publication_context']=pub.review_context(item,item['bindings'][0],pub.inputs())
audit['lean']['statement_representation']=dict(kind='literal-public-header',actual_header=s[s.index('theorem actual_prescribed_path_density_rewrite'):s.index(' := by\n',s.index('theorem actual_prescribed_path_density_rewrite'))],kernel_header_and_literal_expansion_checked=True,original_seal='runs/20261007-companion-priority/pbps-prescribed-path-density-preread94/root.statement-seal94.json')
assert rt.decoder_packet(audit)==load(root/'runs/semantic-roundtrip/anonymous94/input.json');save(ap,audit)
save(run/'publication-freeze94.json',dict(status='DRAFT_PENDING_WHOLE_MATH_SOURCE_EXPOSITION',module=pin(module),inputs=[pin(x) for x in [pp,lp,ap]],steps=len(steps),conceptual_mirror_audit=dict(status='none-found',reason='Finite arc integration and incoming limits realize the existing prescribed-path mechanism; no new cross-domain transport found.'),PROVED_LOCAL=False,VERIFIED=False))
pub.check_advance([decl],reviewed=False)
print(json.dumps(dict(steps=len(steps),publication_binding_sha256=audit['publication_binding_sha256'],parents=parents)))
