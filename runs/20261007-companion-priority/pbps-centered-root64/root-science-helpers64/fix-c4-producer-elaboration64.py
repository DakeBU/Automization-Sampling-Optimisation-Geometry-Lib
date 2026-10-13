from pathlib import Path
root=Path.cwd();r=root/'runs/20261007-companion-priority/pbps-centered-root64'
src=(r/'combined-draft-v6.lean').read_text(encoding='utf-8')
old='''  obtain ⟨_,G,_,hClose,hClosed,hGraph,hPI⟩ :=
    AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalPoincare.actual_gaussian_marginal_centered_poincare
      hα hαβ hV hH hη hβη
  obtain ⟨_,G',_,_,_,hGraph',Tr,K,hRough⟩ :=
    RoughMeanGradient.actual_rough_mean_gradient hα hαβ hV hH hη hβη
'''
new='''  have hPIBase :=
    AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalPoincare.actual_gaussian_marginal_centered_poincare
      (E:=E) (V:=V) (α:=α) (β:=β) (η:=η) hα hαβ hV hH hη hβη
  dsimp only at hPIBase
  rcases hPIBase with ⟨_,G,_,hClose,hClosed,hGraph,hPI⟩
  have hRoughBase := RoughMeanGradient.actual_rough_mean_gradient
    (E:=E) (V:=V) (α:=α) (β:=β) (η:=η) hα hαβ hV hH hη hβη
  dsimp only at hRoughBase
  rcases hRoughBase with ⟨_,G',_,_,_,hGraph',Tr,K,hRough⟩
'''
assert src.count(old)==1
src=src.replace(old,new)
full=r/'combined-draft-v8.lean';assert not full.exists()
full.write_text(src,encoding='utf-8',newline='\n')
markers={
 '  have hPIBase :=':'BEFORE_GAUSSIAN_PRODUCER',
 '  have hRoughBase :=':'AFTER_GAUSSIAN_BEFORE_ROUGH_PRODUCER',
 '  have hSameG :':'AFTER_ROUGH_BEFORE_GRAPH_IDENTIFICATION',
 '  have hSameT :':'AFTER_GRAPH_BEFORE_MEAN_IDENTIFICATION',
}
prefix=src.split('  subst Tr\n')[0]+'  subst Tr\n'
for fragment,label in markers.items():
 assert prefix.count(fragment)==1
 prefix=prefix.replace(fragment,'  run_tac Lean.logInfo "64_DIAGNOSTIC_'+label+'"\n'+fragment)
prefix+='  exact noProof64_C4_V8_DIAGNOSTIC_INTENTIONALLY_UNDEFINED\n\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredRootOrderInverse\n'
p=r/'c4-prefix-diagnostic-v8.lean';assert not p.exists();p.write_text(prefix,encoding='utf-8',newline='\n')
print('v8 internally fixes all implicit producer parameters and exposes their definitional lets before destructuring. No type or mathematical premise changed. Diagnostic has four bounded stage markers and an undefined tail.')
