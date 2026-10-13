import sys,pathlib,json,hashlib,subprocess,re,posixpath
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
sys.stdout.reconfigure(encoding="utf-8")
ROOT=pathlib.Path("E:/Samplinglib")
OUT=ROOT/"runs/20261007-companion-priority/pbps-outer-gradient-energy/exposition-seal49"
COMMIT="39d72437b565e21c65364187a810501754a38c4b"
BASE="runs/20261007-companion-priority/pbps-outer-gradient-energy/"
seen={}
def digest(b):return hashlib.sha256(b).hexdigest()
def read(p,binary=False):
 b=(ROOT/p).read_bytes()
 seen[p]={"path":p,"bytes":len(b),"raw_sha256":digest(b)}
 if not binary:
  t=b.decode("utf-8");seen[p]["lf_sha256"]=digest(t.replace("\r\n","\n").replace("\r","\n").encode())
  return t.replace("\r\n","\n").replace("\r","\n")
 return b
def load(p):return json.loads(read(p))
def gitbytes(p):
 q=subprocess.run(["git","show",COMMIT+":"+p],cwd=ROOT,capture_output=True)
 return q.returncode,q.stdout
class N:
 def __init__(self,t="",a=()):self.tag=t;self.attrs=dict(a);self.children=[]
 def text(self):return "".join(x.text() if isinstance(x,N) else x for x in self.children)
 def all(self,t=None):
  out=[self] if t is None or self.tag==t else []
  for x in self.children:
   if isinstance(x,N):out+=x.all(t)
  return out
class P(HTMLParser):
 def __init__(self):super().__init__();self.root=N();self.stack=[self.root]
 def handle_starttag(self,t,a):
  n=N(t,a);self.stack[-1].children.append(n)
  if t not in ["meta","link","img","input","br","hr","source","wbr"]:self.stack.append(n)
 def handle_endtag(self,t):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i].tag==t:self.stack=self.stack[:i];break
 def handle_data(self,s):self.stack[-1].children.append(s)
def tree(p):
 t=P();t.feed(read(p));return t.root
checks={}
def check(k,v):
 checks[k]=bool(v)
 if not v:raise AssertionError(k)
check("actual_HEAD_is_frozen_commit",subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT).decode().strip()==COMMIT)
lesson_path="website/content/declaration_lessons/pbps-conditional-gradient-energy.json"
pub_path="website/content/publications/pbps-conditional-gradient-energy.json"
cell_path="research-wiki/frontier-cells/ASTIS-SW-PBPS-conditional-gradient-energy.json"
audit_path="research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261007-PBPSConditionalGradientEnergy.json"
lean_path="AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalGradientEnergy.lean"
unit=load(lesson_path)["units"][0];item=load(pub_path)["items"][0];cell=load(cell_path);audit=load(audit_path);lean=read(lean_path)
review=load(BASE+"source.0.review.json")
ctx=review["publication_review_context"]
check("authored_statement_matches_reviewed_source_context",item["statement"]==ctx["statement"]==unit["statement"])
check("all_eight_authored_steps_match_admitted_source_exposition",unit["steps"]==ctx["lesson"]["steps"] and len(unit["steps"])==8)
check("source_attribution_matches_reviewed_context",item["source"]==ctx["source"])
check("ASTIS_and_Mathlib_dependency_lists_match_reviewed_exposition",unit["astis_dependencies"]==ctx["lesson"]["astis_dependencies"] and unit["mathlib_dependencies"]==ctx["lesson"]["mathlib_dependencies"])
check("current_full_module_matches_independently_reviewed_module",lean==ctx["current_lean_module"])
graph_source=load("runs/20261007-companion-priority/pbps-outer-gradient-topology-overlay49/source-proof-graph.after.json")
backpressure=cell["learning_contract"]["reader_backpressure"]
source_ids=backpressure["source_expansion_nodes"]
check("all_exposition_source_node_ids_exist",set(source_ids)<=set(x["id"] for x in graph_source["nodes"]))
topology=load("runs/20261007-companion-priority/pbps-outer-gradient-source-topology-review49/source-topology-review.repaired.json")
check("retained_purification_status_is_pending",cell["purification"]["status"]=="pending")
page="_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html"
reader=tree(page)
section=next(x for x in reader.all() if x.attrs.get("id")==item["id"])
check("exact_original_publication_id",section.attrs.get("data-publication-item")==item["id"])
txt=section.text()
check("complete_current_statement_and_all_assumptions_rendered",unit["statement"] in txt and all(x in txt for x in unit["assumptions"]))
check("all_eight_current_math_explanations_and_formulas_rendered",all(s["title"] in txt and s["text"] in txt and s["formula"] in txt for s in unit["steps"]))
check("exact_main_energy_and_variance_formula_rendered",unit["formula"] in txt)
details=section.all("details")
check("all_thirteen_disclosures_initially_closed",len(details)==13 and all("open" not in d.attrs for d in details))
inline={d.attrs.get("class"):d for d in details if "inline-lean" in d.attrs.get("class","")}
start=lean.index("theorem reflected_conditional_gradient_energy")
end=lean.index("\nend AutoSamplingTheory.",start)
full=lean[start:].strip()
statement=full.split(" := by",1)[0]
check("exact1795_statement_seal_including_trailing_LF",len((statement+"\n").encode())==1795 and digest((statement+"\n").encode())==cell["statement_seal"]["signature_digest"])
check("folded_statement_is_exact_current_Lean_header",inline["inline-lean inline-lean-statement"].all("code")[0].text().strip()==statement)
check("folded_proof_is_exact_current_Lean_declaration_with_closing_namespace",inline["inline-lean inline-lean-proof"].all("code")[0].text().strip()==full)
check("remaining_rough_operator_main_cost_composition_boundary_rendered","Full B13 roughclosure/operator/halfturn/main/errors/querycost/composition remain open" in txt and unit["boundary"] in txt)
links=[]
for a in section.all("a"):
 href=a.attrs.get("href","")
 u=urlparse(href)
 if u.scheme:
  links.append({"href":href,"scope":"pinned external identity, reused admitted source; no web access","valid":href==item["source"]["url"]});continue
 target=posixpath.normpath(posixpath.join(posixpath.dirname(page),unquote(u.path)))
 check("link_stays_inside_static_site_"+str(len(links)),target.startswith("_site/"))
 target_tree=tree(target)
 exists_fragment=not u.fragment or any(x.attrs.get("id")==unquote(u.fragment) for x in target_tree.all())
 links.append({"href":href,"target":target,"fragment":u.fragment,"valid":exists_fragment})
 check("reader_link_target_and_fragment_"+str(len(links)),exists_fragment)
module_page="_site/modules/autosamplingtheory-examplecases-proximalbps-conditionalgradientenergy.html"
module=tree(module_page)
module_source=next(x for x in module.all() if x.attrs.get("id")=="complete-module-source")
check("complete_module_source_link_contains_exact_source_and_private_helper",any(x.text().strip()==lean.strip() for x in module_source.all("code")) and "private theorem reflected_second_moment" in module_source.text())
graph=load("_site/data/underlying-lean-graph.json")
graph_page=read("_site/lean-foundations.html")
ident="decl:"+unit["declaration"];node=next(n for n in graph["nodes"] if n["id"]==ident)
theorem_page="_site/"+node["url"];theorem=tree(theorem_page)
check("focused_graph_node_has_current_decl_and_code_line",next(x["value"] for x in node["details"] if x["label"]=="Source")==lean_path+":67" and lean.splitlines()[66].startswith("theorem reflected_conditional_gradient_energy"))
check("focused_graph_current_reader_link_exists",any(a.attrs.get("href")=="../modules/autosamplingtheory-examplecases-proximalbps-conditionalgradientenergy.html#complete-module-source" for a in theorem.all("a")))
edges=[e for e in graph["edges"] if ident in [e.get("source"),e.get("target")]]
check("graph_ownership_edge_is_declares",any(e["relation"]=="declares" and e["source"]=="module:AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalGradientEnergy" for e in edges))
check("graph_scanned_references_are_explicitly_incomplete",any(x["label"]=="References (name scan; incomplete)" for x in node["details"]) and "incomplete" in graph_page and all(e["relation"]=="source reference (scanner)" for e in edges if e["relation"].startswith("source reference")))
visual=load(BASE+"visual.inspection.json")
for a in visual["artifacts"]:
 b=read(a["portable_path"],binary=a["portable_path"].endswith(".png"))
 check("portable_visual_raw_binding_"+pathlib.Path(a["portable_path"]).name,seen[a["portable_path"]]["raw_sha256"]==a["raw_sha256"])
capture=load(BASE+"visual-inspection49/cdp.capture.json")
proofcap=load(BASE+"visual-inspection49/proof.capture.json")
check("actual_local_capture_browsers_exited_zero",capture["ownedBrowserExit"]["code"]==proofcap["ownedBrowserExit"]["code"]==0)
check("desktop_DOM_ten_math_thirteen_closed",capture["records"][0]["mathContainers"]==10 and capture["records"][0]["closedLeanDetails"]==13)
check("actual_graph_capture_focus_is_exact_current_decl",ident.replace(":","%3A",1) in capture["records"][1]["url"])
tracked=[]
for path,b in list(seen.items()):
 if path.startswith("_site/"):continue
 code,blob=gitbytes(path)
 if code==0:
  check("checked_commit_byte_binding_"+path,digest(blob)==b["raw_sha256"])
  tracked.append(path)
# Protocol inputs previously read and current audit roots also bound without reopening old decoder artifacts.
for path in ["docs/proof-digestion-protocol.md","docs/theorem-publication-protocol.md","docs/evidence-routed-memory-protocol.md",BASE+"publication-plan.json",BASE+"integration.notes.json",BASE+"integration.site-build.log"]:
 if path not in seen:read(path)
result={"schema_version":1,"status":"SCOPED_STATIC_AND_LOCAL_DESKTOP_PASS_WITH_PRESENTATION_DEBT","checked_commit":COMMIT,"reviewer":"/root/anonymous_decoder_49","checks":checks,"input_artifacts":list(seen.values()),"commit_byte_bound_inputs":tracked,"reader_links":links,"source_expansion_nodes":source_ids,"lean_expansion_nodes":backpressure["lean_expansion_nodes"],"source_graph_path":cell["source_proof_coverage"]["source_graph"],"admitted_source_review_path":BASE+"source.0.review.json","focused_graph_node":node,"focused_graph_edges":edges,"folded_statement_utf8_bytes":len(statement.encode()),"folded_statement_sha256":digest(statement.encode()),"folded_full_declaration_sha256":digest(full.encode()),"rendered_step_count":8,"closed_details":len(details),"current_full_module_sha256":digest(lean.encode()),"compiler_started":False,"source_text_visible":True,"prior_decoder_artifacts_read_or_written":False}
(OUT/"static-checks.json").write_bytes((json.dumps(result,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
print(json.dumps({"status":result["status"],"checks_passed":len(checks),"input_artifact_count":len(seen),"commit_byte_bound_inputs":len(tracked),"folded_statement_utf8_bytes":result["folded_statement_utf8_bytes"],"eight_steps":True,"links":len(links)}))