from pathlib import Path
import hashlib,json,re,subprocess,os
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC');OUT=ROOT/'.astis/semantic-neutral-20261109/src_9a6d2f/phase3'
def h(b):return hashlib.sha256(b).hexdigest()
log=(OUT/'lean-evidence/kernel-probe.log').read_text();run=json.loads((OUT/'lean-evidence/kernel-probe-run.json').read_text());assert run['returncode']==0 and 'PRIVATE_LITERAL_KERNEL_TYPE_APPLICATION_PASS' in log
matches=re.findall(r'DIRECT_ASTIS (.*?): \[([^\]]*)\]',log,re.S);direct={n:[x.strip() for x in names.split(',') if x.strip()] for n,names in matches};assert len(direct)==2
expected={
'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGeometry.actual_potential_geometry':[
'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAdmissibility.actual_precision_admissible',
'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumFirstOrder.actual_first_order_query',
'AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexGradientConverse.strongConvexOn_of_gradient_inner_lower_bound'],
'_private.Tests.GaussianComplexityFixedSpectrumGeometry.0.actual_first_order_oracle_measurable':[
'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGeometry.actual_potential_geometry',
'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumFirstOrder.actual_first_order_query']}
assert {k:set(v) for k,v in direct.items()}=={k:set(v) for k,v in expected.items()}
axioms={n:[x.strip() for x in names.split(',') if x.strip()] for n,names in re.findall(r'KERNEL_AXIOMS (.*?): \[([^\]]*)\]',log,re.S)};assert len(axioms)==2 and all(set(v)=={'propext','Classical.choice','Quot.sound'} for v in axioms.values())
(OUT/'lean-evidence/kernel-summary.json').write_text(json.dumps({'kernel_probe_returncode':0,'direct_ASTIS_proof_constants':direct,'recursive_kernel_axioms':axioms,'public_sealed_anonymous_type_application':'passed by example : ExpectedPublic := @actual_potential_geometry','private_literal_type_application':'passed by kernel addDecl with ExpectedPrivate and the actual imported private constant','same_tree_fresh_imports':True,'failed_probe_scope':'Three failed private evidence-tool probes were preserved as failed-v1/v2/v3, caused by record-layout then command/CoreM API errors; candidate math and modules unchanged.'},indent=2)+'\n')
paths=['tools/astis_site.py','website/scripts/inline_lean.py','website/scripts/declaration_lessons.py','website/scripts/build_site.py','tools/astis_publication.py','tools/astis_semantic_roundtrip.py','tools/astis_semantic_roundtrip_core.py']
records=[{'path':rel,'bytes':len((ROOT/rel).read_bytes()),'sha256':h((ROOT/rel).read_bytes()),'role':'process/renderer/local-schema implementation read; no transition execution'} for rel in paths]
windows={'Analysis/CStarAlgebra/Matrix.lean':[(116,130)],'LinearAlgebra/Matrix/PosDef.lean':[(48,70),(154,170)],'Analysis/InnerProductSpace/Rayleigh.lean':[(112,132)]}
directory=OUT/'standard-windows';directory.mkdir(exist_ok=True)
for rel,ranges in windows.items():
 p=ROOT/'.lake/packages/mathlib/Mathlib'/rel;b=p.read_bytes();lines=b.splitlines(keepends=True);row={'path':str(p.relative_to(ROOT)),'bytes':len(b),'sha256':h(b),'role':'necessary critical implementation standard definition/theorem semantics','windows':[]}
 for a,c in ranges:
  raw=b''.join(lines[a-1:c]);name=rel.replace('/','__')+f'.L{a}-L{c}.txt';(directory/name).write_bytes(raw);row['windows'].append({'file':'standard-windows/'+name,'start':a,'end':c,'sha256':h(raw)})
 records.append(row)
leanroot=Path('/Users/zhouhuanjian/.elan/toolchains/leanprover--lean4---v4.33.0/src/lean/Lean')
for rel in ('Declaration.lean','Util/FoldConsts.lean','Util/CollectAxioms.lean','Elab/Command.lean'):
 p=leanroot/rel;b=p.read_bytes();records.append({'path':str(p),'bytes':len(b),'sha256':h(b),'role':'Lean kernel evidence API definitions/search windows; toolchain version/binary separately recorded'})
(OUT/'supplementary_input_hashes.json').write_text(json.dumps(records,indent=2)+'\n')
# Ensure actual candidate/pinned inputs stayed unchanged after all checking.
pins=json.loads((OUT/'inputs/evidence__full-review-input-pins.json').read_text());env=dict(os.environ);env['GIT_OPTIONAL_LOCKS']='0';head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,env=env,text=True).strip();assert head==pins['checked_candidate_commit']
for p,digest in pins['exact_inputs'].items():assert h((ROOT/p).read_bytes())==digest,p
assert subprocess.run(['git','diff','--quiet'],cwd=ROOT,env=env).returncode==0 and subprocess.run(['git','diff','--cached','--quiet'],cwd=ROOT,env=env).returncode==0
(OUT/'postcheck-preservation.json').write_text(json.dumps({'candidate_HEAD':head,'all12_pinned_actual_inputs_unchanged':True,'canonical_blind_audit_sha256':pins['exact_inputs']['research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-geometry.json'],'both_ledgers_unchanged':True,'tracked_working_tree_and_index_clean':True,'canonical_sourceV_transition':'not executed','checked_candidate_vs_future_carrier':'All mathematical checks bind this ab8b47ca candidate. No accepted-audit carrying commit exists in this reviewer scope.'},indent=2)+'\n')
print(json.dumps({'kernel_summary':'passed','direct_ASTIS_parents':direct,'preservation':'passed'}))
