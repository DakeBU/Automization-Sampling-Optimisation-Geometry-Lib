import pathlib, json, hashlib, sys, os, stat, traceback
data=json.loads(sys.argv[1])
base=pathlib.Path(".astis/semantic-neutral-20261111/p_kr_91de5a")
run=base/"run"
run.mkdir()
original=run/"original"
evidence=run/"evidence"
original.mkdir()
evidence.mkdir()
(evidence/"write_script.py").write_text(sys.argv[2],encoding="utf-8")
(evidence/"write_payload.json").write_text(sys.argv[1],encoding="utf-8")
(evidence/"initial_tool_receipts.json").write_text(json.dumps(data["read_receipts"],ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def digest(b): return hashlib.sha256(b).hexdigest()
def canonical(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")
try:
    source=base/"input.json"
    raw=source.read_bytes()
    assert digest(raw)=="456c06a158477e5b3fed15fb6ed7d69a5c7a15e5776f26387f48478016f6224b"
    packet=json.loads(raw)
    core=dict(packet)
    core.pop("packet_sha256")
    canonical_packet=canonical(core)
    assert digest(canonical_packet)==packet["packet_sha256"]
    rendered=data["rendered"].encode("utf-8")
    plain=data["plain"].encode("utf-8")
    reconstruction=data["semantic"]
    reconstruction["reconstructed_text_sha256"]=digest(rendered)
    reconstruction["plain_string_sha256"]=digest(plain)
    reconstruction["decoder_run_sha256"]=digest(canonical(reconstruction))
    inventory={
      "schema_version":1,
      "actor":data["actor"],
      "source_text_visible":False,
      "content_input_files":[{"path":str(source),"raw_sha256":digest(raw),"read_count":3,"read_purposes":["First tool call: obtain exact raw hash, byte length and packet text.","Second tool call: independently recompute statement and canonical packet hashes.","This creation command: copy and verify the exact input bytes; reconstruction content was already composed."]}],
      "other_existing_task_files_read":[],
      "other_exposures":["Source-blind task instructions and system/developer tool and environment instructions."],
      "own_artifact_verification":"This command will read the files it has just created under run/original to compare their exact hashes. The resulting actual verification record is saved in evidence/write_internal_receipt.json. No pre-existing file other than the designated input is read.",
      "forbidden_operations_used":[],
      "source_search_performed":False,
      "network_or_api_retrieval_performed":False,
      "lean_or_git_executed":False,
      "source_identity_inferred":False
    }
    files={
      "input.raw.json":raw,
      "input.canonical.json":canonical_packet,
      "reconstructed_theorem.md":rendered,
      "reconstructed_theorem.txt":plain,
      "reconstruction.json":(json.dumps(reconstruction,ensure_ascii=False,indent=2)+"\n").encode("utf-8"),
      "read_inventory.json":(json.dumps(inventory,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
    }
    for name,b in files.items():
        (original/name).write_bytes(b)
    immutable_failures=[]
    def freeze_file(path):
        os.chmod(path,0o444)
        if hasattr(os,"chflags") and hasattr(stat,"UF_IMMUTABLE"):
            try:
                os.chflags(path,stat.UF_IMMUTABLE)
            except Exception:
                failure=traceback.format_exc()
                immutable_failures.append({"path":str(path),"unchanged_traceback":failure})
    for name in files:
        freeze_file(original/name)
    entries=[]
    actual_reads=[]
    for name,expected in files.items():
        p=original/name
        actual=p.read_bytes()
        actual_reads.append(str(p))
        assert actual==expected, name
        st=p.stat()
        entries.append({"path":name,"sha256":digest(actual),"bytes":len(actual),"mode":oct(stat.S_IMODE(st.st_mode)),"flags":getattr(st,"st_flags",None),"uf_immutable":bool(getattr(st,"st_flags",0)&getattr(stat,"UF_IMMUTABLE",0))})
    manifest={
      "schema_version":1,
      "actor":data["actor"],
      "original_payload":True,
      "preserve_bytes":True,
      "files":entries,
      "manifest_self_hash":"Excluded to avoid a recursive self-hash. The actual manifest hash is in the write receipt and parent report.",
      "freeze_mechanism":"Files set to mode 0444; UF_IMMUTABLE requested where this Python/platform supports os.chflags; original directory set to mode 0555 after manifest creation.",
      "failure_count":len(immutable_failures)
    }
    manifest_bytes=(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
    manifest_path=original/"manifest.json"
    manifest_path.write_bytes(manifest_bytes)
    freeze_file(manifest_path)
    manifest_actual=manifest_path.read_bytes()
    actual_reads.append(str(manifest_path))
    assert manifest_actual==manifest_bytes
    if immutable_failures:
        (evidence/"immutable_failures.original.json").write_text(json.dumps(immutable_failures,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    os.chmod(original,0o555)
    mst=manifest_path.stat()
    receipt={
      "status":"written_and_verified",
      "actor":data["actor"],
      "run_path":str(run),
      "source_text_visible":False,
      "input_raw_sha256":digest(raw),
      "canonical_packet_sha256":digest(canonical_packet),
      "reconstructed_text_sha256":digest(rendered),
      "plain_string_sha256":digest(plain),
      "decoder_run_sha256":reconstruction["decoder_run_sha256"],
      "original_manifest_sha256":digest(manifest_actual),
      "original_manifest_bytes":len(manifest_actual),
      "manifest_mode":oct(stat.S_IMODE(mst.st_mode)),
      "manifest_flags":getattr(mst,"st_flags",None),
      "manifest_uf_immutable":bool(getattr(mst,"st_flags",0)&getattr(stat,"UF_IMMUTABLE",0)),
      "original_directory_mode":oct(stat.S_IMODE(original.stat().st_mode)),
      "original_files_verified":entries,
      "own_artifact_read_inventory":actual_reads,
      "actual_failures_preserved":len(immutable_failures),
      "failure_artifact":str(evidence/"immutable_failures.original.json") if immutable_failures else None,
      "receipt_scope":"Internal process receipt for actual writes, byte comparisons, stat results and freeze operations. The outer exec_command receipt is preserved separately after the tool returns."
    }
    receipt_text=json.dumps(receipt,ensure_ascii=False,indent=2)+"\n"
    (evidence/"write_internal_receipt.json").write_text(receipt_text,encoding="utf-8")
    print(receipt_text,end="")
except Exception:
    failure=traceback.format_exc()
    (evidence/"creation_failure.original.txt").write_text(failure,encoding="utf-8")
    print(failure,file=sys.stderr,end="")
    raise
