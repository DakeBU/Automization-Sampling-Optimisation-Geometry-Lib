from pathlib import Path
import json
r=Path('runs/20261007-companion-priority/pbps-real-root-unique62');n=Path('runs/20261007-companion-priority/pbps-real-root-unique-preproof62/independent-preproof62');review=json.loads((n/'statement-binder.review.json').read_bytes())
for i,cid in enumerate(['ASTIS-SHARED-l2-positive-real-root-uniqueness','ASTIS-SW-PBPS-real-defect-root-uniqueness']):
 p=Path('research-wiki/frontier-cells')/(cid+'.json');(r/f'cell.{i}.before-metadata-correction62.exactraw.snapshot.json').write_bytes(p.read_bytes());x=json.loads(p.read_bytes());searched=['Samplinglib actual60 canonical positive complex lift and actual61 positive REAL root; pinned Mathlib complex CFC.sqrt_unique and equality-of-positive-squares APIs, independently inspected in source/API scout62 and preproof62.'];x['shared_floor_audit']['searched']=searched;x['reuse_plan']['searched_existing']=searched
 for ref in x['source_detail_audit']['consulted']:
  ref['expanded_binder_audit']=review['generic' if i==0 else 'actual']['binders'];ref['hypothesis_adapter']='Exact independently sealed '+('arbitrary measure, positive bounded REAL A/B and same square; internal complex CFC only' if i==0 else 'original potential/C2/both Hessians/positive capped step; actual S/T/D/root conclusions, no energy premise on alternatives')+'. Expanded binder records retained separately.'
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Corrected only missing literal library names and string-typed metadata adapter; exact statement/binders/source/route unchanged. Initial failed native check retained.')
