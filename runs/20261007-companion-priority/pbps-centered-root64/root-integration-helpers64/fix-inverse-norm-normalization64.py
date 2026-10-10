from pathlib import Path
r=Path('runs/20261007-companion-priority/pbps-centered-root64')
s=(r/'combined-draft-v9.lean').read_text(encoding='utf-8')
old='simpa only [one_div,div_eq_mul_inv,mul_comm] using hh'
assert s.count(old)==1
s=s.replace(old,'simpa only [one_div,div_eq_mul_inv,mul_comm,one_mul] using hh')
p=r/'combined-draft-v10.lean';assert not p.exists();p.write_text(s,encoding='utf-8',newline='\n')
print('v10 removes the sole remaining inverse-bound scalar normalization mismatch, with exact theorem type retained.')
