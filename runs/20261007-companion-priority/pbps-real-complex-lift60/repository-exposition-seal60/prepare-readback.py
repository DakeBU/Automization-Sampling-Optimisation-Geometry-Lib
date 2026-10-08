import pathlib,json,hashlib,os,re
from html.parser import HTMLParser
ROOT=pathlib.Path('E:/Samplinglib');R=ROOT/'runs/20261007-companion-priority/pbps-real-complex-lift60';D=R/'repository-exposition-seal60'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(q):return json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def load(p):return json.loads(pathlib.Path(p).read_bytes())
def write(p,q):pathlib.Path(p).write_bytes((json.dumps(q,ensure_ascii=False,indent=2)+'\n').encode())
def path(s):
 p=pathlib.Path(s.replace('\\','/'));return p if p.is_absolute() else ROOT/p
class CodeParser(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.details=[];self.pre=False;self.parts=[];self.blocks=[]
 def handle_starttag(self,tag,attrs):
  if tag=='details':self.details.append(dict(attrs))
  if tag=='pre':self.pre=True;self.parts=[];self.closed=[dict(x) for x in self.details]
 def handle_endtag(self,tag):
  if tag=='pre' and self.pre:self.blocks.append((''.join(self.parts),self.closed));self.pre=False
  if tag=='details':self.details.pop()
 def handle_data(self,s):
  if self.pre:self.parts.append(s)
p=ROOT/'_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html';hp=pin(p);parser=CodeParser();parser.feed(p.read_text(encoding='utf8'));code=[]
freeze=load(R/'math-freeze.json')
for name,row in zip(freeze['mathematical_declarations'],freeze['inputs'][:2]):
 s=path(row['path']).read_text(encoding='utf8');short=name.rsplit('.',1)[-1];start=re.search(r'^theorem '+re.escape(short)+r'\b',s,re.M);assert start
 exact=s[start.start():].rstrip();matches=[(b,d) for b,d in parser.blocks if exact==b.strip()];assert matches,(name,'ACTUAL_CODE_BLOCK_NOT_EXACT')
 assert all(d and all('open' not in a for a in d) for b,d in matches)
 code.append(dict(declaration=name,actual_compiled_source=pin(path(row['path'])),exact_statement_plus_proof_chars=len(exact),HTML_exact_blocks=len(matches),initially_folded=True))
write(D/'reader-exact-Lean.json',dict(status='PASS',actual_PID=os.getpid(),page=hp,scope='Exact two current public declaration bodies in rendered adjacent folded code, no whole-page mathematical seal',blocks=code))
# Post-input scoped61 claim changes ONLY reviewed ledger identity; exact hash mapping.
h=load(ROOT/'runs/20261007-companion-priority/pbps-real-defect-root61/ledger-history.json');before=pin(path(h['exact_raw_snapshot']['path']));assert all(before[k]==h['original'][k] for k in ['bytes','raw_sha256','lf_sha256'])
original=dict(before,path=path(h['original']['path']).as_posix());hist=dict(original=original,exact_snapshot=before,reason='Post-review-input SAU61 claim outside63c7435; exact original63c ledger snapshot, no future61 mathematical reads',history=pin(ROOT/'runs/20261007-companion-priority/pbps-real-defect-root61/ledger-history.json'))
assert any(x['resolved']['path']==original['path'] and x['resolved']['raw_sha256']==original['raw_sha256'] for x in load(D/'input.manifest.json')['artifacts'])
write(D/'post-input-ledger-mapping.json',hist)
q=load(D/'payload.json');payload=q['named_repository_exposition_payload'];payload['exact_adjacent_folded_Lean']=pin(D/'reader-exact-Lean.json');payload['post_input_scope_note']='Root claimed61 after this63c7435 input/review. Complete d8c944... native graph input and511 source pins retained from before claim; no future61 proof or graph acceptance. Only exact reviewed ledger pin resolves via explicit before61 snapshot.';payload['post_input_ledger_mapping']=pin(D/'post-input-ledger-mapping.json');ps=sha(canon(payload));q['named_repository_exposition_payload_sha256']=ps;write(D/'payload.json',q)
receipt=load(D/'receipt.json');receipt['status']='ACCEPTED_SCOPED';receipt['payload']=pin(D/'payload.json');receipt['named_repository_exposition_payload_sha256']=ps;receipt['exact_adjacent_folded_Lean']=pin(D/'reader-exact-Lean.json');receipt['post_input_ledger_mapping']=pin(D/'post-input-ledger-mapping.json');write(D/'receipt.json',receipt)
run=load(D/'run.json');run['receipt']=pin(D/'receipt.json');run['payload_file']=pin(D/'payload.json');run['named_repository_exposition_payload']=payload;run['named_repository_exposition_payload_sha256']=ps;run['run_sha256']=sha(canon({k:v for k,v in run.items() if k!='run_sha256'}));write(D/'run.json',run)
print(json.dumps(dict(status='EXACT_FOLDED_CODE_AND_POST_INPUT_MAP_READY',actual_PID=os.getpid(),run_sha256=run['run_sha256'],payload_sha256=ps)),flush=True)
