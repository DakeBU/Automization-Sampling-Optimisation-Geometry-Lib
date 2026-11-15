"""Project actual independent bounded reader acceptance; never append an ASTIS event."""
from pathlib import Path
import copy, hashlib, json, subprocess

r=Path.cwd(); w=r/'.astis/huanjian-gc-matrix-mgf-domain-20261115'
e=r/'research-wiki/technical-lemmas/matrix-mgf-domain-semantic-evidence'
cell=r/'research-wiki/frontier-cells/ASTIS-SHARED-REAL-MATRIX-EXPONENTIAL-DOMAIN.json'
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
def write(p,x):
    assert not p.exists(),str(p)
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def find_exact(root,h):
    ps=[p for p in root.rglob('*') if p.is_file() and sha(p.read_bytes())==h]
    assert len(ps)==1,(h,[str(p) for p in ps])
    return ps[0]
def identity(p):
    b=p.read_bytes();return {'file':str(p.relative_to(r)),'bytes':len(b),'sha256':sha(b)}

assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()=='8a6274eef3c466d618d2fc6222d985728246cfaf'
assert not subprocess.check_output(['git','diff','--cached','--name-only'])
for p,h in {
 'AutoSamplingTheory/TechnicalLemmas/Probability/RealMatrixPositiveDefIntegral.lean':'d3c6e5a194fecf1ae1abe45c70310f4f47d66e903b098019c326ee0d3018b024',
 'Tests/GaussianComplexityMatrixMgfDomain.lean':'60e9f7b928ebc1b8a0d9efad93f39f1b172fe0a871893d67eb1015582c5d5c61',
 'website/content/declaration_lessons/huanjian-matrix-mgf-domain.json':'62bb756e1a030d7f7444a5571cb2008663ccedcda39f9782bdecf641fa9fa08d',
 'website/content/publications/huanjian-matrix-mgf-domain.json':'d2b60c1a9e827f7c6fb81c648930183b77015950de0d97a3acf4d7adb6574f1a',
 'lean-toolchain':'302cd63c54178885b89e669f33b38f12f4dd7ae7e5cac537b3203e3768d8fb2b',
 'lake-manifest.json':'b83ca83b9cf7caa85fa8b023c2ff9a3fb7a7cce7e1c332e810c348535ec49c37',
}.items(): assert sha((r/p).read_bytes())==h,p
assert sha((e/'PROVED_LOCAL-evidence.full.json').read_bytes())=='4e1ae70212a5c951239de161597d0ebf816632c70762305d8c22a7841ea1e520'
portable=e/'reader-originals/successor-v5'
review=find_exact(portable,'8be01dcb356632540df08a5c592c8b6496e442d180a9f743b20c50dac4a1e33c')
a=load(review)
assert a['status']=='PASS_BOUNDED_ISOLATED_READER' and a['necessary_reader_residual_count']==0
assert a['actual_run']['OS_exit_code']==0 and a['actual_run']['runtime_checks']==523 and a['actual_run']['runtime_false_checks']==0
assert a['independent_basis']['all50_new_original_PNGs_actually_viewed'] is True
assert a['exact_binding']['source_reviewed_publication_binding_sha256']=='5e79fa3d4390c4d1e689174b0c014d67fb8dbfb550f986b4af7d8474ef644691'
assert a['explicit_limits']['normal_API_V_cell_ledger_Git_actions_by_reader_review']==0
x=load(cell);assert x['status']=='proved_locally' and x['evidence']['independent_verification']==''
old=cell.read_bytes(); snap=e/'reader-originals/root-cell.before-successor-reader-projection.original.json'
assert not snap.exists();snap.write_bytes(old)
old_reader=copy.deepcopy(x['evidence']['reader_review'])
x['evidence']['reader_review']={
 'status':a['status'],'independent_acceptance':identity(review),
 'actual_result_sha256':a['exact_binding']['actual_result_sha256'],
 'actual_exit_code':0,'checks':523,'false_checks':0,'actual_PNGs':50,
 'independent_actual_data_checks':261,'necessary_reader_residual_count':0,
 'server_and_thread_stopped':True,'preview_manifest_sha256':a['exact_binding']['preview_manifest_sha256'],
 'source_reviewed_binding':a['exact_binding']['source_reviewed_publication_binding_sha256'],
 'original_failed_snapshot_preserved':old_reader,
 'old_failure_disposition':'Original v3 remains FAIL501/3/50. Separate actual diagnosis identifies two pre-settlement anchor measurements and one real mobile grid overflow. v5 changes only scoped grid CSS; new generic observation waits for natural settled geometry with original strict predicate. No forced scrolling or tolerance relaxation.',
 'scope':'Only frozen isolated selected reader closure, desktop1440x1000/mobile390x844 headless Chrome; no production/full-site/physical-touch/purification acceptance.',
 'normal_V_by_reader':0,'mathematical_source_Lean_lesson_changes':0,
}
x['graph_contribution']['visual_review']='Independent actor61 actually inspected all50 new PNGs and audited graph11nodes/15edges,6clip cases, exact native P→PSD and privateT→P/Trace/Radius/Structure. Local graph only; selected corelabels visible fraction1 in both viewports, long full IDs remain in detail. No privateT public theorem or new global graph.'
x['semantic_roundtrip'].update(state='source-reviewed',qualification='Actual source-blind P/T decoding and independent fresh raw-first seven-slot/whole-module/five-step review accepted the unchanged5e79 binding. Separate locator overlay accepted; exact original audits retained. Not normalV or purification.')
x['source_detail_audit']['gap']='The generic PD integral and actual matrix-MGF domain bridge are author-derived infrastructure for source-omitted finite-expectation/positive domain. Independent preproof topology and postproof fresh source review accepted their bounded role; optional uniform-lower-envelope route was not implemented.'
x['source_proof_coverage']['independent_verdict_scope']='Independent preproof exact statement/topology, then separate fresh raw-first postproof source/whole-module/reader-span review and distinct locator-only overlay. Native truth and actual reader are separately evidenced.'
x['learning_contract']['failure_class']='NONE'
x['learning_contract']['salvage'].update(required=True,status='completed',reason='Original failed v3 and separate diagnostic retained with independent reviews. All original mathematical/native/source results and valid reader fragments retained; scoped CSS repair plus natural-stability observation successor accepted independently. No discarded source lines, mathematical route or weakened geometry predicate.',promoted_fragments=[],discarded_fragments=[])
x['truth_boundary']='Compiled generic real probability AE-PD integral and associated private literal Gaussian matrix-exponential means only: matrix Bochner integrability, true mean positive definiteness, ordinary trace commutation/strict positivity and exact r² exp(|s|dRstar) cap. Independent immutablea8bb native/type/value/kernel and fresh source-blind/seven-slot/whole-module/five-step fidelity accepted; exact two locator fields corrected by separately reviewed overlay. One actual normal PL; independent bounded isolated reader523checks/0false/50newPNG accepted. Independent normalV remains pending. No matrix-log identity, quantitative uniform lower eigenvalue bound, Lieb/Jensen/master-tail/Bernstein/C6/main lower bound or oracle/TV/precision/deterministic-query-cap/expected-cost adapter. Main/shared imports/Registry/global graph/source index/production site/purification and Goal completion remain held or pending.'
x['phase_snapshot']='Native/source/locator/actual isolated reader independently accepted. Actual normalPL1, RootV0 and independentnormalV0. This is pre-V metadata only; next freeze carrier, six real metadata gates, independent normalV and separate typed cell projection, then owned-only safe-public review/push/readback.'
x['compiled_worktree_candidate'].update(immutable_candidate_commit_pending=False,actual_immutable_native_rebuilt_commit='a8bb8ea5b4474be5214bd83ae380a612e2cecb78')
x['source_detail_audit']['fidelity_boundary']=x['truth_boundary']
cell.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
memory=e/'local-cycle-memory.json'; oldmem=memory.read_bytes()
oldmem_path=e/'reader-originals/local-cycle-memory.original-at-PL.json'
assert not oldmem_path.exists(); oldmem_path.write_bytes(oldmem)
m=load(memory);m.update(reader='Independent PASS_BOUNDED_ISOLATED_READER; actual523/0/50 newPNG; originalFAIL501/3/50 retained',independent_normal_V_calls=0,next='Freeze preV metadata carrier, six actual gates, independent one normalV plus separate typed cell projection, owned-only safe public candidate audit/CAS push/readback.')
memory.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
write(e/'reader-originals/root-pre-V-reader-projection.json',{'kind':'ROOT-current-owned-metadata-projection-not-independent-verification','previous_cell_sha256':sha(old),'current_cell_sha256':sha(cell.read_bytes()),'actual_independent_acceptance':identity(review),'mathematical_commit':'a8bb8ea5b4474be5214bd83ae380a612e2cecb78','source_reviewed_publication_binding':'5e79fa3d4390c4d1e689174b0c014d67fb8dbfb550f986b4af7d8474ef644691','normal_PL_calls':1,'Root_V_calls':0,'independent_normal_V_calls':0,'original_PL_evidence_unchanged':True,'purification_or_main_or_production_acceptance':False})
print(json.dumps({'status':x['status'],'reader':a['status'],'normal_PL':1,'Root_V':0,'independent_V':0,'math_source_lesson_publication_env_unchanged':True}))
