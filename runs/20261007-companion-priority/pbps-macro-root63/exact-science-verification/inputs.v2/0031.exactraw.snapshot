from pathlib import Path
import json,hashlib,re,os
r=Path('runs/20261007-companion-priority/pbps-macro-root-preproof63');load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
records=[]
for i in range(2):
 d=r/f'named-type{i}-ambient-corrected';q=load(d/'receipt.json');s=(d/'stdout.log').read_text(encoding='utf-8')
 errors=re.findall(r'^.*?:\d+:\d+: error[^\n]*$',s,re.M)
 assert q['exit_code']==1 and q['terminal_closed'] and len(errors)==1 and f'ASTIS63_NAMED_TYPE_{i}_ELABORATED_NO_PROOF' in errors[0]
 assert not (d/'stderr.log').read_bytes()
 for p in q['inputs']:
  b=Path(p['path']).read_bytes();assert sha(b)==p['raw_sha256'] and sha(b.replace(b'\r\n',b'\n'))==p['lf_sha256']
 header=(r/f'header{i}.lean').read_text(encoding='utf-8');named=(r/f'named-type{i}.lean').read_text(encoding='utf-8')
 assert header+f':= by\n  fail "ASTIS63_NAMED_TYPE_{i}_ELABORATED_NO_PROOF"\n' in named
 records.append(dict(receipt=str(d/'receipt.json'),actual_compiler_pid=q['actual_foreground_pid'],actual_compiler_exit_code=1,only_expected_deliberate_fail_marker=True,header_raw_sha256=sha((r/f'header{i}.lean').read_bytes()),named_TYPE_raw_sha256=sha((r/f'named-type{i}.lean').read_bytes())))
out=r/'root.named-types63.adoption.json';assert not out.exists();out.write_text(json.dumps(dict(status='BOTH_FULL_NAMED_THEOREM_TYPES_ELABORATED_NO_PROOF',actual_adopter_pid=os.getpid(),records=records,initial_negative=str(r/'named-type0-initial/receipt.json'),correction='Ambient Product measurable instance restored internally; same source domains and public assumptions.',mathematical_proof=False,statement_seal=False,claimed=False),indent=2)+'\n',encoding='utf-8',newline='\n')
print('Both full named63 producer/consumer TYPES elaborate: sole deliberate fail marker each, actual compiler EXIT1 retained; no proof/claim/seal.')
