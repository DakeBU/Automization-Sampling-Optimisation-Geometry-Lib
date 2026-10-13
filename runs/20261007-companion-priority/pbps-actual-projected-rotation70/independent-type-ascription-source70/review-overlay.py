import base64,datetime,hashlib,json,os,pathlib,re
out=pathlib.Path(__file__).resolve().parent;repo=out.parents[3]
diag=out.parent/'compiler-diagnosis70'
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda n:json.loads((out/n).read_bytes())
manifest=load('input-manifest.initial.json');inputs=manifest['inputs']
for p,n in [(diag/'header-type-ascription70.proposal.json','overlay.proposal.RAW.json'),
            (diag/'header-type-ascription70.proposed.lean','overlay.proposed-header.RAW.lean')]:
    b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');(out/n).write_bytes(b);(out/(n+'.LF')).write_bytes(lf)
    inputs.append(dict(original_path=p.as_posix(),name=n,RAW_bytes=len(b),RAW_sha256=sha(b),LF_bytes=len(lf),LF_sha256=sha(lf),LF_recipe='CRLF-to-LF only'))
original=(out/'original-sealed-header.RAW.lean.LF').read_bytes()
candidate=(out/'overlay.proposed-header.RAW.lean.LF').read_bytes()
proposal=load('overlay.proposal.RAW.json')
assert sha(candidate)==proposal['proposed_header_RAW_sha256']=='7269efa8dcae309de6761e32d0b8d8608d046fe612fbc9628f594e11a4a578e5'
assert sha(original)==proposal['original_header_RAW_sha256']=='9261f488432664370ae1b1146b098bf86c17dfd476bfe2e149d3024a77529e19'
old_lines=original.splitlines(keepends=True);new_lines=candidate.splitlines(keepends=True)
assert len(old_lines)==116 and len(new_lines)==118
assert old_lines[:9]==new_lines[:9]
assert new_lines[9]==b'    (show Prop from\n' and new_lines[-1]==b'    )\n'
assert all(line.startswith(b'  ') for line in new_lines[10:-1])
recovered=b''.join(new_lines[:9]+[line[2:] for line in new_lines[10:-1]])
assert recovered==original
(out/'inverse-transformed-exact-original-header.LF.lean').write_bytes(recovered)
assert candidate==b''.join(old_lines[:9]+[b'    (show Prop from\n']+[b'  '+line for line in old_lines[9:]]+[b'    )\n'])
assert not any(x in candidate for x in [b'private ',b':= by',b'sorry',b'axiom '])
common_witnesses=['S','e','U','T','Γ','q','ΓP0','Inv','A0','B0','V0','R']
forall_public=original.decode('utf-8').splitlines()[:9]
assert all(('∃ '+name+' :') in original.decode('utf-8') for name in common_witnesses)
old_dir=repo/'runs/20261007-companion-priority/pbps-actual-projected-rotation-preproof70/independent-header-source70'
old_manifest=load('prior-CLOSED83.manifest.RAW.json');old_lease=load('prior-CLOSED83.lease.RAW.json')
assert len(old_manifest['regular_file_entries'])==81
for e in old_manifest['regular_file_entries']:
    b=(old_dir/e['name']).read_bytes()
    assert len(b)==e['RAW_bytes'] and sha(b)==e['RAW_sha256']
    assert sha(b.replace(b'\r\n',b'\n'))==e['LF_sha256']
assert sha((old_dir/'owned-manifest.json').read_bytes())==old_lease['manifest_RAW_sha256']
assert len([p for p in old_dir.iterdir() if p.is_file()])==83
coverage=load('prior-source-coverage.RAW.json')
assert coverage['source_math']==419 and coverage['source_NODE']==173 and coverage['source_EXCLUDED']==246
line_map=[dict(original_line=i+1,candidate_line=i+1 if i<9 else i+2,
    classification='identical public binder/name line' if i<9 else 'same exact return-type line plus two leading spaces',
    original_LF_sha256=sha(line),candidate_LF_sha256=sha(new_lines[i if i<9 else i+1])) for i,line in enumerate(old_lines)]
checks=[
 dict(id='TA70-1',decision='PASS',field='sealed baseline/provenance',evidence='CLOSED83 lease/manifest and all81 regular RAW/LF entries verify; baseline RAW9261... and root StatementSeal70 match.'),
 dict(id='TA70-2',decision='PASS',field='six public callers and public representation',evidence='Original lines1-9 are byte-identical. Same theorem name and expanded public return; no privateProp/provider or new premise.'),
 dict(id='TA70-3',decision='PASS',field='entire return type exact inverse',evidence='Candidate line10 is the outer show-Prop opener,118 the one new closer. Candidate11-117 undoing two leading spaces restores original10-116 exactly, including all parentheses and line endings after CRLF-only mapping.'),
 dict(id='TA70-4',decision='PASS',field='same witnesses/domains/formulas/quantifiers',evidence='Complete whole-header equality after inverse transform preserves all12 common witnesses, every69 conclusion, centered gP/actual gV, exact signed rotation and norm-square sum; rank0/alphaeta1/no ontoV remain unchanged.'),
 dict(id='TA70-5',decision='PASS_RETAIN_OBLIGATION',field='source primary-first obligations',evidence='Reuse original419 items/7regions/22nodes49edges; mean_g remains an internal proof obligation from SAME U/P integral preservation. No new source claim or caller.'),
 dict(id='TA70-6',decision='PASS_WITH_NO_COMPILER_CREDIT',field='compiler and BODY boundary',evidence='Header-only comparison; no BODY is contained in the candidate. Proposal BODY hash609dc... is recorded without reading/reviewing BODY. Root reports diagnostic39696 EXIT1, same unknown free variable before first tactic. Ascription did not fix the reported failure and no elaboration theorem is certified.')]
decision=dict(schema='astis-type-ascription70-independent-source-overlay-decision-v1',owner='/root/independent_primary69',
    verdict='ADMIT_SOURCE_REPRESENTATION_EQUIVALENCE_ONLY_NOT_COMPILER_REPAIR',actual_review_pid=os.getpid(),
    expectations_frozen_before_overlay_RAW_sha256=sha((out/'expectations.before-overlay.json').read_bytes()),
    original_header_RAW_sha256=sha(original),proposed_header_RAW_sha256=sha(candidate),proposal_RAW_sha256=sha((out/'overlay.proposal.RAW.json').read_bytes()),
    prior_CLOSED83_lease_RAW_sha256=sha((out/'prior-CLOSED83.lease.RAW.json').read_bytes()),old_CLOSED83_all83_unchanged=True,
    exact_inverse_recovers_original_header=True,public_header_lines_original=116,public_header_lines_proposed=118,
    preserved_public_conditions=6,preserved_common_witnesses=common_witnesses,missing_or_extra_public_premises=0,
    original_primary_first_coverage_reused=dict(math_items=419,regions=7,nodes=22,edges=49,NODE=173,EXCLUDED=246),
    checks=checks,mathematical_statement_repair_required=False,required_source_repairs=[],
    required_compiler_action='The reported pre-first-tactic unknown-free-variable failure remains unresolved. This source-equivalent annotation must not be credited as a compiler repair; root must diagnose separately before any compiled-theorem claim.',
    root_diagnostic_report=dict(actual_pid=39696,actual_exit=1,error='unknown free variable _fvar.8864 before first tactic',
        source_of_observation='Parent root message; not an independently run or independently inspected Lean diagnostic in this source-only scope'),
    BODY_reviewed=False,proposal_opaque_BODY_RAW_sha256=proposal['proof_BODY_RAW_sha256'],Lean_compilation_run=False,proof_search=False,
    new_full_theorem_source_fidelity_or_VERIFIED_credit=False,canonical_Lean_source_Git_ledger_Goal_edits=False,
    remaining_truth_boundary='Only exact public-header representation overlay. Original actual-input centering/integral-preservation and rotation proof obligations remain internal; B21 corrector/B4/main/composition and full source/theorem/VERIFIED admission are not established here.')
(out/'decision.json').write_text(json.dumps(decision,sort_keys=True,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(out/'exact-116-line-source-retention-map.json').write_text(json.dumps(dict(schema='type-ascription70-exact-header-line-map-v1',line_map=line_map,
    added_wrapper_lines=[10,118],source_expressions_changed=0,caller_fields_changed=0,original_recovered_RAW_sha256=sha(recovered)),sort_keys=True,indent=2)+'\n',encoding='utf-8')
(out/'input-manifest.json').write_text(json.dumps(dict(schema='type-ascription70-complete-named-input-manifest-v1',count=len(inputs),inputs=inputs),sort_keys=True,indent=2)+'\n',encoding='utf-8')
payload=[]
for e in inputs:
    b=(out/e['name']).read_bytes();lf=b.replace(b'\r\n',b'\n')
    payload.append(dict(attribution=e,RAW_base64=base64.b64encode(b).decode('ascii'),LF_base64=base64.b64encode(lf).decode('ascii')))
(out/'RAW-LF-input-payload.json').write_text(json.dumps(dict(schema='type-ascription70-complete-RAW-LF-inputs-v1',count=len(inputs),
    LF_recipe='Only CRLF-to-LF; preserve every other byte',inputs=payload),sort_keys=True,indent=2)+'\n',encoding='utf-8')
(out/'finite-coverage.json').write_text(json.dumps(dict(source_overlay_checks=6,original_lines=116,candidate_lines=118,
    covered_original_lines=116,covered_candidate_lines=118,wrapper_only_lines=2,unclassified_lines=0,input_count=len(inputs),
    reused_source_math=419,reused_source_NODE=173,reused_source_EXCLUDED=246,statement_source_repairs=0),sort_keys=True,indent=2)+'\n',encoding='utf-8')
(out/'negative-observations.json').write_text(json.dumps(dict(helper_failure=dict(actual_pid=49532,actual_exit=1,
    cause='Wrong assumed manifest.final.json name; native CLOSED83 actually owns owned-manifest.json.',
    preserved_script='freeze-expectations.v1.failed.py',preserved_receipt='freeze-expectations.receipt.json',
    correction_actual_pid=10832,correction_actual_exit=0,candidate_overlay_unseen_until_successful_freeze=True),
    no_Lean_run_or_compiler_failure_fabricated=True),sort_keys=True,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(actual_review_pid=os.getpid(),verdict=decision['verdict'],exact_inverse=True,source_repairs=0,
    compiler_fix=False,inputs=len(inputs),old_CLOSED83_unchanged=True,decision_RAW_sha256=sha((out/'decision.json').read_bytes())),sort_keys=True))
