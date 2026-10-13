from pathlib import Path
import hashlib,json,os,sys
sys.path.insert(0,str(Path.cwd()/'tools'))
import astis_semantic_roundtrip as rt,astis_publication as pub
r=Path('runs/20261007-companion-priority/pbps-actual-finite-jump-recursion76');pre=r.parent/'pbps-recursive-preproof76'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.resolve().as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def new(p,x):
 p=Path(p);assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
assert load(r/'root.decoder76.adoption.json')['status']=='CLOSED_BLIND_DECODER76_ADOPTED_ONLY'
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualFiniteJumpRecursion.json');a=load(ap);assert a['state']=='blind-reconstructed' and a['source_review']=={'state':'pending'}
p=load(r/'source-review.packet.json');assert p==rt.semantic_reviewer_packet(a)
assert all(v is False for v in p['anti_anchoring'].values())
pp=Path('website/content/publications/pbps-actual-finite-jump-recursion.json');item=load(pp)['items'][0];binding=item['bindings'][0]
assert p['publication_binding_sha256']==a['publication_binding_sha256']==pub.binding_digest(item,binding,pub.inputs())
assert p['candidate_publication_context']==a['publication_context']==pub.review_context(item,binding,pub.inputs())
cp=Path('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-finite-jump-recursion.json');binders=load(cp)['statement_seal']['binder_audit']
forbidden={'semantic_slots','semantic_deltas','deltas','fidelity_verdict','verdict','reviewer_decision','review_run_sha256','source_review_decision','repairs'}
def neutral(x):
 if isinstance(x,dict):
  assert not (set(x)&forbidden),set(x)&forbidden
  for v in x.values():neutral(v)
 elif isinstance(x,list):
  for v in x:neutral(v)
neutral(binders);neutral(p['candidate_publication_context'])
assert binders['counts']==dict(callers=6,conclusion_groups=10,literal_definitions=11,typing=5)
bp=r/'neutral-expanded-binders76.json';new(bp,binders)
clean=r/'source-review.clean.packet.json';assert not clean.exists();clean.write_bytes((r/'source-review.packet.json').read_bytes())
primary=Path('runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html')
module=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean');assert module.read_bytes()==(r/'canonical76.frozen.exactraw.lean').read_bytes()
ownfreeze=pre/'fresh-compiled-source76/source-only.freeze76.json';assert sha(ownfreeze.read_bytes())=='b543f6543f3d6c8e22bea1986427c41e9b10a45e0f732f143c59c4d75a3f771f'
paths=[clean,primary,module,r/'canonical76.frozen.exactraw.lean',r/'expanded76.frozen.header.lean',bp,Path('lean-toolchain'),Path('lake-manifest.json'),*[module.with_name(n+'.lean') for n in ['ActualHarmonicFlow','ActualBounceRate','ActualHazardClock']],r/'focused-native-branches76/receipt.json',r/'axioms/receipt.json',Path('website/content/declaration_lessons/pbps-actual-finite-jump-recursion.json'),ownfreeze]
new(r/'source-review.freeze76.json',dict(status='ANTI_ANCHORED_ACTUAL_COMPILED76_FINITE_DISPATCH_AFTER_INDEPENDENT_SOURCE_ONLY_FREEZE',actual_root_PID=os.getpid(),inputs=[pin(x) for x in paths],input_count=len(paths),source_only_freeze_before_candidate=pin(ownfreeze),canonical_reviewer_packet_sha256=p['packet_sha256'],publication_binding_sha256=p['publication_binding_sha256'],canonical_math_context_equals_current=True,expanded_binders_neutral=True,no_prior_source_or_math_verdicts_supplied=True,excluded_inputs=['Root header review/adoption verdicts','Prior prospective header76 source verdict/deltas/repairs and source graph metadata','Independent whole-math76 outcome','Full canonical audit/cell/publication metadata and previous agent transcripts'],hash_only_coordinator_pins=[pin(x) for x in [ap,cp,pp]],hash_only_coordinator_pins_may_be_read_as_bytes_for_hash_only=True,source_review=False,PROVED_LOCAL=False,VERIFIED=False,Goal_complete=False))
print('PASS76 finite anti-anchored source dispatch15 inputs; original source-only freeze retained, full compiled module/ten BODY proof steps included, prior reviewer outcomes excluded.')
