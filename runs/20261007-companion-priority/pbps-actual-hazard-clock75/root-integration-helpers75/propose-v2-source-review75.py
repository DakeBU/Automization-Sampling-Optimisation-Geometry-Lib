from pathlib import Path
import hashlib,json,os
r=Path('runs/20261007-companion-priority/pbps-clock-preproof75');old=r/'header75.proposed.lean';raw=old.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='05ffee849dcf32541a948c1e9539550f122db34274e69d5b64397003de914263'
a=b'ProbabilityTheory.expMeasure1';b='(ProbabilityTheory.expMeasure (1 : ℝ))'.encode();assert raw.count(a)==1;v2=raw.replace(a,b)
assert hashlib.sha256(v2).hexdigest()=='00c9f04ff2d9ed037e3d8eab926a1cddc9fe3679a8b320267c641b86a0c243ee'
p=r/'header75.v2.proposed.lean';assert not p.exists();p.write_bytes(v2)
def pin(p):
 p=Path(p);x=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(x),RAW_sha256=hashlib.sha256(x).hexdigest(),LF_sha256=hashlib.sha256(x.replace(b'\r\n',b'\n')).hexdigest())
out=r/'exact-API-overlay75.source-review-proposal.json';assert not out.exists()
out.write_text(json.dumps(dict(status='EXACT_PROPOSED_API_NAME_OVERLAY_ONLY_AWAITING_DISTINCT_SOURCE_REVIEW',actual_root_PID=os.getpid(),before=pin(old),proposed=pin(p),exact_old=a.decode(),exact_new=b.decode(),occurrences=1,all_other_bytes_identical=True,previous_review_verdicts_included=False,Statement_Seal=False,proof_search=False,new_SAU=False,Goal_complete=False),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('PROPOSED75 exact v2 header frozen for distinct source comparison; not a seal or adoption.')
