from pathlib import Path
import json,hashlib
O=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-actual-physical-time-law81/exact-commit-verification81')
p=O/'verify81.py';s=p.read_text(encoding='utf8')
old="assert len(regions)==10 and regions[0]['start']==100 and regions[-1]['end']==313\nassert b''.join(step['lean'].encode() for step in lesson['steps'])==b''.join(lines[99:313])"
new="assert len(regions)==10 and regions[0]['start']==110 and regions[-1]['end']==310\nassert b''.join(step['lean'].encode() for step in lesson['steps'])==b''.join(lines[109:310])\nassert all(regions[i]['end']+1==regions[i+1]['start'] for i in range(9))\nassert lines[99].startswith(b'theorem ') and b'ideal_half_turn_returned_position_kernel_statement' in lines[109]\nassert b':= by' in lines[109] and lines[110].strip()==b'classical'"
assert old in s
with (O/'verify81-v2.py').open('x',encoding='utf8',newline='\n') as f:f.write(s.replace(old,new))
data=dict(status='VERIFIER_RANGE_ASSERTION_DIAGNOSED',original_driver_RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),original_terminal_exit_code=1,original_terminal_traceback='verify81.py line77: assert len(regions)==10 and regions[0][start]==100 and regions[-1][end]==313; AssertionError',native_terminal_evidence='functions.exec/exec_command chunk e18126 reported exit1 after3.7618423s; original tool transcript is retained. No native subprocess log existed for this preflight assertion.',actual_ten_regions_first_line=110,actual_ten_regions_last_line=310,reason='Public theorem signature occupies100–109; BODY begins target :=by at110 and ends310; namespace end313 is outside BODY.',classification='VERIFIER_IMPLEMENTATION_FAILED',science_repair=False,source_or_lesson_edits=False,corrected_driver='verify81-v2.py')
with (O/'preflight-range-diagnosis81.json').open('x',encoding='utf8') as f:json.dump(data,f,ensure_ascii=False,indent=2);f.write('\n')
