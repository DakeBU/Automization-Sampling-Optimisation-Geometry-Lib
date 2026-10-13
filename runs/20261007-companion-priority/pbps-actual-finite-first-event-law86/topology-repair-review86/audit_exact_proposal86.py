from pathlib import Path
import datetime, hashlib, json, subprocess

R = Path('E:/Samplinglib')
O = Path(__file__).parent
S = R/'runs/20261007-companion-priority/pbps-actual-finite-first-event-law86/independent-source86'
B = R/'runs/20261007-companion-priority/pbps-path-law-preread86'
now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
def raw(p):
    b = p.read_bytes()
    return dict(path=p.relative_to(R).as_posix(), raw_sha256=hashlib.sha256(b).hexdigest(), bytes=len(b))
def read(p): return json.loads(p.read_text('utf-8'))
def write(name, obj):
    with (O/name).open('x', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2); f.write('\n')

pins = {
 'topology-additive-proposal86.json':'2bf3b9eaf3a0e1adf87d67286a5c27cf9362d977c70f501b2f12644399891d20',
 'source-proof-graph86.exhaustive-successor.json':'7a8311d827023c26059618345872987308e854b274e1c13c51bb5c05a987974d',
 'source-inventory86.exhaustive-successor.json':'cd5f487c3091946ab0699c4c50203a1703ff8b6e0f44a67cfa86920c9a26db3f',
 'topology-successor-freeze86.json':'f87a1a879c48d23cd6adfbce97e198f1b269766db5af479dde7200e7f2218488'}
for n,h in pins.items(): assert raw(S/n)['raw_sha256']==h
g=read(S/'source-proof-graph86.exhaustive-successor.json')
i=read(S/'source-inventory86.exhaustive-successor.json')
og=read(B/'source-proof-graph86.reviewed-effective.json')
oi=read(B/'source-inventory86.reviewed-effective.json')
assert raw(B/'source-proof-graph86.reviewed-effective.json')['raw_sha256']=='e13eb32c3b941ba7df6a9b10b804b156877af76e74bf283a3c109670a6518fb2'
assert raw(B/'source-inventory86.reviewed-effective.json')['raw_sha256']=='f389f21eedbcff89ccb04ac68893e900a98a9f702b9247f8046e98d4baf0f53a'

# Reuse the already frozen independent parser CLASS, without running its output
# code. Add exact proposition leaf paragraphs for post-proposal coverage readback;
# the entire containing proposition was already read before proposal access.
parser_source=(O/'read_primary_first86.py').read_text('utf-8').split('p=Reader();')[0]
parser_source=parser_source.replace("if paragraph or eq or background:", "if paragraph or eq or background or re.fullmatch(r'A1\\.(?:Thmtheorem1|I1\\.i[123])\\.p1\\.[12]',i):")
ns={ '__file__': str(O/'read_primary_first86.py') }
exec(compile(parser_source, 'independent_source_parser_postproposal', 'exec'), ns)
p=ns['Reader'](); p.feed(ns['raw'].decode('utf-8'))
records=p.records
atomic={x['id']: x for x in records if x['scope']=='SS1' and x['id']!='A1.Thmtheorem1'}
assert len(atomic)==72, (len(atomic), list(atomic))
write('.private.postproposal-atomic-readback86.json', dict(created_utc=now(), chronology='POST_PROPOSAL_COVERAGE_CHECK; original entire proposition and SS1 readback was frozen first', records=list(atomic.values())))
dis={a['anchor']:a for a in i['atomic_dispositions']}
assert set(dis)==set(atomic), (set(dis)-set(atomic),set(atomic)-set(dis))
itemmap={x['id']:x for x in i['items']}
for a,d in dis.items():
    assert d['inventory_ids']
    for ident in d['inventory_ids']: assert a in itemmap[ident]['source_ids']
for a in i['anchors']:
    candidates={x['id']:x for x in records}
    assert a['source_id'] in candidates
    assert a['normalized_anchor_sha256']==candidates[a['source_id']]['normalized_sha256'], a
for key in ['nodes','edges']:
    assert g[key][:len(og[key])]==og[key], key
assert g['junctions']==og['junctions']
assert i['items'][:len(oi['items'])]==oi['items']
assert i['source_gaps']==oi['source_gaps']
assert i['anchors']==oi['anchors']
assert (len(g['nodes']),len(g['edges']),len(i['items']))==(38,75,47)
deps=[e for e in g['edges'] if e['dependency_edge']]
assert len(deps)==72
assert len(g['edges'])-len(deps)==3
ids={n['id'] for n in g['nodes']}
for e in g['edges']: assert e['from'] in ids and e['to'] in ids
seen={'G86-08'}
for _ in range(len(ids)): seen|={e['to'] for e in deps if e['from'] in seen}
assert 'G86-38' not in seen
incoming=[e for e in deps if e['to']=='G86-38']
assert {e['from'] for e in incoming}=={'G86-25','G86-27','G86-29','G86-33'}
pending=set(ids); done=set()
while pending:
    ready={n for n in pending if all(e['from'] in done for e in deps if e['to']==n)}
    assert ready, 'cycle'
    done|=ready; pending-=ready

overlay=dict(schema='astis.independent.strict-topology-repair-proposal.v1',status='PROPOSED_REQUIRES_DISTINCT_REVIEW_NOT_APPLIED',reviewer_id='/root/exact_verify77',created_utc=now(),target=raw(S/'source-proof-graph86.exhaustive-successor.json'),operations=[dict(op='append-edge',collection='edges',value=dict(id='E86-R76', **{'from':'G86-08','to':'G86-38'},classification='FUTURE_SOURCE_INGREDIENT',route='L2_EXTENSION_AND_GAUSSIAN_AVERAGING',dependency_edge=True,consumer_use_site='A1.SS1.SSS0.Px1.p7.2; A1.I1.i3.p1.1',reason='The actual jointly Borel phase evaluated under its probability input yields a fixed-time positive, constant-preserving expectation operator. Gaussian lift and averaging preserve positivity and constants. Together with the four other incoming ingredients (AND), this supplies the inherited Markov part of the averaged operator. Consume the actual phase/probability-law component of G86-08; a typed kernel representation is optional. This does not require or prove memorylessness, restart, Chapman-Kolmogorov, or a position semigroup. The AE-safe L2 descent still requires the invariant-law/Jensen component G86-27; all global conclusions remain OPEN.')))],expected_counts=dict(nodes=38,relations=76,dependency_edges=73,excluded_associations=3),invariants=['Do not alter original frozen proposal/successors or existing 75 relations.','No new mathematical hypothesis, source assumption, Lean theorem, or completion credit.','Five incoming route ingredients are jointly required, not alternatives.','G86-31 remains separately OPEN; no G86-08 to G86-31 implication is introduced.'],rationale='The exact proposal itself says transition-probability Markov property remains required in E86-A73, but G86-08 is neither a direct nor transitive dependency of G86-38. Selfadjointness and L2 contraction cannot supply positivity/T1=1. A single use-site edge is the smallest repair using existing nodes.')
write('minimal-strict-overlay86.json',overlay)
evidence=dict(status='COMPLETED_INDEPENDENT_EXACT_PROPOSAL_AUDIT',reviewer_id='/root/exact_verify77',created_utc=now(),observed_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),chronology=[dict(order=1,event='Independently read full primary SS1 and entire proposition plus standing context; froze reconstruction before new proposal access.',artifact=raw(O/'primary-first-synthesis86.json'),native_freeze_utc=read(O/'primary-first-synthesis86.json')['created_utc']),dict(order=2,event='Renamed long original readback .private.* byte-exact before proposal access; retained classification diagnosis; excluded private extracts from staging.'),dict(order=3,event='Read only authorized exact proposal, graph successor, inventory successor, and freeze; no source verdict/renderer/root adoption read.'),dict(order=4,event='Post-proposal exact 72-atom enumeration; five proposition leaf paragraphs supplement the previously read containing proposition. No claim that this later leaf enumeration preceded proposal.')],coverage=dict(independent_atoms=72,table_or_paragraph_leaf_atoms=sum(x['tag']!='tbody' for x in atomic.values()),equation_row_anchors=sum(x['tag']=='tbody' for x in atomic.values()),all_atomic_dispositions_exact=True,all_56_legacy_anchor_normalized_hashes_match=True,original_37_nodes_71_relations_40_items_preserved=True,original_source_gaps_and_OR_junctions_preserved=True,successor_counts=dict(nodes=38,relations=75,dependency_edges=72,excluded_associations=3,inventory_items=47),atomic_checks=[dict(source_id=a,normalized_sha256=atomic[a]['normalized_sha256'],disposition=dis[a]['disposition'],inventory_ids=dis[a]['inventory_ids']) for a in sorted(atomic)]),mathematical_findings=[dict(id='F1',status='ACCEPT_BOUNDED_ADDITIONS',finding='Heuristic p1.1-p1.6/Ex12-17 are explicitly excluded as an unjustified formal generator/exponentiation route, preserving the source discontinuity/domain warning. They are covered without being a sufficient rigorous OR branch.'),dict(id='F2',status='ACCEPT_BOUNDED_ADDITIONS',finding='Full proposition, Gaussian p7.1/Ex23/p7.2, literal flow/bounce and phase-law notation are now explicitly covered. A3 extension needs reversal, contraction/boundedness, and independent density. Gaussian evenness and lift/average adjointness support R cancellation; exact q times Gaussian context is retained.'),dict(id='F3',status='REQUIRED_REPAIR',finding='New G86-38 has no actual phase probability-law ancestor. E86-A73 prose names the missing Markov ingredient but no edge consumes it. L2 selfadjointness plus contraction does not imply positivity or T1=1.',exact_missing_use_site='A1.SS1.SSS0.Px1.p7.2',repair='minimal-strict-overlay86.json'),dict(id='F4',status='ACCEPT_BOUNDARIES',finding='Conditional unused-tail laws, A7 residual survival/path summability/reversal/invariance/Jensen/density/full semigroup remain OPEN. Fixed-time Markov-operator inheritance does not require CK, does not prove process Markov, and does not make typed-kernel representation logically necessary.')],remaining_obligations=['Distinct exact review of this minimal single-edge proposal before application.','Retain all future OPEN analytic/path/operator obligations; first-event86 has no full-path/Markov/invariance credit.'],exclusions=['No final/provisional source86 verdict, renderer review, root source adoption, decoder or production BODY used for this topology review.','The reviewer previously reviewed the full Lean proof in a separate role; this is not a source-blind decoder or claim of never having seen implementation.','Full source extracts are private excluded artifacts; public audit carries hashes and paraphrases only.'])
write('evidence86.json', evidence)
write('decision86.json',dict(status='REJECT_EXACT_PROPOSAL_PENDING_MINIMAL_DEPENDENCY_REPAIR',reviewer_id='/root/exact_verify77',created_utc=now(),scope='Independent source-only exact additive topology proposal review; no canonical application or theorem acceptance.',checked_proposal=raw(S/'topology-additive-proposal86.json'),checked_graph=raw(S/'source-proof-graph86.exhaustive-successor.json'),checked_inventory=raw(S/'source-inventory86.exhaustive-successor.json'),checked_freeze=raw(S/'topology-successor-freeze86.json'),accepted_components=['72 atomic source coverage and all 56 legacy normalized pins','Original nodes/edges/items/gaps/AND-OR unchanged','Explicit heuristic exclusion and final Gaussian averaging source coverage','Future OPEN boundaries preserved'],required_repairs=[dict(id='R86-MARKOV-USE-SITE',target='G86-38 incoming dependencies',proposal=raw(O/'minimal-strict-overlay86.json'),distinct_review_required=True)],evidence=raw(O/'evidence86.json'),truth_boundary='No VERIFIED transition, source final verdict, statement/proof repair, or whole-paper/Goal completion.'))
print(json.dumps(dict(status='AUDIT_COMPLETED_WITH_EXPLICIT_BLOCKER',atoms=72,original_preserved=True,missing='Actual phase probability-law use-site edge for G86-38',decision=raw(O/'decision86.json'),overlay=raw(O/'minimal-strict-overlay86.json'))))
