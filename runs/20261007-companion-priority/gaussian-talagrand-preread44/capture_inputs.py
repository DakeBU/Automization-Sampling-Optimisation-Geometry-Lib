from pathlib import Path
import hashlib,json,re
from pypdf import PdfReader
D=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def put(n,o):(D/n).write_bytes((json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode())
items=[]
def capture(id,p,ranges=None):
    raw=Path(p).read_bytes();whole=sha(raw)
    if ranges:
        lines=raw.decode('utf-8-sig').splitlines(keepends=True)
        raw=''.join(''.join(lines[a-1:b]) for a,b in ranges).encode('utf-8')
    lf=raw.replace(b'\r\n',b'\n')
    (D/(id+'.raw.snapshot')).write_bytes(raw);(D/(id+'.lf.snapshot')).write_bytes(lf)
    items.append({'id':id,'path':str(p),'raw_sha256':sha(raw),'lf_sha256':sha(lf),'whole_file_raw_sha256':whole,'selected_physical_ranges':ranges,'bytes':len(raw)})
capture('primary','runs/20261007-companion-priority/gaussian-canonical-kl-fisher-preread43/primary.raw.snapshot.html',[[652,661],[1289,1314],[7517,7526]])
for id,p,rg in [
 ('cardMeasure','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.TechnicalLemmas.Measure.md',None),
 ('cardFunctionalInequalities','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.md',None),
 ('cardProbability','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.Probability.md',None),
 ('cardSDE','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.SDE.md',None),
 ('sourceEdition','website/content/source_edition.json',[[1,11]]),
 ('Transport','AutoSamplingTheory/TechnicalLemmas/Measure/Transport.lean',[[11,38],[53,58]]),
 ('WassersteinSpace','AutoSamplingTheory/TechnicalLemmas/Measure/WassersteinSpace.lean',[[14,32],[36,40],[49,54],[61,66],[116,123]]),
 ('OptimalContinuousCost','AutoSamplingTheory/TechnicalLemmas/Measure/OptimalContinuousCost.lean',[[9,23]]),
 ('Brenier','AutoSamplingTheory/TechnicalLemmas/Measure/QuadraticOptimalBrenierMap.lean',[[34,55],[132,145]]),
 ('W2finite','AutoSamplingTheory/TechnicalLemmas/Measure/WassersteinFiniteSecondMoment.lean',[[17,25],[83,87]]),
 ('W2symmetry','AutoSamplingTheory/TechnicalLemmas/Measure/WassersteinSymmetry.lean',[[93,96]]),
 ('GaussianDensity','AutoSamplingTheory/TechnicalLemmas/Measure/IsotropicGaussianDensity.lean',[[22,36]]),
 ('EntropyPushforward','AutoSamplingTheory/TechnicalLemmas/Measure/DisplacementEntropyPushforward.lean',[[23,47]]),
 ('JacobianMatrixLeaves','AutoSamplingTheory/TechnicalLemmas/Measure/DisplacementJacobianEntropy.lean',[[7,48],[53,59],[64,88]]),
 ('ConvexGradientPositive','AutoSamplingTheory/TechnicalLemmas/Measure/DisplacementConvexGradientPositive.lean',[[27,43]]),
 ('ChangeOfVariables','AutoSamplingTheory/TechnicalLemmas/Measure/DisplacementChangeOfVariables.lean',[[26,67]]),
 ('PotentialEnergy','AutoSamplingTheory/TechnicalLemmas/Measure/DisplacementPotentialEnergy.lean',[[9,16],[19,29],[94,111]]),
 ('GeodesicConvexity','AutoSamplingTheory/TechnicalLemmas/Geometry/GeodesicConvexity.lean',[[11,31]]),
 ('KLcanonical','.lake/packages/mathlib/Mathlib/InformationTheory/KullbackLeibler/Basic.lean',[[51,61],[100,100]]),
 ('stdGaussian','.lake/packages/mathlib/Mathlib/Probability/Distributions/Gaussian/Multivariate.lean',[[44,74],[82,83],[108,108]]),
 ('GaussianMemLp','.lake/packages/mathlib/Mathlib/Probability/Distributions/Gaussian/Fernique.lean',[[38,41],[182,186],[209,210]])]:capture(id,p,rg)
pdf=D/'chewi-pinned.raw.snapshot.pdf';assert sha(pdf.read_bytes())=='9b454ccf44fe700081e13a766ae9cabb83c3530f5fdc532d59ac335f53652597'
r=PdfReader(pdf)
pages=[32,45,46,58,60,61,81]
for n in pages:
    t=r.pages[n-1].extract_text()+'\n';b=t.encode('utf-8');name='chewi-page%03d'%n
    (D/(name+'.raw.snapshot.txt')).write_bytes(b);(D/(name+'.lf.snapshot.txt')).write_bytes(b.replace(b'\r\n',b'\n'))
    items.append({'id':name,'path':'chewi-pinned.raw.snapshot.pdf','pdf_page_1_based':n,'book_page':n-12,'extracted_text_raw_sha256':sha(b),'extracted_text_lf_sha256':sha(b.replace(b'\r\n',b'\n')),'lines':len(t.splitlines()),'binary_pdf_raw_sha256':sha(pdf.read_bytes()),'LF_pdf':'not applicable: binaryPDF'})
put('input-bindings.json',{'inputs':items,'mathlib_revision':'db584cd6d46c92f209a44c0f1c829460d327499d','book_immutable_url':'https://raw.githubusercontent.com/chewisinho/chewisinho.github.io/b3ad6e874119983ae5f689a3295df4cdb44b11a7/main.pdf','prior_preread_primary_bytes':'historical43primary raw SHA ec485cdad5fe140114be35eef93d19398e0cafcf21abb3fff1bdbbf462e5f94d','source_expansion_boundary':'Narrow declarations/contracts/definitions and explicit gaps; not proof implementation or source graph.'})
