from pathlib import Path
import json, hashlib, datetime, re, html
ROOT=Path('E:/Samplinglib')
OUT=ROOT/'runs/20261007-companion-priority/pbps-ordered-history-iteration-preread91/independent-source-first91'
def raw(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def write(n,x):
 p=OUT/n;assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8');return raw(p)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
primary=ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
assert raw(primary)['raw_sha256']=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
b=primary.read_bytes(); lines=b.splitlines(keepends=True)
spec=[('P91-V',250,265),('P91-H',349,361),('P91-ETA',610,617),('P91-CENTER',1486,1492),('P91-A1',2859,2911),('P91-CAP',2913,2973),('P91-A7',3147,3173),('P91-A8',3174,3190),('P91-A2',3325,3339)]
spans=[];private=[]
for aid,a,z in spec:
 chunk=b''.join(lines[a-1:z]);s={'id':aid,'line_start':a,'line_end':z,'byte_start':sum(map(len,lines[:a-1])),'byte_end_exclusive':sum(map(len,lines[:z])),'raw_sha256':hashlib.sha256(chunk).hexdigest(),'bytes':len(chunk)};spans.append(s);private.append({**s,'html':chunk.decode('utf8')})
extract=write('primary-spans91.private.json',{'publication':'PRIVATE primary extracts; do not publish','primary':raw(primary),'spans':private})
items=[
('C01','P91-V','standing','Fixed arXiv2609.06905v1, 07 Sep 2026; perpetual non-exclusive arXiv distribution license. Local attributed restatement only.'),
('C02','P91-H','hypothesis','V is globally C2; 0<alpha<=beta and alpha I<=Hess V(x)<=beta I for every x.'),
('C03','P91-ETA','hypothesis','0<eta<=1/beta. Fixed y, reference x and initial phase; dimension is a finite Euclidean typing choice.'),
('C04','P91-CENTER','definition','Center c=y-eta gradV(reference); gradient difference g(x)=gradV(x)-gradV(reference).'),
('C05','P91-A1','definition','Literal harmonic flow, nonnegative rate sqrt(eta)[p dot g(x)]+, momentum reflection with zero-normal identity.'),
('C06','P91-A1','probability-input','Independent Exp(1) sequence at fixed deterministic event depth; next unused coordinate, not an arbitrary random history or physical-time residual clock.'),
('C07','P91-A1','definition','Next relative wait is the integrated-hazard threshold infimum on nonnegative time, with empty crossing infinity.'),
('C08','P91-A1','definition','Finite next wait gives absolute Tnext=T+wait and post-bounce S(Phi_wait(z)); infinite wait terminates recursion.'),
('C09','P91-A1','definition','Between events the path follows Phi, on the half-open pre-event time interval. Post-jump records determine subsequent segments.'),
('C10','P91-A2','printed-proof','Joint Borel flow/rate/bounce, hazard, threshold hitting and finite recursion are proved from continuity and rational-time tests.'),
('C11','P91-A7','printed-target','A7 integrates over strict 0<t1<...<tn<T, with n=0 empty vector and empty product one.'),
('C12','P91-A7','printed-definition','Prescribed path is built by flowing and bouncing at the supplied strict times. Its pre-bounce rate is evaluated at t_j minus.'),
('C13','P91-A7','source-implicit','Iterate the conditional finite-event law with complete generated history and unused iid input to multiply finite-event density factors.'),
('C14','P91-A7','source-implicit','Convert relative waits to cumulative absolute event times, either one-step conditional translation or full triangular cumulative-sum substitution; alternatives, not simultaneous AND.'),
('C15','P91-A7','source-implicit','Identify constructed complete histories with prescribed-path states on strict ordered time support, and retain all earlier records.'),
('C16','P91-A7','source-implicit','Final no-next-event factor is exp(-hazard at duration T-Tn) on live finite histories; arbitrary Borel history-dependent duration is required.'),
('C17','P91-A7','source-implicit','Sum segment hazards including final duration to the integrated rate along the prescribed full path; finite point changes do not change Lebesgue integrals.'),
('C18','P91-A7','source-implicit','Identify exactly n events before horizon with first n finite ordered events and final survival; strict versus non-strict horizon boundary requires an internally proved no-finite-atom edge if equality is asserted.'),
('C19','P91-CAP','printed-proof','Energy preservation and the finite rate cap imply nonexplosion from exponential sums; needed for exhaustive finite-count partition, not a one-step coordinate translation.'),
('C20','P91-A7','printed-proof','Bounded measurable path tests, simplex volume T^n/n!, and energy rate cap justify absolute convergence and signed expectation assembly.'),
('C21','P91-A2','source-implicit','For generalized nonnegative joint tests, require jointly Borel constructed histories/path observables and Tonelli; these are proof obligations, not extra source analytic assumptions.'),
('C22','P91-CAP','excluded','Physical-time exponential residual memorylessness/Markov restart is a separate argument and is not a parent for fixed-depth finite-event iteration.'),
('C23','P91-A8','excluded','Path reversal, invariance and semigroup conclusions follow after A7 and are outside this preread target.'),
('C24','P91-A2','excluded','Terminal infinite-process limit/kernel/L2 claims are separate from finite deterministic history coordinate laws.'),
('C25','P91-A7','convention','Unnormalized restricted measures handle null history events; stopped tags have no finite next density; live infinite waits supply missing finite-event mass and final survival.'),
('C26','P91-A7','convention','Zero horizon/cutoff has empty positive-wait support. Rank zero or zero hazard has no positive finite-event component; n=0 remains a live deterministic initial record.'),
('C27','P91-A7','boundary','Finite horizon T is fixed, not random stopping time; a cutoff d(Hn) is random only by evaluating a fixed Borel finite-valued function on the whole past.')]
inventory=write('source-inventory91.primary-first.native.json',{'schema':'astis-independent-primary-inventory91-v1','reviewer':'/root/fresh_source87','primary':raw(primary),'spans':spans,'coverage':[{'id':i,'anchor':a,'disposition':d,'restatement':s} for i,a,d,s in items],'creator_self_independent_approval':False})
graphmath={
 'source_inputs':['C02','C03','C04','C05','C06','C07','C08','C09'],
 'nodes':[
 {'id':'I91-M','claim':'Joint Borel finite recursion and canonical histories/path constructors','anchors':['P91-A1','P91-A2']},
 {'id':'I91-D','claim':'Conditional positive finite next-wait density from actual past/unused iid threshold','anchors':['P91-A1','P91-A7']},
 {'id':'I91-E','claim':'Actual complete next-history extension on strict finite relative-wait support','anchors':['P91-A1','P91-A2']},
 {'id':'I91-C','claim':'Relative-to-absolute event-time coordinate law preserving strict support and all joint nonnegative tests','anchors':['P91-A1','P91-A7']},
 {'id':'I91-J','claim':'Finite-depth ordered absolute-time density multiplication and prescribed complete-history identification','anchors':['P91-A7']},
 {'id':'I91-S','claim':'Conditional live final-wait survival at the history-dependent remaining horizon','anchors':['P91-A1','P91-A7']},
 {'id':'I91-F','claim':'Combine finite-event products and final survival into full path hazard factor','anchors':['P91-A7']},
 {'id':'I91-B','claim':'Boundary-event nullness only for required strict/non-strict count identifications','anchors':['P91-A7']},
 {'id':'I91-N','claim':'Nonexplosion and exhaustive finite-count partition at fixed finite horizon','anchors':['P91-CAP','P91-A7']},
 {'id':'I91-A7','claim':'Bounded measurable actual path expectation equals the full absolutely convergent A7 series','anchors':['P91-A7']}],
 'and_junctions':[
 {'target':'I91-J','parents':['I91-M','I91-D','I91-E','I91-C'],'note':'Iterative route: D may be transitive through E; avoid demanding duplicate theorem premises.'},
 {'target':'I91-F','parents':['I91-J','I91-S'],'note':'Need segment-hazard algebra and prescribed-path identification internally.'},
 {'target':'I91-A7','parents':['I91-F','I91-N','I91-M'],'note':'Boundary edge B is additionally required if chosen count convention equates strict/non-strict endpoints; cap supplies convergence.'}],
 'or_routes':[
 {'target':'I91-C','alternatives':['one-step history-dependent translation u=Tn+s','iterate relative waits first, then triangular cumulative-sum change of coordinates']},
 {'target':'I91-J','alternatives':['iterate existing actual complete-history extension','rederive sections directly from actual history/unused-tail law and deterministic density']},
 {'target':'I91-B','alternatives':['deduce fixed finite-time atoms vanish from finite density','avoid endpoint equality while stating only strict restricted submeasures']}],
 'excluded_and_parents':['physical-time residual memorylessness','survival as a parent of finite-density-only coordinate law','no-atom as a parent of strict-to-strict coordinate transport','arbitrary stopping-time independence','provider constructor/density/measurability hypotheses'],
 'self_topology_approval':False}
inventory_math=write('primary-reconstruction91.before-retrieval.native.json',graphmath)
inputs=[raw(primary)]+[raw(ROOT/p) for p in ['runs/20261007-companion-priority/pbps-ordered-history-iteration-preread91/pre-fetch91.workspace-RAW.json','runs/20261007-companion-priority/pbps-ordered-history-iteration-preread91/capsule.exactraw.log','runs/20261007-companion-priority/pbps-ordered-history-iteration-preread91/scheduling91.json','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','.agents/skills/astis-semantic-roundtrip/SKILL.md','.agents/skills/astis-substantive-advance/SKILL.md','docs/proof-digestion-protocol.md']]
freeze=write('primary-first91.freeze.native.json',{'schema':'astis-source-preread91-v1','closed':True,'utc':now,'reviewer':'/root/fresh_source87','formalizer':'/root','scope':'SOURCE ONLY; no91 candidate/header/BODY read or available; no proof or status credit','prior_familiarity':'Independent prospective headers and complete source audits of87-90, including89 density and90 extension, previously reviewed. This reread reconstructs source topology directly and freezes before fresh accepted-interface/retrieval consultation. Current handoff/capsule necessarily disclose accepted90 boundary.','sequence':['Read current pre-fetch/capsule/execution/latest90 handoff and skills','Direct pinned primary raw read/version/license/assumptions/A1/A2/A7','Independent source mathematical inventory and proof-route alternatives frozen now','Only after this closed freeze: accepted graphs/interfaces and local reuse search'],'primary_version':'arXiv:2609.06905v1 [math.ST] 07 Sep 2026','license':'arXiv.org perpetual non-exclusive license','inputs':inputs,'outputs':[extract,inventory,inventory_math],'unresolved':'No new91 statement/SAU chosen until interface retrieval. All I91-J/F/N/A7 and global obligations remain open.','creator_self_independent_approval':False})
manifest=write('closed-raw-manifest.primary-first91.native.json',{'schema':'astis-closed-raw-manifest91-v1','closed':True,'inputs':inputs,'outputs':[extract,inventory,inventory_math,freeze,raw(Path(__file__).resolve())],'no_self_hash':True,'verification':'Every descriptor rehashed against exact native bytes before terminal closure.'})
for d in inputs+[extract,inventory,inventory_math,freeze,manifest]:
 p=ROOT/d['path'];assert raw(p)==d
print(json.dumps({'primary_first_freeze':freeze,'manifest':manifest,'inventory':inventory,'source_math':inventory_math},indent=2))
