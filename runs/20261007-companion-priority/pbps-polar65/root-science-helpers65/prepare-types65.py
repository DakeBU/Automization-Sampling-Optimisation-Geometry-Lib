from pathlib import Path
import hashlib,json
r=Path('runs/20261007-companion-priority/pbps-polar-preproof65');p=r/'header.candidate.lean'
s=p.read_text(encoding='utf-8');a=s.index('theorem actual_centered_polar_isometry');b=s.rindex(':= by')
assert '__ASTIS_TYPE_ONLY_UNDEFINED_POLAR65__' in s[b:]
h=s[a:b].rstrip()+'\n';(r/'header0.lean').write_text(h,encoding='utf-8',newline='\n')
test=s.replace('namespace AutoSamplingTheory.ExampleCases.ProximalBPS.PolarIsometry','namespace Tests.ProximalBPSPolarIsometry').replace('end AutoSamplingTheory.ExampleCases.ProximalBPS.PolarIsometry','end Tests.ProximalBPSPolarIsometry').replace('theorem actual_centered_polar_isometry','theorem genuine_actual_polar_corrector_consumer')
old='(∀ f : HP0, ‖V0 f‖ = ‖f‖) := by'
new='''(∀ f : HP0, ‖V0 f‖ = ‖f‖) ∧
                        (∀ g : Hperp, B0.adjoint g = ΓP0 (V0.adjoint g)) ∧
                        (∀ g : Hperp, ‖V0.adjoint g‖ ≤ ‖g‖) ∧
                        (∀ g : Hperp, V0.adjoint (g-V0 (V0.adjoint g))=0) := by'''
assert test.count(old)==1;test=test.replace(old,new).replace('__ASTIS_TYPE_ONLY_UNDEFINED_POLAR65__','__ASTIS_TYPE_ONLY_UNDEFINED_CONSUMER65__')
(r/'test.candidate.lean').write_text(test,encoding='utf-8',newline='\n');a=test.index('theorem genuine_actual_polar_corrector_consumer');b=test.rindex(':= by');(r/'header1.lean').write_text(test[a:b].rstrip()+'\n',encoding='utf-8',newline='\n')
rows=[]
for n in ['header.candidate.lean','test.candidate.lean','header0.lean','header1.lean']:
 q=r/n;raw=q.read_bytes();rows.append(dict(path=q.as_posix(),bytes=len(raw),raw_sha256=hashlib.sha256(raw).hexdigest()))
(r/'type-candidates.json').write_text(json.dumps(dict(status='TYPE_ONLY_INTENTIONALLY_UNDEFINED_NO_PROOF_NO_SAU_NO_STATEMENT_SEAL',candidates=rows,primary_adoption=(r/'root.primary65.adoption.json').as_posix(),proof_search=False,consumer='Original inputs produce actual adjoint corrector action/contraction and explicit untouched orthogonal residual; no surjectivity.'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Prepared exact polar65 and genuine adjoint-corrector TYPE-only headers; no proof/SAU/Statement Seal.')
