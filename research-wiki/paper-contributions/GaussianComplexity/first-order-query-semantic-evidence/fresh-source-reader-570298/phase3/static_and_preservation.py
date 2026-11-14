from pathlib import Path
import gzip,hashlib,json,re,subprocess,sys
from bs4 import BeautifulSoup
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC')
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'));sys.path.insert(0,str(ROOT/'website/scripts'))
import astis_advance as advance
import astis_site as site
import astis_publication as publication
import declaration_lessons,publication_reader,inline_lean

def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def dump(name,v):(OUT/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
TARGET='ASTIS-SA-20261107-GaussianComplexityFirstOrderQuery'
NAME='AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderQuery.actual_first_order_query'
base=ROOT/'research-wiki/paper-contributions/GaussianComplexity/first-order-query-semantic-evidence'
packet=json.loads((base/'full-anti-anchored-reviewer-packet.json').read_bytes())
selective=json.loads((base/'phase2-selective-input.json').read_bytes())
decoder_raw=(base/'decoder-input.json').read_bytes();decoder=json.loads(decoder_raw)
assert decoder==selective['anonymous_decoder_packet']
assert decoder['lean']['statement']==packet['lean']['statement']
assert packet['blind_reconstruction']['text']==selective['blind_reconstruction']['reconstructed_theorem_text']
assert sha(canonical({k:v for k,v in decoder.items() if k!='packet_sha256'}))==decoder['packet_sha256']
assert sha(canonical({k:v for k,v in packet.items() if k!='packet_sha256'}))==packet['packet_sha256']
assert packet['roles']['formalizer']!=packet['roles']['blind_decoder']!='/root/reader_570298'
snap=OUT/'input-snapshots';snap.mkdir(exist_ok=True)
paths=[
'AutoSamplingTheory/ExampleCases/GaussianComplexity/FirstOrderQuery.lean',
'Tests/GaussianComplexityFirstOrderQuery.lean',
'AutoSamplingTheory/ExampleCases/GaussianComplexity/BlockFamily.lean',
'AutoSamplingTheory/ExampleCases/GaussianComplexity/DeterminantFamily.lean',
'website/content/declaration_lessons/huanjian-first-order-query.json',
'website/content/publications/huanjian-first-order-query.json',
'research-wiki/semantic-roundtrip/audits/huanjian-first-order-query.json',
'lean-toolchain','lake-manifest.json',
str((base/'full-anti-anchored-reviewer-packet.json').relative_to(ROOT)),
str((base/'decoder-input.json').relative_to(ROOT)),
]
records=[]
for i,name in enumerate(paths):
 b=(ROOT/name).read_bytes(); saved=f'{i:02d}-{Path(name).name}'
 assert not (snap/saved).exists()
 (snap/saved).write_bytes(b)
 tree=subprocess.check_output(['git','show','214b6214c5b08bd52b6faa59a3ccd6ca35998420:'+name],cwd=ROOT)
 assert b==tree,name
 records.append({'path':name,'snapshot':'input-snapshots/'+saved,'bytes':len(b),'sha256':sha(b),'equal_to_214b_tree':True})
data=publication.inputs();items=publication.load()
item=next(i for i in items if i['id']=='huanjian-first-order-query')
binding=item['bindings'][0];unit=data['lessons'][NAME]
assert publication.binding_digest(item,binding,data)==packet['publication_binding_sha256']
assert publication.review_context(item,binding,data)==packet['candidate_publication_context']
assert packet['candidate_publication_context']['current_lean_module']==(ROOT/packet['lean']['file']).read_text()
dump('input-pins-and-chain.json',{'checked_commit':'214b6214c5b08bd52b6faa59a3ccd6ca35998420',
 'files':records,'decoder_full_raw_sha256':sha(decoder_raw),'decoder_equals_frozen_selective_packet':True,
 'actual_approved_context_equals_phase2':True,'anonymous_statement_unchanged':True,'blind_reconstruction_unchanged':True,
 'canonical_full_packet_sha256':packet['packet_sha256'],'publication_binding_sha256':packet['publication_binding_sha256'],
 'live_publication_context_equals_packet':True,'audit_tree_state_before_review':data['audits']['ASTIS-RT-20261107-HuanjianFirstOrderQuery']['state']})

# Byte- and state-level preservation baseline. Foreign content is not rendered or interpreted.
ledger=advance.DEFAULT_ADVANCE_LEDGER.read_bytes()
(OUT/'advance-ledger-before.exact.jsonl.gz').write_bytes(gzip.compress(ledger,mtime=0))
states=advance.current_advances();foreign={k:v for k,v in states.items() if k!=TARGET}
assert len(foreign)==279 and states[TARGET]['state']=='PROVED_LOCAL'
assert states[TARGET]['owner_id']=='huanjian_gc_20261107_first_order_query'
discovery=advance.DEFAULT_DISCOVERY_LEDGER.read_bytes()
frontiers={str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in sorted((ROOT/'research-wiki/frontier-cells').glob('*.json'))}
audits={str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in sorted((ROOT/'research-wiki/semantic-roundtrip/audits').glob('*.json'))}
dump('preservation-before.json',{'advance_ledger_bytes':len(ledger),'advance_ledger_sha256':sha(ledger),
 'advance_ledger_exact_snapshot':'advance-ledger-before.exact.jsonl.gz','target_before':states[TARGET],
 'foreign_advance_count':len(foreign),'foreign_states_sha256':sha(canonical(foreign)),
 'discovery_ledger_bytes':len(discovery),'discovery_ledger_sha256':sha(discovery),
 'frontier_hashes':frontiers,'audit_fragment_hashes':audits,
 'registry_sha256':sha((ROOT/'research-wiki/semantic-roundtrip/registry.json').read_bytes())})

# Sanitized scans include the complete changed production/Test and actual ASTIS ancestry.
lean_paths=paths[:4]
hits=[];sanitized=[]
pattern=re.compile(r'\b(?:sorry|admit|axiom|sorryAx)\b|\bProp\s*:=\s*True\b|:=\s*trivial\b')
for name in lean_paths:
 raw=(ROOT/name).read_bytes();clean=site.sanitize_lean(raw.decode())
 for m in pattern.finditer(clean):hits.append({'file':name,'line':clean.count('\n',0,m.start())+1,'token':m.group()})
 sanitized.append({'path':name,'raw_sha256':sha(raw),'sanitized_sha256':sha(clean.encode()),
 'imports':re.findall(r'^import\s+([^\s]+)',clean,re.M)})
assert not hits,hits
dump('sanitized-fake-closure-scan.json',{'status':'PASS','method':'Actual astis_site.sanitize_lean strips comments/strings; scan declaration/proof text for sorry, admit, axiom, sorryAx, Prop := True and := trivial; combine with fresh compiler #print axioms in direct checks.','files':sanitized,'hits':hits,
 'scope':'Whole target/Test plus all two ASTIS ancestor modules; not a source-fidelity proof by itself.'})
relevant={'AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily.singleBlockPrecision',
 'AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily.singleBlockPrecision_regular',
 'AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily.blockPrecision',
 'AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily.blockPrecision_regular',NAME}
mapped=[]
for i in items:
 bs=[b for b in i['bindings'] if b['declaration'] in relevant]
 if bs:mapped.append({'source_item':i['id'],'source':i['source'],'bindings':[{'declaration':b['declaration'],'role':b['role'],'supports':b['supports'],'cell':b['cell']} for b in bs]})
dump('bounded-source-ancestry.json',{'nodes':sorted(relevant),'mapped_source_items':mapped,
 'ancestry_review':'FirstOrderQuery imports canonical BlockFamily, which imports canonical DeterminantFamily. Read complete bodies. Source literal definitions agree with E4/E5; regularity reaches source B.3 through the existing single/block nodes. No private duplicate precision/regularity theorem or convenience premise was introduced.',
 'source_vs_ingredient':'Only hn,hnd,hκ and actual orthogonal tuple are public premises. blockPrecision_regular is called inside proof and only its symmetry component is consumed. Matvec, derivative and coordinate identities are proved internally.'})

# Render only the exact target through the stock publication/lesson/inline-Lean renderer.
# This is a bounded static reader, not canonical site generation or browser QA.
rel='proofs/source-huanjian-first-order-query.html'
html=site.page('Actual first-order query reconstruction',rel,publication_reader.source_card(item,rel))
static=OUT/'static-reader';(static/'proofs').mkdir(parents=True,exist_ok=True)
(static/rel).write_text(html)
source=(ROOT/packet['lean']['file']).read_bytes()
(static/'FirstOrderQuery.exact.lean').write_bytes(source)
doc=BeautifulSoup(html,'html.parser')
article=doc.find('article',attrs={'data-authored-declaration':NAME});assert article is not None
first=article.find('section',class_='reader-first-pass');assert first
assert 'Exact forward and inverse block products' in first.get_text()
assert len(first.select('.reader-main-equation'))==1
assumptions=article.find('details',class_='assumption-ledger');assert assumptions and not assumptions.has_attr('open')
for text in ['k=','r=','A=','primitive oracle','g_j','zero']:
 assert text in assumptions.get_text(),text
panels=article.find_all('details',attrs={'data-inline-lean':NAME});assert len(panels)==2
assert all(not p.has_attr('open') for p in panels)
decl=inline_lean.declarations()[NAME]
exact=inline_lean.display_source(decl.source_text)
signature,_=inline_lean.split_statement(exact)
proof_panel=next(p for p in panels if 'inline-lean-proof' in p['class'])
statement_panel=next(p for p in panels if 'inline-lean-statement' in p['class'])
proof_text=proof_panel.find('code').get_text();statement_text=statement_panel.find('code').get_text()
assert proof_text==exact
assert statement_text==signature
assert exact in source.decode()
assert len(article.select('.reader-proof-disclosure'))==5
assert all(not p.has_attr('open') for p in article.select('.reader-proof-disclosure'))
assert 'Finite-horizon adaptive simulation' in article.get_text()
for dep in ['blockPrecision_regular','singleBlockPrecision','Matrix.inner_toEuclideanCLM','HasFDerivAt.inner']:
 assert dep in article.get_text(),dep
dump('static-reader-review.json',{'status':'PASS','method':'Stock astis_site.page + publication_reader.source_card + declaration_lessons/inline_lean; parsed actual rendered HTML with BeautifulSoup; independently inspected attributed statement/conditions and all five authored formula-proof steps against exact source and actual proof.',
 'rendered_path':str((static/rel).relative_to(ROOT)),'html_bytes':len(html.encode()),'html_sha256':sha(html.encode()),
 'exact_module_copy':str((static/'FirstOrderQuery.exact.lean').relative_to(ROOT)),'exact_module_copy_sha256':sha(source),
 'first_pass':'Single observation equation and concise claim; complete actual objects/query/g definitions are in folded assumptions and notation.',
 'exact_statement_equals_stock_source_split':True,'exact_proof_equals_complete_scanned_declaration':True,
 'whole_module_context_matches_checked_commit':True,'lean_panels_initially_closed':True,
 'formula_steps_count':5,'all_formula_steps_initially_closed':True,'source_attribution_and_boundary_visible_in_stock_reader':True,
 'review_limit':'Static rendered reader and exact extraction only. No actual HTTP/Chrome, mobile, visual or canonical-site/root integration acceptance is claimed. Status is pre-review blind-reconstructed, as correctly present in the checked 214b tree.'})
print('PASS input chain, publication binding, preservation baseline (279 foreign advances), whole-file sanitized scan, bounded ancestry, stock static reader and exact extraction.')
