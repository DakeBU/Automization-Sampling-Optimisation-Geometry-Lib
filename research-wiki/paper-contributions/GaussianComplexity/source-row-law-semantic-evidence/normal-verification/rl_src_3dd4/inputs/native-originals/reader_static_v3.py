"""Actual production renderer, frozen exact candidate, bounded static HTML checks."""
import hashlib,html,json,pathlib,re,sys
from html.parser import HTMLParser
from run import ROOT,REPO,sha
sys.path[:0]=[str(REPO/'tools'),str(REPO/'website/scripts')]
import astis_site as base,declaration_lessons as lessons,inline_lean,astis_publication as pub
I=ROOT/'inputs';m=json.loads((ROOT/'input-manifest.json').read_text())
u=json.loads((I/'website/content/declaration_lessons/huanjian-gaussian-source-row-law.json').read_text())['units'][0]
item=json.loads((I/'website/content/publications/huanjian-gaussian-source-row-law.json').read_text())['items'][0]
base.ROOT=lessons.ROOT=pub.ROOT=I
base.project_lean_paths=lambda:[I/p for p in m['modules']]
mods,decls=base.scan_project_sources();known={d.full_name:d for d in decls}
base._SOURCE_BY_NAME=known;base._ALL_MODULES=mods;inline_lean.declarations.cache_clear()
base._ACTIVE_GIT=base.GitContext(commit=m['candidate_commit'],ref='independent-frozen-row-law-native',remote_url='',web_root='',commit_published=False,public_source_links=False,dirty_files=set())
base._ACTIVE_GATE=base.GateEvidence(passed=False,current=False,commit=m['candidate_commit'],source_digest='',generated_at='',commands=[],note='Bounded independent native proof evidence is separate; aggregate gate not asserted.')
binding=pub.binding_digest(item,item['bindings'][0],{'declarations':known,'lessons':{u['declaration']:u}})
assert binding=='f86fb828622e7c5c6e34ae2cb49dc1a6428d94701d36d7bb81a523861d48e419',binding
page='proofs/source-'+item['id']+'.html';body=lessons.render_unit(u,page)
out=ROOT/'reader';target=out/page;target.parent.mkdir(parents=True,exist_ok=True)
target.write_text(base.page(u['title'],page,body))
class Node:
    def __init__(self,tag,attrs,parent=None):self.tag=tag;self.attrs=dict(attrs);self.parent=parent;self.children=[];self.parts=[]
    def all(self,t):return ([self] if self.tag==t else [])+[z for c in self.children for z in c.all(t)]
    def text(self):return ''.join(p if isinstance(p,str) else p.text() for p in self.parts)
class Parse(HTMLParser):
    def __init__(self):super().__init__();self.root=Node('root',[]);self.stack=[self.root]
    def handle_starttag(self,t,a):
        n=Node(t,a,self.stack[-1]);self.stack[-1].children.append(n);self.stack[-1].parts.append(n)
        if t not in {'meta','link','br','hr','input','img','source','area','base','embed','param','track','wbr'}:self.stack.append(n)
    def handle_endtag(self,t):
        for i in range(len(self.stack)-1,0,-1):
            if self.stack[i].tag==t:self.stack=self.stack[:i];break
    def handle_data(self,d):self.stack[-1].parts.append(d)
p=Parse();p.feed(body)
assert all('open' not in n.attrs for n in p.root.all('details'))
steps=[n for n in p.root.all('details') if 'reader-proof-disclosure' in n.attrs.get('class','').split()]
assert len(steps)==6
receipts=[]
for i,(node,s) in enumerate(zip(steps,u['steps']),1):
    div=next(n for n in node.children if n.tag=='div');folds=div.all('details');assert len(folds)==1
    code=folds[0].all('code');assert len(code)==1 and code[0].text()==s['lean']
    assert div.children[0].tag=='p' and div.children[1].tag=='div' and div.children[2] is folds[0]
    assert div.children[0].text()==html.unescape(lessons.inline_text(s['text'])) and div.children[1].text()=='\\['+s['formula']+'\\]'
    owners=[f for f in m['modules'] if s['lean'] in (I/f).read_text()];assert len(owners)==1,(i,owners)
    raw=(I/owners[0]).read_text();pos=raw.index(s['lean'])
    receipts.append({'step':i,'file':owners[0],'start_line':raw[:pos].count('\n')+1,'lines':len(s['lean'].splitlines()),'sha256':sha(s['lean'].encode()),'exact_adjacent_formula_and_Lean':True,'initially_closed':True})
P=next(x for x in m['modules'] if x.endswith('/FixedSpectrumSourceRowLaw.lean'))
T=next(x for x in m['modules'] if x.startswith('Tests/'))
assert ''.join(s['lean'] for s in u['steps'][:2]) in (I/P).read_text()
assert '\n'.join(s['lean'] for s in u['steps'][2:])==(I/T).read_text()
assert len((I/T).read_text().splitlines())==145
consumer=next(d for d in decls if d.short_name=='actual_original_all_good_cutoff_probability');assert consumer.source_line==14
assert item['statement']==u['statement'] and item['assumptions']==u['assumptions']
assert item['formulae'][0]['tex']==u['formula'] and item['formulae'][1]['tex']==u['steps'][2]['formula']
assert u['astis_dependencies']==[] and 'no ASTIS theorem parent' in u['dependency_notes']
assert 'StdGaussianRadialExponential.integrable_exp_norm_sq_div_three_and_integral_stdGaussian' in u['dependency_notes']
assert 'MeasureTheory.integral_map' in u['mathlib_dependencies'] and 'requires no injectivity' in u['steps'][2]['text']
theme=(REPO/'_site/textbook/index.html').read_bytes();d=out/'textbook/index.html';d.parent.mkdir(exist_ok=True);d.write_bytes(theme)
(I/'theme-reference.html').write_bytes(theme)
lessons.export_sources(out,[u])
for mod in mods:
    path=out/'modules'/(base.slugify(mod.name)+'.html');path.parent.mkdir(exist_ok=True)
    path.write_text(base.render_source_module(mod,[]))
    download=out/'downloads/lean'/mod.source_file;download.parent.mkdir(parents=True,exist_ok=True);download.write_bytes((I/mod.source_file).read_bytes())
    mp=Parse();mp.feed(path.read_text());section=next(n for n in mp.root.all('section') if n.attrs.get('id')=='complete-module-source')
    assert section.all('code')[-1].text()==(I/mod.source_file).read_text()
links=[n.attrs.get('href','') for n in p.root.all('a')]
local=[x for x in links if 'data/lesson-sources/' in x];assert len(local)==1 and local[0].endswith('.lean.html#L14')
checked=[]
for l in [x for x in links if 'downloads/lean/' in x or 'modules/' in x or 'data/lesson-sources/' in x]:
    dest=(target.parent/l.split('#')[0]).resolve();assert dest.is_relative_to(out) and dest.exists(),l
    if '#' in l:assert 'id="'+l.split('#')[1]+'"' in dest.read_text(),l
    checked.append(l)
exports=out/'data/lesson-sources'/T;sp=Parse();sp.feed(exports.with_suffix('.lean.html').read_text())
numbered={n.attrs['id']:n for n in sp.root.all('span') if n.attrs.get('id','').startswith('L')}
assert len(numbered)==145 and numbered['L14'].text().startswith('private theorem actual_original_all_good_cutoff_probability')
assert '\n'.join(numbered['L'+str(i)].text() for i in range(1,146))+'\n'==(I/T).read_text()
runtime=[]
for filename in ['tools/astis_site.py','tools/astis_publication.py','website/scripts/declaration_lessons.py','website/scripts/inline_lean.py','website/scripts/source_lineage.py','website/scripts/library_shelves.py','website/scripts/formalization_progress.py']:
    b=(REPO/filename).read_bytes();d=ROOT/'runtime'/filename;d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(b)
    runtime.append({'path':filename,'sha256':sha(b)})
result={'candidate_commit':m['candidate_commit'],'binding_sha256':binding,'six_steps':receipts,'all_details_initially_closed':True,'private_consumer_full_module_exact_145_lines':True,'step_separator_blank_lines':[66,86,110],'private_source_link_line':14,'production_module_renderer_used':True,'local_links_and_anchors_checked':checked,'source_map_checked_separately':'locator-checks.json','all_formulas_present':True,'ASTIS_vs_Mathlib_dependency_distinction_present':True,'native_general_noninjective_integral_map_applicability_checked_separately':True,'production_runtime':runtime,'theme_reference_sha256':sha(theme),'page':str(target.relative_to(ROOT)),'page_sha256':sha(target.read_bytes()),'scope':'Actual production render_unit, export_sources, render_source_module on exact frozen bounded candidate; static output and anchors only.','HOLD':['browser desktop/mobile','MathJax rendered layout','clipboard runtime','interactive download runtime','fullsite/globalgraph','root Tests and fullrepo gates','public publication/integration','source-fidelity verdict','purification']}
(ROOT/'reader-static.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
