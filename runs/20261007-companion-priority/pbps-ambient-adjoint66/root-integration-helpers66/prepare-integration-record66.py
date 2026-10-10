from pathlib import Path
old=Path('.astis/pbps-polar65');out=Path('.astis/pbps-ambient-adjoint66')
def write(name,s):
 p=out/name;assert not p.exists(),p;p.write_text(s,encoding='utf-8',newline='\n')
def common(s):
 return s.replace('pbps-polar65','pbps-ambient-adjoint66').replace('integration65','integration66').replace('visual65','visual66').replace('verification65','verification66').replace('Registry511','Registry512').replace('registry_count=511','registry_count=512').replace('aggregate65','aggregate66').replace('exact65b','exact66').replace('Exact65b','Exact66')
s=common((old/'preserve-integration-newlines65-final.py').read_text());write('preserve-integration-newlines66-final.py',s)
s=common((old/'record-integration65.py').read_text())
s=s.replace('pbps-actual-polar-isometry','pbps-ambient-adjoint-corrector').replace('PolarIsometry.lean','AmbientAdjointCorrector.lean')
s=s.replace("len(capture['records'])==7","len(capture['records'])==8").replace("==5","==6").replace('all5','all6').replace('steps=5','steps=6').replace('steps=5','steps=6').replace('5literal','6literal').replace('7viewed','8viewed').replace('232','233')
s=s.replace("reviewed64_metadata_overlay=(r/'integration66/stale-cell-overlay64.applied.json').as_posix(),",'')
s=s.replace('One exact actual polar-isometry declaration/module and typed adjoint-corrector Test;one affected card and current aggregate graph artifacts. No new private provider or conceptual bridge promoted into a formal edge.','One actual ambient-adjoint/global-centering declaration/module and genuine global norm-budget Test; one affected card and current aggregate graph artifacts. Two literal Prop representations add no private mathematical provider or conceptual formal edge.')
s=s.replace('Ambient block-adjoint extension and globally centered input adapter;B20/B21/halfturn/H1/dynamics/main/errors/expectedquerycost/composition remain open.','Full B20 first-corrector energy bound;B21/halfturn/H1/dynamics/main/errors/expectedquerycost/composition remain open.')
s=s.replace('Focused and independent math/decoder/source/exact-commit,required frontier metadata correction,publication and local aggregate accepted within B16/typed corrector scope.','Focused and independent math/decoder/source/exact-commit, reviewed dependency catalogues, publication and local aggregate accepted within ambient-adjoint/global-centering scope.')
s=s.replace('full statement still uses plain Unicode/underscored notation; default placement of complete Lean disclosures remains part','full statement still uses plain Unicode/underscored notation and two reviewed literal private Prop representations; default placement of complete Lean disclosures remains part')
write('record-integration66.py',s)
print('Prepared root-owned66 aggregate recorder and newline-preservation helper; not executed.')
