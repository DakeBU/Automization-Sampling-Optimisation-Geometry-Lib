"""Distinct exact one-line syntax-overlay review and corrected source-header scope."""
from pathlib import Path
import json,hashlib,datetime,copy
ROOT=Path('E:/Samplinglib')
BASE='runs/20261007-companion-priority/pbps-outer-bounded-l2-preread84/header-source-review84/'
R84='runs/20261007-companion-priority/pbps-actual-outer-bounded-l2-continuity84/'
OUT=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=(ROOT/p).read_bytes();return {'path':p,'raw_sha256':sha(b),'bytes':len(b)}
oldpath=R84+'header84.proposed.lean'
newpath=R84+'header-review84/header84.syntax-only-proposed.lean'
proposalpath=R84+'header-review84/syntax-only-proposal84.json'
diffpath=R84+'header-review84/syntax-only-proposed84.diff'
expected={oldpath:'936b76036df8d283acb212f2f1ba780c4446aa2e1c7dc84bfdff0ff9c02f29b0',
 newpath:'5c4e379caa337d1ac903d509eca30ef7db7b1905715c7a65b878afb33f9d2ded',
 proposalpath:'5fc600eabd3c091a9a54be81872287279dc0d8102b8c660eb06f9038c715752e',
 diffpath:'9db04c8db83e7ed93d3e23c57819feb2209648e30a04c99d3c77e40308294f32',
 BASE+'header-source.decision84.json':'1f8fbec04806e6d565f6e055d013e05c88af01a8fb62e4624f89339d63c7c560',
 BASE+'header-source.run-evidence84.json':'beff9e6f0d19409781c14d4217f62b025bc625ed42037325db38f5dc1f3f21eb',
 BASE+'header-source.run-manifest84.json':'86ffe52f57c004744b68b6aa22e27b799d01a86d10c6208f448fe423436c7d4f'}
for p,v in expected.items():assert pin(p)['raw_sha256']==v,p
original=json.loads((ROOT/(BASE+'header-source.decision84.json')).read_bytes())
original_evidence=json.loads((ROOT/(BASE+'header-source.run-evidence84.json')).read_bytes())
original_manifest=json.loads((ROOT/(BASE+'header-source.run-manifest84.json')).read_bytes())
for x in original_manifest['raw_inputs']+original_manifest['raw_outputs']:
 assert pin(x['path'])==x,('original raw input/output mutated',x['path'])
old=(ROOT/oldpath).read_bytes();new=(ROOT/newpath).read_bytes()
ol=old.splitlines(keepends=True);nl=new.decode().splitlines()
assert len(old)==7652 and len(new)==7616
assert len(ol)==128 and len(nl)==127
assert ol[110]==b'set_option maxHeartbeats 1600000 in\n'
assert b''.join(ol[:110]+ol[111:])==new
assert old.count(b'set_option maxHeartbeats 1600000 in')==1
assert b'set_option maxHeartbeats 1600000 in' not in new
proposal=json.loads((ROOT/proposalpath).read_bytes())
assert proposal['proposer']=='/root/exact_verify77'
assert proposal['original_RAW_sha256']==sha(old)
assert proposal['exact_proposed_RAW_sha256']==sha(new)
assert proposal['exact_proposed_RAW_bytes']==7616
assert proposal['mathematical_clause_or_binder_change'] is False
assert proposal['new_proof_or_premise'] is False
assert len(original['inventory_coverage'])==47
assert len(original['source_graph_coverage']['nodes'])==23
assert len(original['source_graph_coverage']['relations'])==39
assert original['source_scope_verdict']=='FAITHFUL_BOUNDED_ASTIS_ELABORATION'
assert [d['id'] for d in original['deltas'] if d['blocking']]==['H84-SYNTAX-001']

# Exact byte deletion is the whole transformation: every source mapping is reused,
# with the deterministic one-line position shift and no mathematical interpretation change.
def shift_line(n):
 assert n!=111,'Mapping unexpectedly treats removed command as a mathematical obligation'
 return n-1 if n>111 else n
items=copy.deepcopy(original['inventory_coverage'])
for x in items:x['header_lines']=[shift_line(n) for n in x['header_lines']]
graph=copy.deepcopy(original['source_graph_coverage'])
for x in graph['nodes']:x['header_lines']=[shift_line(n) for n in x['header_lines']]
for x in graph['relations']:x['header_target_lines']=[shift_line(n) for n in x['header_target_lines']]
regions=copy.deepcopy(original['whole_header_coverage']['regions'])
for x in regions:
 a=x['start_line'];b=x['end_line']
 x['start_line']=a-1 if a>111 else a
 x['end_line']=b-1 if b>=111 else b
 if x['region_id']=='H84-10':x['assessment']='Blank separation and final conjunction preserved after exact standalone-command deletion'
 x['line_code_utf8_lf_sha256']=sha(('\n'.join(nl[x['start_line']-1:x['end_line']])+'\n').encode())
flat=[n for r in regions for n in range(r['start_line'],r['end_line']+1)]
assert sorted(flat)==list(range(20,125)) and len(flat)==len(set(flat))
slots=copy.deepcopy(original['semantic_slots'])
slots['scopes']={'original':original['semantic_slots']['scopes']['original'],
 'reconstructed':'Corrected whole private Prop excludes all-L2 AE operator/invariance/Jensen/contraction/density/Markov/main/cost. Exact one-line standalone-command deletion joins the retained83 contract to the new final conjunct without changing any mathematical clause.',
 'evidence':'Prospective corrected header5c4e379c...7616bytes equals original RAW936b7603 minus only original line111. Exhaustive47item/23node/39relation source mapping is unchanged modulo deterministic line shift. FutureOPEN5 dependencies and2 excluded associations remain.',
 'relation':'equivalent-after-elaboration'}
for name,s in slots.items():
 if name!='scopes':
  s['evidence']+=' Evidence line references in this slot describe original header; exact corrected references appear in exhaustive remapped coverage.'
independence={**original['independence'],
 'exact_syntax_overlay_proposer':False,
 'distinct_exact_overlay_proposer':'/root/exact_verify77',
 'scope':'Distinct exact syntax-only overlay review plus whole corrected prospective source-header scope; no BODY/proof or source-completion verdict.',
 'source_first':'Same closed primary-first header review continued: full pinned source/47item/23node/39relation mapping was completed before exact syntax proposal read.',
 'other_math_or_header_reviewer_verdicts_read':False,
 'native_typecheck_claim':'No compiler/typecheck acceptance claimed by this source reviewer; handled separately by independent mathematics/typechecker.',
 'writes':'Append-only owned header-source-review84 outputs; original review/header/freeze unchanged.'}
raw_inputs=copy.deepcopy(original_evidence['raw_inputs'])
for p in expected:
 if not any(x['path']==p for x in raw_inputs):raw_inputs.append(pin(p))
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
operation={'id':'S84-SYNTAX-DELETE-001','operation':'delete_exact_original_line','original_line':111,
 'deleted_utf8':'set_option maxHeartbeats 1600000 in\n','deleted_bytes':36,
 'decision':'ACCEPT_EXACT_SYNTAX_ONLY_PATCH','blocking':False,
 'reason':'Removes only an accidental standalone command between Prop conjuncts. All other bytes, including every source assumption, actual definition, quantifier, conclusion and exclusion, are unchanged.',
 'source_semantics_changed':False,'proof_or_premise_added':False}
evidence={'schema':'astis.corrected-prospective-header-source-review84.run-evidence.v1','status':'closed','created_utc':now,
 'raw_inputs':raw_inputs,'original_header_raw_sha256':sha(old),'corrected_header_raw_sha256':sha(new),
 'exact_repair_proposal_raw_sha256':pin(proposalpath)['raw_sha256'],
 'exact_diff_raw_sha256':pin(diffpath)['raw_sha256'],
 'exact_patch_operations':[operation],
 'checks':{'exact_delete_original_line111_only':True,'all_other_bytes_identical':True,
  'mathematical_binders_definitions_conclusions_and_boundaries_unchanged':True,
  'all47inventory23nodes39relations_mapped':True,'future_open_dependencies':5,'excluded_associations':2,
  'normalization_complete_routes_OR_preserved':True,'internal_required_AND_preserved':True,
  'whole_corrected_private_prop_coverage_no_gap_or_overlap':True,'original_review_and_header_and_freeze_raws_unchanged':True},
 'source_anchor_pins_from_closed_primary_first_run':original_evidence['all_frozen_primary_anchor_hashes_match'],
 'independence':independence,
 'noncircularity':'This evidence does not include corrected decision/manifest hashes. Corrected decision binds exact evidence RAW; final manifest binds outputs and omits own hash.'}
def emit(n,obj):
 p=OUT/n;assert not p.exists(),p;p.write_bytes((json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode())
emit('header-source.corrected-run-evidence84.json',evidence)
decision={'schema':'astis.corrected-prospective-whole-header-source-review84.v1','status':'closed','created_utc':now,
 'verdict':'ACCEPT_PROSPECTIVE_HEADER_SOURCE_SCOPE',
 'repair_verdict':'ACCEPT_EXACT_SYNTAX_ONLY_PATCH',
 'verdict_reason':'The distinct proposed one-line deletion repairs the only identified exact-header blocker and changes no mathematics. The entire corrected private Prop faithfully retains actual83 and adds the exact normalized phase-law bounded C_b squared-integral DCT ingredient, with every scoped source item/edge and OPEN boundary preserved.',
 'exact_original_header_raw_sha256':sha(old),'exact_reviewed_corrected_header_raw_sha256':sha(new),
 'exact_reviewed_corrected_header_bytes':7616,
 'primary_raw_sha256':original['primary_raw_sha256'],
 'original_closed_review_raw_sha256':pin(BASE+'header-source.decision84.json')['raw_sha256'],
 'review_run_sha256':sha((OUT/'header-source.corrected-run-evidence84.json').read_bytes()),
 'semantic_slots':slots,'per_patch_acceptance':[operation],
 'deltas':[d for d in original['deltas'] if not d['blocking']]+[
  {'id':'H84-SYNTAX-CLOSED-004','slot':'scopes','classification':'DISTINCT_REVIEWED_SYNTAX_ONLY_REPAIR','blocking':False,
   'description':'Original H84-SYNTAX-001 is resolved only for exact corrected RAW5c4e379c...; original header936b7603 and its negative prospective decision remain immutable.'}],
 'blocking_deltas':[],'additional_required_repairs':[],'no_required_mathematical_repairs':True,
 'inventory_coverage':items,'source_graph_coverage':graph,
 'whole_header_coverage':{'expected_private_prop_lines':[20,124],'regions':regions,'gaps':[],'overlaps':[],
  'body_reviewed':False,'body_exists_claimed':False},
 'truth_boundary':original['truth_boundary'],
 'source_scope_ready_for_separate_owner_statement_seal':True,
 'statement_seal_or_proof_state_written':False,
 'source_completion_credit':False,'proof_or_verification_credit':False,
 'independence':independence}
emit('header-source.corrected-decision84.json',decision)
outputs=['review_syntax_successor84.py','header-source.corrected-run-evidence84.json','header-source.corrected-decision84.json']
manifest={'schema':'astis.corrected-prospective-header-source-review84.raw-manifest.v1','status':'closed','created_utc':now,
 'raw_inputs':raw_inputs,'raw_outputs':[pin((OUT/n).relative_to(ROOT).as_posix()) for n in outputs],
 'selfhash_convention':'Omit own hash. Exact evidence -> corrected decision -> manifest bindings are acyclic; external report pins final manifest RAW.',
 'owned_directory':OUT.relative_to(ROOT).as_posix(),'original_artifacts_unchanged':True,
 'no_production_header_or_state_mutation':True,'source_completion_credit':False}
emit('header-source.corrected-run-manifest84.json',manifest)
print(json.dumps({'verdict':decision['verdict'],'repair_verdict':decision['repair_verdict'],
 'outputs':[pin((OUT/n).relative_to(ROOT).as_posix()) for n in outputs+['header-source.corrected-run-manifest84.json']]},indent=2))
