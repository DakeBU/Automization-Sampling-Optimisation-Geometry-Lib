import pathlib,os,json,hashlib,gzip,sys,datetime
ROOT=pathlib.Path('E:/Samplinglib');os.chdir(ROOT);D=ROOT/'runs/20261007-companion-priority/pbps-centered-defect59/repository-exposition-seal59'
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'website/scripts')]
import publication_reader
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def write(p,q):p.write_bytes((json.dumps(q,ensure_ascii=False,indent=2)+'\n').encode())
p=ROOT/'_site/data/underlying-lean-graph.json';b=p.read_bytes();g=json.loads(b);expected=publication_reader.graph_input_digest();assert g['publication_inputs_sha256']!=expected
snap=D/'graph-freshness.before-admin-refresh.exactraw.json.gz';snap.write_bytes(gzip.compress(b,mtime=0));assert gzip.decompress(snap.read_bytes())==b
mapping=dict(original=pin(p),exact_gzip_snapshot=pin(snap),snapshot_encoding='gzip exact raw payload, mtime0',decompressed_raw_bytes=len(b),decompressed_raw_sha256=sha(b),decompressed_lf_sha256=sha(b.replace(b'\r\n',b'\n')))
helper=ROOT/'website/scripts/publication_reader.py';lines=helper.read_bytes().replace(b'\r\n',b'\n').splitlines(keepends=True);selected=b''.join(lines[182:187]);(D/'graph_input_digest.L183-187.LF.snapshot').write_bytes(selected)
write(D/'lease.open.json',dict(status='OPEN',actor='/root/whole_math52/repository-exposition59',scope='Read-only exact47a integration/scoped exposition; no compiler',actual_archive_pid=os.getpid(),checked_commit='47a28adfa36bfa67ce201f9b3ff9823c85fc3b45',compiler='NOT_STARTED_CLOSED'))
write(D/'graph-freshness.negative.json',dict(status='GENERATED_GRAPH_STALE_AFTER_ADMINISTRATION',actual_foreground_pid=os.getpid(),original_tool_chunk='557360',original_tool_exit_code=0,graph_publication_inputs_sha256=g['publication_inputs_sha256'],current_native_graph_input_digest=expected,qualified_original_to_snapshot_mapping=mapping,helper_whole=pin(helper),helper_selected=pin(D/'graph_input_digest.L183-187.LF.snapshot'),science_mathematics_source_unchanged=True,repair_boundary='Only official generated graph refresh against current canonical metadata; no math/source/body/lesson/cell edits'))
print(json.dumps(dict(status='EXACT_NEGATIVE_RAW_SNAPSHOT_READY',actual_pid=os.getpid(),raw_bytes=len(b),raw_sha256=sha(b),gzip_snapshot_raw_sha256=pin(snap)['raw_sha256'],expected_digest=expected)),flush=True)
