from pathlib import Path
import hashlib,json,os,subprocess
r=Path('runs/20261007-companion-priority/pbps-actual-projected-rotation70');load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.resolve().as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
notes=load(r/'integration.notes.json');assert notes['status']=='SERIALIZED_SHARED_AGGREGATE70_AND_CURRENT_GRAPH_PASS_NOT_MAIN_NOT_PURIFIED'
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert head==notes['proof_commit']
plan=load(r/'publication-plan.json')
paths=[Path(p) for p in ['lean-toolchain','lake-manifest.json','AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl','runs/substantive_advances.jsonl','docs/module-graph.svg','docs/assets/astis_lean_arsenal_module_graph.svg','research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json','research-wiki/sampling-sde-library/lean-leaf-module-graph.md','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation.md','AutoSamplingTheory/ExampleCases/ProximalBPS/ActualProjectedRotation.lean','website/scripts/inline_lean.py','website/scripts/check_cross_domain_browser.py','_site/data/underlying-lean-graph.json','_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html']]
for slug,aid,cid in zip(plan['slugs'],plan['audit_ids'],plan['active_cells']):
 paths.extend([Path('website/content/publications')/(slug+'.json'),Path('website/content/declaration_lessons')/(slug+'.json'),Path('research-wiki/semantic-roundtrip/audits')/(aid+'.json'),Path('research-wiki/frontier-cells')/(cid+'.json')])
paths.extend(r/p for p in ['claim.json','publication-plan.json','integration.notes.json','visual.inspection.json','integration70/final-admin.json','root.source70.adoption.json','root.exact-verification70.adoption.json','verified.json'])
for check in notes['checks']:
 paths.extend(r/'integration70'/check['label']/p for p in ['receipt.json','stdout.log','stderr.log'])
paths.extend(p for p in (r/'integration70/visual70').iterdir() if p.is_file())
paths.extend(r/p for p in ['independent-math70/lease.final.json','independent-source70/lease.final.json','exact-science-verification70/lease.final.json','exact-science-verification70-label-supplement/lease.final.json','anonymous-decoder/lease.json','independent-reader-helper-code70/lease.final.json'])
paths=list(dict.fromkeys(paths));assert all(p.is_file() for p in paths)
paths.append(Path('conversion-windows/ASTIS-SW-PBPS-2026.md'))
dest=r/'final-reader-repository-packet70.json';assert not dest.exists()
packet=dict(status='FROZEN_FINAL70_FOR_INDEPENDENT_REPOSITORY_AND_SCOPED_READER',actual_root_PID=os.getpid(),checked_science_commit=head,original_math_commit='e44b6b1e08c8a259a1f48006d822b53efd3fecb8',inputs=[pin(p) for p in paths],RAW_authority=True,LF_rule='CRLF to LF only',expected=dict(registry_count=518,root_jobs=notes['root_jobs'],test_jobs=notes['test_jobs'],publication_units=239,statements=1,formula_BODY_steps=8,actual_captures=10,copy_callbacks=3,RAW_downloads=3),native_math_source_decoder_reviews_reused=True,current_helper_code_independently_reviewed=True,fresh_full_python_and_real_browser=True,independent_aggregate_reader_verdict_pending=True,full_Exposition_Seal=False,PURIFIED=False,main_live=False,wholepaper_or_Goal_complete=False)
dest.write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('PASS final70 packet',len(paths),'inputs',sha(dest.read_bytes()))
