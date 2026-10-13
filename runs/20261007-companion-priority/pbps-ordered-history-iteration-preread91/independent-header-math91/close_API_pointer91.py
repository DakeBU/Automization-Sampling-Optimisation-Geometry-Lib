import pathlib,json,hashlib,datetime
R=pathlib.Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-ordered-history-iteration-preread91/independent-header-math91'
def desc(p):
 p=pathlib.Path(p);p=p if p.is_absolute() else R/p;b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def write(n,d):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
 return desc(O/n)
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
old=json.loads((O/'API-review91.json').read_text(encoding='utf8'));new=json.loads(json.dumps(old))
assert new['references'][2]['line']==109
p=R/new['references'][2]['file'];lines=p.read_text(encoding='utf8').splitlines();assert lines[109].startswith('theorem actual_finite_history_extension')
new['references'][2]['line']=110
write('API-review91.v2.json',new)
write('API-pointer91.negative.json',{'utc':utc,'class':'REVIEWER_API_LINE_POINTER_OFF_BY_ONE','original':desc(O/'API-review91.json'),'corrected':desc(O/'API-review91.v2.json'),'exact_delta':'actual90 theorem declaration line109 -> line110; no API name, contract, mathematical statement, compilation receipt or acceptance change. Original retained.','native_check':'rg -n ^theorem actual_finite_history_extension AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryExtension.lean returned110, EXIT0'})
run=write('run91.authoritative.json',{'utc':utc,'status':'CLOSED_HEADER_REVIEW_ONLY','original_run':desc(O/'run91.json'),'unchanged_decision':desc(O/'decision91.json'),'pointer_only_successor':desc(O/'API-pointer91.negative.json'),'authoritative_API_readback':desc(O/'API-review91.v2.json'),'whole_header_receipts':[desc(O/'header-original91.receipt.json'),desc(O/'header-private-check91.receipt.json')],'all_native_typecheck_terminal_exits':[0,0],'no_recompile_of_unchanged_header':True})
oldm=json.loads((O/'closed-RAW-manifest91.json').read_text(encoding='utf8'))
for d in oldm['frozen_current_inputs']:assert desc(d['path'])['raw_sha256']==d['raw_sha256']
m=write('closed-RAW-manifest91.authoritative.json',{'utc':utc,'closed':True,'reviewer_id':'/root/exact_verify77','frozen_current_inputs':oldm['frozen_current_inputs'],'owned_artifacts':[desc(p) for p in sorted(O.iterdir()) if p.is_file()],'self_hash_excluded':True,'noncircular':True,'original_closure_preserved':desc(O/'closed-RAW-manifest91.json'),'authoritative_run':run,'decision':desc(O/'decision91.json'),'successor_reason':'Exact declaration line-pointer only; full mathematical acceptance and both native typechecks unchanged.'})
print(json.dumps({'decision':desc(O/'decision91.json'),'run':run,'authoritative_closed_manifest':m}))
