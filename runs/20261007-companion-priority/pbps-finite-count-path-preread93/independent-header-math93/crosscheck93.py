from pathlib import Path
import hashlib,json,collections
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=R/'runs/20261007-companion-priority/pbps-actual-ordered-prefix92';G=B/'next-source-graph93';H=O.parent/'Header93.lean'
def path(p):
 p=Path(p);return p if p.is_absolute() else R/p
def info(p):
 p=path(p);b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def load(p):return json.loads(path(p).read_bytes())
def check(e):assert info(e['path'])==e
def save(n,v):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
gp=G/'candidate-source-proof-graph93.v2.native.json';cp=G/'candidate-source-coverage93.v2.native.json';g=load(gp);c=load(cp);check(c['graph']);check(g['primary']);check(g['candidate']);check(g['source_first_provenance']);check(c['predecessor_inventory'])
assert info(H)['raw_sha256']=='90bca17fbb11d9a8fea226bd0dca6494ef9a61f3db31beaf52c0ef2999cf9cfe'
old_report=info(O/'header-math-review93.native.json');old_manifest=info(O/'closed-RAW93.native.json')
assert old_report['raw_sha256']=='3fcfe3724bce7e4a3ff340e289e669773fae65646ba44c19af9af2124a089163';assert old_manifest['raw_sha256']=='ee6ef15e43c4668cb9262c9260725db6eb8db9f004237369f5b59a8640b9c217'
nodes={n['id']:n for n in g['nodes']};assert len(nodes)==g['node_count']==35;assert len(g['edges'])==g['edge_count']==94;assert len(c['coverage'])==c['coverage_count']==55
assert len({r['id'] for r in c['coverage']})==55
primary=path(g['primary']['path']).read_bytes()
for e in list(g['source_regions'].values())+list(c['source_regions'].values())+[r['source_region'] for r in c['coverage']]:assert hashlib.sha256(primary[e['byte_start']:e['byte_end_exclusive']]).hexdigest()==e['raw_sha256']
covered=set();indegree={n:0 for n in nodes};children=collections.defaultdict(list)
for e in g['edges']:
 assert e['from'] in nodes and e['to'] in nodes;assert e['relation']=='source-proof-ingredient-not-Lean-edge';indegree[e['to']]+=1;children[e['from']].append(e['to'])
queue=[n for n in nodes if indegree[n]==0];topo=[]
while queue:
 n=queue.pop();topo.append(n)
 for d in children[n]:
  indegree[d]-=1
  if indegree[d]==0:queue.append(d)
assert len(topo)==35
for r in c['coverage']:
 assert r['disposition'] in ['NODE','SOURCE_GAP','EXCLUDED'] and r['reason'] and r['no_proof_credit']
 assert r['node_statuses']=={n:nodes[n]['status'] for n in r['nodes']};covered.update(r['nodes'])
assert covered==set(nodes);assert not c['unmapped_rows'] and not c['uncovered_selected_inventory_rows']
pred=load(c['predecessor_inventory']['path']);assert {r['predecessor_row'] for r in c['coverage'] if r['predecessor_row']}=={r['id'] for r in pred['coverage']}
mapping={'SURV93':['DUR93','LOCAL93','DENS93'],'HISTORY_PATH_ADAPTER93':['HISTPATH93','TEST93'],'PATH93':['GAMMA93','PATHSPACE93','PATHM93','IDENT93'],'END93':['NULL93','END93','POS93'],'COUNT93':['SELECT93','COVER93','COUNT93'],'JOINT_LAW93':['DENS93','TEST93','JOINT93']}
old_feas=load(B/'next-boundary-math93/feasibility-review93.native.json');assert set(mapping)=={x['id'] for x in old_feas['required_internal_obligations']}
edges={(e['from'],e['to'],e['logic']) for e in g['edges']};assert all((x,'JOINT93','AND') in edges for x in ['DENS93','COUNT93','PATHM93','IDENT93','ZERO93','TEST93'])
assert ('HISTPATH93','TEST93','AND') in edges and ('IDENT93','TEST93','AND') in edges and ('PATHM93','TEST93','AND') in edges
assert {(e['from'],e['to']) for e in g['edges'] if e['logic']=='OR'}=={('CAP93','A7'),('MASS93','A7')}
for n in ['HAZARD93','LEFT93','TERM93','CAP93','A7']:assert nodes[n]['status']=='FUTURE_OPEN'
assert nodes['MASS93']['status']=='FUTURE_OPTIONAL_OPEN';assert nodes['SKOR93']['status']=='OUTSIDE_CURRENT_CARRIER'
report=dict(decision='ACCEPT_BOUNDED_TOPOLOGY_COVERAGE_CROSSCHECK',reviewer='/root/independent_math91',header=info(H),preserved_header_acceptance=old_report,preserved_header_manifest=old_manifest,graph=info(gp),coverage=info(cp),scope='Independent cross-check of the source-derived candidate graph/coverage against the accepted prospective Header93; not a proof, finalized Statement Seal, compiled dependency certificate or canonical transition.',counts={'nodes':35,'edges':94,'dispositions':55,'preserved_predecessor_dispositions':46,'additional_dispositions':9,'all_nodes_covered':True,'acyclic':True},feasibility_obligation_to_nodes=mapping,findings=[
'All six named obligation groups from the prior feasibility audit have explicit nodes. The previously missing total ambient-history path map is HISTPATH93, and the measurable h->F(h,Psi(h)) transport is TEST93. HISTPATH93/IDENT93/PATHM93 feed TEST93, which is an AND parent of JOINT93.',
'Header93 implements the graph planned representations literally: finite ascending fold for the total largest-eligible-index Psi, Gamma=Psi(K), explicit product path carrier, strict C, Nat.find/zero-fallback N, and terminal rho. Its six original analytic premises remain the only substantive binders. Joint measurability, actual path identity, count/no-endpoint assertions, measure law and tests are conclusions to prove.',
'Every edge explicitly says source-proof-ingredient-not-Lean-edge. Existing interface pointers have proof_reverified=false; new adapters are PROPOSED_OBLIGATION and JOINT93 is PROPOSED_TARGET_NOT_SEALED. This graph cannot be substituted for the future compiled dependency traversal.',
'All35 nodes occur in at least one coverage row, every row has a disposition/reason and status-consistent node references, and all46 predecessor selected-source subclaims survive among55 rows. All source-region RAW byte hashes match the pinned primary. Exhaustiveness is explicitly bounded to the selected inventory, not the whole paper.',
'The target AND bundle contains terminal density, count identification, path measurability, pointwise identity, zero cases and joint-test transport. Existing78/79 nonaccumulation/coverage is reused via ENERGY93/COVER93, rather than replaced with a public rate-cap hypothesis or re-awarded as new work.',
'HAZARD93, LEFT93 and TERM93 remain future requirements for the printed full-path integrand. TERM93 and COUNT93 are common A7 prerequisites; CAP93 versus MASS93 remains a genuine OR group for convergence/integrability. Neither future convergence branch is an extra mandatory parent of the finite-count target.',
'SKOR93 is correctly outside the selected carrier and is not mislabeled as an interchangeable proof route. Full A7, random-depth restart/Markovness, reversal, stationary/random-reference averaging, operator/mixing/cost statements remain future or explicitly excluded.',
'The raw/AE distinction matches the accepted header: pointwise path equality only on measurable C_n, fixed-T AE no-endpoint and count identities, no uncountable AE intersection and no path-diagonal measurability premise.'
],bounded_reading_notes=[
'C93-24 phrase n0 survives with probability1 must be read in its explicit T0-bookkeeping context and together with ZERO93/Header93. For n0 and T>0, terminal survival mass is exp(-Lambda(z0,T)), generally below1. A later reader rendering should retain the T=0 qualifier. This is not a header error or topology blocker.',
'exact_Lean_signature_not_yet_drafted=true and the coverage source-before-signature wording describe the preserved graph creation snapshot. This cross-check supplies the later exact Header93 binding without rewriting that historical artifact.'
],required_corrections=[],header_report_unchanged=True,proof_credit=False,canonical_state_changed=False)
save('topology-crosscheck93.native.json',report)
inputs=[gp,cp,H,path(g['primary']['path']),path(g['candidate']['path']),path(g['source_first_provenance']['path']),path(c['predecessor_inventory']['path']),B/'next-boundary-math93/feasibility-review93.native.json',O/'header-math-review93.native.json',O/'closed-RAW93.native.json']
save('closed-RAW93.topology-successor.native.json',dict(predecessor_manifest=old_manifest,inputs=[info(p) for p in inputs],outputs=[info(p) for p in sorted(O.iterdir()) if p.is_file()],closure='Append-only successor closure; accepted header report and prior manifest bytes preserved. Self hash excluded.'))
assert info(O/'header-math-review93.native.json')==old_report and info(O/'closed-RAW93.native.json')==old_manifest
for p in [O/'topology-crosscheck93.native.json',O/'closed-RAW93.topology-successor.native.json']:print(json.dumps(info(p)),flush=True)
