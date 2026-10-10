from pathlib import Path
import hashlib,json,os,sys
r=Path('runs/20261007-companion-priority/pbps-b4-corrector-perturbation72');p=Path('AutoSamplingTheory/TechnicalLemmas/Analysis/HilbertCorrectorPerturbation.lean')
raw=p.read_bytes();out=r/'typed-inner-repair';out.mkdir(exist_ok=False)
(out/'generic-first.exactraw.lean').write_bytes(raw)
(out/'executed-implement-helper.exactraw.py').write_bytes(Path('.astis/pbps-perturbation72/implement-generic72.py').read_bytes())
text=raw.decode();needle='  dsimp only\n';assert text.count(needle)==1
text=text.replace(needle,needle+'''  have ha (x y : H) : inner ℝ (A x) y=inner ℝ x (A y) := hA.isSymmetric x y
  have hg (x y : H) : inner ℝ (G x) y=inner ℝ x (G y) := hG.isSymmetric x y
  have hi (x y : H) : inner ℝ (Inv x) y=inner ℝ x (Inv y) := hInv.isSymmetric x y
''',1)
text=text.replace('hA.isSymmetric (A x) x,hG.isSymmetric (G x) x','ha (A x) x,hg (G x) x')
text=text.replace('hA.isSymmetric (Inv u) (A r),hInv.isSymmetric u (A (A r))','ha (Inv u) (A r),hi u (A (A r))')
p.write_text(text,encoding='utf8',newline='\n')
diagnosis=dict(failure_class='IMPLEMENTATION_FAILED',actual_root_PID=os.getpid(),first_compile='focused-generic-first/receipt.json',first_compile_PID=13416,first_compile_EXIT=1,issue='IsSelfAdjoint.isSymmetric yields a coerced linear-map application which rw does not syntactically match. Typed local equalities expose the same mathematically definitionally equal CLM applications.',mathematical_statement_changed=False,new_assumptions=[],same_route_repeats=0,old_RAW_sha256=hashlib.sha256(raw).hexdigest(),new_RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),failed_axiom_print_not_certificate=True,salvage='Already elaborated inverse/square/linear identities retained; failed whole module grants no compiled theorem credit.')
(out/'diagnosis.json').write_text(json.dumps(diagnosis,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
sys.path.insert(0,str(Path('tools').resolve()));import astis_advance as adv
claim=json.loads((r/'claim.json').read_bytes())
adv.checkpoint_advance(claim['advance_id'],worker_id=claim['created_by'],route_fingerprint='Hilbert-perturbation/typed-selfadjoint-inner-equalities',progress_signature='first-13416EXIT1-coercion-pattern-diagnosed-no-mathematical-change',mathematical_delta=claim['theorem_delta'],exact_residual='Compile exact unchanged generic statement after typed coercion normalization, then actual consumer and independent reviews.')
print('TYPED compiler diagnosis recorded; exact sealed statement unchanged.')
