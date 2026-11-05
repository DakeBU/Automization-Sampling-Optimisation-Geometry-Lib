"""Trusted, read-only supervisor inside a nonroot Docker container.

The submitted source is compiled/exported only below real Landrun. Comparator
compares serialized challenge/solution meanings, audits axioms and replays the
proof in a fresh kernel. Neither untrusted stdout nor #print output is a verdict.
"""
import ctypes
import base64
import json
import os
from pathlib import Path
import platform
import resource
import signal
import shutil
import subprocess
import sys


def readonly_precheck_command(*, probe=False):
    """Stream the actual compiler before Lake's buffered build, never accept it.

    No writable project/cache path: this pass runs BEFORE comparator exports the
    challenge, so letting it mutate .lake could corrupt that trusted baseline.
    Only the child's own /dev I/O is writable, as in upstream Landrun. The fixed
    source has no -o/-c output and no shell or agent-controlled argv.
    """
    # Match the unchanged official comparator's ABI negotiation. The separate
    # preflight still REJECTS ABI<6; this is not a no-sandbox/old-kernel fallback.
    argv=['lake','env','/opt/judge/landrun-env','--best-effort',
            '--ro','/','--rw','/dev','-ldd','-add-exec',
            '--env','PATH','--env','HOME','--env','LEAN_PATH',
            '--env','LEAN_ABORT_ON_PANIC','--rox','/opt/lean',
            '--','/opt/lean/bin/lean']
    return argv+(['--version'] if probe else ['Solution.lean'])


def preflight(p):
    status=Path('/proc/self/status').read_text()
    fields=dict(line.split(':',1) for line in status.splitlines() if ':' in line)
    if platform.machine()!='x86_64': raise RuntimeError('Linux x86_64 is the initial supported runtime')
    libc=ctypes.CDLL(None,use_errno=True)
    abi=libc.syscall(444,0,0,1)  # landlock_create_ruleset(NULL, 0, VERSION)
    observations={'uid':os.getuid(),'gid':os.getgid(),'landlock_abi':abi,
        'no_new_privs':fields['NoNewPrivs'].strip(), 'cap_eff':fields['CapEff'].strip(),
        'interfaces':sorted(x.name for x in Path('/sys/class/net').iterdir()),
        'memory_max':Path('/sys/fs/cgroup/memory.max').read_text().strip(),
        'pids_max':Path('/sys/fs/cgroup/pids.max').read_text().strip(),
        'cpu_max':Path('/sys/fs/cgroup/cpu.max').read_text().strip(),
        'proxy_variables_blank':all(not os.getenv(name) for name in (
            'HTTP_PROXY','HTTPS_PROXY','FTP_PROXY','ALL_PROXY','NO_PROXY',
            'http_proxy','https_proxy','ftp_proxy','all_proxy','no_proxy')),
        'root_read_only':bool(os.statvfs('/').f_flag & os.ST_RDONLY)}
    limits=p['limits']
    quota,period=observations['cpu_max'].split()
    if not (observations['uid']==observations['gid']==1000 and abi>=p['minimum_landlock_abi']
            and observations['no_new_privs']=='1' and int(observations['cap_eff'],16)==0
            and observations['interfaces']==['lo'] and observations['root_read_only']
            and observations['proxy_variables_blank']
            and int(observations['memory_max'])==limits['memory_mb']*1024*1024
            and int(observations['pids_max'])==limits['pids']
            and quota!='max' and int(quota)==limits['cpus']*int(period)):
        raise RuntimeError('Runtime isolation preflight did not match the policy: '+json.dumps(observations))
    return observations


def main():
    policy=json.loads(Path('/opt/judge/policy.json').read_text())
    observed=preflight(policy)
    # Only the caller's one bounded regular-file submission is mounted; no agent
    # directory, oracle, Docker socket, credentials, or writable host checkout.
    sys.path.insert(0,'/opt/judge')
    from bench_bounded_io import read_bounded
    raw=read_bounded('/input/Solution.lean',policy['limits']['submission_bytes'])
    raw.decode('utf-8',errors='strict')
    work=Path('/work/project');shutil.copytree('/task/project',work)
    (work/'.lake/build').mkdir(parents=True)
    shutil.copytree('/task/owned-build',work/'.lake/build',dirs_exist_ok=True)
    (work/'.lake/packages').symlink_to('/deps/packages',target_is_directory=True)
    shutil.copyfile('/task/Challenge.lean',work/'Challenge.lean')
    (work/'Solution.lean').write_bytes(raw)
    environment=dict(os.environ,COMPARATOR_LANDRUN='/opt/judge/landrun-env',
        COMPARATOR_LEAN4EXPORT='/opt/judge/lean4export',LEAN_ABORT_ON_PANIC='1')
    # Bound captured diagnostic storage and the final JSON. Internal Lean/Lake
    # and serialized-proof buffers instead share the container RAM/wall bounds;
    # a source can behave differently in the subsequent buffered build/export.
    # Real child
    # output is data, escaped below, not a report that can override an exit code.
    cap=policy['limits']['diagnostic_bytes']
    def child_limits():
        # This cap applies to compiler artifacts too, not just diagnostics.
        resource.setrlimit(resource.RLIMIT_FSIZE,(64*1024*1024,64*1024*1024))
        resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    diagnostic_total=0
    def capture(argv,phase):
        nonlocal diagnostic_total
        proc=subprocess.Popen(argv,cwd=work,env=environment,stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,preexec_fn=child_limits,start_new_session=True)
        diagnostic=bytearray();limited=False
        try:
            while chunk:=proc.stdout.read1(min(4096,cap-diagnostic_total+1)):
                kept=chunk[:max(0,cap-diagnostic_total)]
                diagnostic.extend(kept);diagnostic_total+=len(kept)
                # Only the readonly supervisor emits protocol frames. Child text
                # stays base64 DATA and survives a later timeout/forced kill.
                print(json.dumps({'kind':'runtime-diagnostic','phase':phase,
                    'chunk_b64':base64.b64encode(kept).decode('ascii')}),flush=True)
                if len(chunk)>len(kept):
                    limited=True;os.killpg(proc.pid,signal.SIGKILL);break
            proc.wait()
        finally:proc.stdout.close()
        return proc.returncode,diagnostic.decode('utf-8',errors='replace'),limited
    # This phase uses ONLY the trusted challenge/imports; a failure here is an
    # infrastructure failure, not a purported refutation of the submitted proof.
    print(json.dumps({'kind':'runtime-phase','phase':'challenge-preflight'}),flush=True)
    code,diagnostic,limited=capture(['lake','build','Challenge'],'challenge-preflight')
    if code!=0 or limited:
        print(json.dumps({'kind':'infrastructure-error','accepted':False,'phase':'challenge-preflight',
            'error':'Trusted challenge build failed','exit_code':code,'diagnostic':diagnostic,
            'diagnostic_limit':limited,'observations':observed}))
        return 20
    # Validate the SAME launcher/sandbox/executable with no submitted source
    # before labeling a later compiler rejection as a source failure. This also
    # keeps missing/unlaunchable Landrun in the infrastructure phase. It is a
    # trusted readiness probe, not evidence that any submitted proof started.
    code,diagnostic,limited=capture(readonly_precheck_command(probe=True),'challenge-preflight')
    if code!=0 or limited or 'version 4.33.0' not in diagnostic:
        print(json.dumps({'kind':'infrastructure-error','accepted':False,'phase':'challenge-preflight',
            'error':'Trusted readonly sandbox/Lean readiness probe failed','exit_code':code,
            'diagnostic_limit':limited,'diagnostic':diagnostic,'observations':observed}))
        return 20
    print(json.dumps({'kind':'runtime-phase','phase':'verifying-solution'}),flush=True)
    # Lake4.33's rawProc -> IO.Process.output buffers a module's stdout until
    # exit, hiding both a sleep marker and a growing output flood. lake env,
    # by contrast, spawns with inherited stdout. This extra REAL sandboxed
    # compiler pass makes those limits observable without changing comparator,
    # its challenge/types/axioms/kernel checks, or any resource budget. It may
    # reject; it NEVER accepts. Successful compilation still runs comparator.
    code,diagnostic,limited=capture(readonly_precheck_command(),'verifying-solution')
    if code!=0 or limited:
        print(json.dumps({'schema_version':1,'kind':'fixed-target-lean-precheck',
            'accepted':False,'compiler_exit':code,'comparator_not_run':True,'sandbox_probe_passed':True,
            'diagnostic_limit':limited,'diagnostic':diagnostic,
            'observations':observed,'external_kernel':False,'model_measurement':False}))
        return 30 if limited else 10
    code,diagnostic,limited=capture(['lake','env','/opt/judge/comparator','/task/config.json'],'verifying-solution')
    report={'schema_version':1,'kind':'fixed-target-comparator','observations':observed,
        'comparator_exit':code,'source_precheck_exit':0,'sandbox_probe_passed':True,
        'accepted':code==0 and not limited,
        'diagnostic_limit':limited,
        'diagnostic':diagnostic,
        'external_kernel':False,'model_measurement':False}
    print(json.dumps(report,ensure_ascii=False))
    return 30 if limited else 0 if code==0 else 10


if __name__=='__main__':
    try: sys.exit(main())
    except Exception as error:
        print(json.dumps({'kind':'infrastructure-error','error':str(error),'accepted':False}))
        sys.exit(20)
