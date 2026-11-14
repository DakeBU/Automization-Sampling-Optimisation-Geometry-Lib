from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,shutil,sys

ROOT=Path('/Users/zhouhuanjian/ASTIS-GC')
OUT=ROOT/'.astis/semantic-neutral-20261108/src_4e8f6a/phase3'
READER=OUT/'reader'
sys.path.insert(0,str(ROOT/'tools'))
sys.path.insert(0,str(ROOT/'website/scripts'))
import astis_site as base
import inline_lean
import declaration_lessons

REL_FILES=[
 'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumFirstOrder.lean',
 'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumAdmissibility.lean',
 'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumAffine.lean',
 'Tests/GaussianComplexityFixedSpectrumFirstOrder.lean']
base.project_lean_paths=lambda:[ROOT/p for p in REL_FILES]
modules,declarations=base.scan_project_sources()
base._SOURCE_BY_NAME={d.full_name:d for d in declarations}
inline_lean.declarations.cache_clear()
base._ACTIVE_GIT=base.GitContext(
 commit='9d306d837fbddf1518b0035494baaf5c21c24488',
 ref='source-review-only',remote_url='',web_root='',commit_published=False,
 public_source_links=False,dirty_files=set())
lesson_path=ROOT/'website/content/declaration_lessons/huanjian-fixed-spectrum-first-order.json'
unit=json.loads(lesson_path.read_text())['units'][0]
rendered=declaration_lessons.render_unit(unit,'index.html')

assets=READER/'assets';assets.mkdir(parents=True,exist_ok=True)
styles=['site.css','proof-readers.css','reader-contract-final.css','textbook-math-contract.css']
scripts=['math-reader.js','site.js']
for name in styles+scripts:
 shutil.copyfile(ROOT/'website/static'/name,assets/name)
shutil.copytree(ROOT/'website/static/vendor/mathjax@3.2.2',assets/'vendor/mathjax@3.2.2',dirs_exist_ok=True)

def shell(title,body,prefix=''):
 return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+base.esc(title)+'</title>'+''.join('<link rel="stylesheet" href="'+prefix+'assets/'+s+'">' for s in styles)+r'''
<style>body{margin:0;background:#f5f7fb;color:#17243a}main{max-width:1100px;margin:auto;padding:24px 28px 80px}.review-only{padding:14px 18px;background:#fff4cf;border:1px solid #d6ad32;border-radius:8px;margin-bottom:24px}.code-block{overflow:auto}.reader-main-equation{font-size:1.12rem}.module-links a{margin-right:1rem}details{margin-bottom:12px}pre code .line{display:block}a{overflow-wrap:anywhere}</style>
<script>window.MathJax={tex:{inlineMath:[['\\(','\\)']],displayMath:[['\\[','\\]']]},options:{skipHtmlTags:['script','noscript','style','textarea','pre','code']}};</script>
'''+f'<script src="{prefix}assets/math-reader.js"></script><script defer src="{prefix}assets/vendor/mathjax@3.2.2/tex-mml-chtml.js"></script><script defer src="{prefix}assets/site.js"></script></head><body><main id="content"><div class="review-only"><strong>Independent source review only</strong><br>Owned static artifact for immutable candidate 9d306d837fbddf1518b0035494baaf5c21c24488. This is not current canonical rootGate, deployed site, Chrome acceptance or publication approval.</div>'+body+'</main></body></html>'

(READER/'index.html').write_text(shell(unit['title'],rendered))
downloads=[];source_pages=[]
for module in modules:
 raw=(ROOT/module.source_file).read_bytes()
 download=READER/'downloads/lean'/module.source_file
 download.parent.mkdir(parents=True,exist_ok=True);download.write_bytes(raw)
 rel='modules/'+base.slugify(module.name)+'.html'
 page=READER/rel;page.parent.mkdir(parents=True,exist_ok=True)
 exact=raw.decode()
 anchors=''.join('<span id="'+base.esc(d.anchor)+'"></span>' for d in module.declarations)
 content='<p><a href="../index.html">Return to owned mathematical lesson</a></p><h1>'+base.esc(module.name)+'</h1><p>Exact complete checkout bytes; no code truncation.</p><p><a href="../downloads/lean/'+base.esc(module.source_file)+'" download>Download exact module (.lean)</a></p>'+anchors+'<pre class="code-block" id="complete-module-source"><code>'+base.esc(exact)+'</code></pre>'
 page.write_text(shell('Exact module source',content,'../'))
 downloads.append({'source_file':module.source_file,'download':download.relative_to(READER).as_posix(),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
 source_pages.append(rel)
target=base._SOURCE_BY_NAME[unit['declaration']]
exact_decl=inline_lean.display_source(target.source_text)
signature,body=inline_lean.split_statement(exact_decl)
assert body and signature.count('let ')==4
assert 'HasGradientAt f (query x) x' in signature
assert 'gradient f x' in signature
assert 'have hgrad' in exact_decl and 'hg.gradient' in exact_decl

class Parse(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True);self.details=[];self.pres=[];self.in_pre=False;self.current=''
 def handle_starttag(self,tag,attrs):
  if tag=='details':self.details.append(dict(attrs))
  if tag=='pre':self.in_pre=True;self.current=''
 def handle_endtag(self,tag):
  if tag=='pre':self.pres.append(self.current);self.in_pre=False
 def handle_data(self,data):
  if self.in_pre:self.current+=data
parser=Parse();parser.feed(rendered)
assert all('open' not in d for d in parser.details)
assert signature in parser.pres
assert exact_decl in parser.pres
scan=[]
for rel in REL_FILES:
 clean=base.sanitize_lean((ROOT/rel).read_text())
 bad=[]
 import re
 for pattern in [r'\b(?:sorry|admit|sorryAx|native_decide)\b',r'(?m)^\s*(?:private\s+)?axiom\b',r'Prop\s*:=\s*True\b',r':=\s*trivial\b']:
  bad.extend(m.group() for m in re.finditer(pattern,clean))
 assert not bad,(rel,bad)
 scan.append({'file':rel,'matches':bad})
(OUT/'focused_fake_closure_receipt.json').write_text(json.dumps({
 'kind':'Focused comment/string-stripped source scan plus independent fresh kernel axiom checks',
 'files':scan,'scan_passed':True,'kernel_evidence':'kernel_application_receipt.json and logs/IndependentKernelApplication.log',
 'limit':'This scan is bounded to actual producer, Test and critical actual ancestors. It is not a whole-repository or deployed-site gate.'
},indent=2)+'\n')
(OUT/'owned_reader_build_receipt.json').write_text(json.dumps({
 'checked_candidate_commit':'9d306d837fbddf1518b0035494baaf5c21c24488',
 'official_lesson':str(lesson_path.relative_to(ROOT)),
 'official_lesson_raw_sha256':hashlib.sha256(lesson_path.read_bytes()).hexdigest(),
 'renderer':'declaration_lessons.render_unit + inline_lean actual source extraction',
 'source_scan_scope':REL_FILES,
 'scope':'Owned source-review-only static reader; no stale _site, gate/status data, current delivery or Chrome acceptance used.',
 'default_details_count':len(parser.details),'all_details_initially_closed':True,
 'exact_adjacent_statement_preserved':True,'exact_adjacent_proof_preserved':True,
 'display_signature_sha256':hashlib.sha256(signature.encode()).hexdigest(),
 'display_declaration_sha256':hashlib.sha256(exact_decl.encode()).hexdigest(),
 'formula_text':'Official lesson text unchanged; standard current math-reader.js and local MathJax copied without custom TeX corrections.',
 'source_pages':source_pages,'downloads':downloads,
 'reader_entry':'reader/index.html'
},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'reader':str(READER/'index.html'),'default_closed_details':len(parser.details),'exact_statement_and_proof':True,'downloads':len(downloads),'fake_closure_scan':'passed'},indent=2))
