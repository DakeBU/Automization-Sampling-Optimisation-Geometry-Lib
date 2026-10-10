from pathlib import Path
import hashlib,json,html,re,os,sys,subprocess,base64
r=Path('runs/20261007-companion-priority/pbps-first-corrector-energy-preproof67');d=r/'independent-primary67'
load=lambda n:json.loads((d/n).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
run,lease,manifest=[load(n) for n in ['review-run.json','lease.final.json','owned-manifest.json']]
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write'] and lease['owned_file_count']==59 and not lease['candidate67_seen'] and not lease['header67_seen']
assert sha((d/'lease.final.json').read_bytes())=='c4ec5c43dff4f4ddedeba0cb1cf4a0c969d8bac33029133a3df63e150cacad8c'
assert sha((d/'owned-manifest.json').read_bytes())==lease['manifest_RAW_sha256']=='02581ac67f2cdf5febd69cb41dbe99163382df40f8abc6f7a624e42b257b13cd'
assert {x['name'] for x in manifest['regular_file_entries']}|{'owned-manifest.json','lease.final.json'}=={p.name for p in d.iterdir() if p.is_file()}
for x in manifest['regular_file_entries']:
 b=(d/x['name']).read_bytes();assert len(b)==x['RAW_bytes'] and sha(b)==x['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==x['LF_sha256']
logical=sha(json.dumps({k:v for k,v in run.items() if k!='run_sha256'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
assert logical==run['run_sha256']==lease['whole_logical_run_sha256']=='41ebfb4ffe59d1d3718f1110db1d46db2e445c9c837d2cd7524300726a95cbcd'
for k in ['COMPLETE_RAW_DECISION','COMPLETE_RAW_REVIEW','SEPARATE_COMPLETE_RAW_INPUT']:
 x=lease[k];b=(d/x['name']).read_bytes();assert sha(b)==x['RAW_sha256'] and len(b)==x['RAW_bytes']
i,c,g,h=[load(n) for n in ['source-input-regions.json','source-coverage-inventory.json','source-proof-graph.json','residual-next-header.json']]
raw=Path(i['whole_primary']['path']).read_bytes();assert sha(raw)==i['whole_primary']['RAW_sha256']=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
assert len(i['regions'])==6 and c['count']==len(c['math_items'])==344
assert c['missing_alttext']==c['missing_annotation']==c['annotation_mismatch']==0
for x in i['regions']:
 a,b=x['source_RAW_range_end_exclusive'];s=raw[a:b];assert s==(d/('source.'+x['name']+'.RAW.html')).read_bytes() and sha(s)==x['RAW_sha256']
for x in c['math_items']:
 a,b=x['source_RAW_range_end_exclusive'];s=raw[a:b];assert sha(s)==x['RAW_sha256']
 assert html.unescape(re.search(rb'\balttext="([^"]*)"',s).group(1).decode())==x['alttext'] and x['alt_annotation_exact']
assert i['source_before_candidate'] and g['source_before_candidate'] and g['independent_of_Lean_topology'] and not c['candidate67_seen']
decision=load('primary-source-decision.json');assert decision['source_candidate_verdict'] is None and not decision['SAU_claim'] and decision['no_candidate67_or_header67_seen'] and len(decision['semantic_slots'])==7
for x in load('RAW-input-payload.json')['inputs']:
 b=base64.b64decode(x['complete_RAW_bytes_base64'],validate=True);assert len(b)==x['pin']['RAW_bytes'] and sha(b)==x['pin']['RAW_sha256']
before={p.name:(sha(p.read_bytes()),p.stat().st_mtime_ns) for p in d.iterdir() if p.is_file()}
subprocess.run([sys.executable,'-B','-X','utf8',str(d/'postclose-readonly.py')],check=True)
assert before=={p.name:(sha(p.read_bytes()),p.stat().st_mtime_ns) for p in d.iterdir() if p.is_file()}
out=r/'root.primary67.adoption.json';assert not out.exists()
out.write_text(json.dumps(dict(status='CLOSED_PRIMARY67_SOURCE_PLANNING_ADOPTED',actual_root_pid=os.getpid(),native_owned_files=59,native_run_sha256=logical,native_complete_RAW_review_sha256=lease['COMPLETE_RAW_REVIEW']['RAW_sha256'],native_complete_RAW_decision_sha256=lease['COMPLETE_RAW_DECISION']['RAW_sha256'],native_complete_RAW_input_sha256=lease['SEPARATE_COMPLETE_RAW_INPUT']['RAW_sha256'],source_regions=6,classified_math_items=344,source_graph_sha256=sha((d/'source-proof-graph.json').read_bytes()),native_lease_RAW_sha256=sha((d/'lease.final.json').read_bytes()),source_only=True,Statement_Seal=False,proof_search=False,SAU_claim=False,postclose_owned_writes=0,numbering='B20 defines corrector; B23 is sharp bound in LemmaB.3.',remaining_boundary=h),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS primary67 CLOSED59:6 exact primary regions,344/344 literal math items; SAME actual root and centered inverse commutation is a real B23/B21 ingredient, not assumed or proved here.')
