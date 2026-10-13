import hashlib,json,os,pathlib
R=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent;P=O.parent;S=R/'runs/20261007-companion-priority/pbps-real-root-unique62/next-macro-source63'
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.relative_to(R).as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def wr(n,x):(O/n).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
top=json.loads((O/'source.topology.receipt.json').read_bytes());assert top['candidate_headers_scout_contract_graph_API_current_Lean_not_read']
paths=[P/x for x in ['header0.lean','header1.lean','statement-candidate.json','named-type0.lean','named-type1.lean','root.named-types63.adoption.json','header0.lean.initial-ambient-negative.exactraw.snapshot','header1.lean.initial-ambient-negative.exactraw.snapshot','named-type0.lean.initial-ambient-negative.exactraw.snapshot','named-type1.lean.initial-ambient-negative.exactraw.snapshot','statement-candidate.json.initial-ambient-negative.exactraw.snapshot']]
for dirname in ['named-type0-initial','named-type0-ambient-corrected','named-type1-ambient-corrected','adopt-named-types63']:
 for n in ['receipt.json','stdout.log','stderr.log']:paths.append(P/dirname/n)
paths += [S/x for x in ['contracts.json','API.search.json','input.manifest.json','lease.json','receipt.json','run.json']]
sm=json.loads((S/'input.manifest.json').read_bytes());selected=[]
for row in sm['qualified_input_snapshot_pairs']:
 q=row['original'];p=pathlib.Path(q['path'])
 if p.suffix=='.lean' and p.parts[-2]!='Tests' or p.name in ['lean-toolchain','lake-manifest.json','math-freeze.json']:
  assert pin(p)['raw_sha256']==q['raw_sha256'] and pin(p)['lf_sha256']==q['lf_sha256'];selected.append(p)
paths+=selected
api=json.loads((S/'API.search.json').read_bytes());maps=[]
for w in api['windows']:
 p=pathlib.Path(w['whole_original']['path']);assert pin(p)['raw_sha256']==w['whole_original']['raw_sha256'];b=b''.join(p.read_bytes().splitlines(keepends=True)[w['line_start']-1:w['line_end']]);a=pathlib.Path(w['exact_raw_selected_bytes']['path']);z=pathlib.Path(w['LF_selected_bytes']['path']);assert a.read_bytes()==b and z.read_bytes()==b.replace(b'\r\n',b'\n');paths += [a,z];maps.append(w)
pairs=[]
for i,p in enumerate(dict.fromkeys(paths)):
 b=p.read_bytes();a=O/'inputs'/f'candidate-{i:02d}-{p.parent.name}-{p.name}.raw.snapshot';z=O/'inputs'/f'candidate-{i:02d}-{p.parent.name}-{p.name}.LF.snapshot';a.write_bytes(b);z.write_bytes(b.replace(b'\r\n',b'\n'));pairs.append(dict(original=pin(p),raw_snapshot=pin(a),lf_snapshot=pin(z)))
wr('candidate.input.manifest.json',dict(actual_foreground_pid=os.getpid(),qualified_raw_LF_pairs=pairs,API_windows_qualified=maps,source_topology_before_candidate=top,chronology='Literal primary reader32888 then independent topology22468 before any candidate/scout contract/API/current Lean read. First corrected candidate reading b8a8a3 preceded this supplemental byte-copy; it is disclosed, not falsely claimed prerun pinning. Root exact namedTYPE corrected receipts contain genuine pre/post header/import/input raw pins and snapshots; current copies independently compare those exact bytes.',parent62_verification_still_required=True,compiler_started=False))
print(json.dumps(dict(actual_foreground_pid=os.getpid(),input_pairs=len(pairs),API_windows=len(maps),source_before_candidate=True,compiler=False)))
