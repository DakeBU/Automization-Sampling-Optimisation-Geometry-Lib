from pathlib import Path
import copy,hashlib,json,sys
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_publication as pub
r=Path(__file__).parent;load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
f=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualSmallTimeContinuity.lean');old=(r/'focused82-attempt5/source.snapshot.lean').read_bytes();new=f.read_bytes()
before=b'/-! Prospective exact statement82 only; no theorem proof or admission.'
after=b'/-! Actual PBPS short-time probability prerequisite, with its proof below.'
assert new==old.replace(before,after,1) and old.count(before)==1
assert old.count(b'\n')==new.count(b'\n')
receipt=r/'focused82-attempt6/receipt.json';q=load(receipt);assert q['exit_code']==0 and q['source_RAW_sha256']==sha(new)
pp=Path('website/content/publications/pbps-actual-small-time-continuity.json');lp=Path('website/content/declaration_lessons/pbps-actual-small-time-continuity.json');ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualSmallTimeContinuity.json')
for p in [pp,lp,ap]:(r/(p.stem+'.before-documentation82.snapshot.json')).write_bytes(p.read_bytes())
l=load(lp);steps=l['units'][0]['steps'];assert len(steps)==9
oldformula=steps[3]['formula'];steps[3]['formula']=r'P\{t<\tau(z_0,\varepsilon_0)\}=e^{-\Lambda(z_0,t)}.'
for x in steps:
 z=x['lean_source_region'];assert z['source_raw_sha256']==sha(old)
 z['source_raw_sha256']=sha(new)
 assert '\n'.join(new.decode().splitlines()[z['start_line']-1:z['end_line']])+'\n'==x['lean']
save(lp,l)
cpath=Path('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-small-time-continuity.json');c=load(cpath);c['evidence']['focused_checks'][0]['evidence']=receipt.as_posix();save(cpath,c)
a=load(ap);assert a['state']=='draft';a['lean']['compiler_evidence']=receipt.as_posix()
pub.inputs.cache_clear();pub.load.cache_clear();p=load(pp)['items'][0]
a['publication_binding_sha256']=pub.binding_digest(p,p['bindings'][0],pub.inputs());a['publication_context']=pub.review_context(p,p['bindings'][0],pub.inputs());save(ap,a)
pub.check_advance([a['lean']['declaration']],reviewed=False)
seal=copy.deepcopy(load(r/'mathematics-freeze82.json'));seal.update(module_RAW_sha256=sha(new),focused_final_receipt=receipt.as_posix(),successor_of='mathematics-freeze82.json',statement_and_BODY_byte_identical=True)
save(r/'mathematics-freeze82.successor.json',seal)
save(r/'documentation-successor82.json',dict(status='DOCUMENTATION_ONLY_SUCCESSOR_CURRENT_FOCUSED_PASS',module_RAW_before=sha(old),module_RAW_after=sha(new),statement_and_BODY_byte_identical=True,line_count_unchanged=True,exact_replacement=dict(before=before.decode(),after=after.decode()),exposition_overlay=dict(step=4,before=oldformula,after=steps[3]['formula'],reason='Independent source reviewer: step4 proves survival only, defect bound is step6 after firstarc step5.'),anonymous_decoder_packet_unchanged=True,publication_binding_sha256=a['publication_binding_sha256'],focused_receipt=receipt.as_posix(),VERIFIED=False))
print('Current doc-only module',sha(new),'publication binding',a['publication_binding_sha256'])
