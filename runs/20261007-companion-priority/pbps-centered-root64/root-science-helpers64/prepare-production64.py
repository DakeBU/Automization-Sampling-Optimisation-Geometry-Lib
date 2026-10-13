from pathlib import Path
import hashlib,json
root=Path.cwd();r=root/'runs/20261007-companion-priority/pbps-centered-root64';pre=root/'runs/20261007-companion-priority/pbps-centered-root-preproof64'
receipt=json.loads((r/'combined-draft-v10/receipt.json').read_bytes())
assert receipt['exit_code']==0 and receipt['terminal_closed']
log=(r/'combined-draft-v10/stdout.log').read_text(encoding='utf-8')
assert 'sorryAx' not in log and ': error' not in log
src=(r/'combined-draft-v10.lean').read_text(encoding='utf-8')
gns='AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareOrder'
ans='AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredRootOrderInverse'
generic=src.split('namespace '+gns+'\n',1)[1].split('\nend '+gns,1)[0]+'\nend '+gns+'\n'
actual=src.split('namespace '+ans+'\n',1)[1].split('\n#print axioms '+ans,1)[0]
for text,i,name in [(generic,0,'positive_square_order'),(actual,1,'actual_centered_root_order_inverse')]:
 h=text.split('theorem '+name,1)[1].split(':= by',1)[0]
 assert ('theorem '+name+h).strip()==(pre/f'header{i}.lean').read_text(encoding='utf-8').strip()
gp=root/'AutoSamplingTheory/TechnicalLemmas/Measure/L2RealSquareOrder.lean'
ap=root/'AutoSamplingTheory/ExampleCases/ProximalBPS/CenteredRootOrderInverse.lean'
assert not gp.exists() and not ap.exists()
gimports='''import AutoSamplingTheory.TechnicalLemmas.Measure.L2RealComplexOperator
import Mathlib.Analysis.InnerProductSpace.StarOrder
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Instances
import Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.Rpow.Order

open MeasureTheory
open scoped ENNReal

'''
aimports='''import AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicDefectRoot
import AutoSamplingTheory.ExampleCases.ProximalBPS.RoughMeanGradient
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalPoincare
import AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareOrder
import Mathlib.Analysis.Normed.Operator.Banach

open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped RealInnerProductSpace ContDiff NNReal Topology

'''
gp.write_text(gimports+'namespace '+gns+'\n'+generic,encoding='utf-8',newline='\n')
ap.write_text(aimports+'namespace '+ans+'\n'+actual,encoding='utf-8',newline='\n')
testheader=(pre/'header1.lean').read_text(encoding='utf-8').replace('theorem actual_centered_root_order_inverse','theorem genuine_actual_centered_inverse_consumer')
testheader=testheader.rstrip()+''' ∧
                    (∀ f : HP0,
                      ‖B (HP0.subtypeL (Inv f))‖ = ‖f‖ ∧
                      P (B (HP0.subtypeL (Inv f))) = 0)
'''
th=r/'test.header64.lean';assert not th.exists();th.write_text(testheader,encoding='utf-8',newline='\n')
seal=r/'test.statement-seal64.json';assert not seal.exists()
seal.write_text(json.dumps(dict(status='SEALED_ORIGINAL_INPUT_TEST_CONSUMER_BEFORE_BODY',header_path=th.as_posix(),header_raw_sha256=hashlib.sha256(th.read_bytes()).hexdigest(),source='PBPS2609.06905v1 B15 and B16 normalized-leakage norm/range input',boundary='Only an original-input integration Test consumer of the same Gram and bounded inverse; no public B16 polar/onto theorem, dynamics or paper/main completion.',parent_seal=(pre/'root.statement-seal64.json').as_posix(),extra_public_premises=False),indent=2)+'\n',encoding='utf-8',newline='\n')
print('Production generic/actual64 extracted from EXIT0 exact sealed full draft; original-input normalized leakage consumer type separately sealed before its proof body. No local/verified publication transition.')
