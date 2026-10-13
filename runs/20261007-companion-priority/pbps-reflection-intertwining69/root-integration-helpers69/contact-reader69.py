from pathlib import Path
import json
from PIL import Image,ImageOps,ImageDraw
source=Path('.astis/pbps-sharp-energy68/visual69-cdp');out=Path('.astis/pbps-sharp-energy68/visual69-contacts');out.mkdir(exist_ok=False)
cap=json.loads((source/'capture.json').read_bytes());assert len(cap['records'])==8 and cap['ownedBrowserExit']['code']==0
steps=[]
for item in cap['records']:
 assert item['bodyVisibility']=='visible' and item['bodyDisplay']!='none' and item['targetRect']['width']>0 and item['targetRect']['height']>0
 if '-proof-' in item['label']:
  assert item['mathContainers']>0
  steps.append(source/(item['label']+'.png'))
assert len(steps)==6
records=[]
for i in range(0,6,4):
 canvas=Image.new('RGB',(2880,1440),'white');draw=ImageDraw.Draw(canvas)
 for j,p in enumerate(steps[i:i+4]):
  im=Image.open(p).convert('RGB');crop=im.crop((0,0,1440,680));x=(j%2)*1440;y=(j//2)*720
  canvas.paste(crop,(x,y+30));draw.text((x+10,y+8),p.stem,fill='black')
 q=out/f'proof-steps-{i+1}-{min(i+4,6)}.png';canvas.save(q);records.append(q.as_posix())
(out/'inspection-manifest.json').write_text(json.dumps(dict(source_capture=source.as_posix(),all6_steps_have_visible_positive_rectangles_and_rendered_math=True,contacts=records,scope='Root visual QA overview crops only; original complete1440x1800 screenshots preserved.'),indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS eight captures/six rendered proof steps; contact previews created; original images unchanged.')
