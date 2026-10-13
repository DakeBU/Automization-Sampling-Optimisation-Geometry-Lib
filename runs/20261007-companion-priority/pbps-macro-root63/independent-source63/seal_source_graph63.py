import hashlib
import json
import re
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

BASE=Path(r'E:\Samplinglib')
OUT=BASE/'runs/20261007-companion-priority/pbps-macro-root63/independent-source63'
def digest(b): return hashlib.sha256(b).hexdigest()
def put(name, obj):
    b=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    (OUT/name).write_bytes(b)
    return digest(b)
manifest=json.loads((OUT/'primary-only.input.manifest.json').read_text(encoding='utf-8'))
raw=(BASE/manifest['source_primary']['path']).read_bytes()
extras=[]
for name,lo,hi in [('root-neighborhood',742298,795302),('C4-proof-neighborhood',1009595,1032500)]:
    b=raw[lo:hi]; lf=b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
    (OUT/f'primary-extra-{name}.exactraw.snapshot.html').write_bytes(b)
    (OUT/f'primary-extra-{name}.lf.snapshot.html').write_bytes(lf)
    extras.append({'name':name,'byte_range':[lo,hi],'raw_sha256':digest(b),'lf_sha256':digest(lf),'raw_path':str(OUT/f'primary-extra-{name}.exactraw.snapshot.html'),'lf_path':str(OUT/f'primary-extra-{name}.lf.snapshot.html')})

nodes=[
 ('source:pbps-standing','S1.p1 / (1.1)','definition/standing','mu=Z^-1 exp(-V)dx on R^d; V in C2; 0<alpha<=beta; alpha I<=Hessian V<=beta I.'),
 ('source:pbps-positive-eta','S2.SS2.p1.1','standing','eta in (0,1/beta]; alpha eta<=beta eta<=1 and eta>0.'),
 ('source:pbps-joint-law','S2.E6','definition','pi_eta(dx dy) proportional exp(-V(x)-||x-y||^2/(2eta))dxdy.'),
 ('source:pbps-joint-representation','S2.E7','definition','X~mu; independent standard Gaussian Z; Y=X+sqrt(eta)Z.'),
 ('source:pbps-real-L2','A4.SS1 / Definition D.1 / D.1-D.2','definition/standing','Real Hilbert L2 of a probability measure consists of ae measurable square-integrable equivalence classes; real inner product int fg; centered subspace int f=0.'),
 ('source:pbps-projection-convention','A4.SS1 / Definition D.1','definition/standing','Closed subspace and unique bounded orthogonal projection P_M; f-P_M f lies in orthogonal complement.'),
 ('source:pbps-bounded-adjoint-order','A4.SS1 / Definition D.1 / D.3','definition/standing','Operators in analysis bounded linear unless stated; adjoint, selfadjointness, norm contraction, unitary, selfadjoint involution; Loewner order via all real quadratic forms.'),
 ('source:pbps-positive-root-convention','A4.SS1 / Definition D.1','standing','Spectral theorem for selfadjoint bounded operators; nonnegative operator has a unique nonnegative square root.'),
 ('source:pbps-conditional-P','A2.E1 / A2.SS1.p1','definition','P f = conditional expectation given Y; depends on y; bounded orthogonal projection on H=L2(pi_eta).'),
 ('source:pbps-macro-micro','A2.E2 / A2.SS1.p1','definition','H_P=ran(P), y-only observables; H_perp=ker(P)=ran(I-P), conditional-zero-mean; orthogonal direct decomposition.'),
 ('source:pbps-block-convention','A2.E3 / A2.SS1.p2','definition','T_ab=P_a T P_b as maps H_b -> H_a; first index target, second source.'),
 ('source:pbps-reflection','A2.E4 / A2.SS1.p3','definition','U f(x,y)=f(x,2x-y); pullback selfadjoint unitary and involutive.'),
 ('source:pbps-macro-compression','A2.SS1.p3','unnamed estimate','C=U_PP=P U P on H_P is selfadjoint contraction; A=U_perpP=Pperp U P maps H_P to H_perp; offdiagonal adjoint.'),
 ('source:pbps-block-Gram','A2.E5 / A2.SS1.p3','display/proof','U^2=I in blocks gives A* A=I-C^2 and A* U_perpperp=-C A*.'),
 ('source:pbps-exchangeable-pair','A2.E8 / A2.SS2','definition/proof','Y+=X+sqrt(eta)Z; Y-=X-sqrt(eta)Z; pair exchangeable; H_P identified with L2(pi_eta^Y).'),
 ('source:pbps-conditional-leakage','A2.E9 / A2.SS2','display/proof','C f(y)=E[f(Y-)|Y+=y]; ||A f||^2=E Var(f(Y-)|Y+).'),
 ('source:pbps-Gamma-definition','A2.E10 / A2.SS2','definition','Gamma_P=(I-C^2)^(1/2) on H_P, nonnegative branch specified by D.1. No inverse used in definition.'),
 ('source:pbps-Gamma-Gram-energy','A2.E11 / A2.SS2','display/proof','From B.5 and Gamma definition: A* A=Gamma_P^2 and ||A f||=||Gamma_P f|| for every f in H_P; squares give energy ||f||^2-||C f||^2.'),
 ('source:pbps-rho-gap','A2.E12 / A2.Thmtheorem1.p1','definition','Under beta eta<=1, rho=(1-alpha eta)/(1+alpha eta); gamma=sqrt(1-rho^2)=2sqrt(alpha eta)/(1+alpha eta), gamma>=sqrt(alpha eta)/2.'),
 ('source:pbps-conditional-density-score','A3.SS1.p2 / C.1','definition/proof ingredient','Density proportional exp(-V((y+u)/2)-||y-u||^2/(8eta)); s_y=-(1/2)grad V((y+u)/2)-(y-u)/(4eta); differentiating normalized density gives gradient C f = conditional covariance.'),
 ('source:pbps-analytic-contraction','A3.E4 / C.1-C.4','upstream theorem/proof','C.1 covariance, conditional Poincare/Cauchy-Schwarz and Hessian bound -> C.2; marginal Poincare C.3 plus C.2 -> ||C f||<=rho||f|| on centered H_P,0.'),
 ('source:pbps-centered-macro','A2.Thmtheorem1 / B.14','definition','H_P,0=H_P intersect L2_0(pi_eta); C preserves it because C is selfadjoint and preserves constants.'),
 ('source:pbps-macro-gap','A2.E15 / A2.Thmtheorem1','display/proof','On H_P,0, ||C||<=rho implies Gamma_P>=gamma I via positive functional calculus; inverse is bounded only on this centered subspace.'),
 ('source:pbps-polar-boundary','A2.E16 / A2.SS2.p5','downstream display','Restricted Gamma inverse gives A=V Gamma, V=A Gamma^-1:H_P,0->H_perp and V*V=I. This is a downstream consumer outside current root/compression/leakage/energy/uniqueness proof unit.')
]
excluded=[
 {'anchor':'A2.SS1.p1 / K transition and halfturn branch / (3.11), Proposition 3.2','reason':'Ideal PBPS full transition and half-turn are surrounding motivation; current root unit uses reflection/projection only.'},
 {'anchor':'A2.SS1.p1 / [14,21]','reason':'References supply terminology hypocoercivity; no independent analytic input to this operator root edge.'},
 {'anchor':'S2.SS2.p1.1 / [17]','reason':'Proximal sampler attribution retained; the explicit augmented joint law and Gaussian representation are the mathematical input.'},
 {'anchor':'A4.SS1 / Definition D.2 / D.4-D.5','reason':'Markov observables, density evolution and chi-square consequences are outside the bounded root unit; Hilbert/adjoint conventions D.1 are included.'},
 {'anchor':'A2.E5 second block identity','reason':'A* U_perpperp=-C A* is retained in source inventory but not needed for root Gram/energy; downstream half-turn lane.'},
 {'anchor':'A2.SS2.p5 final half-turn sentence','reason':'Near -I action on polar microscopic directions is a downstream half-turn result.'},
 {'anchor':'extra root context / A.9, Proposition A.2, B.6-B.7','reason':'Half-turn block and K factorization are a separate downstream ideal-chain convergence lane.'},
 {'anchor':'extra root context / B.13 smoothing and B.14 lower bound C>=-I/2','reason':'Full smoothing estimate and additional spectral lower bound are not conclusions of the present bounded positive-root unit; C.4 norm contraction is an upstream producer.'},
 {'anchor':'extra C4 proof / conditional and marginal Poincare and C.1 differentiation','reason':'These are recorded upstream analytic dependencies, not reproved by the root/compression unit; regularity/normalization must stay discharged by their analytic producer and may not be added as root public hypotheses.'}
]

region_map={0:['source:pbps-conditional-P'],1:['source:pbps-macro-micro'],2:['source:pbps-block-convention'],3:['source:pbps-reflection'],4:['source:pbps-block-Gram'],5:['source:pbps-real-L2','source:pbps-projection-convention','source:pbps-bounded-adjoint-order','source:pbps-positive-root-convention'],6:['source:pbps-analytic-contraction'],7:['source:pbps-Gamma-definition'],8:['source:pbps-Gamma-Gram-energy'],9:['source:pbps-macro-gap'],10:['source:pbps-polar-boundary'],11:['source:pbps-polar-boundary'],12:['source:pbps-conditional-leakage'],13:['source:pbps-rho-gap'],14:['source:pbps-standing'],15:['source:pbps-joint-law'],16:['source:pbps-joint-representation'],17:['source:pbps-conditional-P','source:pbps-macro-micro'],18:['source:pbps-block-convention'],19:['source:pbps-reflection','source:pbps-macro-compression','source:pbps-block-Gram'],20:['source:pbps-exchangeable-pair'],21:['source:pbps-conditional-density-score'],22:['source:pbps-rho-gap'],23:['source:pbps-positive-eta']}
coverage=[]
for r in manifest['primary_regions']:
    coverage.append({'region':r['index'],'all_literal_ids':r['ids'],'nodes':region_map[r['index']],'exclusions':[x for x in excluded if (r['index']==5 and x['anchor'].startswith('A4.SS1')) or (r['index']==17 and x['anchor'].startswith('A2.SS1.p1')) or (r['index']==11 and x['anchor'].startswith('A2.SS2.p5')) or (r['index']==23 and x['anchor'].startswith('S2.SS2')) or (r['index']==4 and 'second block' in x['anchor'])],'disposition':'NODE with explicit excluded subitems where listed; all nested mathematical markup covered by its containing display/paragraph','raw_sha256':r['raw_sha256']})
edges=[
 (['source:pbps-standing','source:pbps-positive-eta'],'source:pbps-joint-law','(2.6) admissible joint law; Gaussian representation (2.7)'),
 (['source:pbps-joint-law','source:pbps-real-L2','source:pbps-projection-convention'],'source:pbps-conditional-P','B.1 conditional projection on H'),
 (['source:pbps-conditional-P'],'source:pbps-macro-micro','B.2 and following direct-decomposition paragraph'),
 (['source:pbps-macro-micro','source:pbps-block-convention','source:pbps-reflection'],'source:pbps-macro-compression','B.4 following selfadjoint contraction paragraph'),
 (['source:pbps-macro-compression','source:pbps-reflection'],'source:pbps-block-Gram','B.5 using U^2=I; contraction also proves defect nonnegative'),
 (['source:pbps-macro-compression','source:pbps-positive-root-convention'],'source:pbps-Gamma-definition','B.10 nonnegative defect root; uniqueness is standing functional calculus, not an extra source binder'),
 (['source:pbps-block-Gram','source:pbps-Gamma-definition','source:pbps-bounded-adjoint-order'],'source:pbps-Gamma-Gram-energy','B.11: Gram square identity -> equal squared norms -> equal nonnegative norms'),
 (['source:pbps-joint-representation','source:pbps-reflection','source:pbps-conditional-P'],'source:pbps-exchangeable-pair','B.8 exchangeability'),
 (['source:pbps-exchangeable-pair','source:pbps-macro-micro'],'source:pbps-conditional-leakage','B.9 expected conditional variance; alternate characterization of same leakage, not an extra AND input to B.11'),
 (['source:pbps-standing','source:pbps-positive-eta'],'source:pbps-rho-gap','B.12; alpha eta in (0,1]'),
 (['source:pbps-conditional-density-score','source:pbps-conditional-leakage','source:pbps-standing','source:pbps-rho-gap'],'source:pbps-analytic-contraction','C.1 -> conditional Poincare -> C.2 + marginal Poincare C.3 -> C.4'),
 (['source:pbps-macro-compression','source:pbps-conditional-P'],'source:pbps-centered-macro','B.14 centered compression invariance'),
 (['source:pbps-analytic-contraction','source:pbps-centered-macro','source:pbps-Gamma-definition','source:pbps-rho-gap','source:pbps-positive-root-convention'],'source:pbps-macro-gap','B.15 restricted spectral lower bound'),
 (['source:pbps-macro-gap','source:pbps-Gamma-Gram-energy'],'source:pbps-polar-boundary','B.16 inverse only on H_P,0; not current completion claim')
]
graph={'schema_version':1,'reviewer':'independent_source63','sealed_utc':datetime.now(timezone.utc).isoformat(),'source_primary_raw_sha256':manifest['source_primary']['raw_sha256'],'source_read_before_candidate':True,'candidate_seen':False,'decoder_seen':False,'prior_verdict_seen':False,'scope':'PBPS Appendix B positive macroscopic root, actual compression, leakage/energy identity and root uniqueness; domain separation H_P versus H_P,0; B.15 recorded as coercivity consumer; inverse/polar and full paper excluded from completion','nodes':[{'id':i,'anchor':a,'kind':k,'mathematics':m} for i,a,k,m in nodes],'edges':[{'parents':p,'consumer':c,'consumer_use_site':u,'route_kind':'AND within recorded route'} for p,c,u in edges],'coverage':coverage,'explicit_exclusions':excluded,'extra_primary_regions':extras,'source_gaps':[{'id':'source-gap:analytic-extension','boundary':'The C.1 differentiation and Poincare route needs its actual analytic producer/existence/regularity proof. This reviewer records dependency rather than assuming a quantified derivative/gradient as a new public binder. Current root unit does not establish Appendix C.'}],'alternative_routes':[{'target':'source:pbps-Gamma-Gram-energy','note':'B.5/B.10 positive-root Gram route is sufficient. B.9 conditional-variance description is another characterization, not a necessary extra analytic premise.'}],'source_first_expected_binders':['SOURCE: source parameters V,alpha,beta,eta and admissibility when using the actual-input root','STANDING: real L2(pi_eta), projection and adjoint/spectral conventions','TYPING: carriers and bounded-linear-map types','EXCESS: externally provided root, compression bound, leakage Gram law, square equation, energy estimate, or analytic conclusions as assumptions of an actual-input source anchor'],'domain_audit':['Gamma_P initially on all H_P; restriction to centered H_P,0 must agree through invariance.','Gamma^-1 unavailable on all H_P because constants have eigenvalue one for C and zero root.','Micro output H_perp contains conditional-zero-mean observables, not just total mean zero.','Quotient semantics are almost-everywhere L2; pointwise formulas represent operators, not arbitrary everywhere equality.']}
gsha=put('source-first.graph.sealed.json',graph)
receipt={'reviewer':'independent_source63','phase':'SOURCE_FIRST_GRAPH_SEALED','actual_foreground_preread_complete':True,'executed_utc':datetime.now(timezone.utc).isoformat(),'terminal_region_readbacks':['4f129d: primary 00-11','4b52b7: primary 12-23','a66e14: direct primary root/C4 neighborhoods'],'primary_only_manifest_raw_sha256':digest((OUT/'primary-only.input.manifest.json').read_bytes()),'source_first_graph_raw_sha256':gsha,'all24_literal_regions_read':True,'candidate_seen':False,'decoder_seen':False,'prior_verdict_seen':False}
put('source-first.seal.receipt.json',receipt)
print(json.dumps({'phase':receipt['phase'],'source_first_graph_raw_sha256':gsha,'regions':len(coverage),'nodes':len(nodes),'explicit_exclusions':len(excluded)},indent=2))
