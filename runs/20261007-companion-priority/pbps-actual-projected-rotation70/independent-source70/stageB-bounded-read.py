import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,os
O=pathlib.Path(__file__).resolve().parent
mode=sys.argv[1];print('actual_pid='+str(os.getpid()))
if mode=='module':
 a,z=map(int,sys.argv[2:4]);s=(O/'current70.source_body.exactraw.lean').read_text(encoding='utf-8').splitlines();print('\n'.join(str(i+1)+': '+s[i] for i in range(a-1,z)))
elif mode=='blind':
 p=json.loads((O/'current70.official-source-review.packet.0.exactraw.json').read_bytes());print(json.dumps(p['blind_reconstruction'],ensure_ascii=False,indent=2));a=json.loads((O/'current70.audit.exactraw.json').read_bytes());print('reconstruction-keys',list(a['reconstruction']));print('publication binding',p['publication_binding_sha256']);print('contract',json.dumps(p['output_contract'],ensure_ascii=False,indent=2))
elif mode=='publication':
 p=json.loads((O/'current70.publication.exactraw.json').read_bytes());print(json.dumps(p,ensure_ascii=False,indent=2));l=json.loads((O/'current70.lesson.exactraw.json').read_bytes());print('LESSON KEYS',list(l));print('LESSON STRUCTURE',[(k,type(v).__name__,len(v) if hasattr(v,'__len__') else None) for k,v in l.items()])
elif mode=='lesson':
 l=json.loads((O/'current70.lesson.exactraw.json').read_bytes());print(json.dumps(l,ensure_ascii=False,indent=2))
elif mode=='packet-context':
 p=json.loads((O/'current70.official-source-review.packet.0.exactraw.json').read_bytes());c=p['candidate_publication_context'];print('contextkeys',list(c));print(json.dumps({k:v for k,v in c.items() if k!='lesson_unit'},ensure_ascii=False,indent=2))
else:raise ValueError(mode)
