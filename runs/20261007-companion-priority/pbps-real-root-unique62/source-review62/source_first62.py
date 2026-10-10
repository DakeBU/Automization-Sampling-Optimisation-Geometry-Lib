import hashlib,json,os,pathlib
R=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent;O.mkdir(exist_ok=True);(O/'inputs').mkdir(exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.relative_to(R).as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def wr(n,x):(O/n).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
B=O.parent;P=R/'runs/20261007-companion-priority/pbps-real-root-unique-preproof62/independent-preproof62';D=B/'anonymous-decoder';M=B/'independent-math62'
paths=[P/'source.coverage.before-candidate.json',P/'source.graph.before-candidate.json',P/'input.manifest.json']
paths += [B/f'source.{i}.reviewer-packet.json' for i in [0,1]]
paths += [D/x for x in ['decoder62.statements.payload.raw.json','native-decoder-run.raw.txt','native-receipt.json','lease.CLOSEDLAST.native.json']]
paths += [R/x for x in ['AutoSamplingTheory/TechnicalLemmas/Measure/L2RealSquareRootUnique.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/RealDefectRootUnique.lean','Tests/ProximalBPSRealDefectRootUnique.lean','AutoSamplingTheory/TechnicalLemmas/Measure/L2RealComplexOperator.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/RealDefectRoot.lean','AutoSamplingTheory/TechnicalLemmas/Measure/L2RealSquareRoot.lean','runs/20261007-companion-priority/pbps-real-root-unique-preproof62/header0.lean','runs/20261007-companion-priority/pbps-real-root-unique-preproof62/header1.lean','lean-toolchain','lake-manifest.json']]
paths += [B/x for x in ['publication-plan.json','exposition.draft.json']]
slugs=['l2-positive-real-square-root-uniqueness','pbps-unique-positive-real-defect-root']
paths += [R/'website/content/declaration_lessons'/f'{x}.json' for x in slugs]+[R/'website/content/publications'/f'{x}.json' for x in slugs]
paths += [M/x for x in ['run.json','verdict.json','native.receipt.json','lease.json','named-mathematics.payload.json']]
paths += [R/'runs/20261007-companion-priority/pbps-real-defect-root61/math-freeze.json']
# Frozen control/support bytes only; no decoder/candidate/source-verdict semantics before primary.
pairs=[]
for i,p in enumerate(paths):
 b=p.read_bytes();a=O/'inputs'/f'{i:02d}-{p.parent.name}-{p.name}.raw.snapshot';z=O/'inputs'/f'{i:02d}-{p.parent.name}-{p.name}.LF.snapshot';a.write_bytes(b);z.write_bytes(b.replace(b'\r\n',b'\n'));pairs.append(dict(original=pin(p),raw_snapshot=pin(a),lf_snapshot=pin(z),scope='Exact raw/LF bytes frozen before current fresh packet/decoder semantics; canonical audits/prior postproof source verdicts excluded'))
cov=json.loads(paths[0].read_bytes());g=json.loads(paths[1].read_bytes());raw=(R/cov['primary']['path']).read_bytes();assert sha(raw)==cov['primary']['raw_sha256']
assert len(cov['regions'])==23 and cov['item_count']==45 and len(g['nodes'])==14 and len(g['hyperedges'])==9
for x in cov['regions']:
 lo,hi=x['byte_range'];assert sha(raw[lo:hi])==x['qualified_raw_slice']['raw_sha256']
mathlease=json.loads((M/'lease.json').read_bytes());assert mathlease['status']=='CLOSED' and mathlease['closed_last'] and mathlease['actual_foreground_readback_exit_codes']==[0,0]
wr('primary-first.boundary.json',dict(actual_foreground_pid=os.getpid(),source_regions=cov['regions'],primary=cov['primary'],source_graph=pin(paths[1]),source_coverage=pin(paths[0]),status='INDEPENDENT_PRIMARY_FIRST_ANTI_ANCHORED_SOURCE62_RECONSTRUCTION',objects='Printed D1 real AE quotient/complete Hilbert bounded operators/nonnegative unique-root background; printed B10 canonical macro root differs from scalar real marginal ν root. Original C2/two global Hessians/0alpha<=beta/η>0/non-strict betaη<=1 model binds actual normalized Gaussian/reflected S/T.',selected_boundary='Generic equal positive REAL square implies equality is attributed ASTIS real Hilbert background completion specialized to arbitrary measure L2. Actual Γ uniqueness among ALL positive alternative roots of SAME D, no supplied energy; source density every-y and observable action per-u ν-AE. Infinite L2/rank0/alphaη1 legal. Probability/canonical S/T/D/root must be internal conclusions.',excluded='JointGammaP/ontoM/typedB*B, centeredorder/inverse/polar,H1,dynamics/main/error/querycost/composition not completed. No η prefactor or publicCFC/complexification/root/preservation/finiteL2/nontrivial certificate.',source_graph_vs_Lean_route='Independent14node9hyperedge source topology literal23/45 coverage remains source-before-implementation. Complex lift/CFC uniqueness/injectivity is ASTIS selected background proof, not printed proof source graph.',source_before_current_packets_decoder=True,math_decision_already_CLOSED=pin(M/'verdict.json'),no_prior_postproof_source_verdict_read=True))
wr('input.manifest.json',dict(qualified_raw_LF_pairs=pairs,primary=cov['primary'],original_input_count=len(paths),primary_regions=23,coverage_items=45,source_nodes=14,source_hyperedges=9,source_first_pid=os.getpid(),math_run_is_distinct_and_already_closed=True))
wr('primary-first.receipt.json',dict(actual_foreground_pid=os.getpid(),current_packets_decoder_not_semantically_read=True,source_regions=23,coverage_items=45,source_nodes=14,source_hyperedges=9,input_pairs=len(pairs),compiler_started=False))
print(json.dumps(dict(actual_foreground_pid=os.getpid(),pairs=len(pairs),source_regions=23,coverage_items=45,source_nodes=14,hyperedges=9,source_text=[dict(id=x['id'],text=x['literal_source_text']) for x in cov['regions']],current_decoder_semantic_read=False),ensure_ascii=True))
