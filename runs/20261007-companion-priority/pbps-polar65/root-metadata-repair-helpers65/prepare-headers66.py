from pathlib import Path
import json,hashlib
pre=Path('runs/20261007-companion-priority/pbps-ambient-adjoint-preproof66');assert (pre/'root.primary66.adoption.json').is_file()
base=Path('runs/20261007-companion-priority/pbps-polar-preproof65/header0.lean').read_text()
anchor='(∀ f : HP0, ‖V0 f‖ = ‖f‖)'
assert base.count(anchor)==1
start=base.index(anchor);common=base[:start]+anchor+''' ∧
                        ∃ R : Lp ℝ 2 J →L[ℝ] Hperp,
                          (∀ g : Lp ℝ 2 J, (R g : Lp ℝ 2 J)=g-P g) ∧
                          (∀ g : Lp ℝ 2 J,
                            B.adjoint g=(B0.adjoint (R g) : HP)) ∧
'''
main=common+'''                          (∀ f : Lp ℝ 2 J, (∫ z, f z ∂J)=0 →
                            ∃ fP : HP0,
                              (fP : HP)=condExpL2 ℝ ℝ (μ:=J) measurable_snd.comap_le f ∧
                              let fperp : Hperp := R f
                              let fV : HP0 := V0.adjoint fperp
                              B.adjoint (fperp : Lp ℝ 2 J)=(ΓP0 fV : HP) ∧
                              (ΓP0 fV : HP)=ΓP (fV : HP) ∧
                              ‖f‖^2=‖fP‖^2+‖fperp‖^2 ∧ ‖fV‖≤‖fperp‖)
'''
test=common+'''                          (∀ f : Lp ℝ 2 J, (∫ z, f z ∂J)=0 →
                            ∃ fP : HP0, ∃ fperp : Hperp, ∃ fV : HP0,
                              f=((fP : HP) : Lp ℝ 2 J)+(fperp : Lp ℝ 2 J) ∧
                              (fperp : Lp ℝ 2 J)=f-P f ∧
                              fV=V0.adjoint fperp ∧
                              B.adjoint f=ΓP (fV : HP) ∧
                              ‖fV‖^2≤‖f‖^2-‖fP‖^2)
'''
headers=[main.replace('actual_centered_polar_isometry','actual_ambient_adjoint_centered_decomposition',1),test.replace('actual_centered_polar_isometry','genuine_actual_global_corrector_consumer',1)]
rows=[]
for i,s in enumerate(headers):
 p=pre/f'header{i}.lean';assert not p.exists();p.write_text(s,encoding='utf-8',newline='\n')
 candidate=pre/('header.candidate.lean' if i==0 else 'test.candidate.lean');namespace='AutoSamplingTheory.ExampleCases.ProximalBPS.AmbientAdjointCorrector' if i==0 else 'Tests.ProximalBPSAmbientAdjointCorrector'
 prefix='import AutoSamplingTheory.ExampleCases.ProximalBPS.PolarIsometry\n\nopen MeasureTheory ProbabilityTheory InnerProductSpace\nopen scoped RealInnerProductSpace ContDiff NNReal Topology ENNReal\nnamespace '+namespace+'\nnoncomputable section\nset_option autoImplicit false\nset_option maxHeartbeats 2000000\n\n'
 candidate.write_text(prefix+s+':= by\n  exact ASTIS_UNIMPLEMENTED_BODY66\n\nend\nend '+namespace+'\n',encoding='utf-8',newline='\n')
 rows.append(dict(header=p.as_posix(),header_RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),candidate=candidate.as_posix(),proof_credit=False))
(pre/'type-candidates.json').write_text(json.dumps(dict(status='TYPE_ONLY_NO_SEAL_NO_PROOF_NO_CLAIM',headers=rows,public_original_inputs_unchanged=True,new_quantified_centering_is_output_scope=True,extra_public_premises=[],source_only_parent='independent-primary66',genuine_consumer='Full ambient first corrector at every actually globally centered input, common HP0 domain and norm budget needed before B20. Intrinsic block adjoint extended canonically; no extra operator premise.',optional_geometry='Orthogonal Pythagorean identity is internally derived, not a source premise.',remaining='B20 full corrector bound,root commutation/B21,halfturn,H1/operator estimates,dynamics/main/errors/expectedcost/composition separate.'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Prepared two TYPE-only66 headers:original inputs,SAME65 outputs,actual ambient adjoint and centered input/corrector norm budget. No proof or SAU claim.')
