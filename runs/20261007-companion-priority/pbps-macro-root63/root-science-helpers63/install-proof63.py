from pathlib import Path
import hashlib,json,re
r=Path('runs/20261007-companion-priority/pbps-macro-root63');pre=Path('runs/20261007-companion-priority/pbps-macro-root-preproof63')
q=json.loads((r/'focused-macro-and-consumer-v7/receipt.json').read_bytes());assert q['exit_code']==0 and q['terminal_closed'];p=r/'macro-root-draft.lean';b=p.read_bytes();assert q['inputs'][0]['raw_sha256']==hashlib.sha256(b).hexdigest()
s=b.decode('utf-8');a=s.index('namespace Tests.ProximalBPSMacroscopicDefectRoot');main=s[:a].rstrip()+'\n';test=s[a:]
headers=[]
for i,text in enumerate([main,test]):
 header=(pre/f'header{i}.lean').read_text(encoding='utf-8').rstrip();assert header in text
 assert not re.search(r'\b(sorry|admit|axiom)\b|Prop\s*:=\s*True|:=\s*trivial',text)
 headers.append(dict(sealed_header=(pre/f'header{i}.lean').as_posix(),raw_sha256=hashlib.sha256((pre/f'header{i}.lean').read_bytes()).hexdigest(),all_binders_and_lets_literal_match=True,only_trailing_blank_line_normalization=True))
main_path=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicDefectRoot.lean');test_path=Path('Tests/ProximalBPSMacroscopicDefectRoot.lean');assert not main_path.exists() and not test_path.exists()
prefix='import AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicDefectRoot\nopen MeasureTheory ProbabilityTheory\nopen scoped ContDiff NNReal ENNReal Topology\nset_option autoImplicit false\nset_option maxHeartbeats 3200000\n\n'
main_path.write_text(main,encoding='utf-8',newline='\n');test_path.write_text(prefix+test,encoding='utf-8',newline='\n')
old=Path('.astis/pbps-macro-root63/proof-gate63.py').read_text(encoding='utf-8');old=old.replace("math=['runs\\\\20261007-companion-priority\\\\pbps-macro-root63\\\\macro-root-draft.lean',", "math=['AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicDefectRoot.lean','Tests/ProximalBPSMacroscopicDefectRoot.lean',")
assert "math=['AutoSamplingTheory" in old
Path('.astis/pbps-macro-root63/focused-gate63.py').write_text(old,encoding='utf-8',newline='\n')
record=dict(status='SCRATCH63_COMPILED_INSTALLED_FOR_FOCUSED_CHECK_NOT_VERIFIED',v7_receipt=(r/'focused-macro-and-consumer-v7/receipt.json').as_posix(),v7_actual_pid=q['actual_foreground_pid'],headers=headers,owned_files=[str(main_path),str(test_path)],no_shared_import_Registry_or_site_edits=True,private_providers=[],remaining='Independent proof/decoder/source/publication and exact-commit verification pending; centered order/inverse/polar/H1/dynamics/main/error/querycost/composition open.')
(r/'installation63.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(record))
