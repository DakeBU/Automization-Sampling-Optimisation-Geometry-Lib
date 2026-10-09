from pathlib import Path
from html.parser import HTMLParser
import html,hashlib,json,os,sys,traceback
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path('E:/Samplinglib');RUN=ROOT/'runs/20261007-companion-priority/pbps-harmonic-flow-preproof73';OWN=RUN/'independent-header-source73'
OLD=ROOT/'runs/20261007-companion-priority/pbps-half-turn-construction-preread73';GRAPH=ROOT/'runs/20261007-companion-priority/pbps-harmonic-flow-sourcegraph73'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def load(p):return json.loads(p.read_bytes())
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_sha256':sha(b.replace(b'\r\n',b'\n')),'LF_recipe':'CRLF-to-LF only; all other bytes preserved'}
def write(n,x):(OWN/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
class View(HTMLParser):
 def __init__(self):super().__init__();self.out=[];self.math=0
 def handle_starttag(self,t,at):
  a=dict(at)
  if t=='math':
   if not self.math:self.out.append(' '+a.get('alttext','[math without alttext]')+' ')
   self.math+=1
  elif not self.math and t in ['p','table','tr','div','section','li','h1','h2','h3','h4']:self.out.append('\n')
 def handle_endtag(self,t):
  if t=='math':self.math-=1
  elif not self.math and t in ['p','table','tr','div','section','li','h1','h2','h3','h4']:self.out.append('\n')
 def handle_data(self,d):
  if not self.math:self.out.append(d)
code=0
try:
 assert not (OWN/'lease.final.json').exists()
 adoptions=[load(RUN/n) for n in ['root.source-first73.adoption.json','root.sourcegraph73.extraction-adoption.json']]
 closure=[]
 for a,p in zip(adoptions,[OLD,GRAPH]):
  lease=load(p/'lease.final.json');assert sha((p/'lease.final.json').read_bytes())==a['native_lease']['RAW_sha256']
  members=lease.get('all_files_except_self',lease.get('files',[]));verified=0
  for r in members:
   f=ROOT/r['path'];b=f.read_bytes();assert sha(b)==r['raw_sha256'] and len(b)==r['bytes'];assert sha(b.replace(b'\r\n',b'\n'))==r['lf_sha256'];verified+=1
  run=load(p/'run.json');s=run.pop('run_sha256');assert sha(canon(run))==s==a['native_whole_logical_run_sha256']
  closure.append({'scope':p.relative_to(ROOT).as_posix(),'lease':pin(p/'lease.final.json'),'whole_logical_run_sha256':s,'opaque_member_hashes_verified':verified,'mathematical_or_topology_verdict_consumed':False})
 primary=ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html';raw=primary.read_bytes();assert len(raw)==1482128 and sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
 regions=load(OLD/'source.regions.json');blocks=load(GRAPH/'source.blocks.json')
 views=[]
 for r in blocks['regions']:
  a,b=r['raw_byte_start_inclusive'],r['raw_byte_end_exclusive'];assert sha(raw[a:b])==r['whole_region_raw_sha256']
  v=View();v.feed(raw[a:b].decode('utf-8'));views.append({'source_id':r['source_id'],'RAW_start':a,'RAW_end_exclusive':b,'RAW_sha256':r['whole_region_raw_sha256'],'direct_primary_readview':'\n'.join(s.strip() for s in ''.join(v.out).splitlines() if s.strip()),'blocks':[]})
  for s in r['blocks']:
   aa,bb=s['raw_byte_start_inclusive'],s['raw_byte_end_exclusive'];assert sha(raw[aa:bb])==s['literal_span_raw_sha256']
   vv=View();vv.feed(raw[aa:bb].decode('utf-8'))
   views[-1]['blocks'].append({'block_id':s['block_id'],'RAW_start':aa,'RAW_end_exclusive':bb,'RAW_sha256':s['literal_span_raw_sha256'],'direct_primary_readview':' '.join(''.join(vv.out).split())})
 assert len(views)==13 and sum(len(r['blocks']) for r in views)==51
 write('StageA.direct-primary13-regions51-blocks.readview.json',{'primary':pin(primary),'count_regions':13,'count_blocks':51,'recipe':'direct exact RAW ranges from fixed primary; HTML text plus original math alttext; no candidate/header/Lean reconstruction','regions':views})
 refs=[RUN/'root.source-first73.adoption.json',RUN/'root.sourcegraph73.extraction-adoption.json',OLD/'lease.final.json',OLD/'run.json',OLD/'selected-contract.json',OLD/'source-expectations.json',OLD/'source.regions.json',OLD/'construction.formula-spans.json',GRAPH/'lease.final.json',GRAPH/'run.json',GRAPH/'source.blocks.json',GRAPH/'source-proof-graph.json',GRAPH/'source.coverage.json',GRAPH/'binder-audit.json',GRAPH/'standing-assumptions.audit.json',GRAPH/'definition-semantics-and-boundary.json',GRAPH/'reuse.gradient-continuity.json',GRAPH/'gradient-continuity.statement.exactraw.txt',ROOT/'AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/Gradient.lean',ROOT/'.agents/skills/astis-proof-dag/SKILL.md']
 write('StageA.finite-input-pins73.json',{'inputs':[pin(p) for p in refs],'input_count':len(refs),'primary_reference':pin(primary),'reference_only_no_recursive_copy':True,'73_header_or_hash_read':False,'72_new_review_source_verdict_read':False,'LF_recipe':'CRLF-to-LF only'})
 write('StageA.native-reference-integrity73.json',{'closures':closure,'previous_closed_trees_written':False,'actual_pid':os.getpid()})
 write('lease.open.json',{'status':'OPEN_STAGE_A_ONLY_BEFORE_HEADER','owned_scope':OWN.relative_to(ROOT).as_posix(),'header_or_hash_read':False,'old_closed_or_canonical_writes':False})
 write('StageA.observer-negatives73.json',{'events':[{'tool_chunk':'604838','exit_code':1,'actual_pid':'not reported; not invented','classification':'stdout GBK UnicodeEncodeError in inline JSON observation; no input mutation or mathematical failure','correction':'this named observer sets UTF8 stdout explicitly'}]})
 print(json.dumps({'actual_pid':os.getpid(),'exit_code':0,'regions':13,'blocks':51,'finite_pins':len(refs),'opaque_closures':closure,'readview_RAW_sha256':sha((OWN/'StageA.direct-primary13-regions51-blocks.readview.json').read_bytes())},ensure_ascii=False,indent=2))
except BaseException:code=1;traceback.print_exc()
finally:write('StageA.freeze-inputs.terminal.json',{'actual_pid':os.getpid(),'exit_code':code,'argv':sys.argv,'background':False})
sys.exit(code)
