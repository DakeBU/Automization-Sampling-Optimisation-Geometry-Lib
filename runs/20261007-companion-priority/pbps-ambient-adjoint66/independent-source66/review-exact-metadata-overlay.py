from pathlib import Path
import json,hashlib,datetime,os
O=Path(r'E:/Samplinglib/runs/20261007-companion-priority/pbps-ambient-adjoint66/independent-source66');ROOT=Path('E:/Samplinglib');P=O.parent/'presentation-overlay66'/'proposal.json';H=lambda b:hashlib.sha256(b).hexdigest();C=lambda d:H(json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
def put(n,d):(O/n).write_bytes((json.dumps(d,sort_keys=True,indent=2,ensure_ascii=True)+'\n').encode())
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return dict(path=str(p).replace('\\','/'),RAW_bytes=len(b),RAW_sha256=H(b),LF_bytes=len(lf),LF_sha256=H(lf))
def diff(a,b,path=()):
 if type(a)!=type(b):return [(path,a,b)]
 if isinstance(a,dict):
  assert set(a)==set(b);r=[]
  for k in a:r.extend(diff(a[k],b[k],path+(k,)))
  return r
 if isinstance(a,list):
  if len(a)!=len(b):return [(path,a,b)]
  r=[]
  for i,(x,y) in enumerate(zip(a,b)):r.extend(diff(x,y,path+(i,)))
  return r
 return [] if a==b else [(path,a,b)]
b=P.read_bytes();proposal=json.loads(b);(O/'overlay.proposal.RAW.json').write_bytes(b);(O/'overlay.proposal.LF.json').write_bytes(b.replace(b'\r\n',b'\n'));calls=['AutoSamplingTheory.TechnicalLemmas.Measure.L2Expectation.one','AutoSamplingTheory.TechnicalLemmas.Measure.L2Expectation.inner_one_eq_integral'];main=(ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/AmbientAdjointCorrector.lean').read_text(encoding='utf-8');assert all(x in main for x in calls);entries=[];changes=[]
assert len(proposal['entries'])==4
for i,e in enumerate(proposal['entries']):
 before=ROOT/e['before_snapshot']['path'];after=ROOT/e['proposed']['path'];bb=before.read_bytes();ab=after.read_bytes();assert H(bb)==e['before']['raw_sha256']==e['before_snapshot']['raw_sha256'];assert H(ab)==e['proposed']['raw_sha256'];assert (ROOT/e['canonical']).read_bytes()==bb
 ds=diff(json.loads(bb),json.loads(ab));assert len(ds)==1;path,old,new=ds[0];assert list(path)==e['allowed_field_paths'][0];assert new==old+calls
 (O/('overlay.%d.before.RAW.json'%i)).write_bytes(bb);(O/('overlay.%d.proposed.RAW.json'%i)).write_bytes(ab)
 entries.append(dict(canonical=e['canonical'],before_snapshot=pin(O/('overlay.%d.before.RAW.json'%i)),proposed_snapshot=pin(O/('overlay.%d.proposed.RAW.json'%i)),allowed_field_paths=e['allowed_field_paths'],all_other_JSON_fields_equal=True,exact_two_list_appends=True));changes.append(dict(file=e['canonical'],path=list(path),before=old,after=new))
for x in proposal['compiled_proof_inputs']:assert H((ROOT/x['path']).read_bytes())==x['raw_sha256']
assert changes==proposal['changes'];assert proposal['source_mathematical_repair'] is False and proposal['formula_changes']==0
slots={k:dict(original='Original compiled proposition,source conditions and geometry preserved',reconstructed='Same proposition with two directly invoked existing ASTIS references catalogued',relation='same',evidence='Exact recursive comparison shows only the four specified list appends; all statements/formulae/Lean BODY/private aliases unchanged') for k in ['objects','domains','quantifiers','assumptions','conclusion','scopes']};slots['constant_dependencies']=dict(original='Actual BODY already invokes L2Expectation.one and inner_one_eq_integral',reconstructed='Same existing dependencies now explicitly listed in four metadata fields',relation='explicit-elaboration',evidence='one defines the constant-one real L2 class; inner_one_eq_integral is the existing integral pairing theorem. Metadata adds neither source hypothesis nor new mathematical producer; private statement definitions remain uncredited aliases.')
verdict=dict(schema='source66-separate-exact-metadata-overlay-verdict-v1',status='ACCEPTED_EXACT_METADATA_ONLY',reviewer='/root/independent_source64',independent_from_overlay_author=True,proposal_RAW_pin=pin(P),proposal_logical_sha256=C(proposal),proposed_files=entries,exact_changes=changes,seven_semantic_slots=slots,deltas=[],repairs=[],source_mathematical_repair=False,new_proof_or_Lean_change=False,new_source_hypothesis=False,formula_changes=0,TeX_false_positive_retracted='TeX-false-positive-correction.json',full_Exposition=False,PURIFIED=False,approved_for_root_application_only=True,final_source_verdict_pending_fresh_packet=True,actual_review_pid=os.getpid(),reviewed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
put('metadata-overlay.verdict.json',verdict);print(json.dumps(dict(status=verdict['status'],proposal_RAW_sha256=verdict['proposal_RAW_pin']['RAW_sha256'],verdict_RAW_sha256=H((O/'metadata-overlay.verdict.json').read_bytes()),all_four_changes_exact=True,proposed_RAW_pins=[x['proposed_snapshot']['RAW_sha256'] for x in entries]),sort_keys=True))