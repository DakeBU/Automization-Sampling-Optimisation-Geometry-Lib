from common import *
sys.stdout.reconfigure(encoding='utf8');sys.path.insert(0,str(R));sys.path.insert(0,str(R/'tools'));sys.path.insert(0,str(R/'website/scripts'))
import astis,astis_advance,astis_publication,publication_reader
E=B/'exact-verification57';W=B/'whole-math57';S=B/'source-review57'
CELL=R/'research-wiki/frontier-cells/ASTIS-SHARED-gaussian-marginal-poincare.json';AUD=R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261008-GaussianMarginalPoincare.json'
assert git('rev-parse','HEAD')==BASE
assert subprocess.run(['git','merge-base','--is-ancestor',SCIENCE,BASE],cwd=R).returncode==0
v=load(B/'verified.json');shared=load(B/'verified-inputs.before-shared-integration.json')['mappings'];srcmaps=load(B/'root.source57.adoption.json')['historical_review_input_snapshot_mapping'];before=v['exact_verified_admin_before_mappings']
assert (len(srcmaps),len(before),len(shared))==(2,2,11)
maps=[('source_admission',m['original'],m['exactraw_snapshot']) for m in srcmaps]+[('exact_transition',m['original'],m['exactraw_snapshot']) for m in before]+[('postVERIFIED_before_shared',m['original'],m['snapshot']) for m in shared]
dec=load(B/'decoded.0.json');temporal=dec['initial_OPEN_lease_mapping'];maps.append(('decoder_original_OPEN',temporal['original'],temporal['actual_preserved']))
inputs={};bindings=[];selfs=[];payloads=[];used=[]
def current(p):a=pin(p);inputs[a['path']]=a;return a
def check(e):
 a=pin(e['path']);route='actual_current';dest=e
 if not matches(e,a):
  for kind,orig,snap in maps:
   if path(e['path'])==path(orig['path']) and matches(e,orig):dest=snap;route=kind;a=pin(dest['path']);break
  else:
   m=v['ledger_before_prefix_mapping'];orig=m['original']
   if path(e['path'])==path(orig['path']) and matches(e,orig):
    b=path(e['path']).read_bytes()[:orig['bytes']];lf=b.replace(b'\r\n',b'\n');assert sha(b)==e['raw_sha256'] and sha(lf)==e['lf_sha256'];route='exact_append_only_ledger_prefix';a=pin(e['path']);dest=e
   else:raise AssertionError(('No exact historical mapping',e,a))
 if route!='exact_append_only_ledger_prefix':assert matches(e,a),(e,a,route)
 inputs[a['path']]=a;bindings.append(dict(original=e,actual=a,route=route,exact_snapshot=dest if route!='actual_current' else None))
 if route!='actual_current':used.append(bindings[-1])
 return a
def walk(d):
 if isinstance(d,dict):
  if {'path','raw_sha256','lf_sha256','bytes'}<=set(d):check(d)
  else:
   for x in d.values():walk(x)
 elif isinstance(d,list):
  for x in d:walk(x)
def full(p,field):
 d=load(p);h=logical({k:v for k,v in d.items() if k!=field});assert h==d[field],(p,field)
 selfs.append(dict(input=current(p),self_field=field,logical_sha256=h,recipe='Entire object minus ONLY named top-level field; sorted compact UTF8 ensure_ascii=False allow_nan=False, no newline'));return d
def payload(d,k,h,p):assert logical(d[k])==d[h];payloads.append(dict(input=current(p),payload_field=k,digest_field=h,logical_sha256=d[h],recipe='Entire named component only; same sorted compact UTF8 recipe, distinct from full-object self digest'))
for kind,orig,snap in maps:assert matches(orig,pin(snap['path']));current(snap['path'])
mf=load(B/'math-freeze.json');assert len(mf['inputs'])==602
for x in mf['inputs']:check(x)
mr=full(W/'run.json','run_sha256');ml=full(W/'lease.json','lease_sha256');full(W/'receipt.json','receipt_sha256');payload(mr,'review_binding_payload','review_binding_payload_sha256',W/'run.json')
assert len(mr['inputs'])==611 and ml['status']=='CLOSED' and ml['actual_compiler_exit_code']==0
for x in mr['inputs']:check(x)
walk(ml['outputs'])
mc=load(W/'checks.json')
for group in ['native_whole_object_self_checks','prior_review_self_checks']:
 for row in mc[group]:
  if 'input' in row:check(row['input']);full(row['input']['path'],row['self_field'])
  else:full(row['path'],row['field'])
walk(mc['original_closed_output_checks']);walk(mc['actual_prior_CLOSED_leases'])
for row in mc['actual_prior_CLOSED_leases']:
 d=load(row['path']);assert d.get('status',d.get('state'))=='CLOSED'
er=full(E/'run.json','run_sha256');el=full(E/'lease.json','lease_sha256');full(E/'receipt.json','receipt_sha256');full(B/'verified.json','verified_sha256');payload(er,'verifier_binding_payload','verifier_binding_payload_sha256',E/'run.json')
assert el['status']=='CLOSED' and el['actual_compiler_exit_code']==0 and v['checked_commit']==SCIENCE and v['verifier_id']=='whole_math52_exact57'
assert len(er['inputs'])==1955
walk(er['inputs']);walk(el['outputs']);walk(load(E/'outputs.final.json'))
sr=full(S/'reviewer.source.run.json','run_sha256')
for p in ['source.review.json','input.manifest.json','input-verification.json','manifest.json','output.readbacks.json','publication.binding.payload.json']:full(S/p,'content_self_sha256')
sl=full(B/'source.review.lease.json','content_self_sha256');assert sl['status']=='CLOSED'
sm=load(S/'input.manifest.json');assert len(sm['pins'])==614;walk(sm['pins']);walk(sl['actual_output_artifacts'])
out=load(S/'output.readbacks.json')['artifacts'];assert len(out)==1251 and len(sl['actual_output_artifacts'])==1252
assert {path(x['path']) for x in sl['actual_output_artifacts']}-{path(x['path']) for x in out}=={S/'output.readbacks.json'}
walk(load(S/'input-verification.json'))
sp=load(S/'publication.binding.payload.json');payload(sp,'payload','named_payload_sha256',S/'publication.binding.payload.json')
for p,f in [('run.json','run_sha256'),('packet0.json','packet_sha256')]:full(B/'anonymous-decoder'/p,f)
dl=load(B/'anonymous-decoder/lease.json');assert dl['status']=='CLOSED';current(B/'anonymous-decoder/lease.json');walk(load(B/'anonymous-decoder/run.json'))
result=load(S/'result0.json');assert result['verdict']=='equivalent-after-elaboration' and load(AUD)['state']=='accepted'
current(S/'result0.json');current(AUD);current(B/'root.source57.adoption.json')
# Actual Git science and integration entries, stdin-batched blobs (no command-line path expansion).
def blobs(entries,key):
 p=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE);buf,err=p.communicate(('\n'.join(e[key] for e in entries)+'\n').encode());assert p.returncode==0;off=0;rows=[]
 for e in entries:
  end=buf.index(b'\n',off);h=buf[off:end].decode().split();n=int(h[2]);b=buf[end+1:end+1+n];off=end+1+n+1;assert h[0]==e[key];rows.append(b)
 assert off==len(buf);return rows,p.pid
sg=load(E/'science.gitbindings.json');assert len(sg['entries'])==1923
sd=subprocess.check_output(['git','diff-tree','--no-commit-id','--raw','--no-abbrev','-r','-z',SCIENCE],cwd=R).split(b'\0')
actual_science={(sd[i+1].decode(),sd[i].decode().split()[3]) for i in range(0,len(sd)-1,2)}
assert actual_science=={(e['path'],e['git_blob']) for e in sg['entries']} and len(actual_science)==1923
sb,pid=blobs(sg['entries'],'git_blob')
for e,b in zip(sg['entries'],sb):check(e['current']);assert sha(b)==e['git_raw_sha256'] and sha(b.replace(b'\r\n',b'\n'))==e['current']['lf_sha256']
raw=subprocess.check_output(['git','diff-tree','--no-commit-id','--raw','--no-abbrev','-r','-z',BASE],cwd=R);parts=raw.split(b'\0');entries=[]
for i in range(0,len(parts)-1,2):
 m=parts[i].decode().split();p=parts[i+1].decode();assert m[4] in ('A','M') and not re.search(r'(?:58|59)(?:/|$)',p);entries.append(dict(path=p,git_blob=m[3],change=m[4]))
bs,ipid=blobs(entries,'git_blob')
for e,b in zip(entries,bs):
 a=current(e['path']);assert sha(b.replace(b'\r\n',b'\n'))==a['lf_sha256'];e.update(current=a,git_bytes=len(b),git_raw_sha256=sha(b),git_lf_sha256=sha(b.replace(b'\r\n',b'\n')))
assert all(e['path'].startswith(B.relative_to(R).as_posix()+'/') or path(e['path']) in {path(m['original']['path']) for m in shared} for e in entries)
dump('Git.integration.json',dict(status='PASS',science=SCIENCE,integration=BASE,entries=entries,actual_entry_count=len(entries),actual_cat_file_PID=ipid,actual_exit_code=0,resource='CLOSED'))
P=R/'AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/GaussianMarginalPoincare.lean';Q=R/'Tests/GaussianMarginalPoincare.lean'
for p in [P,Q,R/'website/content/publications/gaussian-marginal-poincare.json',R/'website/content/declaration_lessons/gaussian-marginal-poincare.json',AUD]:
 blob=subprocess.check_output(['git','show',SCIENCE+':'+p.relative_to(R).as_posix()],cwd=R);assert sha(blob.replace(b'\r\n',b'\n'))==current(p)['lf_sha256']
check(load(W/'receipt.json')['focused_Lean_gate']['production']);check(load(W/'receipt.json')['focused_Lean_gate']['Tests'])
header=P.read_text(encoding='utf8');header=header[header.index('theorem actual_gaussian_marginal_centered_poincare'):header.index(' := by')]+'\n';assert len(header.encode())==1244 and sha(header.encode())=='e706b4e6c3c07f58a090ee86cb51dd91be2f11afe707db653737e4983c7181e9'
sharedmap={path(m['original']['path']):m for m in shared}
def old(p):return path(sharedmap[path(p)]['snapshot']['path']).read_text(encoding='utf8')
agg=R/'AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities.lean';t=R/'Tests.lean';basic=R/'Tests/Basic.lean';reg=R/'AutoSamplingTheory/TechnicalLemmas/Registry.lean'
new=agg.read_text(encoding='utf8');added='import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalPoincare\n';assert new.replace(added,'',1)==old(agg)
assert all(not l.strip() or l.strip().startswith('import ') for l in astis.strip_lean_comments_and_strings(new).splitlines())
assert t.read_text(encoding='utf8').replace('import Tests.GaussianMarginalPoincare\n','',1)==old(t)
assert basic.read_text(encoding='utf8')==old(basic).replace('formalizedTechnicalLemmaCount = 497','formalizedTechnicalLemmaCount = 498')
assert len(re.findall('status := LemmaMemoryStatus.formalizedLocal',reg.read_text(encoding='utf8')))==498 and TARGET in reg.read_text(encoding='utf8')
for p,imp in [(R/'AutoSamplingTheory.lean','import AutoSamplingTheory.TechnicalLemmas'),(R/'AutoSamplingTheory/TechnicalLemmas.lean','import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities')]:assert imp in p.read_text(encoding='utf8');current(p)
def delta(x,y,p=''):
 if isinstance(x,dict) and isinstance(y,dict):
  z=[]
  for k in sorted(set(x)|set(y)):z+=([p+'/'+k] if k not in x or k not in y else delta(x[k],y[k],p+'/'+k))
  return z
 return [] if x==y else [p]
cb=load(sharedmap[CELL]['snapshot']['path']);ca=load(CELL);changes=delta(cb,ca)
assert ca['status']=='independently_verified' and ca['learning_contract']==cb['learning_contract'] and ca['target_statement']==cb['target_statement']
assert all(x.startswith(('/evidence/','/blocked/','/purification/')) for x in changes),changes
notes=load(B/'integration.notes.json');assert (notes['root_jobs'],notes['test_jobs'],notes['registry_count'])==(9160,9449,498);walk(notes['checks']);walk(notes['shared_files']);gates=[]
for p in sorted(B.glob('integration.0.*.status.json')):
 d=load(p);log=p.with_name(p.name.replace('.status.json','.log'));assert d['exit_code']==0 and d['proof_commit']==SCIENCE and current(log)['raw_sha256']==d['log_raw_sha256'];gates.append(dict(status=current(p),native=d,log=pin(log)))
assert len(gates)==12
tl=(B/'integration.0.tests.log').read_text(encoding='utf8');mlog=(B/'integration.0.mandatory.log').read_text(encoding='utf8');assert 'Build completed successfully (9449 jobs)' in tl and 'Build completed successfully (9160 jobs)' in mlog and 'ASTIS check passed' in mlog
closures=[dict(declaration=n,axioms=[s.strip() for s in a.split(',')]) for n,a in re.findall(r"'([^']+)' depends on axioms: \[(.*?)\]",tl,re.S) if n==TARGET or n.startswith('Tests.GaussianMarginalPoincare.')];assert len(closures)==2 and all(set(x['axioms'])=={'propext','Classical.choice','Quot.sound'} for x in closures)
fake=[]
for p in [P,Q,agg,t]:
 code=astis.strip_lean_comments_and_strings(p.read_text(encoding='utf8'));hits=[i for i,l in enumerate(code.splitlines(),1) if astis.FORBIDDEN_REGEX.search(l)];assert not hits;fake.append(dict(input=current(p),findings=hits))
states=astis_advance.current_advances();assert states['ASTIS-SA-20261008-GaussianMarginalPoincare']['state']=='VERIFIED' and states['ASTIS-SA-20261008-GaussianMarginalPoincare']['last_actor']=='whole_math52_exact57';assert [k for k,x in states.items() if x['state']=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
astis_publication.check_advance([TARGET],reviewed=True)
reads=set()
def readhook(event,args):
 if event=='open' and args and isinstance(args[0],(str,bytes,os.PathLike)):
  p=path(os.fsdecode(args[0]));mode=args[1] if len(args)>1 else 'r'
  if str(p).lower().startswith(str(R).lower()) and (not isinstance(mode,str) or 'r' in mode):reads.add(p)
sys.addaudithook(readhook);astis_publication.inputs.cache_clear();astis_publication.load.cache_clear();digest=publication_reader.graph_input_digest();gp=R/'_site/data/underlying-lean-graph.json';graph=load(gp);assert graph['publication_inputs_sha256']==digest
ident='decl:'+TARGET;node=next(x for x in graph['nodes'] if x['id']==ident);edges=[x for x in graph['edges'] if ident in (x['source'],x['target'])];assert len(edges)==7
graphinputs=[current(p) for p in sorted(reads) if p.is_file() and p!=gp and '.lake' not in p.parts and O not in p.parents]
import inspect
helper_source=inspect.getsource(publication_reader.graph_input_digest).encode('utf8')
dump('graph.boundary.json',dict(status='PASS_FULL_NATIVE_DIGEST',helper=current(R/'website/scripts/publication_reader.py'),selected_helper_source_utf8=helper_source.decode(),selected_helper_bytes=len(helper_source),selected_helper_sha256=sha(helper_source),normative_dependencies=[current(R/'tools/astis_publication.py'),current(R/'tools/astis_site.py')],full_native_digest=digest,generated=current(gp),actual_canonical_input_count=len(graphinputs),actual_canonical_inputs=graphinputs,exact_target=node,incident_edges=edges,semantics='Module/import ownership is structural. Dashed name references are explicitly incomplete; incidental LogConcaveOn calls are not certified theorem edges. Actual six mathematical parents follow compiled reviewed body, not scanner certification.'))
debts=[]
for name,n,paths in [('whitespace-diagnosis57',3809,309),('integration-whitespace57',None,None)]:
 d=load(B/name/'diagnosis.json');z=path(d['gzip']['path']).read_bytes();plain=gzip.decompress(z);assert sha(z)==d['gzip']['raw_sha256'] and sha(plain)==d['full_negative_raw_sha256'] and int.from_bytes(z[4:8],'little')==0 and d['full_staged_exit']==2 and d.get('authored_exit',d.get('authored_check_exit'))==0
 count=d['findings'] if isinstance(d['findings'],int) else len(d['findings']);pp=sorted(set(re.findall(rb'(?m)^(.+?):[0-9]+: (?:trailing whitespace|new blank line at EOF|space before tab in indent)',plain)))
 if n is not None:assert count==n and len(pp)==paths
 walk(d['immutable_raw_artifacts']);walk(d['gzip']);walk(d.get('authored_log',[]));current(B/name/'diagnosis.json');debts.append(dict(name=name,full_staged='NEGATIVE_RETAINED_NOT_PASS',findings=count,exact_native_paths=len(pp),paths=[x.decode() for x in pp],gzip=current(d['gzip']['path']),decompressed_sha256=sha(plain),authored_complement_only='Sequential bounded path batches PASS; no folder blanket exclusion'))
vis=load(B/'visual.inspection.json');assert len(vis['viewed_images'])==4
for e in vis['artifacts']:
 a=current(e['portable_path']);assert a['bytes']==e['bytes'] and a['raw_sha256']==e['raw_sha256']
capture_records=[]
for name in ['cdp.capture.json','proof.capture.json']:
 d=load(B/'visual-inspection57'/name);assert d['ownedBrowserExit']['code']==0 and d['ownedBrowserExit']['signal'] is None;capture_records.append(dict(input=current(B/'visual-inspection57'/name),native=d))
dump('visual-review.json',dict(status='FOUR_ACTUAL_ARCHIVED_CAPTURES_INDEPENDENTLY_VIEWED',images=vis['viewed_images'],artifacts=vis['artifacts'],capture_records=capture_records,observations='All six formula steps visible, complete actual-source statement visible, exact Lean initially folded. Actual source-table horizontal scrollbar and right-column clipping retained as presentation debt. Graph explicitly incomplete name-reference scanning, not six-parent implication certification. No mobile/physical/live/full-reader/PURIFIED acceptance.'))
for name in ['root.integration.0.lease.json','root.desktop-capture57.lease.json']:
 d=load(B/name);assert d['status']=='CLOSED' and d['exit_code']==0;current(B/name)
for name in ['desktop57.companion.status.json','desktop57.proof.status.json']:
 d=load(B/name);assert d['exit_code']==0;current(B/name);log=B/name.replace('.status.json','.log');assert current(log)['raw_sha256']==d['log_raw_sha256']
current(B/'visual.inspection.json');current(B/'integration.notes.json');current(B/'verified-inputs.before-shared-integration.json')
main=git('rev-parse','origin/main');assert subprocess.run(['git','merge-base','--is-ancestor',main,BASE],cwd=R).returncode==0;assert git('status','--porcelain','--untracked-files=no')==''
dump('checks.json',dict(status='PASS_SCOPED_REPOSITORY57',science_commit=SCIENCE,integration_commit=BASE,math_originals=602,math_distinct_inputs=611,source_originals=614,source_terminal_outputs=1252,source_predecessor_outputs=1251,science_entries=1923,integration_entries=len(entries),actual_pin_check_count=len(bindings),actual_pin_checks=bindings,native_selfcheck_count=len(selfs),native_selfchecks=selfs,named_payload_checks=payloads,historical_mapping_usage=used,exact_mapping_counts=dict(source=2,transition=2,shared=11,decoder_OPEN=1),current_cell_admin_delta_paths=changes,actual12gates=gates,root_jobs=9160,Tests_jobs=9449,Registry_count=498,axiom_closures=closures,fake_closure_scan=fake,graph_digest=digest,graph_canonical_input_count=len(graphinputs),actual_visual_images_independently_viewed=vis['viewed_images'],visual_debts=['Actual source-table horizontal scrollbar/right-column clipping; dense ASCII notation, long companion layout, repeated heading and awkward qualified graph linewrap. Formulas visible and Lean initially folded.','Graph scanner references incomplete; root six-parent prose justified by reviewed body, not all-six scanner edges. Separate ExpositionSeal/full-reader acceptance.'],whitespace_debts=debts,sole_STABILIZING='ASTIS-SA-20261005-SPHMCImplementedPhaseKernel',origin_main_ancestor=main,tracked_tree='CLEAN',source_math_blockers=[],remaining_truth_boundary=v['remaining_truth_boundary'],compiler='NOT_STARTED_CLOSED'))
dump('inputs.pre-close.json',dict(status='PASS',actual_distinct_input_count=len(inputs),inputs=[inputs[k] for k in sorted(inputs)],raw_LF_recipe='Exact raw bytes and only CRLF pairs -> LF, preserving actual lengths. Exact full-row historical mappings or exact append-only ledger prefix; never path-only fallback.'))
print(json.dumps(dict(status='PASS_SCOPED_REPOSITORY57',pin_checks=len(bindings),distinct_inputs=len(inputs),native_selfchecks=len(selfs),integration_entries=len(entries),graph_inputs=len(graphinputs),compiler='NOT_STARTED_CLOSED')))
