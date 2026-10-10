from pathlib import Path
import datetime,hashlib,json,re,sys
R=Path('E:/Samplinglib');O=Path(__file__).parent
sys.path.insert(0,str(R))
from tools import astis
def pin(p):
 p=Path(p);b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def put(name,v):
 with (O/name).open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
 return pin(O/name)
t=(O/'fresh-whole-source-kernel.stdout.log').read_text('utf8')
def values(marker):return re.findall('^'+re.escape(marker)+r' (.+)$',t,re.M)
owned=values('LOCAL_PROOF_CONSTANT');direct=values('EXTERNAL_ASTIS_DEPENDENCY');trans=values('TRANSITIVE_ASTIS_CONSTANT');edges=values('TRANSITIVE_ASTIS_EDGE');generic=values('GENERIC_DEPENDENCY')
assert len(owned)==18 and len(direct)==24 and len(trans)==77 and len(edges)==126 and len(generic)==545
assert not values('LOCAL_NO_VALUE') and not values('PROJECT_NO_VALUE')
axioms_match=re.search(r'depends on axioms:\s*\[([^]]+)\]',t,re.S);assert axioms_match
axioms=[x.strip() for x in axioms_match.group(1).split(',')]
assert set(axioms)=={'propext','Classical.choice','Quot.sound'} and len(axioms)==3
public=[s for s in direct if s.startswith('AutoSamplingTheory.')]
assert len(public)==6
assert not any('ActualConditionalNextWaitSurvival' in s for s in owned+direct+trans)
def source_for(n):
 n=n[n.rfind('AutoSamplingTheory.'):]
 parts=n.split('.')
 for k in range(len(parts),0,-1):
  p=R/('/'.join(parts[:k])+'.lean')
  if p.is_file():return p
 raise AssertionError('No actual source found: '+n)
files=sorted({source_for(n) for n in owned+direct+trans})
bindings=[{'constant':n,'source':pin(source_for(n))} for n in sorted(set(owned+direct+trans))]
kernel=put('kernel-dependency89.json',{
 'schema':1,'status':'ACCEPTED_NATIVE_ELABORATED_KERNEL_CLOSURE','reviewer_id':'/root/exact_verify77',
 'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'module':pin(R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualConditionalNextWaitDensity.lean'),
 'probe':pin(O/'FreshWholeSourceKernelClosure89.lean'),'native_log':pin(O/'fresh-whole-source-kernel.stdout.log'),
 'standard_axioms_only':True,'axioms':axioms,'owned_constants':owned,'owned_constant_count':len(owned),
 'owned_generated_constants_included':True,'immediate_ASTIS_dependencies':direct,'immediate_public_producers':public,
 'immediate_public_count':len(public),'immediate_private_generated_count':len(direct)-len(public),
 'transitive_ASTIS_constants':trans,'transitive_ASTIS_constant_count':len(trans),'transitive_ASTIS_edges':edges,
 'transitive_ASTIS_edge_count':len(edges),'generic_direct_dependencies':generic,'generic_direct_count':len(generic),
 'ASTIS_source_files':[pin(p) for p in files], 'ASTIS_source_file_count':len(files),'constant_source_bindings':bindings,
 'all_project_constants_have_value':True,'actual88_absent':True,
 'method':'Actual fresh whole-source Lean elaboration; traverse type and value of public theorem and all owned generated constants, then recursively every ASTIS dependency type/value. Generic Mathlib/Lean constants logged separately. Source binding uses the longest existing real file prefix, not graph name scans.',
 'mathematical_dependency_roles':{
  'ActualHazardClock':'Joint actual hazard and hitting-time Borel APIs.',
  'ActualHarmonicFlow':'Joint continuous/measurable actual harmonic flow.',
  'ActualBounceRate':'Joint continuous actual nonnegative bounce rate.',
  'UnitExponentialProduct':'Actual P probability internally.',
  'ActualFiniteHistoryTailLaw':'Actual H and raw unused-tail product law.',
  'ActualFiniteFirstEventLaw':'Exact deterministic actual Ioc density map law, further restricted on both sides.'},
 'generic_roles':'Sum/product measurable equivalences, WithTop extraction/comparison, kernel withDensity measurable branch, measure restriction/map, product sections, ENNReal lintegral withDensity/indicator and Tonelli. These are compiled generic proof ingredients, not new public PBPS hypotheses.',
 'claim_limit':'Independent mathematical/kernel evidence only; no source-blind decoder/final source/VERIFIED/aggregate credit.'})
hits=astis.forbidden_pattern_hits()
fake=put('fake-closure89.json',{'schema':1,'reviewer_id':'/root/exact_verify77','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'function':'tools.astis.forbidden_pattern_hits','scanner':pin(R/'tools/astis.py'),'scope':'All current production ASTIS Lean sources, Tests and roots returned by lean_source_files; comments/strings stripped by canonical scanner. Does not claim aggregate Lean build.','source_file_count':len(astis.lean_source_files()),'hits':hits,'pass':not hits,'module':pin(R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualConditionalNextWaitDensity.lean')})
assert not hits,hits
print(json.dumps({'kernel':kernel,'source_files':len(files),'public_producers':public,'fake_closure':fake},ensure_ascii=False))
