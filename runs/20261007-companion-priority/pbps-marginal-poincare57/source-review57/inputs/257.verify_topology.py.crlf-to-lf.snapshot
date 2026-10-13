from pathlib import Path
from html.parser import HTMLParser
import json,hashlib,collections,re,sys,datetime,os
sys.stdout.reconfigure(encoding='utf8')
R=Path('E:/Samplinglib'); B=R/'runs/20261007-companion-priority/pbps-marginal-poincare-sourcegraph57'; O=R/'runs/20261007-companion-priority/pbps-marginal-poincare-sourcegraph-review57'; P=R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(j):return json.dumps(j,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf8')
def pin(p):
 p=Path(p);p=p if p.is_absolute() else R/p;b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return {'path':str(p).replace('\\','/'),'bytes':len(b),'raw_sha256':sha(b),'lf_bytes':len(lf),'lf_sha256':sha(lf)}
def write(n,j):
 j['content_self_sha256']=sha(canon(j));p=O/n;p.write_bytes((json.dumps(j,ensure_ascii=False,indent=2)+'\n').encode('utf8'));q=json.loads(p.read_bytes());v=q.pop('content_self_sha256');assert sha(canon(q))==v
checks=[];selfchecks=[];inputs={};historical_checks=[]
def receipt_check(q,where):
 p=Path(q['path']);p=p if p.is_absolute() else R/p;a=pin(p)
 if any(a[k]!=q[k] for k in ['bytes','raw_sha256','lf_sha256'] if k in q):
  alternatives={'website/content/samplewiki_companion_frontiers.json':'samplewiki_companion_frontiers.exactraw.snapshot','docs/companion-papers-handoff.md':'companion-papers-handoff.exactraw.snapshot'}
  assert where.startswith('own-primary/lease.json/inputs/') and q['path'] in alternatives,(where,q['path'])
  old=pin(P/alternatives[q['path']]);assert all(old[k]==q[k] for k in ['bytes','raw_sha256','lf_sha256'] if k in q)
  historical_checks.append({'location':where,'historical_original_pin':q,'current_mutable_pin':a,'exact_preserved_historical_snapshot':old,'meaning':'Canonical file legitimately changed after historical CLOSED freeze; historical receipt verified against owned frozen raw snapshot, not asserted current.'});a=old
 for k in ['bytes','raw_sha256','lf_sha256']:
  if k in q:assert a[k]==q[k],(where,k,q['path'])
 inputs[a['path']]=a;checks.append({'location':where,'actual':a})
def walk(j,where):
 if isinstance(j,dict):
  if {'path','bytes','raw_sha256','lf_sha256'}<=set(j):receipt_check(j,where)
  if 'content_self_sha256' in j:
   x=dict(j);v=x.pop('content_self_sha256');assert sha(canon(x))==v,where;selfchecks.append({'location':where,'field':'content_self_sha256','digest':v,'recipe':'Complete object minus ONLY this field, sorted compact UTF8 ensure_ascii=False.'})
  for k,v in j.items():walk(v,where+'/'+k)
 elif isinstance(j,list):
  for i,v in enumerate(j):walk(v,where+'/'+str(i))
for n in ['source-only-freeze.json','graph.packet.json','binder-and-reuse-audit.json','coverage.citation-supplement.json','input-manifest.json','complete.json','lease.open.json','lease.json']:
 p=B/n;j=json.loads(p.read_bytes());inputs[str(p).replace('\\','/')]=pin(p);walk(j,n)
for n in ['primary.contract.json','source.precision-addendum.json','next-consumer.blueprint.json','source-anchor-manifest.json','lease.json']:
 p=P/n;inputs[str(p).replace('\\','/')]=pin(p);walk(json.loads(p.read_bytes()),'own-primary/'+n)
assert pin(B/'graph.packet.json')['raw_sha256']=='b4c3f3db9ff224bf7fcf048026e3cc1ca003b93b708f080dca2e5307cca6c6ed'
assert pin(B/'lease.json')['raw_sha256']=='52e92f9f1048d3823dd1c02a17c0f4655bc1e243058ee3dc834e62c9895e938c'
f=json.loads((B/'source-only-freeze.json').read_bytes());g=json.loads((B/'graph.packet.json').read_bytes());sup=json.loads((B/'coverage.citation-supplement.json').read_bytes());anchors=json.loads((P/'source-anchor-manifest.json').read_bytes())['anchors']
raw=(P/'primary-pbps.exactraw.snapshot.html').read_bytes();s=raw.decode('utf8'); assert sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
lineoffs=[0]
for line in s.splitlines(keepends=True):lineoffs.append(lineoffs[-1]+len(line))
charbytes=[0]
for c in s:charbytes.append(charbytes[-1]+len(c.encode('utf8')))
class Regions(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=False);self.stack=[];self.regions=[]
 def handle_starttag(self,t,attrs):
  q=dict(attrs);classes=q.get('class','').split();kind=None
  if t=='p' and 'ltx_p' in classes:kind='substantive-paragraph'
  elif 'ltx_equation' in classes:kind='display-equation'
  elif 'ltx_theorem' in classes:kind='source-statement'
  elif 'ltx_proof' in classes:kind='proof-container'
  elif t=='cite':kind='external-citation'
  l,c=self.getpos();start=lineoffs[l-1]+c
  if t not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:self.stack.append((t,start,kind,q.get('id')))
 def handle_startendtag(self,t,attrs):pass
 def handle_endtag(self,t):
  l,c=self.getpos();end=s.find('>',lineoffs[l-1]+c)+1
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i][0]==t:
    _,start,kind,identity=self.stack[i];self.stack=self.stack[:i]
    if kind:
     a,b=charbytes[start],charbytes[end]
     if any(x['source_start_utf8_byte']<=a and b<=x['source_end_utf8_byte_exclusive'] for x in anchors):self.regions.append({'kind':kind,'start':a,'end':b,'id':identity})
    break
p=Regions();p.feed(s)
expected={(x['kind'],x['start'],x['end']) for x in p.regions}
actual={(x['kind'],x['primary_start_utf8_byte'],x['primary_end_utf8_byte_exclusive']) for x in f['coverage']+sup['coverage']}
missing=sorted(expected-actual);extra=sorted(actual-expected)
assert not missing and not extra,(len(expected),len(actual),missing[:4],extra[:4])
assert len(f['coverage'])==596 and len(sup['coverage'])==10
nodeids={n['id'] for n in g['nodes']};assert len(nodeids)==len(g['nodes'])
for c in f['coverage']+sup['coverage']:
 b=raw[c['primary_start_utf8_byte']:c['primary_end_utf8_byte_exclusive']];assert sha(b)==c['raw_sha256'] and sha(b.replace(b'\r\n',b'\n'))==c['lf_sha256'];assert c['disposition'] in ['NODE','EXCLUDED'] and c['reason'].strip()
 if c['disposition']=='NODE':assert c['node_id'] in nodeids
for e in g['edges']:assert e['consumer'] in nodeids and all(n in nodeids for n in e['parents']) and e['formal_dependency_admitted'] is False
assert f['edges']==g['edges']
original_sem=[n for n in f['nodes'] if not n.get('coverage_node_only')]; active_sem=[n for n in g['nodes'] if not n.get('coverage_node_only')];assert original_sem==active_sem
assert f['chronology']['prospective_statement_read'] is False and g['chronology']['candidate_read_after_freeze'] is True
assert json.loads((B/'lease.json').read_bytes())['state']=='CLOSED'
# Extract ONLY public prefixes. Stop on the first literal proof marker, retaining all ambient typing.
header_receipts=[]
for slug,rel in [('SmoothedHessianUpper','AutoSamplingTheory/ExampleCases/SmoothedPicardHMC/SmoothedHessianUpper.lean'),('SmoothedGibbsPotential','AutoSamplingTheory/ExampleCases/SmoothedPicardHMC/SmoothedGibbsPotential.lean')]:
 path=R/rel;parts=[];marker=False
 with path.open('rb') as h:
  for line in h:
   if b':= by' in line:parts.append(line.split(b':= by',1)[0]);marker=True;break
   parts.append(line)
 assert marker;hb=b''.join(parts);lf=hb.replace(b'\r\n',b'\n');(O/(slug+'.public-header.exactraw.snapshot.lean')).write_bytes(hb);(O/(slug+'.public-header.lf.snapshot.lean')).write_bytes(lf)
 rec={'path':rel,'header_raw_bytes':len(hb),'header_raw_sha256':sha(hb),'header_lf_bytes':len(lf),'header_lf_sha256':sha(lf),'cutoff':'Before first literal := by; proof suffix not read or displayed; ambient typeclasses retained.'};header_receipts.append(rec)
 if slug=='SmoothedGibbsPotential':assert hb==(B/'SmoothedGibbsPotential.public-header.exactraw.snapshot.lean').read_bytes()
write('native.verification.json',{'schema_version':1,'actor':'/root/next_primary56','native_receipt_checks':checks,'native_receipt_check_count':len(checks),'historical_snapshot_resolutions':historical_checks,'native_complete_self_hash_checks':selfchecks,'native_complete_self_hash_count':len(selfchecks),'independent_source_enumeration':{'parser':'Independent stdlib HTMLParser global raw UTF8 byte offsets; p.ltx_p / any.ltx_equation / any.ltx_theorem / any.ltx_proof / cite, within union of exact21 balanced anchors; deduplicated by kind/span. No creator parser code used.','expected_region_count':len(expected),'actual_region_count':len(actual),'missing':missing,'extra':extra,'frozen_regions':596,'citation_supplement':10,'frozen_dispositions':dict(collections.Counter(c['disposition'] for c in f['coverage'])),'citation_dispositions':dict(collections.Counter(c['disposition'] for c in sup['coverage']))},'source_graph':{'nodes':len(g['nodes']),'semantic_nodes':len(active_sem),'edges':len(g['edges']),'frozen_semantics_and_edges_unchanged':True,'all_node_edge_references_exist':True,'coverage_node_exists_for_all_NODE':True},'header_only_receipts':header_receipts,'creator_finalizer_actual_external_exit0':'ecfbe0 provided by parent; independent native complete/source-process exit0 fields verified, not rerun','compiler':'NOT_STARTED_CLOSED','proof_bodies_read':False,'operational_notes':['Read-only exploratory stdout had a KeyError on a header-only receipt lacking bytes and a truncated UTF8 prefix decode; corrected native header-receipt interpretation, no source or mathematical inference from those operational errors.','Initial strict check rejected legitimately changed current frontier standing file in historical own lease; exact owned historical snapshot verified and explicitly distinguished from current canonical bytes.']})
write('input.manifest.json',{'schema_version':1,'actor':'/root/next_primary56','inputs':list(inputs.values()),'header_only_inputs':header_receipts,'raw_lf_recipe':'Hash exactraw bytes, LF replaces ONLY CRLF with LF; never JSON reserialization. Parent Lean reads stop before proof marker; no full-module receipt or body read.','input_count':len(inputs)})
(O/'inputs').mkdir(exist_ok=False)
for i,q in enumerate(inputs.values()):
 b=Path(q['path']).read_bytes();stem=f'{i:03d}.{Path(q["path"]).name}';a=O/'inputs'/(stem+'.raw.snapshot');z=O/'inputs'/(stem+'.lf.snapshot');a.write_bytes(b);z.write_bytes(b.replace(b'\r\n',b'\n'));assert a.read_bytes()==b and z.read_bytes()==b.replace(b'\r\n',b'\n')
print(json.dumps({'status':'NATIVE_VERIFICATION_EXIT0','pid':os.getpid(),'inputs':len(inputs),'receipt_checks':len(checks),'self_hash_checks':len(selfchecks),'regions':len(expected),'nodes':len(g['nodes']),'edges':len(g['edges']),'header_only':2},ensure_ascii=False))
