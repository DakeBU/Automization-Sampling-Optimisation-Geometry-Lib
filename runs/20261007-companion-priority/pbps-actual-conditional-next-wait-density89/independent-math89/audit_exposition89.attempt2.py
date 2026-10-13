import json,hashlib
from pathlib import Path
O=Path(__file__).parent
p=O/'audit_exposition89.py'
negative={'status':'REVIEWER_BOUNDARY_MARKER_ASSERTION_FAILED_BEFORE_AUDIT_OUTPUT','original_script_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'terminal_tool_chunk':'f0989c','terminal_exit_code':1,'cause':'Reviewer guessed final BODY text ends D h s; actual final line436 is the indicator outside-A simplification. Exact six region byte checks had already passed. No production, theorem or exposition mutation.','observed_line436':'      · simp [f, ha]','correction':'Check the actual final line and the subsequent section/namespace ends instead of guessed mathematical text.'}
with (O/'exposition-boundary-probe89.negative.json').open('x',encoding='utf8',newline='\n') as f:json.dump(negative,f,indent=2);f.write('\n')
s=p.read_text('utf8')
old="assert lines[113].endswith(':= by') and lines[435].strip().endswith('D h s')"
new="assert lines[113].endswith(':= by') and lines[435].strip()=='· simp [f, ha]' and lines[436]=='' and lines[437]=='end' and lines[438].startswith('end AutoSamplingTheory.')"
assert s.count(old)==1
exec(compile(s.replace(old,new,1),str(p),'exec'),{'__file__':str(p),'__name__':'__main__'})
