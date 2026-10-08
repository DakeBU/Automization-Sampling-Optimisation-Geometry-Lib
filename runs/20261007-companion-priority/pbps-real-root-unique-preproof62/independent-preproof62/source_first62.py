import hashlib,json,os,pathlib,sys
R=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent;O.mkdir(exist_ok=True);(O/'inputs').mkdir(exist_ok=True)
S=R/'runs/20261007-companion-priority/pbps-real-defect-root61/next-macro-source62';C=O.parent
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.relative_to(R).as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def wr(n,x):(O/n).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
pm=json.loads((S/'primary.manifest.json').read_bytes());sg=json.loads((S/'source-proof-graph.json').read_bytes())
primary=pathlib.Path(pm['primary_original']['path']);raw=primary.read_bytes();assert sha(raw)==pm['primary_original']['raw_sha256']
regions=pm['regions'];assert len(regions)==23
paths=[S/x for x in ['primary.manifest.json','source-proof-graph.json','api-search.json','contracts.json','run.json','payload.json','lease.json','receipt.json']]
paths += [C/x for x in ['header0.lean','header1.lean','statement-candidate.json','elab0.lean','elab1.lean']]
for n in ['type-header0','type-header1']:paths += [C/n/x for x in ['receipt.json','stdout.log','stderr.log']]
paths += [R/x for x in ['AutoSamplingTheory/TechnicalLemmas/Measure/L2RealSquareRoot.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/RealDefectRoot.lean','Tests/ProximalBPSRealDefectRoot.lean','AutoSamplingTheory/TechnicalLemmas/Measure/L2RealComplexOperator.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/CenteredDefectOperator.lean','lean-toolchain','lake-manifest.json']]
paths += sorted(S.glob('api-*.raw.snapshot'))
pairs=[]
for i,p in enumerate(paths):
 b=p.read_bytes();a=O/'inputs'/f'{i:02d}-{p.parent.name}-{p.name}.raw.snapshot';z=O/'inputs'/f'{i:02d}-{p.parent.name}-{p.name}.LF.snapshot';a.write_bytes(b);z.write_bytes(b.replace(b'\r\n',b'\n'));pairs.append(dict(original=pin(p),raw_snapshot=pin(a),lf_snapshot=pin(z),scope='Frozen before candidate header semantics; TYPE receipts only diagnostics, no proof; current61 math parent bytes only, no mutable aggregation/cells'))
classify={
'A4.SS1':('NODE','Real complete Hilbert/AE L2, bounded operators, positive implies selfadjoint, unique nonnegative square root. General background uniqueness selected; Markov/chi-square definitions contextual, no dynamics claim.'),
'S1.p1':('NODE','Original global C2 potential/two Hessian bounds and positive alpha order; actual consumer binder context.'),
'S2.E6':('NODE','Normalized independent Gaussian joint law actual J/nu context.'),
'S2.E7':('NODE','Same normalized conditional law; actual S definition context.'),
'A3.SS1.p2':('NODE','Reflected every-state normalized density only; score derivative/C1 EXCLUDED.'),
'A2.E8':('NODE','Yplus/Yminus reflection law context; no rate conclusion.'),
'A2.Thmtheorem1.p1':('NODE','Literal beta eta<=1 binder context ONLY; rho/gamma and whole theorem conclusions EXCLUDED.'),
'A2.E1':('NODE','Conditional projection dictionary to actual scalar T context; no new joint claim.'),
'A2.E2':('EXCLUDED','Printed macro ranP dictionary retained for failure boundary; no ontoM/root transport62.'),
'A2.E3':('EXCLUDED','Printed joint block operators; no new typed joint square identity62.'),
'A2.E4':('NODE','Reflection U contextual origin of actual selfadjoint scalar T; no new U theorem62.'),
'A2.E5':('EXCLUDED','Printed U² block B*B identity retained; uniqueness62 is not its completion.'),
'A2.E10':('EXCLUDED','Printed canonical GammaP on macro real Hilbert space. D1 uniqueness supports later identification, but62 scalar root is not GammaP.'),
'A2.E11':('EXCLUDED','Printed microscopic norm/typed Gram relation; no ontoM/B*B transport62.'),
'A2.E9':('EXCLUDED','Centered contraction rate not needed for root uniqueness.'),
'A2.E12':('EXCLUDED','rho/gamma quantitative centered rate/order constants not selected.'),
'A2.E15':('EXCLUDED','Loewner lower root order not a uniqueness consequence supplied62.'),
'A2.E16':('EXCLUDED','Centered positive inverse bound excluded.'),
'A2.SS2.p5':('EXCLUDED','Polar isometry/partial isometry/centered inverse route excluded.'),
'A3.E4':('EXCLUDED','Local variance/gradient Dirichlet inequality not new uniqueness dependency.'),
'A2.SS1.p1':('NODE','Real joint space/conditional projection context; extension to canonical scalar is ASTIS adapter, not source graph substitution.'),
'A2.SS1.p2':('EXCLUDED','Block target/source conventions preserve future macro boundary.'),
'A2.SS1.p3':('NODE','Selfadjoint unitary reflection gives scalar selfadjoint contraction context; printed B5 block conclusions separately EXCLUDED.')}
coverage=[]
for r in regions:
 lo,hi=r['byte_range'];assert sha(raw[lo:hi])==r['raw_slice']['raw_sha256']
 for k in ['raw_slice','LF_slice']:
  p=pathlib.Path(r[k]['path']);assert sha(p.read_bytes())==r[k]['raw_sha256']
 cov,why=classify[r['id']];coverage.append(dict(id=r['id'],coverage=cov,reason=why,qualified_raw_slice=r['raw_slice'],qualified_LF_slice=r['LF_slice'],byte_range=r['byte_range'],literal_source_text=r['source_text']))
extra=[dict(id='D1:unique-positive-root',source='A4.SS1',coverage='NODE',reason='For any bounded positive real operator the nonnegative square root is unique. Equivalent background consequence: positive A,B and A²=B² imply A=B; square-positive fact is internal, not extra source binder.'),dict(id='D1:root-existence',source='A4.SS1',coverage='NODE',reason='Actual61 positive scalar root existence/energy is mathematical parent; exact verification pending, no admission assumed.'),dict(id='D1:adjoint-vs-pointwiseC',source='A4.SS1',coverage='EXCLUDED',reason='Paper real operator adjoint is not pointwise complex conjugation. Complexification uniqueness route is ASTIS background proof route, not printed source proof.'),dict(id='C1:score-derivative',source='A3.SS1.p2',coverage='EXCLUDED',reason='Only density portion in scope.'),dict(id='CAP:rho-gamma',source='A2.Thmtheorem1.p1',coverage='EXCLUDED',reason='Only non-strict cap assumption selected; centered rates remain separate.'),dict(id='whole-program',source='bounded paper context',coverage='EXCLUDED',reason='Joint GammaP/ontoM/B*B, centered order/inverse/polar,H1,dynamics,main,error,cost,composition excluded.'),dict(id='geometry:rank-zero',source='S1.p1',coverage='NODE',reason='Explicit ASTIS coordinate-free finite-real-Hilbert extension including rank0, not literal paper Euclidean positive-dimension assertion.'),dict(id='typing:real-L2',source='A4.SS1',coverage='NODE',reason='Real complete possibly infinite-dimensional AE L2; arbitrary measured base generic implementation, finite E does not mean finite L2.' )]
wr('source.coverage.before-candidate.json',dict(status='INDEPENDENT_SOURCE_FIRST_BOUNDED_NODE_EXCLUDED_RECONSTRUCTION',primary=pin(primary),regions=coverage,detail_items=extra,region_count=23,item_count=len(coverage)+len(extra),scope='Exhaustive for selected bounded23 frozen regions/details, not exhaustive whole paper. Scout classification not copied; cap assumption reclassified NODE, quantitative conclusions excluded.'))
nodes=[dict(id='SRC:real-hilbert',source='A4.SS1',role='printed real complete AE Hilbert convention'),dict(id='SRC:positive-operator',source='A4.SS1',role='printed bounded nonnegative selfadjoint operator'),dict(id='SRC:unique-root',source='A4.SS1',role='printed unique positive square root background'),dict(id='SRC:macro-GammaP',source='A2.E10',role='printed unique macro root, EXCLUDED current completion'),dict(id='SRC:model',source='S1.p1',role='printed C2/two Hessians/alpha beta'),dict(id='SRC:gaussian-law',source='S2.E6/S2.E7/A2.E8',role='printed actual normalized Gaussian law'),dict(id='SRC:reflection-density',source='A3.SS1.p2',role='printed reflected conditional density'),dict(id='SRC:reflection-selfadjoint',source='A2.E4/A2.SS1.p3',role='printed unitary involutive selfadjoint U'),dict(id='SRC:cap',source='A2.Thmtheorem1.p1',role='printed beta eta<=1 assumption only'),dict(id='SRC:macro-block',source='A2.E2/A2.E3/A2.E5',role='printed macro/Gram identity, EXCLUDED current completion'),dict(id='SRC:B11',source='A2.E11',role='printed full macro energy relation, EXCLUDED current completion'),dict(id='ASTIS:scalar62-uniqueness',source='D1 background elaboration',role='UNPROVED selected real-L2 specialization/equal-positive-square consequence'),dict(id='ASTIS:actual61-root',source='current exact parent bytes',role='Existing scalar existence/energy; parent verification admission pending'),dict(id='ASTIS:actual62-unique-root',source='D1/source model scalar adapter',role='UNPROVED selected original-input consumer')]
edges=[dict(parents=['SRC:real-hilbert','SRC:positive-operator'],child='SRC:unique-root',relation='printed standard spectral-theorem background'),dict(parents=['SRC:unique-root','SRC:macro-block'],child='SRC:macro-GammaP',relation='printed canonical macro-root definition, no new Lean edge'),dict(parents=['SRC:macro-GammaP','SRC:macro-block'],child='SRC:B11',relation='printed typed square/norm relation, excluded62'),dict(parents=['SRC:model'],child='SRC:gaussian-law',relation='printed model definition'),dict(parents=['SRC:gaussian-law'],child='SRC:reflection-density',relation='printed conditional density definition'),dict(parents=['SRC:gaussian-law'],child='SRC:reflection-selfadjoint',relation='printed reflection law/isometry'),dict(parents=['SRC:unique-root','SRC:real-hilbert'],child='ASTIS:scalar62-uniqueness',relation='attributed background consequence/specialization; source topology, not yet Lean proof'),dict(parents=['SRC:model','SRC:cap','SRC:reflection-density','SRC:reflection-selfadjoint'],child='ASTIS:actual61-root',relation='actual scalar source adapter established by exact61 math parent; no admission claim'),dict(parents=['ASTIS:actual61-root','ASTIS:scalar62-uniqueness'],child='ASTIS:actual62-unique-root',relation='selected genuine scalar integration target, unproved')]
wr('source.graph.before-candidate.json',dict(status='INDEPENDENT_SOURCE_FIRST_TOPOLOGY_NOT_IMPLEMENTATION_PROOF',nodes=nodes,hyperedges=edges,source_graph_scope='Literal real-Hilbert uniqueness/model/macro background; no complexification/CFC route imported as printed source edge.',implementation_route_separate=True,scout_graph_pin=pin(S/'source-proof-graph.json'),candidate_semantics_read=False))
wr('input.manifest.json',dict(qualified_raw_LF_pairs=pairs,primary=pin(primary),primary_regions=coverage,source_first_pid=os.getpid(),inputs_exclusion='No mutable61 aggregation/cells/globalledger or previous postproof source verdict; mathematical parent bytes only.'))
wr('source-first.receipt.json',dict(actual_foreground_pid=os.getpid(),source_before_candidate=True,regions=23,coverage_items=31,source_nodes=len(nodes),source_hyperedges=len(edges),candidate_semantics_read=False,compiler_started=False))
print(json.dumps(dict(actual_foreground_pid=os.getpid(),pairs=len(pairs),source_text=[dict(id=r['id'],text=r['source_text']) for r in regions],source_nodes=len(nodes),source_hyperedges=len(edges),candidate_semantics_read=False),ensure_ascii=True))
