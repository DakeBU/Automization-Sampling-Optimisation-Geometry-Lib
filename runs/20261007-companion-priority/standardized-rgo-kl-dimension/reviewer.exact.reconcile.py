from pathlib import Path
import json,hashlib,datetime,subprocess
r=Path(r'E:/Samplinglib');run=r/'runs/20261007-companion-priority/standardized-rgo-kl-dimension';prefix=run.relative_to(r).as_posix();sha=lambda b:hashlib.sha256(b).hexdigest();lf=lambda b:b.replace(b'\r\n',b'\n').replace(b'\r',b'\n');load=lambda p:json.loads((r/p).read_text(encoding='utf-8-sig'))
def bind(p):
 b=(r/p).read_bytes();return {'path':p,'raw_sha256':sha(b),'lf_sha256':sha(lf(b)),'bytes':len(b)}
def diff(a,b,p=''):
 if a==b:return []
 if isinstance(a,dict) and isinstance(b,dict):
  out=[]
  for k in sorted(set(a)|set(b)):out+=diff(a.get(k),b.get(k),p+'/'+k)
  return out
 return [p]
audit='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261007-StandardizedRGOKLDimension.json';cell='research-wiki/frontier-cells/ASTIS-SW-SPHMC-standardized-rgo-kl-dimension.json';ad=diff(load(prefix+'/source-admission-before.0.raw.snapshot.audit.json'),load(audit));cd=diff(load(prefix+'/source-admission-before.0.raw.snapshot.cell.json'),load(cell));print('ADMINAUDIT',ad,'ADMINCELL',cd)
assert all(x.startswith(('/source_review','/semantic_slots','/deltas','/state','/verdict')) for x in ad);assert all(x.startswith(('/status','/evidence')) for x in cd)
for k in ['source','lean','reconstruction','publication_binding_sha256','publication_context']:assert load(prefix+'/source-admission-before.0.raw.snapshot.audit.json')[k]==load(audit)[k],k
# Dictionary-schema decoder pins, including original lease initial-read projection.
ar=load(prefix+'/anonymous-decoder/run.json');extra=[]
for section in ['input_artifacts']:
 for name,item in ar['execution_payload'][section].items():
  fn='initial-lease.raw.snapshot.json' if name=='lease.json_initial_read' else name;path=prefix+'/anonymous-decoder/'+fn;actual=bind(path)
  assert all(actual[k]==v for k,v in item.items()),(name,item,actual);extra.append({'original_dict_key':name,'actual':actual,'status':'PASS'})
for name,item in ar['output_artifacts'].items():
 actual=bind(prefix+'/anonymous-decoder/'+name);assert all(actual[k]==v for k,v in item.items());extra.append({'original_dict_key':name,'actual':actual,'status':'PASS'})
assert (r/'.astis/decoder-45/packet0.json').read_bytes()==(run/'anonymous-decoder/packet0.json').read_bytes()
assert bind(prefix+'/anonymous-decoder/run.json')['raw_sha256']=='3a177bb2690ccda0cacbe8dc94396dc169b86f7aa62fcfb01442a8197428e527'
assert bind(prefix+'/source.0.review.json')['raw_sha256']=='367df02d099129d2298abf19164885e185e7a60661881c2a6d2f8d5f5fa56108'
leasepaths=['compiler.lease.json','whole-proof-review45/reviewer.math.lease.json','anonymous-decoder/lease.json','source.review.lease.json','source.review.primary-first.lease.json'];leases=[]
for p in leasepaths:
 j=load(prefix+'/'+p);assert j['status']=='CLOSED'
 fields={k:v for k,v in j.items() if isinstance(v,(str,bool,int)) and ('lease' in k.lower() or k in ['status','read','write','Python','compiler','compiler_started','opened_utc','closed_utc','compiler_terminal_utc','python_lease_closed_utc'])};assert not any(v=='OPEN' for v in fields.values());leases.append({'path':prefix+'/'+p,'binding':bind(prefix+'/'+p),'fields':fields})
primary=load(prefix+'/source.review.primary-first.lease.json');math=load(prefix+'/whole-proof-review45/reviewer.math.lease.json');anonymous=load(prefix+'/anonymous-decoder/lease.json');source=load(prefix+'/source.review.lease.json');exact=load(prefix+'/reviewer.exact.lease.open.raw.snapshot.json')
chronology=[('ownsourceprimaryclosed',primary['closed_utc']),('rootcompilerclosed',load(prefix+'/compiler.lease.json')['closed_utc']),('wholemathleaseopened',math['opened_utc']),('decoderinstrumentedreceiptfinal',anonymous['python_lease_closed_utc']),('wholemathcompilerterminal',math['compiler_terminal_utc']),('wholemathreviewclosed',math['closed_utc']),('sourcefidelityclosed',source['closed_utc']),('actualproofcommit',subprocess.check_output(['git','show','-s','--format=%cI','76373366787499ebbc9e778fe568d0332233aef0'],cwd=r).decode().strip()),('exactverifieropened',exact['opened_utc'])];times=[datetime.datetime.fromisoformat(x[1].replace('Z','+00:00')) for x in chronology];assert times==sorted(times)
j={'checked_commit':'76373366787499ebbc9e778fe568d0332233aef0','historical_admin_resolution':{'audit_before':bind(prefix+'/source-admission-before.0.raw.snapshot.audit.json'),'audit_current':bind(audit),'audit_changed_paths':ad,'cell_before':bind(prefix+'/source-admission-before.0.raw.snapshot.cell.json'),'cell_current':bind(cell),'cell_changed_paths':cd,'source_Lean_reconstruction_publication_context_unchanged':True,'scope':'Source acceptance and PROVED_LOCAL administration after closedsource45review; everyhistoricalpinresolvedstrictlyagainstactualbefore snapshot, no source or proof repair.'},'decoder_original_dictionary_schema':{'extra_dict_bindings':extra,'portable_run_raw_sha256':bind(prefix+'/anonymous-decoder/run.json')['raw_sha256'],'ignored_neutral_packet_equals_committed_portable':True,'original_schema_preserved':True,'blind_scope':'Packet-only proposition/approved context; inherited generic project instructions disclosed. Exact initial uninstrumented read time unavailable and not invented. No task-specific source/proof/review/repair read.'},'leases':leases,'chronology':[{'stage':a,'utc':b} for a,b in chronology],'chronology_monotone':True,'previous43':'Root9149/Tests9427 and repositoryProofSeal43 at4dff antecedent965 are previous evidence only; root45shared imports/Registry/aggregate/reader/publicationseals require serialized integration after this admission.','unrelated46':'Untracked source-only46 folder excluded; no code/compile/Goal/commit credit.'};(run/'reviewer.exact.admission-reconciliation.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('DECODEREXTRA',len(extra),'LEASES',len(leases),'CHRONOLOGY',chronology)
