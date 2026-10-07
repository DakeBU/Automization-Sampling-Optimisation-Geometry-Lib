from pathlib import Path
import json,hashlib
from datetime import datetime,timezone
R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/gaussian-product-entropy-preproof-review';C=R/'runs/20261007-companion-priority/gaussian-product-entropy-preproof'
H=lambda b:hashlib.sha256(b).hexdigest()
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def put(n,b):
 with (O/n).open('xb') as f:f.write(b)
pins=[]
for i,p in enumerate([C/'signature.prospective.txt',C/'root.statement-proposal.json',C/'StatementProbe.lean',C/'typecheck.0.log',O/'primary.contract.json',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Function/L1Space/Integrable.lean',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Prod.lean']):
 b=p.read_bytes();l=b.replace(b'\r\n',b'\n').replace(b'\r',b'\n');n=f'statement.input.{i:02d}'
 put(n+'.raw.snapshot',b);put(n+'.lf.snapshot',l);pins.append({'path':p.relative_to(R).as_posix(),'raw_sha256':H(b),'lf_sha256':H(l),'bytes':len(b),'raw_snapshot':n+'.raw.snapshot','lf_snapshot':n+'.lf.snapshot'})
sig=(C/'signature.prospective.txt').read_text(encoding='utf8');probe=(C/'StatementProbe.lean').read_text(encoding='utf8');assert len(sig.encode())==1029;assert H(sig.encode())=='4c3634612a055d16e4aec0516823192db42307ac1330ae4bddb88b959a436b0d'
body=sig.split('\n',1)[1];binders,concl=body.split(' :\n',1)
expected='#check (∀ '+binders+',\n'+concl+' : Prop)'
assert expected in probe
assert 'theorem ' not in probe and 'sorry' not in probe and ':= by' not in probe
log=(C/'typecheck.0.log').read_text(encoding='utf8');assert ': Prop' in log and 'error:' not in log
slots={'objects':'μ,ν actual probability measures; measurable F on X×Y. Phi=t*log(t), A=actual ν slice integral, B=actual μ slice integral, m=actual product integral.',
 'quantifiers':'Arbitrary measurable types, every pair of actual probability laws and actual pointwise bounded nonnegative measurable F. Every x and every y slice, not merely AE, because pointwise assumptions hold at every fixed parameter.',
 'hypotheses':'MeasurableSpace X/Y; IsProbabilityMeasure μ/ν; Measurable F; pointwise F>=0; ∃ real upper bound. No desired inequality, L1, kernel, positive fiber/mass, normalization or Gaussian premise.',
 'domains':'Real Bochner integrals with all joint/FlogF/slice/marginal domains in conclusion. C may be replaced internally by max(C,0). Probability implies finite and SFinite laws. Scalar real Borel/complete Banach space are canonical.',
 'constants':'Loss-free marginal inequality; no LSI constant introduced. Phi(0)=0 via Real.log0=0. Later Gaussian function LSI coefficient2 is not an output here.',
 'conclusion':'J_A+J_B <= J_F+Phi(m), with all listed integrability outputs. Equivalent binary entropy subadditivity needs actual Fubini and subtraction using these domains. Conditional outer entropy L1 is derivable bounded-domain work but not explicitly an output of this signature.',
 'scope':'Authored bounded heterogeneous binary product background sufficient for later compact C2 g²; narrower bounded class and stronger pointwise hypotheses than external unbounded AE SLT source. Not printed SPHMC theorem or finite tensorization/full GaussianLSI/T2.'}
classification=[{'binder':'X,Y : Type*','kind':'TYPECLASS_CONTEXT','expansion':'Arbitrary measurable carriers; no metric/topology/dimension.'},
 {'binder':'MeasurableSpace X,Y','kind':'TYPECLASS','expansion':'Product sigma algebra and canonical real Borel structure.'},
 {'binder':'μ,ν','kind':'OBJECT','expansion':'Actual laws; not supplied desired-property witnesses.'},
 {'binder':'IsProbabilityMeasure μ,ν','kind':'TYPECLASS_SOURCE_BACKGROUND','expansion':'Source independent probability-product setting; finite/SFinite/mass1 derived.'},
 {'binder':'F','kind':'OBJECT','expansion':'Actual product observer.'},
 {'binder':'hF','kind':'SOURCE_BACKGROUND','expansion':'Real-valued joint measurability, canonical strong measurability; every section measurable by fixed-coordinate composition.'},
 {'binder':'hF0','kind':'AUTHORED_GENERIC_CLASS_RESTRICTION','expansion':'Pointwise nonnegative rather than source AE; needed all-slice output. Signed g allowed through F=g².'},
 {'binder':'hFb','kind':'AUTHORED_GENERIC_CLASS_RESTRICTION','expansion':'Existential actual real upper bound, not inequality certificate. Consumer compact continuous g² must produce it internally; no public source Gaussian bound premise licensed.'},
 {'binder':'Phi,A,B,m','kind':'DEFINITION','expansion':'Literal actual real log/marginals/mass; no RN representative or posterior reinterpretation.'},
 {'binder':'all L1/bounds/positive regularization/inequality','kind':'DERIVED_INTERNAL','expansion':'No such caller binder exists.'}]
route=['Choose C0=max(C,0), derive section and joint measurability/bounds and true L1; bound continuous Phi on [0,C0]. Produce measurable bounded A/B and their Phi L1.',
 'Set δn=1/(n+1)>0 and Fn=F+δn. Probability/Fubini give An=A+δn,Bn=B+δn,mn=m+δn, all in [δn,C0+δn].',
 'Rn=An*Bn/mn is positive with fixed-n upper/lower bounds; ∫Rn=mn. All log-weighted terms genuinely L1.',
 'Integrate Fn log(Fn/Rn)-Fn+Rn>=0 from x-1<=x logx; log expansion plus Fubini gives J_An+J_Bn<=J_Fn+Phi(mn).',
 'Use uniform Phi bounds on [0,C0+1] and continuous tlogt to pass four entropy terms by bounded DCT. Cross-log terms are never passed near zero.',
 'Assemble all outputs including zero functions/fibers/mass; no positive lower bound on original F.',
 'Later entropy-chain/finite-coordinate iteration plus conditional compact scalar LSI, Hilbert transport/cutoff and actual32/33 consumer are distinct open assembled nodes.']
review={'schema_version':1,'verdict':'ACCEPTED_EXACT_PROSPECTIVE_STATEMENT_ONLY','status':'accepted-scoped-statement-only','reviewer':'gaussian_domain_preproof_reviewer_29','independent_of_statement_author':True,
 'primary_first_contract':'primary.contract.json','primary_first_hash':pins[4]['raw_sha256'],'declaration':'AutoSamplingTheory.TechnicalLemmas.InformationTheory.ProductEntropy.bounded_product_entropy_subadditivity','signature_raw_LF_sha256':pins[0]['raw_sha256'],'signature_bytes':1029,
 'seven_slots':slots,'binder_classification':classification,'source_excess':0,'convenience_output_certificates':0,'blockers':[],
 'type_only_evidence':{'exact_forall_transformation':True,'root_reported_exit_code':0,'log_contains_Prop_and_no_errors':True,'probe_has_no_theorem_body_or_placeholder':True,'named_declaration_elaborated':False,'reviewer_compiler_started':False,'boundary':'Root anonymous-proposition typecheck evidence only. No namespace/named statement compilation or mathematical proof credit.'},
 'mathematical_validity':'Loss-free inequality is equivalent to entropy subadditivity. Positive regularized independent product density R has mass m; scalar logsum yields correct sign. Bounded Phi DCT includes m=0/zero fibers without passing cross logs. Pointwise bound justifies every slice L1.',
 'source_scope':'SPHMC first4.6 invokes omitted GaussianLSI/T2. External SLT gives general finite homogeneous probability-product entropy subadditivity with AE nonnegative and supplied actual L1 domains. This is authored bounded heterogeneous binary integration with domains produced internally, not a literal port or completed paper result.',
 'authored_route_at_most_seven_steps':route,'remaining_boundary':['source graph independent topology admission','actual implementation/focused tests/independent whole math/source review','finite-coordinate entropy assembly','compact Gaussian product LSI/Hilbert/noncompact cutoff','Gaussian T2/FIRST4.6/paper main/work/cost'],
 'inputs':pins,'primary_source_API_27_pins':'primary.contract.json','source_graph_selfvalidation':False,'canonical_mutations':False,'leases':{'read':'CLOSED','write':'CLOSED','Python':'CLOSED','compiler':'CLOSED'}}
put('statement.review.json',enc(review));run={'inputs':pins,'review_sha256':H(enc(review)),'compiler_started':False};run['run_sha256']=H(enc(run));put('run.json',enc(run))
lease=json.loads((O/'lease.json').read_text());lease.update({'status':'CLOSED','read_lease':'CLOSED','write_lease':'CLOSED','Python_lease':'CLOSED','candidate_stage':'CLOSED','review_sha256':H(enc(review)),'run_sha256':run['run_sha256'],'closed_utc':datetime.now(timezone.utc).isoformat()});(O/'lease.json').write_bytes(enc(lease))
print(json.dumps({'verdict':review['verdict'],'review_sha256':H(enc(review)),'run_sha256':run['run_sha256'],'leases':'CLOSED'}))
