import pathlib,json,sys,hashlib,os,stat,traceback
run=pathlib.Path(".astis/semantic-neutral-20261111/p_kr_91de5a/run")
evidence=run/"evidence"
def digest(b): return hashlib.sha256(b).hexdigest()
def shellquote(s): return "'"+s.replace("'","'\"'\"'")+"'"
failure_script=(evidence/"finalizer_script.py").read_text(encoding="utf-8")
failure_input=(evidence/"finalizer_input.json").read_text(encoding="utf-8")
failure_output="Traceback (most recent call last):\n  File \"<string>\", line 36, in <module>\n    os.chmod(p,0o444)\n    ~~~~~~~~^^^^^^^^^\nPermissionError: [Errno 1] Operation not permitted: '.astis/semantic-neutral-20261111/p_kr_91de5a/run/original/input.canonical.json'\n"
failure_receipt={
 "tool":"tools.exec_command",
 "arguments":{"cmd":"python3 -c "+shellquote(failure_script)+" "+shellquote(failure_input)+" "+shellquote(failure_script),"workdir":"/Users/zhouhuanjian/ASTIS-GC","max_output_tokens":2000},
 "result":{"chunk_id":"6f0041","wall_time_seconds":0,"exit_code":1,"original_token_count":126,"output":failure_output+failure_output},
 "evidence_note":"Exact displayed exec_command result copied by the actor after the finalizer returned; the original caught traceback remains unchanged in finalizer_exception.original.txt. The failed command is reconstructed exactly from its own saved script and argv payload."
}
(evidence/"finalizer_failure_tool_receipt.json").write_text(json.dumps(failure_receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
(evidence/"recovery_script.py").write_text(sys.argv[1],encoding="utf-8")
created_failures=[]
def protect(p):
    st=p.stat()
    immutable=bool(getattr(st,"st_flags",0)&getattr(stat,"UF_IMMUTABLE",0))
    if immutable:
        if stat.S_IMODE(st.st_mode)!=0o444:
            raise RuntimeError("Already immutable file has unexpected mode: "+str(p))
        return
    if stat.S_IMODE(st.st_mode)!=0o444: os.chmod(p,0o444)
    if hasattr(os,"chflags") and hasattr(stat,"UF_IMMUTABLE"): os.chflags(p,stat.UF_IMMUTABLE)
try:
    before=[]
    actual_reads=[str(evidence/"finalizer_script.py"),str(evidence/"finalizer_input.json")]
    for p in sorted(run.rglob("*")):
        if p.is_file():
            b=p.read_bytes()
            actual_reads.append(str(p))
            protect(p)
            st=p.stat()
            before.append({"path":str(p.relative_to(run)),"sha256":digest(b),"bytes":len(b),"mode":oct(stat.S_IMODE(st.st_mode)),"flags":getattr(st,"st_flags",None),"uf_immutable":bool(getattr(st,"st_flags",0)&getattr(stat,"UF_IMMUTABLE",0))})
    final_manifest={
      "schema_version":1,
      "actor":"/root/neutral_decoder_91de5a",
      "source_text_visible":False,
      "status":"Original reconstruction unchanged; evidence finalization repaired by skipping already immutable files.",
      "files":before,
      "exclusions":["final_manifest.json (self-hash excluded)","final_receipt.json (contains final manifest hash)"],
      "supersedes_for_complete_run_inventory":"manifest.json",
      "previous_failed_finalization":{"exception_artifact":"evidence/finalizer_exception.original.txt","tool_receipt":"evidence/finalizer_failure_tool_receipt.json","reason":"Initial finalizer attempted chmod on an already UF_IMMUTABLE mode-0444 original file and received PermissionError. Original payload was not modified.","preserved_unchanged":True},
      "read_inventory_this_command":actual_reads,
      "input_exposure_limit":"Only the designated input packet was read for mathematical content; recovery reads only this actor's newly created run artifacts.",
      "freeze_policy":"Every file mode 0444 with UF_IMMUTABLE; directories mode 0555. Already immutable originals were never unlocked or rewritten.",
      "scope":"Reconstruction only; no mathematical proof, source verdict, normal verification or publication approval."
    }
    fm=(json.dumps(final_manifest,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
    mp=run/"final_manifest.json"
    mp.write_bytes(fm)
    assert mp.read_bytes()==fm
    protect(mp)
    receipt={
      "status":"frozen_after_preserved_finalization_failure",
      "actor":"/root/neutral_decoder_91de5a",
      "run_path":str(run),
      "source_text_visible":False,
      "final_manifest_sha256":digest(fm),
      "original_manifest_sha256":"f9851e5258869b842fba4fddae5a6fb39ea3ec29ed4f425919b5b3b7f4eecfc7",
      "reconstructed_text_sha256":"f56c7a92022f341b5b628d35cca0a33667b40f6b0fd96f739616db0d64726c03",
      "plain_string_sha256":"9929790b8441ef76e11338df2bf19b0d2fe34e1be3088c496ac58536ac2275e9",
      "reconstruction_json_sha256":"e27e06dd20504c1244ededa511014cf1ddb43fbf3ef348e8efbe6eccbcedbe32",
      "decoder_run_sha256":"d598f9c4d3d1b138036358a3b95df161242ee2efd5dc6e0da974d0864b66d02f",
      "actual_failed_commands":1,
      "unchanged_failure_artifact":"evidence/finalizer_exception.original.txt",
      "failure_scope":"Receipt finalization chmod only; reconstruction and its frozen original bytes remain unchanged.",
      "receipt_limits":"Exact initial read/hash/writer tool receipts and the displayed failed finalizer receipt are preserved. The successful recovery's internal result is this file and its final tool output. The recovery's outer tool envelope remains in conversation rather than causing an infinite chain.",
      "additional_own_artifact_read":"final_manifest.json was read back after creation solely to check byte equality.",
      "all_files_before_final_receipt_observed_mode_0444_and_immutable":all(v["mode"]=="0o444" and v["uf_immutable"] for v in before),
      "final_receipt_and_directories":"This receipt is frozen after writing; directory modes are set to 0555; the final process output reports observed values."
    }
    rb=(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
    rp=run/"final_receipt.json"
    rp.write_bytes(rb)
    protect(rp)
    for p in sorted([v for v in run.rglob("*") if v.is_dir()],key=lambda v:len(v.parts),reverse=True):
        if stat.S_IMODE(p.stat().st_mode)!=0o555: os.chmod(p,0o555)
    os.chmod(run,0o555)
    all_stats=[p.stat() for p in run.rglob("*") if p.is_file()]
    print(json.dumps({"status":receipt["status"],"run_path":str(run),"final_manifest_sha256":digest(fm),"final_receipt_sha256":digest(rb),"all_files_mode_0444":all(stat.S_IMODE(s.st_mode)==0o444 for s in all_stats),"all_files_uf_immutable":all(bool(getattr(s,"st_flags",0)&getattr(stat,"UF_IMMUTABLE",0)) for s in all_stats),"all_output_directory_modes_0555":all(stat.S_IMODE(p.stat().st_mode)==0o555 for p in [run]+[v for v in run.rglob("*") if v.is_dir()]),"actual_failed_commands_preserved":1,"new_failures":0,"source_text_visible":False},indent=2))
except Exception:
    failure=traceback.format_exc()
    (evidence/"recovery_failure.original.txt").write_text(failure,encoding="utf-8")
    print(failure,file=sys.stderr,end="")
    raise
