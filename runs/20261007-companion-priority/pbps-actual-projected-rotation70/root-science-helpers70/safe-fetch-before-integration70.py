from pathlib import Path
import hashlib, json, os, subprocess
r = Path('runs/20261007-companion-priority/pbps-actual-projected-rotation70/safe-fetch-before-integration70')
r.mkdir(exist_ok=False)
sha = lambda b: hashlib.sha256(b).hexdigest()
def git(*args):
    return subprocess.check_output(['git', *args])
before_head = git('rev-parse', 'HEAD')
before_tracked = git('status', '--porcelain=v1', '--untracked-files=no')
before_main = git('rev-parse', 'origin/main')
(r / 'before.tracked.RAW.log').write_bytes(before_tracked)
cmd = ['git', '-c', 'http.sslBackend=openssl', '-c', 'credential.helper=',
       '-c', 'credential.helper=!gh auth git-credential', 'fetch', 'origin']
with (r / 'fetch.stdout.RAW.log').open('wb') as out, (r / 'fetch.stderr.RAW.log').open('wb') as err:
    child = subprocess.Popen(cmd, stdout=out, stderr=err)
    code = child.wait()
assert code == 0, code
after_head = git('rev-parse', 'HEAD')
after_tracked = git('status', '--porcelain=v1', '--untracked-files=no')
after_main = git('rev-parse', 'origin/main')
(r / 'after.tracked.RAW.log').write_bytes(after_tracked)
assert after_head == before_head and after_tracked == before_tracked
ancestor = subprocess.run(['git', 'merge-base', '--is-ancestor', 'origin/main', 'HEAD']).returncode
remote_contains_local = subprocess.run(['git', 'merge-base', '--is-ancestor', 'HEAD', 'origin/main']).returncode
receipt = dict(status='SAFE_FETCH_NO_CHECKOUT_NO_MERGE_NO_RESET', actual_pid=child.pid, exit_code=code,
    head=after_head.decode().strip(), origin_main_before=before_main.decode().strip(),
    origin_main_after=after_main.decode().strip(), tracked_status_unchanged=True,
    before_tracked_RAW_sha256=sha(before_tracked), after_tracked_RAW_sha256=sha(after_tracked),
    main_is_ancestor_of_head=ancestor == 0, head_is_ancestor_of_main=remote_contains_local == 0,
    working_tree_retained=True, root_pid=os.getpid())
(r / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8', newline='\n')
print(json.dumps(receipt))
