from pathlib import Path
import json, os, runpy

OUT=Path('/Users/zhouhuanjian/ASTIS-GC/.astis/semantic-neutral-20261109/src_cosine_5d8c2a/phase3/resumed1')
p=runpy.run_path(str(OUT/'run_fresh_checks.py'))
ROOT,FRESH,LEAN,run,sha=[p[k] for k in ['ROOT','FRESH','LEAN','run','sha']]
manifest_bytes=(ROOT/'lake-manifest.json').read_bytes()
manifest=json.loads(manifest_bytes)
pins=[];libs=[]
for i,pkg in enumerate(manifest['packages']):
    observed=(OUT/f'020-pin-{i}-{pkg["name"]}.stdout').read_text().strip()
    clean=(OUT/f'021-clean-{i}-{pkg["name"]}.stdout').read_text().strip()
    assert observed==pkg['rev'] and clean==''
    lib=ROOT/'.lake/packages'/pkg['name']/'.lake/build/lib/lean'
    if lib.is_dir():libs.append(str(lib))
    pins.append({'name':pkg['name'],'url':pkg['url'],'expected_rev':pkg['rev'],'observed_rev':observed,'tracked_clean':True,'lib_path':str(lib),'prebuilt_lib_present':lib.is_dir()})
(OUT/'probe-003-cli-lib-absence.json').write_text(json.dumps({'failed_script':'run_fresh_checks.py','exit_code':1,'error':'AssertionError: .lake/packages/Cli/.lake/build/lib/lean is absent','stage':'environment path construction before fresholean or any candidate compilation','diagnosis':'Cli pin and clean-source checks passed; this unused package has no prebuilt Lean library directory. Keep all nine pin checks, include only existing dependency library paths.','source_or_statement_change':False},indent=2)+'\n')
FRESH.mkdir(exist_ok=False)
env=dict(os.environ);env['LEAN_PATH']=':'.join([str(FRESH),str(ROOT/'.lake/build/lib/lean')]+libs)
(OUT/'fresh-environment.json').write_text(json.dumps({'lean_executable':str(LEAN),'lean_executable_sha256':sha(LEAN.read_bytes()),'lean_version':(OUT/'012-lean-version.stdout').read_text().strip(),'toolchain_file_sha256':sha((ROOT/'lean-toolchain').read_bytes()),'manifest_sha256':sha(manifest_bytes),'pins':pins,'LEAN_PATH':env['LEAN_PATH'],'fresholean_first':True,'fresholean_did_not_exist_before_run':True,'cli_lib_absence_handling':'pin still independently checked; missing unused lib path omitted','dependency_scope':'Exact pinned existing dependency oleans reused. Both candidate modules compile into new first-path fresholean.'},indent=2)+'\n')
for label,module in [('030-fresh-production','AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumCosineExpansion'),('031-fresh-test','Tests/GaussianComplexityFixedSpectrumCosineExpansion')]:
    dest=FRESH/(module+'.olean');dest.parent.mkdir(parents=True,exist_ok=True)
    run(label,[str(LEAN),'-o',str(dest),module+'.lean'],env)
print('FRESH_CANDIDATE_MODULES_COMPILED',flush=True)
