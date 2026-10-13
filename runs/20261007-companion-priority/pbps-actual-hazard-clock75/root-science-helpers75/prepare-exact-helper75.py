from pathlib import Path
import ast,re
p=Path('.astis/pbps-bounce74/adopt-exact74.py');s=p.read_text(encoding='utf8')
s=s.replace('pbps-actual-bounce-rate74','pbps-actual-hazard-clock75')
s=re.sub(r'74(?![0-9a-f])','75',s)
s=s.replace("=='d556a7550f0395d149720da6478bfdfff98368a7'",'')
s=s.replace('fresh_Lean_PID_19204_reused_exact_RAW=True','fresh_direct_Lean_math75_PID18716_exact_RAW_reused=True')
ast.parse(s);out=Path('.astis/pbps-clock75/adopt-exact75.py');assert not out.exists();out.write_text(s,encoding='utf8',newline='\n')
print('PASS75 exact SCI adoption template prepared; native schema/decision will be checked before execution; no transition or gate credit.')
