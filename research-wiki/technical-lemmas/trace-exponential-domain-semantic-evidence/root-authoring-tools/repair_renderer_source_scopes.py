from pathlib import Path
import json,hashlib,subprocess,copy
r=Path.cwd();w=r/'.astis/huanjian-gc-trace-mgf-domain-20261115'
e=r/'research-wiki/technical-lemmas/trace-exponential-domain-semantic-evidence'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
lp=r/'website/content/declaration_lessons/huanjian-trace-exponential-domain.json'
ap=r/'research-wiki/semantic-roundtrip/audits/huanjian-trace-exponential-domain.json'
rp=w/'private-consumer-audit.registry.json'
old=json.loads(lp.read_text());new=copy.deepcopy(old)
assert sha(lp)=='e76e0ac66463451564cce08d087357ff50e9481003899e7c5d26ab85d5503921'
changes=[]
scopes={1:'Exact Lean source for the shared deterministic envelope.',
 2:'Exact Lean source for the private Gaussian application in proof steps4–5.',
 3:'Original unconditional Gaussian experiment and inclusive own-row truncation.',
 4:'The two separate operator-norm input bounds, consumed from the existing canonical Radius theorem.',
 5:'The centered-summand radius, derived internally in the private application.',
 6:'Downstream context only; the weighted tail bound remains open.'}
for i,text in scopes.items():
    entry=new['units'][0]['sources'][i];assert 'scope' not in entry
    changes.append({'source_entry_index0':i,'before':copy.deepcopy(entry),'after':{**entry,'scope':text}})
    entry['scope']=text
proposal={'kind':'presentation-metadata-missing-required-source-scope-repair',
 'failure_class':'IMPLEMENTATION_FAILED','actual_failure_receipt':'.astis/huanjian-resume-20261103/20261115T084120392857Z-gc-trace-exp-render-source-reviewed-five-fold-isolated-reader.receipt.json',
 'failure':'Real renderer KeyError scope at source_citation; original failure/snapshot/partial attempt retained.',
 'exact_changes':changes,'unchanged':'All P/T source, source URLs/labels/anchors, statements, assumptions, five mathematical steps, all243 exact code lines, Lean/scopes/native/decoder evidence remain unchanged.',
 'review':'Prior82c0 wholemodule/seven-slot review retained, not silently replayed against a refreshed hash. Independent exact successor/delta review pending.'}
cust=e/'metadata-custody/source-scope-repair-v1';assert not cust.exists();cust.mkdir(parents=True)
for name,p in [('lesson.before.json',lp),('public-audit.before.json',ap),('private-registry.before.json',rp),
 ('publication-context.before.original.json',w/'publication-context.authored-v3.original.json')]:
    (cust/name).write_bytes(p.read_bytes())
(cust/'repair.proposal.v1.json').write_text(json.dumps(proposal,ensure_ascii=False,indent=2)+'\n')
lp.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n')
P=old['units'][0]['declaration']
raw=subprocess.check_output(['python3','tools/astis_publication.py','review-context','--item','huanjian-trace-exponential-domain','--declaration',P])
cp=w/'publication-context.authored-v4.original.json';assert not cp.exists();cp.write_bytes(raw);c=json.loads(raw)
pa=json.loads(ap.read_text());reg=json.loads(rp.read_text());ta=reg['audits'][0]
for a in [pa,ta]:
    assert a['state']=='draft' and a['publication_binding_sha256']=='82c0d7528f45857836c4910efd2ac7dda87cd60d86e76348f6ef4dbb6db7b3e8'
    a['publication_binding_sha256']=c['publication_binding_sha256'];a['publication_context']=c['publication_context']
    a['binding_status']='ACTUAL_CURRENT_SIX_SOURCE_SCOPE_REPAIR_CONTEXT; INDEPENDENT_DELTA_REVIEW_PENDING'
ap.write_text(json.dumps(pa,ensure_ascii=False,indent=2)+'\n');reg['audits']=[ta]
rp.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
for args,out in [([],w/'P.reviewer-packet.v2.json'),(['--registry',str(rp)],w/'T.reviewer-packet.v2.json')]:
    aid=pa['id'] if not args else ta['id']
    subprocess.run(['python3','tools/astis_semantic_roundtrip.py',*args,'reviewer-packet','--audit-id',aid,'--output',str(out)],check=True)
print(json.dumps({'new_binding':c['publication_binding_sha256'],'lesson_sha256':sha(lp),
 'proposal_sha256':sha(cust/'repair.proposal.v1.json'),'new_context_sha256':sha(cp),
 'exact_source_scopes_added':6,'P_T_and_decoder_unchanged':True,'normal_PL_calls':0,'normal_V_calls':0}))
