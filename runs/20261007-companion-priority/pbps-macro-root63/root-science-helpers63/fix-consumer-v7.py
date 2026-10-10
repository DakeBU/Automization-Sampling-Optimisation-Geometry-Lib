from pathlib import Path
import hashlib,json
r=Path('runs/20261007-companion-priority/pbps-macro-root63');p=r/'macro-root-draft.lean';b=p.read_bytes();q=r/'macro-root-draft.v6.consumer-negative.exactraw.snapshot.lean';assert not q.exists();q.write_bytes(b)
s=b.decode('utf-8');a=s.index('namespace Tests.ProximalBPSMacroscopicDefectRoot');head=s[:a];test=s[a:]
test=test.replace(' := by\n  classical\n  dsimp only',' := by\n  classical\n  let mY : MeasurableSpace (E × E) :=\n    MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E)\n  letI : MeasurableSpace (E × E) := Prod.instMeasurableSpace\n  letI : Fact (mY ≤ (inferInstance : MeasurableSpace (E × E))) :=\n    ⟨measurable_snd.comap_le⟩\n  dsimp only')
assert test!=s[a:];p.write_text(head+test,encoding='utf-8',newline='\n');(r/'consumer63.body-and-header.lean').write_text(test,encoding='utf-8',newline='\n')
print(json.dumps({'failed_v6_raw_sha256':hashlib.sha256(b).hexdigest(),'main_proof_unchanged':True,'diagnosis':'Consumer dsimp removed the signature-scoped Fact(mY≤ambient) from typeclass context. Derive the SAME product measurability Fact internally before conjugating; no public premise/statement change.'}))
