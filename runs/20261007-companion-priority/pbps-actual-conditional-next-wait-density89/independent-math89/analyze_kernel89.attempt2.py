from pathlib import Path
import hashlib,json,runpy,sys
R=Path('E:/Samplinglib');O=Path(__file__).parent
p=O/'analyze_kernel89.py';b=p.read_bytes()
d=O/'kernel-analysis-import89.negative.json'
with d.open('x',encoding='utf8',newline='\n') as f:
 json.dump({'tool_chunk':'7c82c5','exit_code':1,'scope':'Reviewer Python postprocessing only; both Lean foreground checks already EXIT0.','cause':'tools.astis imports sibling astis_harness as a top-level module. Reviewer supplied repo root but omitted tools directory from sys.path.','original_script':{'path':p.relative_to(R).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)},'repair':'Successor adds actual tools directory to Python import search; no Lean/source/statement change.','original_failure_retained':True},f,indent=2);f.write('\n')
sys.path.insert(0,str(R/'tools'))
runpy.run_path(str(p),run_name='__main__')
