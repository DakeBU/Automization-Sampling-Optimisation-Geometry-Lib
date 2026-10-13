import pathlib,json,hashlib,subprocess,os,time,datetime
R=pathlib.Path('E:/Samplinglib'); O=pathlib.Path(__file__).parent
def raw(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def save(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
old=R/'runs/20261007-companion-priority/pbps-actual-finite-count-path93/scoped-classical93/module.before.exactraw.lean'
prod=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteCountPath.lean'
header=R/'runs/20261007-companion-priority/pbps-finite-count-path-preread93/Header93.lean'
core=R/'.astis/toolchain/lean-4.33.0-windows/src/lean/Init/Classical.lean'
assert raw(old)['raw_sha256']=='4926508e4b11b3d4823056e1068f601d4a95b6a5e1ec495b7902cc3c4a1d2943'
assert raw(prod)['raw_sha256']=='5467078f497e0d40e1916550b2e5e9a5be992a69b20fc143bda06dd988d86d9d'
assert old.read_bytes().count(b'attribute [local instance] Classical.propDecidable')==1
assert old.read_bytes().replace(b'attribute [local instance] Classical.propDecidable',b'open scoped Classical')==prod.read_bytes()
orig=json.loads((O.parent/'input-manifest93.native.json').read_bytes())
deps=[x for x in orig['inputs'] if x['path'].startswith('AutoSamplingTheory/') and x['path']!=raw(prod)['path']]
assert all(raw(R/x['path'])['raw_sha256']==x['raw_sha256'] for x in deps)
inputs=[raw(f) for f in [old,prod,header,core,R/'lean-toolchain',R/'lake-manifest.json']]
for i,f in enumerate([old,prod,header,core,R/'lean-toolchain',R/'lake-manifest.json']):
 (O/f'{i:02d}.{f.name}.RAW').write_bytes(f.read_bytes())
save('exact-delta93.native.json',{'old':raw(old),'new':raw(prod),'line':29,'old_text':'attribute [local instance] Classical.propDecidable','new_text':'open scoped Classical','only_raw_byte_change':True,'baseline_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'dependencies_rehashed_unchanged':deps,'inputs':inputs})
p=prod.read_text(encoding='utf-8');h=header.read_text(encoding='utf-8')
decl=h.split('def candidate_finite_count_path_statement',1)[1].split('\n#check',1)[0].rstrip()
assert decl==p.split('private def actual_finite_count_path_statement',1)[1].split('/-- Exact sealed',1)[0].rstrip()
binder=decl.split(' : Prop := by',1)[0]
w=p+'\n'+h[h.index('namespace Candidate93'):]+'\nnamespace ScopedClassicalReview93\nopen InnerProductSpace MeasureTheory ProbabilityTheory Filter\nopen scoped ContDiff NNReal ENNReal Topology Interval BigOperators Classical\nnoncomputable section\nset_option autoImplicit false\n'
w+='theorem scoped_instance_is_core (p : Prop) : (inferInstance : Decidable p) = Classical.propDecidable p := rfl\n'
w+='theorem decision_witness_independence (p : Prop) (d1 d2 : Decidable p) : d1 = d2 := Subsingleton.elim _ _\n'
w+='theorem sealed_header_witness'+binder+' : Candidate93.candidate_finite_count_path_statement hα hαβ hV hH hη hβη := by\n  exact AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteCountPath.actual_finite_count_path_law hα hαβ hV hH hη hβη\n'
w+='#check @AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteCountPath.actual_finite_count_path_law\n#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteCountPath.actual_finite_count_path_law\n#print axioms sealed_header_witness\n#print axioms scoped_instance_is_core\n#print axioms decision_witness_independence\nend\nend ScopedClassicalReview93\n'
wp=O/'ScopedClassicalKernelWitness93.lean';wp.write_text(w,encoding='utf-8')
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None)
lake=R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'
checks=[]
for name,f in [('fresh-scoped-production',prod),('fresh-scoped-sealed-witness',wp)]:
 t=time.time();cmd=[str(lake),'env','lean',str(f)]
 with (O/(name+'.stdout.log')).open('wb') as stdout,(O/(name+'.stderr.log')).open('wb') as stderr:
  r=subprocess.run(cmd,cwd=R,env=env,stdout=stdout,stderr=stderr)
 checks.append({'name':name,'command':cmd,'exit_code':r.returncode,'elapsed_seconds':time.time()-t,'source':raw(f),'ELAN_TOOLCHAIN_removed':True})
 save('kernel-receipt93.native.json',{'checks':checks});print(name,r.returncode,flush=True)
assert all(x['exit_code']==0 for x in checks)
assert all(raw(R/x['path'])['raw_sha256']==x['raw_sha256'] for x in inputs+deps)
report={'schema_version':1,'reviewer':'independent_whole_math93','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'decision':'ACCEPT_SCOPED_CLASSICAL_WHOLE_MATHEMATICS_TRANSFER','old_module':raw(old),'new_module':raw(prod),'exact_byte_delta_only_line29':True,'header_literal_unchanged':True,'kernel_checks':checks,'axioms':['propext','Classical.choice','Quot.sound'],'core_evidence':{'file':raw(core),'line':81,'declaration':'noncomputable scoped instance (priority := low) propDecidable (a : Prop) : Decidable a'},'semantic_analysis':['open scoped Classical activates the existing Lean core Classical.propDecidable scoped instance; it does not declare a new premise or mathematical provider.','The old local instance registration and scoped activation may affect instance-search priority. This review does not assert all elaborated proof terms or decisions are byte-identical.','Fresh scoped_instance_is_core proves by rfl that scope-based inference for an arbitrary proposition yields the core instance. Decidable p is a subsingleton, so alternative decision witnesses cannot change mathematical values; the existing find_decidable_eq helper explicitly handles this for the total count.','Both the exact changed production module and a fresh file containing that entire changed module plus independent sealed-header witness compile. The public theorem still inhabits the exact independent literal statement and has only standard axioms.','All declaration bodies, signatures, imports, literal definition formulas and proof text are byte-unchanged. All local imported Lean sources rehash equal to the independently reviewed versions. Prior whole mathematical reasoning and exposition-region comparison therefore transfer.'],'necessary_fixes':[],'scope_limit':'This acceptance is whole mathematics/kernel transfer for the one-line scoped-instance repair. Source-fidelity packet transfer, publication inventory admission, aggregate build and reader acceptance remain separate. Original decisions and closed manifests are unmodified.','failed_trials':[]}
save('scoped-classical-transfer93.native.json',report)
save('closed-RAW-scoped-classical93.native.json',{'artifacts':[raw(f) for f in sorted(O.iterdir()) if f.is_file() and f.name!='closed-RAW-scoped-classical93.native.json'],'closure':'Only this new scoped-classical93 directory, excluding manifest itself.','all_inputs_and_local_dependencies_rehashed_unchanged':True,'runtime':[raw(lake),raw(lake.with_name('lean.exe'))]})
print(json.dumps({'decision':raw(O/'scoped-classical-transfer93.native.json'),'manifest':raw(O/'closed-RAW-scoped-classical93.native.json')},indent=2))
