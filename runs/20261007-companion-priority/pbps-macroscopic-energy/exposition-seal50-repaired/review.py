import pathlib,subprocess,json,hashlib,sys
sys.stdout.reconfigure(encoding="utf8")
R=pathlib.Path("E:/Samplinglib");B="runs/20261007-companion-priority/pbps-macroscopic-energy/";O=R/(B+"exposition-seal50-repaired");C="161c2337f23807bfd01d99be95cdd18442a58fee";P="6b6877482d1c4316b9a8009ebc8d0b0cff6e10cf";seen={};checks={}
def sha(b):return hashlib.sha256(b).hexdigest()
def bind(p,b):
 d={"path":p,"bytes":len(b),"raw_sha256":sha(b)}
 if not p.endswith(".png"):d["lf_sha256"]=sha(b.decode("utf8").replace("\r\n","\n").replace("\r","\n").encode())
 return d
def read(p):b=(R/p).read_bytes();seen[p]=bind(p,b);return b
def load(p):return json.loads(read(p))
def check(k,v):
 checks[k]=bool(v)
 if not v:raise AssertionError(k)
def git(p,c=C):return subprocess.check_output(["git","show",c+":"+p],cwd=R)
check("actual_HEAD",subprocess.check_output(["git","rev-parse","HEAD"],cwd=R).decode().strip()==C)
check("exact_parent",subprocess.check_output(["git","rev-parse",C+"^"],cwd=R).decode().strip()==P)
op=load(B+"integration-cell-overlay50/operations.json")
orig=load(B+"exposition-seal50/receipt.json");old=load(B+"exposition-seal50/bindings.json");oldrun=load(B+"exposition-seal50/run.json")
check("original_negative_receipt_raw_preserved",seen[B+"exposition-seal50/receipt.json"]["raw_sha256"]=="64e49476d508fa0f53f5e0da89801c14aae120fd5c7e21547f1ea3fe2d00b4a6")
check("original_negative_status_preserved",orig["status"]=="BLOCKED_EXACT_COMMIT_GRAPH_INPUT_CLOSURE_WITH_REUSABLE_READER_PASS")
check("original48_reader_checks_preserved",sum(old["checks"].values())==48 and [k for k,v in old["checks"].items() if not v]==["EXACT_COMMIT_FRONTIER_CELL_MATCHES_WORKING_GRAPH_INPUT","INTEGRATION_NOTES_BIND_CURRENT50_CELL"])
payload=oldrun["run_payload"]
check("original_ordered_run_logical_digest_preserved",sha(json.dumps(payload,ensure_ascii=False,separators=(",",":")).encode())==oldrun["review_run_sha256"])
for a in payload["inputs"]+payload["outputs"]+[payload["expected_final_closed_lease"]]:
 b=read(a["path"]);check("old_run_bound_"+pathlib.Path(a["path"]).name,sha(b)==a["raw_sha256"] and len(b)==a["bytes"])
closed=json.loads(read(payload["expected_final_closed_lease"]["path"]))
check("original_role_lease_remains_closed",all(closed[x]=="CLOSED" for x in ["status","read_lease","write_lease","compiler_lease"]))
note_path=B+"integration.notes.json";cp="research-wiki/frontier-cells/ASTIS-SW-PBPS-macroscopic-energy.json"
notes=load(note_path);cell=load(cp)
check("new_notes_exact_commit_raw",read(note_path)==git(note_path))
check("new_cell_exact_commit_raw",read(cp)==git(cp))
check("staged_same_prior_working_cell_not_rewritten",seen[cp]["raw_sha256"]==next(x["raw_sha256"] for x in old["input_artifacts"] if x["path"]==cp))
check("cell_verified",cell["status"]=="independently_verified")
check("shared_gate_evidence_retained","serialized_shared_gate" in cell["evidence"])
check("exact_shared_PASS_9153_9435_record_retained",cell["evidence"]["serialized_shared_gate"]["status"]=="PASS" and cell["evidence"]["serialized_shared_gate"]["root_jobs"]==9153 and cell["evidence"]["serialized_shared_gate"]["test_jobs"]==9435)
before_note_p=B+"integration-cell-overlay50/notes.before.6b.raw.snapshot.json";before_cell_p=B+"integration-cell-overlay50/cell.before.6b.raw.snapshot.json";after_cell_p=B+"integration-cell-overlay50/cell.after.working.raw.snapshot.json"
before_note_b=read(before_note_p);before_cell_b=read(before_cell_p);after_cell_b=read(after_cell_p)
check("before_notes_exact6b",before_note_b==git(note_path,P))
check("before_cell_exact6b",before_cell_b==git(cp,P))
check("after_cell_snapshot_exact_current_commit",after_cell_b==read(cp))
for field in ["before_notes","after_notes","before_cell","after_cell"]:
 a=op[field];b=read(a["path"]);check("operations_raw_lf_binding_"+field,len(b)==a["bytes"] and seen[a["path"]]["raw_sha256"]==a["raw_sha256"] and seen[a["path"]].get("lf_sha256")==a["lf_sha256"])
before_notes=json.loads(before_note_b);repaired=dict(notes);provenance=repaired.pop("integration_metadata_repair")
expected=json.loads(before_note_b);expected["shared_files"][6]=seen[cp]
check("notes_only_currentcell_row_plus_repair_provenance",repaired==expected)
check("notes_current50cell_row_hashes_exact",notes["shared_files"][6]==seen[cp])
check("repair_provenance_original_commit",provenance["original_commit"]==P)
negativeproof=provenance["original_negative_proofseal"];proofb=read(negativeproof["path"])
check("original_ProofSeal_negative_raw_preserved",sha(proofb)=="e17343882a5a2eff2de65551e6e99bbc0b6a8b56a40d43be86908582ed4b0f10"==negativeproof["raw_sha256"])
check("original_negative_receipts_now_committed",git(B+"exposition-seal50/receipt.json")==read(B+"exposition-seal50/receipt.json") and git(negativeproof["path"])==proofb)
unchanged=[];exceptions=[]
for a in old["input_artifacts"]:
 b=read(a["path"])
 if a["path"]==note_path:exceptions.append({"path":a["path"],"reason":"Reviewed exact metadata repair"});continue
 check("prior_reader_visual_input_unchanged_"+a["path"],seen[a["path"]]["raw_sha256"]==a["raw_sha256"] and len(b)==a["bytes"])
 unchanged.append(seen[a["path"]])
for a in before_notes["checks"]:
 b=read(a["path"]);check("original_gate_artifact_preserved_"+a["path"],sha(b)==a["raw_sha256"] and len(b)==a["bytes"])
check("all_gate_records_and_visual_provenance_unchanged",notes["checks"]==before_notes["checks"] and notes["visual_inspection"]==before_notes["visual_inspection"])
changes=subprocess.check_output(["git","diff","--name-only",P,C],cwd=R).decode().splitlines()
allowed=lambda p:p in [cp,note_path] or p.startswith(B+"integration-cell-overlay50/") or p.startswith(B+"exposition-seal50/") or p.startswith(B+"repository-seal50/")
check("commit_changes_only_exact_metadata_and_retained_review_artifacts",all(allowed(p) for p in changes))
images=[a for a in unchanged if a["path"].endswith(".png")]
check("all_four_actual_viewed_PNGs_byte_unchanged",len(images)==4)
result={"schema_version":1,"status":"BOUNDED_EXACT_METADATA_REPAIR_ACCEPTED","checked_commit":C,"parent_commit":P,"reviewer":"/root/anonymous_decoder_49","checks":checks,"input_artifacts":list(seen.values()),"unchanged_prior_reader_inputs":unchanged,"reviewed_exception":exceptions,"original_negative_receipt":seen[B+"exposition-seal50/receipt.json"],"original_negative_proofseal":seen[negativeproof["path"]],"original_run":seen[B+"exposition-seal50/run.json"],"original_reader_checks_reused":48,"unchanged_images":images,"new_cell_status":cell["status"],"new_cell_binding":seen[cp],"new_notes_binding":seen[note_path],"graph_digest_reused":old["graph_publication_inputs_sha256"],"original_source_expansion_nodes":old["source_expansion_nodes"],"original_lean_expansion_nodes":old["lean_expansion_nodes"],"copy_download":old["copy_download"],"original_scoped_receipt_full_debt_retained":orig["presentation_debt"],"actual_visual_inspection_reused":"All four images actually viewed in prior closed exposition task; no new browser/image review asserted.","git_changed_paths":changes,"compiler_started":False,"source_text_visible":True,"source_fidelity_or_proof_admission":False}
(O/"bindings.json").write_bytes((json.dumps(result,ensure_ascii=False,indent=2)+"\n").encode())
print(json.dumps({"status":result["status"],"repair_checks":len(checks),"reused48checks":True,"unchanged_prior_inputs":len(unchanged),"images":len(images),"cell_status":cell["status"],"old_negatives_preserved":True}))