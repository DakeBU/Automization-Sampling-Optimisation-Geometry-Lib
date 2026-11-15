from pathlib import Path
import hashlib,json,subprocess
r=Path.cwd();w=r/'.astis/huanjian-gc-matrix-laplace-20261114'
n=r/'.astis/semantic-neutral-20261114/laplace_native_61e4/reader-runtime-v3'
a=w/'metadata-drafts/reader-runtime-public-selection'
e=r/'research-wiki/technical-lemmas/matrix-laplace-tail-semantic-evidence/reader-originals/laplace_native_61e4/v3'
packer=w/'lossless_allowlist_container.native-dag-v2.py'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(packer)=='4385d8e2ab61344e1ecfdbd3d3f8e5f74f1f5983f33fc5ee3c5efaf1468db774'
manifest=n/'presentation-selected-originals.manifest.v1.json'
selection=a/'reader-runtime-public-selection.356.v1.json'
audit=a/'reader-runtime-selection-privacy-audit.v1.json'
assert sha(manifest)=='3cea83cd0e61df11cba9ab36dca51f1f64c79b18df1238b836d8f9c05f301451'
assert sha(selection)=='32eb21e057e3be2b440d4be3bdf20d1aac0e5c65b067ac0daafaf17f5fd69ed3'
assert sha(audit)=='45799399f5a9bb7d121aa579d95d4129f3f90122a4eb572b8a9d9bc66e207271'
x=json.loads(manifest.read_text());s=json.loads(selection.read_text())
assert s['files']==x['leaves'] and len(s['files'])==356
assert sum(v['bytes'] for v in s['files'])==25128875
e.mkdir(parents=True,exist_ok=True)
for p in [manifest,selection,audit,a/'audit_reader_selection.v1.py']:
    target=e/p.name
    assert not target.exists()
    target.write_bytes(p.read_bytes())
archive=e/'selected-presentation-originals.actual-v3.356.v1.tar.gz'
custody=e/'ROOT-selected-presentation356-container-custody.v1.json'
assert not archive.exists() and not custody.exists()
subprocess.run(['python3',str(packer),'--source-base',str(n),'--manifest',str(selection),
 '--output-archive',str(archive),'--custody-json',str(custody)],check=True)
note={'classification':'ROOT_LATER_LOSSLESS_CONTAINER_OF_ACTUAL_V3_RAW_BROWSER_EVIDENCE',
 'actual_run':'2026-11-14T13:51:27.441984+00:00 to 2026-11-14T13:52:52.131906+00:00',
 'actual_browser_exit_code':0,'raw_script_checks':398,'raw_script_false_checks':0,
 'original_actor_manifest_unchanged':True,'exact_original_leaf_count':356,
 'original_bytes_not_normalized_or_reconstructed':True,
 'independent_privacy_selection_is_not_math_or_presentation_acceptance':True,
 'independent_visual_finding':'The two desktop parent actual-UI-zoom-pan PNGs are empty in the graph region: the harness panned nodes outside the SVG clip. Its font-size check did not check visible-area intersection. Raw398PASS is preserved as an actual original output, not accepted as evidence of those parent nodes being visible.',
 'current_status':'Independent targeted browser supplement and fresh visual review pending for parent SVG zoom/pan visibility. No normal VERIFIED or complete presentation acceptance is claimed by this container.',
 'v4':'No browser-v4 execution. Only the exact207 served-byte identity transfers page observations; metadata/source review remains separately bound.',
 'limits':['Responsive desktop/mobile viewports, not physical touch devices.','Default-fit graph labels are small; long SVG labels may be ellipsized or outside the mobile viewport; full identifiers are readable in detail.','The frozen isolated fixture TODO/Lean-gate badges are not production or post-VERIFIED status pixels.'],
 'archive_sha256':sha(archive),'archive_bytes':archive.stat().st_size,
 'scope':'Isolated reader evidence only; main/shared integration, production site and purification remain separate.'}
(e/'ROOT-container-truth-boundary.v1.json').write_text(json.dumps(note,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'members':356,'archive_sha256':sha(archive),'archive_bytes':archive.stat().st_size,'V_calls':0,'parent_zoom_visibility_supplement_pending':True}))
