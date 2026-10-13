"""Finish the existing owned staging set without rewriting immutable CRLF evidence."""
from pathlib import Path
import datetime,hashlib,json,subprocess
R=Path('E:/Samplinglib');r=Path(__file__).parent
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
def git(args):return subprocess.check_output(['git',*args],cwd=R)
staging=r/'science-staging91.json';x=load(staging)
expected={v['path'] for v in x['files']}|{staging.relative_to(R).as_posix()}
assert set(git(['diff','--cached','--name-only']).decode().splitlines())==expected
for v in x['files']:
    assert sha(git(['show',':'+v['path']]))==v['raw_sha256'],v['path']
negative=subprocess.run(['git','diff','--cached','--check'],cwd=R,capture_output=True)
(r/'staged-native-CRLF91.failure.log').write_bytes(negative.stdout+negative.stderr)
assert negative.returncode==2
checked=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],cwd=R,capture_output=True)
assert checked.returncode==0,(checked.stdout+checked.stderr).decode(errors='replace')
record=dict(classification='NATIVE_EVIDENCE_LINE_ENDINGS',reason='Native reviewer/receipt files contain immutable CRLF. Plain worktree diff gate passed after only new ledger-tail normalization. Established science lane recognizes CRLF as line endings for staged native evidence; raw bytes and their reviews remain unchanged.',plain_staged_exit=negative.returncode,staged_cr_at_eol_exit=checked.returncode)
(r/'staged-native-CRLF91.diagnosis.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
subprocess.run(['git','commit','-q','-m','Prove actual PBPS next absolute event-time law'],cwd=R,check=True,capture_output=True)
head=git(['rev-parse','HEAD']).decode().strip()
saved=load(r.parent/'pbps-ordered-history-iteration-preread91/pre-fetch91.workspace-RAW.json')['tracked_modified']
for p,h in saved.items():assert sha(Path(p).read_bytes())==h,p
receipt=r/'science-commit91.receipt.json';assert not receipt.exists()
receipt.write_text(json.dumps(dict(commit=head,files=len(expected),archives=x['archive_count'],utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_review='accepted',exact_commit_verification='pending',full_integration='pending',all21_collaborator_files_preserved=True,staging_diagnosis=record),indent=2)+'\n',encoding='utf-8',newline='\n')
print('SCIENCE_COMMIT',head,'files',len(expected))
