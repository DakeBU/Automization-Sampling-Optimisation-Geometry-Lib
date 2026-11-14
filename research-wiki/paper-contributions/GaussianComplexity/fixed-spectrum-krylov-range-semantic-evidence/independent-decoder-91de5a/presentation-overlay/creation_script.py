import pathlib,sys,json,hashlib,re,stat
data=json.loads(sys.argv[1])
base=pathlib.Path(".astis/semantic-neutral-20261111/p_kr_91de5a")
original_run=base/"run"
source=original_run/"original"/"reconstructed_theorem.md"
overlay=base/"presentation-overlay"
overlay.mkdir()
def digest(b): return hashlib.sha256(b).hexdigest()
def inventory():
    out=[]
    for p in sorted(original_run.rglob("*")):
        st=p.stat()
        row={"path":str(p.relative_to(original_run)),"mode":oct(stat.S_IMODE(st.st_mode)),"flags":getattr(st,"st_flags",None)}
        if p.is_file():
            b=p.read_bytes()
            row.update({"kind":"file","bytes":len(b),"sha256":digest(b)})
        elif p.is_dir(): row["kind"]="directory"
        out.append(row)
    st=original_run.stat()
    out.insert(0,{"path":".","kind":"directory","mode":oct(stat.S_IMODE(st.st_mode)),"flags":getattr(st,"st_flags",None)})
    return out
try:
    before=inventory()
    raw=source.read_bytes()
    assert digest(raw)=="f56c7a92022f341b5b628d35cca0a33667b40f6b0fd96f739616db0d64726c03"
    runs=[]
    for m in re.finditer(rb"\x5c+",raw):
        runs.append({"source_start_byte":m.start(),"source_end_byte_exclusive":m.end(),"display_start_byte":m.start(),"display_end_byte_exclusive":m.end(),"backslash_count":len(m.group()),"hex":m.group().hex(),"classification":"required TeX cases row separator" if len(m.group())==2 else "single TeX command, delimiter or spacing escape"})
    double_runs=[r for r in runs if r["backslash_count"]>1]
    assert len(double_runs)==1
    assert double_runs[0]["backslash_count"]==2
    assert raw[double_runs[0]["source_end_byte_exclusive"]:double_runs[0]["source_end_byte_exclusive"]+1]==b"\n"
    counts={
      "literal_double_backslash_open_paren":raw.count(bytes((92,92,40))),
      "literal_double_backslash_close_paren":raw.count(bytes((92,92,41))),
      "literal_double_backslash_open_bracket":raw.count(bytes((92,92,91))),
      "literal_double_backslash_close_bracket":raw.count(bytes((92,92,93))),
      "single_backslash_open_paren":raw.count(bytes((92,40))),
      "single_backslash_close_paren":raw.count(bytes((92,41))),
      "single_backslash_open_bracket":raw.count(bytes((92,91))),
      "single_backslash_close_bracket":raw.count(bytes((92,93))),
      "backslash_run_count":len(runs),
      "runs_with_two_backslashes":len(double_runs),
      "runs_with_more_than_two_backslashes":sum(r["backslash_count"]>2 for r in runs)
    }
    assert all(counts[k]==0 for k in counts if k.startswith("literal_double"))
    display=raw
    (overlay/"display.md").write_bytes(display)
    mapping={
      "schema_version":1,
      "actor":"/root/neutral_decoder_91de5a",
      "source_text_visible":False,
      "purpose":"presentation-only, not mathematical/source repair; original canonical reconstruction unchanged",
      "result":"No escaping repair needed.",
      "source_path":str(source),
      "source_sha256":digest(raw),
      "source_bytes":len(raw),
      "display_path":str(overlay/"display.md"),
      "display_sha256":digest(display),
      "display_bytes":len(display),
      "transformation":{"name":"identity","definition":"T(b)=b for every byte b; preserve the entire byte sequence exactly, including every TeX row separator.","edits":[],"contiguous_byte_mapping":[{"source_start":0,"source_end_exclusive":len(raw),"display_start":0,"display_end_exclusive":len(display)}],"inverse":"The same identity mapping."},
      "counts":counts,
      "backslash_byte_mapping":runs,
      "row_separator_policy":"The single run of two literal backslashes is the TeX row separator inside the cases expression. It is preserved as exactly two bytes 5c5c; there is no global backslash collapsing.",
      "interpretation":"The original Markdown bytes contain single-backslash commands and delimiters. Doubled backslashes appearing inside a JSON string representation encode those single bytes and do not demonstrate doubled bytes in the original Markdown.",
      "exposure_limits":"Only this actor's designated original packet and own output artifacts are allowed. This task read only own run artifacts; no packet reread was needed. No source, repository source, Lean, network, API, Git or list_agents was accessed.",
      "semantic_status":"No mathematical wording, original reconstruction, original hash, original evidence, file mode or file flag was changed. This overlay grants no semantic or source verdict and requires separate source/reader comparison.",
      "renderer_limit":"No frontend renderer was invoked; the evidence determines literal escaping bytes only."
    }
    (overlay/"mapping.json").write_text(json.dumps(mapping,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (overlay/"scope.txt").write_text("presentation-only, not mathematical/source repair; original canonical reconstruction unchanged\nNo escaping repair needed. display.md is an exact byte copy of the frozen reconstructed_theorem.md. No semantic or source verdict is granted. Separate source/reader comparison remains required.\n",encoding="utf-8")
    (overlay/"inspection_tool_receipt.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (overlay/"creation_script.py").write_text(sys.argv[2],encoding="utf-8")
    (overlay/"creation_input.json").write_text(sys.argv[1],encoding="utf-8")
    after=inventory()
    assert before==after
    own_written=[]
    for p in sorted(overlay.iterdir()):
        if p.is_file():
            b=p.read_bytes()
            own_written.append({"path":p.name,"bytes":len(b),"sha256":digest(b)})
    receipt={
      "status":"identity_overlay_created",
      "actor":"/root/neutral_decoder_91de5a",
      "overlay_path":str(overlay),
      "source_text_visible":False,
      "purpose":"presentation-only, not mathematical/source repair; original canonical reconstruction unchanged",
      "no_repair_needed":True,
      "display_sha256":digest(display),
      "display_equals_original_bytes":True,
      "counts":counts,
      "original_run_unchanged_bytes_modes_flags":before==after,
      "original_run_before_and_after_inventory":before,
      "own_overlay_files_read_back":own_written,
      "read_inventory":"The initial inspection read run/original/reconstructed_theorem.md. This creation command read only the original run files listed here, before and after creating the overlay, plus the Markdown once directly. Newly created overlay files were read back only for local hashes.",
      "actual_failures":0,
      "receipt_scope":"Internal process receipt. The outer creation exec_command receipt will be saved during overlay finalization."
    }
    rt=json.dumps(receipt,ensure_ascii=False,indent=2)+"\n"
    (overlay/"creation_internal_receipt.json").write_text(rt,encoding="utf-8")
    print(json.dumps({"status":receipt["status"],"overlay_path":str(overlay),"display_sha256":digest(display),"no_repair_needed":True,"original_run_unchanged_bytes_modes_flags":True,"counts":counts,"actual_failures":0},indent=2))
except Exception:
    import traceback
    failure=traceback.format_exc()
    (overlay/"creation_failure.original.txt").write_text(failure,encoding="utf-8")
    print(failure,file=sys.stderr,end="")
    raise
