from repo64 import *
def diff(a,b,path=''):
 if type(a)!=type(b):return [path]
 if isinstance(a,dict):return sum((diff(a.get(k),b.get(k),path+'/'+k) for k in a.keys()|b.keys()),[])
 return [] if a==b else [path]
def check():
 assert git('rev-parse',COMMIT+'^')==SCI
 for x in load(OUT/'input.manifest.json')['exact_inputs']:validate(x)
 # Reuse the immutable exact-science verdict; do not replay proofs or promote a new source decision.
 ad=load(BASE/'root.exact-verification64.adoption.json');vr=load(BASE/'verified.json');native=BASE/'exact-science-verification';lease=load(native/'lease.json');run=load(native/'run.json');r0=dict(run);r0.pop('run_sha256');assert sha(compact(r0))==run['run_sha256']==ad['native_run_sha256'];assert sha((native/'named-verification.payload.json').read_bytes())==ad['native_complete_RAW_verdict_sha256'];assert sha((native/'lease.json').read_bytes())==ad['native_lease_RAW_sha256'];assert lease['status']=='CLOSED_LAST' and vr['checked_commit']==ad['verified_commit']==SCI
 for x in lease['complete_owned_output_manifest_after_actual_readback']:validate(x)
 science=[]
 for rel in SCIENCE:
  b=blob(COMMIT,rel);assert b==blob(SCI,rel)==(ROOT/rel).read_bytes();science.append({'path':rel,'RAW_sha256':sha(b),'exact_science_parent_RAW_equal':True})
 for rel in ['research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-RealL2PositiveSquareOrder.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSCenteredRootOrderInverse.json','website/content/publications/real-l2-positive-square-order.json','website/content/publications/pbps-centered-root-order-inverse.json','website/content/declaration_lessons/real-l2-positive-square-order.json','website/content/declaration_lessons/pbps-centered-root-order-inverse.json']:
  assert blob(COMMIT,rel)==blob(SCI,rel)
 roots=[]
 for rel in ROOTS:
  b=blob(COMMIT,rel);old=blob(SCI,rel);patch=subprocess.check_output(['git','diff','--numstat',SCI,COMMIT,'--',rel],cwd=ROOT).decode().strip();roots.append({'path':rel,'committed_RAW_sha256':sha(b),'science_parent_RAW_sha256':sha(old),'numstat':patch})
 assert b'import AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredRootOrderInverse' in blob(COMMIT,ROOTS[0]);assert b'import AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareOrder' in blob(COMMIT,ROOTS[1]);assert b'import Tests.ProximalBPSCenteredRootOrderInverse' in blob(COMMIT,'Tests.lean');reg=blob(COMMIT,ROOTS[2]).decode();assert reg.count('status := LemmaMemoryStatus.formalizedLocal')==510;assert b'formalizedTechnicalLemmaCount = 510' in blob(COMMIT,'Tests/Basic.lean')
 # All root process receipts are actual terminal records; old command-name negatives remain failures.
 gates=[];historical=[]
 for label in LABELS:
  p=INT/label/'receipt.json';r=load(p);assert r['terminal_closed'] and r['actual_foreground_pid']>0;expected=2 if label in ['frontier','semantic'] else 0;assert r['exit_code']==expected
  validate(r['stdout']);validate(r['stderr']);assert len(r['inputs'])==len(r['input_snapshots'])==18
  for original,m in zip(r['inputs'],r['input_snapshots']):
   assert original==m['original'];b=validate(original,m['exact_raw_snapshot']['path']);validate(m['exact_raw_snapshot']);lf=validate(m['LF_snapshot']);assert lf==b.replace(b'\r\n',b'\n');rel=pth(original['path']).relative_to(ROOT).as_posix();current=blob(COMMIT,rel)
   relation='RAW-exact' if current==b else ('RAW-distinct-LF-equal' if current.replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n') else 'explicit-historical-input-map')
   if relation=='explicit-historical-input-map':
    assert rel in ['research-wiki/frontier-cells/ASTIS-SHARED-l2-real-positive-square-order.json','research-wiki/frontier-cells/ASTIS-SW-PBPS-centered-root-order-inverse.json'];changes=diff(json.loads(b),json.loads(current));historical.append({'receipt':label,'original_path':rel,'historical_RAW_sha256':sha(b),'explicit_snapshot':m['exact_raw_snapshot'],'current_committed_RAW_sha256':sha(current),'metadata_diff_paths':changes})
  gates.append({'label':label,'actual_pid':r['actual_foreground_pid'],'exit_code':r['exit_code'],'terminal_closed':True,'receipt':pin(p),'scope':'retained negative wrong command name' if expected else 'accepted terminal gate','RAW_LF_input_pairs':18})
 mandatory=(INT/'mandatory-astis-check-final/stdout.log').read_text(encoding='utf-8');jobs=re.findall(r'Build completed successfully \((\d+) jobs\)',mandatory);assert jobs==['9172','9468'] and 'ASTIS check passed' in mandatory
 regression=(INT/'python-regression-suite/stderr.log').read_text(encoding='utf-8');assert re.search(r'Ran 296 tests in [\d.]+s\s+OK',regression)
 assert 'Publication PASS: 231 source items' in (INT/'publication-final-admin/stdout.log').read_text(encoding='utf-8');assert 'ASTIS contributor contract PASS' in (INT/'contributor-final-admin/stdout.log').read_text(encoding='utf-8');assert 'protocol check passed' in (INT/'frontier-final-admin/stdout.log').read_text(encoding='utf-8')
 graphchecks=[]
 for label in ['cell-graph-check-actual','cell-graph-check-shared']:
  g=load(INT/label/'stdout.log');assert g['status']=='graph coverage checked';graphchecks.append(g)
 # Exact body excerpts, folded steps, four copy callbacks and four UTF8 RAW source download matches.
 cc=load(INT/'visual64/copy-capture.json');rc=load(INT/'visual64/render-capture.json');assert cc['ownedBrowserExit']['code']==rc['ownedBrowserExit']['code']==0;assert len(rc['records'])==16
 body=[];downloads=[];panels=[]
 for record,slug,rel in zip(cc['records'],['real-l2-positive-square-order','pbps-centered-root-order-inverse'],SCIENCE[:2]):
  u=load(ROOT/f'website/content/declaration_lessons/{slug}.json')['units'][0];assert record['initialFolded'] and record['copyProbeUsesIsolatedPageClipboardCallback'] and not record['physicalOSClipboardTest'];assert len(record['panels'])==len(record['downloads'])==2
  source_text=blob(COMMIT,rel).decode();theorem_start=source_text.index('theorem ');expected_panels=[source_text[theorem_start:source_text.index(':= by',theorem_start)].rstrip(),source_text[theorem_start:].rstrip('\n')]
  for p,k,expected_code in zip(record['panels'],['lean_statement','lean_proof'],expected_panels):assert p['callbackCalled'] and p['copiedExactly'] and p['code']==expected_code;panels.append({'publication':slug,'panel':k,'exact_callback':True,'exact_code_from_committed_theorem_source':True,'RAW_code_sha256':sha(p['code'].encode())})
  for d in record['downloads']:
   b=d['text'].encode();assert d['status']==200 and b==blob(COMMIT,rel);downloads.append({'publication':slug,'href':d['href'],'status':200,'actual_UTF8_RAW_bytes':len(b),'actual_UTF8_RAW_sha256':sha(b),'capture_bytes_field_means_JS_string_length':d['bytes'],'RAW_equal_exact_committed_source':True})
  assert len(record['steps'])==len(u['steps'])
  for index,(captured,s) in enumerate(zip(record['steps'],u['steps'])):
   assert captured['initiallyFolded'] and captured['lean']==s['lean'];r=s['lean_source_region'];raw=blob(COMMIT,r['path']);region=b''.join(raw.splitlines(keepends=True)[r['start_line']-1:r['end_line']]);assert region==s['lean'].encode() and sha(raw)==r['source_raw_sha256'] and sha(region)==r['exact_code_raw_sha256'];assert sum(len(v) for v in raw.splitlines(keepends=True)[:r['start_line']-1])>raw.index(b':= by');body.append({'publication':slug,'step':index+1,'path':r['path'],'whole_file_RAW_sha256':sha(raw),'start_line':r['start_line'],'end_line':r['end_line'],'literal_BODY_line_span_RAW_sha256':sha(region),'initially_folded':True,'exact_committed_literal':True})
 assert len(panels)==len(downloads)==4 and len(body)==12
 # Four changed aggregate graph artifacts, two enriched cards and preserved old context.
 mg=load(ROOT/GRAPHS[2]);mods={m['module']:m for m in mg['modules']};assert len(mods)==len(mg['modules'])==518
 for rel,card in zip([SCIENCE[1],SCIENCE[0]],CARDS):
  module=rel[:-5].replace('/','.');m=mods[module];s=blob(COMMIT,card).decode();assert SCI in s and 'remain separate' in s;assert module in s;imports=re.findall(r'^import (.+)$',blob(COMMIT,rel).decode(),re.M);assert m['imports']==imports;assert all(i in s for i in imports)
 graphpins=[]
 for rel in GRAPHS+CARDS:
  assert blob(COMMIT,rel)!=blob(SCI,rel) if rel in GRAPHS else True;graphpins.append({'path':rel,'committed_RAW_sha256':sha(blob(COMMIT,rel))})
 preservation=load(INT/'generated-context-preservation-data/manifest.json');preserved=[];aggregates=[]
 for x in preservation['emitted_snapshots']:
  emitted=gzip.decompress((ROOT/x['emitted_snapshot']).read_bytes());assert sha(emitted)==x['emitted_raw_sha256'];base=blob(SCI,x['path']);assert sha(base)==x['baseline_raw_sha256']
  if x['action']=='restored root-generated unrelated changes to exact HEAD bytes':assert blob(COMMIT,x['path'])==base;preserved.append(x['path'])
  else:assert x['path'] in GRAPHS;aggregates.append(x['path'])
 assert len(preserved)==87 and set(aggregates)==set(GRAPHS)
 for x in preservation['preserved_canonical_metadata']:assert sha(blob(COMMIT,x['canonical_card']))==x['card_raw_sha256']
 cache=load(INT/'generated-card-cache64.json');assert len(cache['moved'])==443 and len(cache['skipped'])==2
 committed_card_paths=set(subprocess.check_output(['git','ls-tree','-r','--name-only',COMMIT,'--','research-wiki/sampling-sde-library/cards'],cwd=ROOT).decode().splitlines())
 for x in cache['moved']:
  validate(x,x['cache']);assert str(pth(x['cache']).resolve()).lower().startswith(str((ROOT/'.astis/pbps-centered-root64/generated-card-cache64').resolve()).lower());assert x['original'] not in committed_card_paths
 whitespace=load(INT/'staging-whitespace/diagnosis.json');assert len(whitespace['findings'])==585 and whitespace['full_staged_exit']==2 and whitespace['full_staged_called_PASS']==False and whitespace['authored_complement_exit']==0
 for x in whitespace['exact_immutable_raw_paths']:validate(x)
 # Separate independent read-only committed whitespace checks, excluding only the finite five immutable RAW artifact paths for authored complement.
 whitespace_runs=[]
 for label,args in [('full-commit-whitespace-cr-at-eol',['git','-c','core.whitespace=cr-at-eol','diff','--check',SCI,COMMIT]),('authored-commit-whitespace-cr-at-eol',['git','-c','core.whitespace=cr-at-eol','diff','--check',SCI,COMMIT,'--','.',*[f':(exclude){x["path"]}' for x in whitespace['exact_immutable_raw_paths']]])]:
  d=OUT/label;d.mkdir(exist_ok=True)
  with (d/'stdout.log').open('wb') as out,(d/'stderr.log').open('wb') as err:p=subprocess.Popen(args,cwd=ROOT,stdout=out,stderr=err);code=p.wait()
  expected=2 if label.startswith('full') else 0;assert code==expected;rr={'command':args,'actual_foreground_pid':p.pid,'exit_code':code,'terminal_closed':True,'stdout':pin(d/'stdout.log'),'stderr':pin(d/'stderr.log')};write(label+'/receipt.json',rr);whitespace_runs.append(rr)
 findings=(OUT/'full-commit-whitespace-cr-at-eol/stdout.log').read_text(encoding='utf-8');assert sum('trailing whitespace.' in l or 'space before tab in indent.' in l or 'new blank line at EOF.' in l for l in findings.splitlines())==585
 debt={'shared_cell_source_anchor':'PBPS2609.06905v1 AppendixD1 square-root monotonicity; ASTIS real-L2 consequence for actual B15','shared_cell_truth_boundary':'Arbitrary-real-L2 positive-square-order auxiliary result, with actual B15 consumer; independent reviews pending.'};cell=json.loads(blob(COMMIT,'research-wiki/frontier-cells/ASTIS-SHARED-l2-real-positive-square-order.json'));assert cell['source_anchor']==debt['shared_cell_source_anchor'] and cell['evidence']['truth_boundary']==debt['shared_cell_truth_boundary']
 for x in load(OUT/'input.manifest.json')['exact_inputs']:validate(x)
 result={'status':'PASS_WITH_BOUNDED_READER_AND_STALE_METADATA_DEBT','checked_commit':COMMIT,'science_parent':SCI,'actual_checker_pid':os.getpid(),'closed_science_reused':{'whole_logical_run_sha256':ad['native_run_sha256'],'distinct_complete_RAW_verdict_sha256':ad['native_complete_RAW_verdict_sha256'],'lease_RAW_sha256':ad['native_lease_RAW_sha256'],'native_owned_outputs_checked':72},'three_science_RAW_equal':science,'frozen_publication_audit_lesson_RAW_equal_science':True,'shared_root_changes':roots,'registry_count':510,'root_jobs':9172,'Tests_jobs':9468,'regressions':296,'publication_items':231,'accepted_actual_terminal_receipts':gates,'finite_exact_gate_historical_input_maps':historical,'same_Lean_graph_and_source_boundary':True,'bounded_graph_checks':graphchecks,'changed_graphs_and_enriched_cards':graphpins,'canonical_leaf_module_graph_entries':len(mods),'render_underlying_Lean_modules_displayed':936,'unchanged_unrelated_canonical_paths':preserved,'unchanged_canonical_card_metadata_count':len(preservation['preserved_canonical_metadata']),'reversible_default_card_cache_count':443,'render_PNGs':16,'copy_probe_PNGs':2,'total_native_PNGs':18,'representative_native_PNGs_independently_viewed':9,'initial_folded_copy_panels':panels,'RAW_UTF8_downloads':downloads,'all_12_literal_BODY_steps':body,'immutable_native_whitespace_findings':585,'full_staged_PASS':False,'authored_complement_PASS':True,'independent_committed_whitespace_receipts':whitespace_runs,'stale_metadata_debt':debt,'stale_metadata_policy':'Parent acknowledged exact two fields; future separately reviewed serialized metadata overlay. Canonical publication/source overlay stays authoritative; no native source review reopened.','native_source_math_decoder_distinct':True,'ledger_or_Git_or_canonical_mutation':False,'VERIFIED_transition':False,'remoteCI_main_live_fullExposition_PURIFIED_fullpaper_Goal_claim':False}
 write('checks.result.json',result);print(json.dumps({'status':result['status'],'actual_pid':os.getpid(),'checked_commit':COMMIT,'root_jobs':9172,'Tests_jobs':9468,'registry':510,'regressions':296,'publication':231,'preserved_unrelated':87,'default_cards_cached':443,'literal_BODY_steps':12,'native_PNGs':18,'independently_viewed_PNGs':9,'immutable_whitespace':585,'full_staged_PASS':False,'authored_complement_PASS':True}))
if __name__=='__main__':
 try:check()
 except Exception as e:write('checks.failure.json',{'actual_pid':os.getpid(),'exception':repr(e)});raise
