from pathlib import Path
import hashlib,json,datetime
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-law81')
pre=Path('runs/20261007-companion-priority/pbps-physical-time-law-preread81')
load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def write(p,x):
 assert not p.exists(),p
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
checked=[]
def verify_tree(obj):
 if isinstance(obj,dict):
  if 'path' in obj and ('RAW_sha256' in obj or 'raw_sha256' in obj):
   p=pin(obj['path']);assert p['RAW_sha256']==obj.get('RAW_sha256',obj.get('raw_sha256')),p
   if 'RAW_bytes' in obj:assert p['RAW_bytes']==obj['RAW_bytes'],p
   checked.append(p)
  for v in obj.values():verify_tree(v)
 elif isinstance(obj,list):
  for v in obj:verify_tree(v)
manifests=[r/'header-review81/closed-manifest81.json',pre/'header-source-review81/header-source-review81.raw-manifest.json',pre/'source_freeze81.complete-raw-manifest.json']
for p in manifests:verify_tree(load(p))
decision=load(r/'header-review81/decision81.json')
source=load(pre/'header-source-review81/header-source-review81.result.json')
receipt=load(r/'header-review81/typecheck81.receipt.json')
assert receipt['exit_code']==0,receipt
print(json.dumps(dict(math=decision,source=source,receipt=receipt),ensure_ascii=False)[:2500])
write(r/'independent-review-adoption81.json',dict(accepted=True,exact_header_RAW_sha256=pin(r/'header81.proposed.lean')['RAW_sha256'],scope='Prospective exact header only; no BODY, proof, final semantic or verification credit.',native_manifests=[pin(p) for p in manifests],checked_raw_files=checked,decision=pin(r/'header-review81/decision81.json'),source_decision=pin(pre/'header-source-review81/header-source-review81.result.json'),typecheck=pin(r/'header-review81/typecheck81.receipt.json'),utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
cells=[]
for name in (r/'retrieval81/shared-current-cells.txt').read_text().splitlines():
 c=load(name);cells.append(dict(path=name,cell_id=c['cell_id'],status=c['status'],target_statement=c.get('target_statement'),parents=c.get('parents'),source_targets=c.get('source_targets')))
write(r/'retrieval81/current-cells-readback81.json',cells)
write(r/'retrieval81/reuse-decision81.json',dict(status='INSPECTED_BEFORE_PROOF',search_manifest=pin(r/'retrieval81/search-manifest81.json'),current_cell_readback=pin(r/'retrieval81/current-cells-readback81.json'),decision='Reuse actual80 phase and actual75/76/73/77 measurable actual recurrence/clock/support; reuse canonical GaussianConditionalKernel and GibbsAugmentation normalization; pinned Mathlib kernel product/map/comap and product AE. No generic kernel copy or upstream transplant.',normalization_route='GibbsAugmentation.normalized_augmentation_density gives positive actual Gibbs normalizer. Integrable.of_integral_ne_zero derives integrability; isProbabilityMeasure_tilted then GaussianConditionalKernel.exists_tilted_isCondKernel and Measure.tilted_tilted identify literal q_y.',fubini_route='At fixed y,x, measurable finite-time live-arc predicate using countable n and measurable Sum projection; ae_prod_iff_ae_ae lifts per-fixed-reference/momentum actual80 event. No arbitrary correlated random input or uncountable-time measurable-set assertion.',kernel_route='Product of R.comap fst, constant Gaussian and actual exponential product; retain input by Kernel.id product; jointly measurable terminal projection map gives H_y.',truth_boundary='Ideal exact-reference Algorithm1 at pi only, no implementation/cost/phase Markov/semigroup/invariance/reversibility/main/composition. Source q_y not q-hat.',upstream='Bounded compatible indexed search empty; no claim of global absence.',new_shared_declarations=[]))
