from pathlib import Path
import hashlib,json,os,subprocess
root=Path.cwd();old=root/'runs/20261007-companion-priority/pbps-first-corrector-energy-preproof67'
r=root/'runs/20261007-companion-priority/pbps-sharp-energy-preproof68';r.mkdir(exist_ok=False)
imports='''import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualRootCommutation
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped RealInnerProductSpace ContDiff NNReal Topology ENNReal
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 2000000
'''
generic='''theorem quadratic_corrector_bound_of_square_identity
    {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]
    (K D : H →L[ℝ] H) (hK : IsSelfAdjoint K) (hD : IsSelfAdjoint D)
    (hSquare : (1 : H →L[ℝ] H)+K*K=D*D)
    (c : ℝ) (hc : 0 ≤ c) (hNorm : ‖D‖ ≤ c) (u v : H) :
    |(1/2 : ℝ)*(‖u‖^2-‖v‖^2)-inner ℝ (K u) v| ≤
      (c/2)*(‖u‖^2+‖v‖^2)
'''
base=(old/'header2-expanded.lean').read_text(encoding='utf-8')
start=base.index('theorem genuine_actual_corrector_coefficient_consumer')
base=base[start:]
# Expanded headers contain only the complete proposition, with no proof body.
assert ':= by' not in base and 'sorry' not in base
main=base.replace('genuine_actual_corrector_coefficient_consumer','actual_sharp_corrector_bound',1)
point='                    let Hperp := P.ker'
assert main.count(point)==1
main=main.replace(point,'''                    let C : HP0 → HP0 → ℝ := fun u v =>
                      (1/2 : ℝ)*(‖u‖^2-‖v‖^2)-inner ℝ ((A0*Inv) u) v
                    (∀ u v : HP0, |C u v| ≤ (‖u‖^2+‖v‖^2)/(2*γ)) ∧
'''+point)
tail='‖f‖^2=‖fP‖^2+‖fperp‖^2 ∧ ‖fV‖≤‖fperp‖)'
assert main.count(tail)==1
main=main.replace(tail,'''‖f‖^2=‖fP‖^2+‖fperp‖^2 ∧ ‖fV‖≤‖fperp‖ ∧
                              ‖fP‖^2+‖fV‖^2≤‖f‖^2 ∧
                              |C fP fV|≤‖f‖^2/(2*γ))''')
test=main.replace('actual_sharp_corrector_bound','genuine_actual_modified_energy_equivalence',1)
tail2='|C fP fV|≤‖f‖^2/(2*γ))'
assert test.count(tail2)==1
test=test.replace(tail2,'''|C fP fV|≤‖f‖^2/(2*γ) ∧
                              (∀ ω : ℝ, 0<ω → ω≤γ →
                                let L : ℝ := ‖f‖^2+ω*C fP fV
                                (1/2 : ℝ)*‖f‖^2≤L ∧ L≤(3/2 : ℝ)*‖f‖^2 ∧
                                |L-‖f‖^2|≤(ω/(2*γ))*‖f‖^2 ∧
                                (ω/(2*γ))*‖f‖^2≤(1/2 : ℝ)*‖f‖^2))''')
entries=[]
for i,text in enumerate([generic,main,test]):
 p=r/f'header{i}-expanded.lean';p.write_text(imports+'\n'+text,encoding='utf-8',newline='\n')
 name=['quadratic_corrector_bound_of_square_identity','actual_sharp_corrector_bound','genuine_actual_modified_energy_equivalence'][i]
 pre,body=text.split(' :\n',1) if i==0 else (None,None)
 if i:
  # Reuse the already independently reviewed literal-Prop representation.
  definition=(old/f'statement{i}.definition.lean').read_text(encoding='utf-8') if i==2 else (old/'statement2.definition.lean').read_text(encoding='utf-8')
  oldname='genuine_actual_corrector_coefficient_consumer_statement'
  assert oldname in definition
  definition=definition.replace(oldname,name+'_statement',1)
  definition=definition.replace(point,'''                    let C : HP0 → HP0 → ℝ := fun u v =>
                      (1/2 : ℝ)*(‖u‖^2-‖v‖^2)-inner ℝ ((A0*Inv) u) v
                    (∀ u v : HP0, |C u v| ≤ (‖u‖^2+‖v‖^2)/(2*γ)) ∧
'''+point)
  assert definition.count(tail)==1
  definition=definition.replace(tail,main.split(tail.split(')')[0])[0] if False else '''‖f‖^2=‖fP‖^2+‖fperp‖^2 ∧ ‖fV‖≤‖fperp‖ ∧
                              ‖fP‖^2+‖fV‖^2≤‖f‖^2 ∧
                              |C fP fV|≤‖f‖^2/(2*γ))''')
  if i==2:definition=definition.replace(tail2,test[test.index('|C fP fV|≤‖f‖^2/(2*γ)'):])
  q=r/f'statement{i}.definition.lean';q.write_text(definition,encoding='utf-8',newline='\n')
 entries.append(dict(path=p.relative_to(root).as_posix(),RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),proposed_name=name))
note=dict(status='HEADER68_DRAFT_NOT_SEALED_NOT_CLAIMED_NO_PROOF_SEARCH',actual_preparer_pid=os.getpid(),base=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),source='arXiv:2609.06905v1 Appendix B3 B19/B20/B22/B23/B24, complete344-item source graph already independently built before67 implementation',source_graph='runs/20261007-companion-priority/pbps-first-corrector-energy-preproof67/independent-primary67/source-proof-graph.json',headers=entries,real_consumer='PBPS Lemma B3 norm equivalence, then Lemma B4 one-step hypocoercivity',route_at_most_seven_steps=['Use exact same67 witnesses; internally derive selfadjoint K=A0Inv and I+K²=Inv².','Expand the source two-component block action; use K selfadjointness for cross cancellation.','Use selfadjoint Inv and the square identity to identify each component sum energy with ‖Inv x‖².','Apply two-component Cauchy-Schwarz with exact sum Hilbert energy, never max product norm.','Obtain sharp1/(2gamma) pair estimate; no loose triangle constant.','Consume actual global Pythagoras and polar adjoint contraction to produce B23 on actual centered f.','Genuine original-input Test proves B19/B22/B24 for all0<omega<=gamma.'],scope_boundary='B21 rotation, B2 weak H1, B4 dynamics, main theorem, errors/cost/composition remain independent. No extra premise/c>=1/Nontrivial/strict endpoint; rank0 and alphaeta1 retained.',source_mathematical_repair=False,canonical_Lean_written=False)
(r/'draft68.json').write_text(json.dumps(note,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Prepared complete header68 drafts only; no proof search/claim/Lean production mutation.')
