from pathlib import Path
import json, re

old=Path('.astis/pbps-root-commutation67'); new=Path('.astis/pbps-sharp-energy68')
replacements=[
 ('pbps-root-commutation67','pbps-sharp-energy68'),('integration67','integration68'),
 ('verification67','verification68'),('visual67','visual68'),('inspect-cdp67','inspect-cdp68'),
 ('inspect-copy67','inspect-copy68'),('generated-card-cache67','generated-card-cache68'),
 ('ASTIS-SHARED-l2-real-positive-square-commutation','ASTIS-SHARED-hilbert-corrector-square-bound'),
 ('ASTIS-SW-PBPS-actual-root-inverse-commutation','ASTIS-SW-PBPS-sharp-corrector-energy'),
 ('AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareCommute.positive_square_commutation','AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorBound.quadratic_corrector_bound_of_square_identity'),
 ('AutoSamplingTheory.ExampleCases.ProximalBPS.ActualRootCommutation.actual_same_root_inverse_commutation','AutoSamplingTheory.ExampleCases.ProximalBPS.SharpCorrectorEnergy.actual_sharp_corrector_bound'),
 ('AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareCommute','AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorBound'),
 ('AutoSamplingTheory.ExampleCases.ProximalBPS.ActualRootCommutation','AutoSamplingTheory.ExampleCases.ProximalBPS.SharpCorrectorEnergy'),
 ('real-l2-positive-square-commutation','hilbert-sharp-quadratic-corrector-bound'),
 ('pbps-actual-root-inverse-commutation','pbps-sharp-corrector-energy'),
 ('3da29415011a971a65f749502a625e416213f487','3ad3b127b5a645be9cf71b3d14520b2d8fea3122'),
 ('kept_two_enriched67_cards','kept_two_enriched68_cards'),
 ('67 module cards','68 module cards'),('science67','science68'),
]
for name in ['inspect-cdp67.mjs','inspect-copy67.mjs','preserve-integration-newlines67.py','cache-generated-cards67.py']:
    text=(old/name).read_text(encoding='utf-8')
    for a,b in replacements:text=text.replace(a,b)
    if name=='inspect-cdp67.mjs':
        pages=[]; rel='example-cases/samplewiki/companions/proximal-bouncy-particle.html'
        for i,(slug,count) in enumerate([('hilbert-sharp-quadratic-corrector-bound',5),('pbps-sharp-corrector-energy',6)]):
            selector="document.getElementById('"+slug+"')"
            pages.append([f'unit{i}-statement',rel,selector])
            for j in range(count):pages.append([f'unit{i}-proof-{j+1}',rel,selector+f'.querySelectorAll(".proof-reader-step")[{j}]'])
        pages.append(['branch-actual-consumer','lean-foundations.html?view=lean&focus=decl%3AAutoSamplingTheory.ExampleCases.ProximalBPS.SharpCorrectorEnergy.actual_sharp_corrector_bound',"document.querySelector('[data-underlying-lean-graph]')"])
        text=re.sub(r' const pages=\[.*?\];',lambda _: ' const pages='+json.dumps(pages)+';',text,count=1)
    destination=new/name.replace('67','68')
    assert not destination.exists(),destination
    destination.write_text(text,encoding='utf-8',newline='\n')
source=old/'preserve-generated-context67.py';text=source.read_text(encoding='utf-8')
for a,b in replacements:text=text.replace(a,b)
start=text.index('for module,layer,summary in ['); end=text.index(':\n item=next',start)
rows=[('AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorBound','Canonical reusable Hilbert operator lemma','Arbitrary complete real Hilbert H, selfadjoint K,D and I+K²=D² with norm(D)<=c and c>=0 give the sharp c/2 quadratic corrector bound. No finite dimension, nontriviality, positivity or commutation premise. Only the PBPS route presently has evidenced consumers; the genuine modified-energy Test is a transitive consumer in that same route.'),('AutoSamplingTheory.ExampleCases.ProximalBPS.SharpCorrectorEnergy','SampleWiki paper route','Same original PBPS inputs/root/inverse yield sharp B23 pair and actual centered-f corrector bounds. Genuine original-input Test proves exact half/three-halves modified energy and perturbation bounds for every0<omegaWeight<=gamma. Literal private Props preserve original statements. B21/H1/B4/dynamics/main/errors/cost/composition remain open.')]
text=text[:start]+'for module,layer,summary in '+repr(rows)+text[end:]
text=text.replace('Independent exact-science67 verified','Independent corrected exact-science68 verified').replace('Bounded root/inverse commutation and corrector coefficient geometry only','Bounded sharp corrector energy and modified-energy equivalence only')
destination=new/'preserve-generated-context68.py';assert not destination.exists();destination.write_text(text,encoding='utf-8',newline='\n')
text=(new/'safe-fetch68.py').read_text(encoding='utf-8').replace('safe-fetch-current68','safe-fetch-before-integration68')
destination=new/'safe-fetch-before-integration68.py';assert not destination.exists();destination.write_text(text,encoding='utf-8',newline='\n')
print('Prepared bounded68 integration, reader capture and context-preservation helpers only; no canonical mutation.')
