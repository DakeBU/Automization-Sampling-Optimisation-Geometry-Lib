import pathlib,sys,json,hashlib,os,stat,traceback
data=json.loads(sys.argv[1])
overlay=pathlib.Path(".astis/semantic-neutral-20261111/p_kr_91de5a/presentation-overlay")
def digest(b): return hashlib.sha256(b).hexdigest()
try:
    (overlay/"creation_tool_receipt.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (overlay/"finalization_script.py").write_text(sys.argv[2],encoding="utf-8")
    (overlay/"finalization_input.json").write_text(sys.argv[1],encoding="utf-8")
    entries=[]
    reads=[]
    for p in sorted(overlay.iterdir()):
        if p.is_file():
            b=p.read_bytes()
            reads.append(str(p))
            entries.append({"path":p.name,"bytes":len(b),"sha256":digest(b),"frozen_mode":"0o444"})
    mapping=json.loads((overlay/"mapping.json").read_bytes())
    manifest={
      "schema_version":1,
      "actor":"/root/neutral_decoder_91de5a",
      "source_text_visible":False,
      "purpose":"presentation-only, not mathematical/source repair; original canonical reconstruction unchanged",
      "result":"No escaping repair needed; identity mapping and byte-identical display copy.",
      "files":entries,
      "exclusions":["manifest.json (self-hash excluded)","finalization_receipt.json (contains manifest hash)"],
      "display_sha256":mapping["display_sha256"],
      "source_sha256":mapping["source_sha256"],
      "mapping_sha256":next(v["sha256"] for v in entries if v["path"]=="mapping.json"),
      "original_run_status":"Creation receipt proves all original run bytes, modes and flags match before/after inventory. This finalization performs writes only within presentation-overlay.",
      "freeze_policy":"All overlay files mode 0444; overlay directory mode 0555; no file flags are set by this overlay workflow.",
      "read_inventory_this_command":reads+["mapping.json read again for machine mapping extraction"],
      "evidence_limits":"Original inspection and overlay creation exec_command receipts are exact tool-return objects. Finalizer actual internal receipt and output are retained; its outer tool envelope remains in the conversation.",
      "semantic_verdict":None,
      "separate_source_reader_comparison_required":True
    }
    mb=(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
    mp=overlay/"manifest.json"
    mp.write_bytes(mb)
    assert mp.read_bytes()==mb
    result={
      "status":"frozen_identity_presentation_overlay",
      "actor":"/root/neutral_decoder_91de5a",
      "overlay_path":str(overlay),
      "purpose":"presentation-only, not mathematical/source repair; original canonical reconstruction unchanged",
      "source_text_visible":False,
      "no_repair_needed":True,
      "display_sha256":mapping["display_sha256"],
      "mapping_sha256":manifest["mapping_sha256"],
      "manifest_sha256":digest(mb),
      "actual_failures":0,
      "original_run_written_by_this_command":False,
      "file_flags_set_by_overlay_workflow":False,
      "receipt_scope":"Actual internal completion receipt; modes are applied and observed before final tool output."
    }
    rb=(json.dumps(result,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
    rp=overlay/"finalization_receipt.json"
    rp.write_bytes(rb)
    for p in overlay.iterdir():
        if p.is_file(): os.chmod(p,0o444)
    os.chmod(overlay,0o555)
    states=[p.stat() for p in overlay.iterdir() if p.is_file()]
    output=dict(result)
    output.update({"finalization_receipt_sha256":digest(rb),"all_overlay_files_mode_0444":all(stat.S_IMODE(s.st_mode)==0o444 for s in states),"overlay_directory_mode":oct(stat.S_IMODE(overlay.stat().st_mode)),"all_overlay_file_flags_zero":all(getattr(s,"st_flags",0)==0 for s in states)})
    print(json.dumps(output,indent=2))
except Exception:
    failure=traceback.format_exc()
    (overlay/"finalization_failure.original.txt").write_text(failure,encoding="utf-8")
    print(failure,file=sys.stderr,end="")
    raise
