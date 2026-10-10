from pathlib import Path
import hashlib,json
pre=Path('runs/20261007-companion-priority/pbps-ambient-adjoint-preproof66');d=pre/'type-coercion-diagnosis-v1';d.mkdir(exist_ok=False)
rows=[]
for name in ['header0.lean','header1.lean','header.candidate.lean','test.candidate.lean']:
 p=pre/name;b=p.read_bytes();(d/name).write_bytes(b);s=b.decode()
 replacements=[('B.adjoint g=(B0.adjoint (R g) : HP)','B.adjoint g=HP0.subtypeL (B0.adjoint (R g))'),('(fP : HP)=condExpL2','HP0.subtypeL fP=condExpL2'),('(ΓP0 fV : HP)','HP0.subtypeL (ΓP0 fV)'),('ΓP (fV : HP)','ΓP (HP0.subtypeL fV)'),('((fP : HP) : Lp ℝ 2 J)','HP.subtypeL (HP0.subtypeL fP)')]
 for a,c in replacements:s=s.replace(a,c)
 p.write_text(s,encoding='utf-8',newline='\n');rows.append(dict(path=p.as_posix(),before_RAW_sha256=hashlib.sha256(b).hexdigest(),after_RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
(d/'diagnosis.json').write_text(json.dumps(dict(status='TYPE_ONLY_LEAN_ELABORATION_DIAGNOSIS',first_compiler_pids=[27172,30188],first_exit_codes=[1,1],observed='unknown free variable _fvar.8860 before intentional unimplemented BODY; no header acceptance or proof credit.',route='Replace ambiguous dependent subtype coercions by explicit subtypeL applications. Identical mathematics/public inputs; source review follows only after successful header elaboration.',headers=rows,source_mathematical_repair=False,Statement_Seal=False,SAU_claim=False),indent=2)+'\n',encoding='utf-8',newline='\n')
print('Retained type-only66 negatives and exact v1 headers; explicit dependent subtypeL syntax prepared for v2, no mathematical/proof credit.')
