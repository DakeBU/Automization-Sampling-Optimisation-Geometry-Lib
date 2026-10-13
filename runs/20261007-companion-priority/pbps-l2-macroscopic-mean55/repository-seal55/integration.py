from common import *
sys.path[:0]=[str(R),str(R/'tools'),str(R/'website/scripts')]
from tools import astis,astis_advance as advance
import astis_site as site,astis_publication as publication,publication_reader as reader
notes=load(B/'integration.notes.json');assert notes['registry_count']==496 and notes['proof_commit']==notes['verified_commit']==SCI
gates=[]
for name in ['tests','mandatory','pycompile','whitespace','publication','semantic','frontier','contributor','site-build','official-graph','graph','site-check']:
 st=load(B/('integration.0.'+name+'.status.json'));lp=pin(B/('integration.0.'+name+'.log'));assert st['exit_code']==0 and st['proof_commit']==SCI and st['log_raw_sha256']==lp['raw_sha256'];gates.append(dict(name=name,status=pin(B/('integration.0.'+name+'.status.json')),log=lp,native=st))
for e in notes['checks']+notes['shared_files']:assert equal(e)
tl=path(B/'integration.0.tests.log').read_text();ml=path(B/'integration.0.mandatory.log').read_text();assert 'Build completed successfully (9445 jobs).' in tl and 'Build completed successfully (9158 jobs).' in ml and 'ASTIS check passed' in ml and 'sorryAx' not in tl and 'sorryAx' not in ml
expected={TARGET,'Tests.ProximalBPSL2MacroscopicMean.actual_rough_difference_variance','Tests.ProximalBPSL2MacroscopicMean.rank_zero_actual_source_constant'}
axioms=[(n,a) for n,a in re.findall(r"'([^']+)' depends on axioms: \[([^\]]+)\]",tl) if n in expected];assert len(axioms)==3 and {n for n,a in axioms}==expected and all(set(re.findall(r'[A-Za-z_.]+',a))=={'propext','Classical.choice','Quot.sound'} for n,a in axioms)
aggregator=path('AutoSamplingTheory/ExampleCases.lean').read_text();stripped=astis.strip_lean_comments_and_strings(aggregator);assert all(not l.strip() or l.startswith('import ') for l in stripped.splitlines());assert 'import AutoSamplingTheory.ExampleCases.ProximalBPS.L2MacroscopicMean' in aggregator and 'import AutoSamplingTheory.ExampleCases' in path('AutoSamplingTheory.lean').read_text()
assert 'import Tests.ProximalBPSL2MacroscopicMean' in path('Tests.lean').read_text();assert 'formalizedTechnicalLemmaCount = 496' in path('Tests/Basic.lean').read_text()
entries=site.parse_registry();formalized=[e for e in entries if e.status=='formalizedLocal'];assert len(formalized)==496 and len([e for e in formalized if e.local_decl==TARGET])==1
state=advance.current_advances();assert state[ADV]['state']=='VERIFIED' and state[ADV]['latest_evidence']['verifier_id']==ACTOR and state[ADV]['latest_evidence']['verified_commit']==SCI
lanes=[k for k,v in state.items() if v['state']=='STABILIZING'];assert lanes==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'] and load(CELL)['status']=='independently_verified'
pubitem=next(i for i in publication.load() if any(b['declaration']==TARGET for b in i['bindings']));binding=next(b for b in pubitem['bindings'] if b['declaration']==TARGET)
payload=publication.binding_payload(pubitem,binding);assert logical(payload)=='3429f3b54edb1b9e40456d5f25677a1a54b4984f8d62aae273ce650e3b6ce862';publication.check_advance([TARGET],reviewed=True)
scan=[]
for row in load(B/'whole-math55/checks.json')['fake_closure_scan']:
 p=row['input']['path'];clean=astis.strip_lean_comments_and_strings(path(p).read_text());hits=[n for n,l in enumerate(clean.splitlines(),1) if astis.FORBIDDEN_REGEX.search(l)];assert not hits;scan.append(dict(input=pin(p),hits=hits))
# Full native digest recipe, never a projection. Record actual canonical opened inputs while computing it.
opened=set();collect=[True]
def audit(event,args):
 if collect[0] and event=='open' and args and isinstance(args[0],(str,bytes,os.PathLike)):
  p=path(args[0])
  if p.is_relative_to(R) and p.is_file() and not p.is_relative_to(O):opened.add(str(p))
sys.addaudithook(audit)
publication.inputs.cache_clear();publication.load.cache_clear();digest=reader.graph_input_digest();data=publication.inputs();sourcedigest=site.source_digest();digest_payload=dict(lean=sourcedigest,items=publication.load(),cells={b['cell']:data['cells'].get(b['cell']) for i in publication.load() for b in i['bindings']});assert logical(digest_payload)==digest
collect[0]=False
canonical=[pin(p) for p in sorted(opened) if not '/.lake/' in p.replace('\\','/')];dump('graph-digest.canonical-inputs.json',dict(status='PASS',actual_opened_canonical_inputs=canonical,count=len(canonical),full_native_digest_payload_sha256=digest,Lean_source_digest=sourcedigest,native_recipe='publication.digest({lean: astis_site.source_digest(), items: publication.load(), cells: exact binding cell lookup from publication.inputs()}); full canonical payload, not sliced/projected'))
helper=path('website/scripts/publication_reader.py').read_bytes().splitlines(keepends=True);selected=b''.join(helper[182:187]);(O/'graph.helper183-187.raw.snapshot.py.txt').write_bytes(selected)
graph=load('_site/data/underlying-lean-graph.json');assert graph['publication_inputs_sha256']==digest
nodeid='decl:'+TARGET;nodes=[n for n in graph['nodes'] if n['id']==nodeid];edges=[e for e in graph['edges'] if e.get('source')==nodeid or e.get('target')==nodeid];assert len(nodes)==1 and len(edges)==7
report=load(B/'integration.0.graph.log');assert report['contributions'][0]['node']==nodeid and len(report['contributions'][0]['connections'])==7 and report['contributions'][0]['omitted_connections']==0
dump('graph.bound-slice.json',dict(status='PASS',graph_raw=pin('_site/data/underlying-lean-graph.json'),native_publication_inputs_sha256=digest,native_source_digest=sourcedigest,scalar_header={k:v for k,v in graph.items() if not isinstance(v,(list,dict))},target=nodes[0],seven_incident_edges=edges,recorded_graph_check=report,helper_whole=pin('website/scripts/publication_reader.py'),helper_selected183_187=pin(O/'graph.helper183-187.raw.snapshot.py.txt'),canonical_inputs=pin(O/'graph-digest.canonical-inputs.json'),semantics='Solid module/import ownership is not theorem implication. Dashed name references are incomplete. Actual five parent proof dependencies are established by unchanged compiled body/full-math review; incidental LogConcaveOn.prod scanner is no proof parent.'))
# Immutable negative diagnoses and authored complement, exact paths only.
debts=[]
for folder,num,pathsnum in [('whitespace-diagnosis55',1014,594),('integration-whitespace55',165,3)]:
 d=load(B/folder/'diagnosis.json');g=path(d['gzip']['path']).read_bytes();raw=gzip.decompress(g);assert sha(raw)==d['full_negative_raw_sha256'] and len(d['immutable_raw_artifacts'])==pathsnum and int.from_bytes(g[4:8],'little')==0
 assert (len(d['findings']) if isinstance(d['findings'],list) else d['findings'])==num and d['full_staged_exit']==2
 if 'lf_sha256' in d['gzip']:assert equal(d['gzip'])
 else:assert sha(g)==d['gzip']['raw_sha256']
 excluded={e['path'] for e in d['immutable_raw_artifacts']};emitted={m.group(1) for m in re.finditer(r'^(.+?):\d+: (?:trailing whitespace|new blank line at EOF)\.?$',raw.decode(),re.M)};assert excluded==emitted
 debts.append(dict(diagnosis=pin(B/folder/'diagnosis.json'),negative=pin(d['gzip']['path']),findings=num,exact_immutable_paths=pathsnum,full_staged_PASS=False))
wd=load(B/'integration-whitespace55/diagnosis.json');excluded={e['path'] for e in wd['immutable_raw_artifacts']};names=[e['path'] for e in load(O/'native-inputs.json')['integration_owned_git_entries'] if e['path'] not in excluded];batches=[]
with (O/'integration.authored-whitespace.log').open('wb') as out:
 for i in range(0,len(names),64):
  cmd=['git','-c','core.whitespace=cr-at-eol','diff','--check',SCI,HEAD,'--']+names[i:i+64];r=subprocess.run(cmd,cwd=R,capture_output=True);out.write(r.stdout+r.stderr);assert r.returncode==0;batches.append(dict(start=i,count=len(names[i:i+64]),exit_code=0))
wr=load(B/'windows-default-whitespace55/receipt.json');raw=gzip.decompress(path(B/'windows-default-whitespace55/default-negative.log.gz').read_bytes());assert sha(raw)==wr['negative_raw_sha256'] and len(raw)==wr['negative_raw_bytes'] and wr['default_exit']==2 and wr['configured_exit']==0
cell_before=load(B/'verified-inputs-before-shared-integration/0.raw.snapshot');cell_now=load(CELL);deltas=[]
def difference(a,b,p=''):
 if isinstance(a,dict) and isinstance(b,dict):
  for k in sorted(set(a)|set(b)):
   if k not in a or k not in b:deltas.append(dict(path=p+'/'+k,before=a.get(k),after=b.get(k)))
   else:difference(a[k],b[k],p+'/'+k)
 elif a!=b:deltas.append(dict(path=p,before=a,after=b))
difference(cell_before,cell_now);assert all(e['path'] in ['/blocked/reason','/evidence/serialized_shared_gate','/evidence/execution_boundary','/purification/dead_code_audit','/purification/scope'] for e in deltas),deltas
assert cell_now['evidence']['serialized_shared_gate']['proof_commit']==SCI and cell_now['evidence']['serialized_shared_gate']['status']=='PASS' and cell_now['evidence']['serialized_shared_gate']['root_jobs']==9158 and cell_now['evidence']['serialized_shared_gate']['test_jobs']==9445 and cell_now['evidence']['serialized_shared_gate']['registry_count']==496
dump('integration.0.metadata-negative.diagnosis.json',dict(status='PRESERVED_OWN_STRICT_ALLOWLIST_NEGATIVE_RESOLVED_AFTER_REVIEW',initial_exit_code=1,initial_error='Own three-field allowlist omitted two actual administrative fields: blocked/reason and evidence/serialized_shared_gate. All underlying gates had passed before assertion.',initial_script=pin(O/'integration.0.metadata-negative.raw.snapshot.py'),actual_five_metadata_deltas=deltas,accepted_reason='blocked/reason names the proved scoped all-L2 edge and explicitly leaves gradient/H1/Gamma/main/cost pending; serialized_shared_gate is actual9158/9445/496 PASS with science commit. No source statement/proof/publication/learning contract or independent verifier evidence changed.',compiler_started=False,canonical_mutation=False))
dump('integration.checks.json',dict(status='PASS',science=SCI,integration=HEAD,actual12_terminal_gates=gates,root9158_Test9445_Registry496=True,actual_three_source_consumers_standard3=axioms,registry496_entry=[e.__dict__ for e in formalized if e.local_decl==TARGET],declaration_free_public_ExampleCases_and_root_Test_imports=True,current_VERIFIED_only_independent55=True,sole_STABILIZING=lanes,reviewed_publication_gate='ACTUALLY PASS',publication_binding_sha256=logical(payload),fake_closure_scan=scan,graph_digest=pin(O/'graph.bound-slice.json'),graph_canonical_inputs=pin(O/'graph-digest.canonical-inputs.json'),cell_shared_administrative_exact_deltas=deltas,preserved_whitespace_debts=debts,authored_complement=dict(paths=len(names),batches64=batches,log=pin(O/'integration.authored-whitespace.log'),exit_code=0),Windows_default_CRLF_negative_preserved=pin(B/'windows-default-whitespace55/receipt.json'),no_compiler_started=True,no_canonical_mutation=True,metadata_observability_debt='Historical pending-shared-integrations text in immutable exact verified artifact/handoff records their chronological stage; actual twelve PASS current integration receipts establish current scoped aggregate. Future next-edge prose grants no theorem credit.'))
print(json.dumps(dict(status='PASS',twelve_actual_gates=12,registry=496,root_jobs=9158,Tests_jobs=9445,graph_digest=digest,graph_canonical_inputs=len(canonical),incident_edges=len(edges),cell_delta_count=len(deltas),authored_paths=len(names),compiler_started=False)))
