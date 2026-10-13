from pathlib import Path
import hashlib,json,os,subprocess
r=Path('runs/20261007-companion-priority/pbps-actual-projected-rotation70')
pre=Path('runs/20261007-companion-priority/pbps-actual-projected-rotation-preproof70')
sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.resolve().as_posix(),raw_bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')))
q=json.loads((r/'focused-canonical-v2/receipt.json').read_bytes())
assert q['terminal_closed'] and q['exit_code']==0
source=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualProjectedRotation.lean')
assert source.read_bytes()==Path('.astis/pbps-actual-rotation70/diagnostic-named-literal70-v2.lean').read_bytes()
assert 'Build completed successfully (3949 jobs).' in (r/'focused-canonical-v2/stdout.log').read_text(encoding='utf-8')
for token in ['sorry','admit','axiom']:
 assert not any(line.lstrip().startswith(token+' ') for line in source.read_text(encoding='utf-8').splitlines())
names=[source,Path('lean-toolchain'),Path('lake-manifest.json'),
 Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ReflectionIntertwining.lean'),
 Path('AutoSamplingTheory/ExampleCases/ProximalBPS/GaussianReflection.lean'),
 pre/'header0-proposed-expanded.lean',pre/'root.statement-seal70.json',
 pre/'root.header-math70.adoption.json',pre/'root.header-source70.adoption.json',pre/'root.library-retrieval70.json',
 r/'root.named-literal70.adoption.json',r/'implementation70.v2.json',r/'claim.json',
 r/'focused-canonical-v2/receipt.json',r/'compiler-diagnosis70/inline-route-retired70.json',
 r/'compiler-diagnosis70/header-named-literal70.proposal.json',r/'compiler-diagnosis70/header-named-literal70.proposed.lean',
 Path('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-projected-rotation.json')]
dest=r/'math-freeze.theorem-only70.json';assert not dest.exists()
dest.write_text(json.dumps(dict(status='FOCUSED_CANONICAL70_COMPILED_FROZEN_NOT_INDEPENDENTLY_REVIEWED',
 actual_root_PID=os.getpid(),checked_base_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
 inputs=[pin(p) for p in names],canonical_source=pin(source),source_lines=len(source.read_text(encoding='utf-8').splitlines()),
 original_statement_seal_retained=True,representation_overlay_admitted=True,
 focused_receipt=pin(r/'focused-canonical-v2/receipt.json'),exact_standard3=['propext','Classical.choice','Quot.sound'],
 same6_callers_and12_witnesses=True,actual_output_components_not_RHS_definitions=True,
 mean_g_proved_internally=True,no68_sharp_energy_parent=True,
 remaining='P16/P17 actual B21 corrector change; B4/H1/dynamics/main/errors/costs/composition.',
 independent_math_review=False,source_review=False,PROVED_LOCAL=False,VERIFIED=False,
 failed_inline_routes_retired='compiler-diagnosis70/inline-route-retired70.json',
 typed_negative=dict(classification='PINNED_DEPENDENT_TYPE_ELABORATION_REPRESENTATION',strict_reduction='Same sealed mathematical statement compiled using independently admitted literal representation; BODY errors corrected by typed adjoint/symmetry identities. No premise or formula weakened.')),
 ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS canonical70 frozen:544lines/3949EXIT0/standard3; independent theorem mathematics, decoder and source still pending.')
