from context101 import *
prior=B.parent/'pbps-actual-prescribed-path-reversal100/exact-commit-verification100/closed-RAW-manifest100.json'
collab=load(prior)['preserved_collaborator_inputs'];assert len(collab)==21
for r in collab:assert info(r['path'])['raw_sha256']==r['raw_sha256'],r['path']
own=[B/'independent-whole-math101/whole-math-decision101.native.json',B/'independent-whole-math101/closed-RAW-manifest101.native.json',B/'independent-whole-math101/fresh-kernel-receipt101.native.json',B/'independent-index-clarification101/index-clarification-decision101.native.json',B/'independent-index-clarification101/closed-RAW-index-clarification101.native.json']
for p in [own[1],own[4]]:
 for r in load(p)['files']:assert info(r['path'])['raw_sha256']==r['raw_sha256'],r['path']
prep=load(B/'independent-whole-math101/prepared-inputs101.native.json')
for k in ['production','header','seal']:assert info(prep[k]['path'])==prep[k]
assert not (O/'root-freeze-dispatch101.native.json').exists()
save('preparation101.native.json',dict(status='PREPARED_AWAITING_EXPLICIT_SCIENCE_SHA_AND_FINAL_SOURCE_COVERAGE',science_commit=None,no_commit_verification_yet=True,no_admission_authorization_exercised=True,reference_workflow=info(prior),reusable_independent_evidence=[info(p) for p in own],production=info(M),header=prep['header'],seal=prep['seal'],preserved_collaborator_inputs=collab,sole_lane_to_preserve='ASTIS-SA-20261011-PBPSActualPrescribedPathDensity',planned_checks=[
 'Pin explicit root science SHA and baseline, exact Git tree, staging scope and working RAWs; reject HEAD drift.',
 'Resolve every native reviewed RAW via exact Git blobs or committed lossless archives, including CRLF originals and pre-coverage publication/cell snapshots; preserve historical inputs and exclude new full-primary bytes.',
 'Recheck21 collaborator RAWs from exact100 closed manifest and all unchanged wholemath/header/index-clarification closures.',
 'Validate native decoder packet, reconstruction/run hash recipes and actual input-only provenance against canonical audit.',
 'Validate final primary-first source run, seven slots/deltas/verdict/repairs, source coverage and exact lesson regions. Account for independent index-clarification acceptance separately from full-source verdict.',
 'Validate owner-provenance erratum against before snapshots: only incorrect companion_root_20261015 label becomes companion_root_20261005, plus justified packet digest updates; source/Lean/lesson/decoder semantics stay unchanged.',
 'Verify final coverage pointers and current publication binding; prove any prior reviewed-publication transfer is metadata-only by structural comparison.',
 'Transfer exact unchanged fresh production/sealed Header kernel/standard3 axioms; run focused module, contributor/publication/semantic/frontier/diff gates and native fake-closure scan.',
 'Only after all PASS and final same-commit state recheck, append one native VERIFIED101 event and change only101 cell status/evidence. Preserve all other advances/cells, sole94 lane and21 collaborator RAWs; close manifest with preserved_collaborator_inputs.'
 ],new_actual_uncertainties=['Exact science commit and final source artifacts are pending; no frozen-commit decision is made during preparation.'],no_shared_edits=True))
print(json.dumps(info(O/'preparation101.native.json')))
