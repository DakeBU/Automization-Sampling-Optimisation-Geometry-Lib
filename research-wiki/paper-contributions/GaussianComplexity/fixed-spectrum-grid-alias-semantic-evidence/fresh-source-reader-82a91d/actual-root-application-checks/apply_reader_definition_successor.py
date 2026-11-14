from pathlib import Path
import hashlib,json,subprocess,sys,tarfile
sys.dont_write_bytecode=True
sys.path.insert(0,'tools');import astis_publication as pub;import astis_semantic_roundtrip as rt
W=Path('.astis/huanjian-gc-fixed-spectrum-grid-alias-20261109')
E=Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-grid-alias-semantic-evidence')
R=Path('.astis/semantic-neutral-20261109/src_82a91d/phase3')
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda x:(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def put(p,b):
 assert not p.exists(),p;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
def ref(p):
 b=p.read_bytes();return {'path':str(p),'sha256':sha(b),'bytes':len(b)}
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()=='cbf3c22b901a484c463f417a3e206bb200622294'
assert not subprocess.check_output(['git','diff','HEAD','--name-only']).strip()
assert sha((R/'FREEZE.json').read_bytes())=='14159626df6c6d70423c5b6412c6c348ed2887c48af5a0feba45f29c5e68f8a0'
d=json.loads((R/'decision.json').read_text());assert d['whole_module_proof_binder_definition_acceptance'] is True and d['fresh_runtime_acceptance'] is True and d['static_authored_reader_acceptance'] is False
F=E/'reader-definition-successor';F.mkdir()
for p in [R/'FREEZE.json',R/'decision.json',R/'review-report.md']:put(F/('initial-phase3-'+p.name),p.read_bytes())
payload=[p for p in sorted(R.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
archive=F/'initial-phase3-whole-module-runtime-and-reader-HOLD.lossless.tar.gz'
with tarfile.open(archive,'w:gz',dereference=True) as t:
 for p in payload:t.add(p,arcname=str(p),recursive=False)
with tarfile.open(archive,'r:gz') as t:
 for p in payload:assert t.extractfile(str(p)).read()==p.read_bytes(),p
put(F/'initial-phase3-archive-manifest.json',dump({'archive':ref(archive),'files':[ref(p) for p in payload],'scope':'Exact accepted initial mathematical/runtime evidence and reader P3-R1 HOLD; failed commands retained. Existing C7 object was explicitly reused/hash-recorded, not claimed freshly rebuilt.'}))
lp=Path('website/content/declaration_lessons/huanjian-fixed-spectrum-grid-alias.json');ap=Path('research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-grid-alias.json');cp=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-grid-alias.json')
old_l=lp.read_bytes();old_a=ap.read_bytes();old_c=cp.read_bytes();lesson=json.loads(old_l);a=json.loads(old_a);cell=json.loads(old_c)
assert sha(old_l)==d['current_lesson_sha256'];assert a['source_review']=={'state':'pending'}
old_binding=a['publication_binding_sha256'];old_packet=rt.semantic_reviewer_packet(a);assert old_packet['packet_sha256']=='e8cacf92f2d511b273fc78eb30e7da6126f673ff6fcc553b569881a206b0cbfc'
put(F/'lesson-before.raw.json',old_l);put(F/'audit-before.raw.json',old_a);put(F/'frontier-before.raw.json',old_c)
step=lesson['units'][0]['steps'][3]
step['text']=r'For the private consumer only, fix real \(\kappa\ge2\) and a natural number \(n\) with \(1\le n<d\), using the same midpoint angles. Define the eigenvalues and radius by the displayed formulas. C7 supplies the reciprocal identity and absolute convergence at every actual grid point. Cosine weighting preserves summability, so the finite grid and infinite series can genuinely be exchanged.'
step['formula']=r'\begin{gathered}\lambda_i=\frac{\kappa+1}{2}+\frac{\kappa-1}{2}\cos\theta_i,\\r=\frac{\sqrt\kappa-1}{\sqrt\kappa+1},\\'+step['formula']+r'\end{gathered}'
step['lean']='The private actual_weighted_inverse_grid_alias_series calls canonical C7 for heq/habs. hsqrt and heigenlower produce positive square root and eigenvalues at least one. hmajor and hsgnorm explicitly produce weighted absolute summability; hs, hsg and hsumG give convergence. heigen normalizes the literal reciprocal eigenvalues, and Summable.tsum_finsetSum is the actual exchange. The public alias theorem itself has no κ or C7 premise.'
lp.write_bytes(dump(lesson))
pub.inputs.cache_clear();pub.load.cache_clear()
item=json.loads(Path('website/content/publications/huanjian-fixed-spectrum-grid-alias.json').read_text())['items'][0];binding=item['bindings'][0]
a['publication_binding_sha256']=pub.binding_digest(item,binding);a['publication_context']=pub.review_context(item,binding)
assert a['lean']['statement_sha256']=='08b70068857a73593fab9e27c9ab19aed6b901a163886b41a38798468e92b8e2'
assert rt.decoder_packet(a)['packet_sha256']=='32e2e7064723e27c4c8d154f55cd8a11f8ee2e1791ced44185db5a223904c1be'
assert a['source_review']=={'state':'pending'} and a['verdict']=='pending' and a['state']=='blind-reconstructed'
ap.write_bytes(dump(a));new=rt.semantic_reviewer_packet(a);assert new['packet_sha256']!=old_packet['packet_sha256'];assert all(v is False for v in new['anti_anchoring'].values())
put(E/'fresh-source-reviewer-packet-reader-v2.json',dump(new))
change={'initial_candidate':'cbf3c22b901a484c463f417a3e206bb200622294','initial_phase3_freeze':ref(R/'FREEZE.json'),'initial_issue':'P3-R1: consumer eigenvalues/radius were undefined and n not explicitly declared integer.','change':'Only lesson step4 text, displayed definitions+existing formula and Lean correspondence are changed. Define lambda_i,r and natural n with1<=n<d adjacent to the actual private consumer explanation. Public source statement, producer/Test bodies and both sealed signatures are unchanged.','old_lesson_sha256':sha(old_l),'new_lesson':ref(lp),'old_publication_binding_sha256':old_binding,'new_publication_binding_sha256':a['publication_binding_sha256'],'old_full_reviewer_packet_sha256':old_packet['packet_sha256'],'new_full_reviewer_packet_sha256':new['packet_sha256'],'anonymous_decoder_packet_unchanged':True,'old_phase1_phase2_phase3_preserved':True,'reader_static_acceptance':'pending exact independent successor review','new_math_or_sourceV_or_UI_credit':False}
put(F/'exposition-change-record.json',dump(change))
cell['evidence']['publication_binding_sha256']=a['publication_binding_sha256'];cell['evidence']['reader_definition_successor']={'record':str(F/'exposition-change-record.json'),'initial_review_run_sha256':d['review_run_sha256'],'state':'EXPOSITION_FIX_APPLIED_EXACT_INDEPENDENT_REVIEW_PENDING'};cp.write_bytes(dump(cell))
for p,h in [(Path('AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumGridAlias.lean'),'c98c899bd8b596388ae433e9241a7827e01d29c3ffcc945719238fa2e96f7d60'),(Path('Tests/GaussianComplexityFixedSpectrumGridAlias.lean'),'9f3b9e64dced3467dbd163fde7918c376571d766bcebf7f7e25717b87de5d128')]:assert sha(p.read_bytes())==h
pub.check_advance([a['lean']['declaration']],reviewed=False)
print(json.dumps(change,ensure_ascii=False))
