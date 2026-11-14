import hashlib,json,pathlib,sys
from datetime import datetime,timezone
R=pathlib.Path('/private/tmp/rt-pkt-5b83e1')
A='/root/neutral_decoder_5b83e1'
P='neutral_decoder_5b83e1_'
new=[]
def digest(b): return hashlib.sha256(b).hexdigest()
def enc(v): return (json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
def write(n,b):
    with (R/n).open('xb') as f: f.write(b)
    new.append(n)
    return b
def own(n): return (R/n).read_bytes()
records=json.loads(bytes.fromhex(sys.argv[1]).decode())
receipt_name=P+'execution.rawreceipt.json'
receipt=write(receipt_name,enc({
    'schema_version':1,'actor':A,
    'scope':'Actual already observed returns: first exec_command; the failed functions.exec preparation (its original error and executed failing expression are retained, with full wrapper source available only in tool history); collaboration.send_message; generation exec_command. The closing command is retained separately; no future enclosing tool-return metadata is invented.',
    'records':records
}))
runhash=digest(receipt)
fn=P+'reconstruction_fields.json'
f=json.loads(own(fn).decode())
audit=f.pop('_input_audit')
md=own('reconstructed_theorem.md')
if md!=f['reconstructed_theorem_text'].encode(): raise ValueError('Text-byte mismatch')
f['reconstructed_text_sha256']=digest(md)
cmdname=P+'seal.command.txt'
write(cmdname,('python3 '+str(R/(P+'seal.py'))+' '+sys.argv[1]+'\n').encode())
run={
    'schema_version':1,'actor':A,'task':'blind-theorem-reconstruction',
    'packet_id':audit['packet_id'],'packet_sha256':audit['declared_packet_sha256'],
    'input_path':str(R/'input.json'),'input_raw_sha256':audit['raw_sha256'],
    'input_byte_count':audit['byte_count'],'lean_statement_sha256':audit['statement_sha256_computed'],
    'canonical_packet_sha256_computed':audit['canonical_packet_sha256_computed'],
    'canonicalization':audit['canonicalization'],'input_hash_checks':audit['checks'],
    'input_scope':'Exact lean.statement, approved_definition_context, metadata and output_contract in input.json.',
    'only_read_input_declaration':'input.json was the sole pre-existing file read. Own newly generated files were read solely for assembly, byte checks and artifact hashing.',
    'source_text_visible':False,
    'source_recognition':{
        'particular_source_identified':False,
        'report':'I do not recognize a particular source, title, theorem number or source anchor. The trigonometric matrix expressions are mathematically familiar. Pretrained knowledge cannot guarantee zero prior encounter with a related or identical source.',
        'uncertain_context':'No unstated source context was used; the provided generic definitions suffice for this literal reconstruction.',
        'pristine_claim':False
    },
    'did_prove_or_compile':False,
    'compiled_flag_status':'compiled=true was supplied metadata; Lean was not executed.',
    'source_equivalence_verdict_given':False,
    'run_hash':runhash,'run_hash_definition':'SHA-256 of the retained execution.rawreceipt.json bytes; that receipt contains no run_hash.',
    'raw_receipt_path':str(R/receipt_name),'raw_receipt_sha256':runhash,
    'receipt_limit':'Full failed functions.exec wrapper source is in actual tool history, not mirrored in these files. Its raw error and failing expression are preserved. Closing seal stdout and command are separate artifacts; enclosing final tool metadata is not guessed.',
    'first_failure':{'tool':'functions.exec','error':'ReferenceError: TextEncoder is not defined','location':'exec_main.mjs:272:22','effect':'Preparation failed before exec_command; no corresponding shell command or file write started.'},
    'truncation_observed':False,
    'completed_before_closing_output_utc':datetime.now(timezone.utc).isoformat()
}
rb=write('decoder_run.json',enc(run))
f['decoder_run_sha256']=digest(rb)
write('reconstruction.json',enc(f))
initial=[P+'step01_input_read.raw.txt','reconstructed_theorem.md',fn,P+'seal.py',P+'step02_generation.stdout.raw.txt']
retained=initial+new
mn=P+'freeze_manifest.json'; rn=P+'freeze_receipt.json'; sn=P+'seal.stdout.raw.txt'
allnames=retained+['exposure.json',mn,rn,sn]
exposure={
    'schema_version':1,'actor':A,'packet_sha256':audit['declared_packet_sha256'],
    'source_text_visible':False,'source_recognized':False,'pristine_claim':False,
    'pretraining_zero_exposure_guaranteed':False,'recognition_report':run['source_recognition'],
    'inherited_exposure':'System/developer/runtime instructions, environment, generic tools/skills catalogs, configured command-prefix strings, and the assignment were visible before the read. No referenced skill, repository, directory inventory, source candidate, other role result or external page was opened. This is not a controlled zero-prior-exposure setting.',
    'pre_existing_file_reads':[
        {'event':'first exec_command','path':str(R/'input.json'),'sha256':audit['raw_sha256'],'bytes':audit['byte_count'],'visible_scope':'Whole input JSON including exact statement, generic definitions, metadata and output contract; full returned read output retained.'},
        {'event':'generation exec_command','path':str(R/'input.json'),'sha256':audit['raw_sha256'],'bytes':audit['byte_count'],'visible_scope':'Same bytes read programmatically to check raw, statement and canonical packet hashes.'}
    ],
    'own_generated_file_reads':{'purpose':'Assembly, equality checks and hash sealing only.','known_paths':[str(R/n) for n in retained+['exposure.json',mn]],'hash_record':str(R/mn)},
    'tool_commands_and_original_outputs':{
        'observed_returns_and_exact_exec_command_arguments':str(R/receipt_name),
        'failed_functions_exec_full_source':'Retained in actual tool history only; no API for reading that transcript was used. Artifact retains the raw returned error and exact failing expression; it does not pretend to be a full wrapper-source copy.',
        'closing_command_verbatim':str(R/cmdname),'closing_stdout_verbatim':str(R/sn),
        'closing_tool':'exec_command via functions.exec',
        'closing_result_metadata':'Available in actual tool response after this script returns; not fabricated in a pre-return file.'
    },
    'first_failure':run['first_failure'],
    'failure_raw_output_retained':True,'truncation_observed':False,
    'first_input_read_complete':'2668 bytes; both BEGIN_INPUT_JSON and END_INPUT_JSON were returned.',
    'no_external_search':True,'no_source_review_or_equivalence_verdict':True,
    'no_proof_verified_website_or_goal_action':True,
    'new_file_inventory':[str(R/n) for n in allnames],
    'closure_hash_rules':'Manifest hashes all retained non-closure artifacts. Separate freeze receipt hashes manifest. Terminal raw stdout gives manifest and freeze-receipt hashes. Their own hashes are excluded from themselves; terminal stdout hash is reported externally from the actual returned bytes.'
}
write('exposure.json',enc(exposure))
entries=[]
for n in retained+['exposure.json']:
    b=own(n);entries.append({'path':str(R/n),'sha256':digest(b),'bytes':len(b),'mode':'0444'})
manifest={
    'schema_version':1,'actor':A,'packet_sha256':audit['declared_packet_sha256'],
    'run_hash':runhash,'algorithm':'sha256','files':entries,
    'closure_exclusions':[
        {'path':str(R/mn),'hash_location':str(R/rn),'reason':'No self-hash.'},
        {'path':str(R/rn),'hash_location':str(R/sn),'reason':'No receipt self-hash.'},
        {'path':str(R/sn),'hash_location':'External final response computed from actual returned stdout.','reason':'Avoid cycle with terminal output committing the closure hashes.'}
    ]
}
mb=write(mn,enc(manifest))
fr={
    'schema_version':1,'actor':A,'packet_sha256':audit['declared_packet_sha256'],'run_hash':runhash,
    'manifest_path':str(R/mn),'manifest_sha256':digest(mb),'manifest_bytes':len(mb),
    'new_file_inventory':[str(R/n) for n in allnames],'final_mode_for_all_new_files':'0444',
    'self_hash':None,'self_hash_location':str(R/sn),'terminal_stdout_hash_location':'External final response from actual returned stdout.'
}
fb=write(rn,enc(fr))
summary={
    'actor':A,'packet_sha256':audit['declared_packet_sha256'],'run_hash':runhash,
    'reconstructed_text_sha256':f['reconstructed_text_sha256'],'decoder_run_sha256':digest(rb),
    'manifest_path':str(R/mn),'manifest_sha256':digest(mb),
    'freeze_receipt_path':str(R/rn),'freeze_receipt_sha256':digest(fb),
    'terminal_stdout_path':str(R/sn),'new_file_count':len(allnames),'all_new_files_mode':'0444',
    'hash_inventory':entries+[
        {'path':str(R/mn),'sha256':digest(mb),'bytes':len(mb),'mode':'0444'},
        {'path':str(R/rn),'sha256':digest(fb),'bytes':len(fb),'mode':'0444'}
    ],
    'limit':'Terminal stdout excludes its own hash. Full failed wrapper source is in actual tool history only; raw error and executed failing expression are retained.'
}
out=enc(summary)
write(sn,out)
for n in allnames:(R/n).chmod(0o444)
sys.stdout.buffer.write(out);sys.stdout.buffer.flush()
