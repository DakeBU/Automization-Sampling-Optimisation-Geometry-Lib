from pathlib import Path
import copy,hashlib,json,os
r=Path('runs/20261007-companion-priority/pbps-actual-hazard-clock75');out=r/'review-input-metadata-overlay75';out.mkdir(exist_ok=False)
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def write(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
neutral=dict(kind='expanded-binder-inventory-only',ambient_typing=['NormedAddCommGroup E','InnerProductSpace ℝ E','FiniteDimensional ℝ E','MeasurableSpace E','BorelSpace E'],source_hypotheses=[dict(name=n,type=t,classification='SOURCE') for n,t in [('hα','0 < (α : ℝ)'),('hαβ','α ≤ β'),('hV','ContDiff ℝ 2 V'),('hH','∀ x v : E, (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧ (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2'),('hη','0 < η'),('hβη','(β : ℝ) * η ≤ 1')]],definitions=8,conclusion_groups=10,extra_public_proof_or_law_providers=[],unexplained_binders=[],boundary='Neutral inventory of the literal sealed statement. No previous reviewer semantic slots, deltas, verdict or repair decisions are included. Review source fidelity independently against the primary source and current implementation.')
cp=Path('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-hazard-clock.json');pp=Path('website/content/publications/pbps-actual-hazard-clock.json')
rows=[]
for i,p in enumerate([cp,pp]):
 original=load(p);after=copy.deepcopy(original);beforep=out/f'{i}.before.exactraw.json';beforep.write_bytes(p.read_bytes());changes=[]
 if p==cp:
  for pointer,parent,key in [('/statement_seal/binder_audit',after['statement_seal'],'binder_audit'),('/source_detail_audit/consulted/0/expanded_binder_audit',after['source_detail_audit']['consulted'][0],'expanded_binder_audit')]:
   changes.append(dict(json_pointer=pointer,old=copy.deepcopy(parent[key]),new=copy.deepcopy(neutral)));parent[key]=copy.deepcopy(neutral)
 else:
  parent=after['items'][0]['statement_seal'];key='binder_audit';changes.append(dict(json_pointer='/items/0/statement_seal/binder_audit',old=copy.deepcopy(parent[key]),new=copy.deepcopy(neutral)));parent[key]=copy.deepcopy(neutral)
 afterp=out/f'{i}.proposed.exactraw.json';write(afterp,after)
 def walk(x):
  if isinstance(x,dict):
   for k,v in x.items():
    assert k not in {'semantic_slots','deltas','verdict','review_run_sha256'},(p,k)
    walk(v)
  elif isinstance(x,list):
   for v in x:walk(v)
 walk(after)
 rows.append(dict(path=p.as_posix(),before=pin(beforep),current=pin(p),proposed=pin(afterp),changes=changes))
proposal=dict(status='PROPOSED_EXACT_THREE_FIELD_PRIOR_REVIEW_REMOVAL_ONLY_NOT_APPLIED',actual_root_PID=os.getpid(),rows=rows,field_count=3,reason='Full historical header-source admission was copied into binder inventory fields. This exposed previous semantic decisions to a new source reviewer. Replace only those three metadata fields with the same neutral literal-binder inventory; preserve the original statement seal hash, Lean/source/definitions/assumptions/conclusions/proof and exhaustive source graph/coverage.',frozen_Lean=pin('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean'),frozen_header=pin('runs/20261007-companion-priority/pbps-clock-preproof75/header75.v2.proposed.lean'),source_packet_before=pin(r/'source-review.packet.json'),previous_review_must_be_supplemental_not_anti_anchored=True,requires_independent_exact_overlay_review=True,requires_fresh_anti_anchored_source_review_after_application=True,PROVED_LOCAL=False,VERIFIED=False,Goal_complete=False)
write(out/'proposal.json',proposal);print('PASS75 exact three-field neutral binder inventory proposal created; no canonical metadata change or source acceptance.')
