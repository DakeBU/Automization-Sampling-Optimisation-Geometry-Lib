from pathlib import Path
import json,hashlib,re

pre=Path('runs/20261007-companion-priority/pbps-sharp-energy-preproof68')
r=Path('runs/20261007-companion-priority/pbps-sharp-energy68')
seal=json.loads((pre/'root.statement-seal68.json').read_bytes())
claim=json.loads((r/'claim.json').read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
rows=[]
for i,f in enumerate(claim['proposed_files']):
 s=Path(f).read_text(encoding='utf-8');short=claim['target_declarations'][i].rsplit('.',1)[1]
 for z in seal['headers'][i].values():assert sha(Path(z['path']).read_bytes())==z['RAW_sha256']
 h=(pre/f'header{i}-expanded.lean').read_text(encoding='utf-8');h=h[h.index('theorem '):].rstrip()
 a=s.index('theorem '+short);b=s.index(':= by',a);actual=s[a:b].rstrip()
 if i==0:assert re.sub(r'\s+','',actual)==re.sub(r'\s+','',h)
 else:
  d=(pre/f'statement{i}.definition.lean').read_text(encoding='utf-8');da=s.index('private def ');db=s.index('\ntheorem ',da)
  assert s[da:db].rstrip()+'\n'==d.rstrip()+'\n'
  assert re.sub(r'\s+','',actual[:actual.index(' : '+short+'_statement')])==re.sub(r'\s+','',h[:h.index(' :\n    let μ')])
  assert len(re.findall(r'^private def ',s,re.M))==1 and not re.findall(r'^private (?:theorem|lemma|abbrev) ',s,re.M)
 assert not re.search(r'\b(sorry|admit|axiom)\b|Prop\s*:=\s*True|:=\s*trivial',s)
 rows.append(dict(file=f,current_RAW_sha256=sha(Path(f).read_bytes()),sealed_header_RAW_sha256=seal['headers'][i]['header']['RAW_sha256'],original_callers_exact=True,private_statement_only=i>0))
assert 'import Tests.' not in Path(claim['proposed_files'][1]).read_text(encoding='utf-8')
p=r/'seal-readback68.json';assert not p.exists();p.write_text(json.dumps(dict(status='EXACT_ORIGINAL_CALLERS_AND_LITERAL_STATEMENT_READBACK',rows=rows,compiler_credit=False,source_review_credit=False),indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS all3 sealed original headers and full literal definitions; no extra provider/consumer premise; not compiler/source acceptance.')
