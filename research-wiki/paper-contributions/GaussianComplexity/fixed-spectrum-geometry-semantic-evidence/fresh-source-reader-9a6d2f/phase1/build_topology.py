from pathlib import Path
from html.parser import HTMLParser
import json
OUT=Path(__file__).parent
nodes=[];edges=[]
def node(id,anchors,kind,claim):
 nodes.append(dict(id=id,anchors=anchors,kind=kind,claim=claim))
def edge(a,b,use,role):edges.append(dict(producer=a,consumer=b,consumer_use_site=use,role=role))
node('model.geometry',['S2.p1.1'],'definition','Euclidean norm, identity and symmetric Loewner order.')
node('model.orthogonal',['S2.p2.1'],'definition','O(d) is the full real orthogonal group O^T O=I; Haar is a probability measure. Its two determinant components are context, not a restriction on C.4.')
node('model.class',['S2.SS0.SSS0.Px1.p1.1','S2.Ex1'],'definition','Normalized precision class at integer d>=1 and kappa>=1: symmetric A with I<=A<=kappa I.')
node('model.quadratic_target',['S2.SS0.SSS0.Px1.p1.2'],'definition','f_A=x^TAx/2 and pi_A=N(0,A^{-1}).')
node('model.reply',['S2.E1'],'definition','Exact first-order response is (x^TAx/2,Ax).')
node('model.oracle_equivalence',['S2.SS0.SSS0.Px1.p2.1'],'source-argument','Reply contains Ax; x and Ax determine scalar value, so exact value-gradient, gradient-only and matvec query complexities coincide.')
node('model.algorithm',['S2.SS0.SSS0.Px2.p1.1'],'definition','Independent private randomness; Borel adaptive query/stopping/output functions; every-input every-seed deterministic query cap.')
node('model.accuracy',['S2.SS0.SSS0.Px4.p1.1','S2.E2','S2.SS0.SSS0.Px4.p1.2'],'definition','Output law averages seed; uniform per-input TV accuracy; infimum over integer deterministic caps, not expected-query budgets.')
node('hard.grid',['S4.SS1.p1.1','S4.E11'],'literal-definition','At integer d>=2,kappa>=2, theta_i=(i-1/2)pi/d; lambda_i=(kappa+1)/2+(kappa-1)cos(theta_i)/2, i=1,...,d; Lambda=diag(lambda_i).')
node('hard.rotation',['S4.SS1.p1.2'],'literal-definition','A=O Lambda O^T; hard prior Haar O independent of algorithm seed, with quadratic potential and Gaussian target.')
node('hard.public_spectrum',['S4.SS1.p2.1'],'source-context','Deterministic spectrum may be supplied to the algorithm; normalizer is known; eigenbasis is hidden.')
node('hard.construction_citation',['S4.SS1.p1.1#citation[22]','bib.bib3'],'external-citation-provenance','OpenAI 2026 preprint, source citation [22], Section 9.2. Identified only; not opened or used as a C.4 proof premise.')
node('lemma.admissibility',['S4.Thmtheorem6','S4.Thmtheorem6.p1.1'],'source-statement','For every orthogonal O, A=O Lambda O^T satisfies I<=A<=kappa I.')
node('c4.angle_eigenvalues',['A3.SS4.p1.1'],'source-proof-step','Actual grid gives 0<theta_i<pi, then -1<cos(theta_i)<1, then 1<lambda_i<kappa.')
node('c4.matrix_bounds',['A3.SS4.p1.1'],'source-proof-step','Orthogonal conjugation gives I<=A<=kappa I.')
node('c4.smooth_geometry',['A3.SS4.p2.1'],'source-proof-step','Quadratic V_A is C-infinity, Hessian A, 1-strongly convex and kappa-smooth.')
node('c4.unique_minimum',['A3.SS4.p2.1'],'source-proof-step','V_A(0)=0 and V_A(x)>=||x||^2/2>0 for x!=0, so 0 is its unique minimizer.')
node('c4.gaussian_target',['A3.SS4.p3.1'],'source-proof-step','Associated normalized target is N(0,A^{-1}).')
node('c4.normalizer',['A3.Ex160'],'source-proof-step','Z_A=(2pi)^(d/2)(det A)^(-1/2)=(2pi)^(d/2)(det Lambda)^(-1/2).')
node('c4.normalizer_public',['A3.SS4.p3.2'],'source-proof-step','Fixed Lambda makes Z_A independent of O and known when spectrum is public.')
node('consumer.uniform_accuracy',['S4.SS3.p2.1'],'downstream-use-site','Theorem4.1 assumes uniform TV guarantee over admissible inputs; Lemma4.6 makes the hard family admissible.')
node('bg.angle_cosine',['A3.SS4.p1.1'],'SOURCE_GAP:standard-background-omitted','Index arithmetic, positivity of pi, strict cosine range and positive affine coefficient; not added source premises.')
node('bg.orthogonal_order',['A3.SS4.p1.1'],'SOURCE_GAP:standard-background-omitted','Square orthogonal inverse/norm identities, diagonal quadratic bounds, symmetry, conjugation/order and positive definiteness.')
node('bg.quadratic_calculus',['A3.SS4.p2.1'],'SOURCE_GAP:standard-background-omitted','Symmetric quadratic derivatives, polynomial smoothness and equivalence between Hessian bounds and Euclidean convexity/smoothness.')
node('bg.gaussian_integral',['A3.SS4.p3.1','A3.Ex160'],'SOURCE_GAP:standard-background-omitted','Positive-definite Gaussian integration with Lebesgue base measure, finite positive normalizer and inverse-precision covariance.')
node('bg.determinant',['A3.Ex160'],'SOURCE_GAP:standard-background-omitted','det(O Lambda O^T)=(det O)^2 det Lambda=det Lambda>0, including det O=-1.')
node('bg.fixed_reply_borel',['S2.E1'],'derived-background-only','Finite-dimensional polynomial reply and continuous reply-conversion maps are Borel for fixed A. Not an expressly stated C.4 claim or an adaptive/probability theorem.')
edge('hard.grid','c4.angle_eigenvalues','A3.SS4.p1.1','actual grid is used, not arbitrary supplied eigenvalue bounds')
edge('bg.angle_cosine','c4.angle_eigenvalues','A3.SS4.p1.1','omitted elementary inference')
edge('c4.angle_eigenvalues','c4.matrix_bounds','A3.SS4.p1.1','diagonal spectral bounds')
edge('hard.rotation','c4.matrix_bounds','A3.SS4.p1.1','orthogonal conjugation formula')
edge('model.geometry','c4.matrix_bounds','A3.SS4.p1.1','Loewner-order meaning')
edge('model.orthogonal','c4.matrix_bounds','A3.SS4.p1.1','orthogonality definition; Haar law unused')
edge('bg.orthogonal_order','c4.matrix_bounds','A3.SS4.p1.1','omitted linear-algebra bridge')
edge('c4.matrix_bounds','lemma.admissibility','A3.SS4.p1.1','author proof establishes displayed lemma')
edge('model.quadratic_target','c4.smooth_geometry','A3.SS4.p2.1','same defined quadratic, denoted V_A here')
edge('c4.matrix_bounds','c4.smooth_geometry','A3.SS4.p2.1','Hessian bounds')
edge('bg.quadratic_calculus','c4.smooth_geometry','A3.SS4.p2.1','omitted derivative/curvature bridge')
edge('c4.matrix_bounds','c4.unique_minimum','A3.SS4.p2.1','lower quadratic bound')
edge('model.quadratic_target','c4.unique_minimum','A3.SS4.p2.1','value at zero')
edge('c4.matrix_bounds','c4.gaussian_target','A3.SS4.p3.1','positive-definite precision')
edge('model.quadratic_target','c4.gaussian_target','A3.SS4.p3.1','source target definition')
edge('bg.gaussian_integral','c4.gaussian_target','A3.SS4.p3.1','normalized quadratic Gaussian identification')
edge('c4.matrix_bounds','c4.normalizer','A3.Ex160','positive definiteness discharges integrability/determinant positivity')
edge('bg.gaussian_integral','c4.normalizer','A3.Ex160','Gaussian integration route')
edge('hard.rotation','c4.normalizer','A3.Ex160','conjugation form')
edge('bg.determinant','c4.normalizer','A3.Ex160','second equality and positivity')
edge('c4.normalizer','c4.normalizer_public','A3.SS4.p3.2','normalizer depends only on fixed spectrum')
edge('hard.public_spectrum','c4.normalizer_public','A3.SS4.p3.2','public information convention; no computation-cost theorem')
edge('lemma.admissibility','consumer.uniform_accuracy','S4.SS3.p2.1','discharges hard-input membership needed by uniform TV assumption')
edge('model.class','consumer.uniform_accuracy','S4.SS3.p2.1','range of uniform accuracy guarantee')
edge('model.accuracy','consumer.uniform_accuracy','S4.SS3.p2.1','per-input output-law TV premise')
edge('model.reply','model.oracle_equivalence','S2.SS0.SSS0.Px1.p2.1','exact reply conversion uses known query x')
edge('model.reply','bg.fixed_reply_borel','S2.E1','elementary consequence of polynomial formula, not source algorithm construction')

# Exact raw-source inventory at theorem, substantive-paragraph, and display granularity.
# A node's paragraph anchor also covers the corresponding ltx_para container.
coverage={}
for n in nodes:
 for a in n['anchors']:coverage.setdefault(a,[]).append(n['id'])
class Inventory(HTMLParser):
 def __init__(self):super().__init__();self.items=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);classes=a.get('class','').split();id=a.get('id')
  if not id:return
  kind=None
  if 'ltx_para' in classes:kind='substantive-paragraph'
  elif 'ltx_theorem' in classes:kind='theorem-or-remark'
  elif 'ltx_equation' in classes or 'ltx_equationgroup' in classes:kind='display'
  elif 'ltx_bibitem' in classes:kind='bibliography-entry'
  if kind:self.items.append((id,kind))
inv=[]
for stem in ['S2','S4.intro','S4.SS1','S4.SS2','A3.SS4','S4.SS3','bib.bib3']:
 p=Inventory();p.feed((OUT/(stem+'.raw.html')).read_text())
 for a,k in p.items:
  ids=list(coverage.get(a,[]))
  if k=='substantive-paragraph':
   ids += [n['id'] for n in nodes if any(x.startswith(a+'.') for x in n['anchors'])]
  ids=sorted(set(ids))
  if ids:rec={'anchor':a,'kind':k,'disposition':'NODE','node_ids':ids}
  else:
   if stem=='S2':reason='TV definition/inequality context is captured, but not a prerequisite of C.4 or of fixed-reply continuity; full probability proofs are out of phase1 local scope.'
   elif stem=='S4.intro':reason='Theorem4.1 and introductory comparison are downstream lower-bound context; their parameter restrictions are not premises of C.4.'
   elif stem=='S4.SS1':reason='Remark4.2 compares kappa=2 and describes downstream statistic behavior; it is not used in C.4. Its statement remains preserved in the raw/readable excerpt.'
   elif stem=='S4.SS2':reason='Sibling Krylov/concentration/target-moment statement or explanatory paragraph; separate input to Theorem4.1, not an input to C.4. No proof of Lemmas4.3-4.5 is being reconstructed.'
   elif stem=='S4.SS3':reason='Downstream lower-bound test/statistic, probability, moment, asymptotic bookkeeping or contradiction; captured to identify actual use, not part of C.4 proof. Only p2 is the local admissibility consumer.'
   else:raise RuntimeError('uncovered primary source '+a)
   rec={'anchor':a,'kind':k,'disposition':'EXCLUDED','reason':reason}
  inv.append(dict(excerpt=stem,**rec))
# C.4 paragraph p3 contains text before and after display; retain both nodes.
for r in inv:
 if r['anchor']=='A3.SS4.p3':r['node_ids']=sorted(set(r['node_ids']+['c4.normalizer_public']))
# C.4 proof has no external citation. Explicit citation coverage for construction.
inv.append({'excerpt':'S4.SS1','anchor':'S4.SS1.p1.1#citation[22]','kind':'external-citation','disposition':'NODE','node_ids':['hard.construction_citation']})
obj={'phase':'1-source-only','status':'frozen-source-reconstruction-no-fidelity-verdict','scope':'C.4 with literal hard input and Section2 model, bounded raw neighbors and actual downstream use','nodes':nodes,'edges':edges,'source_inventory':inv,'routes':[{'target':'lemma.admissibility','route':'C.4 angle -> cosine -> eigenvalue -> orthogonal-order route','logic':'single sufficient route; no alternative routes identified in local raw proof'}],'non_edges':['No edge from Lemma4.3,4.4,4.5 or C.1-C.3 to C.4.','No edge from Theorem4.1 parameter/query constraints back into C.4.','Construction citation [22] is provenance, not an unquoted necessary C.4 theorem.','C.4 normalizer/minimizer conclusions have no explicit use cited in Section4.3.','Fixed-reply Borel continuity is not an adaptive algorithm, joint random-input law, probability bound or cost theorem.'],'review_boundary':'This is one independent reader source-only reconstruction. No self-VERIFIED lifecycle action, Lean acceptance, final source-fidelity decision or independent approval of this topology is asserted.'}
(OUT/'source_topology.json').write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'nodes':len(nodes),'edges':len(edges),'inventory_items':len(inv),'NODE':sum(x['disposition']=='NODE' for x in inv),'EXCLUDED':sum(x['disposition']=='EXCLUDED' for x in inv)}))
