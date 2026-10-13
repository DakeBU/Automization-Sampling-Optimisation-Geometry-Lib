from pathlib import Path
import json,hashlib,sys,datetime,os
sys.stdout.reconfigure(encoding='utf8')
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-marginal-poincare-consumer-overlay57';O=R/'runs/20261007-companion-priority/pbps-marginal-poincare-consumer-overlay-review57';G=R/'runs/20261007-companion-priority/pbps-marginal-poincare-sourcegraph57';N=R/'runs/20261007-companion-priority/pbps-marginal-poincare-sourcegraph-review57'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(j):return json.dumps(j,ensure_ascii=False,allow_nan=False,sort_keys=True,separators=(',',':')).encode('utf8')
def pin(p):
 p=Path(p);p=p if p.is_absolute() else R/p;b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return {'path':str(p).replace('\\','/'),'bytes':len(b),'raw_sha256':sha(b),'lf_bytes':len(lf),'lf_sha256':sha(lf)}
def write(n,j):
 j['content_self_sha256']=sha(canon(j));p=O/n;p.write_bytes((json.dumps(j,ensure_ascii=False,indent=2)+'\n').encode('utf8'));q=json.loads(p.read_bytes());v=q.pop('content_self_sha256');assert sha(canon(q))==v;return pin(p)
checks=[];selfchecks=[];inputs={};unused_modules=[]
def check(q,where):
 a=pin(q['path']);assert all(a[k]==q[k] for k in ['bytes','raw_sha256','lf_bytes','lf_sha256'] if k in q),(where,q['path']);inputs[a['path']]=a;checks.append({'where':where,'actual':a})
def walk(j,where):
 if isinstance(j,dict):
  if {'path','bytes','raw_sha256','lf_sha256'}<=set(j):check(j,where)
  if 'content_self_sha256' in j:
   q=dict(j);v=q.pop('content_self_sha256');assert sha(canon(q))==v,where;selfchecks.append({'where':where,'digest':v})
  for k,v in j.items():
   if where.startswith('overlay/parent_public_headers/') and k=='module':unused_modules.append({'where':where+'/module','creator_metadata_only':v,'review_uses_public_header_only':True});continue
   walk(v,where+'/'+k)
 elif isinstance(j,list):
  for i,v in enumerate(j):walk(v,where+'/'+str(i))
overlay=json.loads((B/'consumer.overlay.json').read_bytes());lease=json.loads((B/'lease.json').read_bytes())
walk(overlay,'overlay');walk(lease,'root-overlay-lease');assert lease['status']=='CLOSED' and lease['compiler']=='NOT_STARTED_CLOSED'
for p in [B/'consumer.overlay.json',B/'lease.json',G/'graph.packet.json',G/'lease.json',G/'source-only-freeze.json',G/'binder-and-reuse-audit.json',N/'topology.review.json',N/'lease.json',N/'native.verification.json',N/'graph.path.evidence.json',N/'reviewer.topology.run.json']:
 inputs[str(p).replace('\\','/')]=pin(p);j=json.loads(p.read_bytes());v=j.pop('content_self_sha256');assert sha(canon(j))==v;selfchecks.append({'where':str(p).replace('\\','/'),'digest':v})
g=json.loads((G/'graph.packet.json').read_bytes());original=json.loads((N/'topology.review.json').read_bytes());assert original['verdict']=='ACCEPT_STANDALONE_PI_SOURCE_EXTRACTION_WITH_TYPED_CONSUMER_BLOCKERS'
assert set(overlay['resolves_only'])=={q['id'] for q in original['consumer_blockers']}
assert len(overlay['nodes'])==7 and len(overlay['edges'])==7
assert pin(G/'graph.packet.json')['raw_sha256']=='b4c3f3db9ff224bf7fcf048026e3cc1ca003b93b708f080dca2e5307cca6c6ed'
assert pin(G/'lease.json')['raw_sha256']=='52e92f9f1048d3823dd1c02a17c0f4655bc1e243058ee3dc834e62c9895e938c'
assert pin(N/'topology.review.json')['raw_sha256']=='14293067722ea97a2e7a4cd76c4a365994a65192c1a3d2d63428b1728314b0a2'
assert pin(N/'lease.json')['raw_sha256']=='aa5eb668eea85d736640a522c1adf9a57b157719af6a86e1d387cdf15aaf8143'
# Review current public prefixes only; actual module proof suffix is never read.
headerchecks=[]
for q in overlay['parent_public_headers']:
 path=R/q['module']['path'];parts=[]
 with path.open('rb') as h:
  for line in h:
   if b' := by' in line:parts.append(line.split(b' := by',1)[0]);break
   parts.append(line)
 prefix=b''.join(parts).replace(b'\r\n',b'\n').rstrip()+b'\n';assert prefix==Path(R/q['public_header']['path']).read_bytes()
 headerchecks.append({'module_path':q['module']['path'],'actual_public_prefix_matches':True,'snapshot':pin(R/q['public_header']['path']),'cutoff':'Before literal space := by; terminal whitespace normalized to one LF; proof suffix not read.'})
core56=(B/'RoughMeanGradient.public-header.lf.snapshot.lean').read_bytes();core55=(B/'L2MacroscopicMean.public-header.lf.snapshot.lean').read_bytes()
for b in [core55,core56]:assert b'let J := (\xce\xbc.prod (stdGaussian E)).map' in b and 'let ν := J.snd'.encode() in b
assert 'Λ.IsCondKernel S ∧ Λ.fst = ν ∧ Λ.snd = ν'.encode() in core55
assert '(T u,K u) ∈ G.closure.graph'.encode() in core56
stmt=(R/overlay['exact_statement']['path']).read_bytes().replace(b'\r\n',b'\n');assert len(stmt)==1244 and sha(stmt)=='e706b4e6c3c07f58a090ee86cb51dd91be2f11afe707db653737e4983c7181e9'
nodes=g['nodes']+overlay['nodes'];ids={n['id'] for n in nodes};assert len(ids)==len(nodes)
edges=[{'parents':e['parents'],'target':e['consumer'],'formal_dependency_admitted':e['formal_dependency_admitted']} for e in g['edges']]+overlay['edges'];parents={n:[] for n in ids}
for e in edges:
 assert e['target'] in ids and all(q in ids for q in e['parents']) and e['formal_dependency_admitted'] is False
 parents[e['target']].extend(e['parents'])
def ancestors(n):
 seen=set();todo=list(parents[n])
 while todo:
  q=todo.pop()
  if q in seen:continue
  seen.add(q);todo.extend(parents[q])
 return sorted(seen)
c3=ancestors('pbps57:scoped-C3');c4=ancestors('pbps57:scoped-C4')
for q in ['pbps57:actual56-pair','pbps57:same-core-closure','pbps57:actual55-stationarity','pbps57:actual56-mean-preservation','pbps57:scoped-compact-PI57']:assert q in c3 and q in c4
for q in ['pbps57:weak-H1-adapter','pbps57:Gamma-root','pbps57:C3','pbps57:C4']:assert q not in c3 and q not in c4
assert parents['pbps57:centered-Af']==[] # Original negative is retained, not silently rewritten.
write('path.verification.json',{'schema_version':1,'actor':'/root/next_primary56','combined_nodes':len(nodes),'combined_edges':len(edges),'source_graph_unchanged':True,'original_centered_Af_parents':parents['pbps57:centered-Af'],'original_C3_parents':parents['pbps57:C3'],'scoped_C3_ancestors':c3,'scoped_C4_ancestors':c4,'required_paths_explicit':True,'weakH1_gap_not_consumed_or_discharged':True,'original_source_C3_C4_not_admitted':True,'native_receipt_checks':checks,'native_receipt_check_count':len(checks),'complete_self_checks':selfchecks,'header_only_verification':headerchecks,'unused_full_module_metadata':unused_modules,'root_author_negative_preserved':lease['negative_read_schema'],'standalone_statement_exact1244_sha256':sha(stmt),'coverage606_reused_unchanged':original['coverage'],'hash_recipe':'COMPLETE object minus ONLY content_self_sha256; sorted compact ensure_ascii=False allow_nan=False UTF8 no newline; actual raw/LF hashes separate.'})
report={'schema_version':1,'artifact_kind':'independent-distinct-consumer-overlay-review','reviewer':'/root/next_primary56','creator':overlay['actor'],'independent_from_creator':True,'verdict':'ACCEPT_PLANNED_SCOPED_CONSUMER_TOPOLOGY_ONLY','overlay':pin(B/'consumer.overlay.json'),'root_closed_lease':pin(B/'lease.json'),'original_graph':pin(G/'graph.packet.json'),'original_negative':pin(N/'topology.review.json'),'resolved_paths':['57-consumer-domain-path','57-consumer-centering-path'],'blockers':[],'statement_repair':None,'semantic_deltas':[],'minimality':'Seven distinct new interface/consumer nodes and seven dependency-plan edges expose the existing56 pair, sealed57 scopedPI, same-core agreement, actual55stationarity, derived56mean preservation and scopedC3/C4. No original node/edge/source/statement is overwritten. Coverage596+10 and all original17semantic/10sourceedges remain immutable.','slot_assessment':{'same_objects':'All parent headers/candidate use original potential and same mu/J/nu. Actual55 S_y EVERY-y literal tilted reflected density agrees with actual56 literal S; no arbitrary caller law.','domain':'Exact graph iff smooth compact phi and AE scalar/vector pair in bothG56/G57 forces graph and partial-operator equality. Therefore closures agree and actual(T56u,K56u) membership transfers internally; C2 energy alone is not used as domain evidence.','quantifiers':'Uniform genuine G56,T56,K56 before allu and uniform G57 before all centered closure-domain z. No observer-dependent selection or extra domain/core/operator certificates.','centering':'Actual55 conditional kernel with Lambda.fst=Lambda.snd=nu gives S composed nu=nu. Probability makes rough L2 input L1; actual56 AE literal conditional mean plus conditional integration/Fubini yields integral(T56u)=integral(u). Centered input then supplies centered output internally.','same_gradient':'Transferred pair means G57bar(T56u)=K56u by genuine graph single-valuedness; scopedPI applies to that exact derivative and SAME T56.','sharp_combination':'m=alpha/(1+alpha eta); m||T56u||²<=||K56u||² plus eta||K56u||²<=c(||u||²−||T56u||²), c=(1-alphaeta)²/[4(1+alphaeta)]. Rearrangement gives normfactor(1-alphaeta)/(1+alphaeta) for centeredu. Original0<alpha<=beta and cappedeta gives0<alphaeta<=1; denominator1+alphaeta positive, no division by1-alphaeta.','scope':'Original printed sourceC3/C4 remain untouched. NewscopedC3/C4 are planned actual L2(nu) compact-closure consumers, no full weakH1, macro onto-range identification, Gamma/spectral/main claim.','binder_audit':'Original source assumptions retained, finiteHilbert/Borel/rank0 extension remains explicit; no added sourcehypothesis/publiccertificate.'},'public_headers_only':headerchecks,'full_module_receipts':'Root overlay includes full module metadata pins; this review relies on public prefix/header snapshots and prior56 accepted evidence. Full module bytes/proof suffixes not reread; no new full-module receipt verification or proof-body blindness claim about historical56.','upper_provider_reuse':'Separately accepted exact SmoothedHessianUpper plus normalization-shift route remains unchanged; no source repair or duplication required.','negative_history':['Original57 zero-parent centered-Af and missing originalC3 domain dependency remain recorded; distinct overlay adds separate scoped consumers, does not retrospectively certify old topology.','Root overlay author initially stopped on originallease status/state schema before any file write; native negative_read_schema retained.','Original56 post-CLOSED mutation/restoration and provider/finalbody blindnessfalse retained; no fabricated fresh blinded rerun.','Original decoder malformed6locators and distinct operational-only repair retained.'],'truth_boundary':'Accept only dependency-plan readiness for exact scoped future consumers. No57SAU/theorem/Test/proof or mathematics admitted; compiler never started, parent proof suffixes not read. Source weakH1/fullB13/Gamma/halfturn/macro-range/main/cost/composition remain OPEN.','repairs':[],'native_hash_recipe':'COMPLETE object excluding only content_self_sha256; sorted compact UTF8 ensure_ascii=False allow_nan=False; raw/LF file receipts distinct.'}
write('consumer-overlay.review.json',report)
write('input.manifest.json',{'schema_version':1,'actor':'/root/next_primary56','inputs':list(inputs.values()),'input_count':len(inputs),'header_only_checks':headerchecks,'unused_full_module_metadata':unused_modules,'receipt_recipe':'Exact raw bytes; LF replaces onlyCRLF; public parent reads stop before proof marker; no full-module bytes needed or claimed checked.'})
(O/'inputs').mkdir(exist_ok=False)
for i,q in enumerate(inputs.values()):
 b=Path(q['path']).read_bytes();stem=f'{i:03d}.{Path(q["path"]).name}';a=O/'inputs'/(stem+'.raw.snapshot');z=O/'inputs'/(stem+'.lf.snapshot');a.write_bytes(b);z.write_bytes(b.replace(b'\r\n',b'\n'));assert a.read_bytes()==b and z.read_bytes()==b.replace(b'\r\n',b'\n')
print(json.dumps({'status':'REVIEW_PREPARED','pid':os.getpid(),'verdict':report['verdict'],'native_receipt_checks':len(checks),'complete_self_checks':len(selfchecks),'inputs':len(inputs),'combined_nodes':len(nodes),'combined_edges':len(edges),'blockers':0},ensure_ascii=False))
