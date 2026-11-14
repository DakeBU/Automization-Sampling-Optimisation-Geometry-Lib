from pathlib import Path
import json,hashlib,subprocess,copy
r=Path.cwd();w=r/'.astis/huanjian-gc-matrix-laplace-20261114'
lp=r/'website/content/declaration_lessons/huanjian-matrix-laplace-tail.json'
before=lp.read_bytes();(w/'lesson.authored-v2.before-radius-citation-repair.json').write_bytes(before)
x=json.loads(before);u=x['units'][0]
s=u['steps'][4]
assert s['source_attribution'][0]['anchor']=='A3.Ex112'
src=copy.deepcopy(s['source_attribution'][0]);src['anchor']='A3.Ex111'
src['url']='https://arxiv.org/html/2610.20492v1#A3.Ex111'
src['region']='Exact separate truncated-matrix norm and actual-mean norm estimates'
s['source_attribution'][0]['region']='Centered-matrix radius after subtracting the actual mean'
s['source_attribution'].insert(0,src)
for i,a in enumerate(u['sources']):
    if a.get('url','').endswith('#A3.Ex112'):
        a['scope']='Centered-matrix radius bound; the separate Y and actual-mean inputs are in Ex111.'
        u['sources'].insert(i,{'url':'https://arxiv.org/html/2610.20492v1#A3.Ex111',
          'label':'Separate truncated-matrix and actual-mean norm estimates',
          'scope':'Exact two source inputs reused through the canonical radius parent.'})
        break
else: raise AssertionError('missing Ex112')
lp.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
script=(w/'prepare_reader_preview.py').read_text()
assert script.count("new=w/'reader-preview-v1'")==1
script=script.replace("new=w/'reader-preview-v1'","new=w/'reader-preview-v3'")
script=script.replace("'--metadata-version','authored-v1'","'--metadata-version','authored-v3'")
(w/'prepare_reader_preview.v3.py').write_text(script)
subprocess.run(['python3',str(w/'prepare_reader_preview.v3.py')],check=True)
cmd=['python3','tools/astis_publication.py','review-context','--item','huanjian-matrix-laplace-tail','--declaration',u['declaration']]
raw=subprocess.check_output(cmd);ctx=json.loads(raw)
(w/'publication-context.authored-v3.original.json').write_bytes(raw)
ap=r/'research-wiki/semantic-roundtrip/audits/huanjian-matrix-laplace-tail.json'
a=json.loads(ap.read_text());a['publication_binding_sha256']=ctx['publication_binding_sha256'];a['publication_context']=ctx['publication_context']
ap.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
ap=w/'private-consumer-audit.registry.json';reg=json.loads(ap.read_text());a=reg['audits'][0]
a['publication_binding_sha256']=ctx['publication_binding_sha256'];a['publication_context']=ctx['publication_context']
ap.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
subprocess.run(['python3','tools/astis_semantic_roundtrip.py','reviewer-packet','--audit-id','ASTIS-RT-20261114-HuanjianMatrixLaplaceTail','--output',str(w/'P.reviewer-packet.v2.json')],check=True)
subprocess.run(['python3','tools/astis_semantic_roundtrip.py','--registry',str(ap),'reviewer-packet','--audit-id',a['id'],'--output',str(w/'T.reviewer-packet.v2.json')],check=True)
report={'classification':'SOURCE_LOCATOR_METADATA_REPAIR_ONLY','trigger':'Independent fresh phase2 found Ex112 is the centered bound; separate Y and actual mean estimates are in Ex111.',
 'exact_change':'Added Ex111 to step5 and source list, and narrowed Ex112 wording to the centered radius. New preview metadata label authored-v3.',
 'proofs_signatures_assumptions_and_all_six_code_fold_bytes_unchanged':True,
 'old_lesson_sha256':hashlib.sha256(before).hexdigest(),'new_lesson_sha256':hashlib.sha256(lp.read_bytes()).hexdigest(),
 'new_binding_sha256':ctx['publication_binding_sha256'],
 'old_source_first_phase2_retained':'e5e1136f7fcdcd4869c7580b40e24e68f51b1e1ccd171174debb7992934a189f',
 'new_exact_context_independent_acceptance':'PENDING','new_exact_reader_native_acceptance':'PENDING',
 'purification_debt':'Frozen T128–133 local positive facts are not used subsequently; no separate proof credit. Post-merge purification remains distinct.'}
(w/'radius-citation-repair.proposal.v1.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'new_lesson_sha256':report['new_lesson_sha256'],'new_binding_sha256':ctx['publication_binding_sha256'],'new_preview_manifest_sha256':hashlib.sha256((w/'reader-preview-v3/preview-freeze-manifest.json').read_bytes()).hexdigest(),'mathematical_bytes_unchanged':True}))
