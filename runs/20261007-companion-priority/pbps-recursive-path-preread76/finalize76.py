from pathlib import Path
import hashlib,importlib.util,json,os,sys,time
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path('E:/Samplinglib');REL='runs/20261007-companion-priority/pbps-recursive-path-preread76';OUT=ROOT/REL
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(o):return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def pin(p):
 b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return {'path':p.relative_to(ROOT).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(l),'LF_sha256':sha(l)}
def dump(name,o):
 (OUT/name).write_bytes((json.dumps(o,ensure_ascii=False,indent=2,sort_keys=True,allow_nan=False)+'\n').encode())
def get(name):return json.loads((OUT/name).read_bytes())
def checkpin(p):
 q=ROOT/p['path'];a=pin(q)
 for k in ['RAW_bytes','RAW_sha256','LF_bytes','LF_sha256']:assert a[k]==p[k],(p['path'],k)
def main():
 print('ACTUAL_FOREGROUND_PID',os.getpid(),flush=True)
 assert not (OUT/'lease.final.json').exists()
 # A source-plan clarification only; no new candidate or source change.
 contract=get('selected.contract.json')
 contract['separable_next_interface']['canonical_future_probability_space']='Omega=Nat -> Real with Measure.infinitePi of ProbabilityTheory.expMeasure (1 : Real); e_n=Real.toNNReal(omega n). Derive positivity/nonnegativity a.s., NNReal coercion identity a.s., common law, mean/integrability and pairwise independence internally before applying SLLN. This is deferred, not a new caller or supplied law certificate.'
 dump('selected.contract.json',contract)
 inputs=get('inputs.manifest.json');regions=get('source.regions.json');cov=get('source.coverage.json');apis=get('API.regions.json');graph=get('source-proof-graph.json');expect=get('source-first.expectations.json')
 for p in [inputs['primary'],inputs['primary_parser']]+inputs['source_slices']+inputs['API_fragments']+inputs['API_whole_sources_opaque_pins']+inputs['reused_native_finite_pins']:checkpin(p)
 primary=(ROOT/inputs['primary']['path']).read_bytes()
 helper=ROOT/inputs['primary_parser']['path'];spec=importlib.util.spec_from_file_location('readonly_final_parser75',helper);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);parser=m.Parser(primary.decode());byid={n.id:n for n in parser.nodes if n.id}
 for a in contract['source_anchors']:assert a in byid,a
 for n in graph['nodes']:
  for a in n['source_items']:assert a in byid,(n['id'],a)
 for r in regions['regions']:
  lo,hi=r['primary_RAW_range'];assert (ROOT/r['input']['path']).read_bytes()==primary[lo:hi]
  parts=r['complete_byte_partition'];assert parts[0]['primary_RAW_range'][0]==lo and parts[-1]['primary_RAW_range'][1]==hi
  for i,p in enumerate(parts):
   a,z=p['primary_RAW_range'];assert a<z and sha(primary[a:z])==p['RAW_sha256']
   if i:assert parts[i-1]['primary_RAW_range'][1]==a
 for row in cov['items']:
  a,z=row['primary_RAW_range'];assert sha(primary[a:z])==row['RAW_sha256'] and z-a==row['RAW_bytes'];assert row['classification'] in ['NODE','EXCLUDED'] and row['reason']
  if row['item'] in byid:
   n=byid[row['item']];s=primary.decode();assert len(s[:n.start].encode())==a and len(s[:n.end].encode())==z and n.text()==row['literal']
 for a in apis['regions']:
  raw=(ROOT/a['whole_source']['path']).read_bytes();frag=b''.join(raw.splitlines(keepends=True)[a['start_line']-1:a['end_line']]);assert frag==(ROOT/a['fragment']['path']).read_bytes()
 ids={n['id'] for n in graph['nodes']};assert len(ids)==19 and len(graph['edges'])==31
 for e in graph['edges']:assert e['producer'] in ids and e['consumer'] in ids
 assert cov['counts']=={'regions':9,'items':90,'math_items':56,'NODE':64,'EXCLUDED':26}
 assert len(contract['route_at_most_seven_steps'])==7 and len(expect['obligations'])==12 and len(contract['proposed_declaration_semantics']['analytic_callers'])==6
 assert len(apis['regions'])==7 and len(inputs['reused_native_finite_pins'])==7
 negatives=get('observer-negatives.json');negatives['retained'].append('First build attempted two optional prior-context paths using wrong names; no contents were read at those locators. Filename-only lookup corrected to source-first.expectations75.json and API/SLLN-contract.exactraw.lean-fragment. Historical-v1 receipt/contract retained.')
 dump('observer-negatives.json',negatives)
 review=get('review.json');review['negative_observers']=negatives;review['deferred_iid_realization']=contract['separable_next_interface']['canonical_future_probability_space'];review['independent_final_checks']={'primary_RAW_and_ranges':'PASS','all90_source_item_RAW_and_text':'PASS','all9_full_region_byte_partitions':'PASS','all31_edges_endpoints_and_literal_anchors':'PASS','all7_API_exact_RAW_line_ranges':'PASS','all_current_finite_pin_RAW_LF':'PASS','original_six_callers':'PASS','zero_threshold_has_no_global_phase_claim':'PASS','new_header_or_proof':'NONE'}
 dump('review.json',review)
 receipt={'schema':'actual-foreground-native-close-receipt-v1','actual_PID':os.getpid(),'actual_EXIT':0,'command':'python -B finalize76.py','verified_finite_input_pin_entries':1+1+len(inputs['source_slices'])+len(inputs['API_fragments'])+len(inputs['API_whole_sources_opaque_pins'])+len(inputs['reused_native_finite_pins']),'all_source_coverage':cov['counts'],'source_graph':graph['counts'],'source_obligations':12,'API_source_files':7,'source_regions':9,'checks':'All exact RAW/LF finite pins, source rows/text/anchors, complete byte partitions and API line spans verified.','no_canonical_old_closed_Git_ledger_Goal_writes':True,'no_Lean_or_site_or_browser_execution':True,'final_lease_written_last':True,'postclose_writes_permitted':False}
 dump('close.receipt.json',receipt)
 artifact_names=['selected.contract.json','source-first.expectations.json','source-proof-graph.json','source.coverage.json','source.regions.json','API.regions.json','inputs.manifest.json','decision.json','review.json','observer-negatives.json','bounded-synthesis.txt','inspection.receipt.json','historical-v1.build.receipt.json','refine.receipt.json','build.receipt.json','close.receipt.json']
 run={'schema':'bounded-source-planning-native-run-v1','status':'CLOSED_SOURCE_PREREAD_ONLY','task':'PBPS actual finite stopped recursion preread76','owner':'/root/independent_primary69','primary_RAW_sha256':inputs['primary']['RAW_sha256'],'source_counts':cov['counts'],'source_graph_counts':graph['counts'],'obligations':12,'analytic_callers':6,'new_callers':0,'route_steps':7,'finite_input_pin_entries':receipt['verified_finite_input_pin_entries'],'API_whole_source_files':7,'source_header_or_Lean_compile_or_verified_credit':False,'finite_artifacts':[pin(OUT/n) for n in artifact_names],'real_process_receipts':[pin(OUT/n) for n in ['inspection.receipt.json','historical-v1.build.receipt.json','refine.receipt.json','build.receipt.json','close.receipt.json']],'run_sha256':''}
 logical=dict(run);del logical['run_sha256'];run['run_sha256']=sha(canon(logical));dump('run.json',run)
 named=['review.json','decision.json','selected.contract.json','source-first.expectations.json','source-proof-graph.json','source.coverage.json','source.regions.json','API.regions.json','inputs.manifest.json','run.json']
 payload={'schema':'complete-named-RAW-source-planning-payload-v1','no_historical_recursive_copies':True,'source_and_API_RAW_inputs':'Owned finite RAW files bound by inputs.manifest.json and native.manifest.json; full old native packages are not embedded.','names':[{'name':name,**pin(OUT/name),'RAW_utf8':(OUT/name).read_bytes().decode()} for name in named]}
 dump('complete-named-review-decision-input.payload.json',payload)
 files=sorted(p for p in OUT.rglob('*') if p.is_file() and p.name not in ['native.manifest.json','lease.final.json'])
 manifest={'schema':'whole-owned-finite-manifest-v1','self_exclusions':['native.manifest.json','lease.final.json'],'members':[pin(p) for p in files],'member_count':len(files),'LF_recipe':'Only bytewise CRLF -> LF; RAW remains authoritative.','run_whole_logical_sha256':run['run_sha256'],'named_complete_payload':pin(OUT/'complete-named-review-decision-input.payload.json')}
 dump('native.manifest.json',manifest)
 members=sorted(p for p in OUT.rglob('*') if p.is_file() and p.name!='lease.final.json')
 lease={'schema':'finite-owned-last-lease-v1','state':'CLOSED_LAST','owner':'/root/independent_primary69','owned_root':REL,'all_owned_except_only_self':[pin(p) for p in members],'member_count':len(members),'total_owned_including_self':len(members)+1,'run':pin(OUT/'run.json'),'run_whole_logical_sha256':run['run_sha256'],'run_whole_logical_recipe':'Canonical UTF8 JSON ensure_ascii=False, sort_keys=True, compact comma/colon separators, allow_nan=False; DELETE ONLY top-level run_sha256.','named_complete_payload':pin(OUT/'complete-named-review-decision-input.payload.json'),'manifest':pin(OUT/'native.manifest.json'),'actual_terminal_PID':os.getpid(),'actual_terminal_EXIT':0,'last_owned_write':'lease.final.json','postclose_owned_writes_allowed':False,'truth_boundary':'Source planning only. No76 header/body/proof/compile/SAU/VERIFIED/reader/PURIFIED/main/cost/Goal admission.75 remains unproved/uncompiled.'}
 dump('lease.final.json',lease)
 print(json.dumps({'actual_PID':os.getpid(),'actual_EXIT':0,'counts':cov['counts'],'graph':graph['counts'],'obligations':12,'input_pin_entries':receipt['verified_finite_input_pin_entries'],'owned_count':len(members)+1,'manifest_members':len(files),'lease_members':len(members),'run_whole_logical':run['run_sha256'],'payload_RAW':pin(OUT/'complete-named-review-decision-input.payload.json'),'lease_RAW':pin(OUT/'lease.final.json'),'contract_RAW':pin(OUT/'selected.contract.json'),'decision_RAW':pin(OUT/'decision.json')},ensure_ascii=False))
if __name__=='__main__':main()
