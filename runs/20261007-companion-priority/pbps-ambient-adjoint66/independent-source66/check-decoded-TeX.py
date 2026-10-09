from pathlib import Path
import json,hashlib,os,datetime
O=Path(r'E:/Samplinglib/runs/20261007-companion-priority/pbps-ambient-adjoint66/independent-source66')
paths=[Path(r'E:/Samplinglib/website/content/publications/pbps-ambient-adjoint-corrector.json'),Path(r'E:/Samplinglib/website/content/declaration_lessons/pbps-ambient-adjoint-corrector.json'),O.parent/'exposition.draft.json'];out=[]
for p in paths:
 b=p.read_bytes();d=json.loads(b)
 fields=[]
 def walk(v,path=''):
  if isinstance(v,dict):
   for k,x in v.items():
    q=path+'.'+k if path else k
    if k in ['formula','tex'] and isinstance(x,str):fields.append((q,x))
    else:walk(x,q)
  elif isinstance(v,list):
   for j,x in enumerate(v):walk(x,path+'[%d]'%j)
 walk(d)
 out.append(dict(path=str(p).replace('\\','/'),RAW_sha256=hashlib.sha256(b).hexdigest(),formulae=[dict(field=k,backslash_count=v.count(chr(92)),adjacent_backslash_pairs=v.count(chr(92)*2),head_decoded_codepoints=list(map(ord,v[:45]))) for k,v in fields]))
assert all(x['adjacent_backslash_pairs']==0 for row in out for x in row['formulae'])
correction=dict(schema='source66-retained-TeX-false-positive-correction-v1',actual_foreground_pid=os.getpid(),observed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),checks=out,finding_retracted='Claim that decoded TeX formula strings contain doubled literal backslashes',reason='The review mistook JSON serialization escaping for decoded TeX characters. All actual decoded formula strings have zero adjacent backslash pairs; renderer direct insertion is appropriate.',formula_changes_required=False,source_mathematical_repair=False,prior_finding_preserved='reader-presentation-debt.initial.false-positive-retained.json',remaining_dependency_catalogue_omission=True)
(O/'reader-presentation-debt.initial.false-positive-retained.json').write_bytes((O/'reader-presentation-debt.json').read_bytes())
(O/'TeX-false-positive-correction.json').write_bytes((json.dumps(correction,sort_keys=True,indent=2)+'\n').encode())
debt=json.loads((O/'reader-presentation-debt.json').read_bytes());debt['debts']=[x for x in debt['debts'] if x['kind']!='literal-TeX-escaping'];debt['TeX_finding_retracted_with_evidence']='TeX-false-positive-correction.json';(O/'reader-presentation-debt.json').write_bytes((json.dumps(debt,sort_keys=True,indent=2)+'\n').encode())
(O/'negative.TeX-observer-one-liner-syntax.json').write_bytes((json.dumps(dict(schema='source66-preserved-observer-negative-v1',tool_chunk='c7125e',actual_tool_exit=1,pid_not_captured=True,issue='Malformed Python observer comprehension; no candidate or formula evaluation occurred; replaced with bounded owned script',candidate_failure=False),sort_keys=True,indent=2)+'\n').encode())
print(json.dumps(correction,sort_keys=True))