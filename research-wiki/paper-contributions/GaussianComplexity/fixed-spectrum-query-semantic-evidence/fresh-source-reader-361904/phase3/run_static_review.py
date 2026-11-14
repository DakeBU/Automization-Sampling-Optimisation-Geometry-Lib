from pathlib import Path
import gzip,hashlib,json,re,sys
from html.parser import HTMLParser
root=Path('/Users/zhouhuanjian/ASTIS-GC')
out=Path(__file__).resolve().parent
sys.path.insert(0,str(root));sys.path.insert(0,str(root/'tools'));sys.path.insert(0,str(root/'website/scripts'))
import astis_site,inline_lean,declaration_lessons
from tools import astis_publication,astis_semantic_roundtrip
H=lambda b:hashlib.sha256(b).hexdigest()
C=lambda o:json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def js(name,obj):(out/name).write_bytes((json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode())
def archive(name,data):
 z=gzip.compress(data,mtime=0);(out/name).write_bytes(z)
 return {'file':name,'bytes':len(data),'sha256':H(data),'gzip_sha256':H(z),'CRLF_count':data.count(b'\r\n'),'LF_count':data.count(b'\n'),'terminal_bytes_hex':data[-32:].hex()}
base=root/'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-query-semantic-evidence'
name='AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAffine.actual_affine_precision_query'
full=json.loads((base/'full-anti-anchored-reviewer-packet.json').read_bytes())
neutralraw=(root/'.astis/semantic-neutral-20261107/c7e2a049/input.json').read_bytes();copyraw=(base/'blind-906213/input.json').read_bytes();outputraw=(base/'blind-906213/output.json').read_bytes();runraw=(base/'blind-906213/run.json').read_bytes()
neutral=json.loads(neutralraw);decoder=json.loads(outputraw);run=json.loads(runraw);selective=json.loads((base/'phase2-selective-input.json').read_bytes());audit=json.loads((root/'research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-query.json').read_bytes())
assert neutralraw==copyraw and neutral==selective['anonymous_decoder_packet']
assert decoder==selective['blind_reconstruction']
assert H(neutralraw)=='458e60258ea72ccacc7e23144299a74e7a7c93cc97fbd2f2a5754d05d29bff9d'
assert H(outputraw)=='ad6a53e01c86639678a530621c85d2bc8cb53a6af0efe48337235b4bc0e7bc5d'
assert H(runraw)=='871c7bef0f2e3d57d6d10244e531fc4d0318b6935f62bf9eb6b4a9d86c8b9e3c'
assert H(C({k:v for k,v in neutral.items() if k!='packet_sha256'}))==neutral['packet_sha256']=='2dc3bb3323fa96592c235e4c218c09e247f62f899041a743e5824a6415836f45'
assert neutral['lean']['statement']==full['lean']['statement']==audit['lean']['statement']
assert neutral['lean']['approved_definition_context']==audit['lean']['decoder_context']
assert H(C(neutral['lean']['approved_definition_context']))==run['input']['approved_definition_context_canonical_json_sha256']=='b13b426a7e6a81c143b792c4dab4010954a0ad7af2937caa94505aab94927a2f'
assert H(decoder['reconstructed_theorem_text'].encode())==full['blind_reconstruction']['text_sha256']=='5361335a0c8bd0108137a8840760227ff719bcc71eefdd30daf7361a73261d35'
assert decoder['source_text_visible'] is False and run['isolation_and_exposure']['source_text_visible'] is False
assert run['isolation_and_exposure']['other_files_read_as_task_evidence']==[]
assert H(full['source']['original_text'].encode())==full['source']['text_sha256']
assert astis_semantic_roundtrip.semantic_reviewer_packet(audit)==full
for secret in ['Gaussian','arxiv','2610','FixedSpectrum','actual_affine','ASTIS-RT','repair']:
 # The packet has generic non-disclosure labels mentioning repair; scan meaning-bearing statement/context only.
 meaningful=neutral['lean']['statement']+'\n'+'\n'.join(neutral['lean']['approved_definition_context'])
 assert secret not in meaningful,secret
js('provenance-verification.json',{'status':'PASS','neutral_input_raw_sha256':H(neutralraw),'copy_raw_exact':True,'selective_packet_exact':True,'original_output_raw_sha256':H(outputraw),'original_run_raw_sha256':H(runraw),'statement_sha256':H(neutral['lean']['statement'].encode()),'definition_context_canonical_sha256':H(C(neutral['lean']['approved_definition_context'])),'canonical_anonymous_packet_sha256':neutral['packet_sha256'],'reconstruction_text_sha256':H(decoder['reconstructed_theorem_text'].encode()),'canonical_reviewer_packet_sha256':full['packet_sha256'],'full_packet_regenerated_exact_from_current_audit':True,'identity_separation':{'reviewer':'/root/reader_361904','formalizer':full['roles']['formalizer'],'decoder':decoder['decoder']},'blindness_evidence':'Neutral source-free locator and meaning-bearing statement/approved context checked; exact original run reports only neutral input read, no source/anchor/declaration/audit visible. This verifies the artifact chain and agent-observed exposure report, not independent OS isolation.'})
# Bind actual whole module and authored publication context with the standard publication API.
item=json.loads((root/'website/content/publications/huanjian-fixed-spectrum-query.json').read_bytes())['items'][0]
binding=item['bindings'][0]
actual_binding=astis_publication.binding_digest(item,binding)
context=astis_publication.review_context(item,binding)
assert actual_binding==full['publication_binding_sha256']=='fafc6866bd79667295b685939cb04e42374863753ab3e205c43ce6d0780e3970'
assert context==full['candidate_publication_context']
production=(root/full['lean']['file']).read_bytes()
assert H(production)==context['file']=='0a46e7bae8d8a9298ba3748a7c94db2f8874f1a4b318169a315c466d86b4a56c'
assert production==context['current_lean_module'].encode()
js('whole-publication-binding-check.json',{'status':'PASS','actual_binding_sha256':actual_binding,'exact_entire_production_sha256':H(production),'candidate_context_exact':True,'actual_audit_state_at_checked_commit':audit['state'],'checked_commit':'de220a52922fc2aa2c007ea14bf2c2949030b8d2','accepted_audit_bytes_in_checked_commit':False})
# Sanitize Lean comments and strings using the stock exact lexer, then inspect real code tokens.
scan=[]
for rel in [full['lean']['file'],'Tests/GaussianComplexityFixedSpectrumAffine.lean']:
 raw=(root/rel).read_bytes();clean=astis_site.sanitize_lean(raw.decode())
 bad={label:[m.start() for m in re.finditer(pattern,clean)] for label,pattern in {'sorry-or-admit':r'\b(?:sorry|admit|sorryAx)\b','axiom-declaration':r'^\s*axiom\s','unsafe-or-opaque':r'^\s*(?:unsafe|opaque)\s','Prop-true':r'Prop\s*:=\s*True','trivial-closure':r':=\s*(?:by\s+)?trivial\b'}.items()}
 assert not any(bad.values()),bad
 scan.append({'path':rel,'raw_sha256':H(raw),'sanitized_sha256':H(clean.encode()),'findings':bad})
js('sanitized-fake-closure-scan.json',{'status':'PASS','lexer':'tools.astis_site.sanitize_lean, comments/nested comments/strings removed with positions retained','files':scan,'proof_inspection':'Entire production theorem and entire actual consumer read. All arithmetic/matrix/vector bridges are proved internally; only source domain and O carrier are public premises. Fresh critical-axiom log separately has only propext, Classical.choice, Quot.sound and no sorryAx.'})
# Stock reader rendering and exact code extraction, without browser or full-site publication.
unit=json.loads((root/'website/content/declaration_lessons/huanjian-fixed-spectrum-query.json').read_bytes())['units'][0]
rel=declaration_lessons.lesson_path(name)
card=declaration_lessons.render_unit(unit,rel)
page=astis_site.page(unit['title'],rel,card,extra_head='<link rel="stylesheet" href="../assets/proof-readers.css">')
page_artifact=archive('static-stock-reader.html.gz',page.encode())
class CodeReader(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.details=[];self.role=None;self.code=False;self.buf=[];self.folds=[];self.open_folds=[];self.code_panels={}
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=='details':
   self.details.append((d,self.role));self.folds.append(d)
   if 'open' in d:self.open_folds.append(d)
   if d.get('data-inline-lean')==name:self.role='statement' if 'inline-lean-statement' in d.get('class','') else 'proof'
  if tag=='code' and self.role and d.get('class')=='language-lean':self.code=True;self.buf=[]
 def handle_endtag(self,tag):
  if tag=='code' and self.code:self.code_panels[self.role]=''.join(self.buf);self.code=False
  if tag=='details':
   _,previous=self.details.pop();self.role=previous
 def handle_data(self,data):
  if self.code:self.buf.append(data)
reader=CodeReader();reader.feed(card)
assert not reader.details and not reader.open_folds
assert set(reader.code_panels)=={'statement','proof'}
decl=inline_lean.declarations()[name]
exact=inline_lean.display_source(decl.source_text);signature,body=inline_lean.split_statement(exact)
assert reader.code_panels['proof']==exact and reader.code_panels['statement']==signature
# This production file uses LF. Stock scanning drops exactly the final LF from the declaration-to-EOF slice; the original file archive remains byte-exact.
start=production.index(b'theorem actual_affine_precision_query')
original_tail=production[start:]
assert original_tail.endswith(b'\n') and original_tail[:-1]==exact.encode()
assert body.startswith(':= by') and 'let θ' in signature and 'let A' in signature and 'let query' in signature
assert 'query 2 x = (κ - 1)⁻¹' in signature and '∀ x : EuclideanSpace' in signature
assert len(unit['steps'])==5 and unit['astis_dependencies']==[]
assert 'reader-first-pass' in card and 'assumption-ledger' in card and 'boundary-ledger' in card
assert len([x for x in reader.folds if 'proof-reader-step' in x.get('class','')])==5
assert all(s['formula'] and s['text'] for s in unit['steps'])
code_archives=[archive('static-extracted-statement.txt.gz',signature.encode()),archive('static-extracted-proof-and-context.txt.gz',exact.encode())]
js('static-reader-check.json',{'status':'PASS_STATIC_ONLY','stock_renderer':'website.scripts.declaration_lessons.render_unit + tools.astis_site.page; no copied renderer implementation','page_path':rel,'artifact':page_artifact,'complete_formula_steps':len(unit['steps']),'all_details_initially_closed':True,'first_pass_formula_and_statement_present':True,'all_domain_notation_boundary_disclosures_present':True,'exact_statement_code_matches_stock_split':True,'exact_proof_code_matches_original_module_slice':True,'raw_original_slice_byte_start':start,'raw_original_slice_removed_terminal_bytes_hex':'0a','stock_scanner_explanation':'The stock scanner omits the single terminal LF at declaration-to-EOF. No other character differs. Both the raw entire module and raw displayed code payloads are preserved. This is an explicitly recorded extraction convention, not silent normalization.','code_archives':code_archives,'ASTIS_parent_list':[],'actual_browser_or_layout_check':False,'full_root_site_build':False,'boundary':'Only stock static rendering and exact code extraction checked. Actual root/site/browser/remote/purification/ExpositionSeal remain separate.'})
# Exact byte excerpts of the meaning-carrying standard definitions and source boundaries.
spans=[]
for rel,first,last,label in [
('.lake/packages/mathlib/Mathlib/LinearAlgebra/UnitaryGroup.lean',50,82,'unitary-and-both-identities'),
('.lake/packages/mathlib/Mathlib/LinearAlgebra/UnitaryGroup.lean',285,304,'full-orthogonal-group'),
('.lake/packages/mathlib/Mathlib/Algebra/Star/Unitary.lean',52,65,'unitary-membership'),
('.lake/packages/mathlib/Mathlib/Data/Real/Star.lean',10,23,'real-trivial-star'),
('.lake/packages/mathlib/Mathlib/Algebra/Star/Basic.lean',390,401,'commutative-trivial-star'),
('.lake/packages/mathlib/Mathlib/LinearAlgebra/Matrix/ConjTranspose.lean',350,359,'real-star-transpose'),
('.lake/packages/mathlib/Mathlib/Analysis/Normed/Lp/WithLp.lean',45,80,'WithLp-literal-carrier'),
('.lake/packages/mathlib/Mathlib/Analysis/Normed/Lp/WithLp.lean',100,116,'WithLp-inverse-and-injective'),
('.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/PiL2.lean',106,115,'Euclidean-l2-carrier'),
('.lake/packages/mathlib/Mathlib/Analysis/Normed/Lp/PiLp.lean',83,94,'PiLp-WithLp-coordinates'),
('.lake/packages/mathlib/Mathlib/Data/Matrix/Diagonal.lean',40,60,'literal-diagonal'),
('.lake/packages/mathlib/Mathlib/Data/Matrix/Mul.lean',690,706,'actual-matrix-vector-product'),
('.lake/packages/mathlib/Mathlib/Data/Matrix/Mul.lean',812,824,'scalar-matvec'),
('.lake/packages/mathlib/Mathlib/Data/Matrix/Mul.lean',988,998,'identity-matvec'),
('.lake/packages/mathlib/Mathlib/Data/Matrix/Mul.lean',1059,1071,'subtraction-matvec'),
('.astis/huanjian-resume-20261103/2610.20492v1.html',635,706,'source-oracle-and-algorithm-context'),
('.astis/huanjian-resume-20261103/2610.20492v1.html',1038,1081,'visible-source-main-boundary-window'),
('.astis/huanjian-resume-20261103/2610.20492v1.html',1082,1127,'source-full-selected-hard-family-remark')]:
 raw=(root/rel).read_bytes();lines=raw.splitlines(keepends=True);start=sum(map(len,lines[:first-1]));end=sum(map(len,lines[:last]));data=raw[start:end]
 entry=archive('meaning-'+label+'.txt.gz',data);entry.update({'source_path':rel,'source_raw_sha256':H(raw),'line_first_inclusive':first,'line_last_inclusive':last,'byte_start_inclusive':start,'byte_end_exclusive':end});spans.append(entry)
js('meaning-and-source-excerpt-manifest.json',{'status':'PASS','policy':'Exact source bytes selected by keepends line spans, no whitespace/CRLF normalization; lossless gzip mtime=0.','spans':spans})
print(json.dumps({'status':'PASS','provenance':'all raw/canonical/context chain hashes verified','binding':actual_binding,'fake_closure_scan':'PASS','static_reader':'PASS_STATIC_ONLY','meaning_excerpts':len(spans),'source_main_boundary':'independently read fixed delta in (0,1), d>=d0(delta), 2<=kappa<=d^(1-delta), 0<epsilon<=1/10; not target premises or completion'},indent=2))
