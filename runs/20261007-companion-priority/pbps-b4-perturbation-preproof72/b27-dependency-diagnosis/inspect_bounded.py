from pathlib import Path
import hashlib, json, os, re, sys, traceback
from html import unescape

ROOT = Path('E:/Samplinglib')
OWN = ROOT/'runs/20261007-companion-priority/pbps-b4-perturbation-preproof72/b27-dependency-diagnosis'
FILES = [
 'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html',
 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean',
 'AutoSamplingTheory/ExampleCases/ProximalBPS/SharpCorrectorEnergy.lean',
 'AutoSamplingTheory/TechnicalLemmas/Probability/KernelReversibility.lean',
 'AutoSamplingTheory/TechnicalLemmas/Probability/KernelMixture.lean',
 'AutoSamplingTheory/TechnicalLemmas/Probability/ConditionalKernel.lean',
 'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-corrector-change.json',
]

def sha(b): return hashlib.sha256(b).hexdigest()
def write(name, value):
 (OWN/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
def plain(s):
 s=re.sub(r'<math\b[^>]*alttext="([^"]*)"[^>]*>.*?</math>', lambda m: ' $'+unescape(m[1])+'$ ',s, flags=re.S)
 return re.sub(r'\s+',' ',unescape(re.sub('<[^>]+>',' ',s))).strip()

code=0
try:
 pins=[]
 for rel in FILES:
  b=(ROOT/rel).read_bytes(); lf=b.replace(b'\r\n',b'\n')
  pins.append({'path':rel,'raw_bytes':len(b),'raw_sha256':sha(b),'lf_bytes':len(lf),'lf_sha256':sha(lf),'lf_recipe':'bytewise CRLF to LF only; all other bytes preserved'})
 write('inputs.finite-pins.json', {'schema':'bounded-source-reuse-input-pins-v1','content_file_limit':7,'content_files_read':len(FILES),'files':pins,'excluded':'No 72 implementation/body, decoder, math verdict, independent sourceplan or canonical edits.'})
 raw=(ROOT/FILES[0]).read_bytes(); text=raw.decode('utf-8')
 hits=[]
 for pat in [r'half.turn',r'Proposition 3\.2',r'Proposition A\.2',r'\(A\.9\)',r'id="A1\.E9',r'id="A2\.E7',r'id="A2\.Ex27',r'id="A2\.E27']:
  matches=list(re.finditer(pat,text,re.I))
  rows=[]
  for m in matches:
   a=max(0,m.start()-1400); z=min(len(text),m.end()+2600)
   rows.append({'raw_byte_hit':len(text[:m.start()].encode()),'context':plain(text[a:z])})
  hits.append({'pattern':pat,'matches':len(matches),'contexts':rows})
 write('primary.search-contexts.json',hits)
 views=[]
 for rel in FILES[1:]:
  s=(ROOT/rel).read_text(encoding='utf-8')
  views.append('FILE '+rel+'\n'+'\n'.join(f'{i}: {v}' for i,v in enumerate(s.splitlines(),1)))
 (OWN/'selected-six.line-readview.txt').write_text('\n\n'.join(views)+'\n',encoding='utf-8',newline='\n')
 print(json.dumps({'pid':os.getpid(),'files':pins,'primary_context_counts':[(h['pattern'],h['matches']) for h in hits]},ensure_ascii=False,indent=2))
except BaseException:
 code=1; traceback.print_exc()
finally:
 write('inspect-bounded.terminal.json',{'actual_pid':os.getpid(),'exit_code':code,'argv':sys.argv,'background':False,'writes_scope':str(OWN),'content_file_limit':7})
sys.exit(code)
