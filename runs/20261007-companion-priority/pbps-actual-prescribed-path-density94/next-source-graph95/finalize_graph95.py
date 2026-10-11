import pathlib,json,hashlib
R=pathlib.Path('E:/Samplinglib');D=R/'runs/20261007-companion-priority/pbps-actual-prescribed-path-density94/next-source-graph95'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def ref(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def put(name,x):
 p=D/name;assert not p.exists();p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8'));return ref(p)
gp=D/'candidate-source-proof-graph95.native.json';g=read(gp);cp=D/'candidate-source-coverage95.native.json';c=read(cp)
assert c['unmapped_graph_nodes']==['JOINT93']
c['version']=2;c['supersedes']=ref(cp);c['refinement']='Add explicit disposition for existing JOINT93 input,which was present in graph but omitted from first new-row coverage inventory. Preserve initial draft as negative consistency-check evidence; no graph,statement or source change.'
r=g['source_regions'];c['new_focused_dispositions'].append({'id':'C95-21','source_regions':[r['A1.SS1.SSS0.Px1.p4.2'],r['A1.E7']],'content':'Existing finite-count complete-history/path nonnegative law supplies the exact sector law before rewriting its density.','nodes':['JOINT93'],'disposition':'EXISTING_DEPENDENCY','reason':'Reuse reviewed93 without re-auditing parent proof or adding its law as a public premise. It is the actual input to TERM95.','completion_credit':False})
c['new_focused_count']=21;c['unmapped_graph_nodes']=[];c['coverage_boundary']=c['coverage_boundary'].replace('and20 new','and21 new')
cref=put('candidate-source-coverage95.v2.native.json',c)
assert {n['id'] for n in g['nodes']} <= {i for row in c['new_focused_dispositions'] for i in row['nodes']}
checks=put('artifact-consistency95.native.json',{'kind':'source-planning-artifact-consistency','graph_nodes':g['node_count'],'graph_edges':g['edge_count'],'retained_previous_rows':72,'new_focused_rows':21,'all_graph_nodes_have_source_disposition':True,'graph_acyclic':True,'source_regions_raw_checked':True,'initial_negative_check':'First coverage version omitted explicit JOINT93 row;v2 adds it and retains v1 unchanged.','no_proof_verification':True})
inputs=[g['primary'],g['prior_graph'],g['prior_coverage'],g['prior_recommendation'],ref(D.parent/'next-primary95/immutable-source-coverage-pins95.native.json')]
outputs=[ref(D/'source-first-provenance95.native.json'),ref(gp),ref(cp),cref,checks,ref(D/'write_graph95.py'),ref(D/'finalize_graph95.py')]
m=put('closed-RAW-source-graph95.native.json',{'schema_version':1,'kind':'closed-RAW-source-graph-manifest','hash_recipe':'SHA256 exact bytes,no newline normalization;source region start inclusive/end exclusive;manifest self-hash reported externally.','inputs':inputs,'outputs':outputs,'current_graph':ref(gp),'current_coverage':cref,'status':'SOURCE_PLANNING_ONLY_NO_COMPLETION_VERDICT','no_production_or_canonical_mutation':True})
for e in inputs+outputs:assert ref(R/e['path'])==e
listed={e['path'] for e in outputs};actual={p.relative_to(R).as_posix() for p in D.iterdir() if p.is_file() and p.name!='closed-RAW-source-graph95.native.json'};assert actual==listed
print(json.dumps({'graph':ref(gp),'coverage':cref,'manifest':m,'counts':[g['node_count'],g['edge_count'],72,21]},indent=2))
