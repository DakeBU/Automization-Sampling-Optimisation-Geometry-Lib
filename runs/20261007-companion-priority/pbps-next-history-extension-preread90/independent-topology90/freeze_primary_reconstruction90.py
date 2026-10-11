from pathlib import Path
import datetime,hashlib,json,re
R=Path('E:/Samplinglib');O=Path(__file__).parent
P=R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'raw_sha256':sha(b),'bytes':len(b)}
def put(n,v):
 p=O/n
 with p.open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
 return pin(p)
b=P.read_bytes();assert sha(b)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
chunks=[]
for label,nextlabel in [('A1.SS1','A1.SS2'),('A1.SS2',None)]:
 token=('id="'+label+'"').encode();start=b.rfind(b'<section',0,b.index(token))
 end=b.rfind(b'<section',0,b.index(('id="'+nextlabel+'"').encode())) if nextlabel else b.index(b'</section>',start)+len(b'</section>')
 z=b[start:end];chunks.append({'anchor':label,'byte_start_zero_based':start,'byte_end_exclusive':end,'raw_span_sha256':sha(z),'exact_html':z.decode('utf8')})
private=put('.private.primary90.full-A1-A2.exact-spans.json',{'primary':pin(P),'spans':chunks,'publication_exclusion':'Long exact primary extracts remain private local; do not publish or archive publicly.'})
time=datetime.datetime.now(datetime.timezone.utc).isoformat()
chronology=put('primary-first90.chronology.json',{'recorded_utc':time,'source_read_terminal':'61f8ba','source_read_exit_code':0,'read_scope':'Complete pinned Appendix A1.SS1 and A1.SS2; explicit A1.E1,A1.E2,A1.E7','earlier_environment_negative':{'terminal':'3d31c7','exit_code':1,'cause':'Optional bs4 import unavailable before any source file was read; replaced with stdlib HTMLParser and exact raw bytes.'},'creator_graph_or_coverage_or_proposal90_read':False,'header90_or_BODY90_read':False,'source_first_reconstruction_frozen_before_creator_comparison':True,'timestamp_claim':'Record creation UTC is observed; no fabricated per-read native timestamps or agent trajectory.'})
reconstruction=put('independent-primary-math-reconstruction90.json',{
 'status':'FROZEN_PRIMARY_FIRST_INDEPENDENT_RECONSTRUCTION_BEFORE_CREATOR_GRAPH','reviewer_id':'/root/exact_verify77','recorded_utc':time,'primary':pin(P),'chronology':chronology,'exact_private_spans':private,
 'source_facts':[
  {'anchors':['A1.SS1.p1','A1.E1','A1.E2'],'fact':'At fixed y/reference, independent Exp1 thresholds drive integrated-hazard crossing. A finite crossing appends cumulative time T_n+s and post-bounce state S(Phi_s z); empty crossing stops at infinity. Zero normal uses identity reflection.'},
  {'anchors':['A1.E7','A1.SS1 surrounding proof'],'fact':'Ordered positive jump times enter the full finite-path density via iteration of independent clock factors and deterministic arc/bounce updates. A single finite-history extension is a source-implicit ingredient of this iteration, not the whole path law.'},
  {'anchors':['A1.SS2 joint-measurability proof'],'fact':'Flow/rate/reflection are jointly Borel; hazard continuous nondecreasing in time gives Borel crossings; each finite jump time/post-jump state is Borel in all deterministic parameters and clock sequence. Fixed finite-depth append therefore needs no nonexplosion assumption.'}
 ],
 'independent_dependency_reconstruction':[
  {'id':'R90-model','role':'Literal tagged stopped recursion, full history H_n of records0..n, existing six standing analytic hypotheses. Source support and ASTIS total representation must be distinguished.'},
  {'id':'R90-append','AND':['finite full-history coordinate operations','joint Borel flow and reflection','measurable live/stopped case split and selected total off-support default'],'output':'Internally derived Borel append App_n(h,s) preserving all old coordinates and adding (T_last+s,S(Phi_s state_last)) on the live, positive-finite density support. Any total fallback is a definition convention, not a source premise.'},
  {'id':'R90-guarded-equality','AND':['literal actual recursion successor','strict guard B_d:0<W_n<d(H_n)','finite crossing coercion/time observable identities'],'output':'On B_d, actual H_(n+1) equals App_n(H_n,timeObs_n) pointwise, together with same relative wait. No unconditional equality after infinite wait/default0 is asserted.'},
  {'id':'R90-density','role':'Verified89 strict finite positive history/relative-wait law for actual Exp product P, finite Borel d, all Borel history A and arbitrary joint ENNReal tests; internally consumes verified87 independence and86 first-event density. Survival88 is adjacent, not an AND prerequisite.'},
  {'id':'R90-law','AND':['R90-append joint measurability','R90-guarded-equality','R90-density exact restricted joint measure law','generic map composition/congruence/restriction'],'output':'Restricted actual next-history/relative-wait joint law is the genuine pushforward of current-history/relative-wait density measure under (h,s)->(App_n(h,s),s). Marginal law follows by first projection.'},
  {'id':'R90-tests','AND':['R90-law or existing89 full arbitrary joint-test identity','composition with Borel append','nonnegative measurable integration'],'output':'Unnormalized test identity for arbitrary jointly Borel ENNReal next-history/time tests and Borel original-history events, including null A. No new L1, bounded cutoff, positive history mass or conditional distribution provider.'}
 ],
 'alternative_routes':[
  'Sufficient route1: prove next-history/time measure pushforward via89 joint law and guarded map equality, then derive tests/marginal by integration/projection.',
  'Sufficient route2: feed the composed next-history/time test into89 arbitrary-test identity, including measurable indicators to derive the joint law. These are OR proof routes, not cumulative mathematical prerequisites.'
 ],
 'counterexample_and_boundary_audit':{
  'unconditional_append_false':'If next wait is infinite, timeObs default0 cannot reconstruct an actual stopped successor by a naive live append. Guarded identity is mandatory.',
  'abstract_stopped_history':'Stopped fibers carry zero density, so total append may choose a measurable stopped default; this convention must not become a source assumption or a nonzero conditional event.',
  'endpoints':'Strict Ioo support and B guard exclude zero wait, cutoff equality and infinity. No equality to closed Ioc mass or no-atom prerequisite is required.',
  'n0_nullA_rank0_flat':'Finite-prefix append works at n0; null events remain unnormalized; rank0/flat hazard may yield all infinite waits and zero finite density law.',
  'unbounded_d_infinite_F':'Borel NNReal cutoff is finite pointwise but may be unbounded across histories; nonnegative ENNReal tests may be infinite without extra L1.',
  'genuine_new_edge':'Actual Borel full-history extension and exact successor-recursion identification are the new bridge. An abstract supplied-measurable-append wrapper or repeating89 unchanged would not supply this edge.'},
 'required_source_dependencies_not_needed':['Survival88 conditional final-factor law','No-atom endpoint theorem','Nonexplosion/all-time process or typed phase-kernel packaging','Positive-history probability/regular conditional probability/normalizer'],
 'global_exclusions_open':['Full ordered-time density iteration and final survival/count partition/path-functional law of A7','Absolute summability/rate domination/global path reversal','Markov/CK/physical-time residual restart','Invariant law/Jensen/L2 density/semigroup/Gaussian averaging','Implementation/cost/main/composition/fullpaper/Goal'],
 'no_Lean_BODY_used_to_determine_source_topology':True,'no_header_approval_no_SAU_claim_no_VERIFIED':True,'canonical_writes':False})
manifest=put('primary-reconstruction90.closed-RAW-manifest.json',{'status':'CLOSED_BEFORE_CREATOR_GRAPH90_READ','primary_input':pin(P),'owned_artifacts':[pin(O/'freeze_primary_reconstruction90.py'),private,chronology,reconstruction],'self_hash_intentionally_omitted':True,'private_exclusions':[private['path']]})
print(json.dumps({'reconstruction':reconstruction,'chronology':chronology,'closed_manifest':manifest},indent=2))
