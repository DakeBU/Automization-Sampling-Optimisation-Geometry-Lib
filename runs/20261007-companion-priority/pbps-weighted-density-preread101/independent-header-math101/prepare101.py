from pathlib import Path
import hashlib,json,re,os,subprocess,datetime
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;P=O.parent;H=P/'Header101.lean'
def info(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def save(n,x):
 p=O/n;assert not p.exists();p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
h=H.read_text(encoding='utf8');base=R/'AutoSamplingTheory/ExampleCases/ProximalBPS';density=(base/'ActualPrescribedPathDensity.lean').read_text(encoding='utf8');pub=density[density.index('theorem actual_prescribed_path_density_rewrite'):]
old=pub[pub.index('    let c :'):pub.index('    ∀ y xRef :')]
new=h[h.index('    let c :'):h.index('    let R :')]
assert re.sub(r'\s+','',old)==re.sub(r'\s+','',new)
lets=re.findall(r'^    let (\S+)',new,re.M);assert len(lets)==20
primary=R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
assert info(primary)['raw_sha256']=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
save('pre-graph-reconstruction101.native.json',dict(kind='independent-mathematical-reconstruction-before-reading101-source-graph',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),reviewer='/root/exact_verifier96',header=info(H),primary=info(primary),prior_context='Reviewer knows earlier99/100 source graphs and independently reviewed their mathematics. The newly authored101 graph/recommendation/coverage have not yet been read. This is not a claim of blindness to earlier work.',twenty_density_definitions_exact_modulo_whitespace=lets,source_regions=[dict(lines=[3176,3198],purpose='A8 reversal and distinct later measure-preserving change of variables'),dict(lines=[3200,3227],purpose='Integrated energy/survival identity plus event factors, then later sector integration/invariance')],route_at_most_seven_steps=[
 'Obtain rho and product equality from actual99 and rho2 with survival equality from actual100. Their coordinate equations force equality pointwise by funext/Subtype.ext; use one common witness. Alternatively choose100 witness then identify99 witness. This alignment is an internal dependency, not a new public premise.',
 'Identify actual99 incoming event product with literal P through the cons/snoc grid identities. Obtain P(reverse)=P(forward), without cancellation or positive-rate assumptions.',
 'Use actual100 to replace the reversed forward integral I(reverse) by the original momentum-reversed integral Iminus. Its actual A and clamp definitions match101 exactly.',
 'Use actual98 exp(-U(z))*exp(-Iplus)=exp(-U(A))*exp(-Iminus). Derive U(R A)=U(A) directly from norm_neg and unchanged position, hence w(R A)=w(A).',
 'Multiply this balance by the common event product and reassociate. This gives the requested real w*dReal equality with the correct negative signs and no missing normalization factor.',
 'Apply actual94 to each original/reversed actual input to identify literal rhoDensity=q*terminalweight with ENNReal.ofReal(dReal). All twenty definitions are unchanged; this is an actual density bridge, not a redefinition of rhoDensity.',
 'Apply congrArg ENNReal.ofReal to the real identity and use ENNReal.ofReal_mul with nonnegativity of each exponential weight to obtain the requested ENNReal weighted identity.'
 ],checks={'original_six_binders':True,'extra_public_provider_premises':False,'energy':'V(x)+||x-y||^2/(2 eta)+||p||^2/2; reversal changes only p, norm squared unchanged.','weight':'Unnormalized exp(-U); no Gibbs normalizing constant or probability measure claim.','n0':'Empty event product1, density terminal survival; equality reduces to98+100.','T0n0':'A=z, no survival integral, product1; w(Rz)=w(z).','T0npos':'Strict prefix empty.','rank0':'Allowed; rates0; npositive densities0, n0 valid.','zero_normals_or_rates':'Literal total reflection and zero factors retained; no division/cancellation of rates.','right_continuity':'Only the already-integrated100 identity is consumed; no equality at genuine jumps is added.','scope':'Two pointwise weighted-density identities; no measure/integral invariance, normalized Gibbs, stationarity or full A8 sector claim.'},required_graph_dependencies=['Coordinate witness alignment from99 and100','99 incoming product -> real weighted identity','100 survival -> real weighted identity','98 Gibbs/survival -> real weighted identity','R/U definition and norm_neg -> weight parity -> real weighted identity','94 actual density bridge + real weighted identity + positive exp/ofReal_mul -> ENNReal weighted identity'],no_implementation=True))
w=O/'Header101.TypeOnly.lean';w.write_bytes(H.read_bytes())
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None);env['PYTHONUTF8']='1';env['LEAN_NUM_THREADS']='2';env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
argv=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(w.relative_to(R))]
p=subprocess.run(argv,cwd=R,env=env,capture_output=True)
(O/'type-only.stdout.log').write_bytes(p.stdout);(O/'type-only.stderr.log').write_bytes(p.stderr)
save('type-only-receipt101.native.json',dict(argv=argv,exit_code=p.returncode,terminal_closed=True,header=info(H),exact_copy=info(w),full_theorem_proof=False))
print(p.stdout.decode('utf8',errors='replace'));print(p.stderr.decode('utf8',errors='replace'));assert p.returncode==0
