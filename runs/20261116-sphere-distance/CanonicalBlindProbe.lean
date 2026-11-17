import AutoSamplingTheory.TechnicalLemmas.Geometry.UnitSphereInducedPathDistance
set_option format.width 120
set_option pp.fullNames true
set_option pp.universes false
set_option pp.proofs true
#eval IO.println "STATEMENT_BEGIN"
#check AutoSamplingTheory.TechnicalLemmas.Geometry.UnitSphereInducedPathDistance.unit_sphere_induced_riemannianEDist_eq_arccos
#eval IO.println "STATEMENT_END"
#print axioms AutoSamplingTheory.TechnicalLemmas.Geometry.UnitSphereInducedPathDistance.unit_sphere_induced_riemannianEDist_eq_arccos
#eval IO.println "CONTEXT_BEGIN"
#print Manifold.riemannianEDist
#print Manifold.pathELength
#print mvfderiv
