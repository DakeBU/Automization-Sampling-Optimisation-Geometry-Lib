from pathlib import Path
import json,hashlib,sys
root=Path(__file__).resolve().parents[3];run=Path(__file__).resolve().parent
sys.path.insert(0,str(root/'tools'))
import astis_semantic_roundtrip as rt
load=lambda p:json.loads(p.read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,x):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def pin(p):return dict(path=p.relative_to(root).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
claim=load(run/'claim.json');decl=claim['target_declarations'][0];file=claim['proposed_files'][0]
module=root/file;raw=module.read_bytes();s=module.read_text(encoding='utf-8')
start=s.index('theorem actual_prescribed_path_density_rewrite');stop=s.index(' := by\n',start)
statement=s[start+len('theorem actual_prescribed_path_density_rewrite'):stop].strip()
pre=root/'runs/20261007-companion-priority/pbps-prescribed-path-density-preread94'
header=(pre/'Header94.lean').read_text(encoding='utf-8')
binders=header[header.index('    {E : Type*}'):header.index(' : Prop := by')]
body=header[header.index('    let c :'):header.index('\n#check')].rstrip()
assert statement==(binders+' :\n'+body).strip()
receipt=run/'checks94/production1/receipt.json';assert load(receipt)['exit_code']==0
assert load(run/'checks94/exact-sealed-kernel1/receipt.json')['exit_code']==0
restatement='''Let E be a finite-dimensional real inner-product space equipped with its Borel sigma algebra; zero dimension is allowed. Let alpha,beta>=0, eta be real, V:E->R. Assume exactly alpha>0, alpha<=beta, V is C2, alpha||v||^2<=D2V(x)[v,v]<=beta||v||^2 for every x,v, eta>0 and beta*eta<=1. All conclusions hold for every y,r in E, initial phase z0=(x0,p0), integer n>=0 and finite T>=0.
Set c=y-eta*grad V(r). For z=(x,p), define Phi_u(z)=(c+cos(u)(x-c)+sqrt(eta)sin(u)p, -sin(u)/sqrt(eta)(x-c)+cos(u)p). Define h_r(x)=grad V(x)-grad V(r), S_r(x,p)=(x,p-[2<p,h_r(x)>/||h_r(x)||^2]h_r(x)) with real division totalized by 0/0=0, lambda_r(x,p)=sqrt(eta)max(0,<p,h_r(x)>), and Lambda_z(u)=integral from0 to u of lambda_r(Phi_s(z)) ds for u>=0, using Lebesgue measure.
A tagged record is either live(a,z), with a>=0, or stopped; Hist_n is the type of all n+1 records. Let Delta_n(T) be the strict simplex 0<t1<...<tn<T. Write a0=0, ai=ti (1<=i<=n), a_(n+1)=T. Given t in Delta_n(T), define z_i=S_r(Phi_(a_i-a_(i-1))(z_(i-1))) for1<=i<=n and K_n(t)_j=live(a_j,z_j). The literal Lean nonnegative conversions preserve these nonnegative times. Define qReal_n(t)=product_(i=1)^n [lambda_r(Phi_(a_i-a_(i-1))(z_(i-1))) exp(-Lambda_(z_(i-1))(a_i-a_(i-1)))], q_n=ofReal(qReal_n).
For arbitrary histories let readTime(live(a,z))=a and readTime(stopped)=0; d_n(T,h)=max(T-readTime(h_n),0). Put W(live(a,z),u)=ofReal(exp(-Lambda_z(u))) and W(stopped,u)=0. Define rho_n(T,t)=q_n(t) W(K_n(t)_n,d_n(T,K_n(t))). Here ofReal(x) is max(x,0) embedded into extended nonnegative reals; no probability law or normalization is assumed in this deterministic identity.
Define Path_T as all phase-valued functions on[0,T]. The total interpolation Psi_n(h)(s) starts at z0 and scans records j=0,...,n in order: a live(a,z) record with a<=s replaces the accumulator by Phi_(max(s-a,0))(z); otherwise it is unchanged. Set Gamma_n(t)=Psi_n(K_n(t)). Extend this particular prescribed path to all real times by gamma(s)=Gamma_n(t)(min(max(s,0),T)). This extension agrees with Gamma on[0,T]; no topology on an entire function space is asserted.
Then lambda_r(gamma(s)) is Lebesgue interval integrable on[0,T], and integral_0^T lambda_r(gamma(s)) ds=sum_(j=0)^n Lambda_(z_j)(a_(j+1)-a_j). For every1<=i<=n, gamma(s) tends from the left at a_i to Phi_(a_i-a_(i-1))(z_(i-1)), and lambda_r(gamma(s)) tends from the left to lambda_r of that same incoming phase. Consequently rho_n(T,t)=ofReal(exp(-integral_0^T lambda_r(gamma(s))ds) * product_(i=1)^n lambda_r(Phi_(a_i-a_(i-1))(z_(i-1)))). The density evaluates the incoming phase, not the reflected value at the jump.
These conclusions include n=0 (one survival arc, empty product1), T=0 (only the zero-event simplex is inhabited), zero-dimensional E and zero rates; no positivity of event densities is assumed. All integrability, continuity along arcs, left limits and identities are proved, not additional premises.
This is an attributed ASTIS completion of the prescribed-trajectory hazard/left-limit ingredient of Appendix A.1 around(A.7), not a quoted standalone theorem. Composing it with the finite-count path law, summing over all counts, signed-observable convergence, Skorokhod compatibility, restart/Markovness, invariance, hypocoercivity, implementation errors, unbounded expected costs and the main paper/composition results remain separate obligations.'''
attribution='Chen, Chewi, Lu and Zhang, arXiv:2609.06905v1, Appendix A.1; faithful attributed restatement and ASTIS proof of the source-implicit finite prescribed-path density ingredient, not verbatim text.'
context=[
 'The ambient norm and inner product are real, and the indicated sigma algebra is Borel. gradient and fderiv are the standard Hilbert gradient and Frechet derivative.',
 'Fin n is the ordered set of integers0 through n-1. Fin.cons prepends one entry; Fin.snoc appends one entry. i.castSucc preserves the numeric index and i.succ increments it. Fin.induction is recursion on this finite index.',
 'Fin.foldl scans finite indices in increasing order, updating its accumulator. A sum tag distinguishes the two displayed record branches; Unit has one element.',
 'Nonnegative-real subtraction truncates at zero; Real.toNNReal(x)=max(x,0). ENNReal.ofReal embeds max(x,0) in the extended nonnegative reals. Real division by zero is zero.',
 'volume on the real line is Lebesgue measure. IntervalIntegrable requires integrability over the unordered interval. The displayed interval integral is oriented, although all displayed time intervals here are nonnegative in order.',
 'The left-neighborhood filter means approach strictly from below in real time. Limits of phase values use the product norm topology. No topology on a function space is implicit.',
 'Products and sums indexed by Fin0 are respectively one and zero. StrictMono and every forall quantifier retain their ordinary pointwise meanings, including empty subtypes.'
]
aid='ASTIS-RT-20261011-PBPSActualPrescribedPathDensity';slug='pbps-actual-prescribed-path-density'
audit=dict(id=aid,state='draft',source=dict(source_id='companion-domain:'+slug,anchor=claim['source_anchor'],url='https://arxiv.org/html/2609.06905v1#A1.E7',original_text=restatement,text_sha256=sha(restatement.encode())),lean=dict(statement=statement,statement_sha256=sha(statement.encode()),compiled=True,decoder_context=context,declaration=decl,file=file,formalizer='companion_root_20261005',compiler_evidence=receipt.relative_to(root).as_posix()),source_review=dict(state='pending'),repairs=[])
ap=root/'research-wiki/semantic-roundtrip/audits'/f'{aid}.json';assert not ap.exists();save(ap,audit)
packet=rt.decoder_packet(audit);out=root/'runs/semantic-roundtrip/anonymous94/input.json';assert not out.exists();save(out,packet)
save(run/'authored-statement94.json',dict(statement=restatement,attribution=attribution))
save(run/'decoder-freeze94.json',dict(module=pin(module),seal=pin(pre/'root.statement-seal94.json'),compile=pin(receipt),exact_kernel=pin(run/'checks94/exact-sealed-kernel1/receipt.json'),packet=pin(out),canonical_packet_sha256=packet['packet_sha256'],source_visible=False,publication_binding_pending=True))
print(json.dumps(dict(packet=pin(out),canonical_packet_sha256=packet['packet_sha256'])))
