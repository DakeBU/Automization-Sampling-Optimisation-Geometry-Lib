from pathlib import Path
import copy,hashlib,json,sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'));import astis_publication as pub,astis_semantic_roundtrip as rt
r=root/'runs/20261007-companion-priority/pbps-centered-root64'
load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 b=p.read_bytes();return dict(path=p.resolve().as_posix(),bytes=len(b),raw_sha256=hashlib.sha256(b).hexdigest(),lf_sha256=hashlib.sha256(b.replace(b'\r\n',b'\n')).hexdigest())
def replace(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
native=load(Path(sys.argv[1]));assert native.get('status',native.get('state')) in ['CLOSED','CLOSED_LAST']
codepaths=[root/p for p in load(r/'claim.json')['proposed_files']];before=[pin(p) for p in codepaths]
slug='pbps-centered-root-order-inverse';aid='ASTIS-RT-20261009-PBPSCenteredRootOrderInverse'
dp=r/'exposition.draft.json';lp=root/'website/content/declaration_lessons'/f'{slug}.json';ap=root/'research-wiki/semantic-roundtrip/audits'/f'{aid}.json'
d=r/'step6-presentation-repair64';d.mkdir(exist_ok=False);oldmaps=[]
for p in [dp,lp,ap]:
 sp=d/(p.parent.name+'-'+p.name+'.before.exactraw.snapshot');sp.write_bytes(p.read_bytes());oldmaps.append(dict(original=pin(p),explicit_exact_raw_snapshot=pin(sp)))
s=codepaths[1].read_text(encoding='utf-8');body=s.index(':= by')+len(':= by');a=s.index('  let qP :',body);b=s.index('  have hCoerc',a);code=s[a:b].rstrip()+'\n'
row=dict(path=codepaths[1].relative_to(root).as_posix(),source_raw_sha256=before[1]['raw_sha256'],start_line=s[:a].count('\n')+1,end_line=s[:b].count('\n'),exact_code_raw_sha256=hashlib.sha256(code.encode()).hexdigest())
draft=load(dp);lesson=load(lp);old=copy.deepcopy(lesson['units'][0]['steps'][5])
assert old['title']=='Restrict the same transported root to the exact centered space'
assert old['lean_source_region']['start_line']<s[:body].count('\n')+1
for step in [draft['units'][1]['steps'][5],lesson['units'][0]['steps'][5]]:step.update(lean=code,lean_source_region=row)
replace(dp,draft);replace(lp,lesson)
pub.inputs.cache_clear();pub.load.cache_clear();data=pub.inputs();item=next(x for x in pub.load() if x['id']==slug);binding=item['bindings'][0];audit=load(ap)
assert audit['state']=='draft';audit['publication_binding_sha256']=pub.binding_digest(item,binding,data);audit['publication_context']=pub.review_context(item,binding,data)
assert rt.decoder_packet(audit)==load(root/'.astis/decoder-64/packet1.json');replace(ap,audit)
assert before==[pin(p) for p in codepaths]
checked=[]
for slug0 in load(r/'publication-plan.json')['slugs']:
 unit=load(root/'website/content/declaration_lessons'/f'{slug0}.json')['units'][0]
 for i,st in enumerate(unit['steps']):
  q=st['lean_source_region'];fp=root/q['path'];text=fp.read_text(encoding='utf-8');lines=text.splitlines(keepends=True);literal=''.join(lines[q['start_line']-1:q['end_line']])
  assert literal==st['lean'] and hashlib.sha256(literal.encode()).hexdigest()==q['exact_code_raw_sha256'],(slug0,i)
  assert q['start_line']>text[:text.index(':= by')].count('\n')+1,(slug0,i,'header instead of proof')
  assert pin(fp)['raw_sha256']==q['source_raw_sha256'];checked.append(dict(slug=slug0,step=i+1,region=q))
record=dict(status='STEP6_BODY_EXCERPT_CORRECTED_SEPARATE_INDEPENDENT_PRESENTATION_ACCEPTANCE_PENDING',cause='The source search selected the first same-named qP let in the theorem header. Restrict the search to after the theorem proof delimiter.',old_region=old['lean_source_region'],new_region=row,finite_historical_maps=oldmaps,original_immutable_math_freeze=pin(r/'math-freeze.json'),current=[pin(dp),pin(lp),pin(ap)],all12_literal_body_regions_checked=checked,production_unchanged=before,anonymous_packet_unchanged=pin(root/'.astis/decoder-64/packet1.json'),source_statement_or_mathematical_repair=False,full_ExpositionSeal=False)
replace(d/'supplement.json',record)
pub.check_advance(load(r/'publication-plan.json')['mathematical_declarations'],reviewed=False)
print('Presentation-only step6 fixed to exact BODY region;',row['start_line'],row['end_line'],';all12 RAW literal regions checked. Independent source/exposition admission still required.')
