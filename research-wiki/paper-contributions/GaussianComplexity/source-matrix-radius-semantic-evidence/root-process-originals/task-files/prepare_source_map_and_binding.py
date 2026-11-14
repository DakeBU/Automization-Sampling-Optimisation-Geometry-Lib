from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,'tools')
import astis_publication as pub
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-radius-semantic-evidence')
P=Path('AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceMatrixRadius.lean')
T=Path('Tests/GaussianComplexityFixedSpectrumSourceMatrixRadius.lean')
A=Path('research-wiki/semantic-roundtrip/audits/huanjian-gaussian-source-matrix-radius.json')
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
def create(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b)
# Exact original tested byte-span helpers, copied with provenance, no previous maps executed.
hp=Path('.astis/huanjian-real-matrix-positive-integral-20261112/make_source_lean_map.generated.py')
h=hp.read_text();h=h[:h.index('shared_maps = [')]
if (W/'source_span_helpers.exact-prefix.original.py').exists():
    assert (W/'source_span_helpers.exact-prefix.original.py').read_bytes()==h.encode()
else:create(W/'source_span_helpers.exact-prefix.original.py',h.encode())
exec(compile(h,'<exact-original-source-span-helper-prefix>','exec'))
P=Path('AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceMatrixRadius.lean')
maps=[
 mapping([primary('S4.Thmtheorem4.p1'),primary('A3.SS2.p1'),primary('A3.Ex107.m1')],[(P,101,162),(T,1,73)],'Sole source range, literal original column-product space/measure and physical rows, exact midpoint features, inclusive row cutoff, actual integral mean and centered matrices. The actual frequency is2q+1; all scalar signs and nonemptiness are internal.','EXACT_SOURCE_REALIZATION'),
 mapping([primary('A3.Ex111.m1')],[(P,1,51)],'The source exact tensor rank-one norm is implemented by the canonical real Euclidean rankOne norm, flattened paired vectors and exact squared-norm product. No new generic paper result or extra source assumption.','AUTHORED_REPRESENTATION_ADAPTER_USING_CANONICAL_MATHLIB'),
 mapping([primary('A3.Ex111.m1')],[(P,52,100)],'The identity tensor feature outer product is selfadjoint with square S times itself. The canonical real matrix C-star norm identity and an actual nonzero diagonal witness yield its exact operator norm S; zero features handled separately. The generic first index must be nonempty, automatically satisfied by Fin(q+1).','AUTHORED_INTERNAL_REAL_NORM_IDENTITY'),
 mapping([primary('A3.SS2.p12'),primary('A3.Ex111.m1')],[(P,163,196)],'Reuse the canonical feature bound and actual mean theorem. Internally bound the retained-radius integral between0 and the full standard Gaussian second moment r, giving0<=a<=1. Actual mean integrability is provided by the existing mean theorem, not assumed.','SOURCE_MEAN_AND_FEATURE_WITH_INTERNAL_MOMENT_APPLICABILITY'),
 mapping([primary('A3.Ex111.m1')],[(P,197,216)],'Exact rank-one tensor norm on the inclusive retained branch and actual zero on its complementary branch yield the pointwise norm bound2rL/d. All signs derive from hq.','SOURCE_POINTWISE_SUMMAND_BOUND'),
 mapping([primary('A3.Ex111.m1')],[(P,217,226)],'Evaluate the actual mean, use exact identity-tensor norm, coefficient a<=1 and feature sum<=2r to obtain actual mean norm<=2r/d.','SOURCE_ACTUAL_MEAN_NORM_BOUND'),
 mapping([primary('A3.SS2.p13'),primary('A3.Ex112.m1')],[(T,74,86)],'Private genuine consumer calls both outputs of P on the same original experiment; triangle inequality gives exact2r(L+1)/d for every sample of actual Zi.','SOURCE_CENTERED_RADIUS_PRIVATE_CONSUMER'),
 mapping([primary('A3.SS2.p13')],[(T,87,95)],'The same private theorem uses |cos((2q+1)theta_i)|<=1 and norm_smul for actual weighted Zi. No concentration or public API credit.','SOURCE_COSINE_WEIGHTED_RADIUS_PRIVATE_CONSUMER')
]
record={'kind':'Authored source-to-code correspondence, not an independent fidelity verdict','raw_source_sha256':sha(raw),'source_span_helper_origin':str(hp),'source_span_helper_origin_sha256':sha(hp.read_bytes()),'exact_helper_prefix_sha256':sha(h.encode()),'mappings':maps,'code_files':[{'path':str(p),'sha256':sha(p.read_bytes())} for p in [P,T]],'source_graph_boundary':'Independent preproof sourcegraphv2 and distinct topology challenge are unchanged. New map links the actual final code; source overlays are not formal Lean implications.','formal_parent_scope':'P has actualMean, cosineFrame, stdGaussianSecondMoment only; T calls P only. No duplicate canonical nodes.','remaining_boundary':'Matrix Bernstein, full Lemma4.4/main lower bounds, oracle/precision/TV/cap/cost, full site integration and purification remain open.'}
create(E/'source-lean-map.authored-v1.json',dump(record))
lesson=Path('website/content/declaration_lessons/huanjian-gaussian-source-matrix-radius.json')
publication=Path('website/content/publications/huanjian-gaussian-source-matrix-radius.json')
for p in [lesson,publication]:
    b=p.read_bytes(); b=b.replace(b'Positivity of \\(d,r,L\\) is derived internally.',b'Positivity of \\(d,r\\) and nonnegativity of \\(L\\) are derived internally.')
    p.write_bytes(b)
data=pub.inputs();item=next(x for x in pub.load() if x['id']=='huanjian-gaussian-source-matrix-radius');binding=item['bindings'][0]
ctx=pub.review_context(item,binding,data);bh=pub.binding_digest(item,binding,data)
a=json.loads(A.read_bytes());a['publication_binding_sha256']=bh;a['publication_context']=ctx;A.write_bytes(dump(a))
create(W/'candidate-publication-context.v1.json',dump({'publication_binding_sha256':bh,'publication_context':ctx}))
t=json.loads((W/'private-consumer-audit.draft.json').read_bytes())
tctx={'canonical_public_producer_context':ctx,'private_consumer':{'file':str(T),'file_sha256':sha(T.read_bytes()),'whole_module_text':T.read_text(),'statement_sha256':t['lean']['statement_sha256'],'placement':'private Tests implementation consumer, not public API/canonical publication node'},'source_lean_correspondence':record}
t['publication_binding_sha256']=sha(json.dumps(tctx,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode());t['publication_context']=tctx
create(W/'private-consumer-audit.bound.v1.json',dump(t));create(W/'private-consumer-registry.bound.v1.json',dump({'schema_version':1,'audits':[t]}))
audit={'status':'none-found','discovery_ids':[],'checked_mechanism':'Real rank-one norm and tensor representation, truncation with actual first mean, triangle centering, deterministic bounded scalar weights.','checked_sources':['Libraries/conceptual-mirror-protocol.json','website/content/graph_memory_index.json','website/content/functor_hypergraph.json','Libraries/frontloaded-shared-spine.json','runs/substantive_discoveries.jsonl'],'finding':'The new steps are literal applications of canonical norm/moment APIs within the same Gaussian source argument. No new source-backed cross-domain hypothesis/estimate/conclusion correspondence has been identified. Existing Gaussian-law-symmetry and oracle-factorization conceptual families concern different mechanisms and are not Lean parents here. No conceptual edge is promoted from tensor resemblance.','failure_boundaries':['The identity-tensor exact norm requires nonempty identity index; actual r>=1 discharges it internally.','An arbitrary mean could not be substituted into the mean bound or centered radius.','Unbounded random weights would require another bound; the actual deterministic cosine is bounded by1.','Pointwise radius bounds do not prove matrix concentration or oracle lower bounds.'],'independent_review':'Pending fresh source reviewer; no self-validation claim.'}
create(E/'conceptual-mirror-audit.authored-v1.json',dump(audit))
print(json.dumps({'source_map_sha256':sha((E/'source-lean-map.authored-v1.json').read_bytes()),'publication_binding_sha256':bh,'private_consumer_binding_sha256':t['publication_binding_sha256'],'new_semantic_verdicts':0}))
