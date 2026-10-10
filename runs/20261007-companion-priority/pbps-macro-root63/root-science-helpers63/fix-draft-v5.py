from pathlib import Path
import hashlib,json
p=Path('runs/20261007-companion-priority/pbps-macro-root63/macro-root-draft.lean');b=p.read_bytes();q=p.with_name('macro-root-draft.v4.failed.exactraw.snapshot.lean');assert not q.exists();q.write_bytes(b)
s=b.decode('utf-8').replace('set_option diagnostics true','set_option diagnostics false')
mark=':= by\n  classical';a=s.index(mark);header=s[:a];body=s[a:]
body=body.replace('  let HP := lpMeas ℝ ℝ mY 2 J\n','  let HP := lpMeas ℝ ℝ mY 2 J\n  letI : NormedAddCommGroup HP := HP.normedAddCommGroup\n  letI : InnerProductSpace ℝ HP := HP.innerProductSpace\n')
body=body.replace('simpa only [LinearIsometryEquiv.conjStarAlgEquiv_apply,e.adjoint_eq_symm] using\n      hΓ.conj_adjoint','simpa only [ΓP,LinearIsometryEquiv.conjStarAlgEquiv_apply,e.adjoint_eq_symm] using\n      hΓ.conj_adjoint')
body=body.replace('simpa only [LinearIsometryEquiv.conjStarAlgEquiv_apply,e.symm.adjoint_eq_symm] using\n        hG.conj_adjoint','simpa only [G0,LinearIsometryEquiv.conjStarAlgEquiv_apply,e.symm.adjoint_eq_symm] using\n        hG.conj_adjoint')
body=body.replace('e.symm_apply_apply,e.apply_symm_apply]','LinearIsometryEquiv.symm_symm,e.symm_apply_apply,e.apply_symm_apply]')
p.write_text(header+body,encoding='utf-8',newline='\n')
record={'failed_v4_raw_sha256':hashlib.sha256(b).hexdigest(),'diagnosis':'Positive-conjugation let aliases not unfolded; symm.symm not simplified in two local operator equalities; repeated synthesis of HP normed subtype times out20000 inside map laws. Whole declaration whnf timeout absent.','repair':'Unfold ΓP/G0 at positivity transfer; simplify actual symm_symm; cache internally-derived canonical HP normed/inner-product instances. No source/public binder change.','no_compilation_credit':True}
p.with_name('v4.compiler-diagnosis.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(record))
