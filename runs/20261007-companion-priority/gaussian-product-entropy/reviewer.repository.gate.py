exec(open('runs/20261007-companion-priority/gaussian-product-entropy/reviewer.exact.gate.py',encoding='utf-8').read().split('assert subprocess.check_output')[0])
C='7e02d986a20af81d3c9ea027b3dcded6a8c25ffa'
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C
put(R/'reviewer.repository.lease.json',dict(status='OPEN',verifier_id=V,checked_commit=C,read='OPEN bounded shared delta and39 immutable evidence',write='OPEN owned repository receipts only',compiler='EXCLUSIVE_FOREGROUND',Python='OPEN',canonical_mutations=False,future40_untracked_source_scope_excluded=True))
env=dict(os.environ,PYTHONUTF8='1',LEAN_NUM_THREADS='2',ELAN_TOOLCHAIN='leanprover/lean4:v4.33.0')
commands=[('aggregate',[PY,'tools/astis.py','check']),('publication',[PY,'tools/astis_publication.py','check','--base','origin/main']),('semantic',[PY,'tools/astis_semantic_roundtrip.py','check']),('frontier',[PY,'tools/astis_frontier_cells.py','check']),('process-memory',[PY,'tools/astis_process_memory.py','check']),('contributor',[PY,'tools/astis_contributor_contract.py','check','--base','origin/main'])]
rows=[]
for label,cmd in commands:
 log=R/f'reviewer.repository.{label}.log';assert not log.exists()
 with log.open('wb') as f:code=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
 st=put(R/f'reviewer.repository.{label}.status.json',dict(checked_commit=C,command=cmd,exit_code=code,completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),log=d(log)))
 rows.append(dict(name=label,command=cmd,returncode=code,**d(log),status=st));print(label,code,flush=True)
 if code:break
put(R/'reviewer.repository.gates.json',dict(checked_commit=C,verifier_id=V,results=rows,compiler='CLOSED',foreground_serialized=True,all_pass=len(rows)==len(commands) and all(x['returncode']==0 for x in rows)))
