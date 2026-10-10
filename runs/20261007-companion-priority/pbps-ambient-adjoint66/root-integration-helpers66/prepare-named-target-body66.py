from pathlib import Path
import hashlib,json
pre=Path('runs/20261007-companion-priority/pbps-ambient-adjoint-preproof66')
r=Path('runs/20261007-companion-priority/pbps-ambient-adjoint66')
p=pre/'independent-type-diagnosis66/exact-Prop-expression0.lean';raw=p.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='3a1f869d16f5c859ea801d6e54b08345060165094f23fc56bb737816fcca2396'
text=raw.decode().replace('\r\n','\n');(r/'named-target66.exactraw.snapshot.lean').write_bytes(raw)
prod=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/AmbientAdjointCorrector.lean').read_text(encoding='utf-8')
body=prod.split('\n:= by\n')[1].split('\nend\n')[0]
body='\n'.join(x for x in body.splitlines() if 'trace "TRACE66' not in x)+'\n'
header=(pre/'header0.lean').read_text(encoding='utf-8')
binders=header[:header.index(' :\n')].replace('actual_ambient_adjoint_centered_decomposition','actual_body66',1)
theorem=binders+' :\n    exact_Prop_expression0 (E:=E) (V:=V) (α:=α) (β:=β) (η:=η) hα hαβ hV hH hη hβη := by\n  unfold exact_Prop_expression0\n'+body
out=r/'named-target-body66.lean';assert not out.exists()
text=text[:text.index('#check exact_Prop_expression0')]+theorem+'\nend\nend IndependentTypeDiagnosis66\n'
out.write_text(text,encoding='utf-8',newline='\n')
print('Named exact-Prop66 scratch proof; immutable copied source pin; canonical statement/proof unchanged; compilation unrun.')
