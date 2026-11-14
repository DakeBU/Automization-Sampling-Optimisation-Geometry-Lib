from pathlib import Path
from html.parser import HTMLParser
import re,json,hashlib
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC');OUT=ROOT/'.astis/semantic-neutral-20261109/src_9a6d2f/phase3';BASE=ROOT/'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-geometry-semantic-evidence/source-only-review/phase2'
s=(ROOT/'.astis/huanjian-resume-20261103/2610.20492v1.html').read_text()
def span(anchor):
 m=re.search(r'<([A-Za-z0-9]+)\b[^>]*\bid="'+re.escape(anchor)+r'"[^>]*>',s);assert m;tag=m.group(1);depth=0
 for t in re.finditer(r'</?'+tag+r'\b[^>]*>',s[m.start():]):
  depth+=-1 if t.group().startswith('</') else 1
  if depth==0:return m.start(),m.start()+t.end()
 raise ValueError(anchor)
class Enumerate(HTMLParser):
 def __init__(self,raw,base):super().__init__(convert_charrefs=True);self.offsets=[0];self.base=base;self.units=[];self.atoms=[]
 def feed_raw(self,raw):
  for i,c in enumerate(raw):
   if c=='\n':self.offsets.append(i+1)
  self.feed(raw)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);cl=a.get('class','').split();id=a.get('id');line,col=self.getpos();offset=self.base+self.offsets[line-1]+col
  if tag=='p' and 'ltx_p' in cl or tag=='table' and 'ltx_equation' in cl or 'ltx_theorem' in cl or 'ltx_bibitem' in cl:
   if id:self.units.append(id)
  if tag=='math':assert id;self.atoms.append(id)
  elif tag=='a':self.atoms.append('link@'+str(offset))
regions=['S2','S4.SS1','S4.Thmtheorem6','A3.SS4','S4.SS2.SSS0.Px4.p1.1','S4.Thmtheorem1','bib.bib3'];units=[];atoms=[]
for region in regions:
 i,j=span(region);p=Enumerate(s[i:j],i);p.feed_raw(s[i:j]);units+=p.units;atoms+=p.atoms
coverage=json.loads((BASE/'source-coverage-v2.proposal.json').read_text());u={x['anchor'] for x in coverage['paragraph_and_display_inventory']};a={x['atom_id'] for x in coverage['formula_and_citation_inventory']}
report={'independently_enumerated_regions':regions,'source_units':len(units),'formula_link_atoms':len(atoms),'inventory_unit_count':len(u),'inventory_atom_count':len(a),'missing_units':sorted(set(units)-u),'extra_units':sorted(u-set(units)),'missing_atoms':sorted(set(atoms)-a),'extra_atoms':sorted(a-set(atoms)),'duplicate_unit_ids':len(units)-len(set(units)),'duplicate_atom_ids':len(atoms)-len(set(atoms)),'scope':'Exact explicitly bounded source inventory; no claim of all Section4.3/downstream proof coverage.'}
(OUT/'source-coverage-completeness.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
assert not any(report[k] for k in ('missing_units','extra_units','missing_atoms','extra_atoms','duplicate_unit_ids','duplicate_atom_ids'))
