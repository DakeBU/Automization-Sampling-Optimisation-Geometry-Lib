from pathlib import Path
import hashlib,json,subprocess,os,time
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent
def write(n,s):
 p=O/n;assert not p.exists();p.write_bytes(s.encode())
imports='\n'.join(x for x in (O.parent/'Header103.lean').read_text(encoding='utf8').splitlines() if x.startswith('import '))+'\n'
good=['AutoSamplingTheory.TechnicalLemmas.Analysis.HessianStrongConvexity.strongConvexOn_univ_of_fderiv2_lower','AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexGibbsIntegrability.integrable_exp_neg_of_strongConvexOn','AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability.lintegral_exp_neg_mul_norm_sq_eq','AutoSamplingTheory.TechnicalLemmas.Measure.IsotropicGaussianDensity.map_sqrt_smul_stdGaussian_eq_withDensity','AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs.isProbabilityMeasure_withDensity_normalized_gibbs','MeasureTheory.Integrable.mono\'','MeasureTheory.integral_exp_pos','MeasureTheory.ofReal_integral_eq_lintegral_ofReal','MeasureTheory.lintegral_prod_mul','MeasureTheory.prod_withDensity','MeasureTheory.prod_withDensity_left','MeasureTheory.Measure.tilted','MeasureTheory.isProbabilityMeasure_tilted','Real.sqrt_eq_rpow','Real.rpow_mul_natCast','ENNReal.ofReal_inv_of_pos','ENNReal.ofReal_mul','ENNReal.ofReal_div_of_pos']
write('PinnedAPIs103.lean',imports+'\n'.join('#check '+x for x in good)+'\n')
write('CreatorNamespaceDiagnostic103.lean',imports+'#check MeasureTheory.Measure.prod_withDensity\n#check MeasureTheory.Measure.prod_withDensity_left\n')
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None);env['PYTHONUTF8']='1';env['LEAN_NUM_THREADS']='2';env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
for name in ['PinnedAPIs103','CreatorNamespaceDiagnostic103']:
 argv=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(O/(name+'.lean'))];t=time.time()
 with (O/(name+'.stdout.log')).open('xb') as out,(O/(name+'.stderr.log')).open('xb') as err:p=subprocess.run(argv,cwd=R,env=env,stdout=out,stderr=err)
 write(name+'.receipt.json',json.dumps(dict(command=argv,exit_code=p.returncode,seconds=time.time()-t,prospective_API_name_check_only=True,no_candidate_proof=True),indent=2)+'\n');print(name,p.returncode,flush=True)
