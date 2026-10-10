from pathlib import Path
import hashlib,json
pre=Path('runs/20261007-companion-priority/pbps-ambient-adjoint-preproof66');r=Path('runs/20261007-companion-priority/pbps-ambient-adjoint66')
d=pre/'independent-type-diagnosis66';p=d/'proposed-named-adapter0.lean';raw=p.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='0c092201c993dc2ee251ff4b207ee8162c4ac11f51aa63daa417c0ac8e62a423'
text=raw.decode().replace('\r\n','\n')
name='actual_ambient_adjoint_centered_decomposition_statement'
text=text.replace('namespace IndependentTypeDiagnosis66','namespace AutoSamplingTheory.ExampleCases.ProximalBPS.AmbientAdjointCorrector',1).replace('end IndependentTypeDiagnosis66','end AutoSamplingTheory.ExampleCases.ProximalBPS.AmbientAdjointCorrector',1)
text=text.replace('def '+name,'private def '+name,1)
text=text.replace('#check '+name+'\n','')
scratch=(r/'named-target-body66.lean').read_text(encoding='utf-8')
body=scratch.split(' hα hαβ hV hH hη hβη := by\n  unfold exact_Prop_expression0\n')[1].split('\nend\n')[0]
assert text.count('  fail "INTENTIONAL_NAMED_PROP_BODY_REACHED66"')==1
text=text.replace('  fail "INTENTIONAL_NAMED_PROP_BODY_REACHED66"','  unfold '+name+'\n'+body.rstrip())
prod=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/AmbientAdjointCorrector.lean')
out=r/'private-statement-representation66';out.mkdir(exist_ok=False);(out/'production.before.exactraw.lean').write_bytes(prod.read_bytes())
prod.write_text(text,encoding='utf-8',newline='\n')
(out/'overlay.applied.json').write_text(json.dumps(dict(kind='SOURCE_EQUIVALENT_PRIVATE_STATEMENT_REPRESENTATION',source_proposal=p.as_posix(),source_proposal_RAW_sha256=hashlib.sha256(raw).hexdigest(),production_RAW_sha256=hashlib.sha256(prod.read_bytes()).hexdigest(),original_public_binders_unchanged=True,literal_original_conclusion_in_private_definition=True,mathematical_provider=False,extra_public_premises=[],root_BODY_from=(r/'named-target-body-v1/receipt.json').as_posix(),process_review='Independent source reviewer approved exact public named statement and prefix-only private def overlay; all neutral probes and previous unsupported inline routes retained.',source_mathematical_repair=False,compiler_credit_pending=True),indent=2)+'\n',encoding='utf-8',newline='\n')
print('Exact source-approved statement value in one private definition; same original theorem binders; compiled scratch BODY reused; no new mathematical premise.')
