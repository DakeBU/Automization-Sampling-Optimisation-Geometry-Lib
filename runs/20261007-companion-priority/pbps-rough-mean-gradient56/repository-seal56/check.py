from common import *
import gzip,runpy,copy
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,str(R));sys.path.insert(0,str(R/'tools'));sys.path.insert(0,str(R/'website/scripts'))
import astis,astis_advance,astis_publication,astis_site,publication_reader
assert git('rev-parse','HEAD')==BASE and subprocess.run(['git','merge-base','--is-ancestor',SCIENCE,BASE],cwd=R).returncode==0
E=B/'exact-verification56';W=B/'whole-math56';S=B/'source-review56';CELL=R/'research-wiki/frontier-cells/ASTIS-SW-PBPS-rough-mean-gradient.json';AUD=R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261008-PBPSRoughMeanGradient.json'
before=load(E/'readback.json')['exact_verified_admin_before_mappings'];shared=load(B/'verified-inputs.before-shared-integration.json')['mappings'];source=load(B/'root.source56.adoption.json')['historical_review_input_snapshot_mapping']
assert len(before)==2 and len(shared)==11 and len(source)==2
maps=[('source432_before_admission',m['original'],m['exactraw_snapshot']) for m in source]+[('exact_pretransition_before',m['original'],m['exact_before_snapshot']) for m in before]+[('postVERIFIED_before_shared',m['original'],m['snapshot']) for m in shared]
bindings=[];used=[];inputs={};selfs=[]
def check(e):
 dest=e;route='unchanged current'
 for kind,orig,snap in maps:
  if e==orig:dest=snap;route=kind;break
 assert e['raw_sha256']==dest['raw_sha256'] and e['lf_sha256']==dest['lf_sha256'] and e['bytes']==dest['bytes']
 assert equal(dest),(e,dest);a=pin(dest['path']);inputs[a['path']]=a;bindings.append({'original':e,'checked_actual':a,'route':route})
 if route!='unchanged current':used.append({'original':e,'exact_snapshot':dest,'route':route})
 return a
def current(p):a=pin(p);inputs[a['path']]=a;return a
def full(p,field):d=load(p);h=logical({k:v for k,v in d.items() if k!=field});assert h==d[field];selfs.append({'input':current(p),'self_field':field,'whole_object_logical_sha256':h,'recipe':'Entire object minus ONLY named field, sorted compact UTF8 JSON ensure_ascii=False allow_nan=False no newline'});return d
for kind,orig,snap in maps:check(orig);assert equal(snap)
mr=full(W/'run.json','run_sha256');full(W/'receipt.json','receipt_sha256');full(W/'lease.json','lease_sha256')
assert mr['review_binding_sha256']==logical(mr['review_binding_payload']) and load(W/'lease.json')['status']=='CLOSED'
for row in mr['inputs']['inputs']+mr['outputs_before_run']:check(row)
for row in load(B/'math-freeze.json')['inputs']:check(row)
assert len(load(B/'math-freeze.json')['inputs'])==418 and len(mr['inputs']['inputs'])==423
for row in load(W/'checks.json')['native_full_self_checks']:
 d=load(row['input']['path']);check(row['input']);field=row['self_field'];h=logical({k:v for k,v in d.items() if k!=field});assert h==row.get('whole_logical_sha256',row.get('logical_sha256'));selfs.append({'input':row['input'],'self_field':field,'whole_logical_sha256':h,'native_fields':d[field]})
for row in load(W/'checks.json')['actual_CLOSED_prior_leases']:check(row['input']);assert load(row['input']['path'])['status']=='CLOSED'
er=full(E/'run.json','run_sha256');full(E/'receipt.json','receipt_sha256');el=full(E/'lease.json','lease_sha256');full(E/'outputs.final.json','content_self_sha256');v=full(B/'verified.json','verified_sha256')
assert er['verifier_binding_sha256']==logical(er['verifier_binding_payload']) and el['status']=='CLOSED' and el['compiler_PID']==47152 and el['compiler_exit_code']==0
for row in er['inputs']['inputs']+er['actual_outputs_before_run']+load(E/'outputs.final.json')['outputs']:check(row)
for key in ('compiler_closed_lease','receipt','run','verified','transition','output_manifest','readback'):check(el[key])
assert v['checked_commit']==SCIENCE and v['verifier_id']=='whole_math52_exact56' and v['status']=='VERIFIED'
helper=R/'.astis/pbps-marginal-gradient51/require-verification56.py';hp=current(helper);adopted=runpy.run_path(str(helper))['require_verified']();assert adopted['root_native_pin_checks']==1468
dump('require-verified.actual.json',{'status':'PASS_READONLY_ACTUAL_CALL','helper':hp,'actual_python_PID':os.getpid(),'function':'require_verified','actual_native_pin_checks':1468,'checked_science_commit':adopted['verified_commit'],'recipe':'Actual exact two BEFORE mappings first and11 postVERIFIED pre-shared mappings only when complete original receipt equals row; no path-only fallback or source/Test substitution','no_saved_root_result_fabricated':True})
sr=full(S/'reviewer.source.run.json','run_sha256');full(S/'complete.json','content_self_sha256');full(S/'manifest.json','content_self_sha256');full(S/'source.review.json','content_self_sha256');full(B/'source.review.lease.json','content_self_sha256')
iv=load(S/'input-verification.json');assert len(iv['inputs'])==432
for e in iv['inputs']:
 check(e['input']);check(e['exactraw_snapshot']);check(e['crlf_to_lf_snapshot']);assert path(e['exactraw_snapshot']['path']).read_bytes().replace(b'\r\n',b'\n')==path(e['crlf_to_lf_snapshot']['path']).read_bytes()
for e in load(S/'manifest.json')['outputs']:check(e)
assert len(load(S/'manifest.json')['outputs'])==889
for p in (S/'decoder-locator-review56/review.json',S/'decoder-locator-review56/reviewer.operational.run.json',S/'decoder-locator-review56/lease.json'):full(p,'content_self_sha256')
for p,f in [(B/'anonymous-decoder/run.json','run_sha256'),(B/'anonymous-decoder/packet0.json','packet_sha256'),(B/'anonymous-decoder/lease.json','closure_record_sha256')]:full(p,f)
assert load(S/'result0.json')['verdict']=='equivalent-after-elaboration' and load(AUD)['state']=='accepted'
assert load(AUD)['source_review']['review_run_sha256']==sr['run_sha256']=='340a5136e28a8da11bbf7e285b83894416b54d4f743df3cdf26ba24d535568a8'
# Actual science delta1361 versus current exact reviewed historical snapshots.
science=load(E/'Git-science.entries.json')['entries'];assert len(science)==1361
for e in science:
 resolved=check(e['current']);assert resolved['lf_sha256']==e['Git_blob_LF_sha256']
# Actual committed integration delta, Git blobs batched through stdin.
raw=subprocess.check_output(['git','diff-tree','--no-commit-id','--raw','--no-abbrev','-r','-z',BASE],cwd=R);parts=raw.split(b'\0');entries=[]
for i in range(0,len(parts)-1,2):
 meta=parts[i].decode().split();p=parts[i+1].decode();assert meta[4] in ('A','M') and not re.search(r'(?:57|58)(?:/|$)',p);entries.append({'path':p,'mode':meta[1],'Git_blob':meta[3],'status':meta[4]})
buf=subprocess.check_output(['git','cat-file','--batch'],cwd=R,input=('\n'.join(e['Git_blob'] for e in entries)+'\n').encode());offset=0
for e in entries:
 end=buf.index(b'\n',offset);h=buf[offset:end].decode().split();size=int(h[2]);blob=buf[end+1:end+1+size];offset=end+1+size+1
 assert h[0]==e['Git_blob'] and blob.replace(b'\r\n',b'\n')==path(e['path']).read_bytes().replace(b'\r\n',b'\n'),e['path'];e.update(current=current(e['path']),Git_raw_sha256=sha(blob),Git_LF_sha256=sha(blob.replace(b'\r\n',b'\n')),Git_bytes=size)
assert offset==len(buf)
dump('Git.integration.json',{'status':'PASS','science':SCIENCE,'integration':BASE,'actual_changed_entries':len(entries),'entries':entries})
immutable=['AutoSamplingTheory/ExampleCases/ProximalBPS/RoughMeanGradient.lean','Tests/ProximalBPSRoughMeanGradient.lean','website/content/publications/pbps-rough-mean-gradient.json','website/content/declaration_lessons/pbps-rough-mean-gradient.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261008-PBPSRoughMeanGradient.json']
for p in immutable:
 blob=subprocess.check_output(['git','show',SCIENCE+':'+p],cwd=R);assert blob.replace(b'\r\n',b'\n')==path(p).read_bytes().replace(b'\r\n',b'\n');current(p)
P=path(immutable[0]);Q=path(immutable[1]);header=P.read_text(encoding='utf8');header=header[header.index('theorem actual_rough_mean_gradient'):header.index(' := by')]+'\n';assert len(header.encode())==1755 and sha(header.encode())=='fea2c3ade170bc0526d659f8c51abedaa0ce1a6186e75f0d8a2532b6608e94d8'
assert P.read_bytes()==(W/'production.raw.snapshot.lean').read_bytes() and Q.read_bytes()==(W/'Tests.raw.snapshot.lean').read_bytes()
sharedmap={m['original']['path']:m for m in shared}
def beforetext(p):return path(sharedmap[p]['snapshot']['path']).read_text(encoding='utf8')
example='AutoSamplingTheory/ExampleCases.lean';tests='Tests.lean';basic='Tests/Basic.lean';registry='AutoSamplingTheory/TechnicalLemmas/Registry.lean'
old=beforetext(example);new=path(example).read_text(encoding='utf8');added='import AutoSamplingTheory.ExampleCases.ProximalBPS.RoughMeanGradient\n';assert added in new and new.replace(added,'',1)==old
assert all(not line.strip() or line.strip().startswith('import ') for line in astis.strip_lean_comments_and_strings(new).splitlines())
old=beforetext(tests);new=path(tests).read_text(encoding='utf8');added='import Tests.ProximalBPSRoughMeanGradient\n';assert new.replace(added,'',1)==old
assert path(basic).read_text(encoding='utf8')==beforetext(basic).replace('formalizedTechnicalLemmaCount = 496','formalizedTechnicalLemmaCount = 497')
reg=path(registry).read_text(encoding='utf8');assert len(re.findall(r'status := LemmaMemoryStatus.formalizedLocal',reg))==497
assert reg.count('key := "pbps.actualL2.roughMeanGradient"')==1 and TARGET in reg
assert 'import AutoSamplingTheory.ExampleCases' in (R/'AutoSamplingTheory.lean').read_text(encoding='utf8')
cb=load(sharedmap[CELL.relative_to(R).as_posix()]['snapshot']['path']);ca=load(CELL)
def delta(x,y,p=''):
 if isinstance(x,dict) and isinstance(y,dict):
  z=[]
  for k in sorted(set(x)|set(y)):
   if k not in x or k not in y:z.append(p+'/'+k)
   else:z+=delta(x[k],y[k],p+'/'+k)
  return z
 return [] if x==y else [p]
changes=delta(cb,ca);assert set(changes)=={'/evidence/execution_boundary','/evidence/independent_verification','/evidence/serialized_shared_gate','/blocked/reason','/purification/dead_code_audit','/purification/scope'},changes
assert ca['status']=='independently_verified' and ca['purification']['status']=='pending' and ca['learning_contract']==cb['learning_contract'] and ca['target_statement']==cb['target_statement']
assert ca['evidence']['independent_verification']==(B/'verified.json').relative_to(R).as_posix()
notes=load(B/'integration.notes.json');assert notes['proof_commit']==SCIENCE and notes['registry_count']==497 and notes['root_jobs']==9159 and notes['test_jobs']==9447
for e in notes['checks']:check(e)
statuses=sorted(B.glob('integration.0.*.status.json'));assert len(statuses)==12
gates=[]
for p in statuses:
 d=load(p);log=p.with_name(p.name.replace('.status.json','.log'));assert d['exit_code']==0 and d['proof_commit']==SCIENCE and pin(log)['raw_sha256']==d['log_raw_sha256'];gates.append({'status':current(p),'actual_native_status':d,'log':current(log)})
assert 'Build completed successfully (9447 jobs)' in (B/'integration.0.tests.log').read_text(encoding='utf8')
mandatory=(B/'integration.0.mandatory.log').read_text(encoding='utf8');assert 'Build completed successfully (9159 jobs)' in mandatory and 'Build completed successfully (9447 jobs)' in mandatory and 'ASTIS check passed' in mandatory
rootlease=load(B/'root.integration.0.lease.json');capturelease=load(B/'root.desktop-capture56.lease.json');assert rootlease['status']==capturelease['status']=='CLOSED' and rootlease['exit_code']==capturelease['exit_code']==0
for p in [B/'root.integration.0.lease.json',B/'root.desktop-capture56.lease.json',B/'integration.notes.json',B/'visual.inspection.json']:current(p)
closures=[{'declaration':n,'axioms':[s.strip() for s in a.split(',')]} for n,a in re.findall(r"'([^']+)' depends on axioms: \[(.*?)\]",(B/'integration.0.tests.log').read_text(encoding='utf8'),re.S) if n==TARGET or n.startswith('Tests.ProximalBPSRoughMeanGradient.')];assert len(closures)==3 and all(set(x['axioms'])=={'propext','Classical.choice','Quot.sound'} for x in closures)
fake=[]
for p in [P,Q,path(example),path(tests)]:
 code=astis.strip_lean_comments_and_strings(p.read_text(encoding='utf8'));hits=[i for i,l in enumerate(code.splitlines(),1) if astis.FORBIDDEN_REGEX.search(l)];assert not hits;fake.append({'input':current(p),'findings':hits})
states=astis_advance.current_advances();assert states['ASTIS-SA-20261008-PBPSRoughMeanGradient']['state']=='VERIFIED' and states['ASTIS-SA-20261008-PBPSRoughMeanGradient']['last_actor']=='whole_math52_exact56'
assert [k for k,x in states.items() if x['state']=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
astis_publication.check_advance([TARGET],reviewed=True)
# Invoke exact official digest helper, record every actual canonical file read by the full computation.
graphreads=set()
def auditread(event,args):
 if event=='open' and args and isinstance(args[0],(str,bytes,os.PathLike)):
  p=path(os.fsdecode(args[0]));mode=args[1] if len(args)>1 else 'r'
  if str(p).lower().startswith(str(R).lower()) and (not isinstance(mode,str) or 'r' in mode):graphreads.add(p)
sys.addaudithook(auditread);astis_publication.inputs.cache_clear();astis_publication.load.cache_clear();digest=publication_reader.graph_input_digest()
gp=R/'_site/data/underlying-lean-graph.json';graph=load(gp);assert graph['publication_inputs_sha256']==digest
ident='decl:'+TARGET;node=next(x for x in graph['nodes'] if x['id']==ident);edges=[x for x in graph['edges'] if ident in (x['source'],x['target'])];assert len(edges)==7
canonical_graph_inputs=[]
for p in sorted(graphreads):
 if p.is_file() and p!=gp and '.lake' not in p.parts and O not in p.parents:canonical_graph_inputs.append(current(p))
current(gp);current(R/'website/scripts/publication_reader.py');current(R/'tools/astis_site.py');current(R/'tools/astis_publication.py')
dump('graph.boundary.json',{'status':'PASS_FULL_OFFICIAL_INPUT_DIGEST','official_helper':'publication_reader.graph_input_digest','full_native_digest':digest,'actual_generated_graph':pin(gp),'current_target':node,'exact_target_incident_count':7,'exact_target_incident_edges':edges,'actual_canonical_graph_input_count':len(canonical_graph_inputs),'actual_canonical_graph_inputs':canonical_graph_inputs,'semantics':'Solid imports/module ownership are structural; dashed source name-reference scans incomplete, incidental LogConcaveOn.prod is not a certified theorem implication. Three actual parents are justified by compiled reviewed body, not graph scans. No future57/58 reads or projected substitute digest.'})
for n,count,paths in [('whitespace-diagnosis56',48200,116),('integration-whitespace56',167,3)]:
 d=load(B/n/'diagnosis.json');z=path(d['gzip']['path']).read_bytes();plain=gzip.decompress(z);assert sha(z)==d['gzip']['raw_sha256'] and sha(plain)==d['full_negative_raw_sha256'];found=sorted(set(m.group(1).decode('utf8') for m in re.finditer(rb'(?m)^(.+?):[0-9]+: (?:trailing whitespace|new blank line at EOF|space before tab in indent|indent with spaces|tab in indent)',plain)));assert len(found)==paths and d['full_staged_exit']==2
 assert (d['findings'] if isinstance(d['findings'],int) else len(d['findings']))==count
 current(B/n/'diagnosis.json');current(d['gzip']['path']);dump(n+'.retained.json',{'status':'FULL_STAGED_NEGATIVE_RETAINED_NOT_PASS','findings':count,'exact_native_paths':paths,'paths':found,'gzip':pin(d['gzip']['path']),'decompressed_raw_sha256':sha(plain),'authored_complement':'Retained sequential batches64 PASS only; no blanket folder exclusion'})
vis=load(B/'visual.inspection.json');assert len(vis['viewed_images'])==4
for e in vis['artifacts']:
 p=e['portable_path'];a=current(p);assert a['raw_sha256']==e['raw_sha256'] and a['bytes']==e['bytes']
for p in (B/'visual-inspection56').iterdir():
 if p.is_file():current(p)
diagnosis=load(B/'integration-helper56.diagnosis.json');assert diagnosis['initial_exit']==1 and diagnosis['mathematical_route_changed']==False;assert pin(diagnosis['original_helper']['path'])['raw_sha256']==diagnosis['original_helper']['raw_sha256'];current(B/'integration-helper56.diagnosis.json');current(diagnosis['original_helper']['path'])
main=git('rev-parse','origin/main');assert main=='c05de12e6a8ca7af8ce2df8608836f8d4e90f617' and subprocess.run(['git','merge-base','--is-ancestor',main,BASE],cwd=R).returncode==0
assert git('status','--porcelain','--untracked-files=no')==''
dump('checks.json',{'status':'PASS_SCOPED_REPOSITORY56','science_commit':SCIENCE,'integration_commit':BASE,'strict_math_originals':418,'math_distinct_inputs':423,'science_actual_entries':1361,'integration_actual_entries':len(entries),'source_originals':432,'source_outputs':891,'actual_raw_LF_pin_check_count':len(bindings),'actual_raw_LF_pin_checks':bindings,'root_require_verified_actual_pin_count':1468,'native_complete_object_selfcheck_count':len(selfs),'native_complete_object_selfchecks':selfs,'exact_historical_mapping_usage':used,'before_maps':{'source_admission':2,'exact_verification':2,'before_shared':11},'cell_current_admin_delta_paths':changes,'current_cell_independently_verified':current(CELL),'source_audit':current(AUD),'actual12gates':gates,'root_jobs':9159,'Tests_jobs':9447,'Registry_count':497,'root_lease':pin(B/'root.integration.0.lease.json'),'capture_lease':pin(B/'root.desktop-capture56.lease.json'),'current_axiom_closures':closures,'fake_closure_scan':fake,'graph_digest':digest,'graph_evidence':pin(O/'graph.boundary.json'),'visual_captures_actually_viewed_by_independent_reviewer':['cdp.pbps.png','cdp.branch.png','proof.proof.png','proof.proof-late.png'],'visual_evidence':vis,'source_exposure_preserved':sr['exposure_and_negative_chronology'],'immutable_whitespace_debts':[pin(O/'whitespace-diagnosis56.retained.json'),pin(O/'integration-whitespace56.retained.json')],'helper_failed_admin_route':diagnosis,'sole_STABILIZING':'ASTIS-SA-20261005-SPHMCImplementedPhaseKernel','origin_main_ancestor':main,'tracked_worktree':'CLEAN','math_or_source_blockers':[],'remaining':load(E/'receipt.json')['remaining_boundary'],'scope':'Read-only scoped RepositoryProofSeal only, no compiler/new VERIFIED/canonical/ledger/PURIFIED/commit/push; future57/58 not read.'})
dump('inputs.pre-close.json',{'status':'PASS','science':SCIENCE,'integration':BASE,'actual_distinct_input_count':len(inputs),'inputs':[inputs[k] for k in sorted(inputs)],'raw_LF_recipe':'Actual raw bytes and exact CRLF->LF bytes, not JSON reserialization; historical mappings bind exact originals to actual raw snapshots only.'})
print(json.dumps({'status':'PASS_SCOPED_REPOSITORY56','science':SCIENCE,'integration':BASE,'actual_pin_checks':len(bindings),'distinct_inputs':len(inputs),'integration_entries':len(entries),'native_self_checks':len(selfs),'graph_digest':digest,'canonical_graph_inputs':len(canonical_graph_inputs),'no_compiler':True},ensure_ascii=False))
