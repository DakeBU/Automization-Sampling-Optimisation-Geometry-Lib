from bootstrap import *
import re, html
from html.parser import HTMLParser
sys.path[:0]=[str(SNAP/'tools'),str(SNAP/'website/scripts')]
import astis_site as site
import astis_publication as publication
import declaration_lessons as lessons
import publication_reader
import inline_lean
import astis

site._ACTIVE_GIT=site.GitContext(CAND,'immutable independent bounded snapshot','','',False,False,set())
site._ACTIVE_GATE=site.GateEvidence(False,False,CAND,'','',[], 'Bounded native compilation is separately evidenced; aggregate project gate not run.')
mods,decls=site.scan_project_sources()
site._ALL_MODULES=mods
known={d.full_name:d for d in decls};site._SOURCE_BY_NAME=known
unit=json.loads((SNAP/LESSON).read_bytes())['units'][0]
item=json.loads((SNAP/PUB).read_bytes())['items'][0]
data={'declarations':known,'lessons':{unit['declaration']:unit},'cells':{},'audits':{}}
binding=publication.binding_digest(item,item['bindings'][0],data)
assert binding=='128fff581c818c13f03d208c546c685e910ade6a30a202e7bee34ce60aa79179',binding
# Supply the bounded candidate records to the unchanged production renderer.
# No review reports/registry are loaded, and no status is synthesized as verified.
publication.inputs=lambda:data
out=ROOT/'bounded-render'
page=publication_reader.source_proof_path(item)
body=publication_reader.source_card(item,page)
dest=out/page;dest.parent.mkdir(parents=True,exist_ok=True)
dest.write_text(site.page(item['title'],page,body))
lessonpage=lessons.lesson_path(unit['declaration'])
dest=out/lessonpage;dest.parent.mkdir(parents=True,exist_ok=True)
dest.write_text(site.page(unit['title'],lessonpage,lessons.render_unit(unit,lessonpage)))
lessons.export_sources(out,[unit])
for mod in mods:
 dest=out/('modules/'+site.slugify(mod.name)+'.html');dest.parent.mkdir(parents=True,exist_ok=True)
 dest.write_text(site.render_source_module(mod,[m.name for m in mods if mod.name in m.imports]))

class Node:
 def __init__(self,tag='',attrs=None,parent=None):self.tag=tag;self.attrs=dict(attrs or []);self.parent=parent;self.children=[];self.parts=[]
 def text(self): return ''.join(x.text() if isinstance(x,Node) else x for x in self.parts)
 def find(self,tag=None,cls=None):
  result=[]
  for c in self.children:
   if (tag is None or c.tag==tag) and (cls is None or cls in c.attrs.get('class','').split()):result.append(c)
   result.extend(c.find(tag,cls))
  return result
class Tree(HTMLParser):
 void={'meta','link','input','br','hr','img','source','area','base','embed','param','track','wbr','col'}
 def __init__(self,text):super().__init__(convert_charrefs=True);self.root=Node();self.stack=[self.root];self.feed(text)
 def handle_starttag(self,tag,attrs):
  n=Node(tag,attrs,self.stack[-1]);self.stack[-1].children.append(n);self.stack[-1].parts.append(n)
  if tag not in self.void:self.stack.append(n)
 def handle_endtag(self,tag):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i].tag==tag:self.stack=self.stack[:i];break
 def handle_data(self,s):self.stack[-1].parts.append(s)

tree=Tree(body);steps=tree.root.find('details','proof-reader-step')
assert len(steps)==5
ranges=[(P,35,78),(P,80,103),(P,105,188),(T,1,101),(T,103,160)]
checks=[]
for k,(step,(p,a,b)) in enumerate(zip(steps,ranges),1):
 assert 'open' not in step.attrs
 folds=step.find('details');assert len(folds)==1 and 'open' not in folds[0].attrs
 codes=folds[0].find('code');assert len(codes)==1
 expected=''.join((SNAP/p).read_text().splitlines(keepends=True)[a-1:b])
 actual=codes[0].text()
 assert actual==expected,(k,len(actual),len(expected))
 assert unit['steps'][k-1]['formula'] in step.text()
 checks.append({'step':k,'source_file':p,'lines_1based':[a,b],'exact_bytes':len(actual.encode()),'exact_sha256':sha(actual.encode()),'closed':True})
for a in unit['assumptions']:assert lessons._canonical_prose(a) in lessons._authored_prose_text(body)
for f in item['formulae']:assert f['tex'] in tree.root.text()
for s in unit['steps']:assert s['formula'] in tree.root.text()
assert len(tree.root.find('article','proof-reader'))==1
assert all('open' not in n.attrs for n in tree.root.find('details'))
sourcepage=out/'data/lesson-sources'/f'{T}.html'
source_tree=Tree(sourcepage.read_text())
source_lines={n.attrs['id']:n.text() for n in source_tree.root.find('span') if n.attrs.get('id','').startswith('L')}
for i,line in enumerate((SNAP/T).read_text().splitlines(),1):assert source_lines[f'L{i}']==line
assert source_lines['L14'].startswith('private theorem actual_truncated_summand_second_moment_bound')
source_links=[n.attrs.get('href') for n in tree.root.find('a')]
assert '../data/lesson-sources/'+T+'.html#L14' in source_links
for d in decls:
 target,lab=site.source_href(d,from_path=page)
 assert target.endswith('#complete-module-source')
 assert (out/pathlib.Path(page).parent/pathlib.Path(target.split('#')[0])).resolve().is_file()
hits=astis.forbidden_pattern_hits();assert not hits,hits
save(ROOT/'bounded-static-reader.json',{'candidate':CAND,'binding_sha256':binding,'production_entrypoints':['publication_reader.source_card','declaration_lessons.render_unit','inline_lean.disclosure','declaration_lessons.export_sources','astis_site.render_source_module','astis_site.page'],'runtime_policy':'Unchanged candidate production renderer source; only bounded candidate input records injected in publication.inputs; absent cells/audits remain pending. No whole-site or browser claim.','publication_page':str((out/page).relative_to(ROOT)),'lesson_page':str((out/lessonpage).relative_to(ROOT)),'source_adjacent_folds':checks,'private_source_L14':{'path':str(sourcepage.relative_to(ROOT)),'all_160_lines_exact':True,'L14':source_lines['L14']},'all_formulae_and_assumption_text_present':True,'all_details_initially_closed':True,'source_context_navigation_targets_exist':True,'fake_closure_production_scanner_hits':hits,'static_acceptance':'ACCEPT bounded immutable lesson/publication rendering','HOLD':['actual desktop browser','actual mobile browser','full-source-index integration','graph integration and visual graph inspection','actual clipboard copy','actual download operation','public URL/site integration','aggregate repository gate','serialized integration','post-merge purification']})

# Independently recompute character, byte and line locations from raw HTML.
raw=(ROOT/'local-private/source-original.html').read_bytes();text=raw.decode()
class SourceNodes(HTMLParser):
 def __init__(self,t):
  super().__init__(convert_charrefs=False);self.t=t;self.starts=[0]+[m.end() for m in re.finditer('\n',t)];self.stack=[];self.nodes={};self.feed(t)
 def pos(self):l,c=self.getpos();return self.starts[l-1]+c
 def handle_starttag(self,tag,attrs):
  if tag in Tree.void:return
  self.stack.append((tag,dict(attrs).get('id'),self.pos()))
 def handle_startendtag(self,tag,attrs):
  ident=dict(attrs).get('id')
  if ident:self.nodes[ident]=(self.pos(),self.pos()+len(self.get_starttag_text()))
 def handle_endtag(self,tag):
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i][0]==tag:
    for _,ident,start in self.stack[i:]:
     if ident:self.nodes[ident]=(start,self.t.index('>',self.pos())+1)
    self.stack=self.stack[:i];break
source_nodes=SourceNodes(text).nodes
mapdata=json.loads((SNAP/MAP).read_text());seal=json.loads((SNAP/SEAL).read_text())
mapchecks=[]
def source_check(s):
 a,b=source_nodes[s['source_id']]
 assert [a,b]==[s['char_start'],s['char_end']],s['source_id']
 assert [len(text[:a].encode()),len(text[:b].encode())]==[s['raw_utf8_start'],s['raw_utf8_end']]
 assert text.count('\n',0,a)+1==s['lf_line_start']
 assert text.count('\n',0,b-1)+1==s['lf_line_end']
 assert a-(text.rfind('\n',0,a)+1)==s['lf_column0_start']
 assert sha(text[a:b].encode())==s['span_sha256']
 mapchecks.append({'kind':'source','id':s['source_id'],'char_span':[a,b],'bytes':len(text[a:b].encode()),'sha256':s['span_sha256']})
def lean_check(s):
 p=SNAP/s['path'] if not s['path'].startswith('.lake/') else REPO/s['path']
 raw=p.read_bytes();txt=raw.decode();a,b=s['decoded_char_span'];lo,hi=s['LF_lines_1based']
 assert sha(raw)==s['file_sha256'],s['path']
 selected=''.join(txt.splitlines(keepends=True)[lo-1:hi])
 assert selected==txt[a:b],(s['path'],lo,hi)
 assert [len(txt[:a].encode()),len(txt[:b].encode())]==s['raw_UTF8_byte_span']
 assert sha(selected.encode())==s['span_sha256']
 mapchecks.append({'kind':'lean','path':s['path'],'lines':[lo,hi],'bytes':len(selected.encode()),'sha256':s['span_sha256']})
for row in mapdata['mappings']:
 for s in row['source']:source_check(s)
 for s in row['lean']:lean_check(s)
for row in mapdata['proof_background']:
 lean_check(row['source']);lean_check(row['consumer'])
for s in seal['source']['anchors']:
 a,b=source_nodes[s['source_id']]
 assert [a,b]==s['char_span'] and sha(text[a:b].encode())==s['span_sha256'],s['source_id']
 assert [len(text[:a].encode()),len(text[:b].encode())]==s['UTF8_byte_span']
 assert [text.count('\n',0,a)+1,text.count('\n',0,b-1)+1]==s['LF_lines_1based']
save(ROOT/'source-lean-map-independent-check.json',{'candidate':CAND,'map_sha256':sha((SNAP/MAP).read_bytes()),'raw_source_bytes':len(raw),'source_html_bytes':len((ROOT/'local-private/source-original.html').read_bytes()),'source_html_sha256':sha((ROOT/'local-private/source-original.html').read_bytes()),'checks':mapchecks,'all_17_seal_anchor_locations_checked':True,'status':'all map and seal offsets, lines, bytes and hashes independently recomputed'})
from bs4 import BeautifulSoup
readable=[]
for ident in [s['source_id'] for s in seal['source']['anchors']]:
 a,b=source_nodes[ident];soup=BeautifulSoup(text[a:b],'html.parser')
 for math in soup.find_all('math'):math.replace_with(' $'+math.get('alttext',math.get_text(' ',strip=True))+'$ ')
 readable.append(ident+'\n'+soup.get_text(' ',strip=True)+'\n')
(ROOT/'source-readable-excerpts.txt').write_text('\n'.join(readable))
print('Bounded static production render and all exact map checks passed.',flush=True)
