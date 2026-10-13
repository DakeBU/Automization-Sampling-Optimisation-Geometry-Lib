import datetime,hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent;run=out.parent
def sha(b):return hashlib.sha256(b).hexdigest()
def put(n,d):(out/n).write_text(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
m=json.loads((out/'input-manifest.json').read_bytes())
assert json.loads((out/'source-expectations70.before-header.json').read_bytes())['candidate_header_or_proposal_seen'] is False
for n,source,role in [('candidate.header0-proposed-expanded.RAW.lean',run/'header0-proposed-expanded.lean','only-current70-proposed-header; no-body'),('candidate.proposal.RAW.json',run/'proposal.json','current70-authored-proposal-claims-to-check-not-verdict')]:
 b=source.read_bytes();lf=b.replace(b'\r\n',b'\n');(out/n).write_bytes(b);(out/(n+'.LF')).write_bytes(lf)
 m['inputs'].append(dict(name=n,original_path=str(source),role=role,RAW_bytes=len(b),RAW_sha256=sha(b),LF_bytes=len(lf),LF_sha256=sha(lf)))
m['count']=len(m['inputs']);m['candidate_seen']=True;m['first_candidate_seen_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();put('input-manifest.json',m)
put('source-before-header-order.json',dict(actual_pid=os.getpid(),source_expectations_RAW_sha256=sha((out/'source-expectations70.before-header.json').read_bytes()),mean_g_completion_RAW_sha256=sha((out/'mean-g-source-and-internal-completion70.json').read_bytes()),source_freeze_completed_before_candidate_snapshot=True,candidate_header_RAW_sha256=sha((out/'candidate.header0-proposed-expanded.RAW.lean').read_bytes()),candidate_proposal_RAW_sha256=sha((out/'candidate.proposal.RAW.json').read_bytes()),candidate_first_seen_utc=m['first_candidate_seen_utc']))
print(json.dumps(dict(actual_pid=os.getpid(),input_count=m['count'],candidate_header_RAW_sha256=sha((out/'candidate.header0-proposed-expanded.RAW.lean').read_bytes()),source_frozen_first=True),sort_keys=True))
