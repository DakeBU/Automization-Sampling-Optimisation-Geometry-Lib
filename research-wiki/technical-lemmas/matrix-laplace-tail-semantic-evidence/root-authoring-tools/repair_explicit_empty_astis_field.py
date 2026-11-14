from pathlib import Path
import json,hashlib,subprocess
r=Path.cwd();w=r/'.astis/huanjian-gc-matrix-laplace-20261114'
lp=r/'website/content/declaration_lessons/huanjian-matrix-laplace-tail.json'
before=lp.read_bytes();(w/'lesson.authored-v3.before-empty-astis-field.json').write_bytes(before)
x=json.loads(before);assert 'astis_dependencies' not in x['units'][0]
x['units'][0]['astis_dependencies']=[]
lp.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
script=(w/'prepare_reader_preview.py').read_text()
script=script.replace("new=w/'reader-preview-v1'","new=w/'reader-preview-v4'")
script=script.replace("'--metadata-version','authored-v1'","'--metadata-version','authored-v4'")
(w/'prepare_reader_preview.v4.py').write_text(script)
subprocess.run(['python3',str(w/'prepare_reader_preview.v4.py')],check=True)
old=json.loads((w/'reader-preview-v3/preview-freeze-manifest.json').read_text())
new=json.loads((w/'reader-preview-v4/preview-freeze-manifest.json').read_text())
equal={}
for variant in ['original','candidate']:
    a={p['path']:(p['sha256'],p['bytes']) for p in old['variants'][variant]['files']}
    b={p['path']:(p['sha256'],p['bytes']) for p in new['variants'][variant]['files']}
    assert a==b,(variant,[(k,a.get(k),b.get(k)) for k in a.keys()|b.keys() if a.get(k)!=b.get(k)])
    for p in a:
        assert (w/'reader-preview-v3/fixtures'/variant/p).read_bytes()==(w/'reader-preview-v4/fixtures'/variant/p).read_bytes()
    equal[variant]={'identical_files':len(a),'path_bytes_sha256_and_direct_bytes_equal':True}
raw=subprocess.check_output(['python3','tools/astis_publication.py','review-context','--item','huanjian-matrix-laplace-tail',
 '--declaration','AutoSamplingTheory.TechnicalLemmas.Probability.MatrixLaplaceTail.max_eigenvalue_tail_le_iInf_trace_exp'])
ctx=json.loads(raw);(w/'publication-context.authored-v4.original.json').write_bytes(raw)
ap=r/'research-wiki/semantic-roundtrip/audits/huanjian-matrix-laplace-tail.json'
(w/'P.audit.source-reviewed.v3.original.json').write_bytes(ap.read_bytes())
a=json.loads(ap.read_text());a['publication_binding_sha256']=ctx['publication_binding_sha256'];a['publication_context']=ctx['publication_context']
a['state']='draft';a['source_review']={'state':'pending'};a['verdict']='pending'
ap.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
ap=w/'private-consumer-audit.registry.json';reg=json.loads(ap.read_text())
(w/'T.registry.source-reviewed.v3.original.json').write_bytes(ap.read_bytes())
a=reg['audits'][0];a['publication_binding_sha256']=ctx['publication_binding_sha256'];a['publication_context']=ctx['publication_context']
a['state']='draft';a['source_review']={'state':'pending'};a['verdict']='pending'
ap.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
subprocess.run(['python3','tools/astis_semantic_roundtrip.py','reviewer-packet','--audit-id','ASTIS-RT-20261114-HuanjianMatrixLaplaceTail','--output',str(w/'P.reviewer-packet.v3.json')],check=True)
subprocess.run(['python3','tools/astis_semantic_roundtrip.py','--registry',str(ap),'reviewer-packet','--audit-id',a['id'],'--output',str(w/'T.reviewer-packet.v3.json')],check=True)
report={'classification':'METADATA_SCHEMA_FIELD_OMISSION_REPAIR_ONLY','trigger':'Actual contributor gate failed only because astis_dependencies field was absent. Generic P has no ASTIS parent, so empty list is exact.',
 'exact_change':'Add astis_dependencies:[] to the authored lesson; no existing key removed or changed.',
 'old_lesson_sha256':hashlib.sha256(before).hexdigest(),'new_lesson_sha256':hashlib.sha256(lp.read_bytes()).hexdigest(),
 'new_binding_sha256':ctx['publication_binding_sha256'],'mathematical_source_files_statements_definitions_proofs_and_all_six_folds_unchanged':True,
 'actual_rendered_fixture_equality':equal,
 'pixel_reuse_boundary':'Only exact served-file byte identity can transfer actual v3 runtime observations to the v4 rendered site. No new browser-v4 run or new metadata source acceptance is claimed.',
 'current_independent_context_acceptance':'PENDING; prior accepted v3 audits and packets retained verbatim'}
(w/'empty-astis-field-repair.proposal.v1.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'new_lesson_sha256':report['new_lesson_sha256'],'new_binding_sha256':ctx['publication_binding_sha256'],'exact_rendered_site_byte_identity':equal}))
