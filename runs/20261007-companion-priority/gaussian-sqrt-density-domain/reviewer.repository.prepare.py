from pathlib import Path
R=Path('runs/20261007-companion-priority/gaussian-sqrt-density-domain')
s=(R/'reviewer.exact.check.reconciled.py').read_text(encoding='utf-8')
s=s.replace("C='1de412105042ebcfe147d50a3d1022fb0514faad'", "C='fbafcea29c4e3d4a90e6401d20edc989c3df9d7a'\nP='1de412105042ebcfe147d50a3d1022fb0514faad'")
s=s.replace("allowed={'/evidence/execution_boundary','/evidence/proof_review','/evidence/source_review','/status'}", "allowed={'/evidence/execution_boundary','/evidence/proof_review','/evidence/source_review','/status','/evidence/independent_verification','/evidence/independent_verification_details','/evidence/integration_receipt','/graph_contribution/visual_review'}")
s=s.replace("assert set(changed)<=allowed,changed", "assert all(any(x==q or x.startswith(q+'/') for q in allowed) for x in changed),changed")
s=s.replace("current_cell['status']=='proved_locally'", "current_cell['status']=='independently_verified'")
before_git=r'''
def gitbytes(commit,p):return subprocess.check_output(['git','show',commit+':'+p])
integration=j(R/'integration.json')
assert integration['verified_proof_commit']==P
assert integration['cell_metadata_preceded_graph_generation'] is True
rootlogs=[]
for row in integration['checks']:
    assert row['exit_code']==0
    h=desc(row['log']);assert h['raw_sha256']==row['raw_sha256']
    paths.add(row['log']);rootlogs.append(h)
verified=j(R/'verified.json')
assert verified['verified_commit']==P and verified['verification_status']=='passed-scoped'
assert desc(R/'verified.json')['raw_sha256']=='d7a4744bd152b7b97ae3780bf48c5416859a4dfa1d35357a6dc73b4447cd8418'
shared=['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas.lean','Tests.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean']
changed=subprocess.check_output(['git','diff','--name-only',P,C,'--','*.lean'],text=True).splitlines()
assert set(changed)==set(shared),changed
import_adds={shared[0]:['import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOSqrtDensity'],shared[1]:['import AutoSamplingTheory.TechnicalLemmas.Measure.GaussianSqrtDensityDomain'],shared[2]:['import Tests.GaussianSqrtDensityDomain','import Tests.StandardizedRGOSqrtDensity']}
import difflib
shared_rows=[]
for p in shared:
    old=gitbytes(P,p).replace(b'\r\n',b'\n').decode();now=Path(p).read_bytes().replace(b'\r\n',b'\n').decode()
    changes=[x for x in difflib.ndiff(old.splitlines(),now.splitlines()) if x.startswith(('+ ','- '))]
    if p in import_adds:assert changes==['+ '+x for x in import_adds[p]],(p,changes)
    elif p.endswith('Tests/Basic.lean'):assert changes==['- example : formalizedTechnicalLemmaCount = 475 := by native_decide','+ example : formalizedTechnicalLemmaCount = 476 := by native_decide'],changes
    else:
        assert len(changes)==10 and all(x.startswith('+ ') for x in changes),changes
        assert any('localDecl := "'+plan['mathematical_declarations'][0]+'"' in x for x in changes)
        assert any('status := LemmaMemoryStatus.formalizedLocal' in x for x in changes)
    paths.add(p);shared_rows.append({'path':p,'old_git_raw_sha256':sha(gitbytes(P,p)),'current':desc(p),'normalized_changes':changes})
for cid in plan['active_cells']:
    p='research-wiki/frontier-cells/'+cid+'.json';old=json.loads(gitbytes(P,p));now=j(p)
    changed=diffs(old,now)
    allowed=['/status','/evidence/execution_boundary','/evidence/independent_verification','/evidence/independent_verification_details','/evidence/integration_receipt','/graph_contribution/visual_review']
    assert all(any(x==a or x.startswith(a+'/') for a in allowed) for x in changed),changed
    assert now['status']=='independently_verified'
    assert now['evidence']['independent_verification']==(R/'verified.json').as_posix()
    assert now['evidence']['integration_receipt']==(R/'integration.json').as_posix()
    for label,b in [('proof-before',gitbytes(P,p)),('shared-current',Path(p).read_bytes())]:
        dest=R/('reviewer.repository.'+cid+'.'+label+'.raw.snapshot.json');dest.write_bytes(b)
    checks.append({'name':'bounded_cell_independent_integration_admin','cell':cid,'fields':changed,'current':desc(p)})
for p in [x['path'] for x in math['frozen_production_files']]:
    assert gitbytes(P,p).replace(b'\r\n',b'\n')==gitbytes(C,p).replace(b'\r\n',b'\n'),p
for slug in plan['slugs']:
    for folder in ['publications','declaration_lessons']:
        p='website/content/'+folder+'/'+slug+'.json'
        assert gitbytes(P,p).replace(b'\r\n',b'\n')==gitbytes(C,p).replace(b'\r\n',b'\n'),p
        paths.add(p)
sys.path.insert(0,'website/scripts')
import publication_reader as reader
graphpath=Path('_site/data/underlying-lean-graph.json');graph=j(graphpath)
assert graph['publication_inputs_sha256']==reader.graph_input_digest()
ids={x['id'] for x in graph['nodes']}
assert all('decl:'+d in ids for d in plan['mathematical_declarations'])
assert all(e in graph['edges'] for edges in integration['structural_branches'].values() for e in edges)
snapshot=R/'reviewer.repository.underlying-lean-graph.raw.snapshot.json';snapshot.write_bytes(graphpath.read_bytes())
sitepath=Path('_site/data/site-data.json');site=j(sitepath);stamp=site['git']
assert stamp['commit']==P and stamp['dirty_files'] and stamp['commit_published'] is False
site_snap=R/'reviewer.repository.site-data.raw.snapshot.json';site_snap.write_bytes(sitepath.read_bytes())
checks.append({'name':'shared_root_Registry_actual_consumer','normalized_Lean_delta':shared_rows,'Registry_count':476,'four_new_imports_actual':True})
checks.append({'name':'independent_root_integration_evidence','receipt':desc(R/'integration.json'),'root_logs':rootlogs,'source_proof_parent':P,'root_prospective_tree_at_gate':True,'fresh_current_commit_gate_supersedes_prospective_stamp':True})
checks.append({'name':'current_official_graph_and_static_reader','graph':desc(graphpath),'snapshot':desc(snapshot),'publication_input_digest':graph['publication_inputs_sha256'],'node_count':len(graph['nodes']),'edge_count':len(graph['edges']),'two_target_nodes_and_actual_import_edges':True,'site_snapshot':desc(site_snap),'generated_site_git_commit':stamp['commit'],'generated_site_dirty_file_count':len(stamp['dirty_files']),'commit_published':False,'site_scope':'Root static site build/check reused with exact log hashes and current graph freshness. Precommit proof-parent plus dirty prospective tree, not a clean shared-head/public/live stamp. Untracked future33 paths in stamp are observability only, excluded from packet32 proof. No rendered or Copy/Download interaction QA.'})
paths.update(p for p in subprocess.check_output(['git','ls-tree','-r','--name-only',C,'--',R.as_posix()],text=True).splitlines())
paths.add((R/'integration.json').as_posix());paths.add((R/'verified.json').as_posix())
'''
s=s.replace("tracked=set(subprocess.check_output",before_git+"\ntracked=set(subprocess.check_output")
start=s.index("assert 'formalizedTechnicalLemmaCount = 475'")
s=s[:start]+s[s.index("pub.check_advance(",start):]
s=s.replace("gates=j(R/'reviewer.exact.gates.json')", "gates=j(R/'reviewer.repository.gates.json');assert gates['checked_commit']==C")
s=s.replace("assert advance.current_advances()[A]['state']=='PROVED_LOCAL'", "assert advance.current_advances()[A]['state']=='VERIFIED'\nfor row in gates['results']:assert desc(row['path'])['raw_sha256']==row['raw_sha256']\naggregate=(R/'reviewer.repository.aggregate.log').read_text(encoding='utf-8');assert 'ASTIS check passed' in aggregate and '9137 jobs' in aggregate and '9404 jobs' in aggregate")
s=s.replace("'artifact_kind':'independent-exact-commit-checks'", "'artifact_kind':'independent-repository-ProofSeal-checks'")
s=s.replace("'read_lease':'OPEN until final sole transition'", "'read_lease':'OPEN until repository receipt and CLOSED lease; no state transition'")
s=s.replace("dest=R/'reviewer.exact.checks.json'", "dest=R/'reviewer.repository.checks.json'")
(R/'reviewer.repository.check.py').write_bytes(s.encode())
