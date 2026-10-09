from pathlib import Path
import hashlib,json,os,sys
sys.path.insert(0,str(Path.cwd()/'tools'))
import astis_publication as pub
import astis_semantic_roundtrip as rt
r=Path('runs/20261007-companion-priority/pbps-actual-harmonic-flow73');o=r/'frontier-label-overlay73';o.mkdir(exist_ok=False)
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
p=Path('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-harmonic-flow.json');before=p.read_bytes();cell=load(p)
old='Exact source-first finite retrieval: runs/20261007-companion-priority/pbps-half-turn-construction-preread73/api.retrieval.json'
new='Samplinglib exact source-first finite retrieval: runs/20261007-companion-priority/pbps-half-turn-construction-preread73/api.retrieval.json'
assert cell['shared_floor_audit']['searched'][0]==cell['reuse_plan']['searched_existing'][0]==old
assert before.count(json.dumps(old).encode())==2;after=before.replace(json.dumps(old).encode(),json.dumps(new).encode());proposed=json.loads(after)
retrieval=load('runs/20261007-companion-priority/pbps-half-turn-construction-preread73/api.retrieval.json');assert any('AutoSamplingTheory/TechnicalLemmas' in q['command'] for q in retrieval['queries'])
assert 'samplinglib' in ' '.join(proposed['shared_floor_audit']['searched']).lower() and 'mathlib' in ' '.join(proposed['shared_floor_audit']['searched']).lower()
(o/'cell.before.exactraw.json').write_bytes(before);(o/'cell.proposed.exactraw.json').write_bytes(after)
item=next(x for x in pub.load() if x['id']=='pbps-actual-harmonic-flow');binding=pub.binding_digest(item,item['bindings'][0],pub.inputs());context=pub.review_context(item,item['bindings'][0],pub.inputs())
audit=load('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualHarmonicFlow.json');packet=load(r/'source-review.packet.json');assert rt.semantic_reviewer_packet(audit)==packet
proposal=dict(schema='astis-independent-frontier-search-label-overlay73/v1',status='PROPOSED_AWAITING_DISTINCT_REPAIR_REVIEW_AND_FAILED_SCI_CLOSURE',proposer='/root',actual_root_PID=os.getpid(),canonical_path=p.as_posix(),before=pin(o/'cell.before.exactraw.json'),after=pin(o/'cell.proposed.exactraw.json'),current=pin(p),changes=[dict(JSON_pointer=ptr,before=old,after=new) for ptr in ['/shared_floor_audit/searched/0','/reuse_plan/searched_existing/0']],existing_search_evidence=pin('runs/20261007-companion-priority/pbps-half-turn-construction-preread73/api.retrieval.json'),binding_sha256=binding,context_sha256=sha(can(context)),source_packet_sha256=packet['packet_sha256'],unchanged=[pin(q) for q in ['AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean','website/content/publications/pbps-actual-harmonic-flow.json','website/content/declaration_lessons/pbps-actual-harmonic-flow.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualHarmonicFlow.json',r/'source-review.packet.json']],no_source_or_mathematical_repair=True,canonical_writes=False,VERIFIED=False,Goal_complete=False)
(o/'proposal.json').write_text(json.dumps(proposal,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps(dict(status='PROPOSED_EXACT_TWO_SEARCH_LABELS_ONLY',proposal=pin(o/'proposal.json'),before=proposal['before'],after=proposal['after'],canonical_unchanged=True)))
