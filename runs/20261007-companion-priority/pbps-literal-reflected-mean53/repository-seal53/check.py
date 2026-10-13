import os,sys,json,pathlib,hashlib,datetime,subprocess,re,gzip
R=pathlib.Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-literal-reflected-mean53';O=B/'repository-seal53';SCI='9f0305db380966529eb3b0fc17a62aa9bcd47a85';COMMIT='ccc75d59bcc7fe303b3aa6e68252cfcc5867d090';TARGET='AutoSamplingTheory.ExampleCases.ProximalBPS.LiteralReflectedMean.reflected_gibbs_mean_c1';CELL='research-wiki/frontier-cells/ASTIS-SW-PBPS-literal-reflected-mean.json';AUDIT='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261008-PBPSLiteralReflectedMean.json'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def path(p):p=pathlib.Path(p);return p if p.is_absolute() else R/p
def load(p):return json.loads(path(p).read_text(encoding='utf-8'))
def dump(n,v):(O/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(b):return hashlib.sha256(b).hexdigest()
def logical(v):return sha(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode())
def pin(p):
 p=path(p);b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')))
def equal(e,p=None):
 a=pin(p or e['path']);return all(a[k]==e[k] for k in ('raw_sha256','lf_sha256')) and a['bytes']==e.get('bytes',e.get('raw_bytes',a['bytes']))
def git(*args):return subprocess.check_output(['git',*args],cwd=R,text=True,encoding='utf-8').strip()
def selfcheck(p,k):
 d=load(p);h=logical({x:y for x,y in d.items() if x!=k});assert h==d[k],str(p);return dict(input=pin(p),self_field=k,logical_sha256=h,recipe='SHA256 sorted compact UTF8 ensure_ascii=False allow_nan=False entire object minus named self field; no newline')
def strict(n):
 results=[]
 maps={AUDIT:B/'source-admission-before.0.raw.snapshot.audit.json',CELL:B/'source-admission-before.0.raw.snapshot.cell.json'}
 for label,rows in [('math492',load(B/'math-freeze.json')['inputs']),('source506',load(B/'source.0.review.json')['input_artifacts'])]:
  for e in rows:
   same=equal(e);snap=None
   if not same:assert label=='source506' and e['path'] in maps;snap=pin(maps[e['path']]);assert equal(e,maps[e['path']])
   results.append(dict(set=label,original=e,current=pin(e['path']),current_equal=same,exact_reviewed_original_snapshot=snap,ok=same or snap is not None))
 assert len(results)==998
 for row in load(B/'reviewer.source.inventory.json')['rows']:assert equal(row['snapshot']) and equal(row['original'],row['snapshot']['path'])
 d=dict(status='PASS',math_count=492,source_count=506,source_opening_snapshots=506,checks=results);dump(n,d);return d
if __name__=='__main__':
 if not (O/'lease.json').exists(): dump('lease.json',dict(status='OPEN',reviewer='whole_math52',opened_utc=utc(),actual_python_pid=os.getpid(),read='OPEN',write='OPEN',Python='OPEN',compiler='NOT_STARTED_CLOSED',checked_integration_commit=COMMIT,checked_science_commit=SCI,scope='Readonly independent scoped repository ProofSeal53; only repository-seal53 outputs owned. No compile/canonical/admission/VERIFIED/STABILIZING/commit/push/future54/55 read.'))
 assert git('rev-parse','HEAD')==COMMIT and git('rev-parse',COMMIT+'^')==SCI and not git('diff','--name-only','HEAD')
 strict('inputs.pre.json')
 native=[]
 for p,k in [('whole-proof-review53/run.json','run_sha256'),('exact-verification53/run.json','run_sha256'),('source.0.review.json','review_run_sha256'),('reviewer.source.run.json','run_sha256'),('reviewer.source.inventory.json','inventory_run_sha256'),('reviewer.source.lease.json','lease_run_sha256'),('source.review.lease.json','lease_run_sha256'),('anonymous-decoder/run.json','run_sha256')]:native.append(selfcheck(B/p,k))
 for p in ['whole-proof-review53/run.json','exact-verification53/run.json']:
  d=load(B/p)
  for e in d['actual_outputs']:assert equal(e),(p,e['path'])
 for p in ['whole-proof-review53/lease.json','whole-proof-review53/compiler.lease.json','exact-verification53/lease.json','exact-verification53/compiler.lease.json','reviewer.source.lease.json','source.review.lease.json','anonymous-decoder/lease.json','root.integration.0.lease.json','root.desktop-capture53.lease.json']:assert load(B/p)['status']=='CLOSED'
 for p in ['reviewer.source.run.json','reviewer.source.lease.json','source.review.lease.json']:
  for e in load(B/p).get('outputs',[]):assert equal(e)
 dr=load(B/'anonymous-decoder/run.json');res=load(B/'anonymous-decoder/result0.json');br=load(B/'anonymous-decoder/binding-receipt.json')
 for e in br['output_artifacts']:assert equal(e)
 assert logical(dr['run_binding_payload'])==dr['decoder_run_sha256']==res['decoder_run_sha256'] and logical(res)==dr['result_logical_sha256']
 assert isinstance(res['decoder'],str) and isinstance(res['reconstructed_theorem_text'],str) and sha(res['reconstructed_theorem_text'].encode())==res['reconstructed_text_sha256'] and not res['source_text_visible'] and not dr['exposures']['strict_source_identity_blindness']
 preserved=[]
 science_files=['AutoSamplingTheory/ExampleCases/ProximalBPS/LiteralReflectedMean.lean','Tests/ProximalBPSReflectedMeanRegularity.lean',AUDIT,'website/content/declaration_lessons/pbps-literal-reflected-mean.json','website/content/publications/pbps-literal-reflected-mean.json','runs/20261007-companion-priority/pbps-literal-reflected-mean53/source.0.review.json']
 for p in science_files:
  a=subprocess.check_output(['git','show',SCI+':'+p],cwd=R);b=subprocess.check_output(['git','show',COMMIT+':'+p],cwd=R);c=path(p).read_bytes();norm=lambda z:z.replace(b'\r\n',b'\n');assert norm(a)==norm(b)==norm(c)
  preserved.append(dict(current=pin(p),science_Git_raw_sha256=sha(a),science_Git_LF_sha256=sha(norm(a)),integration_Git_raw_sha256=sha(b),integration_Git_LF_sha256=sha(norm(b)),same_science_LF=True))
 for p,s in [(science_files[0],'production.actual.raw.snapshot.lean'),(science_files[1],'Tests.actual.raw.snapshot.lean')]:assert path(p).read_bytes()==path(B/'whole-proof-review53'/s).read_bytes()
 bb=path(science_files[0]).read_bytes();head=bb[bb.index(b'theorem reflected_gibbs_mean_c1'):bb.index(b' := by',bb.index(b'theorem reflected_gibbs_mean_c1'))].replace(b'\r\n',b'\n');assert len(head)==758 and sha(head)=='43d2831fa373729dc44cfd575fa4e1b68b2462688db8445320f13e433ddbe23e'
 notes=load(B/'integration.notes.json')
 for e in notes['checks']+notes['shared_files']:assert equal(e)
 gates=[]
 for p in sorted(B.glob('integration.0.*.status.json')):
  d=load(p);log=p.with_name(p.name.replace('.status.json','.log'));assert d['exit_code']==0 and d['proof_commit']==SCI and sha(log.read_bytes())==d['log_raw_sha256'];gates.append(dict(status=pin(p),log=pin(log),command=d['command'],exit_code=0,started_utc=d['started_utc'],finished_utc=d['finished_utc']))
 assert len(gates)==12
 assert 'Build completed successfully (9441 jobs).' in path(B/'integration.0.tests.log').read_text() and 'Build completed successfully (9156 jobs).' in path(B/'integration.0.mandatory.log').read_text() and 'ASTIS check passed' in path(B/'integration.0.mandatory.log').read_text()
 agg=path('AutoSamplingTheory/ExampleCases.lean').read_text();basic=path('Tests/Basic.lean').read_text();assert 'import AutoSamplingTheory.ExampleCases.ProximalBPS.LiteralReflectedMean' in agg and 'import Tests.ProximalBPSReflectedMeanRegularity' in path('Tests.lean').read_text() and re.search(r'formalizedTechnicalLemmaCount = 494 := by native_decide',basic)
 sys.path[:0]=[str(R),str(R/'tools'),str(R/'website/scripts')]
 from tools import astis_publication as pub,astis_advance as advance,astis
 code=astis.strip_lean_comments_and_strings(agg);assert not astis.LEAN_DECL_REGEX.search(code)
 reg=path('AutoSamplingTheory/TechnicalLemmas/Registry.lean').read_text();count=len(re.findall(r'status := LemmaMemoryStatus.formalizedLocal',reg));assert count==494 and TARGET in reg
 pub.check_advance([TARGET],reviewed=True)
 item=next(i for i in pub.load() if any(b['declaration']==TARGET for b in i['bindings']));binding=next(b for b in item['bindings'] if b['declaration']==TARGET);digest=pub.binding_digest(item,binding);assert digest=='f418bdbebf422f0ccb6feadbd83f4d8da8d6de35101705473bf57abbeaffc6ee'
 import publication_reader
 graph=load('_site/data/underlying-lean-graph.json');assert graph['publication_inputs_sha256']==publication_reader.graph_input_digest();report=pub.graph_report('ASTIS-SW-PBPS-literal-reflected-mean',R/'_site');assert report==load(B/'integration.0.graph.log')
 target='decl:'+TARGET;incident=[e for e in graph['edges'] if target in (e['source'],e['target'])];assert len(incident)==4 and {e['relation'] for e in incident}=={'declares','source reference (scanner)','Lean target under audit','source correspondence; not a Lean dependency'}
 dump('graph.current.json',dict(input=pin('_site/data/underlying-lean-graph.json'),publication_inputs_sha256=graph['publication_inputs_sha256'],own_helper_input_digest_equal=True,official_one_hop_report=report,incident=incident,semantics='Solid imports/module-declaration ownership are structural; dashed incomplete name/source/audit references are not certified theorem implication. ParentG and ParentA are real proof consumers despite their absence from the one-hop name scan. No conceptual bridge or Tf/domain completion inferred.'))
 state=advance.current_advances();sa=state['ASTIS-SA-20261008-PBPSLiteralReflectedMean'];assert sa['state']=='VERIFIED' and sa['latest_evidence']['verifier_id']=='whole_math52' and sa['latest_evidence']['verified_commit']==SCI
 lane=[i for i,d in state.items() if d.get('state')=='STABILIZING'];assert lane==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
 rows=path('runs/substantive_advances.jsonl').read_bytes().splitlines();verified=[json.loads(x) for x in rows if b'ASTIS-SA-20261008-PBPSLiteralReflectedMean' in x and json.loads(x).get('to_state')=='VERIFIED'];assert len(verified)==1 and verified[0]['worker_id']=='whole_math52'
 cell=load(CELL);assert cell['status']=='independently_verified' and isinstance(cell['evidence']['independent_verification'],str)
 original_cell=load(B/'exact-verification53/before.ASTIS-SW-PBPS-literal-reflected-mean.json');changed_cell={k for k in set(cell)|set(original_cell) if cell.get(k)!=original_cell.get(k)};assert changed_cell=={'status','evidence','blocked','purification'}
 assert cell['learning_contract']==original_cell['learning_contract'] and cell['blocked']['status'] is False and cell['purification']['status']=='pending'
 detail=cell['evidence']['independent_verification_details'];assert detail['checked_commit']==SCI and detail['verifier']=='whole_math52' and detail['focused_compiler_pid']==41368
 assert cell['evidence']['independent_verification']=='runs/20261007-companion-priority/pbps-literal-reflected-mean53/verified.json' and cell['evidence']['serialized_shared_gate']['status']=='PASS'
 dump('cell-integration-metadata.check.json',dict(status='PASS',immutable_exact_transition_cell_pin=load(B/'exact-verification53/transition.actual.json')['cell_after'],current_integrated_cell=pin(CELL),changed_top_fields_from_exact_pre_admission_snapshot=sorted(changed_cell),current_independent_evidence=cell['evidence'],blocked=cell['blocked'],purification=cell['purification'],learning_contract_unchanged=True,full_publication_binding_unchanged=digest,scope='Explicit independent VERIFICATION status/evidence plus serialized-root integration evidence/blocked/dead-code process metadata. Source/binders/proof/learning contracts preserved; pending purification is not promoted. No fake raw restoration or skipped mismatch.'))
 source=load(B/'source.0.review.json');audit=load(AUDIT);assert source['status']=='ACCEPTED_SCOPED_SOURCE_FIDELITY' and source['verdict']==audit['verdict']=='equivalent-after-elaboration' and not source['blocking'] and source['deltas']==source['repairs']==[]
 scan=[]
 for row in load(B/'whole-proof-review53/checks.json')['fake_closure_scan']:
  p=row['input']['path'];assert equal(row['input']);co=astis.strip_lean_comments_and_strings(path(p).read_text());hits=[n for n,l in enumerate(co.splitlines(),1) if astis.FORBIDDEN_REGEX.search(l)];assert not hits;scan.append(dict(input=pin(p),hits=hits))
 for p in ['prod.0','prod.1','Tests.0','Tests.1']:
  s=load(B/(p+'.status.json'));assert sha(path(B/(p+'.log')).read_bytes())==s['log_raw_sha256'] and load(B/(p+'.compiler.lease.json'))['status']=='CLOSED' and s['exit_code']==(1 if p.endswith('.0') else 0)
 assert 'sorryAx' in path(B/'Tests.0.log').read_text() and 'sorryAx' not in path(B/'Tests.1.log').read_text()
 visual=load(B/'visual.inspection.json');visualpins=[]
 for e in visual['artifacts']:
  actual=pin(e['portable_path']);assert actual['raw_sha256']==e['raw_sha256'] and actual['bytes']==e['bytes'];visualpins.append(actual)
 assert len(visualpins)==10
 for n in ['cdp','proof']:
  cp=load(B/'visual-inspection53'/(n+'.capture.json'));assert cp['ownedBrowserExit']['code']==0
 for name in ['companion','proof']:
  s=load(B/('desktop53.'+name+'.status.json'));assert s['exit_code']==0 and sha(path(B/('desktop53.'+name+'.log')).read_bytes())==s['log_raw_sha256']
 assert load(B/'root.desktop-capture53.lease.json')['exit_code']==0 and load(B/'root.integration.0.lease.json')['exit_code']==0
 fetch=load(B/'sync-before-aggregate53-fetch.json');assert fetch['fetch_exit']==0 and fetch['main_before']==fetch['main_after']==git('rev-parse','origin/main')=='c05de12e6a8ca7af8ce2df8608836f8d4e90f617' and sha(path(B/'sync-before-aggregate53-fetch.log').read_bytes())==fetch['fetch_log_raw_sha256']
 ws=[]
 for folder,nfinding,npaths,base,headcommit in [('whitespace-diagnosis53',646,195,'241e01d0d1917a6400a0f43ea48697b72cee88df',SCI),('integration-whitespace53',159,3,SCI,COMMIT)]:
  d=load(B/folder/'diagnosis.json');gz=path(d['gzip']['path']).read_bytes();negative=gzip.decompress(gz);assert sha(gz)==d['gzip']['raw_sha256'] and sha(negative)==d['full_negative_raw_sha256'] and int.from_bytes(gz[4:8],'little')==0 and d['full_staged_exit']==2
  assert (len(d['findings']) if isinstance(d['findings'],list) else d['findings'])==nfinding and len(d['immutable_raw_artifacts'])==npaths
  for e in d['immutable_raw_artifacts']:assert equal(e)
  orig=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--check',base,headcommit],cwd=R,capture_output=True);assert orig.returncode==2 and orig.stdout==negative
  exclusions=[e['path'] for e in d['immutable_raw_artifacts']];cmd=['git','-c','core.whitespace=cr-at-eol','diff','--check',base,headcommit,'--','.']+[':(exclude)'+p for p in exclusions];a=subprocess.run(cmd,cwd=R,capture_output=True);assert a.returncode==0;(O/(folder+'.authored.log')).write_bytes(a.stdout+a.stderr)
  ws.append(dict(diagnosis=pin(B/folder/'diagnosis.json'),gzip=pin(d['gzip']['path']),negative_raw_sha256=sha(negative),findings=nfinding,exact_paths=exclusions,authored_command=cmd,authored_exit=0,no_full_staged_PASS=True))
 changed=git('diff','--name-only',SCI,COMMIT).splitlines();assert not any(re.search(r'[A-Za-z-](?:54|55)/',p) for p in changed)
 delta=git('diff',SCI,COMMIT,'--','AutoSamplingTheory/ExampleCases.lean','Tests.lean','Tests/Basic.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean');(O/'shared-integration.diff.raw.snapshot.txt').write_text(delta+'\n',encoding='utf-8')
 dump('checks.json',dict(status='PASS',actual_python_pid=os.getpid(),checked_integration_commit=COMMIT,science_commit=SCI,compiler_invocations=0,all_math492_source506_originals_checked=True,native_logical_checks=native,science_preserved=preserved,integration_gates=gates,root_jobs=9156,test_jobs=9441,actual_root_lease=pin(B/'root.integration.0.lease.json'),Registry_formalizedLocal_count=count,Registry_total_records=len(re.findall(r'status := LemmaMemoryStatus\.',reg)),declaration_free_public_aggregator=pin('AutoSamplingTheory/ExampleCases.lean'),real_root_Test_Basic494_consumers=True,publication_binding_sha256=digest,real_check_advance_reviewed=True,current_cell=pin(CELL),only_independent_VERIFIED_transition=verified[0],sole_STABILIZING=lane,fake_closure_scan=scan,source_review_status=source['status'],source_review_verdict=source['verdict'],decoder_plain_string_and_source_text_blind=True,strict_decoder_identity_blind=False,visual_inputs=visualpins,visual_viewed_images=['cdp.pbps.png','cdp.branch.png','proof.proof.png','proof.proof-late.png'],owned_browser_HTTP_Node_CLOSED0=True,desktop_root_lease=pin(B/'root.desktop-capture53.lease.json'),whitespace=ws,fetch=pin(B/'sync-before-aggregate53-fetch.json'),origin_main_unchanged=True,integration_ownedpaths=changed,future54_55_not_integrated_or_read=True,remote_CI_boundary='No old52 CI applies to new53 science/integration head;53 not yet pushed. Actual old52 snapshot binding is a separate provenance check, not newhead acceptance.'))
 strict('inputs.post.json');print(json.dumps(dict(status='PASS',native_logical_checks=len(native),integration_gates=len(gates),Registry494=count,graph_incident_count=len(incident),visual_artifacts=len(visualpins),compiler_invocations=0)))
