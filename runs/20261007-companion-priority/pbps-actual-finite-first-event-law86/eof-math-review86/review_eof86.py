from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys
R=Path('E:/Samplinglib');O=Path(__file__).parent
B=R/'runs/20261007-companion-priority/pbps-actual-finite-first-event-law86'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def read(p):return json.loads(p.read_text('utf8'))
def put(n,v):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
proposal=B/'eof-whitespace-repair86/proposal.json'
assert pin(proposal)['raw_sha256']=='f2ce75c62f2c526028f75276ef0729e35ca96ca508bf9439658beabf6fa16ae6'
p=read(proposal); before=R/p['before']['path'];after=R/p['after']['path'];canonical=R/p['target']
old=before.read_bytes();new=after.read_bytes()
assert pin(before)['raw_sha256']=='cb8bd3e3ed053d114c6871ceaff24ab7782b46be405d69afe7174e0f4b7721d5'
assert pin(after)['raw_sha256']=='d6667ccbb917d6463e96b2082a5a26089950889fd20af4859052cd7a9a1db776'
assert len(old)==23001 and len(new)==23000
assert old==new+b'\n' and old.endswith(b'\n\n') and new.endswith(b'\n') and not new.endswith(b'\n\n')
assert canonical.read_bytes()==old
seal=B/'root.statement-seal86.json'; sealed=read(seal)['expanded_literal_Prop'].encode('utf8')
assert sealed in old and sealed in new
lesson=R/'website/content/declaration_lessons/pbps-actual-finite-first-event-law.json'
unit=read(lesson)['units'][0]; assert len(unit['steps'])==11
checks=[]
for k,s in enumerate(unit['steps']):
 q=s['lean_source_region'];lo=q['start_line'];hi=q['end_line']
 a=b''.join(old.splitlines(keepends=True)[lo-1:hi]);b=b''.join(new.splitlines(keepends=True)[lo-1:hi])
 assert a==b
 assert hashlib.sha256(a).hexdigest()==q['exact_code_raw_sha256']
 assert a.decode()==s['lean']
 checks.append(dict(step=k+1,start_line=lo,end_line=hi,byte_identical=True,raw_sha256=hashlib.sha256(a).hexdigest()))
toolchain=R/'lean-toolchain';manifest=R/'lake-manifest.json'
assert pin(toolchain)['raw_sha256']=='b2b5068d5a4835675e651ce83b29c0ddb308d28b80076e7c007aef4630af0477'
assert pin(manifest)['raw_sha256']=='b1f16b43aaf4a886cfe0382d5e3ae63d6904281c00afd8f35af20f0270a747e2'
mathdecision=B/'independent-math86/decision86.json';kernel=B/'independent-math86/kernel-dependency-summary86.json';mathmanifest=B/'independent-math86/closed-RAW-manifest86.json';priorreceipt=B/'independent-math86/fresh-whole-module.receipt.json'
assert pin(mathdecision)['raw_sha256']=='75b2a3a1219e8b7ebdd090a50dd718bcd2714aa1e78182692e0181c6323ecab9'
assert pin(kernel)['raw_sha256']=='f20414e498d36b17d564402e4ae464068fa779f939b7cbe3e3ee17d130b5df07'
assert read(kernel)['standard_axioms_only']
assert read(priorreceipt)['exit_code']==0
put('input-freeze86.json',dict(created_utc=now(),inputs=[pin(x) for x in [proposal,before,after,canonical,seal,lesson,toolchain,manifest,mathdecision,kernel,mathmanifest,priorreceipt]],canonical_before=pin(canonical)))
put('byte-comparison86.json',dict(status='PASS_EXACT_ONE_FINAL_LF_REMOVAL',created_utc=now(),before=pin(before),after=pin(after),exact_relation='before == after + b"\\n"',removed_offset_zero_based=23000,removed_hex='0a',remaining_final_newline=True,all_preceding_23000_bytes_identical=True,sealed_complete_private_Prop_byte_identical=True,five_helpers_and_six_public_BODY_regions=checks,proof_term_effect='All mathematical source tokens including private helpers, generated-proof source and public BODY are byte-identical. Prior axiom/kernel evidence reused on that identity; no new kernel closure extraction claimed.',source_blind_statement='The literal statement is unchanged; no new anonymous packet or source verdict consulted.'))
put('read-path-diagnosis86.json',dict(status='CORRECTED_LOOKUP_ONLY',description='Initial read attempted nonexistent independent-math86/full-source.receipt.json; rg located actual fresh-whole-module.receipt.json. No inference from failed lookup; actual native receipt is pinned.',mathematical_change=False))
cmd=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env',str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe'),str(after)]
start=now();proc=subprocess.Popen(cmd,cwd=R,env=dict(os.environ,PYTHONUTF8='1'),stdout=subprocess.PIPE,stderr=subprocess.PIPE);stdout,stderr=proc.communicate()
for n,v in [('fresh-proposed-source.stdout.log',stdout),('fresh-proposed-source.stderr.log',stderr)]:
 with (O/n).open('xb') as f:f.write(v)
put('fresh-proposed-source.receipt.json',dict(command=cmd,cwd=str(R),actual_foreground_PID=proc.pid,started_utc=start,finished_utc=now(),exit_code=proc.returncode,terminal_closed=True,source=pin(after),stdout=pin(O/'fresh-proposed-source.stdout.log'),stderr=pin(O/'fresh-proposed-source.stderr.log'),toolchain=pin(toolchain),lake_manifest=pin(manifest),native_reasoning_trajectory_claimed=False))
assert proc.returncode==0, stderr.decode('utf8',errors='replace')
assert canonical.read_bytes()==old and after.read_bytes()==new
put('decision86.json',dict(status='ACCEPT_EXACT_EOF_WHITESPACE_ONLY_PROPOSAL',reviewer_id='/root/exact_verify77',created_utc=now(),scope='One final LF removal only; no full mathematical re-review or VERIFIED admission.',checked_proposal=pin(proposal),before=pin(before),accepted_candidate=pin(after),byte_comparison=pin(O/'byte-comparison86.json'),fresh_whole_source_elaboration=pin(O/'fresh-proposed-source.receipt.json'),reused_unchanged_math=pin(mathdecision),reused_kernel_axioms=pin(kernel),conclusion='Full sealed private Prop, six original assumptions, fourteen literal definitions, five helpers and six public BODY regions are byte-identical. Existing standard-three-axiom/kernel mathematics acceptance transfers across this EOF-only edit; fresh complete proposed-source fixed Lean elaboration EXIT0.',required_repairs=[],canonical_module_mutated=False,VERIFIED=False,remaining='Root application and metadata full-file RAW rebinding, later exact science admission and all existing global/open truth boundaries.'))
inputs=read(O/'input-freeze86.json')['inputs']
put('run-manifest86.json',dict(status='CLOSED',reviewer_id='/root/exact_verify77',created_utc=now(),actual_inputs=inputs,command_receipt=pin(O/'fresh-proposed-source.receipt.json'),decision=pin(O/'decision86.json'),ownership='Only eof-math-review86 outputs written; canonical module and all prior native snapshots preserved.',native_receipt_terminal_exit=0))
artifacts=[pin(x) for x in sorted(O.iterdir()) if x.is_file() and x.name!='closed-RAW-manifest86.json']
put('closed-RAW-manifest86.json',dict(status='CLOSED',reviewer_id='/root/exact_verify77',created_utc=now(),frozen_current_inputs=inputs,owned_artifacts=artifacts,self_hash_policy='Excludes itself; reported in terminal and final.',canonical_mutation=False))
for q in inputs+artifacts:assert pin(R/q['path'])['raw_sha256']==q['raw_sha256']
print(json.dumps(dict(status='ACCEPT_TERMINAL0_CLOSED_REHASH_PASS',decision=pin(O/'decision86.json'),manifest=pin(O/'closed-RAW-manifest86.json'),receipt=pin(O/'fresh-proposed-source.receipt.json'),candidate=pin(after))))
