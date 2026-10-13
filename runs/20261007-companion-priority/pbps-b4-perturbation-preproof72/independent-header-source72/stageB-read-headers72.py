import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os,re
B=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent;R=O.parent
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return {'path':p.relative_to(B).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(lf),'LF_sha256':sha(lf)}
inputs=[]
for i,(name,digest,size) in enumerate([('header72.generic.proposed.lean','d1435ac883ab1ba0d2b763a8094664d3eba18970a0fa8ff9cd051dc2966fdd8a',761),('header72.actual.named-literal.proposed.lean','bb6eaa684a81dbf74d7778e8fa6e98f15c1b443fa3c1e0ec4d2b36560b1ab88d',9016)]):
 p=R/name;b=p.read_bytes();assert len(b)==size and sha(b)==digest
 raw=f'stageB.input.{i:02}.exactraw.snapshot.lean';lf=f'stageB.input.{i:02}.LF.snapshot.lean';(O/raw).write_bytes(b);(O/lf).write_bytes(b.replace(b'\r\n',b'\n'));inputs.append({**pin(p),'snapshot':raw,'LF_snapshot':lf,'role':'authorized72prospectiveheaderONLY; noimplementation/proofBODY'})
 print('\nEXACT HEADER '+name+'\n'+b.decode())
parent=B/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean';b=parent.read_bytes();assert sha(b)=='f321d13c612a3702e3d42043a49fff8feb3b76bb302638a60f9dad4cb166ad1a'
a=b.index(b'private def ');z=b.index(b'\ntheorem ',a);fragment=b[a:z];(O/'stageB.parent71.literal.exactraw.fragment.lean').write_bytes(fragment);(O/'stageB.parent71.literal.LF.fragment.lean').write_bytes(fragment.replace(b'\r\n',b'\n'))
publicstart=z+1;publicend=b.index(b' := by',publicstart)+len(b' := by');public=b[publicstart:publicend];(O/'stageB.parent71.public.exactraw.fragment.lean').write_bytes(public);(O/'stageB.parent71.public.LF.fragment.lean').write_bytes(public.replace(b'\r\n',b'\n'))
inputs.append({**pin(parent),'role':'opaque full-parent RAW/LF pin; mathematically inspect ONLY complete literal and public header fragments','fragments':[{'snapshot':'stageB.parent71.literal.exactraw.fragment.lean','LF_snapshot':'stageB.parent71.literal.LF.fragment.lean','RAW_start':a,'RAW_end_exclusive':z,'RAW_bytes':len(fragment),'RAW_sha256':sha(fragment)},{'snapshot':'stageB.parent71.public.exactraw.fragment.lean','LF_snapshot':'stageB.parent71.public.LF.fragment.lean','RAW_start':publicstart,'RAW_end_exclusive':publicend,'RAW_bytes':len(public),'RAW_sha256':sha(public)}],'parent_BODY_reread':False})
(O/'stageB.exact-header-input-manifest72.json').write_text(json.dumps({'schema':'source72-exact-prospective-header-input-manifest-v1','actual_pid':os.getpid(),'inputs':inputs,'LF_recipe':'ONLY byte CRLF to LF; preserve every otherbyte','candidate72_BODY_or_otheragent_math_sourceplan_verdict_read':False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('\nEXACT CURRENT PARENT71 COMPLETE LITERAL AND PUBLIC HEADER ONLY\n'+fragment.decode()+'\n'+public.decode())
print(json.dumps({'actual_pid':os.getpid(),'status':'AUTHORIZED_EXACT_TWO_HEADERS_AND_PARENT_LITERAL_PINNED','candidate72proofBODY_exists_or_read':False,'current_parent_BODY_reread':False},indent=2))
