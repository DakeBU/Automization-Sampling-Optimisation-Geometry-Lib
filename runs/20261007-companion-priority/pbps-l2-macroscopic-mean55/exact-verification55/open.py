from common import *
assert not (O/'lease.json').exists()
dump('lease.json',dict(status='OPEN',actor=ACTOR,stage='independent exact scientific commit55',opened_utc=utc(),actual_python_PID=os.getpid(),read='OPEN',write='OPEN',Python='OPEN',compiler='NOT_STARTED',checked_commit=SCI,scope='Only exact-verification55/ and parent verified.json plus authorized independent VERIFIED/cell transition; no proof/shared edits or commit/push.'))
assert git('rev-parse','HEAD')==SCI and git('rev-parse','HEAD^')==BASE
for p,n in [(CELL,'before.cell.raw.snapshot.json'),(AUDIT,'before.audit.raw.snapshot.json'),('runs/substantive_advances.jsonl','before.ledger.raw.snapshot.jsonl')]: (O/n).write_bytes(path(p).read_bytes())
print('OPEN exact55 '+SCI)
