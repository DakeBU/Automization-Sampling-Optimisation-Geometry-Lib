import sys,json,hashlib,subprocess,re,html,struct
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.dont_write_bytecode=True
root=Path(r'E:\Samplinglib');run=root/'runs/20261007-companion-priority/pbps-source-mean-gradient-domain54';role=run/'exposition-seal54'
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(o):return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode('utf-8')
def emit(o):return (json.dumps(o,sort_keys=True,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode('utf-8')
def write(p,o):p.write_bytes(emit(o))
def bind(p):
 b=p.read_bytes();return {'path':p.relative_to(root).as_posix(),'bytes':len(b),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n'))}
opened=[]
def guard(event,args):
 if event!='open' or not isinstance(args[0],(str,bytes)):return
 p=Path(args[0]).resolve()
 try:rel=p.relative_to(root).as_posix()
 except ValueError:return
 if 'private.future55' in rel or (rel.startswith('runs/20261007-companion-priority/') and any('55' in x for x in rel.split('/')[2:-1])):
  raise RuntimeError('Future55 evidence read forbidden: '+rel)
 opened.append(rel)
sys.addaudithook(guard)
sys.path.insert(0,str(root/'tools'));sys.path.insert(0,str(root/'website/scripts'))
import publication_reader as reader
import inline_lean
value=reader.graph_input_digest();graph_path=root/'_site/data/underlying-lean-graph.json';g=json.loads(graph_path.read_bytes());assert value==g['publication_inputs_sha256']
canonical_open_paths=sorted(set(opened));canonical_binding=[bind(root/p) for p in canonical_open_paths if (root/p).is_file()]
write(role/'canonical-input-bindings54.json',{'purpose':'Inputs actually opened by native current graph digest helper only; canonical established audit-backed reads do not imply semantic replay. Future55 guard active.','files':canonical_binding})
helper=root/'website/scripts/publication_reader.py';raw=helper.read_bytes();selected=b''.join(raw.splitlines(keepends=True)[182:187]);(role/'publication_reader.183-187.raw.snapshot.py').write_bytes(selected)
helpers=[Path(m.__file__).resolve() for m in list(sys.modules.values()) if getattr(m,'__file__',None) and str(Path(m.__file__).resolve()).startswith(str(root)) and Path(m.__file__).suffix=='.py']
name='AutoSamplingTheory.ExampleCases.ProximalBPS.SourceMeanGradientDomain.literal_source_mean_in_closed_gradient';cellid='ASTIS-SW-PBPS-source-mean-gradient-domain';cell=reader.publication.inputs()['cells'][cellid];decl=reader.publication.inputs()['declarations'][name]
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root).decode().strip();science='16797326f3e06a853e2d047f67fde924ac8c1647';assert head=='d6341c498a5a2f6e3f73f540896b0d1b7dbe4bd6'
production='AutoSamplingTheory/ExampleCases/ProximalBPS/SourceMeanGradientDomain.lean';tests='Tests/ProximalBPSSourceMeanGradientDomain.lean';sources=[]
for rp,expected in [(production,88),(tests,113)]:
 b=(root/rp).read_bytes();assert len(b.decode('utf-8').splitlines())==expected;rows=[]
 for commit in [head,science]:
  gb=subprocess.check_output(['git','show',commit+':'+rp],cwd=root);glf=gb.replace(b'\r\n',b'\n');assert glf==b.replace(b'\r\n',b'\n')
  rows.append({'commit':commit,'git_raw_sha256':sha(gb),'git_lf_sha256':sha(glf),'current_raw_equals_git_raw':b==gb,'current_lf_equals_git_lf':True})
 sources.append({'current':bind(root/rp),'actual_lines':expected,'git':rows})
html_path=root/'_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html';s=html_path.read_text(encoding='utf-8');exact=inline_lean.display_source(decl.source_text);signature,_=inline_lean.split_statement(exact);folds=[]
for rn,expected in [('statement',signature),('proof',exact)]:
 m=re.search(r'<details class="inline-lean inline-lean-'+rn+r'" data-inline-lean="'+re.escape(name)+r'"[^>]*>(.*?)</details>',s,re.S);assert m
 code=re.search(r'<pre[^>]*>(.*?)</pre>',m[1],re.S);assert code
 actual=html.unescape(re.sub(r'<[^>]*>','',code[1]));assert actual.strip()==expected.strip()
 folds.append({'role':rn,'initially_folded':True,'native_exact_equals_rendered':True,'native_UTF8_sha256':sha(expected.strip().encode()),'rendered_UTF8_sha256':sha(actual.strip().encode()),'lines':len(expected.splitlines()),'source_line':decl.source_line,'context_hrefs':re.findall(r'href="([^"]+)"',m[1])})
start=s.index('<section id="pbps-source-mean-gradient-domain"');section=s[start:];article_end=section.index('</article>')+len('</article>');article=section[:article_end]
assert article.count('class="proof-reader-step"')==5
status_neutral=all(t not in article for t in ['independent mathematics/source/exact-commit/shared integration remain pending','independent review/integration pending'])
audit_path=root/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261008-PBPSSourceMeanGradientDomain.json';audit=json.loads(audit_path.read_bytes());deltas=audit['deltas'];assert len(deltas)==3
for d in deltas:assert html.escape(d['description']) in article and html.escape(d['evidence']) in article
parent_names=json.loads((run/'publication-plan.json').read_bytes())['actual_ASTIS_parents'];parent_headers=[]
for pn in parent_names:
 pd=reader.publication.inputs()['declarations'][pn];ptext=inline_lean.display_source(pd.source_text);psig,_=inline_lean.split_statement(ptext)
 parent_headers.append({'declaration':pn,'source_file':pd.source_file,'source_line':pd.source_line,'public_statement':psig,'public_statement_UTF8_sha256':sha(psig.encode()),'source_file_binding':bind(root/pd.source_file),'proof_not_semantically_replayed':True})
write(role/'public-parent-bindings54.json',parent_headers)
module=root/'_site/modules/autosamplingtheory-examplecases-proximalbps-sourcemeangradientdomain.html';module_s=module.read_text(encoding='utf-8');assert 'id="complete-module-source"' in module_s
gates=[];paths=[root/production,root/tests,html_path,graph_path,module,helper,root/'website/scripts/inline_lean.py',root/'website/content/publications/pbps-source-mean-gradient-domain.json',root/'website/content/declaration_lessons/pbps-source-mean-gradient-domain.json',audit_path,root/cell['__path__'],root/'lean-toolchain',root/'lake-manifest.json',root/'AutoSamplingTheory/ExampleCases.lean',root/'AutoSamplingTheory/TechnicalLemmas/Registry.lean',root/'Tests.lean',root/'Tests/Basic.lean']+[root/pd['source_file'] for pd in parent_headers]
for p in sorted(run.glob('integration.0.*.status.json')):
 d=json.loads(p.read_bytes());log=run/p.name.replace('.status.json','.log');paths += [p,log];gates.append({'path':p.relative_to(root).as_posix(),'exit_code':d.get('exit_code'),'command':d.get('command'),'proof_commit':d.get('proof_commit'),'log_sha_matches':d.get('log_raw_sha256')==sha(log.read_bytes())})
assert len(gates)==12 and all(x['exit_code']==0 and x['log_sha_matches'] for x in gates)
for fn in ['publication-plan.json','verified.json','integration.notes.json','visual.inspection.json','source.0.review.json','reviewer.source.run.json','reviewer.source.lease.json','root.integration.0.lease.json','root.desktop-capture54.lease.json','desktop54.companion.status.json','desktop54.proof.status.json','desktop54.companion.log','desktop54.proof.log']:
 paths.append(run/fn)
for fn in ['desktop54.companion.status.json','desktop54.proof.status.json']:
 d=json.loads((run/fn).read_bytes());paths.append(root/Path(d['command'][1].replace('\\','/')))
visual=sorted((run/'visual-inspection54').glob('*'));paths+=visual;images=[]
for p in visual:
 if p.suffix=='.png':
  b=p.read_bytes();images.append({'binding':bind(p),'width':struct.unpack('>I',b[16:20])[0],'height':struct.unpack('>I',b[20:24])[0],'actually_viewed_with_view_image':True})
ident='decl:'+name;module_id='module:'+decl.module;node=next(n for n in g['nodes'] if n['id']==ident);edges=[e for e in g['edges'] if ident in [e['source'],e['target']] or (e['target']==module_id and e['relation']=='imports')]
imports={}
for rp in ['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests.lean']:
 imports[rp]=[ln for ln in (root/rp).read_text(encoding='utf-8').splitlines() if any(t in ln for t in ['SourceMeanGradientDomain','pbps.literalSourceMean.closedGradientDomain'])]
source_review=json.loads((run/'source.0.review.json').read_bytes());capture=json.loads((run/'visual-inspection54/cdp.capture.json').read_bytes());scoped=capture['records'][0]
obs={'current_head':head,'science_commit':science,'source_git_bindings':sources,'inputs':[bind(p) for p in dict.fromkeys(paths)],'helpers':[bind(p) for p in dict.fromkeys(helpers)],'native_selected_helper':{'whole':bind(helper),'selected_lines':[183,187],'selected_raw_sha256':sha(selected),'selected_lf_sha256':sha(selected.replace(b'\r\n',b'\n')),'snapshot':bind(role/'publication_reader.183-187.raw.snapshot.py')},'graph':{'publication_inputs_sha256':value,'recipe':'Native publication_reader.graph_input_digest183-187 -> publication.digest({lean:astis_site.source_digest(),items:publication.load(),cells:dict bound ids from publication.inputs}); source_digest hashes exact ordered path UTF8/NUL/raw bytes/NUL, publication.digest uses sorted compact ensure_ascii=False UTF8 JSON default allow_nan=True. Distinct from native role hashes allow_nan=False.','canonical_open_paths':canonical_open_paths,'node':node,'one_hop_edges':edges,'cell_path':cell['__path__'],'cell_status':cell.get('status')},'rendered':{'five_steps':5,'folds':folds,'initially_closed_details':len(re.findall(r'<details\b(?![^>]*\bopen\b)',article)),'status_neutral_residual':status_neutral,'source_comparison_displayed':True,'all_three_informational_elaborations_displayed':True,'audit_deltas':deltas,'source_citation_hrefs':sorted(set(html.unescape(h) for h in re.findall(r'href="([^"]+)"',article) if '2609.06905' in h)),'source_module_anchor_exists':True,'module_hrefs':sorted(set(html.unescape(h) for h in re.findall(r'href="([^"]+)"',module_s) if any(x in h.lower() for x in ['download','source','sourcemeangradientdomain']))),'DOM_math_containers':scoped['mathContainers'],'DOM_closedLeanDetails':scoped['closedLeanDetails']},'gates':gates,'imports':imports,'images':images,'source_review_exposure_as_existing_provenance':source_review['exposure_disclosure'],'audit_state':audit['state'],'audit_verdict':audit['verdict'],'helper_scope':'Explicit parent authorization for current54 canonical graph only; future55 directories/private.future55 guard active, bytecode writes disabled; established canonical audit-backed evidence may be read for digest only, not semantically replayed.','failures':[]}
write(role/'input-bindings54.json',obs)
print(json.dumps({'graph_digest':value,'canonical_open_count':len(canonical_open_paths),'source_linecounts':[x['actual_lines'] for x in sources],'gates':len(gates),'folds':folds,'rendered_status_neutral':status_neutral,'three_elaborations_displayed':True,'closedDetails':obs['rendered']['initially_closed_details'],'images':len(images),'audit_state':audit['state']},ensure_ascii=False,indent=2))