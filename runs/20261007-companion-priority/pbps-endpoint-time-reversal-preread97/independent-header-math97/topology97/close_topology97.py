from pathlib import Path
import json,hashlib,copy
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;P=O.parents[1]
sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(p.read_bytes())
def info(p):return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def write(n,v):
 p=O/n;assert not p.exists();p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
initial=load(O/'initial-topology-findings97.native.json');oldref=initial['inputs'][1];original=R/oldref['path'];old=load(original)
assert sha(original.read_bytes())==oldref['raw_sha256']=='6182556a00cda5d7554ba4f05c8b24c72830e6b599eda948d6c82661296fb72a'
v2path=P/'source-proof-graph97.v2.native.json';v2=load(v2path)
assert sha(v2path.read_bytes())=='6873df1267043d0da4bf8789d9964213a6558aecb1e90f0124220b679346078e'
assert v2['predecessor']['path']==oldref['path'] and v2['predecessor']['raw_sha256']==oldref['raw_sha256']
want=copy.deepcopy(old);edges=v2['edges'][len(old['edges']):]
assert len(edges)==2 and {(x['from'],x['to']) for x in edges}=={('D97','END_VOL97'),('REV_TIME97','END_INV97')}
assert all(x['logic']=='AND' and x['certified_Lean_edge'] is False for x in edges)
assert edges[0]['consumer_use_site']=='Actual zAt finite phase composition and terminal harmonic flow identifying the prescribed endpoint'
assert edges[1]['consumer_use_site']=='Only the defining rho coordinate equation and reversed arc-gap order; no use of time-volume preservation'
assert old['kind']=='source-only-proof-graph97' and v2['kind']=='source-proof-graph97-corrected-before-proof'
want['kind']=v2['kind'];want['edges']+=edges;want['predecessor']=v2['predecessor'];want['revision_reason']=v2['revision_reason'];assert want==v2
snap=O/'inputs/6.source-proof-graph97.v2.native.json.exactraw';snap.write_bytes(v2path.read_bytes())
for x in initial['inputs']:assert sha((R/x['path']).read_bytes())==x['raw_sha256'],x['path']
assert sha((R/initial['primary']['path']).read_bytes())==initial['primary']['raw_sha256']
assert sha((P/'Header97.lean').read_bytes())=='2f27a049026ab398bfc85cecf1b2a450e8fef17c45e3a79e8b492c731343800b'
decision=dict(kind='independent-source-topology-and-coverage-validation',reviewer='/root/exact_verifier96',decision='ACCEPT_CORRECTED_V2_BOUNDED_SOURCE_TOPOLOGY_AND_COVERAGE',mode='Independent validation; proposed topology and Header97 had already been seen before direct primary re-reading. NOT source-blind reconstruction and NOT anti-anchored final semantic theorem review.',original_graph=info(original),corrected_graph=dict(**info(v2path),snapshot=snap.relative_to(R).as_posix()),initial_required_corrections=info(O/'initial-topology-findings97.native.json'),corrections_closed=[dict(id='D97-to-END_VOL97',status='accepted',reason='Adds exact actual endpoint-construction use site required by source finite-composition argument.'),dict(id='REV_TIME97-to-END_INV97',status='accepted',reason='Adds only rho coordinate/reversed-gap projection consumed by endpoint inverse; explicitly excludes time-volume as an inversion prerequisite.')],original_negative_evidence_preserved=True,no_unreviewed_graph_changes=True,no_required_corrections_remaining=True,
primary=initial['primary'],coverage=initial['inputs'][0],selected_source_regions=initial['selected_region_checks'],selected_region_count=15,inherited_inventory_exact_references_verified=True,
independent_primary_findings=[
 'Standing source S1.p1 gives V C2 and 0<alpha<=beta with matrix-order Hessian bounds. S2.SS2.p1 gives eta in (0,1/beta]. Header expresses these as the original six analytic binders; finite Hilbert/Borel and rank-zero choices remain explicit coordinate elaborations, not new analytic premises.',
 'A1.SS1.p1 defines the exact scaled harmonic flow, reflection and R0=I. A1.SS1.p2 assigns post-jump states and half-open between-jump intervals; treating this as D97 convention does not import the random clock as a dependency.',
 'The pre-A5 conjugation/commutation identities and A6 factor volume furnish M96 inputs. A5 rate matching is correctly excluded from the unweighted97 theorem and retained for DENSITY98.',
 'A1.Ex19 defines the strict open ordered simplex; the immediately following prescribed-path paragraph defines the actual finite trajectory. These justify D97 and the reversed tuple construction, with no closed-simplex replacement or factorial normalization.',
 'A7 and the absolute-series/initial-average paragraph are upstream evidence for later AVG98, not prerequisites of deterministic endpoint/time97. The graph explicitly keeps this direction and preserves prior coverage by exact references.',
 'A8 specifies time complementation after index reversal. Its path display conflicts at nontrivial jumps with the earlier post-jump convention if interpreted as literal all-time right-continuous equality. Header97 uses only endpoint/time involution; the existing off-event/pre-post warning correctly preserves this boundary.',
 'Source lines3184-3194 justify the endpoint as a finite composition of Borel preserving factors despite bounce discontinuity. Corrected D97 and M96 edges into END_VOL97 now expose both actual composition and factor laws. Joint state/time measurability and the product-map bridge remain explicit proof obligations.',
 'Source lines3195-3198 use reversed ordered times for the inverse and time-map volume for the full change of variables. The corrected graph distinguishes the reversed-gap projection used in END_INV97 from the separate volume conclusion needed at K97.',
 'The source calls time reversal linear, but for nonzero T it is affine with signed-permutation linear part and unit absolute determinant. The intended measure statement remains sound and the coverage records this notation resolution.',
 'Source lines3200-3227 separately integrate A4, match A5 factors, use nonnegative Tonelli then signed decomposition, derive skew balance and take F=1 for invariance. DENSITY98,AVG98,INV98 remain excluded97 consumers. No restart/Markov/L2 or paper-completion dependency is smuggled into97.' ],
coverage_boundary='All 15 selected source regions have exact byte bindings and explicit NODE/CONVENTION-or-EXCLUDED dispositions. D97 convention is treated as a definition/convention node. This is a bounded review of the97 source slice; no exhaustive rereview of all inherited whole-paper inventory or future weighted98 proof is claimed.',
graph_truth_boundary='All edges remain source-planning AND edges with certified_Lean_edge=false. K97 is the conceptual endpoint/time map and Header97 calls its concrete transform Theta to avoid collision with K(history). No Lean theorem, compiled dependency, proof completion or Goal credit is granted.',
source_review_separation='This reviewer is independent of source_final96, the author of the source-only proposal. The review closes bounded topology/coverage corrections; Header97 still requires its separately assigned source-header fidelity review and later blind decoder/final source review after proof.',theorem_credit=False,proof_started=False,shared_mutations=False)
decision['metadata_only_kind_label_change']='source-only-proof-graph97 -> source-proof-graph97-corrected-before-proof; inspected and accepted alongside predecessor/revision metadata.'
write('source-topology-decision97.native.json',decision)
write('closed-RAW-topology97.native.json',dict(kind='closed-independent-topology-validation',reviewer='/root/exact_verifier96',mode='nonblind independent validation',self_excluded=True,files=[info(p) for p in sorted(O.rglob('*')) if p.is_file() and '__pycache__' not in p.parts],external_primary=initial['primary'],corrected_graph=info(v2path),original_negative_preserved=True,all_inputs_rehashed=True,theorem_credit=False))
for n in ['source-topology-decision97.native.json','closed-RAW-topology97.native.json']:print(json.dumps(info(O/n)),flush=True)
