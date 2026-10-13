from pathlib import Path
root=Path.cwd();r=root/'runs/20261007-companion-priority/pbps-centered-root64'
src=(r/'combined-draft-v6.lean').read_text(encoding='utf-8')
marker='  subst Tr\n'
assert src.count(marker)==1
prefix=src.split(marker)[0]+marker
out=r/'c4-prefix-diagnostic-v7.lean'
assert not out.exists()
out.write_text(prefix+'  exact noProof64_C4_PREFIX_DIAGNOSTIC_INTENTIONALLY_UNDEFINED\n\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredRootOrderInverse\n',encoding='utf-8',newline='\n')
print('Diagnostic only: same sealed full type and proof prefix through exact rough/Poincare graph and same-T identification; undefined tail intentionally retained.')
