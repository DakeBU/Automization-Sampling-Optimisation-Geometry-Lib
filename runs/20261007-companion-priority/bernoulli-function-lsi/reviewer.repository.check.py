from pathlib import Path
import json,hashlib,subprocess,sys,re,datetime
sys.path.insert(0,'tools')
import astis_publication as pub,astis_advance as advance,astis,publication_reader
R=Path('runs/20261007-companion-priority/bernoulli-function-lsi');R35=Path('runs/20261007-companion-priority/balanced-rademacher-clt')
C='d0b872541758537a4f42d9d3e6e8deb12b5bb028';P='4d9e71a6b835b54453a5cfd2d132f9a51f66f69c';V='picard_commit_verifier_20261005'
def j(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def h(b):return hashlib.sha256(b).hexdigest()
def d(p):
 b=Path(p).read_bytes();return {'path':Path(p).as_posix(),'raw_sha256':h(b),'lf_sha256':h(b.replace(b'\r\n',b'\n')),'bytes':len(b)}
def put(p,o):
 assert not p.exists();p.write_bytes((json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode());return d(p)
def old(p):return subprocess.check_output(['git','show',P+':'+p])
def diff(a,b,p=''):
 if type(a)!=type(b):return[p]
 if isinstance(a,dict):return[q for k in sorted(a.keys()|b.keys()) for q in ([p+'/'+k] if k not in a or k not in b else diff(a[k],b[k],p+'/'+k))]
 if isinstance(a,list):return[p] if len(a)!=len(b) else[q for i,(x,y) in enumerate(zip(a,b)) for q in diff(x,y,p+'/'+str(i))]
 return[] if a==b else[p]
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C
assert subprocess.check_output(['git','rev-parse','HEAD^'],text=True).strip()==P
assert subprocess.check_output(['git','-C','.lake/packages/mathlib','rev-parse','HEAD'],text=True).strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
assert Path('lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0'
g=j(R/'reviewer.repository.gates.json');assert g['checked_commit']==C and len(g['results'])==6 and g['compiler']=='CLOSED'
for row in g['results']:assert row['returncode']==0 and d(row['path'])['raw_sha256']==row['raw_sha256']
assert re.findall(r'Build completed successfully \((\d+) jobs\)',(R/'reviewer.repository.aggregate.log').read_text(encoding='utf-8'))==['9141','9411']
proof=j(R35/'reviewer.exact.bindings.json');assert d(R35/'reviewer.exact.bindings.json')['raw_sha256']=='965db59cb8d18fb6adfa784222ecc2c1b101124a1deff89afa684a97099364b5'
admin=[];unchanged=0
for row in proof['exact_currentGit_inputs']:
 p=Path(row['path']);current=d(p)
 if current['raw_sha256']==row['raw_sha256']:unchanged+=1;continue
 assert p.parent==Path('research-wiki/frontier-cells')
 previous=json.loads(old(p.as_posix()));now=j(p);delta=diff(previous,now)
 common={'/evidence/execution_boundary','/evidence/independent_verification','/evidence/independent_verification_details','/evidence/integration_receipt','/graph_contribution/visual_review','/status'}
 allowed=common|({'/purification/dead_code_audit'} if 'balanced-rademacher' in p.name else {'/conceptual_mirror_audit/reason'})
 assert set(delta)==allowed and previous['status']=='proved_locally' and now['status']=='independently_verified'
 assert isinstance(now['evidence']['independent_verification'],str) and j(now['evidence']['independent_verification'])['verification_status']=='passed-scoped'
 assert now['evidence']['integration_receipt']==(R/'integration.json').as_posix()
 i=len(admin);before=R/f'reviewer.repository.cell.{i}.before.GitLF.snapshot.json';after=R/f'reviewer.repository.cell.{i}.current.raw.snapshot.json'
 assert not before.exists() and not after.exists();before.write_bytes(old(p.as_posix()));after.write_bytes(p.read_bytes())
 admin.append({'cell':now['cell_id'],'before_GitLF':d(before),'current_raw':d(after),'current_file':current,'exact_pointers':delta,'statement_source_and_binding_unchanged':True})
assert unchanged==838 and len(admin)==3
for run in [R,R35]:
 receipt=j(run/'verified.json');assert receipt['verification_status']=='passed-scoped'
 pub.check_advance(receipt['lean_declarations'],reviewed=True)
 assert advance.current_advances()[receipt['advance_id']]['state']=='VERIFIED'
 assert advance.current_advances()[receipt['advance_id']]['latest_evidence']['verifier_id']==V
for row in proof['current3_source_bindings']:
 assert d(row['source_receipt']['path'])['raw_sha256']==row['source_receipt']['raw_sha256']
 assert d(row['packet']['path'])['raw_sha256']==row['packet']['raw_sha256']
 data=pub.inputs();item=next(i for i in pub.load() if any(b['declaration']==row['declaration'] for b in i['bindings']));b=next(x for x in item['bindings'] if x['declaration']==row['declaration'])
 assert pub.binding_digest(item,b,data)==row['binding_sha256'] and data['audits'][row['audit_id']]['source_review']['review_run_sha256']==row['review_run_sha256']
roots=['AutoSamplingTheory/TechnicalLemmas.lean','Tests.lean','Tests/Basic.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean']
added_imports=[]
for p in roots[:2]:
 oldlines=old(p).decode().splitlines();newlines=Path(p).read_text(encoding='utf-8').splitlines();assert all(x in newlines for x in oldlines)
 added_imports+=list(x for x in newlines if x not in oldlines)
assert set(added_imports)=={'import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.TwoPointEntropy','import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.BernoulliLogSobolev','import AutoSamplingTheory.TechnicalLemmas.Probability.BalancedRademacherCLT','import Tests.BernoulliLogSobolev','import Tests.BalancedRademacherCLT'}
assert old(roots[2]).replace(b' = 476 :=',b' = 479 :=').replace(b'\r\n',b'\n')==Path(roots[2]).read_bytes().replace(b'\r\n',b'\n')
registry=Path(roots[3]).read_text(encoding='utf-8');oldreg=old(roots[3]).decode()
assert registry.count('status := LemmaMemoryStatus.formalizedLocal')==oldreg.count('status := LemmaMemoryStatus.formalizedLocal')+3
for row in proof['current3_source_bindings']:assert f'localDecl := "{row["declaration"]}"' in registry
integrations=[]
for run in [R,R35]:
 r=j(run/'integration.json');assert r['aggregate_summary']=={'root_build_jobs':9141,'tests_build_jobs':9411}
 for check in r['checks']:assert check['exit_code']==0 and d(check['log'])['raw_sha256']==check['raw_sha256']
 integrations.append(d(run/'integration.json'))
for name in ['aggregate','publication','semantic','frontier-integrated','process-memory-integrated','contributor-integrated','site-build','official-graph-refresh']:
 assert j(R/(name+'.status.json'))['exit_code']==0
graph=j('_site/data/underlying-lean-graph.json');site=j('_site/data/site-data.json');graphchecks=[]
assert graph['publication_inputs_sha256']==publication_reader.graph_input_digest()
for i in range(3):
 retained=j(R/f'graph.{i}.json');assert pub.graph_report(retained['cell'],Path('_site'))==retained
 graphchecks.append(d(R/f'graph.{i}.json'))
bridge_id='transport:bernoulli-gaussian-entropy-energy-limit';family_id='family:entropy-coordinate-energy'
fh='website/content/functor_hypergraph.json';gm='website/content/graph_memory_index.json'
f=j(fh);f0=json.loads(old(fh));memory=j(gm);m0=json.loads(old(gm))
assert {k:v for k,v in memory.items() if k!='families'}=={k:v for k,v in m0.items() if k!='families'}
assert [x for x in memory['families'] if x['id']!=family_id]==m0['families']
assert [x for x in f['hyperedges'] if x['id']!=bridge_id]==f0['hyperedges']
assert [x for x in f['objects'] if x['id'] not in {'concept:finite-boolean-product','concept:real-gaussian-function-entropy'}]==f0['objects']
for k,v in f0['sources'].items():assert f['sources'][k]==v
assert {k:v for k,v in f.items() if k not in {'hyperedges','objects','sources'}}=={k:v for k,v in f0.items() if k not in {'hyperedges','objects','sources'}}
bridge=next(x for x in f['hyperedges'] if x['id']==bridge_id);assert bridge['formal_refs']==[] and bridge['status']=='not-Lean-certified' and 'compiled_transport' not in bridge
assert next(x for x in graph['hyperedges'] if x['id']==bridge_id)==bridge
assert advance.current_discoveries()[bridge['review']['discovery_id']]['status']=='validated'
assert d(bridge['review']['evidence'][0])['raw_sha256']==bridge['review']['review_raw_sha256']
for p in bridge['review']['evidence']:assert Path(p).exists()
family=next(x for x in memory['families'] if x['id']==family_id);assert family['compiled_substrate_bindings']==[] and len(family['formal_search_nodes'])==2
slt='research-wiki/cited-results/SLT_reuse_audit.md';oldtext=[x for x in old(slt).decode().splitlines() if x.strip()];newtext=[x for x in Path(slt).read_text(encoding='utf-8').splitlines() if x.strip()]
assert newtext[:len(oldtext)]==oldtext and len(newtext)==len(oldtext)+2
assert '26 private reachable helpers' in newtext[-1] and 'ASTIS-authored RMS induction' in newtext[-1] and 'No SLT Lake dependency' in newtext[-1]
assert not astis.forbidden_pattern_hits();files=astis.lean_source_files()
assert [k for k,v in advance.current_advances().items() if v['state']=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
changed=subprocess.check_output(['git','diff','--name-only',P,C],text=True).splitlines();assert len(changed)==62
proc=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE);out,_=proc.communicate(('\n'.join(C+':'+p for p in changed)+'\n').encode());assert proc.returncode==0
offset=0;gitrows=[]
for p in changed:
 end=out.index(b'\n',offset);n=int(out[offset:end].split()[-1]);offset=end+1;blob=out[offset:offset+n];offset+=n+1;live=Path(p).read_bytes();raw=p.startswith('runs/')
 assert (blob==live if raw else blob.replace(b'\r\n',b'\n')==live.replace(b'\r\n',b'\n')),p
 gitrows.append({**d(p),'git_blob_sha256':h(blob),'mode':'raw-exact' if raw else 'LF-exact'})
evidence=put(R/'reviewer.repository.bindings.json',{'checked_commit':C,'parent_proof_commit':P,'prior_independent_exact_bindings':d(R35/'reviewer.exact.bindings.json'),'prior841_inputs_unchanged':838,'allowed3cell_admin_changes':admin,'shared_imports':added_imports,'registry_count':479,'TestsBasic_actual_count':479,'integration_receipts':integrations,'affected_graph_checks':graphchecks,'graph_publication_inputs_sha256':graph['publication_inputs_sha256'],'graph_counts':graph['counts'],'conceptual_mirror':bridge,'all_old_graph_entries_preserved':True,'SLT_old_nonempty_lines_unchanged':len(oldtext),'SLT_added_nonempty_lines':2,'changed62_Git_inputs':gitrows,'generated_site_inputs':[d('_site/data/underlying-lean-graph.json'),d('_site/data/site-data.json')],'generated_site_git_stamp':{'commit':site['git']['commit'],'dirty_files_count':len(site['git']['dirty_files']),'commit_published':site['git']['commit_published']},'generated_site_historical_gate_stamp':site['gate'],'reader_delivery_boundary':j(R/'integration.json')['reader_inspection'],'full_fake_closure_scan':{'canonical_files':len(files),'hits':[]},'named_axioms_reused_unchanged_from_exact_proofs':['propext','Classical.choice','Quot.sound']})
receipt=put(R/'reviewer.repository.ProofSeal.json',{'schema_version':1,'status':'accepted-scoped','verification_status':'passed-scoped','checked_commit':C,'verifier_id':V,'seal_kind':'joint34+35 repository ProofSeal','mathematical_verified_commits':{'34':j(R/'verified.json')['verified_commit'],'35':P},'previous_local_verification':[d(R/'verified.json'),d(R35/'verified.json')],'fresh_repository_gates':g,'raw_LF_Git_shared_and_source_evidence':evidence,'scope':'Three actual canonical declarations, complete unchanged mathematical modules/Test/lessons/signatures and three current accepted source/decoder bindings, genuine root/Test integration and Registry479, fresh all-workspace Lean/source/fake admission. Not new mathematical credit or another VERIFIED/STABILIZING transition.','remaining_boundary':['Actual signed finite Bernoulli functionLSI plus actual count weakCLT only.','Gaussian entropy/derivative/fullflip4 limits, compact GaussianLSI, actual noncompact/hilbert domain extension, T2/FIRST4.6/bias/fullLemma/main/work/composition remain open.','ExpositionSeal, folded complete Test source/CopyDownload/interaction/renderedQA, postmerge purification, exact-head remoteCI/mainmerge/live delivery remain separate.','Generated site stamp honestly records precommit4d9+dirty and an older historical gate stamp; current repository acceptance is established by this exactd0b fresh gate and matching canonical bytes, without relabelling the generated stamp.','Future36 source-only preproof artifacts excluded; no claim or production result accepted here.'],'canonical_mutations':False,'leases':{'read':'CLOSED','write':'CLOSED','compiler':'CLOSED','Python':'CLOSED'},'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
(R/'reviewer.repository.lease.json').write_bytes((json.dumps({'status':'CLOSED','checked_commit':C,'verifier_id':V,'read':'CLOSED','write':'CLOSED','compiler':'CLOSED','Python':'CLOSED','receipt':receipt},indent=2)+'\n').encode())
print(json.dumps({'status':'accepted-scoped','checked_commit':C,'receipt':receipt,'all_leases':'CLOSED'}))
