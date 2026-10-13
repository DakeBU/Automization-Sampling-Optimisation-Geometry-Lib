from pathlib import Path
import hashlib,json,os
root=Path.cwd();r=root/'runs/20261007-companion-priority/pbps-centered-root64';out=r/'frontier-process-repair64';out.mkdir(exist_ok=False)
load=lambda p:json.loads(p.read_bytes())
def pin(p):
 b=p.read_bytes();return dict(path=p.resolve().as_posix(),bytes=len(b),raw_sha256=hashlib.sha256(b).hexdigest(),lf_sha256=hashlib.sha256(b.replace(b'\r\n',b'\n')).hexdigest())
rows=[]
for cid in ['ASTIS-SW-PBPS-centered-root-order-inverse','ASTIS-SHARED-l2-real-positive-square-order']:
 p=root/'research-wiki/frontier-cells'/f'{cid}.json';old=load(p);sp=out/f'{cid}.before.exactraw.snapshot.json';sp.write_bytes(p.read_bytes());before=pin(p)
 if cid.startswith('ASTIS-SW'):
  field='/reuse_plan/reused_declarations';decl='AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareOrder.positive_square_order';assert decl not in old['reuse_plan']['reused_declarations'];old['reuse_plan']['reused_declarations'].append(decl)
 else:
  field='/graph_contribution/lean_view';assert old['graph_contribution']['lean_view']=='reusable-interface';old['graph_contribution']['lean_view']='new-node'
 p.write_text(json.dumps(old,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');rows.append(dict(original=before,explicit_exact_raw_snapshot=pin(sp),current=pin(p),only_changed_field=field))
(out/'repair.json').write_text(json.dumps(dict(status='TWO_CONTRIBUTOR_PROCESS_FIELDS_CORRECTED',actual_preparer_pid=os.getpid(),trigger=(r/'contributor-science64/receipt.json').relative_to(root).as_posix(),finite_historical_maps=rows,reason='The actual lesson already named the real compiled generic proof parent, but the cell reuse list omitted it. reusable-interface is an SAU result kind; graph lean_view admits new-node/reuse-only/integration-node.',Lean_statements_proofs_source_publications_audits_unchanged=True,independent_exact_commit_review_pending=True,VERIFIED_transition=False),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Corrected two contributor process fields only; proof/source/publication bindings unchanged. Independent exact-commit audit remains pending.')
