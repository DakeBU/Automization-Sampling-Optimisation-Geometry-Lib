import sys,os,json,traceback,copy
from pathlib import Path
from types import SimpleNamespace
import final68 as F
import review68 as R
O=R.O;P=R.P;ROOT=R.ROOT;pin=R.pin;sha=R.sha;save=R.save;get=R.get;read=R.read;now=R.now
D=P/'prose-and-span-overlay68-v2'
def diff(a,b,p=''):
 if type(a)!=type(b):return [(p,a,b)]
 if isinstance(a,dict):
  out=[]
  for k in sorted(set(a)|set(b)):
   if k not in a or k not in b:out.append((p+'.'+k,a.get(k),b.get(k)))
   else:out+=diff(a[k],b[k],p+'.'+k)
  return out
 if isinstance(a,list):
  if len(a)!=len(b):return [(p,a,b)]
  out=[]
  for i,(x,y) in enumerate(zip(a,b)):out+=diff(x,y,p+f'[{i}]')
  return out
 return [] if a==b else [(p,a,b)]
def run():
 F.stable();proposal=read(D/'proposal.json');assert pin(D/'proposal.json')['raw_sha256']=='7cf9aa588d6bbbf0843b59b048b6fc58dda10c1dce30f255cf6c3accdadf47b2'
 paths=[D/'proposal.json',P/'prose-overlay68/proposal.json',ROOT/'tools/astis_publication.py']
 for q in proposal['changes']:paths += [D/q['before_snapshot'],D/q['after_snapshot']]
 rows=[]
 for i,path in enumerate(paths):
  b=path.read_bytes();rp=O/f'overlay-inputs/{i:03}.RAW.snapshot';lp=O/f'overlay-inputs/{i:03}.LF.snapshot';rp.parent.mkdir(exist_ok=True);rp.write_bytes(b);lp.write_bytes(b.replace(b'\r\n',b'\n'));rows.append(dict(original=pin(path),RAW_snapshot=pin(rp),LF_snapshot=pin(lp)))
 save('overlay.inputs.manifest.json',dict(actual_PID=os.getpid(),utc=now(),input_count=len(rows),inputs=rows,proposed_not_applied=True))
 assert pin(P/'prose-overlay68/proposal.json')['raw_sha256']==proposal['superseded_proposal_RAW_sha256']=='f5e5289aeedade3b48af64f4745e2dd2c232c42efd2d7e815dcac58296858d8f'
 changes=[];before=[];after=[]
 for q in proposal['changes']:
  old=D/q['before_snapshot'];new=D/q['after_snapshot'];assert pin(old)['raw_sha256']==q['before_raw_sha256'] and pin(new)['raw_sha256']==q['after_raw_sha256']
  assert old.read_bytes()==F.frozen(ROOT/q['path']).read_bytes()
  a=read(old);b=read(new);delta=diff(a,b);assert [p.lstrip('.') for p,_,_ in delta]==sorted(q['changed_fields']),delta
  changes.append(dict(target=q['path'],before=pin(old),after=pin(new),exact_differences=[dict(field=p.lstrip('.'),before=x,after=y) for p,x,y in delta]));before.append(a);after.append(b)
 oldstep=before[0]['units'][0]['steps'][1]['text'];newstep=after[0]['units'][0]['steps'][1]['text'];assert newstep==oldstep.replace('use both inverse identities','use the right inverse identity twice')
 assert after[0]['units'][0]['steps'][4]['lean_source_region']['end_line']==412 and after[0]['units'][0]['steps'][5]['lean_source_region']['end_line']==420
 body=F.frozen(F.MAIN).read_text(encoding='utf-8');coefficient=body.split('have hCoefficient :',1)[1].split('  let γ :',1)[0];assert 'rw [hRight,one_mul,hRight]' in coefficient and 'hLeft' not in coefficient
 strict=[]
 for slug,lesson in [('hilbert-sharp-quadratic-corrector-bound',read(F.frozen(ROOT/'website/content/declaration_lessons/hilbert-sharp-quadratic-corrector-bound.json'))),('pbps-sharp-corrector-energy',after[0])]:
  for i,q in enumerate(lesson['units'][0]['steps']):
   r=q['lean_source_region'];raw=F.frozen(ROOT/r['path']).read_bytes();span=b''.join(raw.splitlines(keepends=True)[r['start_line']-1:r['end_line']]);assert sha(raw)==r['source_raw_sha256'] and span==q['lean'].encode() and sha(span)==r['exact_code_raw_sha256']
   strict.append(dict(slug=slug,step=i+1,start_line=r['start_line'],end_line=r['end_line'],span_RAW_bytes=len(span),span_RAW_sha256=sha(span),strict_RAW_literal_BODY_match=True))
 assert len(strict)==11
 sys.path.insert(0,str(ROOT/'tools'));sys.path.insert(0,str(ROOT/'website/scripts'));import astis_publication as pub
 item=read(F.frozen(ROOT/'website/content/publications/pbps-sharp-corrector-energy.json'))['items'][0];binding=item['bindings'][0];name=binding['declaration'];decl=SimpleNamespace(source_file=F.MAIN.relative_to(ROOT).as_posix())
 for lesson,audit,label in [(before[0],before[1],'before'),(after[0],after[1],'after')]:
  data=dict(declarations={name:decl},lessons={name:lesson['units'][0]});assert pub.binding_digest(item,binding,data)==audit['publication_binding_sha256'];assert pub.review_context(item,binding,data)==audit['publication_context']
 assert before[1]['publication_binding_sha256']==proposal['old_binding'] and after[1]['publication_binding_sha256']==proposal['proposed_binding']=='dd53a8d89ef3aca6b14d30e4eb6c8284f078050e56f452da0abefc9d4270dd79'
 F.stable();save('presentation-overlay.decision.json',dict(decision='APPROVED_PROPOSED_V2_NOT_APPLIED',actor=R.ACTOR,actual_PID=os.getpid(),utc=now(),proposal=pin(D/'proposal.json'),superseded_V1=pin(P/'prose-overlay68/proposal.json'),complete_before_after_differences=changes,original_frozen_inputs_preserved=True,original44_input_manifest=pin(O/'final.inputs.manifest.json'),original_strict_RAW_spans=9,original_two_negative_intervals_retained=get('formula-BODY.audit.json'),V2_proposed_strict_RAW_spans=11,proposed_strict_intervals=strict,coefficient_explanation='hRight is called twice in hFirst; hLeft is retained but not used in this coefficient proof.',publication_digest_algorithm=pin(ROOT/'tools/astis_publication.py'),old_binding=proposal['old_binding'],proposed_binding=proposal['proposed_binding'],exact_after_context_recomputed=True,mathematical_source_statement_Lean_private_Prop_formulas_code_and_11_excerpts_unchanged=True,current_canonical_before_bytes_still_unchanged=True,canonical_writes=False,approval_scope='Only the exact proposed lesson explanation/endpoints and corresponding audit binding/context. Does not approve future decoder/source statuses or a full Exposition Seal.',VERIFIED=False,PURIFIED=False))
 print(json.dumps(dict(decision='APPROVED_PROPOSED_V2_NOT_APPLIED',actual_PID=os.getpid(),original_strict_RAW=9,retained_negative_maps=2,proposed_strict_RAW=11,binding=proposal['proposed_binding'])))
if __name__=='__main__':
 try:run()
 except Exception as e:
  if not (O/'lease.final.json').exists():save((sys.argv[2] if len(sys.argv)>2 else 'overlay')+'.failure.json',dict(actual_PID=os.getpid(),utc=now(),error=repr(e),traceback=traceback.format_exc()))
  raise
