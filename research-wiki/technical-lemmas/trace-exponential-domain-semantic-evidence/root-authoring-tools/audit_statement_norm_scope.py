from pathlib import Path
r=Path.cwd();w=r/'.astis/huanjian-gc-trace-mgf-domain-20261115'
formation=(w/'InterfaceFormation.v2.lean').read_text()
assert formation.count('open scoped BigOperators Matrix.Norms.L2Operator MatrixOrder ENNReal')==1
extra='''
set_option pp.all true in
#print GCTraceMgfDomainMinimalInterfaceOnly.CandidateP
section ExactNormScopeAudit
variable {ι : Type u} [Fintype ι] [DecidableEq ι] [Nonempty ι]
set_option pp.all true in
#synth Norm (Matrix ι ι ℝ)
end ExactNormScopeAudit
'''
p=w/'StatementNormScopeAudit.lean';assert not p.exists();p.write_text(formation+extra)
print('Only exact proposition/full elaboration and selected norm instance; no target theorem proof.')
