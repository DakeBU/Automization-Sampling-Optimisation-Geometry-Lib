from pathlib import Path
import json,hashlib,os,sys,copy
from types import SimpleNamespace
from datetime import datetime,timezone
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'tools'))
import astis_publication as pub
import astis_semantic_roundtrip as rt
def sha(b):return hashlib.sha256(b).hexdigest()
def can(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(b.replace(b'\r\n',b'\n')),'LF_sha256':sha(b.replace(b'\r\n',b'\n'))}
def load(n):return json.loads((O/n).read_bytes())
def check(z,override=None):
 p=Path(override or z['path']);p=p if p.is_absolute() else R/p;b=p.read_bytes();assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==z['LF_sha256'];return b
def write(n,x):
 p=O/n;assert not p.exists();p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
assert O.relative_to(R).as_posix()=='runs/20261007-companion-priority/pbps-actual-bounce-rate74/independent-source74'
assert not (O/'lease.final.json').exists()
run=load('source.0.run.json');logical=sha(can({k:v for k,v in run.items() if k!='run_sha256'}));assert logical==run['run_sha256']
check(run['input_manifest']);check(run['coverage']);check(run['review'])
inputs=load('source.0.input-manifest.json');decision=load('source.0.decision.json');admission=load('source.0.admission-fields.json');coverage=load('source.0.coverage.json')
assert inputs['current_input_count']==8 and inputs['source_contract_input_count']==18 and inputs['historical_version_count']==7 and inputs['repair_authority_count']==9
for group in ['final_current_inputs','immutable_source_contract_inputs','protocol_and_freeze_inputs','repair_authority_inputs']:
 for z in inputs[group]:check(z)
check(inputs['primary_reference'])
for z in inputs['final_current_inputs']+inputs['historical_versions']:
 old=check(z,O/z['RAW_snapshot']);assert (O/z['LF_snapshot']).read_bytes()==old.replace(b'\r\n',b'\n')
 if z in inputs['historical_versions']:
  check(z['final_current'])
  if z['version_relation']=='unchanged':assert old==(R/z['path']).read_bytes()
  else:
   assert z['version_relation']=='approved_exact_metadata_only_replacement';m=z['approved_mapping'];assert sha(old)==m['before']['RAW_sha256'] and pin(R/z['path'])==m['after'];check(m['authority'])
assert coverage['counts']==dict(module_lines=211,source_regions=15,source_blocks=53,source_items=95,NODE=38,EXCLUDED=57,source_nodes=28,source_edges=52,internal_bridges_produced=13,source_callers=6,conclusions=10,lesson_steps=7)
assert coverage['unclassified']==0 and coverage['all_source_classifications_unchanged'] and coverage['local_source_math_exposition_accepted']
assert len(coverage['95_source_item_projection'])==95 and len(coverage['211_line_classification'])==211
assert all('pending' not in z['source_review_status'].lower() for z in coverage['7_BODY_formula_checks'])
assert all('preparation_finding' not in z for z in coverage['26_obligations'])
assert decision['verdict']=='equivalent-after-elaboration' and decision['review_run_sha256']==logical and decision['blocking_semantic_deltas']==0 and not decision['repairs']
assert set(decision['semantic_slots'])==set(rt.SEMANTIC_SLOTS) and len(decision['deltas'])==13 and all(z['severity']=='informational' for z in decision['deltas'])
payload=load('complete-named-review-decision-input-payload.json');assert payload['whole_logical_run_sha256']==logical and payload['named_payload_count']==len(payload['named_payloads'])==5
for z in payload['named_payloads']:assert check(z['pin'])==z['complete_RAW_UTF8'].encode('utf-8')
rr=R/'runs/20261007-companion-priority/pbps-actual-bounce-rate74'
packet=json.loads((rr/'source-review.packet.json').read_bytes())
auditpath=R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualBounceRate.json';audit=json.loads(auditpath.read_bytes());accepted=copy.deepcopy(audit);accepted.update(admission['audit_fields'])
assert rt.semantic_reviewer_packet(audit)==rt.semantic_reviewer_packet(accepted)==packet
assert packet['packet_sha256']==admission['official_packet_sha256']==decision['reviewer_packet_sha256']
assert sha((rr/'source-review.packet.json').read_bytes())==admission['official_packet_RAW_sha256']
reg=rt.load_registry();reg['audits']=[accepted if z['id']==accepted['id'] else z for z in reg['audits']];errors=rt.validate_registry(reg);assert not errors,errors
item=json.loads((R/'website/content/publications/pbps-actual-bounce-rate.json').read_bytes())['items'][0]
lesson=json.loads((R/'website/content/declaration_lessons/pbps-actual-bounce-rate.json').read_bytes())['units'][0];name=packet['lean']['declaration']
data={'declarations':{name:SimpleNamespace(source_file='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBounceRate.lean')},'lessons':{name:lesson}}
oldcontext=pub.review_context(item,item['bindings'][0],data);newitem=copy.deepcopy(item);newitem['source_proof_coverage']=admission['publication_source_proof_coverage']
assert pub.binding_digest(newitem,newitem['bindings'][0],data)==pub.binding_digest(item,item['bindings'][0],data)==admission['publication_binding_sha256']
assert pub.review_context(newitem,newitem['bindings'][0],data)==oldcontext==packet['candidate_publication_context']
expanded=(rr/'expanded74.frozen.header.lean').read_bytes();assert expanded==b'theorem actual_bounce_rate_energy_laws'+packet['lean']['statement'].encode('utf-8')+b'\n'
summary='''Accepted bounded SOURCE74 implementation and local exposition: equivalent-after-elaboration,7 independently authored semantic slots,13 informational deltas,0 blocker/0 mathematical repair. Complete211-line ActualBounceRate.lean, six original callers, six actual definitions, ten conclusions and seven exact BODY/formula steps are covered. The unchanged primary-first95item/15region53block/21formula/28node52edge source contract and26 obligations are reused;13 internal bridges are accounted for, including canonical QuadReg r=0 beta-Lipschitz production, zero-safe reflection and Borel total division. Source inputs/hypotheses, local definitions and internal proof ingredients stay distinct.

R0 is identity; S is jointly Borel, not asserted continuous at zero normal; rate is continuous/Borel and has exact positive-part/sign identities. H is the SAME centered weighted SUM. The last cap has exact sqrteta,beta,2 factors on the SAME deterministic energy equality layer and includes zero energy/rank0/alphaeta1. It does not produce a recursive stochastic path or its initial-energy conservation.73 remains a sibling with no formal74 import.

Official packet canonical649b468a636925f4644cda84268990c868a37fe1e036bace641594318034a30e / RAW61dbfd843c68bdf06367342a3d3a09a0c0464be1c662a0977d6606cf0b4781b3 and publication binding599d4550f863962f6ef74dd0821ef433ebe7c8f5ead8d907d8a5f409fb0feeca are exactly preserved before/after proposed portable audit and coverage admission. In-memory registry validation passes.8 frozen current inputs,7 historical versions(5unchanged,2independently approved metadata replacements),18 immutable source-contract pins,10 protocol/freeze inputs and9 repair-authority pins are separated. Two dead_code_audit strings were independently approved by exact_science63 CLOSED25 and applied by root32304; source reviewer did not self-approve/apply them.

All original preparation bytes and native provisional state-completion mappings are retained. One observer failure54236 EXIT1 incorrectly compared a named expanded-header file to a bare packet statement; corrected42264 EXIT0 proves the exact theorem-name + statement + LF wrapper. Premature stdout EXIT0 is explicitly rejected as terminal evidence. This was no mathematical/source/candidate repair. Final review construction30404 EXIT0 and native status completion34140 EXIT0 are separately recorded. No fresh Lean/site/browser/graph checks, other math verdict reliance, canonical/Git/globalledger or old CLOSED writes. Exact SCI/VERIFIED, serialized aggregate/current runtime reader, full Exposition/PURIFIED/main/live/wholepaper/Goal remain unaccepted. Clocks/hazards/random path/nonexplosion/Markov/invariance/terminal H_y/K/r_rho/B27/B28 and main/errors/expected-query costs remain open.
'''
(O/'bounded-synthesis.final74.md').write_text(summary,encoding='utf-8',newline='\n')
write('terminal.close-source74.receipt.json',{'actual_PID':os.getpid(),'exit_code':0,'argv':sys.argv,'whole_logical_run_sha256':logical,'input_counts':{'current':8,'historical':7,'immutable_source':18,'protocol_and_freeze':10,'repair_authority':9},'named_RAW_payloads_verified':5,'all_current_pins_and_approved_historical_mappings_verified':True,'registry_errors':0,'packet_binding_context_unchanged_by_admission':True,'negative54236_EXIT1_and_corrected42264_EXIT0_retained':True,'canonical_Git_ledger_or_old_CLOSED_written':False,'VERIFIED_or_full_paper_credit':False})
members=sorted(p for p in O.rglob('*') if p.is_file() and p.name not in ['whole-owned.manifest.json','lease.final.json'])
manifest={'scope':O.relative_to(R).as_posix(),'count':len(members),'files':[pin(p) for p in members],'LF_recipe':'CRLF pairs -> LF only; preserve bare CR and every other byte','complete_owned_files_except_manifest_and_last_lease':True}
write('whole-owned.manifest.json',manifest)
all_except=sorted(members+[O/'whole-owned.manifest.json'])
lease={'status':'CLOSED_LAST','exit_code':0,'actual_last_writer_PID':os.getpid(),'closed_utc':datetime.now(timezone.utc).isoformat(),'owned_file_count_including_self':len(all_except)+1,'all_files_except_self':[pin(p) for p in all_except],'whole_owned_manifest':pin(O/'whole-owned.manifest.json'),'whole_logical_run_sha256':logical,'native_run':pin(O/'source.0.run.json'),'complete_named_RAW_payload':pin(O/'complete-named-review-decision-input-payload.json'),'canonical_Git_ledger_or_old_CLOSED_written':False,'VERIFIED_or_full_paper_credit':False,'last_owned_write':'lease.final.json','postclose_policy':'Read-only external verification only; zero owned writes after this last lease.','source_verdict':'equivalent-after-elaboration','mathematical_repairs':[],'approved_metadata_repairs_are_distinct_authority_only':True,'input_counts':{'current':8,'historical':7,'immutable_source':18,'protocol_and_freeze':10,'repair_authority':9}}
write('lease.final.json',lease)
print(json.dumps({'actual_close_PID':os.getpid(),'EXIT':0,'CLOSED_owned_files':len(all_except)+1,'whole_logical_run_sha256':logical,'run_RAW':pin(O/'source.0.run.json'),'decision_RAW':pin(O/'source.0.decision.json'),'admission_RAW':pin(O/'source.0.admission-fields.json'),'named_payload_RAW':pin(O/'complete-named-review-decision-input-payload.json'),'lease_RAW':pin(O/'lease.final.json'),'whole_manifest_RAW':pin(O/'whole-owned.manifest.json')},ensure_ascii=True))
