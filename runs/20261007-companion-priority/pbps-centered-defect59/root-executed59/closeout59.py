from pathlib import Path
import json,hashlib,subprocess
root=Path.cwd();r=root/'runs/20261007-companion-priority/pbps-centered-defect59';d=r/'integration59/accepted-closeout';d.mkdir(exist_ok=False)
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return dict(path=p.relative_to(root).as_posix(),bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')))
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()=='47a28adfa36bfa67ce201f9b3ff9823c85fc3b45'
assert load(r/'root.repository-exposition59.adoption.json')['status']=='INDEPENDENT_SCOPED_REPOSITORY_EXPOSITION59_ACCEPTED'
remote=[]
for n in [37791236055,37791236039,37791236018]:
 p=r/f'integration59/remote-terminal-{n}/stdout.log';x=load(p)
 assert x['headSha']=='47a28adfa36bfa67ce201f9b3ff9823c85fc3b45' and x['status']=='completed' and x['conclusion']=='success'
 assert all(j['status']=='completed' and j['conclusion'] in ['success','skipped'] for j in x['jobs'])
 remote.append(dict(run=n,evidence=pin(p),name=x['jobs'][0]['name']))
p=root/'docs/companion-papers-handoff.md';before=p.read_bytes();snap=d/'handoff.before-closeout.exactraw.snapshot.md';snap.write_bytes(before)
addition='''## Accepted scoped centered-defect integration59 (2026-10-08)

Science2d6cd016 and serialized integration47a28adf both reached terminal SUCCESS
in GitHub Lean, site and contributor workflows. The exact47a integration has an
independent scoped repository/exposition acceptance in
`runs/20261007-companion-priority/pbps-centered-defect59/repository-exposition-seal59/`;
root readback is `root.repository-exposition59.adoption.json` beside that folder.
The post-administration stale graph was archived as a typed negative. The official
successor changes only its input-digest header, with identical nodes/edges and
both affected graph checks plus final site validation passing. No mathematics,
source statement, lesson or semantic binding changed. Draft deployment remains
skipped; main/live/full Chapter1.3 reader/PURIFIED are not granted.

Next60 is only an unproved real-L2 positive-operator complex-lift candidate with
actual PBPS D=I-T*T as its internally produced consumer. Both full signatures
elaborate, but preproof sealing/source topology and actual proofs must precede
admission. No caller CFC/root/operator certificate or finite-dimensional L2
assumption is allowed. Real Gamma descent/uniqueness, centered order/inverse/polar
and the remaining paper/main/error/querycost/composition boundaries remain open.
Push each meaningful reviewed science milestone and accepted integration.

'''
title=b'# Companion-paper formalization handoff\n\n';assert before.startswith(title)
p.write_bytes(title+addition.encode()+before[len(title):])
body=Path('.astis/pbps-real-complex-lift60/pr-body59.md');text=body.read_text(encoding='utf-8')
old='The exact integration repository and scoped exposition seal is being finalized after an additive official graph refresh: final administrative metadata had changed its input digest, and the original stale-graph negative is preserved.'
new='The independent exact47a repository and scoped exposition seal is accepted. Final administrative metadata had changed the graph input digest; its typed original negative is archived and the additive official graph successor was independently checked.'
assert old in text;body.write_text(text.replace(old,new),encoding='utf-8',newline='\n')
export=r/'root-executed59'
for name in ['adopt-repository59.py','closeout59.py','cache-generated-cards59.py']:
 src=Path('.astis/pbps-centered-defect59')/name;dest=export/name;assert not dest.exists();dest.write_bytes(src.read_bytes())
note=dict(status='ACCEPTED_SCOPED59_CLOSEOUT_NO_NEW_MATHEMATICAL_TRANSITION',science_commit='2d6cd0167adc4fae1d8d166068a2eda51cd3c3ad',integration_commit='47a28adfa36bfa67ce201f9b3ff9823c85fc3b45',native_seal=pin(r/'repository-exposition-seal59/receipt.json'),root_readback=pin(r/'root.repository-exposition59.adoption.json'),terminal_ci=remote,administrative_exact_history=dict(original=dict(path=p.relative_to(root).as_posix(),bytes=len(before),raw_sha256=sha(before),lf_sha256=sha(before.replace(b'\r\n',b'\n'))),exact_raw_snapshot=pin(snap),successor=pin(p)),root_schema_diagnosis='Initial root readback confused10 available mappings with6 actually used; exact native files retained and v2 checks both counts explicitly. No semantic/native review changed.',scope='Scoped repository/exposition only. Main/live/PURIFIED/full papers/Goal remain open.')
(d/'closeout.json').write_text(json.dumps(note,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Recorded accepted scoped seal and actual47a three terminal CI runs; preserved exact prior handoff and native reviews; authored current handoff prefix.')
