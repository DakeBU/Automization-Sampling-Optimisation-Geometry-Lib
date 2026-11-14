from runner import *
import shutil, re
C=OUT/'candidate';SITE=OUT/'reader-site'
sys.path[:0]=[str(C/'tools'),str(C/'website/scripts')]
import astis_site as base, declaration_lessons as lessons, publication_reader, astis_publication as pub, source_lineage
base._ACTIVE_GATE=base.GateEvidence(False,False,COMMIT,'','',[],'Bounded fixture; aggregate gate intentionally unverified')
base._ACTIVE_GIT=base.GitContext(COMMIT,'fixed-e654-native-reader','','',False,False,set())
modules,decls=base.scan_project_sources();base._SOURCE_BY_NAME={d.full_name:d for d in decls};base._ALL_MODULES=modules
unit=json.loads((C/'website/content/declaration_lessons/huanjian-gaussian-source-matrix-variance.json').read_text())['units'][0]
item=json.loads((C/'website/content/publications/huanjian-gaussian-source-matrix-variance.json').read_text())['items'][0]
# Explicit adapter only supplies the bounded inputs. No prior source-review or compiled badge is loaded.
data={'declarations':base._SOURCE_BY_NAME,'lessons':{unit['declaration']:unit},'audits':{},'cells':{}}
pub.inputs=lambda:data
SITE.mkdir(exist_ok=False);(SITE/'textbook').mkdir()
theme='<html><head>'+''.join(f'<link rel="stylesheet" href="../assets/{x}">' for x in ['site.css','information-architecture.css','proof-readers.css'])+'</head><body>Minimal canonical theme seed; unverified.</body></html>'
(SITE/'textbook/index.html').write_text(theme)
for p in (C/'website/static').rglob('*'):
 if p.is_file():
  q=SITE/'assets'/p.relative_to(C/'website/static');q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
pages=[]
lesson=lessons.lesson_path(unit['declaration']);proof=publication_reader.source_proof_path(item)
for rel,body in [(lesson,lessons.render_unit(unit,lesson)),(proof,publication_reader.source_card(item,proof))]:
 html=base.page(unit['title'],rel,body,extra_head='<link rel="stylesheet" href="../assets/proof-readers.css">')
 html=source_lineage.canonical_shell(html,rel,SITE)
 base.write_page(SITE,rel,html);pages.append(rel)
# Real production source export plus production source-module renderer.
lessons.export_sources(SITE,[unit])
for m in modules:
 rel=f'modules/{base.slugify(m.name)}.html'
 html=base.render_source_module(m,[x.name for x in modules if m.name in x.imports])
 base.write_page(SITE,rel,source_lineage.canonical_shell(html,rel,SITE))
 q=SITE/'downloads/lean'/m.source_file;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((C/m.source_file).read_bytes())
checks=[]
for rel in pages:
 html=(SITE/rel).read_text()
 assert html.count('class="proof-reader-step reader-proof-disclosure"')==7
 assert 'unverified' in html and 'pending historical audit' in html if rel==proof else 'unverified' in html
 for lo,hi,key in [(0,4,'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceMatrixVariance.lean'),(4,7,'Tests/GaussianComplexityFixedSpectrumSourceMatrixVariance.lean')]:
  actual=''.join(s['lean'] for s in unit['steps'][lo:hi]).encode()
  expected=(C/key).read_bytes();assert actual==expected,(rel,key,sha(actual),sha(expected))
 checks.append({'path':rel,'sha256':sha((SITE/rel).read_bytes()),'steps':7,'exact_P_folds_lines':216,'exact_T_folds_lines':206})
result={'commit':COMMIT,'page_contexts':pages,'checks':checks,'global_navigation_and_late_overlays':'outside bounded fixture','minimal_theme_seed':theme,'empty_audits_cells':True,'source_export_function':'declaration_lessons.export_sources','source_module_renderer':'astis_site.render_source_module','download_export':'verbatim production build_site per-module write_bytes operation (lines 3205-3207)','remote_citations':'not fetched','passive_historical_labels':['lesson sources label Complete exact compiled declaration source; not used as evidence']}
(OUT/'reader-build.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
