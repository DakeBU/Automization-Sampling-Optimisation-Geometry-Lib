import hashlib,json,os,pathlib
from html.parser import HTMLParser
R=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent;S=R/'runs/20261007-companion-priority/pbps-real-root-unique62/next-macro-source63'
O.mkdir(exist_ok=True);(O/'inputs').mkdir(exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.relative_to(R).as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def wr(n,x):(O/n).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
class Text(HTMLParser):
 def __init__(self):super().__init__();self.t=[];self.ids=[];self.math=[]
 def handle_data(self,s):self.t.append(s)
 def handle_starttag(self,t,a):
  d=dict(a)
  if 'id' in d:self.ids.append(d['id'])
  if t=='math' and 'alttext' in d:self.math.append(d['alttext']);self.t.append(d['alttext'])
paths=sorted(S.glob('primary-*.exactraw.snapshot.html'));assert len(paths)==24
paths.append(S/'source-cap.supplement.json');pairs=[]
for i,p in enumerate(paths):
 b=p.read_bytes();a=O/'inputs'/f'primary-{i:02d}-{p.name}.raw.snapshot';z=O/'inputs'/f'primary-{i:02d}-{p.name}.LF.snapshot';a.write_bytes(b);z.write_bytes(b.replace(b'\r\n',b'\n'));pairs.append(dict(original=pin(p),raw_snapshot=pin(a),lf_snapshot=pin(z)))
primary=R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html';whole=primary.read_bytes();assert sha(whole)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
regions=[]
for p in paths[:-1]:
 b=p.read_bytes();lo=whole.find(b);assert lo>=0 and whole.find(b,lo+1)<0
 text=Text();text.feed(b.decode('utf8'));regions.append(dict(snapshot=pin(p),primary=pin(primary),byte_range=[lo,lo+len(b)],ids=text.ids,math_alttext=text.math,literal_source_text=' '.join(' '.join(text.t).split())))
wr('primary.first.manifest.json',dict(actual_foreground_pid=os.getpid(),qualified_raw_LF_pairs=pairs,fixed_primary=pin(primary),source_regions=regions,candidate_headers_current_Lean_scout_contract_graph_API_not_read=True,source_only_scope='23 frozen literal primary regions plus literal positive-eta/model cap supplement; no scout graph/contract/API or candidate content read'))
wr('primary.first.receipt.json',dict(actual_foreground_pid=os.getpid(),regions=24,raw_LF_pairs=25,source_only=True,candidate_not_read=True,compiler=False,prior_source_verdict_not_read=True))
print(json.dumps(dict(actual_foreground_pid=os.getpid(),literal_regions=regions,source_cap_supplement=json.loads(paths[-1].read_bytes()),candidate_not_read=True),ensure_ascii=False))
