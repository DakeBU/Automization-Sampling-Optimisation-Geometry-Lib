from pathlib import Path
import json,os,sys,traceback,hashlib
ROOT=Path('E:/Samplinglib');RUN=ROOT/'runs/20261007-companion-priority/pbps-b4-corrector-perturbation72';OWN=RUN/'independent-source72'
PRIOR=ROOT/'runs/20261007-companion-priority/pbps-b4-perturbation-preproof72/independent-header-source72'
def write(n,x): (OWN/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
code=0
try:
 sys.stdout.reconfigure(encoding='utf-8')
 for n in [0,1]:
  p=json.loads((RUN/f'source-review.packet.{n}.json').read_text(encoding='utf-8'))
  d=json.loads((RUN/f'anonymous.{n}.decoder.json').read_text(encoding='utf-8'))
  write(f'StageB.semantic-unit.{n}.readview.json',{'source_original':p['source']['original_text'],'reconstruction':p['blind_reconstruction'],'lean_statement':p['lean']['statement'],'anonymous_approved_context':d.get('approved_definition_context',d.get('definition_context')),'anonymous_packet_keys':list(d)})
 coverage=json.loads((PRIOR/'stageA.finite-source255-plus-supplemental-coverage72.frozen.json').read_text(encoding='utf-8'))
 graph=json.loads((PRIOR/'stageA.source-proof-graph72.before-header.frozen.json').read_text(encoding='utf-8'))
 formulas=json.loads((PRIOR/'stageA.target20-exact-RAW-formulas72.frozen.json').read_text(encoding='utf-8'))
 print(json.dumps({'actual_pid':os.getpid(),'coverage_keys':list(coverage),'coverage_key_types':{k:type(v).__name__ for k,v in coverage.items()},'coverage_examples':{k:v[:2] for k,v in coverage.items() if isinstance(v,list)},'graph_keys':list(graph),'nodes':graph.get('nodes'),'formula_keys':list(formulas),'formulas':formulas},ensure_ascii=False,indent=2))
except BaseException:
 code=1;traceback.print_exc()
finally:write('StageB.inspect-semantics.terminal.json',{'actual_pid':os.getpid(),'exit_code':code,'argv':sys.argv,'background':False})
sys.exit(code)
