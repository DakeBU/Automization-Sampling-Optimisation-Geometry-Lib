import json,re
from record import ROOT
C=ROOT/'candidate'
s=json.loads((C/'research-wiki/technical-lemmas/real-matrix-positive-integral-statement-seal.json').read_text())['producer']
p=json.loads((C/'research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-statement-seal.json').read_text())['producer']
ss=s['signature']; ps=p['signature']; empty=ss.replace('{n Ω : Type*}','{Ω : Type*}').replace('[Fintype n] [DecidableEq n] ','').replace('Matrix n n','Matrix (Fin 0) (Fin 0)')
q0=re.sub(r'\bq\b','0',ps.replace('{d q : ℕ}','{d : ℕ}'))
head='''import Lean
import Tests.RealMatrixPositiveIntegral
open Lean Lean.Meta Lean.Elab Lean.Elab.Command
open MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix.Norms.L2Operator
set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 0
'''
probes=(f'theorem nativeLiteralS\n{ss}:= by\n  exact {s["name"]} f hf hpos\n'
 +f'theorem nativeEmptyS\n{empty}:= by\n  exact {s["name"]} f hf hpos\n'
 +f'theorem nativeLiteralP\n{ps}:= by\n  exact {p["name"]} hq\n'
 +f'theorem nativeZeroQueryP\n{q0}:= by\n  exact {p["name"]} (q := 0) hq\n')
(C/'NativeAudit.lean').write_text(head+probes+(ROOT/'audit-tail.lean').read_text())
print('generated literal universal S/P, generic-universe S, empty-index S and q=0 P proof applications')
