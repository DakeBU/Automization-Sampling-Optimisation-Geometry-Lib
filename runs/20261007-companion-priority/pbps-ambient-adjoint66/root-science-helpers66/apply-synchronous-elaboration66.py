from pathlib import Path
import hashlib,json
r=Path('runs/20261007-companion-priority/pbps-ambient-adjoint66');pre=Path('runs/20261007-companion-priority/pbps-ambient-adjoint-preproof66')
receipt=json.loads((r/'named-target-body-v1/receipt.json').read_bytes());assert receipt['exit_code']==0 and receipt['terminal_closed']
p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/AmbientAdjointCorrector.lean');old=p.read_bytes()
out=r/'synchronous-elaboration66-v2';out.mkdir(exist_ok=False);(out/'production.before.exactraw.lean').write_bytes(old)
scratch=(r/'named-target-body66.lean').read_text(encoding='utf-8')
body=scratch.split(' hα hαβ hV hH hη hβη := by\n  unfold exact_Prop_expression0\n')[1].split('\nend\n')[0]
candidate=(pre/'header.candidate.lean').read_text(encoding='utf-8')
new=candidate.replace('set_option autoImplicit false','set_option Elab.async false\nset_option autoImplicit false',1).replace('  ASTIS_UNIMPLEMENTED_BODY66\n',body+'\n')
header=(pre/'header0.lean').read_text(encoding='utf-8');assert header in new
assert header.split(' :\n',1)[1] in scratch
p.write_text(new,encoding='utf-8',newline='\n')
(out/'diagnosis.json').write_text(json.dumps(dict(kind='PINNED_LEAN_THEOREM_ASYNC_ELABORATION_MODE',before_RAW_sha256=hashlib.sha256(old).hexdigest(),after_RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),header_RAW_sha256=hashlib.sha256((pre/'header0.lean').read_bytes()).hexdigest(),sealed_header_unchanged=True,math_body_reused_from_compiled_exact_named_target=(r/'named-target-body-v1/receipt.json').as_posix(),new_target_definition=False,proof_or_source_assumption_changed=False,compilation_unrun=True,diagnosis='Neutral async=false probe reaches valid BODY; named exact-Prop full mathematics compiled. Test exact original inline target with synchronous theorem elaboration before adding any permanent representation adapter.'),indent=2)+'\n',encoding='utf-8',newline='\n')
print('Original exact sealed header/compiled body retained; only synchronous Lean elaboration mode added; no new definition/premise.')
