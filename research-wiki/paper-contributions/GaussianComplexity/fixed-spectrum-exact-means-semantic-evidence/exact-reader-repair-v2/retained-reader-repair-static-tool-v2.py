from pathlib import Path
import sys,json,hashlib,re,html
sys.dont_write_bytecode=True;sys.path.insert(0,'website/scripts');sys.path.insert(0,'tools')
import declaration_lessons as dl
W=Path('.astis/huanjian-gc-fixed-spectrum-exact-means-20261110');out=W/'reader-repair-candidate-v2-render';assert not out.exists();out.mkdir()
p=W/'lesson-exact-step-code-candidate-v2.json';u=json.loads(p.read_bytes())['units'][0];name=u['declaration'];page=dl.lesson_path(name)
s=dl.render_unit(u,page)
assert not re.search(r'<details\b[^>]*\bopen(?:\s|=|>)',s)
assert s.count('<summary>Corresponding Lean step</summary>')==6
for step in u['steps']:
 assert '\n' in step['lean']
 assert html.escape(step['lean'],quote=True) in s or step['lean'] in html.unescape(s)
test=Path('Tests/GaussianComplexityFixedSpectrumExactMeans.lean').read_text();assert test in html.unescape(s)
expected=dl.source_link(u['sources'][-1],page);assert expected in html.unescape(s)
(out/'exact-lesson-fragment.html').write_text(s)
dl.export_sources(out,[u])
source=out/'data/lesson-sources/Tests/GaussianComplexityFixedSpectrumExactMeans.lean.html';assert source.is_file();ctx=html.unescape(source.read_text());assert 'private theorem actual_gaussian_closed_means_bias_ratio' in ctx
r={'scope':'Actual isolated static candidate render and exact Test module source export only; NOT canonical site build, browser/desktop/mobile, source acceptance or normalV.','candidate_lesson_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'six_corresponding_Lean_steps_are_literal_code':True,'full_exact_Test_source_adjacent_step6':True,'all_details_initially_closed':True,'Test_context_link':expected,'Test_context_export':str(source),'exact_lesson_fragment_sha256':hashlib.sha256(s.encode()).hexdigest(),'renderer_unchanged':True}
(out/'actual-static-check.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
