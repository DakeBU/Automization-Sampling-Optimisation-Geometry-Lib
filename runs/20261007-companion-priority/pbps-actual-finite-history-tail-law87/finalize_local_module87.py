from pathlib import Path
import json,hashlib,datetime
R=Path('E:/Samplinglib');r=Path(__file__).parent;p=r/'implementation87.lean'
raw=p.read_bytes();s=raw.decode('utf-8');assert json.loads((r/'focused/explicit-factorization7/receipt.json').read_bytes())['exit_code']==0
assert hashlib.sha256(raw).hexdigest()==json.loads((r/'focused/explicit-factorization7/receipt.json').read_bytes())['module_raw_sha256']
sealed=json.loads((r/'root.statement-seal87.json').read_bytes())['expanded_literal_Prop']
assert s.split('private def ',1)[1].split('\n\nset_option',1)[0].strip()==sealed.strip()
s='\n'.join(line for line in s.split('\n') if not line.lstrip().startswith('trace "87:'))
s=s.replace('Prospective header87. Source-implicit deterministic-depth probability bridge.','Source-implicit deterministic-depth probability bridge.\n+Chen--Chewi--Lu--Zhang, arXiv:2609.06905v1, Appendix A.1 (A.1),(A.2),\n+the unused-input bridge implicit in (A.7), and Appendix A.2 Borel recursion.\n+The prefix/tail argument is an attributed ASTIS completion.').replace('\n+','\n')
assert s.split('private def ',1)[1].split('\n\nset_option',1)[0].strip()==sealed.strip()
dest=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryTailLaw.lean';assert not dest.exists();dest.write_text(s,encoding='utf-8',newline='\n')
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'previous_raw_sha256':hashlib.sha256(raw).hexdigest(),'production_module_raw_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'sealed_Prop_unchanged':True,'changes_after_initial_compile':'Remove diagnostic traces only; add exact source attribution outside theorem statement. Full production focused compile and independent reviews pending.','status':'LOCAL_SOURCE_CREATED_REVIEW_PENDING','PROVED_LOCAL':False,'VERIFIED':False}
(r/'local-finalization87.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8',newline='\n')
print(receipt)
