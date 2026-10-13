from pathlib import Path
import hashlib,json,os,subprocess
r=Path('runs/20261007-companion-priority/pbps-actual-hazard-clock75');load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.resolve().as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
n=load(r/'integration.notes.json');head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert head==n['proof_commit']==load(r/'root.exact-verification75.adoption.json')['verified_commit']
assert n['status']=='SERIALIZED_SHARED_AGGREGATE75_AND_CURRENT_GRAPH_PASS_NOT_MAIN_NOT_PURIFIED'
paths=[Path(p) for p in load(r/'integration75/before-generator-state.json')['keep'] if Path(p).is_file()]
paths.extend(Path(p) for p in ['lean-toolchain','lake-manifest.json','AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean','website/content/publications/pbps-actual-hazard-clock.json','website/content/declaration_lessons/pbps-actual-hazard-clock.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualHazardClock.json','website/scripts/inline_lean.py','website/scripts/check_cross_domain_browser.py','_site/data/underlying-lean-graph.json','_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html'])
paths.extend(r/p for p in ['claim.json','publication-plan.json','integration.notes.json','visual.inspection.json','root.viewed-captures75.json','verified.json','root.math75.adoption.json','root.decoder75.adoption.json','root.source75.adoption.json','root.exact-verification75.adoption.json','root.review-input-metadata75.adoption.json','source-review.clean.packet.json','implementation-source-map75.json','integration75/owned-before.json','integration75/before-generator-state.json','integration75/final-admin.json','integration75/unchanged-regression-reuse.json','integration75/pr315-body75.md'])
for a in ['root.math75.adoption.json','root.source75.adoption.json','root.exact-verification75.adoption.json','root.review-input-metadata75.adoption.json']:paths.append(Path(load(r/a)['native_lease']['path']))
paths.append(r/'anonymous-decoder/CLOSED_LAST.json')
for q in n['checks']:paths.extend(r/'integration75'/q['label']/p for p in ['receipt.json','stdout.log','stderr.log'])
paths.extend(p for p in (r/'integration75/visual75').iterdir() if p.is_file())

paths.extend(r/'integration75/affected-module-graph'/p for p in ['receipt.json','stdout.log','stderr.log','affected-graph.receipt.json'])
paths.extend((r/'integration75').glob('cell.*.exactraw.snapshot.json'));paths=list(dict.fromkeys(paths))
assert all(p.is_file() for p in paths),[p.as_posix() for p in paths if not p.is_file()]
out=r/'final-reader-repository-packet75.json';assert not out.exists()
out.write_text(json.dumps(dict(status='FROZEN_FINAL75_FOR_INDEPENDENT_SCOPED_AGGREGATE_READER',actual_root_PID=os.getpid(),checked_science_commit=head,inputs=[pin(p) for p in paths],expected=dict(registry_count=524,root_jobs=n['root_jobs'],test_jobs=n['test_jobs'],publication_units=245,statements=1,formula_BODY_steps=9,module_lines=396,actual_captures=12,copy_callbacks=3,RAW_downloads=3),RAW_authority=True,LF_rule='CRLF byte pairs -> LF only',native_math_source_decoder_reviews_reused=True,prior_full_regressions_reused_with_explicit_runtime_qualification=True,fresh_current_scoped_browser=True,independent_scoped_reader_pending=True,full_Exposition_Seal=False,PURIFIED=False,main_live=False,wholepaper_or_Goal_complete=False),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS75 finite final reader freeze',len(paths),'inputs; aggregate/reader scope only.')
