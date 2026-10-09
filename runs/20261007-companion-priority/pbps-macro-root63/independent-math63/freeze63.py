import hashlib,json,os,pathlib
R=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent;B=O.parent
O.mkdir(exist_ok=True);(O/'inputs').mkdir(exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.relative_to(R).as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def wr(n,x):(O/n).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
freeze=json.loads((B/'math-freeze.json').read_bytes());assert len(freeze['inputs'])==30 and freeze['checked_base_commit']=='44dc6d6f744e76b86df88cfde1926552dff12cf5'
paths=[]
for q in freeze['inputs']:
 p=pathlib.Path(q['path']);now=pin(p);assert now['raw_sha256']==q['raw_sha256'] and now['lf_sha256']==q['lf_sha256'] and now['bytes']==q['raw_bytes'];paths.append(p)
paths += [B/'math-freeze.json',R/'AutoSamplingTheory/TechnicalLemmas/Measure/L2RealComplexOperator.lean']
for n in ['macro-root-draft.v1.failed.exactraw.snapshot.lean','macro-root-draft.v2.failed.exactraw.snapshot.lean','macro-root-draft.v3.failed.exactraw.snapshot.lean','macro-root-draft.v4.failed.exactraw.snapshot.lean','macro-root-draft.v5.PASS.exactraw.snapshot.lean','macro-root-draft.v6.consumer-negative.exactraw.snapshot.lean','v3.compiler-diagnosis.json','v4.compiler-diagnosis.json']:paths.append(B/n)
for dirname in ['focused-macro-draft-v2','focused-macro-draft-v3','focused-macro-draft-v4','focused-macro-draft-v5','focused-macro-and-consumer-v6','focused-macro-and-consumer-v7']:
 for n in ['receipt.json','stdout.log','stderr.log']:paths.append(B/dirname/n)
pairs=[]
for i,p in enumerate(paths):
 b=p.read_bytes();a=O/'inputs'/f'{i:02d}-{p.parent.name}-{p.name}.raw.snapshot';z=O/'inputs'/f'{i:02d}-{p.parent.name}-{p.name}.LF.snapshot';a.write_bytes(b);z.write_bytes(b.replace(b'\r\n',b'\n'));pairs.append(dict(original=pin(p),raw_snapshot=pin(a),lf_snapshot=pin(z),scope='Original30 mathematical freeze or finite explicitly named parent/negative support; no decoder/public source verdict inputs'))
cov=json.loads((R/'runs/20261007-companion-priority/pbps-macro-root-preproof63/independent-preproof63/source.coverage.before-candidate.json').read_bytes())
graph=json.loads((R/'runs/20261007-companion-priority/pbps-macro-root-preproof63/independent-preproof63/source.graph.before-candidate.json').read_bytes())
whole=(R/cov['fixed_primary']['path']).read_bytes();assert sha(whole)==cov['fixed_primary']['raw_sha256']
for x in cov['regions']:
 a,b=x['byte_range'];assert sha(whole[a:b])==x['snapshot']['raw_sha256']
assert len(cov['regions'])==24 and cov['item_count']==56 and len(graph['nodes'])==19 and len(graph['hyperedges'])==13
wr('input.manifest.json',dict(actual_foreground_pid=os.getpid(),qualified_raw_LF_pairs=pairs,original30=freeze['inputs'],source_primary=cov['fixed_primary'],primary_regions=cov['regions'],source_graph_counts=[19,13],source_coverage_count=56,whole_math_before_current_body_read=True,decoder_not_read=True,original30_before_compiler=True,checked_parent=freeze['checked_base_commit']))
wr('primary-first.receipt.json',dict(actual_foreground_pid=os.getpid(),reuse_unchanged_preproof_source_topology=True,source_before_current_body=True,regions=24,coverage_items=56,nodes=19,context_edges=13,original30_pinned=True,decoder_not_read=True,compiler_started=False))
print(json.dumps(dict(actual_foreground_pid=os.getpid(),original30=30,total_pairs=len(pairs),source24coverage56=True,current_body_not_read=True,decoder_not_read=True,compiler=False)))
