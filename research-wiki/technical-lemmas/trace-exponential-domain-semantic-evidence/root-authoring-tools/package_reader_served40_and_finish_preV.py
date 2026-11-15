from pathlib import Path
import hashlib,json,subprocess
r=Path.cwd();w=r/'.astis/huanjian-gc-trace-mgf-domain-20261115'
e=r/'research-wiki/technical-lemmas/trace-exponential-domain-semantic-evidence'
d=w/'metadata-drafts/reader-public-custody-v1';sd=d/'served-delta-subreview'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
selection=sd/'reviewed-forty.selection.v1.json';assert sha(selection)=='b0bb21f84450c3e0829353ac3811024a5dd52ea1f8c27f6fd8b24774ca785b5a'
assert sha(sd/'served-delta-privacy-subreview.json')=='05b4ac8d0cc602f7683b5ee419010c9909bce5f99009438007f65d5e0305eabe'
assert sha(sd/'served-delta-byte-closure.audit.json')=='fed039f6a7f03f71f61dd23063cc724574b3ab2f0045289b325aededabf21e2b'
original=w/'reader-served-byte-delta-v1/served-delta.selection.v1.json'
assert sha(original)=='b935d564528150647cec5278c9e4c1b42e674d75988e016cbc48069318df7dcf'
out=e/'reader-served-byte-closure';assert not out.exists();out.mkdir()
for p in [selection,original,sd/'served-delta-privacy-subreview.json',sd/'served-delta-byte-closure.audit.json']:(out/p.name).write_bytes(p.read_bytes())
packer=r/'.astis/huanjian-gc-matrix-laplace-20261114/lossless_allowlist_container.native-dag-v2.py'
assert sha(packer)=='4385d8e2ab61344e1ecfdbd3d3f8e5f74f1f5983f33fc5ee3c5efaf1468db774'
archive=out/'new-exact-reader-served-and-freeze-originals40.v1.tar.gz';custody=out/'ROOT-later-lossless-served40-custody.v1.json'
subprocess.run(['python3',str(packer),'--source-base',str(w),'--manifest',str(selection),
 '--output-archive',str(archive),'--custody-json',str(custody)],check=True)
v=json.loads(original.read_text());assert len(v['all207_served_byte_resolutions'])==207
envelope={'kind':'ROOT-later-complete-current-served-byte-resolution-not-a-browser-run',
 'new_archive':str(archive.relative_to(r)),'new_archive_sha256':sha(archive),
 'new_member_names_are':'selected_relative_path exactly for new served members; five renderer/freeze originals per exact40manifest',
 'all207_resolutions':v['all207_served_byte_resolutions'],
 'authority':'Exact independent40-leaf privacy/custody and public-f1d58 oldarchive byte resolution, not transferred R15 reader/math/source verdict.',
 'actual_current_runtime_and_visual':'Independent R16 actual-result17654105... and reader report59bed62c...; code/fixture/PNG identities unchanged.'}
(out/'ROOT-complete-current-served-byte-resolution.v1.json').write_text(json.dumps(envelope,ensure_ascii=False,indent=2)+'\n')
privacy=e/'reader-originals/trace_exp_reader_61e4/privacy-custody-originals';privacy.mkdir()
for name,h in [('READER77-CUSTODY-SUMMARY.v1.json','2924d5e395a37c4507f7206bdbf391a0b100137daf9f416007b898b79f0e2738'),
 ('READER77-PRIVACY-CUSTODY-REVIEW.v1.json','84503ef59730d256737715de8520a65498de4ddfedf941019befa1de21214a16')]:
    p=d/name;assert sha(p)==h;(privacy/name).write_bytes(p.read_bytes())
cp=r/'research-wiki/frontier-cells/ASTIS-SHARED-REAL-TRACE-EXPONENTIAL-DOMAIN.json';c=json.loads(cp.read_text())
report=e/'reader-originals/trace_exp_reader_61e4/readable-originals/reader-acceptance-v1/reader-acceptance-report.json'
assert sha(report)=='59bed62c292887d2f8bfa1c8401443033a1a4e8ea4cacb68188a4e96cd9a1071'
c['reader_contract']['status']='Current e441 authored source/wholemodule/seven-slot exposition and actual isolated desktop/mobile reader accepted independently. Main/production/purification remain separate.'
c['graph_contribution']['visual_review']='Actual independent inspection of all36 current PNGs, including all six P/Radius/Structure desktop/mobile actual focus states, node/label SVGclip intersections1 and full IDs in detail. One canonical P; private T only module; source references remain dashed. No full/global graph fit or production claim.'
c['graph_contribution']['current_reader_report']={'file':str(report.relative_to(r)),'sha256':sha(report)}
c['evidence']['reader_review']={'report':{'file':str(report.relative_to(r)),'sha256':sha(report)},
 'actual_runtime_result_sha256':'17654105a8a14921e275ba90191df0ab125a297b7a94032155eab08b577d27c2',
 'actual_exit_code':0,'actual_checks':389,'false_checks':0,'actual_PNGs':36,'independent_actual_PNGs_viewed':36,
 'required_isolated_reader_residuals':0,'originals77_archive':'research-wiki/technical-lemmas/trace-exponential-domain-semantic-evidence/reader-originals/trace_exp_reader_61e4/selected-actual-reader-originals77.v1.tar.gz',
 'complete_served_byte_resolution':str((out/'ROOT-complete-current-served-byte-resolution.v1.json').relative_to(r)),
 'limits':'Headless Chrome responsive CSS viewports, not physical touch. SVG longID ellipsis resolved in full detail. Glyph bbox subpixel overhang<=0.359375px within original1CSSpx contract; actual glyphs readable. Steps1/5 representativePNG; all five folds/source/copy/download checks actual. Clipboard payloads not separately saved;18 exact real comparisons retained. Not production/fullsite/postV-pixels/purification.'}
c['phase_snapshot']='One actual normal PROVED_LOCAL; original24 evidence unchanged. Independent immutable301728 native/source/currente441 exposition and actual isolated reader accepted, necessary local reader residual0. Normal proofV and main/Registry/global sourceIndex/graph/production/purification/full paper remain open.'
cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
mem=e/'local-cycle-memory.json';m=json.loads(mem.read_text());m.update(reader_runtime='Actual389/0false/36PNG plus independent all36-PNG/geometry/copy/source/download acceptance; required bounded residual0',reader_report_sha256=sha(report));mem.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
assert sha(e/'PROVED_LOCAL-evidence.full.json')=='a17ff70fa56a86070673d630943b43148f32f874f6f3f1243ddf6b73c2d889bf'
print(json.dumps({'served40_archive_sha256':sha(archive),'all_current_served_files_resolve':207,
 'old_immutable_file_bytes_only_reused':172,'independent_reader_accepted':True,'original_PL24_unchanged':True,'normal_proof_V':0}))
