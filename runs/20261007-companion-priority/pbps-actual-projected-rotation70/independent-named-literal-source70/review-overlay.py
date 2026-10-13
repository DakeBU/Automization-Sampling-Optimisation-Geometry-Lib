import base64,hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent;repo=out.parents[3];diag=out.parent/'compiler-diagnosis70'
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda n:json.loads((out/n).read_bytes())
inputs=load('input-manifest.initial.json')['inputs']
def snap(p,n,role,expected=None):
    b=p.read_bytes();lf=b.replace(b'\r\n',b'\n')
    if expected:assert sha(b)==expected,p.as_posix()
    (out/n).write_bytes(b);(out/(n+'.LF')).write_bytes(lf)
    inputs.append(dict(original_path=p.as_posix(),name=n,role=role,RAW_bytes=len(b),RAW_sha256=sha(b),LF_bytes=len(lf),LF_sha256=sha(lf),LF_recipe='CRLF-to-LF only'))
    return b
proposal_raw=snap(diag/'header-named-literal70.proposal.json','overlay.proposal.RAW.json','current proposed representation metadata')
proposal=json.loads(proposal_raw)
candidate_raw=snap(diag/'header-named-literal70.proposed.lean','overlay.proposed-header.RAW.lean','private literal/public header only',proposal['proposed_RAW_sha256'])
for i,e in enumerate(proposal['reused_retired_inline_routes']):
    b=snap(repo/e['snapshot'],'opaque-origin%d.exactraw.snapshot'%i,'opaque provenance only; no66 diagnosis/verdict or69 mathematics decoded/used',e['RAW_sha256'])
    assert len(b)==e['RAW_bytes']
production=snap(repo/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualProjectedRotation.lean','opaque-production-V1.RAW.lean',
    'opaque structural BODY equality only; no mathematical BODY review',proposal['production_unchanged_RAW_sha256'])
diagnostic=snap(repo/proposal['diagnostic_file'],'opaque-named-literal-diagnostic.RAW.lean',
    'opaque structural replacement/unfold equality only; no mathematical BODY review or compile',proposal['diagnostic_RAW_sha256'])
original=(out/'original-sealed-header.RAW.lean.LF').read_bytes()
candidate=candidate_raw.replace(b'\r\n',b'\n')
oldlines=original.splitlines(keepends=True)
private=b'private def actual_projected_rotation_statement\n'+b''.join(oldlines[1:8])+oldlines[8].replace(b' :\n',b' : Prop :=\n')+b''.join(oldlines[9:])
call='actual_projected_rotation_statement (E:=E) (V:=V) (α:=α) (β:=β) (η:=η) hα hαβ hV hH hη hβη'.encode('utf-8')
public=b''.join(oldlines[:8])+oldlines[8].rstrip(b'\n')+b' '+call+b'\n'
assert candidate==private+b'\n'+public
assert len(oldlines)==116 and len(candidate.splitlines())==126
assert private.splitlines(keepends=True)[9:]==oldlines[9:]
recovered=b'theorem actual_projected_rotation\n'+b''.join(private.splitlines(keepends=True)[1:8])+private.splitlines(keepends=True)[8].replace(b' : Prop :=\n',b' :\n')+b''.join(private.splitlines(keepends=True)[9:])
assert recovered==original
(out/'inverse-expanded-public-result.exact-original.LF.lean').write_bytes(recovered)
needle=original.rstrip(b'\n')+b' := by\n'
replacement=candidate.rstrip(b'\n')+b' := by\n  unfold actual_projected_rotation_statement\n'
assert production.count(needle)==1
assert production.replace(needle,replacement,1)==diagnostic
oldbody=production.split(needle,1)[1]
newbody=diagnostic.split(replacement,1)[1]
assert oldbody==newbody
structural=dict(schema='named-literal70-exact-opaque-structural-overlay-v1',
    original_header_lines=116,proposed_header_lines=126,private_literal_lines=[1,116],public_theorem_lines=[118,126],
    private_value_lines=[10,116],all107_value_lines_exact=True,
    literal_body_LF_sha256=sha(b''.join(oldlines[9:])),public_call_exact_same_parameters_and_six_hypotheses=True,
    entire_diagnostic_exact_original_module_replacement_plus_one_unfold=True,
    retained_BODY_and_trailer_RAW_bytes=len(oldbody),retained_BODY_and_trailer_RAW_sha256=sha(oldbody),
    inserted_BODY_line='  unfold actual_projected_rotation_statement\n',
    opaque_BODY_bytes_not_mathematically_reviewed=True,opaque_origins_not_used_as_source_truth=True)
(out/'exact-literal-public-and-opaque-BODY-overlay.json').write_text(json.dumps(structural,sort_keys=True,indent=2)+'\n',encoding='utf-8')
old_dir=repo/'runs/20261007-companion-priority/pbps-actual-projected-rotation-preproof70/independent-header-source70'
oldmanifest=load('prior-CLOSED83.manifest.RAW.json');oldlease=load('prior-CLOSED83.lease.RAW.json')
for e in oldmanifest['regular_file_entries']:
    b=(old_dir/e['name']).read_bytes();assert len(b)==e['RAW_bytes'] and sha(b)==e['RAW_sha256']
    assert sha(b.replace(b'\r\n',b'\n'))==e['LF_sha256']
assert sha((old_dir/'owned-manifest.json').read_bytes())==oldlease['manifest_RAW_sha256']
assert len([p for p in old_dir.iterdir() if p.is_file()])==83
checks=[
 dict(id='NL70-1',decision='PASS',field='original sealed/source-first baseline',evidence='Original9261f488... and all CLOSED83 RAW/LF regular entries/manifest verify; original primary-first419/7/22/49 coverage reused, no66 verdict supplies mathematical truth.'),
 dict(id='NL70-2',decision='PASS',field='private Prop literal exact value',evidence='Private lines10-116 equal all107 original return-expression lines byte-for-byte. Replacing only declaration name/type annotation reconstructs all116 original sealed lines exactly.'),
 dict(id='NL70-3',decision='PASS',field='public callers and literal instantiation',evidence='Public theorem118-126 retains original name,type parameters,typeclasses and all6 analytic hypotheses; one exact literal call supplies those same parameters/hypotheses in original order. No extra premise/provider.'),
 dict(id='NL70-4',decision='PASS',field='source objects/formulas/scopes',evidence='Exact complete literal equality preserves all12 common witnesses,old69 conclusions,SAME actual g,internally produced mean_g,actual conditional gP and polar gV,two signed rotations and square sum;rank0/alphaeta1/no ontoV/no68sharpenergy.'),
 dict(id='NL70-5',decision='PASS_STRUCTURAL_ONLY',field='one-unfold BODY delta',evidence='Pinned diagnostic module equals pinned current V1 module with only the exact header replacement and one unfold line inserted before the original BODY. Remaining BODY/trailer bytes are identical. No mathematics of BODY is reviewed and no Lean is run.'),
 dict(id='NL70-6',decision='PASS_WITH_READER_OBLIGATION',field='reader/public representation',evidence='Inline public syntax abbreviates the return type. Complete fullidentity private literal must be exposed in an adjacent initially folded Lean panel with full module link, as proposition representation; reader delivery remains future independent acceptance.'),
 dict(id='NL70-7',decision='PASS_SCOPE_ONLY',field='compiler/source credit',evidence='Proposal process origins66/69 are opaque hash provenance only. No compile result,whole theorem source fidelity,VERIFIED,B21/B4/main/composition or Exposition credit is inferred.')]
decision=dict(schema='astis-named-literal70-independent-source-overlay-decision-v1',owner='/root/independent_primary69',
    verdict='ADMIT_EXACT_NAMED_LITERAL_REPRESENTATION_ONLY_WITH_READER_OBLIGATION',actual_review_pid=os.getpid(),
    expectations_frozen_before_overlay_RAW_sha256=sha((out/'expectations.before-overlay.json').read_bytes()),
    original_sealed_header_RAW_sha256=sha(original),proposed_header_RAW_sha256=sha(candidate_raw),proposal_RAW_sha256=sha(proposal_raw),
    prior_source_CLOSED83_lease_RAW_sha256=sha((out/'prior-CLOSED83.lease.RAW.json').read_bytes()),old_CLOSED83_unchanged=True,
    exact_literal_value_preserves_complete_original_result=True,exact_public_six_caller_instantiation=True,
    public_inline_syntax_changed=True,mathematical_statement_changed=False,missing_or_extra_public_premises=0,
    common_witnesses=['S','e','U','T','Γ','q','ΓP0','Inv','A0','B0','V0','R'],
    original_primary_first_coverage_reused=dict(math_items=419,regions=7,nodes=22,edges=49,NODE=173,EXCLUDED=246),
    checks=checks,mathematical_source_statement_repairs_required=[],
    required_reader_followup=[
        'Expose AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation.actual_projected_rotation_statement by fullidentity as complete adjacent initially folded literal declaration with public signature and full module source link.',
        'Explicitly label the private literal as the complete proposition representation, never a proof provider/dependency/caller certificate.',
        'Bind source/statement seal and future blind/source/reader packets to this exact representation when root applies it; no current delivery claim.'],
    mean_g_internal_obligation_unchanged=load('prior-mean-g-obligation.RAW.json'),
    opaque_structural_BODY_overlay=structural,old66_origins_opaque_hashed_only=True,
    Lean_compilation_run=False,proof_search=False,mathematical_BODY_review=False,
    new_full_theorem_source_fidelity_or_VERIFIED_credit=False,canonical_Lean_source_Git_ledger_Goal_edits=False,
    remaining_truth_boundary='Representation overlay admission only. Root must separately diagnose/compile/prove the actual centered rotation and complete subsequent independent full source/blind/reader gates. B21 corrector,B4/main/composition and fullExposition remain open.')
(out/'decision.json').write_text(json.dumps(decision,sort_keys=True,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(out/'input-manifest.json').write_text(json.dumps(dict(schema='named-literal70-complete-named-input-manifest-v1',count=len(inputs),inputs=inputs),sort_keys=True,indent=2)+'\n',encoding='utf-8')
payload=[]
for e in inputs:
    b=(out/e['name']).read_bytes();lf=b.replace(b'\r\n',b'\n')
    payload.append(dict(attribution=e,RAW_base64=base64.b64encode(b).decode('ascii'),LF_base64=base64.b64encode(lf).decode('ascii')))
(out/'RAW-LF-input-payload.json').write_text(json.dumps(dict(schema='named-literal70-complete-RAW-LF-inputs-v1',count=len(inputs),
    LF_recipe='Only CRLF-to-LF; preserve every other byte',inputs=payload),sort_keys=True,indent=2)+'\n',encoding='utf-8')
(out/'finite-coverage.json').write_text(json.dumps(dict(source_overlay_checks=7,original_lines=116,proposed_lines=126,
    private_literal_lines=116,public_header_lines=9,separator_lines=1,original_value_lines=107,unclassified_lines=0,input_count=len(inputs),
    reused_source_math=419,reused_source_NODE=173,reused_source_EXCLUDED=246,statement_source_repairs=0,
    reader_followup_obligations=3,mathematical_BODY_review=False,opaque_BODY_equality_checked=True),sort_keys=True,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(actual_review_pid=os.getpid(),verdict=decision['verdict'],exact_literal=True,exact_public_call=True,
    exact_opaque_BODY_plus_one_unfold=True,source_repairs=0,reader_followups=3,input_count=len(inputs),
    decision_RAW_sha256=sha((out/'decision.json').read_bytes())),sort_keys=True))
