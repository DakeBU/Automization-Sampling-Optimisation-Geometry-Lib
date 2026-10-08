import pathlib,json,hashlib,gzip,os,sys
ROOT=pathlib.Path('E:/Samplinglib');os.chdir(ROOT);sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'website/scripts')]
R=ROOT/'runs/20261007-companion-priority/pbps-centered-defect59';D=R/'repository-exposition-seal59'
import publication_reader,astis_publication as publication,astis_site
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(q):return json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def load(p):return json.loads(pathlib.Path(p).read_bytes())
def write(p,q):pathlib.Path(p).write_bytes((json.dumps(q,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
def path(s):
 p=pathlib.Path(str(s).replace('\\','/'));return p if p.is_absolute() else ROOT/p
def pin(p):
 p=path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
old=json.loads(gzip.decompress((D/'graph-freshness.before-admin-refresh.exactraw.json.gz').read_bytes()));p=ROOT/'_site/data/underlying-lean-graph.json';new=load(p)
expected=publication_reader.graph_input_digest();assert new['publication_inputs_sha256']==expected
changed=[k for k in sorted(new.keys()|old.keys()) if new.get(k)!=old.get(k)]
assert changed==['publication_inputs_sha256'],changed
site=load(ROOT/'_site/data/site-data.json');assert not publication_reader.validate_graph(new,site)
decls=load(R/'math-freeze.json')['mathematical_declarations'];slices=[]
for i,n in enumerate(decls):
 ident='decl:'+n;node=next(x for x in new['nodes'] if x['id']==ident)
 incident=[x for x in new['edges'] if ident in [x['source'],x['target']]]
 assert len(incident)==[5,3][i]
 assert node==next(x for x in old['nodes'] if x['id']==ident)
 assert incident==[x for x in old['edges'] if ident in [x['source'],x['target']]]
 slices.append(dict(node=node,incident_edges=incident,incident_count=len(incident),unchanged_from_actually_viewed_capture=True))
gates=[]
for label in ['official-graph-final-admin','graph-producer-final-admin','graph-consumer-final-admin']:
 qpath=R/'integration59'/label/'receipt.json';q=load(qpath);assert q['exit_code']==0 and q['terminal_closed'] and q['checked_science_parent']=='47a28adfa36bfa67ce201f9b3ff9823c85fc3b45'
 for k in ['stdout','stderr']:
  a=pin(q[k]['path']);assert a['raw_sha256']==q[k]['raw_sha256'] and a['lf_sha256']==q[k]['lf_sha256'] and a['bytes']==q[k]['bytes']
 gates.append(dict(label=label,receipt=pin(qpath),actual_pid=q['actual_foreground_pid'],exit_code=0,command=q['command'],stdout=q['stdout'],stderr=q['stderr']))
data=publication.inputs();items=publication.load();cells={b['cell']:data['cells'].get(b['cell']) for item in items for b in item['bindings']}
native_full_digest=publication.digest(dict(lean=astis_site.source_digest(),items=items,cells=cells));assert native_full_digest==expected
write(D/'graph-successor.json',dict(status='EXACT_CURRENT_METADATA_GRAPH_FRESHNESS_REPAIRED',actual_independent_reader_pid=os.getpid(),current_generated_graph=pin(p),site_data=pin(ROOT/'_site/data/site-data.json'),native_full_graph_input_digest=expected,recipe='Full native publication_reader.graph_input_digest: digest({lean: astis_site.source_digest(), items: publication.load(), cells: full cells referenced by every publication binding}); no projected substitute',canonical_input_counts=dict(publication_items=len(items),referenced_cells=len(cells)),only_generated_graph_changed_fields=changed,math_and_reader_visual_content_unchanged=True,old_negative_mapping=load(D/'graph-freshness.negative.json')['qualified_original_to_snapshot_mapping'],exact_two_target_slices=slices,root_successor_gates=gates,source_scanner_incomplete=True,source_scanner_LogConcaveOn_prod_not_theorem_certificate=True,Test_compiled_but_graph_source_present_partial=True))
print(json.dumps(dict(status='EXACT_CURRENT_GRAPH_SUCCESSOR_PASS',actual_independent_reader_pid=os.getpid(),native_digest=expected,only_changed_field=changed,exact_incident_counts=[5,3],root_gate_pids=[x['actual_pid'] for x in gates])),flush=True)
