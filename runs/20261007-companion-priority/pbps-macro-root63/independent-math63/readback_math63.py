import hashlib,json,os,pathlib,sys
R=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def j(n):return json.loads((O/n).read_bytes())
def ck(p):
 b=(R/p['path']).read_bytes();l=b.replace(b'\r\n',b'\n');assert len(b)==p['bytes'] and len(l)==p['lf_bytes'] and sha(b)==p['raw_sha256'] and sha(l)==p['lf_sha256'],p['path']
m=j('input.manifest.json')
for row in m['qualified_raw_LF_pairs']:
 for k in ['original','raw_snapshot','lf_snapshot']:ck(row[k])
ck(m['source_primary']);raw=(R/m['source_primary']['path']).read_bytes()
for x in m['primary_regions']:
 ck(x['snapshot']);lo,hi=x['byte_range'];assert sha(raw[lo:hi])==x['snapshot']['raw_sha256']
before=j('compiler.inputs.before.json');after=j('compiler.inputs.after.json')
assert before['original30']==after['original30'] and before['all58']==after['all58']
c=j('focused.receipt.json');assert c['exit_code']==0 and c['terminal_closed'] and c['compiler_runs']==1 and c['nonforced']
for k in ['stdout','stderr','inputs_before','inputs_after']:ck(c[k])
proof=j('mathematical-proof.review.json');assert len(proof['eight_mathematical_formula_steps'])==8
for n,x in enumerate(proof['eight_mathematical_formula_steps']):
 s=x['authored_step'];q=s['lean_source_region'];bb=(R/q['path']).read_bytes();assert sha(bb)==q['source_raw_sha256']
 excerpt=b''.join(bb.splitlines(keepends=True)[q['start_line']-1:q['end_line']]);assert sha(excerpt)==x['actual_literal_span_sha256']
 if n!=2:assert excerpt==s['lean'].encode() and x['exact_multiline_excerpt_verified']
 else:assert not x['exact_multiline_excerpt_verified'] and sha(excerpt)=='90b9b65491cb5fdace9c60c5e65ddae6e777b2eea20b588dbcd74a1311cae609'
proposal=j('publication-step3.binding.issue-and-proposal.json')['minimal_proposed_repair'];bb=(R/proposal['path']).read_bytes()
excerpt=b''.join(bb.splitlines(keepends=True)[proposal['start_line']-1:proposal['end_line']]);assert sha(excerpt)==proposal['exact_code_raw_sha256'] and excerpt.decode()==proposal['lean']
d=j('mathematical.decision.sealed.json');assert d['verdict']=='accepted-scoped-whole-math63' and d['decoder_not_read'] and d['compiler_runs']==1
assert d['repairs']==[] and d['blocking_issues']==[] and len(d['publication_binding_issues'])==1
for a in d['public_axioms'].values():assert set(a)=={'propext','Classical.choice','Quot.sound'}
if sys.argv[1]=='final':
 run=j('run.json');assert sha(canon({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256'];ck(run['named_payload'])
 for p in run['sealed_support_outputs']:ck(p)
 payload=j('named-mathematics.payload.json');assert payload['complete_decision']==d and payload['complete_mathematical_proof_review']==proof and payload['complete_input_manifest']==m
 assert payload['complete_publication_binding_issue']==j('publication-step3.binding.issue-and-proposal.json')
 assert j('verdict.json')==dict(d,review_run_sha256=run['run_sha256'])
 print(json.dumps(dict(actual_foreground_pid=os.getpid(),all_checks='PASS',mode='final',run_sha256=run['run_sha256'],named_mathematics_payload_sha256=run['named_mathematics_payload_sha256'],decoder_read=False,compiler_runs=1,publication_issue_preserved=True)))
else:print(json.dumps(dict(actual_foreground_pid=os.getpid(),all_checks='PASS',mode='preseal',pairs=len(m['qualified_raw_LF_pairs']),primary_regions=len(m['primary_regions']),compiler_runs=1,decoder_read=False,publication_issue_preserved=True)))
