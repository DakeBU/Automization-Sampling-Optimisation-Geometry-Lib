from pathlib import Path
r=Path('runs/20261007-companion-priority/pbps-centered-root64')
s=(r/'combined-draft-v8.lean').read_text(encoding='utf-8')
patches=[
('''    intro u v
    simp only [hQ,inner_sub_left,inner_sub_right,inner_smul_left,inner_smul_right]
    rw [real_inner_comm v q]
    ring
''','''    intro u v
    change inner ℝ (Q u) v=inner ℝ u (Q v)
    simp only [hQ,inner_sub_left,inner_sub_right,inner_smul_left,inner_smul_right,
      starRingEnd_apply,star_trivial]
    rw [real_inner_comm q u]
    ring
'''),
('real_inner_comm (Q u) q,hQmean','real_inner_comm q (Q u),hQmean'),
('''    rw [← hΓQ u,hΓEnergy,← pow_two γ,hγSq]
    nlinarith [hcSq]
''','''    rw [← hΓQ u,hΓEnergy,← pow_two γ,hγSq]
    simp only [starRingEnd_apply,star_trivial]
    nlinarith only [hcSq]
'''),
('''    rw [← e.apply_symm_apply f, e.inner_map_map,hq]
''','''    rw [← e.apply_symm_apply f, e.inner_map_map,hq,e.symm_apply_apply]
'''),
('''      ContinuousLinearMap.one_apply,inner_sub_left,inner_smul_left,real_inner_self_eq_norm_sq] at h
''','''      ContinuousLinearMap.one_apply,inner_sub_left,inner_smul_left,real_inner_self_eq_norm_sq,
      starRingEnd_apply,star_trivial] at h
'''),
('''    change ↑(hUnit.unit⁻¹)*ΓP0=1
    rw [← hUnit.unit_spec]
    exact Units.inv_mul hUnit.unit
''','''    exact (congrArg (fun C : HP0 →L[ℝ] HP0 => Inv*C) hUnit.unit_spec).symm.trans
      (Units.inv_mul hUnit.unit)
'''),
('''    change ΓP0*↑(hUnit.unit⁻¹)=1
    rw [← hUnit.unit_spec]
    exact Units.mul_inv hUnit.unit
''','''    exact (congrArg (fun C : HP0 →L[ℝ] HP0 => C*Inv) hUnit.unit_spec).symm.trans
      (Units.mul_inv hUnit.unit)
'''),
('apply ContinuousLinearMap.opNorm_le_bound (by positivity)','apply Inv.opNorm_le_bound (show 0≤1/γ from by positivity)'),
]
for old,new in patches:
 assert s.count(old)==1,(old,s.count(old))
 s=s.replace(old,new)
p=r/'combined-draft-v9.lean';assert not p.exists();p.write_text(s,encoding='utf-8',newline='\n')
print('v9: typed symmetric action, real scalar conjugation, exact inverse application congruence and explicit opNorm operator. Same sealed declarations.')
