from pathlib import Path
import sys,json,hashlib
r=Path.cwd();w=r/'.astis/huanjian-gc-matrix-laplace-20261114'
sys.path.insert(0,str(r/'tools'));import astis_publication as p
data=p.inputs(); item=next(x for x in p.load() if x['id']=='huanjian-matrix-laplace-tail')
b=item['bindings'][0]; old=json.loads((w/'lesson.authored-v1.before-source-scope-repair.json').read_text())['units'][0]
data={**data,'lessons':{**data['lessons'],b['declaration']:old}}
ctx={'publication_binding_sha256':p.binding_digest(item,b,data),'publication_context':p.review_context(item,b,data)}
assert ctx['publication_binding_sha256']=='bbd9f5d9b871d123080ac2827d70fde13c2e4fb0534948754c32a6b1a0ce9e56'
out=w/'publication-context.authored-v1.reconstructed-after-accidental-overwrite.json'
out.write_text(json.dumps(ctx,ensure_ascii=False,indent=2)+'\n')
current=(w/'publication-context.v1.json').read_bytes()
(w/'publication-context.authored-v2.original.json').write_bytes(current)
report={'failure_class':'METADATA_IMPLEMENTATION_FAILED','mathematics_unchanged':True,
 'first_failure':'Authored lesson source citation rows lacked mandatory scope keys; isolated renderer exited KeyError scope. Original lesson and partial reader v1 preserved.',
 'repair':'Added explicit mathematical scope to each source citation. New isolated reader v2 generated successfully. P/T source bytes, public source item and literal decoder packet mathematics unchanged.',
 'custody_correction':'The context-preparation helper overwrote the first raw context file before it was independently reviewed. Its original raw bytes are not claimed retained. This separate labeled reconstruction derives the previous context from preserved exact lesson-v1, unchanged source item/P module/toolchain/manifest, and matches the binding digest printed by the original actual receipt. The current v2 raw context is separately preserved.',
 'old_digest':ctx['publication_binding_sha256'],'new_digest':json.loads(current)['publication_binding_sha256'],
 'old_reconstruction':str(out.relative_to(r)),'new_raw_context':str((w/'publication-context.authored-v2.original.json').relative_to(r)),
 'no_independent_review_invalidated':True,'reason':'Fresh source phase2 had not been given either context; decoder sees only unchanged anonymous types.'}
(w/'reader-scope-repair-and-context-custody.v1.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'old_binding_reconstruction_matches_actual_recorded_digest':True,'new_original_preserved':True}))
