from pathlib import Path
import hashlib,json,os,re
r=Path('runs/20261007-companion-priority/pbps-polar-preproof65');sha=lambda b:hashlib.sha256(b).hexdigest();rows=[]
for label,name,sentinel in [('type-header65','header.candidate.lean','__ASTIS_TYPE_ONLY_UNDEFINED_POLAR65__'),('type-consumer65','test.candidate.lean','__ASTIS_TYPE_ONLY_UNDEFINED_CONSUMER65__')]:
 d=r/label;x=json.loads((d/'receipt.json').read_bytes());s=(r/name).read_text(encoding='utf-8');body=s[:s.rindex(':= by')].count('\n')+1
 assert x['exit_code']==1 and x['terminal_closed'] and s.splitlines()[body].strip()==sentinel
 log=(d/'stdout.log').read_text(encoding='utf-8')+(d/'stderr.log').read_text(encoding='utf-8')
 errors=re.findall(r'^.*?:(\d+):(\d+): error: ([^\n]+)',log,re.M)
 assert len(errors)==2 and sorted(e[2] for e in errors)==['unknown tactic','unsolved goals']
 assert all(int(e[0])>=body for e in errors) and {int(e[0]) for e in errors}=={body,body+1}
 for q in x['inputs']:
  b=Path(q['path']).read_bytes();assert sha(b)==q['raw_sha256'] and sha(b.replace(b'\r\n',b'\n'))==q['lf_sha256']
 rows.append(dict(candidate=name,header_BODY_line=body,actual_foreground_pid=x['actual_foreground_pid'],actual_exit_code=1,all_errors_only_intentional_unproved_BODY=True,diagnostics=errors,receipt=(d/'receipt.json').as_posix(),candidate_RAW_sha256=sha((r/name).read_bytes())))
out=r/'root.type-only65.adoption.json';assert not out.exists()
out.write_text(json.dumps(dict(status='HEADERS_ELABORATE_ONLY_INTENTIONAL_UNPROVED_BODY_DIAGNOSTICS',actual_reader_pid=os.getpid(),checks=rows,compiler_success=False,theorem_compiled=False,proof_search=False,Statement_Seal=False,SAU_claim=False),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('TYPE-only65:both headers elaborate; actual Lean EXIT1 retained, solely2 intentional BODY diagnostics each; no compiled theorem or seal.')
