from pathlib import Path
import hashlib, json, os, subprocess

root=Path.cwd(); out=Path('runs/20261007-companion-priority/pbps-sharp-energy-preproof68/root-library-retrieval68')
out.mkdir(exist_ok=False); sha=lambda b:hashlib.sha256(b).hexdigest(); rows=[]
paths=['.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Basic.lean',
       '.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Adjoint.lean',
       '.lake/packages/mathlib/Mathlib/Analysis/Normed/Operator/Basic.lean',
       'research-wiki/sampling-sde-library/cards/AutoSamplingTheory.TechnicalLemmas.Analysis.md',
       'research-wiki/technical-lemmas/README.md',
       'AutoSamplingTheory/TechnicalLemmas/Analysis/GradientDescentContraction.lean']
for i,name in enumerate(paths):
    b=Path(name).read_bytes(); p=out/f'{i:02}.exactraw.snapshot';p.write_bytes(b)
    rows.append(dict(path=name,raw_bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')),snapshot=p.as_posix()))
queries=[['rg','-n','corrector|square_identity|norm_add_sq_real|norm_sub_sq_real',
          'AutoSamplingTheory/TechnicalLemmas/Analysis','AutoSamplingTheory/TechnicalLemmas/Measure',
          'Tests/ProximalBPSActualRootCommutation.lean'],
         ['rg','-n','norm_add_sq_real|norm_sub_sq_real|real_inner_mul_inner_self_le|theorem isSymmetric|le_opNorm',*paths[:3]]]
receipts=[]
for i,cmd in enumerate(queries):
    child=subprocess.Popen(cmd,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout,stderr=child.communicate();assert child.returncode in [0,1]
    (out/f'query{i}.stdout.RAW.txt').write_bytes(stdout);(out/f'query{i}.stderr.RAW.txt').write_bytes(stderr)
    receipts.append(dict(command=cmd,actual_PID=child.pid,exit_code=child.returncode,terminal_closed=True,
                         stdout_RAW_sha256=sha(stdout),stderr_RAW_sha256=sha(stderr)))
manifest=json.loads(Path('lake-manifest.json').read_bytes())
mathlib=next(x for x in manifest['packages'] if x['name']=='mathlib')
assert mathlib['rev']=='db584cd6d46c92f209a44c0f1c829460d327499d'
record=dict(status='PREPROOF_RETRIEVAL_NO_PROOF_SEARCH',actual_root_PID=os.getpid(),snapshots=rows,queries=receipts,
    lean_toolchain_RAW_sha256=sha(Path('lean-toolchain').read_bytes()),mathlib_revision=mathlib['rev'],
    conclusion='No local sharp Hilbert corrector lemma found; existing actual67 coefficient proof is a real consumer prerequisite. Fixed Mathlib supplies selfadjoint symmetry, exact norm-square expansions and operator norm bounds.',
    source_statement_change=False,SLT_OpenAI_upstream_used=False,proof_credit=False)
(out/'manifest.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Recorded6 exact pinned API/card/README snapshots and2 real retrieval processes; no proof or source change.')
