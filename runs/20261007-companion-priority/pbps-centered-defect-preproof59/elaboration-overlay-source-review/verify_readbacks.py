from pathlib import Path
import hashlib,json,sys
sys.stdout.reconfigure(encoding='utf8')
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
load=lambda n:json.loads((O/n).read_bytes())
def check(p):
 b=(R/p['path']).read_bytes();lf=b.replace(b'\r\n',b'\n')
 assert len(b)==p['bytes'] and sha(b)==p['raw_sha256']
 assert len(lf)==p['lf_bytes'] and sha(lf)==p['lf_sha256']
m=load('input.manifest.json');assert len(m['indexed_inputs'])==m['input_count']==14
for x in m['indexed_inputs']:
 check(x['qualified_input']);check(x['immutable_exactraw_snapshot'])
 assert (R/x['qualified_input']['path']).read_bytes()==(R/x['immutable_exactraw_snapshot']['path']).read_bytes()
for x in m['reference_only_native_runs']:
 check(x);r=json.loads((R/x['path']).read_bytes());h=r.pop('run_sha256');assert sha(canon(r))==h
v=load('source-overlay-review.json');assert v['status']=='EXACT_SYNTAX_OVERLAY_ACCEPTED'
assert v['EXCESS_count']==0 and not v['mathematical_statement_change'] and not v['source_assumption_repair']
assert not v['PROVED_or_VERIFIED_or_Gamma_admission'] and v['compiler_by_reviewer']=='NOT_STARTED'
c=load('exact-comparison.json');assert len(c['checks'])==2 and c['total_annotation_occurrences']==11
assert [x['replacement_count'] for x in c['checks']]==[7,4]
assert all(x['exact_text_reconstruction'] and x['reverse_strip_equals_original'] and x['binders_exactly_unchanged'] and x['named_rfl_binder_and_body_readback'] for x in c['checks'])
assert all(x['proposer_compiler_EXIT0']==0 and x['proposer_Lean_PID']==49340 for x in c['checks'])
assert not (O/'lease.json').exists(),'CLOSEDLAST must follow actual foreground readback EXIT0.'
print(json.dumps({'status':'PASS','immutable_indexed_inputs':14,'exact_headers':2,
 'typed_identity_annotations':11,'complete_named_rfl_equalities':2,'EXCESS':0,
 'compiler_by_reviewer':'NOT_STARTED','source_repair':False,'formal_admission':False}))
