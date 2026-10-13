from pathlib import Path
import hashlib,json,subprocess
r=Path(__file__).parent;load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def verify(p,h,keys):
 assert pin(p)['RAW_sha256']==h
 m=load(p)
 for k in keys:
  for x in m[k]:
   b=Path(x['path']).read_bytes();assert len(b)==x.get('RAW_bytes',x.get('bytes')) and hashlib.sha256(b).hexdigest()==x.get('RAW_sha256',x.get('raw_sha256')),x['path']
 return pin(p)
top=verify(r/'independent-topology83/closed-RAW-manifest83.json','17d1c82788a18c8b8c53c89e638407f44cbc437aca347808d76aa67037645b79',['frozen_source_inputs','owned_outputs'])
review=verify(r/'overlay-review83/overlay-review83.closed-raw-manifest.json','22be7ba723c330baca0875e389c125fb7aff11018e8556b35a63c752acb07785',['raw_inputs','raw_outputs'])
overlay=r/'independent-topology83/proposed-minimal-topology-overlay83.json';assert pin(overlay)['RAW_sha256']=='6a8870abda762b76523c2bc9fef7dac87cef1b7dd64c1c034865745abbb702a6'
o=load(overlay);g=load(r/'source_proof_graph83.json');s=load(r/'optional-route-topology-supplement83.json')
assert len(o['patches'])==3
for patch in o['patches']:
 if patch['artifact']=='optional-route-topology-supplement83.json':
  edgeid=patch['selector'].split('id=')[1].split(']')[0];e=next(x for x in s['added_edges'] if x['id']==edgeid);assert e['status']==patch['before'];e['status']=patch['after']
 else:
  idx=next(i for i,x in enumerate(g['edges']) if x['id']=='E83-28');assert g['edges'][idx]==patch['before'];g['edges'][idx]=patch['after']
g['edges']+=s['added_edges'];g['reviewed_junctions']=o['junctions'];g['reviewed_overlay']=pin(overlay);g['truth_boundary']='Source proof topology only; no83 Lean or theorem admission. Original frozen artifacts retained unchanged.'
p=r/'source_proof_graph83.reviewed-effective.json';assert not p.exists();p.write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
(r/'root.topology-adoption83.json').write_text(json.dumps(dict(independent_topology=top,separate_exact_overlay_review=review,adopted_overlay=pin(overlay),effective_graph=pin(p),effective_nodes=17,effective_relations=30,dependency_rows=29,boundary_associations=1,StatementSeal=False,proof=False,VERIFIED=False),indent=2)+'\n',encoding='utf8',newline='\n')
old=load(r/'pre-fetch83.workspace-RAW.json');preserved=load('runs/20261007-companion-priority/pbps-actual-small-time-continuity82/pre-fetch82.workspace-RAW.json')['tracked_modified']
for p,h in preserved.items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,p
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==old['commit']
successor=dict(old,tracked_modified=preserved,raw_preservation_note='Initial diff --name-only was empty under Git newline normalization despite21 porcelain stat entries. Corrected RAW preservation scope from prior snapshot, all21 hashes verified now unchanged; initial artifact retained.',fetch_exit_code=0,origin_main=subprocess.check_output(['git','rev-parse','origin/main'],text=True).strip(),work_branch_updated=False)
(r/'post-fetch83.workspace-RAW.corrected.json').write_text(json.dumps(successor,indent=2)+'\n',encoding='utf8',newline='\n')
print('Independent source topology and exact overlay mechanically adopted; original frozen bytes preserved;21 collaborator RAWs unchanged; no83 seal/proof')
