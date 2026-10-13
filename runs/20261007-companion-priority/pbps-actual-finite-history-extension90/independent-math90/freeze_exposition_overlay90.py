from pathlib import Path
import datetime,hashlib,json
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent
def pin(p):
 p=Path(p);b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def put(n,v):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
def copy(src,n):
 q=O/n
 with q.open('xb') as f:f.write(src.read_bytes())
 return q
L=R/'website/content/declaration_lessons/pbps-actual-finite-history-extension.json'
P=R/'website/content/publications/pbps-actual-finite-history-extension.json'
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryExtension.lean'
S=B/'root.statement-seal90.json';F=B/'publication-freeze90.json'
assert pin(L)['raw_sha256']=='3f65dd2d096a9441d20ed6f47002ca4b0572cbb56ee9dd2157de02b285314b75'
assert pin(P)['raw_sha256']=='627a7fbf941b24201511026b7b021be27e64ca2c16b4d481923ed4cd74f864e0'
assert pin(M)['raw_sha256']=='6cdc14328be5ec3ece3f028e6e1dd0185ee4031a8e651956ee0f55d4beebf029'
ls=copy(L,'lesson90.original.exactraw.json');ps=copy(P,'publication90.original.exactraw.json');fs=copy(F,'publication-freeze90.original.exactraw.json')
seal=copy(S,'statement-seal90.original.exactraw.json')
lj=json.loads(ls.read_text('utf8'));pj=json.loads(ps.read_text('utf8'))
old=lj['units'][0]['steps'][0]['formula'];assert old==pj['items'][0]['formulae'][0]['tex']
new=old.replace(r'\operatorname{live}(T+s,',r'\operatorname{live}(T+\max\{s,0\},').replace(r',\ s>0,',',')
assert new!=old and 's>0' not in new and r'\max\{s,0\}' in new
def candidate(src,n):
 oldb=json.dumps(old,ensure_ascii=False).encode('utf8');newb=json.dumps(new,ensure_ascii=False).encode('utf8')
 b=src.read_bytes();assert b.count(oldb)==1
 q=O/n
 with q.open('xb') as f:f.write(b.replace(oldb,newb,1))
 return q
lc=candidate(ls,'lesson90.proposed-total-append-formula.exactraw.json');pc=candidate(ps,'publication90.proposed-total-append-formula.exactraw.json')
lj['units'][0]['steps'][0]['formula']=new;pj['items'][0]['formulae'][0]['tex']=new
assert lj==json.loads(lc.read_text('utf8')) and pj==json.loads(pc.read_text('utf8'))
snapshots=[{'original':pin(a),'closed_snapshot':pin(b)} for a,b in [(L,ls),(P,ps),(F,fs),(S,seal)]]
put('original-exposition-snapshot-index90.json',{'snapshots':snapshots,'historical_original_paths_may_later_change_only_after_distinct_repair_acceptance':True,'authoritative_historical_bytes_are_snapshots':True,'module_original_snapshot':pin(O/'module90.exactraw.lean')})
changes=[{'target':pin(L),'pointer':'/units/0/steps/0/formula','before':old,'after':new,'proposed':pin(lc)}, {'target':pin(P),'pointer':'/items/0/formulae/0/tex','before':old,'after':new,'proposed':pin(pc)}]
put('proposed-exposition-overlay90.json',{
 'kind':'EXACT_TWO_FIELD_EXPOSITION_DEFINITION_COMPLETENESS_PROPOSAL_NOT_APPLIED',
 'proposer_id':'/root/exact_verify77','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'changes':changes,
 'rationale':'Displayed append is defined for all abstract histories and real times in the statement/Lean. Original formula gives live branch only for s>0, leaving live s<=0 unspecified even though the following proof establishes Borel total append. Show exact live cumulative increment max{s,0} and remove the s>0 side condition. Raw-real Phi_s and stopped branch stay unchanged. This matches existing definition, no theorem or source mathematics change.',
 'semantic_delta_only_two_fields':True,'canonical_files_not_changed':True,'distinct_review_required':True,
 'unchanged':[pin(M),pin(S)],'original_snapshots':snapshots,
 'no_statement_BODY_or_anonymous_decoder_packet_change':True})
put('exposition-repair-review-packet90.json',{
 'kind':'CLEAN_EXACT_TWO_FIELD_EXPOSITION_REPAIR_REVIEW_REQUEST',
 'primary':pin(R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'),
 'primary_url':'https://arxiv.org/html/2609.06905v1#A1.E2',
 'original_module':pin(O/'module90.exactraw.lean'),'statement_seal':pin(seal),
 'original_lesson':pin(ls),'original_publication':pin(ps),'original_publication_freeze':pin(fs),
 'proposal':pin(O/'proposed-exposition-overlay90.json'),'candidates':[pin(lc),pin(pc)],
 'pointers':[x['pointer'] for x in changes],
 'review_question':'Independently check original formula versus exact literal append and source finite-update convention. Does displaying T+max{s,0} for every live h_n and removing s>0 solely restore the already specified total definition, while keeping real Phi_s and stopped branch? Check exactly two fields changed, every other decoded/raw byte unchanged, no statement/proof/public-provider or source-scope modification.',
 'earlier_acceptance_or_final_source_blind_verdicts_included':False,
 'candidate_not_applied':True,'reviewer_must_be_distinct_from_proposer_and_formalizer':True})
inps=[L,P,M,S,F];outs=[ls,ps,fs,seal,lc,pc,O/'original-exposition-snapshot-index90.json',O/'proposed-exposition-overlay90.json',O/'exposition-repair-review-packet90.json',Path(__file__)]
put('exposition-overlay90.closed-RAW-manifest.json',{'kind':'CLOSED_NONCIRCULAR_EXACT_PROPOSAL_ONLY','proposer_id':'/root/exact_verify77','inputs':[pin(p) for p in inps],'outputs':[pin(p) for p in outs],'snapshot_resolution':pin(O/'original-exposition-snapshot-index90.json'),'self_hash_intentionally_omitted':True,'no_acceptance_or_canonical_application':True})
print(json.dumps({'proposal':pin(O/'proposed-exposition-overlay90.json'),'packet':pin(O/'exposition-repair-review-packet90.json'),'manifest':pin(O/'exposition-overlay90.closed-RAW-manifest.json'),'candidates':[pin(lc),pin(pc)]},indent=2))
