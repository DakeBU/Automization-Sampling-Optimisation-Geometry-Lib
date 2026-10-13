from common import *
import importlib.util,gzip
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tools'));sys.path.insert(0,str(ROOT/'website/scripts'))
assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==HEAD
inputs={};reads=set();checks=[]
def audit(event,args):
 if event=='open' and isinstance(args[0],(str,bytes,pathlib.Path)):
  p=pathlib.Path(os.fsdecode(args[0]));p=p if p.is_absolute() else ROOT/p
  if p.is_relative_to(ROOT):
   rel=p.relative_to(ROOT).as_posix()
   if any(re.search(r'(?:59|60)(?:-|$)',part) for part in p.relative_to(ROOT).parts[:-1]) and rel.startswith(('runs/','.astis/')):raise RuntimeError('future packet directory read denied: '+rel)
   if not p.is_relative_to(D):reads.add(p.as_posix())
sys.addaudithook(audit)
write(D/'lease.open.json',dict(status='OPEN',actor=ACTOR,checked_science_commit=SCI,checked_integration_commit=HEAD,actual_worker_PID=os.getpid(),compiler='NOT_STARTED_CLOSED',read='OPEN',write='OPEN',Python='OPEN'))
# Invoke only the exported read-only function, never its mutating __main__.
helper=R/'root-executed58/require-verification58.py';spec=importlib.util.spec_from_file_location('required58_readonly',helper);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);v=mod.require_verified();assert v['verified_commit']==SCI and v['actual_root_native_pin_checks']==3840
write(D/'native-verification.actual.json',dict(status='PASS',actual_PID=os.getpid(),helper=pin(helper),exact_function='require_verified',no___main___execution=True,actual_return=v))
freeze=load(R/'math-freeze.json');assert len(freeze['inputs'])==72
for row in freeze['inputs']:checks.append(dict(expected=row,actual=check(row)))
# Integration commit only: exact 153 paths through bounded cat-file batch.
names=subprocess.check_output(['git','diff','--name-only','-z',SCI,HEAD]).split(b'\0');names=[n.decode() for n in names if n];assert len(names)==153
assert all(n.startswith('runs/20261007-companion-priority/pbps-macroscopic-centered-range58/') or n in ['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl','runs/substantive_advances.jsonl','website/content/samplewiki_companion_frontiers.json'] or n in ['research-wiki/frontier-cells/'+c+'.json' for c in load(R/'proved-local.json')['active_cells']] for n in names)
p=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate(''.join(HEAD+':'+n+'\n' for n in names).encode());assert p.returncode==0
pos=0;gitrows=[]
for n in names:
 end=out.index(b'\n',pos);h=out[pos:end].decode().split();assert h[1]=='blob';size=int(h[2]);b=out[end+1:end+1+size];pos=end+size+2;a=pin(n);assert a['lf_sha256']==sha(b.replace(b'\r\n',b'\n'));gitrows.append(dict(path=n,git_blob_oid=h[0],git_raw_sha256=sha(b),git_lf_sha256=sha(b.replace(b'\r\n',b'\n')),current=a))
write(D/'integration.git.json',dict(status='PASS',checked_commit=HEAD,science_parent=SCI,entry_count=len(names),actual_cat_file_PID=p.pid,actual_exit_code=0,entries=gitrows))
claim=load(R/'proved-local.json');fixed=claim['lean_files']+['website/content/publications/'+n+'.json' for n in ['l2-pullback-range','pbps-macroscopic-centered-range','pbps-centered-macro-defect-gap']]+['website/content/declaration_lessons/'+n+'.json' for n in ['l2-pullback-range','pbps-macroscopic-centered-range','pbps-centered-macro-defect-gap']]+['research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261008-'+n+'.json' for n in ['L2PullbackRange','PBPSMacroscopicCenteredRange','PBPSCenteredMacroDefectGap']]
unchanged=[]
for n in fixed+['AutoSamplingTheory/TechnicalLemmas/Measure.lean']:
 b=subprocess.check_output(['git','show',SCI+':'+n]);c=subprocess.check_output(['git','show',HEAD+':'+n]);assert b==c and sha(b.replace(b'\r\n',b'\n'))==pin(n)['lf_sha256'];unchanged.append(dict(path=n,science_git_raw_sha256=sha(b),integration_git_raw_sha256=sha(c),current=pin(n)))
notes=load(R/'integration.notes.json');assert (notes['registry_count'],notes['root_jobs'],notes['test_jobs'])==(500,9162,9452)
for row in rows(notes):checks.append(dict(expected=row,actual=check(row)))
gates=[]
labels=['tests','mandatory','pycompile','whitespace','publication','semantic','frontier','contributor','site-build','official-graph','graph','graph-macro','graph-consumer','site-check']
for n in labels:
 s=load(R/f'integration.1.{n}.status.json');log=R/f'integration.1.{n}.log';assert s['exit_code']==0 and s['proof_commit']==SCI and sha(log.read_bytes())==s['log_raw_sha256'];gates.append(dict(name=n,status=pin(R/f'integration.1.{n}.status.json'),log=pin(log),actual_exit_code=0,command=s['command']))
mandatory=(R/'integration.1.mandatory.log').read_text(encoding='utf8');tests=(R/'integration.1.tests.log').read_text(encoding='utf8');assert re.findall(r'Build completed successfully \((\d+) jobs\)',mandatory)[-2:]==['9162','9452'] and 'ASTIS check passed' in mandatory and 'Build completed successfully (9452 jobs)' in tests
for f,rc in [('root.integration.1.lease.json',0),('root.integration.0.lease.json',1),('root.desktop-capture58.lease.json',0)]:
 q=load(R/f);assert q['status']=='CLOSED' and q['exit_code']==rc
for n in ['companion','proof']:
 q=load(R/f'desktop58.{n}.status.json');assert q['exit_code']==0 and sha((R/f'desktop58.{n}.log').read_bytes())==q['log_raw_sha256']
neg=load(R/'integration.0.route-diagnosis.json');assert neg['blocker_class']=='conservative-changed-module-publication' and load(R/'integration.0.publication.status.json')['exit_code']==1
imports={n:path(n).read_bytes().replace(b'\r\n',b'\n').decode() for n in ['AutoSamplingTheory/TechnicalLemmas.lean','AutoSamplingTheory/ExampleCases.lean','Tests.lean']}
assert 'import AutoSamplingTheory.TechnicalLemmas.Measure.L2PullbackRange\n' in imports['AutoSamplingTheory/TechnicalLemmas.lean'];assert 'import AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicRange\n' in imports['AutoSamplingTheory/ExampleCases.lean'];assert 'import Tests.ProximalBPSMacroscopicRange\n' in imports['Tests.lean']
from tools import astis,astis_advance
assert not re.search(r'\b(theorem|lemma|def|axiom|instance|opaque|abbrev)\b',astis.strip_lean_comments_and_strings(imports['AutoSamplingTheory/TechnicalLemmas.lean']))
registry=(ROOT/'AutoSamplingTheory/TechnicalLemmas/Registry.lean').read_text(encoding='utf8');assert all(n in registry for n in claim['lean_declarations'][:2]) and claim['lean_declarations'][2] not in registry
assert 'formalizedTechnicalLemmaCount = 500' in (ROOT/'Tests/Basic.lean').read_text(encoding='utf8')
state=astis_advance.current_advances();assert state['ASTIS-SA-20261008-PBPSMacroscopicCenteredRange']['state']=='VERIFIED';assert [k for k,q in state.items() if q['state']=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
admin=[];maps=load(R/'verified-inputs.before-shared-integration.json')['mappings'];assert len(maps)==7
for m in maps:
 assert all(m['original'][k]==m['snapshot'][k] for k in ['bytes','raw_sha256','lf_bytes','lf_sha256']);check(m['snapshot'])
 if '/frontier-cells/' in m['original']['path']:
  old=load(path(m['snapshot']['path']));cur=load(path(m['original']['path']));ds=diff(old,cur);assert cur['status']=='independently_verified' and isinstance(cur['evidence']['independent_verification'],str)
  assert set(ds)=={'/evidence/serialized_shared_gate','/evidence/independent_verification'},ds
  assert cur['evidence']['independent_verification']==str((R/'verified.json').relative_to(ROOT)).replace('\\','/')
  admin.append(dict(exact_before=m,current=pin(m['original']['path']),actual_jsonpointer_diffs=ds))
fake=[]
for n in claim['lean_files']+['AutoSamplingTheory/TechnicalLemmas/Measure.lean']:
 code=astis.strip_lean_comments_and_strings(path(n).read_text(encoding='utf8'));hits=[i for i,l in enumerate(code.splitlines(),1) if astis.FORBIDDEN_REGEX.search(l)];assert not hits;fake.append(dict(input=pin(n),findings=hits))
visual=load(R/'visual.inspection.json');assert len(visual['screenshots'])==4
for row in rows(visual):checks.append(dict(expected=row,actual=check(row)))
visual_observation=dict(actual_four_archived_PNGs_independently_viewed=True,root_capture_and_Node_resources_CLOSED=True,formula_and_folded_exact_Lean_visible=True,remaining_presentation_debts=['Actual assumption table horizontal scrollbar and rightmost text overflow in proof captures.','Long declaration name wraps heavily in graph detail card.','Some statement prose repeats; scientific boundary remains explicit.'],no_full_reader_or_physical_device_or_live_credit=True)
wd=load(R/'integration-whitespace58/diagnosis.json');b=gzip.decompress(path(wd['gzip']['path']).read_bytes());assert sha(b)==wd['full_negative_raw_sha256'] and len(b)==wd['full_negative_raw_bytes'] and wd['gzip_mtime']==0; assert len(wd['findings'])==398;wp=sorted({v['path'] for v in wd['findings']});assert len(wp)==5
write(D/'checks.json',dict(status='PASS_SCOPED_REPOSITORY_CONTROLS',science_commit=SCI,integration_commit=HEAD,reused_actual_native_verification=v,math_originals=72,math_checks=checks[:72],actual_additional_pin_checks=len(checks)-72,unchanged_science_packet=unchanged,all_required_gates=gates,gate_count=14,root_jobs=9162,test_jobs=9452,Registry=500,actual_new_Registry_declarations=claim['lean_declarations'][:2],actual_Test_not_Registry=claim['lean_declarations'][2],shared_imports_declaration_free=True,old_Measure_module_restored=True,preserved_import_negative=pin(R/'integration.0.route-diagnosis.json'),exact_admin_maps7=maps,actual_cell_admin_deltas=admin,fake_scan=fake,visual_observation=visual_observation,whitespace=dict(full_staged_negative=398,exact_immutable_paths=wp,lossless_gzip=pin(wd['gzip']['path']),authored_complement_only_PASS=True,full_staged_PASS=False),source_math_repair=False,remaining=notes['remaining']))
# Canonical graph freshness uses the actual complete native helper recipe, never a projection.
import publication_reader,astis_publication,astis_site
data=astis_publication.inputs();items=astis_publication.load();graph_payload={'lean':astis_site.source_digest(),'items':items,'cells':{b['cell']:data['cells'].get(b['cell']) for i in items for b in i['bindings']}}
dg=astis_publication.digest(graph_payload);assert publication_reader.graph_input_digest()==dg
graphpath=ROOT/'_site/data/underlying-lean-graph.json';graph=load(graphpath);assert graph['publication_inputs_sha256']==dg
targets={'decl:'+n for n in claim['lean_declarations']};nodes=[n for n in graph['nodes'] if n['id'] in targets];edges=[e for e in graph['edges'] if e['source'] in targets or e['target'] in targets];assert len(nodes)==3
write(D/'graph.bounded.json',dict(status='PASS_CURRENT_COMPLETE_INPUT_DIGEST',generated_graph=pin(graphpath),native_publication_inputs_sha256=dg,native_recipe='publication.digest({lean:astis_site.source_digest(),items:publication.load(),cells:all binding cells from actual publication.inputs()}); complete native object, no projected replacement.',canonical_item_count=len(items),canonical_bound_cell_count=len(graph_payload['cells']),helper_whole=pin(ROOT/'website/scripts/publication_reader.py'),source_digest_helper=pin(ROOT/'tools/astis_site.py'),publication_helper=pin(ROOT/'tools/astis_publication.py'),targets=nodes,incident_edges=edges,actual_incident_count=len(edges),truth_contract='Solid module/import ownership; dashed incomplete source-name references/correspondence. Scanner LogConcaveOn.prod reference does not certify exact theorem implication. Actual reviewed body/imports establish producer evidence; scanner is not exhaustive.',no_graph_rebuild=True))
for p in sorted(reads):
 f=pathlib.Path(p)
 if f.is_file():inputs[f.as_posix()]=pin(f)
write(D/'inputs.json',dict(status='PASS',actual_input_count=len(inputs),inputs=list(inputs.values()),index_recipe='Unique absolute qualified path per actual opened scoped input; no same-basename snapshot alias.',future59_60_guard=True,scope='Actual exported native verification helper inputs plus72 freeze originals, exact integration153 entries/gates/shared metadata/captures and complete canonical graph helper inputs; no old57 subtree re-review.'))
print(json.dumps(dict(status='PASS_REPOSITORY_REVIEW_WORKER',actual_PID=os.getpid(),science_commit=SCI,integration_commit=HEAD,integration_entries=153,native_checks=3840,math_originals=72,gates=14,inputs=len(inputs),graph_incident_edges=len(edges)),sort_keys=True))
