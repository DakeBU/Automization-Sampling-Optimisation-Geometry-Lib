from pathlib import Path
import hashlib, json, shutil

r = Path.cwd()
e = r/'research-wiki/technical-lemmas/matrix-laplace-tail-semantic-evidence'
w = r/'.astis/huanjian-gc-matrix-laplace-20261114'
e.mkdir(exist_ok=True, parents=True)
files = ['AutoSamplingTheory/TechnicalLemmas/Probability/MatrixLaplaceTail.lean',
         'Tests/GaussianComplexityLaplaceTail.lean']
receipts = [
'20261114T121038198059Z-matrix-laplace-P-explicit-finite-spectral-sum-proof',
'20261114T121225753642Z-matrix-laplace-P-production-AE-strong-measurability-import',
'20261114T121442230413Z-matrix-laplace-T-confirmed-global-selfadjoint-sum-API']
out = e/'local-math-originals'
out.mkdir(exist_ok=True)
manifest=[]
for stem in receipts:
    for suffix in ['.log','.receipt.json']:
        p=r/'.astis/huanjian-resume-20261103'/(stem+suffix)
        b=p.read_bytes()
        (out/p.name).write_bytes(b)
        manifest.append({'path':str((out/p.name).relative_to(r)), 'bytes':len(b),
                         'sha256':hashlib.sha256(b).hexdigest(), 'original':str(p.relative_to(r))})
report={'schema_version':1,'status':'ROOT_LOCAL_COMPILED_ONLY_NOT_PROVED_LOCAL_OR_VERIFIED',
 'P':files[0],'T':files[1],
 'inputs':[{'path':f,'bytes':len((r/f).read_bytes()),'sha256':hashlib.sha256((r/f).read_bytes()).hexdigest()} for f in files],
 'actual_checks_originals':manifest,
 'consumer':'All four signed ordinary/cosine centered sums under the original Gaussian product law; all positive s and all real a, including q=0.',
 'derived_inside_T':['Measurability and Hermiticity of all four sums',
 'A finite uniform norm bound, then matrix exponential integrability',
 'Trace-exponential nonnegativity and integrability',
 'Extended nonnegative expectation equals ofReal of the actual Bochner expectation'],
 'proof_route':'Spectral theorem and unnormalized trace identity; a maximum eigenvalue contributes one positive term; AE event inclusion; scalar nonnegative Markov; reciprocal exponential; positive-parameter infimum.',
 'source_route_note':'Direct Markov on trace exponential combines the two elementary inequalities used in Tropp Prop3.1. It does not assert operator monotonicity or a product MGF bound. Independent fresh review remains pending.',
 'remaining':['Independent anonymous decoding and fresh anti-anchored source/whole-module/reader review',
 'Immutable independent native build/type-value dependency audit',
 'Authored declaration lesson, source binding, isolated reader acceptance',
 'Normal PROVED_LOCAL and independent VERIFIED if their actual gates pass',
 'Main/shared graph/site integration, purification and full-paper conclusions'],
 'not_closed':['Independent-sum/master Laplace MGF upper bound','Matrix Bernstein','C6 / Lemma4.4','Either main lower bound','Oracle / precision / cost adapters','Whole Goal']}
(e/'local-mathematics-checkpoint.v1.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'copied_real_receipt_leaves':len(manifest),'source_files':report['inputs'],'status':report['status']},ensure_ascii=False))
