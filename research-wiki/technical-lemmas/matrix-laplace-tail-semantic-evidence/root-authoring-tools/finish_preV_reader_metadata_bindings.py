from pathlib import Path
import json,hashlib
r=Path.cwd();e=r/'research-wiki/technical-lemmas/matrix-laplace-tail-semantic-evidence'
p=r/'research-wiki/frontier-cells/ASTIS-SHARED-REAL-MATRIX-LAPLACE-TAIL.json'
x=json.loads(p.read_text());a=e/'post-PL-current-reader-acceptance.v1.json'
assert hashlib.sha256(a.read_bytes()).hexdigest()=='f9587b8bb5d30642913ed8a072d366d10deb1f65325f5192d2974a99425063d5'
assert x['status']=='proved_locally' and x['evidence']['current_normal_stage']['theorem_VERIFIED'] is False
v=x['source_detail_audit']['fidelity_boundary']
start=v.index('One normal PROVED_LOCAL is recorded');end=v.index('Authored-v4 served bytes',start)
x['source_detail_audit']['fidelity_boundary']=v[:start]+('One normal PROVED_LOCAL is recorded. Independent current isolated reader acceptance combines the original genuine v3 run/source/navigation observations with four actual supplemental desktop/mobile parent viewport states and independent SVG geometry/PNG review. The supplemental process remains exit1 with2false crop/completion checks: wrong desktop crops are excluded as SVG evidence and later repeated mobile steps did not execute. All original failures/PNGs remain preserved; independent necessary isolated-reader residual is0. Optional corrected-crop v3 was cancelled before execution and supplies no evidence. Proof VERIFIED remains pending. ')+v[end:]
rc=x['reader_contract']
rc['status']='Independent bounded isolated reader accepted by fresh8d2a; exact original v3 plus genuine targeted-v2 complete viewport correction. Native supplemental contract remains FAIL, optional v3 not executed; proofV and production acceptance remain separate.'
rc['served_byte_identity_to_v3']['reader_acceptance']='bounded isolated acceptance recorded separately; no new v4 browser run'
rc['current_runtime_state']={
 'actual_browser_run':'original reader-runtime-v3 plus targeted parent-supplement-v2',
 'new_v4_browser_run':False,'raw_automated_result_scope':'Original398/0false preserved; supplemental167/2false/exit1 preserved, never relabelled PASS.',
 'original356_preserved':True,'independent_visual_finding':'R15-VIS-GRAPH-PARENT-SVG-CLIP closed by four actual complete viewport states plus unchanged prior source/nav; wrong crops excluded.',
 'reader_acceptance':'ACCEPTED_BOUNDED_ISOLATED_SCOPE_NECESSARY_RESIDUAL0',
 'portable_evidence_binding':str(a.relative_to(r)),
 'optional_corrected_crop_repeat':'v3 cancelled before execution; no runtime evidence'}
p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'corrected_current_reader_fields':True,'normal_V_calls':0,'cell_status':x['status'],'historical_original24_untouched':True}))
