"""Independent reader76 preparation utilities; execution waits for root's final packet.

The final finite checks will be bound to that exact packet after explicit dispatch.
No prior review75 verdict, count, run receipt or acceptance is reused here.
"""
from pathlib import Path
from html.parser import HTMLParser
import datetime, hashlib, json, os, subprocess, sys

ROOT=Path('E:/Samplinglib')
R=ROOT/'runs/20261007-companion-priority/pbps-actual-finite-jump-recursion76'
O=R/'independent-repository-reader76'
CACHE=ROOT/'.astis/repository-reader76'
DIS=R/'final-reader-repository-packet76.json'
ACTOR='/root/fresh_source76'
SCI='e1f1d85d34426954829a97a46b563ea8e1dab8f1'
DECL='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion'
MOD='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean'
SOURCE='1f1ebc187676e0481247bc2f58ec0bf94b2fc6f02a563b87009a0fe7bfb4910c'
SOURCE_REVIEW=ROOT/'runs/20261007-companion-priority/pbps-recursive-preproof76/fresh-compiled-source76'
SOURCE_LEASE_SHA='0ca0645db780b696424ca80753fcf5a843369a5037a2bb26049a553dbeeb7d79'
PY=Path('C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe')
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1',PYTHONPYCACHEPREFIX=str(CACHE))
sys.dont_write_bytecode=True

def sha(raw): return hashlib.sha256(raw).hexdigest()
def can(value): return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def resolve(path):
    path=Path(path)
    return path if path.is_absolute() else ROOT/path
def load(path): return json.loads(resolve(path).read_bytes())
def pin(path):
    path=resolve(path); raw=path.read_bytes()
    return dict(path=path.as_posix(),RAW_bytes=len(raw),RAW_sha256=sha(raw),LF_sha256=sha(raw.replace(b'\r\n',b'\n')))
def check(record):
    path=resolve(record['path']); raw=path.read_bytes()
    count=record.get('RAW_bytes',record.get('raw_bytes',record.get('bytes')))
    digest=record.get('RAW_sha256',record.get('raw_sha256'))
    assert count is not None and digest is not None,path
    assert len(raw)==count and sha(raw)==digest,path
    lf=record.get('LF_sha256',record.get('lf_sha256'))
    if lf is not None: assert sha(raw.replace(b'\r\n',b'\n'))==lf,path
    return raw
def save(name,value):
    assert not (O/'lease.final.json').exists(),'Closed directory is immutable.'
    path=O/name; path.parent.mkdir(parents=True,exist_ok=True)
    assert not path.exists(),path
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8',newline='\n')
def command(label,args):
    assert not (O/'lease.final.json').exists()
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    argv=[str(value) for value in args]
    process=subprocess.Popen(argv,cwd=ROOT,env=ENV,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    print(json.dumps(dict(START=label,actual_foreground_PID=process.pid,driver_PID=os.getpid())),flush=True)
    stdout,stderr=process.communicate(); exit_code=process.wait()
    directory=O/'terminals'; directory.mkdir(exist_ok=True)
    out=directory/(label+'.stdout.RAW'); err=directory/(label+'.stderr.RAW')
    assert not out.exists() and not err.exists()
    out.write_bytes(stdout); err.write_bytes(stderr)
    receipt=dict(label=label,actual_foreground_PID=process.pid,actual_driver_PID=os.getpid(),command=argv,Popen_wait_used=True,terminal_closed=True,terminal_EXIT=exit_code,started_UTC=started,finished_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),stdout=pin(out),stderr=pin(err))
    save('terminals/'+label+'.receipt.json',receipt)
    print(json.dumps(dict(END=label,actual_foreground_PID=process.pid,terminal_EXIT=exit_code)),flush=True)
    # Failures stay native; an explicit later diagnosis must precede a changed route.
    assert exit_code==0,label
    return stdout,receipt

class Node:
    def __init__(self,tag='',attrs=None): self.tag=tag; self.attrs=dict(attrs or []); self.children=[]
    def all(self,tag=None):
        result=[self] if tag is None or self.tag==tag else []
        for child in self.children:
            if isinstance(child,Node): result+=child.all(tag)
        return result
    def text(self): return ''.join(child.text() if isinstance(child,Node) else child for child in self.children)
class Tree(HTMLParser):
    def __init__(self): super().__init__(convert_charrefs=True); self.root=Node(); self.stack=[self.root]
    def handle_starttag(self,tag,attrs):
        node=Node(tag,attrs); self.stack[-1].children.append(node)
        if tag not in ['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr']: self.stack.append(node)
    def handle_endtag(self,tag):
        for index in range(len(self.stack)-1,0,-1):
            if self.stack[index].tag==tag: self.stack=self.stack[:index]; break
    def handle_data(self,text): self.stack[-1].children.append(text)

def verify_finite_closed(lease_path,records,extra_paths=None,directory=None):
    """Integrity reuse only; this never recertifies mathematics or source meaning."""
    lease_path=resolve(lease_path); directory=resolve(directory) if directory else lease_path.parent
    extras={resolve(path).resolve() for path in (extra_paths or [lease_path])}
    expected={resolve(record['path']).resolve() for record in records}|extras
    actual={path.resolve() for path in directory.rglob('*') if path.is_file()}
    assert actual==expected,(directory,len(actual),len(expected))
    for record in records:
        check(record)
        assert resolve(record['path']).stat().st_mtime_ns<=lease_path.stat().st_mtime_ns
    return dict(lease=pin(lease_path),owned_files=len(actual),all_native_owned_RAW_LF_unchanged=True,new_mathematics_certification=False,new_source_certification=False)

def final_packet_inputs(expected_packet_RAW_sha256):
    """Call only after the parent explicitly authorizes the frozen final dispatch."""
    raw=DIS.read_bytes()
    assert sha(raw)==expected_packet_RAW_sha256
    packet=json.loads(raw)
    assert packet['checked_science_commit']==SCI
    assert isinstance(packet['inputs'],list) and packet['inputs']
    paths=[record['path'] for record in packet['inputs']]
    assert len(paths)==len(set(paths))
    for record in packet['inputs']: check(record)
    return packet

def build_run(decision,inputs,checks,views,named_review_path,complete_path):
    """Same native run recipe as reader75, with this actor and actual receipts only."""
    run=dict(schema='independent-scoped-repository-reader76/v1',actor=ACTOR,checked_science_commit=SCI,decision=pin(decision),inputs_manifest=pin(inputs),complete_named_RAW_payload=pin(complete_path),named_review=pin(named_review_path),checks=pin(checks),owned_script=pin(O/'review76.py'),independent_PNG_observations=pin(views),writer_PID=os.getpid(),foreground_terminal_basis='Actual Popen.wait receipts and complete RAW stdout/stderr are retained. No PID or exit is inferred from expected counts.',writer_EXIT_contract='Final lease is last owned write. Its actual writer exit and external read-only validation are captured outside the owned directory.',whole_logical_recipe='SHA256 canonical sorted compact UTF8 JSON; remove ONLY top-level run_sha256; LF pins replace CRLF byte pairs only.',new_independent_mathematics_certification=False,new_VERIFIED_transition=False)
    run['run_sha256']=sha(can(run)); return run
def seal_native_run(run,completed_receipts):
    """Only the authorized final execution calls this after all checks and PNG views."""
    assert not (O/'lease.final.json').exists()
    assert sha(can({key:value for key,value in run.items() if key!='run_sha256'}))==run['run_sha256']
    save('run.json',run)
    rows=[pin(path) for path in sorted(O.rglob('*'),key=lambda path:path.as_posix()) if path.is_file()]
    assert all(not row['path'].endswith('lease.final.json') for row in rows)
    lease=dict(schema='independent-scoped-reader76-CLOSED-LAST/v1',status='CLOSED_LAST',actor=ACTOR,checked_science_commit=SCI,writer_PID=os.getpid(),all_prior_child_sessions_terminal_closed=True,completed_check_receipts=completed_receipts,postclose_owned_writes_forbidden=True,final_owned_write=True,files=rows,file_count_including_lease=len(rows)+1,closure_logical_sha256=sha(can(rows)),run_sha256=run['run_sha256'],actual_writer_EXIT_observation='No self-asserted exit; external foreground Popen.wait captures writer termination and actual EXIT.',new_VERIFIED_transition=False)
    save('lease.final.json',lease)
    # No own-directory writes, receipts, logs or metadata are permitted from here.
    print(json.dumps(dict(status='CLOSED_LAST',actual_writer_PID=os.getpid(),run_sha256=run['run_sha256'],lease_RAW_sha256=sha((O/'lease.final.json').read_bytes()),complete_named_RAW_payload=run['complete_named_RAW_payload'],owned_count=lease['file_count_including_lease'],closure_logical_sha256=lease['closure_logical_sha256']),ensure_ascii=False))

if __name__=='__main__':
    raise SystemExit('PREPARATION_ONLY: root final-packet authorization and packet-specific finite checker are still required. No current reader checks have run.')
