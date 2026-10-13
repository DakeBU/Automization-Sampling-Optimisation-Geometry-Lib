import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os,html.parser,collections
O=pathlib.Path(__file__).resolve().parent;R=O.parent;B=pathlib.Path('E:/Samplinglib');D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation.actual_projected_rotation';H=D+'_statement'
def sha(b):return hashlib.sha256(b).hexdigest()
def write(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
extra=[]
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();extra.append({'path':str(p).replace('\\','/'),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_sha256':sha(b.replace(b'\r\n',b'\n'))});return b
class Node:
 def __init__(self,tag='',attrs=(),parent=None):self.tag=tag;self.attrs=dict(attrs);self.children=[];self.parent=parent
 def text(self):return ''.join(x.text() if isinstance(x,Node) else x for x in self.children)
 def walk(self):
  yield self
  for x in self.children:
   if isinstance(x,Node):yield from x.walk()
 def find(self,tag=None,cls=None):return [x for x in self.walk() if (tag is None or x.tag==tag) and (cls is None or cls in x.attrs.get('class','').split())]
class Parser(html.parser.HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.root=Node();self.cur=self.root
 def handle_starttag(self,t,a):
  n=Node(t,a,self.cur);self.cur.children.append(n)
  if t not in ['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr']:self.cur=n
 def handle_endtag(self,t):
  n=self.cur
  while n.parent and n.tag!=t:n=n.parent
  if n.parent:self.cur=n.parent
 def handle_data(self,s):self.cur.children.append(s)
p=Parser();p.feed((B/'_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html').read_text(encoding='utf-8'));sections=[x for x in p.root.walk() if x.attrs.get('data-publication-item')=='pbps-actual-projected-rotation'];assert len(sections)==1;s=sections[0]
lesson=json.loads((B/'website/content/declaration_lessons/pbps-actual-projected-rotation.json').read_bytes())['units'][0];pub=json.loads((B/'website/content/publications/pbps-actual-projected-rotation.json').read_bytes())['items'][0];cell=json.loads((B/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-projected-rotation.json').read_bytes());audit=json.loads((B/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSActualProjectedRotation.json').read_bytes())
assert lesson['declaration']==D and lesson['helpers']==[H]
print('publication keys',list(pub));print('binding',pub['bindings']);print('audit source keys',list(audit.get('source_review',{})))
assert len(pub['bindings'])==1 and pub['bindings'][0]['declaration']==D;assert pub['bindings'][0]['cell']==cell['cell_id'];assert pub['bindings'][0]['audit_id']=='ASTIS-RT-20261009-PBPSActualProjectedRotation'
assert lesson['statement'] in s.text()
steps=s.find('div','proof-reader-step');assert len(steps)==8 and len(lesson['steps'])==8
raw=(B/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualProjectedRotation.lean').read_bytes();assert sha(raw)=='03a0721ae952f744d0bfdf568039b77f7035bec0a50642f8bc8ebc895273b998';lines=raw.decode().splitlines();ranges=[(144,309),(310,336),(337,365),(366,381),(382,422),(423,448),(449,455),(456,539)];rows=[]
for i,(step,ls,(a,z)) in enumerate(zip(steps,lesson['steps'],ranges),1):
 code='\n'.join(lines[a-1:z]);assert ls['lean'].rstrip('\r\n')==code
 codes=step.find('code','language-lean');assert len(codes)==1 and codes[0].text().rstrip('\r\n')==code
 ds=step.find('details');assert len(ds)==1 and 'open' not in ds[0].attrs
 eq=step.find('div','proof-reader-equation');assert len(eq)==1 and ls['formula'] in eq[0].text();assert ls['title'] in step.text()
 rows.append({'step':i,'title':ls['title'],'line_start':a,'line_end':z,'literal_code_UTF8_sha256':sha(code.encode()),'formula_UTF8_sha256':sha(ls['formula'].encode()),'initially_folded':True,'exact_lesson_DOM_module_match':True})
details=[x for x in s.find('details') if x.attrs.get('data-inline-lean') in [D,H]];assert len(details)==3 and all('open' not in x.attrs for x in details)
helper=next(x for x in details if x.attrs.get('data-inline-lean')==H);hc=helper.find('code','language-lean')[0].text();assert hc.rstrip('\r\n')=='\n'.join(lines[17:133]);assert 'Full Lean proposition (definition)' in helper.text() and 'no mathematical proof or additional hypothesis' in helper.text()
assert helper.parent is not None;assert any(x.attrs.get('data-inline-lean')==D and 'inline-lean-proof' in x.attrs.get('class','') and helper in list(x.walk()) for x in details)
cp=json.loads((R/'integration70/visual70/copy-unit0-copy-and-download.inspect.json').read_bytes());assert cp['initialFolded'] and cp['copyProbeUsesIsolatedPageClipboardCallback'] and not cp['physicalOSClipboardTest'];assert len(cp['panels'])==3 and len(cp['downloads'])==3 and len(cp['steps'])==8
for i,pr in enumerate(cp['panels']):assert pr['callbackCalled'] and pr['copiedExactly'] and pr['status']=='Copied'
publicstatement=next(x for x in details if x.attrs.get('data-inline-lean')==D and 'inline-lean-statement' in x.attrs.get('class',''))
publicproof=next(x for x in details if x.attrs.get('data-inline-lean')==D and 'inline-lean-proof' in x.attrs.get('class',''))
assert cp['panels'][0]['code']==publicstatement.find('code','language-lean')[0].text();assert cp['panels'][0]['code']=='\n'.join(lines[134:143]).removesuffix(' := by')
assert cp['panels'][1]['code']==publicproof.find('code','language-lean')[0].text();assert cp['panels'][1]['code'].rstrip('\r\n')=='\n'.join(lines[134:])
assert cp['panels'][2]['code'].rstrip('\r\n')==hc.rstrip('\r\n')
for ls,ps in zip(lesson['steps'],cp['steps']):assert ps['initiallyFolded'] and ps['lean']==ls['lean']
download=[]
for i,q in enumerate(cp['downloads'],1):
 rb=q['text'].encode('utf-8');assert q['status']==200 and rb==raw;f=(B/'_site/example-cases/samplewiki/companions'/q['href']).resolve();assert pin(f)==raw
 download.append({'index':i,'status':200,'UTF8_RAW_bytes':len(rb),'UTF8_RAW_sha256':sha(rb),'recorded_bytes_field':q['bytes'],'recorded_bytes_is_JS_string_length_not_UTF8_byte_count':True,'exact_RAW_module_match':True})
captures=json.loads((R/'integration70/visual70/render-capture.json').read_bytes());assert len(captures['records'])==10;caprows=[]
for x in captures['records']:
 f=R/'integration70/visual70'/('render-'+x['label']+'.png');rb=f.read_bytes();assert rb.startswith(b'\x89PNG\r\n\x1a\n');orig=pathlib.Path(x['png_path']);assert pin(orig)==rb
 assert x['bodyVisibility']=='visible' and x['bodyDisplay']=='block'
 if x['label'].startswith('unit0-proof-'):assert x['closedLeanDetails']==1 and x['mathContainers']==1
 caprows.append({'label':x['label'],'path':str(f.relative_to(B)).replace('\\','/'),'RAW_sha256':sha(rb),'independently_visually_viewed':True,'native_actual_CDP_url':x['url'],'initially_folded_count':x['closedLeanDetails'],'rendered_math_containers':x['mathContainers']})
graph=json.loads((B/'_site/data/underlying-lean-graph.json').read_bytes());nodes={x['id']:x for x in graph['nodes']};ids=['decl:'+D,'module:AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation','semantic-audit:ASTIS-RT-20261009-PBPSActualProjectedRotation','case:ASTIS-SW-PBPS-2026'];assert all(x in nodes for x in ids);assert nodes[ids[0]]['status']=='compiled';edges=[x for x in graph['edges'] if ids[0] in [x['source'],x['target']]];assert len(edges)==5;assert any(x['relation']=='source correspondence; not a Lean dependency' for x in edges);assert not any('68' in str(x) for x in edges)
assert graph['publication_inputs_sha256']==json.loads((R/'integration.notes.json').read_bytes())['publication_inputs_sha256'];assert 'Name-scanned references are incomplete' in graph['reference_contract'];assert 'decl:'+H not in nodes
br=(R/'integration70/browser-full-current/stdout.log').read_text(encoding='utf-8');assert 'Task-local Playwright1.57.0 with installed Chrome' in br and 'actual browser-check Python PID 37180' in br and 'browser-check EXIT 0' in br
browser=json.loads(br[br.index('{'):br.rindex('}')+1]);assert not browser['runtime_errors'];pb=[x for x in browser['companion_publications'] if x['path'].endswith('proximal-bouncy-particle.html')][0];assert pb=={'path':'example-cases/samplewiki/companions/proximal-bouncy-particle.html','declarations':79,'proof_panels':81,'adjacent_lean':True,'mobile_overflow':False}
result={'schema':'independent-scoped-reader70-checks-v1','actual_PID':os.getpid(),'scope':'Current frozen local artifacts and actual native local Chrome run; no new browser suite or physical clipboard interaction.','single_source_publication_lesson_cell_audit_identity':True,'literal_definition':{'full_scanner_identity':H,'exact_lines':[18,133],'RAW_line_code_sha256':sha(hc.encode()),'complete_value_exact':True,'definition_nonprovider_label_exact':True,'adjacent_nested_in_public_proof_fold':True,'initially_folded':True,'not_a_graph_provider_node':True},'steps':rows,'copy_callbacks':{'count':3,'all_called_exact':True,'OS_clipboard_credit':False},'RAW_downloads':download,'actual_captures':caprows,'browser':{'native_wrapper_PID':41280,'native_actual_checker_PID':37180,'EXIT':0,'installed_Chrome':True,'isolated_headless_profile':True,'local_HTTP':True,'current_reader_script_RAW_pins_match_CLOSED169':True,'PBPS_current_result':pb,'runtime_errors':[],'new_suite_not_run':True,'owned_Chrome_closed_after_native_run':True},'graph':{'current_digest':graph['publication_inputs_sha256'],'node_ids':ids,'edges':edges,'scanner_refs_are_incomplete_dashed_signals':True,'spurious_name_scan_LogConcaveOn_prod_not_formal_dependency':True},'reader_debt':['Dense untypeset Unicode/underscore notation in complete source statement; no full Chapter1.3 Exposition Seal.','Dense inherited graph labels and one incomplete scanner false-positive LogConcaveOn.prod; exact compiled dependence not inferred from scan.','Download evidence field bytes records JavaScript string length24755, independently measured UTF8 RAW26615 matches canonical module exactly.','Isolated copy callbacks do not demonstrate physical OS clipboard or live deployment.'],'no_credit':['main/live','full Exposition Seal','PURIFIED','B21 corrector change','B4 dynamics','wholepaper','Goal completion']}
write('reader70.checks.json',result);write('reader70.additional-input-pins.json',{'count':len(extra),'LF_rule':'CRLF to LF only','inputs':extra});print('PASS reader8steps 10captures 3callbacks 3RAWdownloads complete literal nonprovider; actual native Chrome EXIT0')
