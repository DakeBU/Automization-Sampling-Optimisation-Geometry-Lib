import pathlib, hashlib, json, subprocess, os, time
R=pathlib.Path('E:/Samplinglib')
P=R/'runs/20261007-companion-priority/pbps-normalized-endpoint-preread104'
O=P/'independent-header-math104'
def sha(b): return hashlib.sha256(b).hexdigest()
def bind(p):
 p=pathlib.Path(p); b=p.read_bytes(); return {'path':p.relative_to(R).as_posix(),'sha256_raw':sha(b),'bytes':len(b)}
def save(n,v):
 p=O/n
 if p.exists(): raise RuntimeError('immutable output exists: '+str(p))
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
header=P/'Header104.lean'
assert sha(header.read_bytes())=='4fc65e051233c07d0d2272b3371fad1c1164546b51a4c313c0ec0d314b805be4'
files=[header,R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html']+[R/('AutoSamplingTheory/ExampleCases/ProximalBPS/'+x+'.lean') for x in ['ActualFiniteCountPath','ActualEndpointTimeReversal','ActualWeightedSector','ActualPhaseNormalization']]
save('independent-route-before-graph104.native.json',{
 'reviewer':'/root/exact_verifier96','scope':'Prospective mathematical reconstruction; no implementation or proof credit',
 'creator_graph_seen':False,'inputs':[bind(p) for p in files],
 'source_regions':['A.1 phase Gibbs 1411-1422','A.7/A.8 3162-3198','integrated A.4 and fixed-count weighted reversal 3200-3227'],
 'route':[
 'Use public93 actual joint density measurability and public97 actual endpoint measurability; B is measurable and J continuous.',
 'The literal strict simplex is Borel by finite coordinate inequalities. Its subtype comap volume is sigma-finite via map_comap_subtype_coe and SigmaFinite.of_map. This is a proof ingredient, not a public premise; private97 endpoint_data cannot be called.',
 'Align the public97 and public102 existential time reversals by their identical coordinate equation T-t(i.rev), using function/subtype extensionality. This identifies the same Theta.',
 'Use public103 normalized phase measure equality and prod_withDensity_left plus withDensity_mul to rewrite sigma as (ell.prod m).withDensity(a*W), with a=Zphase inverse and W=ofReal(exp(-U))*actual rho.',
 'Apply public102 weighted nonnegative test identity to test functions composed with B; constant lintegral multiplication transports it through normalization without finite-integral assumptions.',
 'Public97 actual endpoint reversal gives B(Theta q)=J(B q); this is an endpoint identity, requiring no naive all-time reversal at events.',
 'Use measurable pushforward composition/lintegral_map and Measure.ext_of_lintegral to prove J.map L=L; pair with measurable J for MeasurePreserving.'
 ],
 'assumptions':'Exactly original six analytic binders; no density provider, minimizer, normalizer, finite-sector mass, sigma-finiteness or endpoint law added as hypothesis.',
 'edge_cases':{'n0':'Empty tuple, product over no events and actual terminal survival remain literal.','T0_npositive':'Strict simplex empty, sigma and L zero; J preserves zero measure.','T0_n0':'Diagonal endpoint pair; phase reversal still applies.','rank0':'Zero-dimensional volume/Gaussian and totalized reflection remain valid.','zero_normals_rates':'No division by a rate or sector mass. Zero normal reflection is literal totalized identity; zero density allowed.','infinity':'Nonnegative extended integrals; no subtraction or cancellation of infinite quantities.'},
 'new_delta':'Actual normalized fixed-count endpoint-pair measure is invariant under reversed/swapped momentum endpoints; not full process invariance or countable recombination.',
 'preliminary_verdict':'Mathematically viable; graph must cover simplex sigma-finiteness, actual density measurability, witness alignment, normalization transport and endpoint intertwining.'})
target=O/'FreshHeader104.lean'; target.write_bytes(header.read_bytes())
api=O/'API104.lean'
api.write_text('import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualWeightedSector\nimport AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseNormalization\n'+''.join('#check '+s+'\n' for s in ['MeasureTheory.prod_withDensity_left','MeasureTheory.Measure.withDensity_mul','MeasureTheory.Measure.ext_of_lintegral','MeasureTheory.Measure.map_map','MeasureTheory.lintegral_map','MeasureTheory.lintegral_const_mul','MeasureTheory.map_comap_subtype_coe','MeasureTheory.SigmaFinite.of_map','measurableSet_lt','MeasurableSet.iInter']),encoding='utf-8')
env=os.environ.copy(); env.pop('ELAN_TOOLCHAIN',None); env['LEAN_NUM_THREADS']='2'; env['PYTHONUTF8']='1'; env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
for name,p in [('fresh-header',target),('api',api)]:
 t=time.time(); cmd=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(p)]; q=subprocess.run(cmd,cwd=R,env=env,capture_output=True)
 (O/(name+'.stdout.log')).write_bytes(q.stdout); (O/(name+'.stderr.log')).write_bytes(q.stderr)
 save(name+'.receipt.json',{'command':cmd,'exit_code':q.returncode,'elapsed_seconds':time.time()-t,'input':bind(p),'stdout':bind(O/(name+'.stdout.log')),'stderr':bind(O/(name+'.stderr.log'))})
 print(name,q.returncode,flush=True)
