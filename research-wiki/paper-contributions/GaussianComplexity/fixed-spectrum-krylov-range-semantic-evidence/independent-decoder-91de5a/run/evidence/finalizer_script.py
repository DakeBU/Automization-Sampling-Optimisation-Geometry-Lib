import pathlib,sys,json,hashlib,os,stat,traceback
data=json.loads(sys.argv[1])
run=pathlib.Path(".astis/semantic-neutral-20261111/p_kr_91de5a/run")
evidence=run/"evidence"
(evidence/"writer_tool_receipt.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
(evidence/"finalizer_script.py").write_text(sys.argv[2],encoding="utf-8")
(evidence/"finalizer_input.json").write_text(sys.argv[1],encoding="utf-8")
def digest(b): return hashlib.sha256(b).hexdigest()
try:
    entries=[]
    read_inventory=[]
    for p in sorted(run.rglob("*")):
        if p.is_file():
            b=p.read_bytes()
            read_inventory.append(str(p))
            entries.append({"path":str(p.relative_to(run)),"sha256":digest(b),"bytes":len(b)})
    manifest={
      "schema_version":1,
      "actor":"/root/neutral_decoder_91de5a",
      "source_text_visible":False,
      "files":entries,
      "exclusions":["manifest.json (self-hash excluded)","finalization_receipt.json (contains manifest hash, excluded to avoid circular hashes)"],
      "original_manifest":"original/manifest.json",
      "freeze_policy":"Every file is mode 0444 and UF_IMMUTABLE; every output directory is mode 0555.",
      "verification_read_inventory":read_inventory,
      "receipt_evidence_limits":"The initial two exec_command receipts and the writer exec_command receipt are exact tool-return objects. The finalizer records its actual internal operations and output; the outer finalizer tool envelope remains in the conversation, avoiding an infinite receipt chain.",
      "status_scope":"Reconstruction only; no proof, source verdict, normal verification or publication approval."
    }
    manifest_bytes=(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
    mp=run/"manifest.json"
    mp.write_bytes(manifest_bytes)
    assert mp.read_bytes()==manifest_bytes
    failures=[]
    for p in sorted(run.rglob("*")):
        if p.is_file():
            os.chmod(p,0o444)
            if hasattr(os,"chflags") and hasattr(stat,"UF_IMMUTABLE"):
                try: os.chflags(p,stat.UF_IMMUTABLE)
                except Exception: failures.append({"path":str(p),"unchanged_traceback":traceback.format_exc()})
    if failures:
        fp=evidence/"finalizer_failure.original.json"
        fp.write_text(json.dumps(failures,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        os.chmod(fp,0o444)
    frozen=[]
    for p in sorted(run.rglob("*")):
        if p.is_file():
            st=p.stat()
            frozen.append({"path":str(p.relative_to(run)),"mode":oct(stat.S_IMODE(st.st_mode)),"flags":getattr(st,"st_flags",None),"uf_immutable":bool(getattr(st,"st_flags",0)&getattr(stat,"UF_IMMUTABLE",0))})
    receipt={
      "status":"frozen" if not failures else "frozen_with_preserved_failures",
      "actor":"/root/neutral_decoder_91de5a",
      "run_path":str(run),
      "run_manifest_sha256":digest(manifest_bytes),
      "run_manifest_bytes":len(manifest_bytes),
      "original_manifest_sha256":"f9851e5258869b842fba4fddae5a6fb39ea3ec29ed4f425919b5b3b7f4eecfc7",
      "reconstructed_text_sha256":"f56c7a92022f341b5b628d35cca0a33667b40f6b0fd96f739616db0d64726c03",
      "decoder_run_sha256":"d598f9c4d3d1b138036358a3b95df161242ee2efd5dc6e0da974d0864b66d02f",
      "files_observed_after_freeze":frozen,
      "actual_failure_count":len(failures),
      "read_inventory_note":"All reads by this finalizer were of its own run artifacts. Content files read before finalization are listed in manifest.json; manifest.json was additionally read to verify the exact bytes just written. File stat operations do not introduce content exposure.",
      "finalization_receipt_self_freeze":"This receipt is subsequently set to mode 0444 and UF_IMMUTABLE; the final process output reports the observed result. All output directories are subsequently set to mode 0555."
    }
    rb=(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
    rp=run/"finalization_receipt.json"
    rp.write_bytes(rb)
    os.chmod(rp,0o444)
    if hasattr(os,"chflags") and hasattr(stat,"UF_IMMUTABLE"):
        os.chflags(rp,stat.UF_IMMUTABLE)
    for p in sorted([v for v in run.rglob("*") if v.is_dir()],key=lambda v:len(v.parts),reverse=True):
        os.chmod(p,0o555)
    os.chmod(run,0o555)
    rst=rp.stat()
    print(json.dumps({"status":receipt["status"],"run_path":str(run),"run_manifest_sha256":digest(manifest_bytes),"finalization_receipt_sha256":digest(rb),"finalization_receipt_mode":oct(stat.S_IMODE(rst.st_mode)),"finalization_receipt_uf_immutable":bool(getattr(rst,"st_flags",0)&getattr(stat,"UF_IMMUTABLE",0)),"run_directory_mode":oct(stat.S_IMODE(run.stat().st_mode)),"actual_failures":len(failures),"read_source_text":False},indent=2))
except Exception:
    failure=traceback.format_exc()
    try: (evidence/"finalizer_exception.original.txt").write_text(failure,encoding="utf-8")
    except Exception: pass
    print(failure,file=sys.stderr,end="")
    raise
