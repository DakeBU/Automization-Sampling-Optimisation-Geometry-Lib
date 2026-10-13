from pathlib import Path
import json,hashlib,copy,datetime
ROOT=Path('E:/Samplinglib');OUT=ROOT/'runs/20261007-companion-priority/pbps-actual-ordered-prefix92/next-source-graph93'
def sha(b):return hashlib.sha256(b).hexdigest()
def bind(p):
 p=Path(p);p=p if p.is_absolute() else ROOT/p;b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'raw_sha256':sha(b),'bytes':len(b)}
def load(n):return json.loads((OUT/n).read_text(encoding='utf8'))
def write(n,x):
 p=OUT/n;assert not p.exists();p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode());return bind(p)
g=load('candidate-source-proof-graph93.native.json');c=load('candidate-source-coverage93.native.json')
provenance=write('source-first-provenance93.v2.native.json',{'record_kind':'source-candidate-internal-adapter-refinement','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'primary':g['primary'],'predecessor':bind(OUT/'source-first-provenance93.native.json'),'trigger':'Independent mathematical review message identified that Gamma only on the simplex is not sufficient to create all-history tests. No future93 implementation or Lean signature read.','independent_source_reasoning':'A1.SS1.p4.2 and A1.E7 demand a functional of the full path. The finite-clock law is a law of complete histories in an ambient total history space; to apply it to that functional, supply a total measurable interpolation of arbitrary finite histories. Source gives only prescribed valid paths, so this adapter is an explicit ASTIS completion, never printed as an author lemma or imported as an assumption.','not_source_authority':'Review feedback locates an omitted interface; its verdict is not evidence of an author claim. The unchanged primary and candidate formula determine scope.','mathematical_target_changed':False,'source_hypotheses_changed':False,'future_implementation_read':False,'accepted_seal':False})
newnode={'id':'HISTPATH93','kind':'ASTIS-total-history-to-path-interpolation','claim':'Construct total measurable Psi_n,T:Hist_n->Path_T. For arbitrary h and s, choose largest j<=n whose record is live(a,z) with a<=s; output Phi_(s-a) z. If no such j exists, output fixed initial phase z0. Finite measurable selection at each s implies product-path measurability. For valid prescribed K_n(t), Psi(K_n(t))=Gamma_n,T(t) pointwise at every s.','source_regions':['A1.SS1.p2','A1.SS1.SSS0.Px1.p4.2','A1.E7'],'status':'PROPOSED_OBLIGATION','boundary':'Arbitrary h may be stopped, unordered or have tied times; largest-index convention and fallback totalize measurably. Their artificial values are used only to define a test, not asserted as actual dynamics. No path-space diagonal measurability assumed.'}
testnode={'id':'TEST93','kind':'ASTIS-admissible-whole-history-path-test','claim':'For every measurable F:Hist_n x Path_T->ENNReal, h->F(h,Psi_n,T(h)) is measurable by product pairing and composition. On C_n it equals F(H_n,Z_T) pointwise; on prescribed K_n it equals F(K_n,Gamma_n,T).','source_regions':['A1.SS1.SSS0.Px1.p4.2','A1.E7'],'status':'PROPOSED_OBLIGATION','boundary':'This internal test adapter is necessary to consume88/92. Gamma measurable only on the simplex would not supply this total history test. No external provider premise.'}
g['nodes'] += [newnode,testnode]
def dep(a,b,why):g['edges'].append({'from':a,'to':b,'logic':'AND','relation':'source-proof-ingredient-not-Lean-edge','consumer_use':why})
for a in ['O93','M93','PATHSPACE93']:dep(a,'HISTPATH93','Finite Borel live/time selection and harmonic interpolation into coordinate product path space.')
dep('HISTPATH93','PATHM93','Construct total history interpolation first; Gamma=Psi composed withK, actualZ coordinatewise measurable.')
dep('HISTPATH93','IDENT93','Pointwise extension equality Psi(K)=Gamma and onC Psi(H)=actual path.')
for a in ['HISTPATH93','IDENT93','PATHM93']:dep(a,'TEST93','Total measurable history test and pointwise valid-history/path substitution.')
dep('TEST93','JOINT93','Apply survived history law to F(h,Psi(h)), then substitute K/Gamma and actual paths.')
for n in g['nodes']:
 if n['id']=='PATHM93':n['claim']='Total measurable Psi_n,T on ambient histories gives Gamma_n,T=Psi_n,T composed withK_n. Joint measurableZ gives measurable sample->Z_T by coordinate evaluations. No path-space diagonal theorem needed.'
 if n['id']=='IDENT93':n['claim']='For every raw w in measurable C_n, observed strict tuple t satisfies H_n=K_n(t) and Psi_n,T(H_n(w))=Z_T(w)=Gamma_n,T(t), by pointwise equality for every s<=T. Do not represent this as a measurable equality event in an uncountable product.'
g['node_count']=len(g['nodes']);g['edge_count']=len(g['edges']);g['source_first_provenance']=provenance
g['AND_routes'][0]['required'].append('TEST93')
g['version']=2;g['predecessor']=bind(OUT/'candidate-source-proof-graph93.native.json')
g['refinement']={'added_internal_nodes':['HISTPATH93','TEST93'],'target_formula_unchanged':True,'no_extra_public_premise':True,'source_gap':'Source prescribes valid paths, but does not print a total ambient-history path map. This is an explicit finite measurable completion needed for whole-path test transport.','no_diagonal_claim':'Use measurable C_n and pointwise extensional identities, not measurability of the equality relation in Path_T x Path_T.'}
graph=write('candidate-source-proof-graph93.v2.native.json',g)
for row in c['coverage']:
 if row['id'] in ['C93-20','C93-21','C93-48','C93-50','C93-52','C93-53']:
  row['nodes'] += [x for x in ['HISTPATH93','TEST93'] if x not in row['nodes']]
  row['node_statuses'].update(HISTPATH93='PROPOSED_OBLIGATION',TEST93='PROPOSED_OBLIGATION')
  row['reason'] += ' Total ambient-history interpolation Psi and measurable F(h,Psi(h)) are explicit internal adapters; no measurable diagonal of Path_T is assumed.'
c['coverage'].append({'id':'C93-55','predecessor_row':None,'source_region':g['source_regions']['A1.SS1.SSS0.Px1.p4.2'],'source_content':'A whole-path observable must become an admissible observable on every ambient finite history to consume the finite-clock law.','disposition':'SOURCE_GAP','nodes':['HISTPATH93','TEST93'],'reason':'Author defines prescribed valid paths but omits total history-space interpolation. Finite last-eligible-live-index selection with initial-phase fallback yields a measurable total Psi, agreeing with Gamma onK and withZ onC. It adds no assumption and needs no diagonal-measurability claim.','node_statuses':{'HISTPATH93':'PROPOSED_OBLIGATION','TEST93':'PROPOSED_OBLIGATION'},'no_proof_credit':True})
c['graph']=graph;c['coverage_count']=len(c['coverage']);c['version']=2;c['predecessor']=bind(OUT/'candidate-source-coverage93.native.json')
c['bounded_exhaustiveness']='All46 predecessor selected-source subclaims retained and re-dispositioned plus9 finer explicit path/count/endpoint/extension/total-history-test obligations. Bounded selected-source exhaustiveness, not whole-paper coverage.'
coverage=write('candidate-source-coverage93.v2.native.json',c)
prev=load('closed-RAW-source-graph93.native.json');inputs=prev['inputs']+prev['outputs']+[bind(OUT/'closed-RAW-source-graph93.native.json')]
manifest=write('closed-RAW-source-graph93.v2.native.json',{'record_kind':'closed-source-candidate-graph-internal-adapter-successor','inputs':inputs,'outputs':[provenance,graph,coverage,bind(OUT/'refine-history-adapter93.py')],'closure':'All inputs and outputs rehashed. Original graph/coverage/provenance/manifest preserved. Planning only; no statement seal, proof credit, code or canonical-state mutation.'})
for i in inputs+[provenance,graph,coverage,bind(OUT/'refine-history-adapter93.py')]:assert bind(i['path'])==i
print(json.dumps({'graph':graph,'coverage':coverage,'provenance':provenance,'manifest':manifest,'counts':[g['node_count'],g['edge_count'],c['coverage_count']]},indent=2))
