from pathlib import Path
import hashlib,json
O=Path(__file__).parent;R=Path('E:/Samplinglib')
p=O/'close_review90.py';b=p.read_bytes();t=b.decode('utf8')
q=O.parent/'audit.before-exposition90.json';qb=q.read_bytes()
assert hashlib.sha256(qb).hexdigest()=='31aebee15fa5d3e0ae3fb0f91c1a4a191e686b36b9606bd552552de480a841e9'
with (O/'closure-stage-pointer90.negative.json').open('x',encoding='utf8',newline='\n') as f:
 json.dump({'tool_chunk':'bdf2d5','exit_code':1,'status':'REVIEWER_WRONG_STAGE_EQUALITY_ASSUMPTION_BEFORE_FINAL_DECISION','original_script':{'path':p.relative_to(R).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)},'assumed_raw':'c623aa7dde64d17fa772cec53e70d4aae769b46016100ffa7090df79b17a1427','actual_root_stage_snapshot_raw':hashlib.sha256(qb).hexdigest(),'actual_root_stage_snapshot_bytes':len(qb),'repair':'Use own previously frozen c623 snapshot for exact c623 references; retain root before-exposition31aeb as a separate hash-only stage. Original b130 root snapshot matches. Do not infer semantics from filenames.','no_mathematical_source_or_Lean_failure':True,'all_original_files_and_partial_native_validation_retained':True},f,indent=2);f.write('\n')
old="assert pin(pre_overlay)['raw_sha256']=='c623aa7dde64d17fa772cec53e70d4aae769b46016100ffa7090df79b17a1427'"
new="assert pin(pre_overlay)['raw_sha256']=='31aebee15fa5d3e0ae3fb0f91c1a4a191e686b36b9606bd552552de480a841e9'"
assert t.count(old)==1;t=t.replace(old,new)
old='Before-exposition c623 matches own observed snapshot.'
new='Own observed c623 snapshot is authoritative for c623 freeze references. Root before-exposition snapshot31aeb is a separate hash-only metadata stage, not asserted equal to c623.'
assert t.count(old)==1;t=t.replace(old,new)
old="def put(n,v):\n with (O/n).open('x',encoding='utf8',newline='\\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\\n')"
new="def put(n,v):\n if (O/n).exists():\n  assert load(O/n)==v, n\n  return\n with (O/n).open('x',encoding='utf8',newline='\\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\\n')"
assert t.count(old)==1;t=t.replace(old,new)
out=O/'close_review90.attempt2.executed.py'
with out.open('xb') as f:f.write(t.encode('utf8'))
exec(compile(t,str(out),'exec'))
