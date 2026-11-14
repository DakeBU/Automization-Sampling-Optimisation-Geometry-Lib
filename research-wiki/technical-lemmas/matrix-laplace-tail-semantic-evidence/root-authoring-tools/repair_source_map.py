from pathlib import Path
import json,copy,hashlib
r=Path.cwd();e=r/'research-wiki/technical-lemmas/matrix-laplace-tail-semantic-evidence'
old=e/'source-lean-correspondence.authored-v1.json';x=json.loads(old.read_text())
rows=x['rows']; pf='AutoSamplingTheory/TechnicalLemmas/Probability/MatrixLaplaceTail.lean'
b=(r/pf).read_bytes();lines=b.decode().splitlines(keepends=True)
rows[0]['signature_code']={'file':pf,'source_sha256':hashlib.sha256(b).hexdigest(),
 'mathematical_commit':'1d1103af694b9663a72b0d610004ed85c7c6b527','LF_lines_1based_inclusive':[55,65],
 'exact_span_sha256':hashlib.sha256(''.join(lines[54:65]).encode()).hexdigest()}
for i in [2,3,4]:
    rows[i]['source_node_coverage']='ABSORBED_IN_EXPLICIT_DIRECT_TRACE_SUFFICIENT_ROUTE; not separately emitted source intermediate lemma'
    rows[i]['not_claimed']=['Standalone largest-eigenvalue exponential measurability theorem',
      'Standalone spectral homogeneity theorem', 'Standalone E exp(s lambdaMax) comparison']
rows[6]['source_nodes'].remove('GC.MEAN')
rows[6]['mean_definition_only']='The let mean:=integral Y names the actual mean. It does not alone prove the radial mean formula or coefficient bounds represented by GC.MEAN.'
rows[7]['source_nodes'].append('GC.MEAN')
rows[7]['node_coverage']='Existing canonical Mean/Radius/Structure source closure reuse, not a new mean lemma or a theorem inferred from an import. The actual value DAG supplies dependency evidence; previous source parents retain their existing review boundaries.'
for i in [10,11]:
    rows[i]['source_node_coverage']='PARTIAL_SUFFICIENT_FOR_SEALED_POSITIVE_PARAMETER_CONSUMER_ONLY'
    rows[i]['not_claimed']=['Whole GC.FINITE.MGF source graph node for every real s',
      'A separately emitted strict positivity of trace exponential statement',
      'An explicitly proved r^2*exp(abs(s)*d*rho) trace cap']
    rows[i]['mathematical_meaning']='For each required s>0, the actual proof gives a matrix exponential norm bound and nonnegative integrable scalar trace exponential, sufficient for the sealed T extended-to-Bochner conversion.'
x['downstream_open'][1]['label']=x['downstream_open'][1].pop('node')
x['downstream_open'][1]['identity_kind']='PLANNED_CONSUMER_LABEL_NOT_A_NODE_OF_THE_28_NODE_GRAPH'
x['source_graph_nodes_with_stronger_unemitted_background']=[{
 'node':'GC.FINITE.MGF','status':'FULL_GRAPH_NODE_REMAINS_OPEN_BEYOND_POSITIVE_PARAMETER_T_INGREDIENT',
 'reason':'The source graph statement includes all-real parameters, strict trace positivity and an explicit dimension-scaled cap. T only needs and internally proves nonnegative trace integrability for positive parameters; its proof does not close those extra conclusions.'}]
x['status']='ROOT_AUTHORED_MAP_v2_AFTER_INDEPENDENT_MAPPING_FINDINGS; INDEPENDENT_EXACT_v2_REVIEW_PENDING'
x['predecessor_map']={'path':str(old.relative_to(r)),'sha256':hashlib.sha256(old.read_bytes()).hexdigest(),'preserved_unchanged':True}
for row in rows:row['independent_source_discharge_status']='P/T exact target source reviews accepted separately; this exact v2 node-map overlay remains pending independent review.'
out=e/'source-lean-correspondence.authored-v2.json';assert not out.exists()
out.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'v2_map_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'proofs_and_target_types_unchanged':True,'stronger_background_node_not_falsely_closed':True}))
