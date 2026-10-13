import os,sys,subprocess
from check import *

assert git('rev-parse','HEAD')==COMMIT and not git('diff','--name-only','HEAD')
c=load(O/'checks.json'); assert c['status']=='PASS'
bindings=[]
for p in c['integration_ownedpaths']:
    blob=subprocess.check_output(['git','show',COMMIT+':'+p],cwd=R)
    current=path(p).read_bytes()
    assert blob.replace(b'\r\n',b'\n')==current.replace(b'\r\n',b'\n'),p
    bindings.append(dict(current=pin(p),integration_Git_raw_sha256=sha(blob),integration_Git_LF_sha256=sha(blob.replace(b'\r\n',b'\n')),current_LF_equal=True))
dump('integration-Git-bindings.json',dict(status='PASS',commit=COMMIT,count=len(bindings),bindings=bindings))
metadata_paths=['docs/companion-papers-handoff.md','research-wiki/cited-results/SLT_reuse_audit.md','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl','website/content/samplewiki_companion_frontiers.json']
delta=subprocess.check_output(['git','diff',SCI,COMMIT,'--',*metadata_paths],cwd=R)
(O/'integration-metadata.diff.raw.snapshot.txt').write_bytes(delta)
registry_rows=[json.loads(x) for x in path(metadata_paths[2]).read_text().splitlines() if x.strip()]
entry=next(x for x in registry_rows if x['local_decl']==TARGET)
assert entry['verified_commit']==SCI and entry['status']=='formalized-local' and entry['local_file']=='AutoSamplingTheory/ExampleCases/ProximalBPS/LiteralReflectedMean.lean'
assert 'not a new SLT admission' in path(metadata_paths[1]).read_text()
execution=load(metadata_paths[3])['execution']
assert execution['current_checkpoint']=='docs/companion-papers-handoff.md#literal-pbps-source-reflected-law-and-mean-c1-2026-10-08'
dump('metadata-review.json',dict(status='PASS',inputs=[pin(p) for p in metadata_paths],registry_entry=entry,execution=execution,findings=['Handoff records actual every-y source S law and whole compact C1 mean, explicit lower-curvature/all-positive-step/Hilbert/rank0 extension, original source consumer bounds, disclosed decoder identity exposure, and open Tf/rough/Gamma/main/cost/composition/Goal boundaries.','Registry is source-specific integration of three existing ASTIS parents; non-SLT audit does not falsely admit a new SLT result.','Execution changes only the current checkpoint; prior four-paper priority and historical frontiers remain.','Handoff wording that aggregate/seals follow is a historical checkpoint; actual integration logs independently establish the later scoped gates. This is retained status-neutral presentation debt.']))
print(json.dumps(dict(status='PASS',current_Git_bindings=len(bindings),metadata_review='PASS',actual_python_pid=os.getpid(),compiler_invocations=0)))
