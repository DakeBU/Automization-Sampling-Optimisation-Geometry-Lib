import json,hashlib,os,datetime,subprocess,struct
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
R=Path('E:/Samplinglib');T=R/'runs/20261007-companion-priority/pbps-macroscopic-centered-range58';B=T/'exposition-seal58';SITE=R/'_site';H=SITE/'example-cases/samplewiki/companions/proximal-bouncy-particle.html';B.mkdir(parents=True,exist_ok=True)
SCI='8c8847715c1d4c3033224b069d8dd694f2a4bd30';INT='a7cafde7957a8562bcd697d89c56b14768914c66'
def h(b):return hashlib.sha256(b).hexdigest()
def can(o):return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def rec(p):
 b=Path(p).read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=str(p).replace('\\','/'),raw_bytes=len(b),raw_sha256=h(b),lf_bytes=len(l),lf_sha256=h(l))
def write(n,o):(B/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
class N:
 def __init__(self,t,a):self.tag=t;self.a=dict(a);self.c=[]
 def text(self):return ''.join(x.text() if isinstance(x,N) else x for x in self.c)
 def all(self):
  yield self
  for x in self.c:
   if isinstance(x,N):yield from x.all()
class Parser(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.root=N('root',[]);self.st=[self.root]
 def handle_starttag(self,t,a):
  n=N(t,a);self.st[-1].c.append(n)
  if t not in {'meta','link','br','img','input','hr','wbr','source','area','base','embed','param','track','col'}:self.st.append(n)
 def handle_endtag(self,t):
  for i in range(len(self.st)-1,0,-1):
   if self.st[i].tag==t:self.st=self.st[:i];break
 def handle_data(self,d):self.st[-1].c.append(d)
def parse(p):x=Parser();x.feed(Path(p).read_text(encoding='utf-8'));return x.root
ids=['l2-pullback-range','pbps-macroscopic-centered-range','pbps-centered-macro-defect-gap']
decls=['AutoSamplingTheory.TechnicalLemmas.Measure.L2PullbackRange.l2_pullback_range_eq_lpMeas','AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicRange.actual_macroscopic_centered_range','Tests.ProximalBPSMacroscopicRange.actual_centered_macro_contraction_and_defect_gap']
codes=[R/'AutoSamplingTheory/TechnicalLemmas/Measure/L2PullbackRange.lean',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicRange.lean',R/'Tests/ProximalBPSMacroscopicRange.lean']
mods=['autosamplingtheory-technicallemmas-measure-l2pullbackrange','autosamplingtheory-examplecases-proximalbps-macroscopicrange','tests-proximalbpsmacroscopicrange']
audits=['ASTIS-RT-20261008-L2PullbackRange','ASTIS-RT-20261008-PBPSMacroscopicCenteredRange','ASTIS-RT-20261008-PBPSCenteredMacroDefectGap']
write('lease.open.json',dict(schema_version=1,status='OPEN',actor='/root/statement_topology58',pid=os.getpid(),compiler='NOT_STARTED_CLOSED',science_commit=SCI,integration_commit=INT,allowed_outputs=str(B)+'/*',scope='Independent scoped exposition/source-expansion and actual four PNG review; no full-reader/PURIFIED/live claim.',opened_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=str(R)).decode().strip();assert head==INT;assert subprocess.run(['git','merge-base','--is-ancestor',SCI,INT],cwd=str(R)).returncode==0
commitchecks=[]
for p in codes:
 path=str(p.relative_to(R)).replace('\\','/');actual=p.read_bytes().replace(b'\r\n',b'\n')
 for c in [SCI,INT]:
  got=subprocess.check_output(['git','show',c+':'+path],cwd=str(R));assert got.replace(b'\r\n',b'\n')==actual;commitchecks.append(dict(commit=c,path=path,normalized_source_sha256=h(actual)))
write('commit-check.json',dict(schema_version=1,head=head,science_commit=SCI,integration_commit=INT,science_is_ancestor=True,code_commit_checks=commitchecks,Git_mutation=False))
inputs=[H,SITE/'lean-foundations.html',SITE/'data/underlying-lean-graph.json',SITE/'assets/site.js',SITE/'assets/module-lean-tutor.js',SITE/'assets/underlying-lean-graph.js',R/'docs/proof-digestion-protocol.md',R/'docs/evidence-routed-memory-protocol.md',R/'lean-toolchain',R/'lake-manifest.json',T/'visual.inspection.json',T/'root.integration.1.lease.json']+codes
P=T.parent/'pbps-macro-range-preproof-review58';G=T.parent/'pbps-macro-range-sourcegraph58'
inputs += [P/'independent-source-reconstruction.json',P/'A2.SS1.raw.html',P/'A2.SS2.raw.html',P/'A3.SS1.raw.html',G/'source-proof-graph.json']
for n in ['prospective-statement.txt','generic-prospective-statement.txt','consumer-prospective-statement.txt']:inputs.append(T.parent/'pbps-macro-range-preproof58'/n)
for sub in ['visual58/cdp','visual58/proof']:
 for p in sorted((T/sub).glob('*')):
  if p.suffix in ['.png','.json']:inputs.append(p)
root=parse(H);rows=[];linkchecks=[];module_evidence=[];gatechecks=[];srcgraph=load(G/'source-proof-graph.json');graph=load(SITE/'data/underlying-lean-graph.json')
for i,(slug,decl,code,mod,auditname) in enumerate(zip(ids,decls,codes,mods,audits)):
 pubpath=R/'website/content/publications'/(slug+'.json');lessonpath=R/'website/content/declaration_lessons'/(slug+'.json');auditpath=R/'research-wiki/semantic-roundtrip/audits'/(auditname+'.json');inputs += [pubpath,lessonpath,auditpath]
 item=load(pubpath)['items'][0];lesson=load(lessonpath)['units'][0];audit=load(auditpath);assert audit['state']=='accepted' and audit['source_review']['state']=='accepted';assert audit['verdict']=='equivalent-after-elaboration'
 reviewpath=R/audit['source_review']['run_artifact'];inputs.append(reviewpath);review=load(reviewpath);assert review['review_run_sha256']==audit['source_review']['review_run_sha256'] and review['publication_binding_sha256']==audit['publication_binding_sha256']
 native=reviewpath.parent/'run.json';lease=reviewpath.parent/'lease.json';inputs += [native,lease];nativej=load(native);nx=nativej.copy();nsha=nx.pop('run_sha256');assert h(can(nx))==nsha==review['review_run_sha256'];assert load(lease)['status']=='CLOSED'
 matches=[x for x in root.all() if x.a.get('id')==slug];assert len(matches)==1;section=matches[0];article=next(x for x in section.all() if x.a.get('data-authored-declaration')==decl);assert item['statement'] in section.text() and lesson['statement'] in article.text()
 proofsteps=[x for x in article.all() if x.a.get('class')=='proof-reader-step'];assert len(proofsteps)==[3,4,4][i]==len(lesson['steps']);formula_checks=[]
 for j,(node,step) in enumerate(zip(proofsteps,lesson['steps'])):
  assert step['text'] in node.text() and step['formula'] in node.text() and step['lean'] in node.text();assert any(x.tag=='details' and 'open' not in x.a for x in node.all());formula_checks.append(dict(index=j+1,title=step['title'],formula=step['formula'],lean_reference=step['lean'],current_payload_equal=True,Lean_step_initially_folded=True))
 details=[x for x in article.all() if x.a.get('data-inline-lean')==decl];assert len(details)==2 and all('open' not in d.a for d in details);actual=code.read_text(encoding='utf-8');inline=[]
 for d in details:
  snippets=[x.text() for x in d.all() if x.tag=='code' and x.a.get('class')=='language-lean'];assert len(snippets)==1 and snippets[0] in actual;inline.append(dict(kind=d.a['class'],text_sha256=h(snippets[0].encode()),length=len(snippets[0]),exact_current_source_substring=True,initially_folded=True))
 for dep in lesson['astis_dependencies']:assert dep in article.text()
 for dep in lesson['mathlib_dependencies']:assert dep in article.text()
 for row in article.all():
  if row.tag!='a':continue
  href=row.a.get('href','');u=urlsplit(href)
  if u.scheme:continue
  target=(H.parent/unquote(u.path)).resolve() if u.path else H;assert target.is_file(),href;assert SITE.resolve() in target.parents
  if u.fragment:assert 'id="'+unquote(u.fragment)+'"' in target.read_text(encoding='utf-8'),href
  linkchecks.append(dict(section=slug,href=href,target=str(target).replace('\\','/'),fragment=u.fragment,status='EXISTS_EXACT_TARGET'))
  # Pin exact module/parent pages; teaching index is only navigation existence.
  if '/modules/' in str(target).replace('\\','/') or '/theorems/' in str(target).replace('\\','/'):inputs.append(target)
 mp=SITE/'modules'/(mod+'.html');inputs.append(mp);mt=parse(mp);complete=next(x for x in mt.all() if x.a.get('id')=='complete-module-source');assert actual in complete.text();module_evidence.append(dict(path=rec(mp),full_source_exact=True,source=rec(code),manual_source_selection_possible=True))
 gn=next(x for x in graph['nodes'] if x['id']=='decl:'+decl);assert (SITE/urlsplit(gn['url']).path).is_file();locator=next((x for x in gn.get('details',[]) if x['label']=='Source'),None)
 if locator:
  filename,line=locator['value'].rsplit(':',1);assert filename==str(code.relative_to(R)).replace('\\','/') and ('theorem '+decl.split('.')[-1]) in actual.splitlines()[int(line)-1]
 rows.append(dict(slug=slug,declaration=decl,publication=rec(pubpath),lesson=rec(lessonpath),audit=rec(auditpath),accepted_source_review=rec(reviewpath),source_review_run_sha256=nsha,proof_step_count=len(proofsteps),formula_steps=formula_checks,inline_exact_Lean=inline,statement_and_assumptions_preserved=True,source_attribution_preserved=True,scope_remaining_preserved=True,ASTIS_parents=lesson['astis_dependencies'],Mathlib_calls=lesson['mathlib_dependencies'],graph_node=gn,Test_scope=(i==2),source_nodes=[n for n in srcgraph['nodes'] if n['id'] in ([ 'BG:comap-representative','BG:Doob-Dynkin','BG:pushforward-Lp','S:M-onto'] if i==0 else ['S:model','S:real-L2','S:P','S:M','S:M-onto','S:mean-pullback','S:centered-onto'] if i==1 else ['S:U','S:blocks','S:block-defect','S:T-same','S:centered-A','S:scalar-C4','S:macro-C4','S:squared-gap'])]))
for sp in sorted(T.glob('integration.1.*.status.json')):
 j=load(sp);assert j['exit_code']==0 and j['proof_commit']==SCI;log=sp.with_name(sp.name.replace('.status.json','.log'));assert rec(log)['raw_sha256']==j['log_raw_sha256'];inputs += [sp,log];gatechecks.append(dict(status=rec(sp),log=rec(log),actual_recorded_exit_code=0,command=j['command']))
assert len(gatechecks)==14 and load(T/'root.integration.1.lease.json')['status']=='CLOSED'
visuals=[]
for name in ['visual58/cdp/pbps.png','visual58/cdp/branch.png','visual58/proof/proof.png','visual58/proof/proof-late.png']:
 p=T/name;b=p.read_bytes();assert b[:8]==b'\x89PNG\r\n\x1a\n';w,ht=struct.unpack('>II',b[16:24]);assert (w,ht)==(1440,1800);visuals.append(dict(image=rec(p),width=w,height=ht,actually_viewed_with_view_image=True,display_resize='Tool displayed 1408x1760; native PNG remains 1440x1800.'))
# Directly loaded scripts and original DOM are checked; no browser is launched or clicked.
pages=[H]+[SITE/'modules'/(m+'.html') for m in mods];scriptpaths=[];controls=[]
for page in pages:
 n=parse(page)
 for x in n.all():
  if x.tag=='a' and 'download' in x.a:controls.append(dict(page=str(page),attrs=x.a))
  if x.tag=='button' and any(y in str(x.a).lower() for y in ['copy','download','clipboard']):controls.append(dict(page=str(page),attrs=x.a))
  if x.tag=='script' and x.a.get('src') and not urlsplit(x.a['src']).scheme:
   s=(page.parent/x.a['src']).resolve();scriptpaths.append(s)
scriptpaths=list(dict.fromkeys(scriptpaths));assert not controls
script_checks=[]
for s in scriptpaths:
 text=s.read_text(encoding='utf-8');hits=[k for k in ['navigator.clipboard','createObjectURL','link.download','a.download','copy-source','download-source'] if k in text];assert not hits;inputs.append(s);script_checks.append(dict(script=rec(s),copy_download_implementation_hits=hits))
delivery=dict(status='BLOCKED_AGREED_COPY_DOWNLOAD_DELIVERY',classification='reader-delivery-missing-clipboard-and-direct-source-download',blocking_full_reader_delivery=True,blocking_mathematical_fidelity=False,evidence_pages=[rec(p) for p in pages],DOM_copy_download_controls=controls,loaded_local_scripts=script_checks,clipboard_or_download_clicks_performed=False,exact_module_source_and_Test_navigation_available=True,interpretation='Lossless inline and module source navigation is narrower than explicit clipboard/direct-source-download delivery. No click, downloaded artifact, live deployment or full reader delivery is inferred.')
debts=[dict(id='inline-notation-and-duplication',evidence='pbps.png shows dense raw inline notation and repeated full statement/assumptions.',blocking_scoped_math=False),dict(id='assumption-table-horizontal-scroll',evidence='proof-late.png shows horizontal scroll and clipped right-most explanation column.',blocking_scoped_math=False),dict(id='companion-height',evidence='Actual capture DOM bodyHeight=340664px; scoped figures do not cover full companion.',blocking_scoped_math=False),dict(id='long-graph-label',evidence='branch.png long qualified declaration wraps across many lines; incomplete name-scan references remain labelled.',blocking_scoped_math=False)]
payload=dict(schema_version=1,actor_identity='/root/statement_topology58',status='SCOPED_MATHEMATICAL_EXPOSITION_ACCEPTED_READER_DELIVERY_BLOCKED',science_commit=SCI,integration_commit=INT,commit_check=rec(B/'commit-check.json'),rows=rows,result_count=3,formula_step_count=11,exact_initially_folded_Lean_disclosures=6,actual_visuals=visuals,visual_coverage='Actual macro statement, actual Test proof/boundary, focused production graph. Generic leaf examined by exact DOM/payload; no separate generic viewport asserted.',source_and_Lean_expansion_preserved=True,blocking_reader_fidelity_deltas=[],reader_delivery_blockers=[delivery],readability_debts=debts,module_source_evidence=module_evidence,local_link_checks=linkchecks,integration_gates=gatechecks,gate_count=14,remaining_boundary='Gamma/root/inverse/full weighted weak H1/C5-C7/half-turn/dynamics/main/errors/cost/actual-input composition/full paper/Goal remain open.',source_acceptance_changed=False,old_science_negatives_reclassified=False,full_Exposition_Seal=False,Chapter1_3_full_reader_acceptance=False,PURIFIED=False,live_or_physical_device_verified=False,compiler_started=False,renderer_or_canonical_or_state_or_Git_edits=False)
write('exposition-seal-payload.json',payload)
inputs=list(dict.fromkeys(inputs));(B/'inputs').mkdir(exist_ok=True);manifest=[];used=set()
for i,p in enumerate(inputs):
 relative=str(p.relative_to(R)).replace('\\','/');qual=('%03d__'%i)+relative.split('/')[0]+'__'+h(relative.encode())[:16]+'__'+p.name[:48];assert qual not in used;used.add(qual);a=B/'inputs'/(qual+'.exactraw.snapshot');f=B/'inputs'/(qual+'.crlf-to-lf.snapshot');b=p.read_bytes();a.write_bytes(b);f.write_bytes(b.replace(b'\r\n',b'\n'));manifest.append(dict(qualified_identity=relative,actual_input=rec(p),exactraw_snapshot=rec(a),crlf_to_lf_snapshot=rec(f),binary_raw_only_for_media=p.suffix=='.png'))
write('input.manifest.json',dict(schema_version=1,input_count=len(manifest),basename_aliases_used=False,qualified_unique_snapshot_count=len(used),inputs=manifest))
print(json.dumps(dict(pid=os.getpid(),status=payload['status'],input_count=len(inputs),rows=3,formula_steps=11,folded_exact_Lean=6,actual_PNGs_viewed=4,gate_count=14,reader_fidelity_blockers=0,reader_delivery_blockers=1,exposition_seal_payload_sha256=h(can(payload)))))
