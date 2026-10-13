import hashlib,json,os,pathlib,sys
R=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf8')
def j(n):return json.loads((O/n).read_bytes())
def ck(q):
 p=R/q['path'];b=p.read_bytes();l=b.replace(b'\r\n',b'\n');assert len(b)==q['bytes'] and len(l)==q['lf_bytes'] and sha(b)==q['raw_sha256'] and sha(l)==q['lf_sha256'],q['path']
for n in ['primary.first.manifest.json','candidate.input.manifest.json']:
 for row in j(n)['qualified_raw_LF_pairs']:
  for k in ['original','raw_snapshot','lf_snapshot']:ck(row[k])
pm=j('primary.first.manifest.json');ck(pm['fixed_primary']);whole=(R/pm['fixed_primary']['path']).read_bytes()
for x in pm['source_regions']:
 a,b=x['byte_range'];assert sha(whole[a:b])==x['snapshot']['raw_sha256']
graph=j('source.graph.before-candidate.json');cov=j('source.coverage.before-candidate.json');assert len(graph['nodes'])==19 and len(graph['hyperedges'])==13 and cov['item_count']==56 and len(cov['regions'])==24
assert graph['source_before_candidate'] and graph['implementation_route_not_read'] and cov['uncovered_bounded_regions']==[]
for w in j('candidate.input.manifest.json')['API_windows_qualified']:
 p=pathlib.Path(w['whole_original']['path']);b=p.read_bytes();assert sha(b)==w['whole_original']['raw_sha256'];span=b''.join(b.splitlines(keepends=True)[w['line_start']-1:w['line_end']]);assert sha(span)==w['exact_raw_selected_bytes']['raw_sha256'] and sha(span.replace(b'\r\n',b'\n'))==w['LF_selected_bytes']['raw_sha256']
for row in j('initial-negative.qualified-map.json')['qualified_input_maps']:
 ck(row['exact_historical_snapshot']);ck(row['LF_historical_snapshot'])
review=j('statement-binder.review.json');assert review['verdict']=='accepted-source-statement-conditional-on-verified62-parent' and review['excess_count']==0 and review['repairs']==[] and review['blocking_statement_issues']==[] and not review['mathematical_proof_credit'] and not review['compiler_started']
assert len(review['expanded_binder_classification'])==18 and len(review['seven_step_route'])==7
for t in review['named_TYPE_classification']:
 assert t['compiler_exit_code']==1 and t['classification']=='FULL_NAMED_TYPE_ELABORATED_EXPECTED_INTENTIONAL_FAIL_ONLY_NO_PROOF';ck(t['receipt']);ck(t['named_probe']);ck(t['header'])
 for p in t['current_post_pins']:ck(p)
if sys.argv[1]=='final':
 run=j('run.json');assert sha(canon({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256'];ck(run['named_payload'])
 for p in run['sealed_support_outputs']:ck(p)
 payload=j('named-preproof.payload.json');assert payload['complete_source_graph']==graph and payload['complete_source_coverage']==cov and payload['complete_statement_review']==review
 assert payload['complete_primary_first_manifest']==pm and payload['complete_candidate_manifest']==j('candidate.input.manifest.json')
 assert j('verdict.json')==dict(review,review_run_sha256=run['run_sha256'])
 print(json.dumps(dict(actual_foreground_pid=os.getpid(),mode='final',checks='PASS',run_sha256=run['run_sha256'],named_preproof_payload_sha256=run['named_preproof_payload_sha256'],source_before_candidate=True,compiler=False)))
else:print(json.dumps(dict(actual_foreground_pid=os.getpid(),mode='preseal',checks='PASS',pairs=100,source24coverage56nodes19edges13=True,compiler=False)))
