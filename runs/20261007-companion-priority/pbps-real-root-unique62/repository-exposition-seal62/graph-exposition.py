from common import *
import re,html
sys.path.insert(0,str(ROOT/'website/scripts'))
import publication_reader as reader,astis_publication as publication,astis_site
tree=J(P/'integration.tree.index.json')['files'];opening=J(P/'opening.inputs.json')['snapshot_pairs']+J(P/'opening.assets.supplement.json')['pairs'];frozen={p['original']['path']:p['exact_raw_snapshot']['path'] for p in opening};pins=[]
def read(p):
 source=path(p);resolved=path(frozen.get(source.as_posix(),source.as_posix()));q=pin(resolved);pins.append(dict(qualified_original=source.as_posix(),actual=pin(source),resolved=q));return resolved.read_bytes()
def git(p):return subprocess.check_output(['git','show',INT+':'+p],cwd=ROOT)
leanfiles=['AutoSamplingTheory.lean',*[p.relative_to(ROOT).as_posix() for p in sorted(ROOT/p for p in tree if p.startswith('AutoSamplingTheory/') and p.endswith('.lean'))],'Tests.lean',*[p.relative_to(ROOT).as_posix() for p in sorted(ROOT/p for p in tree if p.startswith('Tests/') and p.endswith('.lean'))],'lakefile.lean','lean-toolchain','lake-manifest.json']
# Exact integration list and native WindowsPath order; newly installed63 never enumerated.
digest=hashlib.sha256()
for p in leanfiles:
 b=read(p);digest.update(p.encode());digest.update(b'\0');digest.update(b);digest.update(b'\0')
source_digest=digest.hexdigest()
pubpaths=sorted(ROOT/p for p in tree if p.startswith('website/content/publications/') and p.endswith('.json'));items=[]
for p in pubpaths:items.extend(json.loads(read(p))['items'])
cells={}
for cid in sorted({b['cell'] for i in items for b in i['bindings']}):
 p=ROOT/'research-wiki/frontier-cells'/f'{cid}.json';q=json.loads(read(p));q['__path__']=p.relative_to(ROOT).as_posix();cells[cid]=q
full_payload=dict(lean=source_digest,items=items,cells=cells);W(P/'graph.digest.complete-payload.json',full_payload)
old_inputs,old_load,old_source=publication.inputs,publication.load,astis_site.source_digest
try:
 publication.inputs=lambda:dict(cells=cells);publication.load=lambda:items;astis_site.source_digest=lambda:source_digest
 actual=reader.graph_input_digest()
finally:publication.inputs,publication.load,astis_site.source_digest=old_inputs,old_load,old_source
graph=json.loads(read('_site/data/underlying-lean-graph.json'));assert actual==graph['publication_inputs_sha256']==publication.digest(full_payload),(actual,graph['publication_inputs_sha256'])
plan=J(R/'publication-plan.json');nodes={n['id']:n for n in graph['nodes']};branches=[]
for decl in plan['mathematical_declarations']:
 n=nodes['decl:'+decl];assert n['status']=='compiled';incident=[e for e in graph['edges'] if e['source']==n['id'] or e['target']==n['id']];branches.append(dict(node=n,incident_edges=incident,truth_contract='Solid imports/ownership; dashed source/scanned-name/curated links are incomplete noncertified references, not exported elaborated theorem implication.'))
W(P/'graph.check.json',dict(status='PASS',science=SCI,integration=INT,native_graph_sha256=pin(path(frozen[path('_site/data/underlying-lean-graph.json').as_posix()])),publication_inputs_sha256=actual,source_digest=source_digest,source_paths_count=len(leanfiles),production_modules=515,all_publication_items=len(items),referenced_cells=len(cells),complete_payload=pin(P/'graph.digest.complete-payload.json'),helper_whole=pin('website/scripts/publication_reader.py'),helper_lines='183-187 graph_input_digest; full exact result, no projected digest',source_order='Exact Git tree candidate paths sorted as native WindowsPath, then raw opening/current unchanged62 bytes; excludes new63 by exact tree membership.',branches=branches,counts=graph['counts'],source_reference_boundary='LogConcaveOn.prod scanner hit is not an exact compiled body parent. Name scans are incomplete. Actual62 positive-complex-lift/shared-uniqueness/actual61 body calls independently reviewed.',no63proofcredit=True))
body=read('_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html').decode();expo=[]
for slug,decl in zip(plan['slugs'],plan['mathematical_declarations']):
 lesson=json.loads(read(f'website/content/declaration_lessons/{slug}.json'))['units'][0];assert len(lesson['steps'])==(4 if slug==plan['slugs'][0] else 3)
 code_rows=[]
 for role in ['statement','proof']:
  pattern=r'<details\b([^>]*class="inline-lean inline-lean-'+role+r'"[^>]*data-inline-lean="'+re.escape(decl)+r'"[^>]*)>(.*?)</details>'
  blocks=re.findall(pattern,body,re.S);assert blocks,decl
  for attrs,block in blocks:
   assert not re.search(r'\bopen(?:\s|=|$)',attrs)
   raw_code=re.findall(r'<pre[^>]*>\s*<code[^>]*>(.*?)</code>\s*</pre>',block,re.S);assert len(raw_code)==1
   code=html.unescape(re.sub('<[^>]+>','',raw_code[0])).strip()
   module=decl.rsplit('.',1)[0].replace('.','/')+'.lean';source=read(module).decode();start=source.index('theorem '+decl.rsplit('.',1)[1]);decl_source=source[start:].strip();expected=decl_source.split(':= by',1)[0].strip() if role=='statement' else decl_source
   assert code==expected,(decl,role,len(code),len(expected))
   hrefs=re.findall(r'<a\b[^>]*href="([^"]+)"',block);download=next(h for h in hrefs if h.endswith('.lean'));context=next(h for h in hrefs if '.html' in h)
   target=(ROOT/'_site/example-cases/samplewiki/companions'/download).resolve();assert target.is_relative_to(ROOT/'_site');assert target.read_bytes().replace(b'\r\n',b'\n')==path(module).read_bytes().replace(b'\r\n',b'\n');pins.append(dict(qualified_original=target.as_posix(),actual=pin(target),resolved=pin(target)))
   context_path=(ROOT/'_site/example-cases/samplewiki/companions'/context.split('#')[0]).resolve();assert context_path.exists();pins.append(dict(qualified_original=context_path.as_posix(),actual=pin(context_path),resolved=pin(context_path)))
   assert 'data-lean-copy' in block
   code_rows.append(dict(role=role,initially_folded=True,exact_complete_code_sha256=H(code.encode()),bytes=len(code.encode()),download=pin(target),context=pin(context_path),copy='Static control points to exact rendered <pre> code; interactive clipboard execution not tested.',copy_tail_debt='Full proof extraction includes following end/noncomputable section/namespace commands. It matches actual source slice but is not isolated standalone copy-paste theorem syntax.'))
 for step in lesson['steps']:
  assert html.escape(step['title']) in body and html.escape(step['text']) in body and html.escape(step['lean']) in body
 expo.append(dict(declaration=decl,full_attributed_statement=lesson['statement'],source_binder_boundary=lesson['assumptions'],formula=lesson['formula'],steps=lesson['steps'],step_count=len(lesson['steps']),step_Lean_is_named_reference_only=True,inline_full_code=code_rows,scope=lesson['boundary']))
capture=J(R/'integration62/visual62/capture.json');assert len(capture['records'])==8 and capture['ownedBrowserExit']['code']==0
for q in capture['records']:
 png=R/'integration62/visual62'/f"{q['label']}.png";dom=R/'integration62/visual62'/f"{q['label']}.inspect.json";read(png);read(dom)
W(P/'exposition.check.json',dict(status='ACCEPT_SCOPED_READER_CONTENT_WITH_EXPLICIT_DEBT',all_eight_images_viewed=True,capture=pin(R/'integration62/visual62/capture.json'),owned_browser_actual_PID=capture['pid'],owned_browser_exit_code=0,units=expo,formula_steps=7,source_and_decoder_separate=True,debts=['Seven per-step Lean disclosures contain named APIs/local references, not executable exact step snippets. Full statement/proof folds checked independently; no full Chapter1.3/ExpositionSeal.','Dense duplicated statements and long graph labels remain reader debt.','Full proof source slices include trailing namespace/end commands; copy control is static checked, clipboard execution unrun.','Graph name scans incomplete; LogConcaveOn.prod signal gives no theorem-edge credit. Graph registry_declarations509 is generated scanner inventory; actual compiled Registry count507 separately proved by Tests.Basic.'],remaining=J(R/'integration.notes.json')['remaining'],no_full_paper_Purified_main_live=True))
W(P/'graph-exposition.inputs.json',dict(count=len(pins),pin_occurrences=pins,scope='ExactINT515 source inventory / all228 publication items / referenced canonical cells needed by complete native graph digest; specific reader/download/context/capture only. No future production63 API/proof read.'))
print('GRAPH_EXPOSITION62_PASS',actual,'source',len(leanfiles),'pin occurrences',len(pins),'eight images/4+3steps')
