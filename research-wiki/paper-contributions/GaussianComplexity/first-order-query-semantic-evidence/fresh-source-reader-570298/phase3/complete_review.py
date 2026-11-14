from datetime import datetime,timezone
from pathlib import Path
import hashlib,json,re,subprocess
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC');OUT=Path(__file__).resolve().parent
BASE=OUT.parent.parent
AUDIT=ROOT/'research-wiki/semantic-roundtrip/audits/huanjian-first-order-query.json'
SELF='/root/reader_570298';COMMIT='214b6214c5b08bd52b6faa59a3ccd6ca35998420'
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def pin(p):
 b=p.read_bytes();return {'path':str(p.relative_to(ROOT)),'bytes':len(b),'sha256':sha(b)}
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==COMMIT
assert not (OUT/'review-run.json').exists()
p1=json.loads((OUT.parent/'phase1/source-semantic-slots.json').read_bytes())
p2=json.loads((OUT.parent/'phase2/seven-slot-comparison.json').read_bytes())
packet=json.loads((BASE/'full-anti-anchored-reviewer-packet.json').read_bytes())
before=json.loads((OUT/'preservation-before.json').read_bytes())
audit_before=AUDIT.read_bytes();audit=json.loads(audit_before)
snapshot=(OUT/'input-snapshots/06-huanjian-first-order-query.json').read_bytes()
assert audit_before==snapshot and audit['state']=='blind-reconstructed'
assert audit_before==subprocess.check_output(['git','show',COMMIT+':'+str(AUDIT.relative_to(ROOT))],cwd=ROOT)
checks=[]
for name in ['focused-build','production-direct','test-direct','critical-expansion']:
 p=OUT/(name+'.receipt.json');r=json.loads(p.read_bytes())
 assert r['exit_code']==0 and r['checked_commit']==r['head_after']==COMMIT
 assert sha((ROOT/r['log']).read_bytes())==r['log_sha256']
 checks.append(pin(p))
critical=(OUT/'critical-expansion.log').read_text()
assert critical.count('depends on axioms: [propext,')==3
assert all(x not in critical for x in ['sorryAx','admitAx','error:'])
for name in ['sanitized-fake-closure-scan.json','static-reader-review.json']:
 assert json.loads((OUT/name).read_bytes())['status']=='PASS'

# Preserve exact primary-source ancestry excerpt and read meaning-bearing library excerpts.
source=ROOT/'.astis/huanjian-resume-20261103/2610.20492v1.html';raw=source.read_bytes()
assert sha(raw)==p1['source']['raw_sha256']
at=raw.index(b'id="A2.SS3"');start=raw.rfind(b'<',0,at);depth=0
for m in re.finditer(rb'<(/?)section\b[^>]*>',raw[start:]):
 depth+= -1 if m.group(1) else 1
 if depth==0:
  end=start+m.end();break
(OUT/'raw-source-B3.exact.html').write_bytes(raw[start:end])
meaning=OUT/'meaning-definition-excerpts';meaning.mkdir(exist_ok=True)
specs=[
('Mathlib/Analysis/Normed/Lp/WithLp.lean',45,80,'WithLp is an entry-preserving wrapper with inverse constructor/projection.'),
('Mathlib/Analysis/InnerProductSpace/PiL2.lean',80,116,'EuclideanSpace is PiLp 2; inner product is the finite sum of coordinate inner products.'),
('Mathlib/LinearAlgebra/UnitaryGroup.lean',285,304,'Real full orthogonal group, not special orthogonal group; transpose is the inverse.'),
('Mathlib/Data/Matrix/Block.lean',318,345,'blockDiagonal uses (local coordinate,block index) and zero between distinct blocks.'),
('Mathlib/LinearAlgebra/Matrix/Defs.lean',518,536,'reindex uses submatrix by the inverse coordinate equivalences.'),
('Mathlib/Logic/Equiv/Fin/Basic.lean',228,242,'finSumFinEquiv concatenates full and residual coordinates.'),
('Mathlib/Logic/Equiv/Fin/Basic.lean',334,350,'finProdFinEquiv applied after prodComm sends (i,j) to i+n*j, equal to j*n+i.'),
('Mathlib/Analysis/Calculus/Gradient/Basic.lean',54,104,'HasGradientAt is genuine Frechet differentiation represented via toDual; gradient totalizes the Frechet derivative through inverse Riesz.'),
('Mathlib/Analysis/Calculus/Gradient/Basic.lean',169,176,'HasGradientAt.gradient obtains the chosen gradient from the proved genuine derivative.'),
('Mathlib/Analysis/CStarAlgebra/Matrix.lean',99,128,'Matrix.toEuclideanCLM represents literal matvec continuously; inner_toEuclideanCLM matches Euclidean inner product to dot/matvec.'),
('Mathlib/Analysis/InnerProductSpace/Calculus.lean',44,53,'Inner-product derivative is the sum of the two derivative terms.'),
('Mathlib/Analysis/InnerProductSpace/Calculus.lean',94,103,'HasFDerivAt.inner provides actual derivative composition.'),
('Mathlib/Analysis/InnerProductSpace/Adjoint.lean',380,384,'Self-adjointness is equivalent to symmetric bilinear action.'),
]
meaning_records=[]
for i,(rel,lo,hi,assessment) in enumerate(specs):
 path=ROOT/'.lake/packages/mathlib'/rel;b=path.read_bytes();lines=b.splitlines(keepends=True)
 excerpt=b''.join(lines[lo-1:hi]);name=f'{i:02d}-{Path(rel).name}-L{lo}-L{hi}.txt'
 (meaning/name).write_bytes(excerpt)
 meaning_records.append({'file':str(path.relative_to(ROOT)),'whole_file_sha256':sha(b),'first_line':lo,'last_line':hi,
  'exact_excerpt':'meaning-definition-excerpts/'+name,'excerpt_sha256':sha(excerpt),'assessment':assessment})
dump('meaning-definition-audit.json',{'status':'PASS','library_context':'Exact lake-manifest/toolchain pinned to checked tree; no project overrides in target namespace/imports. Every six approved context entries agrees with actual source meaning.',
 'excerpts':meaning_records,'raw_source_ancestry':{'source_raw_sha256':sha(raw),'source_id':'A2.SS3','byte_start_inclusive':start,'byte_end_exclusive':end,'excerpt_sha256':sha(raw[start:end])},
 'B3_ancestry':'Actual source B.3 uses orthogonality, Cauchy-Schwarz, literal E4 quadratic expansion, block sums and identity residual; complete DeterminantFamily/BlockFamily bodies match that route. The target consumes only the existing canonical blockPrecision_regular symmetry component; no ancestry statement is supplied as a public target premise.'})

full_evidence={
'objects':'Whole target module and canonical singleBlockPrecision/blockPrecision definitions agree literally with the expansion and source E4/E5. Fresh exact expansion elaborates using the real theorem with no proof search beyond exact.',
'domains':'Complete blockCoordinates and library finProdFinEquiv/finSumFinEquiv definitions confirm contiguous j*n+i and q*n+i encoding; Nat.div_add_mod and Fin 0 implement the residual convention. All parameters/Os/all x retain source domains.',
'quantifiers':'Whole module has autoImplicit false and no outer section variables/instances changing target binders; expanded theorem has only hn,hnd,hκ and actual orthogonal tuple, then universal x. Genuine derivative is a conclusion.',
'assumptions':'Symmetry is obtained inside the proof from the already existing canonical blockPrecision_regular; hsingle,hG,hgrad are internally proved. No response-correctness, symmetry, differentiability, spectral or operational-budget theorem-shaped assumption is smuggled into the target.',
'conclusion':'Reviewed hraw/hlin derive the actual quadratic Frechet derivative; hsingle expands actual E4, hG expands actual E5, hg transports the genuine gradient, and hval recovers actual value. Fresh production/Test/expansion all compile. Test uses actual Os1/Os2 and primitive equality at the same arbitrary x to equate real observations.',
'scopes':'Authored lesson/publication explicitly retain pointwise observation scope, unchanged residual and no adaptive/budget/law/TV/lower-bound claim. Static stock reader keeps actual definitions folded next to the single first-reading observation equation, five formula steps and exact closed Lean panels.',
'constant_dependencies':'Checked literal definitions and proof preserve (κ+1)/2,(κ-1)/4 and the value factor 1/2; no fresh constants or hidden tolerance/probability/T dependencies occur. Two expressions per block are not an operational cap theorem.',
}
relations={'objects':'equivalent','domains':'equivalent','quantifiers':'same','assumptions':'same','conclusion':'explicit-elaboration','scopes':'equivalent','constant_dependencies':'same'}
decoder=json.loads((BASE/'blind-730418/decoder-result.json').read_bytes())
run=json.loads((BASE/'blind-730418/decoder-run.json').read_bytes())
assert decoder==json.loads((BASE/'phase2-selective-input.json').read_bytes())['blind_reconstruction']
assert run['isolation']['read_only_packet'] and not run['isolation']['source_text_visible']
assert run['input_raw_sha256']==sha((BASE/'decoder-input.json').read_bytes())
slots={}
for key in relations:
 slots[key]={'original':' '.join(x['statement'] for x in p1['slots'][key]),
  'reconstructed':decoder[key],'relation':relations[key],
  'evidence':p2['slots'][key]['independent_reading_of_expanded_statement']+' '+full_evidence[key]}
delta_slots={'D1':'domains','D2':'domains','D3':'objects','D4':'conclusion','D5':'scopes','D6':'assumptions'}
deltas=[{'id':d['id'],'slot':delta_slots[d['id']],'severity':'informational','blocking':False,
 'classification':d['classification'],'description':'Source: '+d['source']+' Candidate: '+d['candidate'],
 'evidence':d['reason']} for d in p2['differences']]
boundary='Selected pointwise Appendix B.1 Ex33–35 only. Operational T→2T/per-block and total caps, adaptive Borel transcript/output simulation and law equality, seed/probability laws, Haar/sign arguments, TV precision, expected costs, main lower bounds, remote delivery, stabilization/merge and postmerge purification remain separate.'
dump('whole-module-static-review.json',{'status':'PASS','checked_commit':COMMIT,'target_declarations':[packet['lean']['declaration']],
 'independent_module_findings':full_evidence,'definition_kind':'literal','excess_binders':[],
 'private_or_other_production_declarations':'None: whole production file contains exactly the single reviewed public theorem and internal let/have proof bindings.',
 'canonical_ancestry':'Reuses singleBlockPrecision, blockPrecision and blockPrecision_regular; generated singleBlockPrecision._proof_1/_proof_2 are transparent declaration-typing internals reported by compiler, not new assumptions or source credit.',
 'test_quality':'Two genuinely distinct universally quantified hidden tuples; equality of actual forward/inverse observations only at the given point yields equality of both actual first-order observations through two target applications. Not a restatement of target assumptions.',
 'fake_closure':'Sanitized complete target/Test/ASTIS ancestry clean; all three checked theorem axiom lists are only propext, Classical.choice, Quot.sound.',
 'source_only_graph_consistency':'The independent phase1 source graph is unchanged: E4+primitive→Ex33, E5+actual quadratic+Ex33→Ex34, actual quadratic+gradient→Ex35. Calculus/coordinates are explicit internal adapters; canonical B3 regularity supplies symmetry as an edge.',
 'authored_proof':'Each of the five formula-proof steps matches the corresponding actual Lean construction. Exact statement/proof extraction checked in stock static reader.',
 'reader_limit':'Static HTML/source review only; no visual/browser/canonical-root-site claim.',
 'boundary':boundary,'no_mathematical_edit':True})
dump('exposure-log.json',{'reviewer':SELF,'phase1_manifest_sha256':'bc44863244c183b086f3c14f1f43a7e6fa5efc3e221a392fb5006ba2e8d985e6',
 'phase2_manifest_sha256':'b4ced2e2b379bd11d4b66826abef03c5735e8af99bd3550f2627c44e1aedc3c8',
 'phase2_comparison_sha256':'e0058783d82f3f2c460f97e8ceba1028b532f3ef0056ddfe6d6b715d2fa133a9',
 'chronology':['Phase1 raw-source-only baseline frozen before candidate exposure.','Phase2 selective statement/approved context/actual decoder comparison frozen before canonical packet/code.','Only after explicit phase3 authorization: read canonical anti-anchored packet, complete target/Test, full actual two-module ASTIS ancestry, current own audit and source/lesson/publication/frontier metadata, actual decoder input/result/run and relevant protocol/API implementations.','Read actual library definition/calculus/coordinate source and primary B.3 raw source. Ran fresh focused build and direct production/Test/critical exact expansion; generated a bounded stock static source card and checked exact extraction.','Foreign state/frontier/discovery/fragment bytes were hashed for preservation, not used as mathematical review content. No root, remote, browser, broad source theorem or previous fidelity verdict was used to decide this review.'],
 'canonical_context_before_phase2_freeze':False,'formalizer':packet['roles']['formalizer'],'decoder':packet['roles']['blind_decoder'],
 'independent_from_both':SELF not in packet['roles'].values(),'no_mathematical_edits':True,
 'permitted_shared_mutations':'Only own source audit and normal API transition for this SAU; frontier remains unchanged for root mechanical projection.'})

evidence_names=['input-pins-and-chain.json','sanitized-fake-closure-scan.json','bounded-source-ancestry.json',
 'static-reader-review.json','meaning-definition-audit.json','whole-module-static-review.json','exposure-log.json']
review_run={'schema':1,'reviewer':SELF,'formalizer':packet['roles']['formalizer'],'blind_decoder':packet['roles']['blind_decoder'],
 'independent_from_formalizer':True,'independent_from_decoder':True,'completed_utc':datetime.now(timezone.utc).isoformat(),
 'checked_commit':COMMIT,'canonical_reviewer_packet_sha256':packet['packet_sha256'],
 'canonical_packet_raw_sha256':sha((BASE/'full-anti-anchored-reviewer-packet.json').read_bytes()),
 'publication_binding_sha256':packet['publication_binding_sha256'],'phase1_manifest_sha256':'bc44863244c183b086f3c14f1f43a7e6fa5efc3e221a392fb5006ba2e8d985e6',
 'phase2_manifest_sha256':'b4ced2e2b379bd11d4b66826abef03c5735e8af99bd3550f2627c44e1aedc3c8',
 'evidence_artifacts':[pin(OUT/n) for n in evidence_names],'fresh_check_receipts':checks,
 'decoder_input':pin(BASE/'decoder-input.json'),'decoder_result':pin(BASE/'blind-730418/decoder-result.json'),'decoder_run':pin(BASE/'blind-730418/decoder-run.json'),
 'prior_audit_sha256':sha(audit_before),'checked_tree_audit_state':'blind-reconstructed',
 'accepted_review_bytes_status':'The accepted audit bytes are a subsequent working-tree metadata update, not present in checked immutable commit214b6214.',
 'verdict':'equivalent-after-elaboration','whole_module_static_reader_result':'PASS','remaining_boundary':boundary}
dump('review-run.json',review_run);run_sha=sha((OUT/'review-run.json').read_bytes())
review_evidence='Independent raw-source-first seven-slot review with phase1/phase2 frozen before full context. Exact214b production/Test and canonical parents, approved meaning definitions, literal anonymous expansion, real compiler/axiom evidence and stock static reader all PASS. Evidence: '+str((OUT/'review-run.json').relative_to(ROOT))+' SHA256 '+run_sha+'. '+boundary
result={'schema':1,'semantic_slots':slots,'deltas':deltas,'verdict':'equivalent-after-elaboration','repairs':[],
 'reviewer':SELF,'independent_from_formalizer':True,'independent_from_decoder':True,
 'review_evidence':review_evidence,'review_run_sha256':run_sha,'reviewer_packet_sha256':packet['packet_sha256'],
 'publication_binding_sha256':packet['publication_binding_sha256'],'checked_commit':COMMIT,'source_raw_sha256':p1['source']['raw_sha256'],
 'static_reader_only':True,'no_blocking_delta':True,'remaining_boundary':boundary,
 'checked_tree_audit_state':'blind-reconstructed','accepted_audit_bytes_not_yet_in_checked_commit':True}
dump('review-result.json',result)

# The only direct shared write: own fragment review fields, preserving all mathematical inputs.
audit.update(state='source-reviewed',semantic_slots=slots,deltas=deltas,verdict=result['verdict'])
audit['source_review']={'state':'accepted','reviewer':SELF,'independent_from_formalizer':True,'independent_from_decoder':True,
 'reviewer_packet_sha256':packet['packet_sha256'],'evidence':review_evidence,'review_run_sha256':run_sha,
 'run_artifact':str((OUT/'review-run.json').relative_to(ROOT)),'result_artifact':str((OUT/'review-result.json').relative_to(ROOT)),
 'verified_commit':COMMIT,'static_reader_only':True}
for key in ['source','lean','reconstruction','publication_binding_sha256','publication_context','repairs']:
 assert audit[key]==json.loads(audit_before)[key],key
assert AUDIT.read_bytes()==audit_before
new=(json.dumps(audit,ensure_ascii=False,indent=2)+'\n').encode();AUDIT.write_bytes(new)
(OUT/'audit-after.source-reviewed.json').write_bytes(new)
dump('audit-update-receipt.json',{'path':str(AUDIT.relative_to(ROOT)),'prior_bytes':len(audit_before),'prior_sha256':sha(audit_before),
 'new_bytes':len(new),'new_sha256':sha(new),'changed_fields':['state','semantic_slots','deltas','verdict','source_review'],
 'mathematical_input_fields_unchanged':True,'prior_state':'blind-reconstructed','new_state':'source-reviewed',
 'source_review':'accepted','checked_commit':COMMIT,'checked_tree_audit_remains_blind':True,
 'accepted_dirty_bytes_not_claimed_in_checked_commit':True,'review_result_sha256':sha((OUT/'review-result.json').read_bytes()),
 'review_run_sha256':run_sha,'canonical_reviewer_packet_sha256':packet['packet_sha256']})
print('Independent source review PASS. Own audit updated only review fields.')
for n in ['review-run.json','review-result.json','audit-update-receipt.json']:
 print(n,sha((OUT/n).read_bytes()))
print('audit prior',sha(audit_before),'new',sha(new))
