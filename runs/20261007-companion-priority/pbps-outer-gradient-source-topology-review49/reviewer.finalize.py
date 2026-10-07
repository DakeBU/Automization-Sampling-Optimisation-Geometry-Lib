import json, hashlib
from pathlib import Path
from datetime import datetime, timezone

BASE=Path('E:/Samplinglib')
R=BASE/'runs/20261007-companion-priority/pbps-outer-gradient-sourcegraph49'
O=BASE/'runs/20261007-companion-priority/pbps-outer-gradient-source-topology-review49'
def sha(b): return hashlib.sha256(b).hexdigest()
def canon(d): return json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def get(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,d): p.write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
def pin(p):
 b=p.read_bytes(); return {'path':p.as_posix(),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n')),'bytes':len(b)}
bindings=get(R/'input-bindings.json'); providers=get(R/'selected-providers.json')
g=get(R/'source-proof-graph.json'); callers=get(R/'caller-inventory.json')['entries']
inputs=[]
for x in bindings:
 p=Path(x['path']); v=pin(p)
 assert v['raw_sha256']==x['whole_raw_sha256'] and v['lf_sha256']==x['whole_lf_sha256'], x['id']
 v['input_id']=x['id'];v['semantic_scope']='selected fragment only; whole-file hash does not assert whole-file reading'
 inputs.append(v)
 for suffix,key in [('.raw','fragment_raw_sha256'),('.lf','fragment_lf_sha256')]:
  p=R/(x['snapshot']+suffix);assert sha(p.read_bytes())==x[key],p
  dest=O/('frozen-'+x['snapshot']+suffix)
  assert not dest.exists();dest.write_bytes(p.read_bytes())
  v=pin(p);v['reviewer_snapshot']=dest.as_posix();inputs.append(v)
artifact_names=['source-proof-graph.json','source-coverage.json','caller-inventory.json','selected-token-inventory.json','selected-providers.json','primary-balanced-inventory.json','input-bindings.json','hypothesis-contract.json','sourcecontract.json','schema-and-boundary.md','capsule.md','run.json','lease.json']
for name in artifact_names:
 p=R/name;inputs.append(pin(p));dest=O/('frozen-'+name);assert not dest.exists();dest.write_bytes(p.read_bytes())
for rel in ['phase-pbps-primary-preread49/primary.contract.json','phase-pbps-primary-preread49/reviewer.primary.lease.json','pbps-outer-gradient-preproof-review49/statement.review.json','pbps-outer-gradient-preproof-review49/reviewer.statement.lease.json']:
 p=BASE/'runs/20261007-companion-priority'/rel
 if p.exists():inputs.append(pin(p))
byte_fail=[]; edge_boundary=[]; named=0
for x in callers:
 if 'caller_start_utf8_byte0' not in x:continue
 named+=1
 b=Path(x['caller_path']).read_bytes()[x['caller_start_utf8_byte0']:x['caller_end_utf8_byte0_exclusive']]
 if b!=x['token'].encode():byte_fail.append(x)
 if not any(e['from_node']==x['resolved_node'] and e['to_node']==x['caller_node'] for e in g['edges']):edge_boundary.append(x)
assert not byte_fail
need=[('additional-P.mean-bound',967,'∫','P.integral','P.mean-bound'),('additional-P.map-prob',125,'map','P.map','P.map-prob'),('additional-P.map-prob',125,'IsProbabilityMeasure','P.prob','P.map-prob'),('additional-P.compact-bound',158,'HasCompactSupport','P.typing','P.compact-bound'),('api-P.var-sub',225,'variance','P.mathlib-variance','P.var-sub'),('api-P.var-sub',225,'μ[X','P.integral','P.var-sub')]
for provider,node in [('parent-context-GibbsAugmentation','A.Gibbs'),('parent-context-GaussianReflection','A.reflection')]:
 for token in ['NormedAddCommGroup','InnerProductSpace','FiniteDimensional','MeasurableSpace','BorelSpace']:
  pr=next(x for x in providers if x['id']==provider);lines=Path(pr['path']).read_text(encoding='utf-8').splitlines()
  line=next(n for n in range(pr['selected_physical_lines1'][0],pr['selected_physical_lines1'][1]+1) if token in lines[n-1])
  need.append((provider,line,token,'P.typing',node))
missing=[]
for provider,line,token,src,dst in need:
 p=next(x for x in providers if x['id']==provider);raw=Path(p['path']).read_bytes(); rows=raw.splitlines(keepends=True);rb=rows[line-1]
 column=rb.index(token.encode());offset=sum(map(len,rows[:line-1]))+column
 assert p['start_utf8_byte0']<=offset<offset+len(token.encode())<=p['end_utf8_byte0_exclusive']
 assert not any(x.get('caller_selected_provider')==provider and x.get('caller_start_utf8_byte0')==offset for x in callers)
 missing.append({'provider_id':provider,'path':p['path'],'physical_line1':line,'token':token,'byte_interval0':[offset,offset+len(token.encode())],'from_node':src,'to_node':dst,'kind':'typing-reference' if src=='P.typing' else 'semantic-public-contract-reference','not_implementation_call':True})
checks={'existing_named_caller_count':named,'exact_byte_failures':byte_fail,'existing_edge_free_typing_self_references':edge_boundary,'missing_public_contract_references':missing,'unqualified_map_and_variance_aliases_require_actual_resolution':True,'independent_math_route_change_required':False,'kernel_compProd_is_not_independent_Measure_prod':'The selected IsCondKernel/Fubini contracts already describe the kernel product; preserve this distinction, do not conflate with P.prod.'}
save(O/'direct-call.checks.json',checks)
repairs=[
 {'id':'T1','class':'SOURCE_COVERAGE_EXPOSURE_REPRESENTATION','locations':['selected-P.fderiv-context2','Measurable.lean:361-368','source-coverage.json','caller-inventory.json','schema-and-boundary.md','source-proof-graph.json edge245'], 'finding':'The frozen purported typing context contains an unrelated theorem and its simp/aesop proof. All eight non-typing rows are currently NODE/P.typing, while raw mathematical proof bodies selected is asserted zero.', 'minimal_repair':'Retain original bytes; classify rows361-368 as explicitly excluded unrelated theorem/proof, or restrict the semantic typing selection to358-359 and370 while retaining incidental raw exposure. Disclose raw proof presence separately from zero semantic proof expansion. Reclassify/remove edge245 and the line364 references as excluded-fragment rather than P.typing mathematical coverage. No proof port or theorem change.'},
 {'id':'T2','class':'DIRECT_PUBLIC_CONTRACT_REFERENCE_CLOSURE','locations':['caller-inventory.json','selected-token-inventory.json','source-proof-graph.json'], 'finding':'Three additional primitive fragments and two parent typing contexts were omitted from the declared configured reference inventory; plain map/variance and expectation notation also escape namespace-only matching.', 'required_references':missing,'minimal_repair':'Record these exact already-selected references and honest ingredient/typing edges. Typing self-references may remain explicitly non-edge boundaries; no fake cycles or implementation callers. Preserve scalar mean-bound mass and kernel-product semantics as actual unexpanded contracts, not independent-product substitutions. Norm references may be grouped in the declared semantic family; do not claim unexpanded proofs.'},
 {'id':'T3','class':'PRINTED_SOURCE_ROW_CLASSIFICATION','locations':['source-coverage.json primary physical4574 A3.SS1.p1.1'], 'finding':'The literal B.13 target citation and It suffices to consider proof-class transition is incorrectly EXCLUDED as HTML/layout, despite existing source-use edges253-255 anchored to that very row.', 'minimal_repair':'Classify the substantive row NODE for the existing compact/rough/operator source context, or give an honest explicit outside-target mathematical exclusion; retain its literal citation edges and density/closedness residual. No new source premise.'}
]
def slot(original,reconstructed,evidence):return {'original':original,'reconstructed':reconstructed,'relation':'faithful-bounded-source-contract; topology representation blocked separately','evidence':evidence}
slots={
 'objects':slot('Actual normalized Gibbs mu, augmentation J, nu=J.snd, common posterior R and reflected S, Tf and centered fiber variance.','Same actual laws and one common R/S; no arbitrary law/kernel certificate.','Selected printed law/reflection anchors and three opaque public headers bind actual objects.'),
 'domains':slot('Source smooth compact signed real f; all probability, differentiation, L2 and variance-L1 facts must be produced.','Finite real Hilbert/Borel, including rank zero, explicitly extends Euclidean representation; outer nu domains, not fiber D_y.','Target1795 and internal domain/Fubini/map obligations; B.13 closure is outside target.'),
 'quantifiers':slot('Source model and step precede common R/S; all smooth compact f then actual outer conclusions.','One common R/S before all f; every-y reflected density, no AE arbitrary kernel version.','Sealed prospective header and I.same witness-coherence node.'),
 'assumptions':slot('C2 V, positive alpha<=beta and source eta cap; signed compact smooth f.','Only source/standing/typing binders. No mean zero, nontriviality, domain, covariance or inequality premise.','Own primary-first contract and independently accepted StatementSeal; no EXCESS found.'),
 'conclusion':slot('Integrated C.2 scalar gradient bound and exact variance defect.','Probability outputs, true differentiability/L2, variance L1/defect identity, eta gradient energy bound with (1-alpha eta)^2/[4(1+alpha eta)].','Graph integration order produces domains before integral algebra; no source theorem proof is admitted here.'),
 'scopes':slot('C.1 compact analytic proof ingredient; source extends B.13 via density/closedness.','Compact scalar target only; rough all-L2/H1, literal Gamma/operator adapter, C.2 half-turn and main/cost remain open.','R.rough/R.operator truth cuts retained; source representation T3 must be corrected.'),
 'constant_dependencies':slot('Exact reflected quarter scaling and eta*(gradient energy) coefficient.','Same source coefficient, squared factor nonnegative including alpha eta=1, dimension-zero not excluded.','I.algebra/I.rankzero and source C.2 anchor; no RGO scale substitution.')}
receipt={'schema_version':1,'actor':'phase_source_reviewer_20261005','status':'BLOCKED_SOURCE_TOPOLOGY_REPRESENTATION','verdict':'blocked','blocking':True,'scope':'Independent implementation-free source-only topology49; not mathematical proof, future source fidelity or SAU admission','independent_from_graph_creator':True,'independent_from_formalizer':True,'independent_from_decoder':True,'source_primary_before_target':True,'exposure':{'historical48_source_and_body':True,'own49_primary_and_statement_reviews':True,'current49_implementation_Test_blind_math_verdict':False,'incidental_selected_unrelated_Mathlib_proof':True,'note':'No49 body exists/read. T1 records the incidental external proof exposure honestly.'},'graph_counts':{'nodes':len(g['nodes']),'edges':len(g['edges']),'or_routes':len(g['or_routes']),'selected_physical_rows':229,'NODE':153,'EXCLUDED':76,'selected_providers':30,'primary_balanced_anchors':20,'strict_inputs':37,'caller_entries':len(callers),'configured_token_occurrences':144},'primary_sha256':'d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760','exact_statement_lf_sha256':'f37b4a07e62e16d22f4ecbc1fba9c38fd80d42f947011b38ded7c5153e0bea1d','semantic_slots':slots,'source_excess':[],'mathematical_statement_deltas':[],'deltas':repairs,'repairs':repairs,'review_evidence':'All37 live whole raw/LF and37 frozen fragment raw/LF bindings match; all20 canonical balanced source outer spans and30 selected provider spans match; independent229-row union and row hashes are exact. All140 existing byte-addressed named callers match raw tokens. The chosen common R/S integration route and1795 source binders are faithful in bounded scope. Acceptance is withheld solely for T1 false typing/proof-exposure classification, T2 omitted actual public-contract/typing references, and T3 substantive source row mislabeled layout. See coverage.byte-checks.json and direct-call.checks.json. No49 implementation, Test, decoder or mathematical review verdict was read; compiler never started.','input_artifacts':inputs,'compiler_started':False,'remaining_boundary':['No49 implementation/theorem proof or compilation credit','Full B.13 rough L2-to-H1 outer closed-domain passage','Literal Gamma/operator norm adapter','Half-turn subsectionC.2, paper main and cost'],'review_completed_utc':datetime.now(timezone.utc).isoformat()}
receipt['review_run_sha256']=sha(canon(receipt));save(O/'source-topology-review.json',receipt)
for x in inputs:
 p=Path(x['path']);assert pin(p)['raw_sha256']==x['raw_sha256'] and pin(p)['lf_sha256']==x['lf_sha256']
lease=get(O/'reviewer.topology.lease.json');lease.update({'status':'CLOSED','read_lease':'CLOSED','write_lease':'CLOSED','python_lease':'CLOSED','compiler_lease':'CLOSED','compiler_started':False,'closed_utc':datetime.now(timezone.utc).isoformat(),'result':pin(O/'source-topology-review.json'),'review_run_sha256':receipt['review_run_sha256'],'input_artifacts':inputs})
lease['lease_run_sha256']=sha(canon(lease));save(O/'reviewer.topology.lease.json',lease)
print(json.dumps({'result':pin(O/'source-topology-review.json'),'review_run_sha256':receipt['review_run_sha256'],'lease':pin(O/'reviewer.topology.lease.json'),'status':'CLOSED','missing_references':len(missing)},ensure_ascii=False))
