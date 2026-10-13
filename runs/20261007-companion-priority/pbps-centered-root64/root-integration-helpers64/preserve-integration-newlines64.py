from pathlib import Path
import difflib,hashlib,json,subprocess
r=Path('runs/20261007-companion-priority/pbps-centered-root64');assert (r/'root.exact-verification64.adoption.json').exists()
paths=['AutoSamplingTheory/TechnicalLemmas.lean','AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json']+['research-wiki/frontier-cells/'+x+'.json' for x in json.loads((r/'publication-plan.json').read_bytes())['active_cells']]
records=[]
sha=lambda b:hashlib.sha256(b).hexdigest()
for name in paths:
 p=Path(name);old=subprocess.check_output(['git','show','HEAD:'+name]);new=p.read_bytes();ol=old.splitlines(keepends=True);nl=new.replace(b'\r\n',b'\n').splitlines(keepends=True);norm=[x.replace(b'\r\n',b'\n') for x in ol];newline=b'\r\n' if old.count(b'\r\n')>old.count(b'\n')/2 else b'\n';parts=[]
 for kind,a,b,c,d in difflib.SequenceMatcher(a=norm,b=nl,autojunk=False).get_opcodes():
  parts.extend(ol[a:b] if kind=='equal' else [x[:-1]+newline if x.endswith(b'\n') else x for x in nl[c:d]])
 result=b''.join(parts);assert result.replace(b'\r\n',b'\n')==new.replace(b'\r\n',b'\n');p.write_bytes(result);records.append(dict(path=name,before_raw_sha256=sha(new),after_raw_sha256=sha(result),lf_sha256=sha(result.replace(b'\r\n',b'\n')),semantic_changes=False,unchanged_lines_retain_HEAD_exact_endings=True))
(r/'integration64/newline-preservation.json').write_text(json.dumps(dict(scope='Root-owned integration administration and aggregation only; science64 proof files/native CLOSED artifacts untouched',records=records),indent=2)+'\n',encoding='utf-8',newline='\n')
print('Preserved exact HEAD line endings on unchanged owned integration lines; normalized content unchanged in',len(records),'files. Mandatory compiler gate follows these exact bytes.')
