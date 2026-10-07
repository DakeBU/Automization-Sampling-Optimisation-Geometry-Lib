from pathlib import Path
import json,hashlib,re,subprocess
run=Path('runs/20261007-companion-priority/standardized-rgo-relative-entropy')
assert not (run/'integration.json').exists()
read=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))
v=read(run/'verified.json');assert v['verification_status']=='passed-scoped'
plan=read(run/'publication-plan.json')
markers={'aggregate':'ASTIS check passed','publication':'Publication PASS','semantic':'registry valid','frontier-integrated':'protocol check passed','process-memory-integrated':'ASTIS process-memory check passed','contributor-integrated':'ASTIS contributor contract PASS','site-build':'compiled local leaves','site-check':'ASTIS site check passed'}
logs={k:run/(k+'.log') for k in markers}
for k,p in logs.items():assert markers[k] in p.read_text(encoding='utf-8-sig'),k
graphs=[read(run/f'graph.{i}.json') for i in range(1)]
for cid,g in zip(plan['active_cells'],graphs):assert g['status']=='graph coverage checked' and g['cell']==cid
g=read('_site/data/underlying-lean-graph.json');branches={}
for name in plan['mathematical_declarations']:
    mid='module:'+name.rsplit('.',1)[0]
    branches[name]=[e for e in g['edges'] if mid in (e.get('source'),e.get('target')) and e.get('relation') in ['imports','declares']]
    assert branches[name],name
html=Path('_site/example-cases/samplewiki/companions/smoothed-picard-hmc.html').read_text(encoding='utf-8')
for token in ['standardized_rgo_unique_prox_and_finite_entropy','inline-lean-statement','StandardizedRGORelativeEntropy','quadratic_eta_two_entropy','zero_dimension_entropy']:assert token in html,token
jobs=re.findall(r'Build completed successfully \((\d+) jobs\)',logs['aggregate'].read_text(encoding='utf-8-sig'));assert len(jobs)==2
assert int(jobs[0])>9137 and int(jobs[1])>9404,jobs
match=lambda k,p:re.search(p,logs[k].read_text(encoding='utf-8-sig'))
pu=match('publication',r'Publication PASS: (\d+)');se=match('semantic',r'(\d+) audits, (\d+) repair proposals');fc=match('frontier-integrated',r'(\d+) registered cells');co=match('contributor-integrated',r'affected declarations=(\d+); changed cells=(\d+)');assert all([pu,se,fc,co])
rec=dict(schema_version=1,status='aggregate-static-reader-graph-accepted-independent-repository-exposition-seals-pending',verified_proof_commit=v['verified_commit'],checked_working_head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),integration_owner='companion_root_20261005',stabilization_lane='Original PhaseKernel sole STABILIZING / same PR313',toolchain='leanprover/lean4:v4.33.0',mathlib_commit='db584cd6d46c92f209a44c0f1c829460d327499d',checks=[dict(name=k,exit_code=0,log=p.as_posix(),raw_sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for k,p in logs.items()],aggregate_summary=dict(root_build_jobs=int(jobs[0]),tests_build_jobs=int(jobs[1])),metadata_checks=dict(publication=int(pu[1]),semantic_audits=int(se[1]),repair_proposals=int(se[2]),frontier_cells=int(fc[1]),contributor_declarations=int(co[1]),contributor_cells=int(co[2])),graph_checks=graphs,structural_branches=branches,small_graph_delta='One actual canonical finite-entropy and unique-proximal-witness source consumer of five real compiled ASTIS parents, with exact compiled import and declaration edges. Existing source topology, dashed conceptual families and unresolved LSI/T2/gap/bias nodes remain. No new conceptual mirror found.',shared_imports=['ExampleCases.SmoothedPicardHMC.StandardizedRGORelativeEntropy','Tests.StandardizedRGORelativeEntropy','Existing generic Registry leaf count476 unchanged and Tests.Basic count exercised'],reader_inspection=dict(path='_site/example-cases/samplewiki/companions/smoothed-picard-hmc.html',formula_proof_and_folded_actual_Lean_present=True,rendered_visual_qa='Open; static structure only. Copy/Download implementation and interaction acceptance remain open.'),independent_admission=(run/'verified.json').as_posix(),truth_boundary=read(run/'claim.json')['truth_boundary'],publication_base='origin/main exact84f0a9fc; no --ci',purification='Pending independent ExpositionSeal and postmerge purification',remote_ci='Current33 requires its own published-head CI. Prior32 1e0818f1 allfour successes cannot validate current33. DraftPR313 unmerged/no live claim.',cell_metadata_preceded_graph_generation=True)
(run/'integration.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Fresh actual33 aggregate/static reader/formal branches recorded; independent repository/exposition seals next.')
