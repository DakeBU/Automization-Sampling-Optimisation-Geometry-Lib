from pathlib import Path
import sys,json,hashlib,re,html
sys.dont_write_bytecode=True;sys.path.insert(0,'website/scripts');sys.path.insert(0,'tools')
import declaration_lessons as dl
W=Path('.astis/huanjian-gc-fixed-spectrum-cosine-gram-20261110')
out=W/'isolated-static-reader-current';assert not out.exists();out.mkdir()
p=Path('website/content/declaration_lessons/huanjian-fixed-spectrum-cosine-gram.json')
u=json.loads(p.read_bytes())['units'][0];page=dl.lesson_path(u['declaration'])
s=dl.render_unit(u,page)
assert not re.search(r'<details\b[^>]*\bopen(?:\s|=|>)',s)
assert s.count('<summary>Corresponding Lean step</summary>')==6
for step in u['steps']:
    assert '\n' in step['lean'] and step['lean'] in html.unescape(s)
T=Path('Tests/GaussianComplexityFixedSpectrumCosineGram.lean');raw=T.read_bytes();test=raw.decode()
assert u['steps'][-1]['lean']==test and test in html.unescape(s)
ref=next(x for x in u['sources'] if x.get('path')==str(T));expected=dl.source_link(ref,page)
assert expected in html.unescape(s)
(out/'exact-lesson-fragment.html').write_text(s)
theme=Path('_site/textbook/index.html');theme_bytes=theme.read_bytes()
(out/'textbook').mkdir();(out/'textbook/index.html').write_bytes(theme_bytes)
dl.export_sources(out,[u])
source=out/'data/lesson-sources'/str(T)
source=source.with_suffix(source.suffix+'.html')
ctx=html.unescape(source.read_text());line=ref['line']
assert 'private theorem actual_gaussian_gram_means' in ctx
assert f'id="L{line}"' in ctx
assert test.splitlines()[line-1].startswith('private theorem actual_gaussian_gram_means')
assert 'complete_lean_step_actions' not in Path('website/scripts/declaration_lessons.py').read_text()
r={'scope':'Isolated unchanged production renderer, literal-code and exact Test source context checks only. No browser/pixel/MathJax/desktop/mobile, full-site, source-index/graph, sourceV/global or Goal acceptance.','candidate_lesson_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'six_literal_Lean_code_steps':True,'complete_Test_bytes_in_step6':len(raw),'Test_raw_sha256':hashlib.sha256(raw).hexdigest(),'all_details_initially_closed':True,'actual_Test_statement_line':line,'Test_context_link':expected,'Test_context_export':str(source),'exact_lesson_fragment_sha256':hashlib.sha256(s.encode()).hexdigest(),'renderer_unchanged':True,'reader_neighbor_delivery':'HOLD: legacy production render_unit has no per-step source/download actions; privateT citation is in later Sources fold. The independently reviewed ZeroQuery v3 renderer proposal is disabled and has not been applied. No current delivery HOLD is removed.','reused_theme_fixture':{'path':str(theme),'sha256':hashlib.sha256(theme_bytes).hexdigest(),'scope':'Old canonical theme fixture only, not a new mathematical page/site build.'}}
(out/'actual-static-check.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r))
