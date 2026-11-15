"""Prepare new bounded renderer from preserved R15 presentation mechanism only.

No browser/server, production/site/global graph change or mathematical verdict.
Rendering is deliberately a later explicit command after source review.
"""
from pathlib import Path
import hashlib,json,difflib
r=Path.cwd();w=r/'.astis/huanjian-gc-trace-mgf-domain-20261115'
old=r/'.astis/huanjian-gc-matrix-laplace-20261114/reader-preview-v4'
new=w/'reader-preview-v1';assert not new.exists();new.mkdir()
mapping={
 '1d1103af694b9663a72b0d610004ed85c7c6b527':'30172847ec40c24426f0b39afc4887719810eca0',
 'huanjian-matrix-laplace-tail':'huanjian-trace-exponential-domain',
 'AutoSamplingTheory/TechnicalLemmas/Probability/MatrixLaplaceTail.lean':'AutoSamplingTheory/TechnicalLemmas/Analysis/MatrixTraceExponentialBounds.lean',
 'Tests/GaussianComplexityLaplaceTail.lean':'Tests/GaussianComplexityTraceMgfDomain.lean',
 'AutoSamplingTheory.TechnicalLemmas.Probability.MatrixLaplaceTail.max_eigenvalue_tail_le_iInf_trace_exp':'AutoSamplingTheory.TechnicalLemmas.Analysis.MatrixTraceExponentialBounds.trace_exp_pos_and_le_card_mul_exp_abs_mul_norm',
 'AutoSamplingTheory.Tests.GaussianComplexityLaplaceTail.actual_source_four_sums_laplace_tail':'AutoSamplingTheory.Tests.GaussianComplexityTraceMgfDomain.actual_source_four_trace_mgfs_integrable_positive_and_bounded',
 '4924fede99548f6aab4f63605d2beed9dc435d6338a61d89ee301d9e83733749':'1ef6f49fa5f0a8b3b61ba42d31bca1bb744bebb64e433075d0ca25ab82570b76',
 '9ecf723f0487ddf50cb1d7c3102ebc04b58c472e56d2b16b186d91bc91cc6aac':'72311555e65cacc8b129510f2158abc9e2e6a230882a2169f6504e80f394fedb',
 'known[P].source_line != 55 or known[T].source_line != 44':'known[P].source_line != 18 or known[T].source_line != 21',
 "'.html#L55'":"'.html#L18'", "'.html#L44'":"'.html#L21'",
 "[PFILE] * 3 + [TFILE] * 3":"[PFILE] * 3 + [TFILE] * 2",
 'exactly P/P/P/T/T/T code folds':'exactly P/P/P/T/T code folds',
 "html.count('data-mgf-step=') != 6":"html.count('data-mgf-step=') != 5",
 "html.count('data-step-source href=') != 6":"html.count('data-step-source href=') != 5",
 'Expected six adjacent':'Expected five adjacent',
 'six_code_folds_exact_P96_T193':'five_code_folds_exact_P60_T183',
 'six_adjacent_source_and_full_download_actions':'five_adjacent_source_and_full_download_actions',
 'Real matrix Laplace tail':'Real Hermitian trace-exponential domain',
 'Laplace tail':'Trace-exponential domain',
}
rows=[]
for name in ['render_preview.py','reader_overlay.py']:
    before=(old/name).read_text();after=before
    for a,b in mapping.items():after=after.replace(a,b)
    (new/name).write_text(after)
    diff=''.join(difflib.unified_diff(before.splitlines(keepends=True),after.splitlines(keepends=True),fromfile='preserved-R15/'+name,tofile='R16/'+name))
    (new/(name+'.exact.diff')).write_text(diff)
    rows.append({'name':name,'reused_original_sha256':hashlib.sha256(before.encode()).hexdigest(),
        'adapted_sha256':hashlib.sha256(after.encode()).hexdigest(),'diff_sha256':hashlib.sha256(diff.encode()).hexdigest()})
obj={'scope':'Only the bounded reader presentation mechanism is reused, with new exact R16 P/T, five exact code folds and source anchors18/21. No R15 math/source/reader verdict inherited. P has no ASTIS value parents; private T has exact P+Radius+Structure parents. The bounded graph uses dashed scanner source references, not new certified theorem implication. No production/shared write.',
    'files':rows,'browser_executed':False,'server_started':False,'fixtures_generated':False}
(new/'reused-mechanism-custody.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'reader_helpers_prepared':str(new.relative_to(r)),'browser_executed':False,'fixtures_generated':False}))
