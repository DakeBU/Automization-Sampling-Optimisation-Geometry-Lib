from pathlib import Path
import hashlib,json
p=Path('runs/20261007-companion-priority/pbps-macro-root63/macro-root-draft.lean')
b=p.read_bytes()
q=p.with_name('macro-root-draft.v2.failed.exactraw.snapshot.lean')
assert not q.exists();q.write_bytes(b)
s=b.decode('utf-8')
s=s.replace('  have hAeq : A=e.conjStarAlgEquiv T := by\n    ext f\n    apply Subtype.ext','  have hAeq : A=e.conjStarAlgEquiv T := by\n    apply ContinuousLinearMap.ext\n    intro f\n    apply Subtype.ext')
s=s.replace('  have hB0Gram : B0.adjoint ∘L B0=P-AJ*AJ := by\n    simpa only [pow_two] using hBB','  have hB0Gram : B0.adjoint ∘L B0=P-AJ*AJ := by\n    have hBBtyped : B0.adjoint ∘L B0 = P-AJ^2 := hBB\n    simpa only [pow_two] using hBBtyped')
s=s.replace('        ext f\n        rw [HP.adjoint_subtypeL]','        apply ContinuousLinearMap.ext\n        intro f\n        rw [HP.adjoint_subtypeL]')
assert s!=b.decode('utf-8')
p.write_text(s,encoding='utf-8',newline='\n')
print(json.dumps({'archived_v2':str(q),'v2_sha256':hashlib.sha256(b).hexdigest(),'header_unchanged':True,'change':'Bound ext to CLM; explicitly type full-joint Gram identity before pow_two.'}))
