import hashlib,json,pathlib,tarfile,sys
ROOT=pathlib.Path('/Users/zhouhuanjian/ASTIS-GC');OUT=pathlib.Path(__file__).resolve().parent;E=OUT.parents[1];N=E/'native-review/rl_native_52e9';sha=lambda b:hashlib.sha256(b).hexdigest()
CAND='d0654e9bbed44ab852fc44598560799949d8bd12';HEAD='2c57883183937fdef1578a2b33e4ea892af2c694'
report_b=(N/'report.original.json').read_bytes();assert sha(report_b)=='74edceb44614716afc5bd13f090e322547b46b25129ccb3c7ebbddd0bfae9125';report=json.loads(report_b)
mb=(N/'portable-manifest.json').read_bytes();assert sha(mb)=='3efa0e70017f1cde3cdf57b513a603955a1edfe45883332683fecae3a33e4caf';manifest=json.loads(mb)
archive=N/'portable-evidence.tar.gz';assert sha(archive.read_bytes())=='3e20649c6649f1ea283af7d43ecf9d4f9ebca0bb6a4343cc9911b9146cd7b049'
inputs=OUT/'inputs';inputs.mkdir(exist_ok=True)
for name in ['report.original.json','portable-manifest.json','relevant-input-binding.json','metadata-carrier-byte-comparison.json','evidence-seal.json']:(inputs/('native-'+name)).write_bytes((N/name).read_bytes())
with tarfile.open(archive,'r:gz') as tar:
 members=tar.getmembers();assert len(members)==334 and all(x.isfile() for x in members)
 native={x.name.removeprefix('rl_native_52e9/'):tar.extractfile(x).read() for x in members}
 assert len(manifest['files'])==333
 for row in manifest['files']:
  b=native[row['path']];assert len(b)==row['bytes'] and sha(b)==row['sha256'],row['path']
 assert native['portable-manifest.json']==mb
 for row in manifest['files']:
  if row['path'].startswith('receipts/') and row['path'].endswith('.json'):
   r=json.loads(native[row['path']]);assert isinstance(r['argv'],list) and r['cwd'] and isinstance(r['exit_code'],int)
   for stream in ['stdout','stderr']:
    b=native[r[stream]['path']];assert len(b)==r[stream]['bytes'] and sha(b)==r[stream]['sha256']
 for name in ['build-driver','compile-0','compile-1','compile-2','compile-3','compile-4','exact-author-kernel-probe','inspect-all-v2','independent-literal-kernel-v3','native-inspect-driver-v3','reader-static-driver-v3']:
  r=json.loads(native['receipts/'+name+'.json']);assert r['exit_code']==0,name
  assert b'error:' not in native[r['stdout']['path']].lower(),name
  if name.startswith('compile-'):
   assert '/ASTIS-GC/.lake/build/lib/lean' not in r['LEAN_PATH']
   assert r['LEAN_PATH'].split(':')[0].endswith('/rl_native_52e9/native-olean')
 for name in ['inspect-all','reader-static-driver','reader-static-driver-v2','independent-literal-kernel-v2']:assert json.loads(native['receipts/'+name+'.json'])['exit_code']==1
 assert native['receipts/independent-literal-kernel-v3.stdout'].count(b'INDEPENDENT_SEAL_KERNEL_APPLICATION_PASS ')==2
 assert b'sorryAx' not in native['receipts/independent-literal-kernel-v3.stdout']
 assert b'NATIVE_MODULE_OWNED_FULL_TYPES_BODIES_AXIOMS_EXPORTED 18' in native['receipts/inspect-all-v2.stdout']
 input_manifest=json.loads(native['input-manifest.json']);build=json.loads(native['native-build.json']);summary=json.loads(native['native-summary.json'])
 assert input_manifest['candidate_commit']==build['candidate']==summary['candidate_commit']==CAND
 assert len(build['outputs'])==5 and all('/ASTIS-GC/.lake/build/lib/lean' not in p for p in build['lean_path'])
 full_path=ROOT/'.astis/semantic-neutral-20261112/rl_native_52e9/native-all-bodies-v2.json';full_b=full_path.read_bytes()
 assert len(full_b)==31070587 and sha(full_b)=='dddedfde1315bac762e4d2637d7547b57d2c6b4eb5543583a8afdf28eec1c84a'
 rows=json.loads(full_b);assert len(rows)==18;allowed={'propext','Classical.choice','Quot.sound'};index={r['name']:r for r in rows}
 for r in rows:
  assert r['type_closed'] and r['body_closed'] and r['type'] and r['body']
  assert set(r['axioms'])<=allowed and r['kind']=='theorem'
  s=next(x for x in summary['all_declarations'] if x['name']==r['name']);assert sha(r['type'].encode())==s['type_sha256'] and sha(r['body'].encode())==s['body_sha256']
 new=[r for r in rows if r['module'] in ['AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw','Tests.GaussianComplexityFixedSpectrumSourceRowLaw']];assert len(new)==4
 P=next(r for r in new if r['name'].endswith('.actual_source_row_marginal_law'));T=next(r for r in new if r['name'].endswith('.actual_original_all_good_cutoff_probability'))
 reach=set(P['transitive_owned']+T['transitive_owned']);assert all(r['name'] in reach for r in new)
 newindex={r['name']:r for r in new}
 def parents(r):
  seen=set();todo=list(r['direct']);out=set()
  while todo:
   n=todo.pop()
   if n in seen:continue
   seen.add(n)
   if n==P['name']:out.add(n)
   elif n in newindex:todo.extend(newindex[n]['direct'])
   elif n.startswith('AutoSamplingTheory.'):out.add(n)
  return sorted(out)
 assert parents(P)==[];assert parents(T)==sorted([P['name'],'AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianRadialExponential.integrable_exp_norm_sq_div_three_and_integral_stdGaussian'])
 assert any('MeasureTheory.integral_map' in r['direct'] for r in new)
 binding=json.loads((N/'relevant-input-binding.json').read_text());assert len(binding['tracked_relevant_input_hashes'])==29
 for r in binding['tracked_relevant_input_hashes']:assert sha((ROOT/r['path']).read_bytes())==r['sha256'],r['path']
 static=json.loads(native['reader-static.json']);assert report['static_reader']['consumer_exact_full_module_lines']==145
 # Retain only bounded relevant original scripts/probes/streams; do not export the31MB dump.
 keep=['run.py','build.py','prepare.py','make_inspector.py','prepare_v2.py','prepare_native_v3.py','check_native_v3.py','reader_static_v3.py','scratch/InspectAllV2.lean','scratch/IndependentLiteralCheckV3.lean','inputs/SourceRowLawKernelProbe.lean','native-build.json','native-summary.json','native-authored-types.txt','native-generated-inspection.json','fake-closure-scan.json','reader-static.json','input-manifest.json']
 for name in ['build-driver','compile-0','compile-1','compile-2','compile-3','compile-4','exact-author-kernel-probe','inspect-all','inspect-all-v2','independent-literal-kernel-v2','independent-literal-kernel-v3','native-inspect-driver-v3','reader-static-driver','reader-static-driver-v2','reader-static-driver-v3']:
  keep += ['receipts/'+name+s for s in ['.json','.stdout','.stderr']]
 for rel in keep:
  p=inputs/'native-originals'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(native[rel])
source_manifest=E/'source-review/rl_src_3dd4/portable-originals-manifest.json';sb=source_manifest.read_bytes();assert sha(sb)=='aa32f9601ccd604c7cc814670879971820922d645e8bd48d71df998b3b2e419f';source=json.loads(sb);assert source['originals_count']==103
for row in source['entries']:
 a=(ROOT/row['source']).read_bytes();b=(ROOT/row['destination']).read_bytes();assert a==b and sha(a)==row['sha256'] and len(a)==row['bytes']
for rel,h in [('source-review/rl_src_3dd4/phase4_freeze.json','2f3b8bb0bb55da138440a4a055046c279a871778062d47dd2c00ddad697af547'),('source-review/rl_src_3dd4/originals/own/phase4/phase4_freeze.json','2f3b8bb0bb55da138440a4a055046c279a871778062d47dd2c00ddad697af547'),('source-review/rl_src_3dd4/originals/own/phase4/portable-originals-manifest.json','aa32f9601ccd604c7cc814670879971820922d645e8bd48d71df998b3b2e419f')]:assert sha((E/rel).read_bytes())==h
G=ROOT/'.astis/huanjian-resume-20261103';gates=[]
for name,expected in [('20261112T063452110453Z-source-row-law-final-reviewed-publication','5adfdfd10ab3a595a76de07c855c476b731444cbe8275466fa57c9168b1d0a1c'),('20261112T063452110484Z-source-row-law-final-semantic','8740aabe4eb7faf95ecf2e801a4f66278b29379738252f41e4b7b1799e73cd06'),('20261112T063452110432Z-source-row-law-final-contributor','d898afa8166aeb55f3e901d8eb23aa10f6d96c8d476b821462269d8eae683059'),('20261112T063452110477Z-source-row-law-final-frontier','4f99e8f98772972c16fadb5ca797f3ee87e882accc791d05fffe9028e4ca029b')]:
 b=(G/(name+'.receipt.json')).read_bytes();r=json.loads(b);log=pathlib.Path(r['log']).read_bytes()
 assert r['exit_code']==0 and r['head_before']==r['head_after']==HEAD and sha(log)==r['log_sha256']==expected
 d=inputs/'final-gates';d.mkdir(exist_ok=True);(d/(name+'.receipt.json')).write_bytes(b);(d/(name+'.log')).write_bytes(log)
 gates.append({'receipt':str((G/(name+'.receipt.json')).relative_to(ROOT)),'receipt_sha256':sha(b),'log_sha256':expected,'exit_code':0,'held_head':HEAD})
pl=(E/'actual-PROVED_LOCAL-evidence.full.json').read_bytes();assert sha(pl)=='253c50d3918d7b679792a0644eb9162ec08b4420629bfc6e568efd6ac8b86c28';(inputs/'actual-PROVED_LOCAL-evidence.full.json').write_bytes(pl)
result={'accepted':True,'verified_math_candidate':CAND,'held_metadata_carrier':HEAD,'native_report_sha256':sha(report_b),'native_manifest_sha256':sha(mb),'native_archive_sha256':sha(archive.read_bytes()),'native_archive_members':334,'native_manifest_files':333,'native_all_actual_receipt_streams_checked':True,'fresh_ASTIS_modules':5,'cached_ASTIS_olean_path_used':False,'owned_closed_types_and_bodies':18,'new_owned_all_reachable':4,'standard_axioms_only':sorted(allowed),'producer_ASTIS_parents':parents(P),'consumer_ASTIS_parents':parents(T),'both_literal_kernel_applications':True,'raw_Expr_equality_claimed':False,'current_candidate_input_hashes_unchanged':29,'source_exact_originals':103,'source_review_report_raw_sha256':'6d13aee164bf8078522540708c18507d252cc7a193bbdc8e885a1eccb1301b5e','four_final_gates':gates,'native_verifier_failures':'Four preserved verifier-only causes inspected; unsuccessful commands rejected fully, later actual successful probes accepted; no candidate mathematical failure inferred.','full31MB_dump_exported':False,'remaining_HOLD':report['HOLD'][3:]}
(OUT/'acceptance-checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
