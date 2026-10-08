import hashlib,json,os,pathlib
R=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent;O.mkdir(exist_ok=True);(O/'inputs').mkdir(exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.relative_to(R).as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def wr(n,x):(O/n).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
base=O.parent;freeze=json.loads((base/'math-freeze.json').read_bytes());assert len(freeze['inputs'])==27
pairs=[]
paths=[pathlib.Path(x['path']) for x in freeze['inputs']]+[base/'math-freeze.json']
P=R/'runs/20261007-companion-priority/pbps-real-root-unique-preproof62/independent-preproof62'
paths += [P/'api.lookup.review.json']
for i,p in enumerate(paths):
 b=p.read_bytes()
 if i<27:
  x=freeze['inputs'][i];assert len(b)==x['raw_bytes'] and sha(b)==x['raw_sha256'] and sha(b.replace(b'\r\n',b'\n'))==x['lf_sha256']
 a=O/'inputs'/f'{i:02d}-{p.parent.name}-{p.name}.raw.snapshot';z=O/'inputs'/f'{i:02d}-{p.parent.name}-{p.name}.LF.snapshot';a.write_bytes(b);z.write_bytes(b.replace(b'\r\n',b'\n'));pairs.append(dict(original=pin(p),raw_snapshot=pin(a),lf_snapshot=pin(z),classification='Exact original27 compiler/math input before any independent compiler and current62 body reads' if i<27 else 'bounded frozen control/API support'))
cov=json.loads((P/'source.coverage.before-candidate.json').read_bytes());raw=(R/cov['primary']['path']).read_bytes();assert sha(raw)==cov['primary']['raw_sha256']
assert len(cov['regions'])==23 and cov['item_count']==45
for x in cov['regions']:
 lo,hi=x['byte_range'];assert sha(raw[lo:hi])==x['qualified_raw_slice']['raw_sha256']
g=json.loads((P/'source.graph.before-candidate.json').read_bytes());assert len(g['nodes'])==14 and len(g['hyperedges'])==9
wr('input.manifest.json',dict(original_math_freeze_inputs=27,qualified_raw_LF_pairs=pairs,source_primary=cov['primary'],source_graph=pin(P/'source.graph.before-candidate.json'),source_coverage=pin(P/'source.coverage.before-candidate.json'),primary_regions=cov['regions'],checked_base_commit=freeze['checked_base_commit'],independent_decoder_read=False,compiler_runs_so_far=0))
wr('primary-first.receipt.json',dict(actual_foreground_pid=os.getpid(),current62_body_not_read_yet=True,source_regions=23,coverage_items=45,source_nodes=14,source_hyperedges=9,source_graph_distinct_from_planned_Lean_route=True,pairs=len(pairs),original_math_freeze_inputs=27,independent_decoder_read=False))
print(json.dumps(dict(actual_foreground_pid=os.getpid(),pairs=len(pairs),original_math_freeze_inputs=27,source_text=[dict(id=x['id'],text=x['literal_source_text']) for x in cov['regions'] if x['id'] in ['A4.SS1','A2.E10','S1.p1','A2.Thmtheorem1.p1']],candidate_proof_read=False),ensure_ascii=True))
