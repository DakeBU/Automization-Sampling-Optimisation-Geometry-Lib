import pathlib,json,hashlib,datetime
R=pathlib.Path('E:/Samplinglib'); O=pathlib.Path(__file__).parent
def raw(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def save(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
inputs=[]
for name in ['declaration_lessons','publications']:
 p=R/'website/content'/name/'pbps-actual-finite-count-path.json'
 snap=O/('exposition-revised-'+name+'.RAW.json');snap.write_bytes(p.read_bytes())
 inputs.append({**raw(p),'snapshot':raw(snap)})
lesson=json.loads((O/'exposition-revised-declaration_lessons.RAW.json').read_bytes())['units'][0]
pub=json.loads((O/'exposition-revised-publications.RAW.json').read_bytes())['items'][0]
production=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteCountPath.lean'
src=production.read_text(encoding='utf-8')
assert raw(production)['raw_sha256']=='4926508e4b11b3d4823056e1068f601d4a95b6a5e1ec495b7902cc3c4a1d2943'
assert lesson['statement']==pub['statement']
assert lesson['assumptions']==pub['assumptions']
assert len(lesson['steps'])==9
assert all(x['lean'].strip() in src for x in lesson['steps'])
assert 'arbitrary measurable for these sigma algebras' in lesson['assumptions'][3]
assert 'if this set is nonempty' in lesson['steps'][0]['formula']
assert 'all positive-index times below T' in lesson['steps'][7]['text']
assert 'Proof not implemented' not in pub['purification']['dead_code_audit']
record={
 'schema_version':1,'reviewer':'independent_whole_math93','role':'independent-mathematics-exposition-consistency-verifier',
 'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'decision':'ACCEPT_REVISED_MATHEMATICAL_EXPOSITION_CONSISTENT_WITH_EXACT_SEALED_LEAN',
 'supersedes':'Only the pending-authored-input exposition field of whole-math-decision93.native.json; original mathematical/kernel verdict remains unchanged.',
 'production':raw(production),'inputs':inputs,'necessary_fixes':[],
 'resolved_initial_findings':['path-sigma','empty-eligible','zero-count-prefix','stale-purification-note'],
 'checks':{'lesson_publication_statements_equal':True,'assumptions_equal':True,'nine_exact_compiled_regions':True,'production_raw_unchanged':True},
 'proof_step_audit':[{'step':i+1,'title':x['title'],'exact_lean_region_in_production':True,'mathematical_explanation':'accepted'} for i,x in enumerate(lesson['steps'])],
 'statement_audit':[
  'All six analytic conditions and finite-dimensional Borel carrier are explicit; no extra theorem-shaped provider is supplied.',
  'Literal flow, reflection, rate, integrated hazard, hitting clock, stopped recurrence, canonical input measure, raw clock extension, history guard, count selector, interpolation, simplex measure and density agree with checked definitions.',
  'Every path-target and path-test measurability claim is explicitly tied to stated sigma algebras. Euclidean/Borel Z and history claims remain justified.',
  'Raw covered-arc/fallback characterization and raw C path identity are separated from fixed-parameter initialization and fixed-horizon count/endpoint AE conclusions.',
  'Finite-count joint measure, arbitrary measurable nonnegative extended tests and exact unnormalized mass are stated with the same measures and restrictions as Lean.',
  'Zero-event terminal survival, zero horizon, infinite waits, rank-zero and exceptional raw fallbacks are not silently excluded.',
  'Formula maximum has nonempty-set guard and z0 fallback; prefix description at zero horizon restricts below-T only to positive indices.',
  'No full A.7, Skorokhod/left-limit result, infinite summation, Markov/restart, invariance, query-cost, composition or whole-paper completion is claimed.'
 ],
 'scope_limit':'Mathematics and exposition consistency only. No source-fidelity decision, publication admission, website rendering acceptance, postmerge purification or whole-Goal completion. Primary-source review belongs to a distinct reviewer.',
 'failed_trials':[]
}
save('exposition-supplement93.native.json',record)
old=O/'closed-RAW93.native.json'; (O/'closed-RAW93.pre-exposition.native.json').write_bytes(old.read_bytes())
orig=json.loads((O/'input-manifest93.native.json').read_bytes())
assert all(raw(R/x['path'])['raw_sha256']==x['raw_sha256'] for x in orig['inputs'])
assert all(raw(R/x['path'])['raw_sha256']==x['raw_sha256'] for x in inputs)
artifacts=[raw(f) for f in sorted(O.rglob('*')) if f.is_file() and f.name!='closed-RAW93.native.json']
save('closed-RAW93.native.json',{'schema_version':1,'closure':'All owned run files except this manifest; parent binds manifest RAW. Original review evidence retained, revised exposition input snapshots pinned.','artifacts':artifacts,'external_inputs':orig['inputs']+inputs,'all_external_inputs_rehashed_unchanged':True,'runtime':[raw(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),raw(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe')]})
print(json.dumps({'supplement':raw(O/'exposition-supplement93.native.json'),'manifest':raw(O/'closed-RAW93.native.json'),'revised_inputs':inputs,'artifacts':len(artifacts)},ensure_ascii=False,indent=2))
