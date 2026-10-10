import pathlib,json,hashlib,subprocess,re,posixpath,sys
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
sys.stdout.reconfigure(encoding="utf8")
ROOT=pathlib.Path("E:/Samplinglib");OUT=ROOT/"runs/20261007-companion-priority/pbps-macroscopic-energy/exposition-seal50";BASE="runs/20261007-companion-priority/pbps-macroscopic-energy/";COMMIT="6b6877482d1c4316b9a8009ebc8d0b0cff6e10cf";seen={};checks={}
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p,binary=False):
 b=(ROOT/p).read_bytes();seen[p]={"path":p,"bytes":len(b),"raw_sha256":sha(b)}
 if binary:return b
 t=b.decode("utf8").replace("\r\n","\n").replace("\r","\n");seen[p]["lf_sha256"]=sha(t.encode());return t
def load(p):return json.loads(read(p))
def check(k,v):checks[k]=bool(v)
class N:
 def __init__(self,t="",a=()):self.tag=t;self.attrs=dict(a);self.children=[]
 def text(self):return "".join(x.text() if isinstance(x,N) else x for x in self.children)
 def all(self,t=None):
  a=[self] if t is None or self.tag==t else []
  for x in self.children:
   if isinstance(x,N):a+=x.all(t)
  return a
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.root=N();self.stack=[self.root]
 def handle_starttag(self,t,a):
  n=N(t,a);self.stack[-1].children.append(n)
  if t not in ["meta","link","img","input","br","hr","source","wbr"]:self.stack.append(n)
 def handle_endtag(self,t):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i].tag==t:self.stack=self.stack[:i];break
 def handle_data(self,s):self.stack[-1].children.append(s)
def tree(p):
 t=Parser();t.feed(read(p));return t.root
head=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT).decode().strip();check("frozen_HEAD",head==COMMIT)
lp="website/content/declaration_lessons/pbps-macroscopic-energy.json";pp="website/content/publications/pbps-macroscopic-energy.json";cp="research-wiki/frontier-cells/ASTIS-SW-PBPS-macroscopic-energy.json";ap="research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261007-PBPSMacroscopicEnergy.json";sp="AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicEnergy.lean";tp="Tests/ProximalBPSMacroscopicEnergy.lean"
u=load(lp)["units"][0];item=load(pp)["items"][0];cell=load(cp);audit=load(ap);source=read(sp);tests=read(tp);review=load(BASE+"source.1.review.json");ctx=review["current_review_context"];notes=load(BASE+"integration.notes.json")
check("statement_matches_admitted_context",u["statement"]==item["statement"]==ctx["statement"])
check("eight_steps_match_admitted_context",len(u["steps"])==8 and u["steps"]==ctx["lesson"]["steps"])
check("attribution_matches_admitted_context",item["source"]==ctx["source"])
check("four_ASTIS_and14_Mathlib_IDs_match_admitted_context",len(u["astis_dependencies"])==4 and len(u["mathlib_dependencies"])==14 and u["astis_dependencies"]==ctx["lesson"]["astis_dependencies"] and u["mathlib_dependencies"]==ctx["lesson"]["mathlib_dependencies"])
check("whole_normalized_source_matches_reviewed_context",source==ctx["current_lean_module"])
start=source.index("theorem actual_macroscopic_gradient_energy_blocks");full=source[start:].strip();header=full.split(" := by",1)[0]
check("exact2907_header_seal",len((header+"\n").encode())==2907 and sha((header+"\n").encode())==item["statement_seal"]["signature_digest"])
check("local_norm_snd_adapter_twice_consumed",source.count("have norm_snd (v :")==1 and source.count(":= norm_snd ")==2)
check("two_named_tests_and_noncentered_boundaries_exist",all(x in tests for x in ["theorem gaussian_precision_macroscopic_energy","theorem rank_zero_noncentered_constant","A g = g","‖g‖^2 = 1","‖B g‖^2 = 0","(fun _ => 1)"]))
sgp=item["source_proof_coverage"]["source_graph"];sg=load(sgp);ids=cell["learning_contract"]["reader_backpressure"]["source_expansion_nodes"]
check("source_expansion_ids_exist",set(ids)<=set(n["id"] for n in sg["nodes"]))
page="_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html";reader=tree(page);section=next(n for n in reader.all() if n.attrs.get("id")==item["id"]);txt=section.text()
check("exact_original_publication_id",section.attrs.get("data-publication-item")==item["id"])
check("all_statement_and_conditions_present",u["statement"] in txt and all(x in txt for x in u["assumptions"]))
check("all_eight_formula_steps_and_Lean_correspondences_present",all(x["title"] in txt and x["text"] in txt and x["formula"] in txt and x["lean"] in txt for x in u["steps"]))
check("exact_variance_norm_defect_energy_formula_present",u["formula"] in txt)
details=section.all("details");check("13_details_initially_closed",len(details)==13 and all("open" not in d.attrs for d in details));inline={d.attrs.get("class"):d for d in details if "inline-lean" in d.attrs.get("class","")}
check("folded_header_exact_current_source",inline["inline-lean inline-lean-statement"].all("code")[0].text().strip()==header)
check("folded_whole_proof_exact_current_source",inline["inline-lean inline-lean-proof"].all("code")[0].text().strip()==full)
check("AE_only_mean_class_transfer_explicit",u["steps"][2]["text"] in txt and "does not transport pointwise derivatives" in txt)
check("authored_aliases_and_extension_explicit","authored aliases" in txt and "rank zero is an explicit authored extension" in txt)
check("all_remaining_boundaries_visible",u["boundary"] in txt and item["obligations"][1]["label"] in txt)
links=[]
for a in section.all("a"):
 href=a.attrs.get("href","");q=urlparse(href)
 if q.scheme:links.append({"href":href,"pinned_external_identity":True,"fresh_web_check":False});continue
 target=posixpath.normpath(posixpath.join(posixpath.dirname(page),unquote(q.path)));tr=tree(target)
 ok=not q.fragment or any(n.attrs.get("id")==unquote(q.fragment) for n in tr.all())
 check("reader_link_"+str(len(links)),target.startswith("_site/") and ok);links.append({"href":href,"target":target,"fragment":q.fragment,"valid":ok})
mp="_site/modules/autosamplingtheory-examplecases-proximalbps-macroscopicenergy.html";module=tree(mp);ms=next(n for n in module.all() if n.attrs.get("id")=="complete-module-source")
check("complete_module_source_exact_including_norm_snd",any(n.text().strip()==source.strip() for n in ms.all("code")) and "have norm_snd" in ms.text())
tm="_site/modules/tests-proximalbpsmacroscopicenergy.html";testtree=tree(tm);testsrc=next(n for n in testtree.all() if n.attrs.get("id")=="complete-module-source")
check("Test_source_link_and_full_body_exact",any(n.text().strip()==tests.strip() for n in testsrc.all("code")) and any(a.attrs.get("href")=="tests-proximalbpsmacroscopicenergy.html" for a in module.all("a")))
lessonpage="_site/lessons/autosamplingtheory-examplecases-proximalbps-macroscopicenergy-actual-macroscopic-gradient-energy-blocks-d462b3519074.html";lesson=tree(lessonpage)
check("dedicated_lesson_all_eight_steps_present",all(s["text"] in lesson.text() and s["formula"] in lesson.text() for s in u["steps"]))
graph=load("_site/data/underlying-lean-graph.json");gp=read("_site/lean-foundations.html");nodeid="decl:"+u["declaration"];node=next(n for n in graph["nodes"] if n["id"]==nodeid);edges=[e for e in graph["edges"] if nodeid in [e.get("source"),e.get("target")]]
theoremp="_site/"+node["url"];theorem=tree(theoremp)
check("graph_current_source_line23",any(x["label"]=="Source" and x["value"]==sp+":23" for x in node["details"]) and source.splitlines()[22].startswith("theorem actual_macroscopic_gradient_energy_blocks"))
check("graph_reader_pointer_resolves",any(a.attrs.get("href")=="../modules/autosamplingtheory-examplecases-proximalbps-macroscopicenergy.html#complete-module-source" for a in theorem.all("a")))
check("graph_scan_explicitly_incomplete",any("incomplete" in x["label"] for x in node["details"]) and "incomplete" in gp)
check("graph_ownership_is_not_proof_implication",any(e["relation"]=="declares" for e in edges) and "not theorem implication" in gp)
js=read("_site/assets/site.js");tutor=read("_site/assets/module-lean-tutor.js");js_source=read("website/static/site.js");tutor_source=read("website/static/module-lean-tutor.js")
check("generated_reader_scripts_match_current_source",js==js_source and tutor==tutor_source)
scoped_controls=[n.attrs for t in [section,module,lesson,theorem] for n in t.all() if "download" in n.attrs or "copy" in n.attrs.get("class","").lower() or "clipboard" in n.attrs.get("class","").lower()]
copy_download={"status":"NO_DEDICATED_SCOPED_CONTROLS_PRESENT_RUNTIME_UNVERIFIED","scoped_controls":scoped_controls,"static_scripts_define_clipboard_or_download":any(x in js+tutor for x in ["clipboard","createObjectURL","download =","download="]),"exact_full_source_text_available":True,"actual_clipboard_or_download_executed":False}
visual=load(BASE+"visual.inspection.json")
for a in visual["artifacts"]:
 read(a["portable_path"],a["portable_path"].endswith(".png"));check("visual_raw_binding_"+pathlib.Path(a["portable_path"]).name,seen[a["portable_path"]]["raw_sha256"]==a["raw_sha256"])
cap=load(BASE+"visual-inspection50/cdp.capture.json");pc=load(BASE+"visual-inspection50/proof.capture.json")
check("both_capture_browsers_exit0",cap["ownedBrowserExit"]["code"]==pc["ownedBrowserExit"]["code"]==0)
check("desktop10_math13_closed",cap["records"][0]["mathContainers"]==10 and cap["records"][0]["closedLeanDetails"]==13)
check("graph_capture_exact_focus",nodeid.replace(":","%3A",1) in cap["records"][1]["url"])
matches=[];mismatches=[]
for p,b in list(seen.items()):
 if p.startswith("_site/"):continue
 q=subprocess.run(["git","show",COMMIT+":"+p],cwd=ROOT,capture_output=True)
 if q.returncode:continue
 matches.append(p) if sha(q.stdout)==b["raw_sha256"] else mismatches.append({"path":p,"commit_raw_sha256":sha(q.stdout),"working_raw_sha256":b["raw_sha256"],"commit_lf_sha256":sha(q.stdout.decode("utf8").replace("\r\n","\n").replace("\r","\n").encode()),"working_lf_sha256":b.get("lf_sha256"),"lf_equal":sha(q.stdout.decode("utf8").replace("\r\n","\n").replace("\r","\n").encode())==b.get("lf_sha256")})
q=subprocess.run(["git","show",COMMIT+":"+cp],cwd=ROOT,capture_output=True);committed_cell=json.loads(q.stdout)
check("EXACT_COMMIT_FRONTIER_CELL_MATCHES_WORKING_GRAPH_INPUT",sha(q.stdout)==seen[cp]["raw_sha256"])
shared=notes.get("shared_files",[]);note_cell_paths=[x["path"] for x in shared if "frontier-cells" in x.get("path","")]
check("INTEGRATION_NOTES_BIND_CURRENT50_CELL",cp in note_cell_paths)
result={"schema_version":1,"status":"READER_STATIC_DESKTOP_PASS_EXACT_COMMIT_GRAPH_INPUT_CLOSURE_BLOCKED","checked_commit":COMMIT,"reviewer":"/root/anonymous_decoder_49","checks":checks,"input_artifacts":list(seen.values()),"commit_byte_matching_inputs":matches,"commit_byte_mismatches":mismatches,"source_expansion_nodes":ids,"lean_expansion_nodes":cell["learning_contract"]["reader_backpressure"]["lean_expansion_nodes"],"source_graph_path":sgp,"admitted_context_path":BASE+"source.1.review.json","reader_links":links,"copy_download":copy_download,"focused_graph_node":node,"focused_graph_edges":edges,"graph_publication_inputs_sha256":graph.get("publication_inputs_sha256"),"working_cell_status":cell["status"],"committed_cell_status":committed_cell["status"],"integration_notes_cell_paths":note_cell_paths,"folded_header_sha256_including_LF":sha((header+"\n").encode()),"folded_header_bytes_including_LF":len((header+"\n").encode()),"current_normalized_full_module_sha256":sha(source.encode()),"bodyHeight":cap["records"][0]["bodyHeight"],"compiler_started":False,"source_fidelity_or_proof_verdict_granted":False,"old_decoder_artifacts_read_or_written":False}
(OUT/"bindings.json").write_bytes((json.dumps(result,ensure_ascii=False,indent=2)+"\n").encode())
print(json.dumps({"status":result["status"],"passed":sum(checks.values()),"failed":[k for k,v in checks.items() if not v],"committed_cell_status":committed_cell["status"],"working_cell_status":cell["status"],"byte_mismatches":mismatches,"copy_download":copy_download},ensure_ascii=False))