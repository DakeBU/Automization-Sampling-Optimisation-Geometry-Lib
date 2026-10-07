# coding: utf-8
import pathlib,re,sys
sys.stdout.reconfigure(encoding='utf-8');files=['AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicEnergy.lean','Tests/ProximalBPSMacroscopicEnergy.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicRepresentative.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/ReflectionL2.lean']
for f in files:
 print(f)
 for i,s in enumerate(pathlib.Path(f).read_text(encoding='utf-8').splitlines(),1):
  if re.match(r'\s*(?:theorem |have (?:norm_snd|hmap|hΛmap|hfst |hΛcond|hκ |hκJ|hUU|hAgS|hgn |hAgn |hvariance|reflected_disintegration|macroscopic_class|projection_kernel|fiber_ae|expectation_memLp|expectation_map|compressed_representative|reflection_lift|kernel_condExp|block_algebra|block_energy|hTf |hAgEq|hmass|hgn1|hAgn1|hB0))',s): print(i,s[:130])
