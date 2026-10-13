from pathlib import Path
import json,hashlib,re

p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/SharpCorrectorEnergy.lean')
s=p.read_text(encoding='utf-8');before=p.read_bytes()
start=s.index('theorem actual_sharp_corrector_bound')
prefix,s=s[:start],s[start:]
s,n=re.subn(r'  run_tac do\n    let _ ← IO.eprintln "68 stage: [^"]+"\n    pure \(\)\n','',s)
assert n==6
points=[('  classical\n','proof-entry'),
 ('  unfold actual_sharp_corrector_bound_statement\n','before-unfold'),
 ('  let μ :=','after-unfold'),
 ('  have hBase :=','before-parent-call'),
 ('  rcases hBase with\n','before-parent-rcases'),
 ('  let A : HP →L[ℝ] HP :=','after-parent-rcases'),
 ('  have hKself :','before-coefficient'),
 ('  let γ : ℝ :=','after-coefficient'),
 ('  have hPair (u v : HP0)','before-pair'),
 ('    change |C u v| ≤','after-generic-leaf'),
 ('      _ = (‖u‖^2+‖v‖^2)/(2*γ) :=','before-ratio-simplification'),
 ('  refine ⟨hμ, ?_⟩','after-pair'),
 ('  intro f hf\n','after-witness-reassembly'),
 ('  have hBudget :','before-budget'),
 ('  refine ⟨fP,hfP','after-budget')]
for i,(needle,label) in enumerate(points):
 assert s.count(needle)==1,(needle,s.count(needle))
 indent='    ' if needle.startswith('    ') else '  '
 if needle.startswith('      '):
  # A calc branch cannot take a tactic before its expression. Pin the marker inside its proof.
  needle='      _ = (‖u‖^2+‖v‖^2)/(2*γ) := by field_simp; ring'
  replacement='''      _ = (‖u‖^2+‖v‖^2)/(2*γ) := by
        run_tac do
          let _ ← IO.FS.writeFile ".astis/pbps-sharp-energy68/stage4-%02d.log" "%s\\n"
          pure ()
        field_simp
        ring'''%(i,label)
 else:
  marker=indent+'run_tac do\n'+indent+'  let _ ← IO.FS.writeFile ".astis/pbps-sharp-energy68/stage4-%02d.log" "%s\\n"\n'%(i,label)+indent+'  pure ()\n'
  replacement=marker+needle
 s=s.replace(needle,replacement)
p.write_text(prefix+s,encoding='utf-8',newline='\n')
r=Path('runs/20261007-companion-priority/pbps-sharp-energy68')
d=r/'compiler-diagnosis68';d.mkdir(exist_ok=False)
(d/'main.before-file-instrumentation.raw.snapshot.lean').write_bytes(before)
(d/'instrumentation.json').write_text(json.dumps(dict(status='LOCAL_COMPILER_DIAGNOSTIC_ONLY',points=[dict(index=i,label=z[1]) for i,z in enumerate(points)],private_statement_and_callers_unchanged=True,mathematical_ingredients_unchanged=True,all_diagnostics_removed_before_final_freeze=True,whole_proof_credit=False),indent=2)+'\n',encoding='utf-8',newline='\n')
print('15 direct-file diagnostic stages installed; no mathematical statement or premise change.')
