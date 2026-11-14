from pathlib import Path
import hashlib,json,re,subprocess,os,sys,datetime
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC');OUT=ROOT/'.astis/semantic-neutral-20261109/src_9a6d2f/phase3';BASE=ROOT/'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-geometry-semantic-evidence'
def h(b):return hashlib.sha256(b).hexdigest()
pins=json.loads((BASE/'full-review-input-pins.json').read_text());env=dict(os.environ);env['GIT_OPTIONAL_LOCKS']='0'
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,env=env,text=True).strip();assert head==pins['checked_candidate_commit']=='ab8b47caed9f781191f8408154cd355c7e7c104c'
assert subprocess.run(['git','diff','--quiet'],cwd=ROOT,env=env).returncode==0
assert subprocess.run(['git','diff','--cached','--quiet'],cwd=ROOT,env=env).returncode==0
records=[]
for rel,expected in pins['exact_inputs'].items():
 p=ROOT/rel;b=p.read_bytes();assert h(b)==expected,rel;name=rel.replace('/','__');(OUT/'inputs'/name).write_bytes(b);records.append({'path':rel,'bytes':len(b),'sha256':h(b),'snapshot':'inputs/'+name})
extras=['full-review-input-pins.json','full-anti-anchored-reviewer-packet.json','proof-digestion-classification.json','source-only-review/phase2/source-graph-v2.proposal.json','source-only-review/phase2/source-coverage-v2.proposal.json']
for rel in extras:
 p=BASE/rel;b=p.read_bytes();name='evidence__'+rel.replace('/','__');(OUT/'inputs'/name).write_bytes(b);records.append({'path':str(p.relative_to(ROOT)),'bytes':len(b),'sha256':h(b),'snapshot':'inputs/'+name})
pkt=json.loads((BASE/'full-anti-anchored-reviewer-packet.json').read_text());assert h((BASE/'full-anti-anchored-reviewer-packet.json').read_bytes())=='254984467d3b1937538be9ca9036e1f78e2c3dc75d4a53c1c1607fff47984311'
payload={k:v for k,v in pkt.items() if k!='packet_sha256'};assert h(json.dumps(payload,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())==pkt['packet_sha256']=='f3b870f73f647b80189c0559c60155ee257ce410a9bb1d484cb71fb75d27285a'
assert pkt['candidate_publication_context']['current_lean_module'].encode()==(ROOT/pkt['lean']['file']).read_bytes()
assert pkt['publication_binding_sha256']=='69c4f115a417c0aea6a8ebc9384cfc66ff07e6fae92de806831b79075a4760fa'
p1=OUT.parent/'phase1';p2=OUT.parent/'phase2'
for directory,manifest_name,expected in [(p1,'phase1_manifest.json','aa9b3ffb40981e0d6d80d9c1ac8458a610c41bb7137e185a89baf6d9c25f81f1'),(p2,'phase2_manifest.json','951200393b1492ea53419605942a792d3506822f3f6937ab5ec46ca374addc17')]:
 assert h((directory/manifest_name).read_bytes())==expected
 for f in json.loads((directory/manifest_name).read_text())['files']:assert h((directory/f['path']).read_bytes())==f['sha256']
# Source-proposal mechanical checks are separate from mathematical source judgment.
source=ROOT/'.astis/huanjian-resume-20261103/2610.20492v1.html';sb=source.read_bytes();assert h(sb)=='6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915';s=sb.decode()
coverage=json.loads((BASE/'source-only-review/phase2/source-coverage-v2.proposal.json').read_text());graph=json.loads((BASE/'source-only-review/phase2/source-graph-v2.proposal.json').read_text())
def span(anchor):
 if anchor.startswith('link@'):i=int(anchor[5:]);m=re.match(r'<([A-Za-z0-9]+)\b[^>]*>',s[i:]);assert m,anchor;tag=m.group(1)
 else:
  m=re.search(r'<([A-Za-z0-9]+)\b[^>]*\bid="'+re.escape(anchor)+r'"[^>]*>',s);assert m,anchor;i=m.start();tag=m.group(1)
 depth=0
 for t in re.finditer(r'</?'+re.escape(tag)+r'\b[^>]*>',s[i:]):
  depth+=-1 if t.group().startswith('</') else 1
  if depth==0:return s[i:i+t.end()].encode()
 raise ValueError(anchor)
checks=[]
for collection,key in [('paragraph_and_display_inventory','anchor'),('formula_and_citation_inventory','atom_id')]:
 for row in coverage[collection]:
  b=span(row[key]);checks.append({'anchor':row[key],'collection':collection,'expected':row['raw_sha256'],'actual':h(b),'matches':h(b)==row['raw_sha256']})
node_ids={n['id'] for n in graph['nodes']};assert len(node_ids)==len(graph['nodes'])
for route in graph['routes']:assert route['consumer'] in node_ids and set(route['prerequisites'])<=node_ids and route['consumer_use_site']
for coll in ('paragraph_and_display_inventory','formula_and_citation_inventory'):
 for row in coverage[coll]:
  if row['disposition']=='NODE':assert set(row['nodes'])<=node_ids
  else:assert row['reason']
(OUT/'source-coverage-static-check.json').write_text(json.dumps({'checks':checks,'raw_items':len(checks),'raw_hash_matches':sum(x['matches'] for x in checks),'nodes':len(graph['nodes']),'routes':len(graph['routes']),'scope':'Raw excerpts and graph structure only, not a mathematical acceptance verdict.'},indent=2)+'\n')
assert all(x['matches'] for x in checks),[x for x in checks if not x['matches']]
# Use repository rendering functions on only the four involved production modules.
sys.path.insert(0,str(ROOT/'tools'));sys.path.insert(0,str(ROOT/'website/scripts'))
import astis_site as base,inline_lean,declaration_lessons
selected=[ROOT/p for p in pins['exact_inputs'] if p.endswith('.lean') and p.startswith('AutoSamplingTheory/')]
base.project_lean_paths=lambda:selected
modules,decls=base.scan_project_sources();base._SOURCE_BY_NAME={d.full_name:d for d in decls};inline_lean.declarations.cache_clear()
unit=json.loads((ROOT/'website/content/declaration_lessons/huanjian-fixed-spectrum-geometry.json').read_text())['units'][0]
rel=declaration_lessons.lesson_path(unit['declaration']);html=declaration_lessons.render_unit(unit,rel)
static=OUT/'static-reader';static.mkdir(exist_ok=True);(static/'authored-lesson.fragment.html').write_text(html)
(static/'authored-lesson.static.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Static evidence only</title></head><body>'+html+'</body></html>')
from html.parser import HTMLParser
class Reader(HTMLParser):
 def __init__(self):super().__init__();self.details=[];self.codes=[];self.cur=None;self.incode=False;self.alltext=[]
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='details':self.details.append(a)
  if t=='code':self.cur=[];self.incode=True
 def handle_endtag(self,t):
  if t=='code':self.codes.append(''.join(self.cur));self.incode=False
 def handle_data(self,d):
  self.alltext.append(d)
  if self.incode:self.cur.append(d)
r=Reader();r.feed(html)
decl=base._SOURCE_BY_NAME[unit['declaration']];exact=inline_lean.display_source(decl.source_text);sig,body=inline_lean.split_statement(exact)
assert sig in r.codes and exact in r.codes
steps=[d for d in r.details if 'reader-proof-disclosure' in d.get('class','').split()];assert len(steps)==7
assert all('open' not in d for d in r.details)
assert html.index('inline-lean-statement')<html.index('Full assumptions and notation')<html.index('1. Write the same quadratic')<html.index('inline-lean-proof')
text=' '.join(r.alltext)
for phrase in ('including either determinant sign','globally C∞','unique','fixed-input','joint','adaptive','worst-query caps','expected-cost','postmerge purification'):
 assert phrase in text,phrase
report={'renderer':'website/scripts/declaration_lessons.py:render_unit, actual unit, bounded current source inventory','selected_source_modules':[str(x.relative_to(ROOT)) for x in selected],'steps':len(steps),'all_details_initially_closed':True,'exact_statement_and_whole_declaration_in_code_panels':True,'statement_adjacent_before_assumption_fold':True,'full_proof_after_formula_steps':True,'scope_boundary_text_present':True,'fragment_sha256':h(html.encode()),'renderer_source_hashes':{str(p.relative_to(ROOT)):h(p.read_bytes()) for p in [ROOT/'tools/astis_site.py',ROOT/'website/scripts/inline_lean.py',ROOT/'website/scripts/declaration_lessons.py']},'not_checked':['browser','pixels','MathJax runtime','desktop/mobile','full-site navigation/link resolution','canonical root/site','Chrome','own-preview','remote delivery']}
(static/'static-reader-check.json').write_text(json.dumps(report,indent=2)+'\n')
(OUT/'input-preservation.json').write_text(json.dumps({'candidate_commit':head,'tracked_working_tree_and_index_clean':True,'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'packet_raw_sha256':'254984467d3b1937538be9ca9036e1f78e2c3dc75d4a53c1c1607fff47984311','packet_canonical_sha256':pkt['packet_sha256'],'publication_binding_sha256':pkt['publication_binding_sha256'],'inputs':records,'phase1_payloads_preserved':28,'phase2_payloads_preserved':25,'source_raw_sha256':h(sb)},indent=2)+'\n')
print(json.dumps({'candidate':head,'input_snapshots':len(records),'coverage_hash_matches':len(checks),'static_reader':report}))
