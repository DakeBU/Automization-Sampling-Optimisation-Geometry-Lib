from pathlib import Path
import datetime, hashlib, importlib.util, json, re, subprocess, sys
R=Path('E:/Samplinglib'); O=Path(__file__).parent; B=O.parent
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
 p=Path(p); b=p.read_bytes(); return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def read(p): return json.loads(Path(p).read_text('utf8'))
def put(n,d):
 with (O/n).open('x',encoding='utf8',newline='\n') as f: json.dump(d,f,ensure_ascii=False,indent=2); f.write('\n')
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryTailLaw.lean'; mr='01fcff944f1dbd42be2af30063b9baf4e191e2cde959e008724387cadb4fc899'
assert pin(M)['raw_sha256']==mr
original=read(O/'input-freeze87.json')
for i in original['actual_inputs']: assert pin(R/i['path'])==i
for i in read(O/'collaborator-preservation87.json')['RAWs']: assert pin(R/i['path'])==i
for name in ['fresh-focused-build','fresh-whole-source-kernel']:
 d=read(O/(name+'.receipt.json')); assert d['exit_code']==0,d
log=(O/'fresh-whole-source-kernel.stdout.log').read_text('utf8')
ax=re.search(r'depends on axioms:\s*\[([^]]+)\]',log,re.S); assert ax
axioms=sorted(x.strip() for x in ax.group(1).split(',')); assert axioms==sorted(['propext','Classical.choice','Quot.sound']),axioms
def marks(prefix): return sorted(set(x[len(prefix)+1:].strip() for x in log.splitlines() if x.startswith(prefix+' ')))
local=marks('LOCAL_PROOF_CONSTANT'); external=marks('EXTERNAL_ASTIS_DEPENDENCY'); trans=marks('TRANSITIVE_ASTIS_CONSTANT'); generic=marks('GENERIC_DEPENDENCY')
le=marks('LOCAL_EDGE'); te=marks('TRANSITIVE_ASTIS_EDGE')
assert not marks('LOCAL_NO_VALUE') and not marks('PROJECT_NO_VALUE')
public=[n for n in external if not n.startswith('_private.')]
expected=['AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion','AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws']
assert public==sorted(expected)
put('kernel-dependency-summary87.json',dict(status='ACCEPTED_ELABORATED_TYPE_AND_VALUE_ASTIS_CLOSURE',reviewer_id='/root/exact_verify77',module=pin(M),probe=pin(O/'FreshWholeSourceKernelClosure87.lean'),native_log=pin(O/'fresh-whole-source-kernel.stdout.log'),standard_axioms_only=True,axioms=axioms,local_proof_constant_count=len(local),local_proof_constants=local,immediate_ASTIS_dependency_count=len(external),immediate_ASTIS_dependencies=external,immediate_public_theorem_parents=public,transitive_ASTIS_constant_count=len(trans),transitive_ASTIS_constants=trans,unique_owned_edges=le,unique_transitive_ASTIS_edges=te,unique_owned_edge_count=len(le),unique_transitive_ASTIS_edge_count=len(te),generic_immediate_constant_count=len(generic),generic_immediate_constants=generic,method='Traverse both elaborated ConstantInfo.type and actual value including generated private proof constants, recursively through all project constants. Generic Mathlib constants are recorded where used by owned constants; not a recursive enumeration of all Mathlib internals.',parent_number_clarification='ActualFiniteJumpRecursion is producer76, not ActualNonaccumulation78; exact compiled constants are authoritative.'))
bindings=[]
for n in trans:
 tokens=n[n.find('AutoSamplingTheory.'):].split('.')
 hits=[]
 for k in range(2,len(tokens)+1):
  p=R.joinpath(*tokens[:k]).with_suffix('.lean')
  if p.is_file(): hits.append(p)
 assert hits, n
 bindings.append(dict(constant=n,source=pin(hits[-1])))
sourcepins={i['source']['path']:i['source'] for i in bindings}
put('transitive-kernel-source-binding87.json',dict(status='ALL_TRANSITIVE_PROJECT_CONSTANTS_BOUND_TO_EXISTING_SOURCE',module=pin(M),bindings=bindings,distinct_project_source_files=list(sourcepins.values()),source_file_count=len(sourcepins),compiled_olean_caveat='The full current target source is freshly elaborated. Imported parents use their pinned current compiled artifacts in the successful fixed lake build; source hashes accompany the actual kernel dependency closure.'))
sys.path.insert(0,str(R/'tools'))
import astis
hits=astis.forbidden_pattern_hits(); assert not hits,hits
put('fake-closure-scan87.json',dict(status='PASS',utc=now(),reviewer_id='/root/exact_verify77',module=pin(M),scanner=pin(R/'tools/astis.py'),method='tools.astis.forbidden_pattern_hits() repository Lean scan plus elaborated theorem standard-axiom check',hits=hits,standard_axioms_only=True,axioms=axioms))
lesson=R/'website/content/declaration_lessons/pbps-actual-finite-history-tail-law.json'; publication=R/'website/content/publications/pbps-actual-finite-history-tail-law.json'; freeze=B/'publication-freeze87.json'
pf=read(freeze)
for p in [lesson,publication]: assert pin(p) in pf['inputs']
snap=[]
for p,name in [(lesson,'lesson87.original.exactraw.json'),(publication,'publication87.original.exactraw.json')]:
 with (O/name).open('xb') as f:f.write(p.read_bytes())
 snap.append(dict(original=pin(p),immutable_snapshot=pin(O/name)))
put('original-exposition-snapshot-index87.json',dict(created_utc=now(),original_freeze=pin(freeze),snapshots=snap,reason='Original draft inputs retained before any independently reviewed successor repair; do not require old locations to retain historical bytes after an explicit successor.'))
u=read(lesson)['units'][0]; pub=read(publication)['items'][0]; steps=u['steps']; assert len(steps)==6
lines=M.read_bytes().splitlines(keepends=True); regions=[]
for i,s in enumerate(steps):
 reg=s['lean_source_region']; a,z=reg['start_line'],reg['end_line']; raw=b''.join(lines[a-1:z]); assert reg['source_raw_sha256']==mr; assert hashlib.sha256(raw).hexdigest()==reg['exact_code_raw_sha256']; assert raw.decode()==s['lean']
 if i: assert a==regions[-1]['end_line']+1
 regions.append(dict(step=i+1,**reg))
assert regions[0]['start_line']==87 and regions[-1]['end_line']==237
assert u['statement']==u['lean_statement']==pub['statement'] and u['assumptions']==pub['assumptions']
assert list(u['astis_dependencies'])==expected
repairs=[dict(target=pin(lesson),pointer='/units/0/steps/1/formula',before=steps[1]['formula'],after=r"w|_{[0,n)}=w\prime|_{[0,n)}\Longrightarrow H_n(w)=H_n(w\prime),\quad H_n\text{ and }Y_n\text{ are ambient Borel measurable}.",reason='This contiguous region proves prefix causality and ambient measurability only. Past-sigma measurability requires truncation/factorization in steps3–4; do not state it before its matching BODY region.'),dict(target=pin(publication),pointer='/items/0/purification/duplicate_semantics_audit',before=pub['purification']['duplicate_semantics_audit'],after=pub['purification']['duplicate_semantics_audit'].replace('already78','already76'),reason='Actual finite-recursion producer is76, matching the actual compiled public constant;78 is nonaccumulation.'),dict(target=pin(publication),pointer='/items/0/purification/canonicalization',before=pub['purification']['canonicalization'],after=pub['purification']['canonicalization'].replace('actual78 recursion','actual76 recursion'),reason='Same exact producer identity correction; no theorem/source/BODY change.')]
assert all(x['before']!=x['after'] for x in repairs)
put('proposed-exposition-overlay87.json',dict(status='PROPOSED_EXPOSITION_ONLY_REQUIRES_DISTINCT_EXACT_REVIEW',created_utc=now(),proposer_id='/root/exact_verify77',module=pin(M),original_freeze=pin(freeze),original_snapshot_index=pin(O/'original-exposition-snapshot-index87.json'),changes=repairs,required_changes=3,Lean_statement_BODY_change=False,decoded_TeX_backslashes='Independently checked decoded strings, all command backslashes single; no escaping proposal or repair.',not_self_approved=True))
put('exposition-original-review87.json',dict(status='MATHEMATICS_ACCEPTED_THREE_EXPOSITION_METADATA_FIELDS_REQUIRE_DISTINCT_OVERLAY_REVIEW',module=pin(M),draft_inputs=[pin(lesson),pin(publication),pin(freeze)],exhaustive_contiguous_public_BODY_regions=regions,entire_BODY_covered=True,statement_assumptions_and_actual_definitions_complete=True,accepted_explanation=['Six analytic hypotheses and literal guarded stopped recursion are fully restated.','Raw tail n+k starts at source E_(n+1); Fin(n+1) history consumes only k<n.','Truncation is solely a measurable factorization; original recursion/input law preserved.','Past/future sigma algebra distinction and whole countable tail are explained.','Unnormalized restriction identity includes zero-probability events, without dividing by an event or point probability.','n=0, stopped/infinite wait, zero normals/rates and rank0 allowed; random depth/residual restart/fullA7 remain open.'],required_repairs=pin(O/'proposed-exposition-overlay87.json'),no_final_source_or_blind_verdict_read=True))
print(json.dumps(dict(owned=len(local),immediate=len(external),public_parents=public,transitive=len(trans),transitive_edges=len(te),owned_edges=len(le),generic=len(generic),sourcefiles=len(sourcepins),exposition_repairs=3),indent=2))
