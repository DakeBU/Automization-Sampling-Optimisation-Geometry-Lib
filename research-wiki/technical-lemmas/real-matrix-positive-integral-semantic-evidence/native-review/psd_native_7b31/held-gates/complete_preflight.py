import json,pathlib
from record import ROOT,EXPECTED_HEAD,sha
original=(ROOT/'preflight.py').read_text()
start=original.index('def checked(');end=original.index("head,_=checked(",start)
replacement='''def checked(label,argv,cwd=REPO):
    matches=[]
    for f in (ROOT/'receipts').glob('*.json'):
        r=json.loads(f.read_text())
        if r['label']==label:matches.append((f,r))
    assert len(matches)==1,(label,len(matches))
    receipt,r=matches[0]
    assert r['argv']==argv and r['cwd']==str(cwd)
    assert r['exit']==0 and r['shared_HEAD_before']==EXPECTED_HEAD and r['shared_HEAD_after']==EXPECTED_HEAD
    stdout=(receipt.parent/r['stdout_file']).read_bytes();stderr=(receipt.parent/r['stderr_file']).read_bytes()
    assert sha(stdout)==r['stdout_sha256'] and sha(stderr)==r['stderr_sha256']
    return stdout,str(receipt.relative_to(ROOT))
'''
code=original[:start]+replacement+original[end:]
code=code.replace("assert audit['state']=='accepted',(auditid,audit.get('state'))","assert audit['state']=='source-reviewed' and audit['source_review']['state']=='accepted',(auditid,audit.get('state'),audit.get('source_review',{}).get('state'))")
code=code.replace("'state':audit['state'],'use':", "'state':audit['state'],'source_review_state':audit['source_review']['state'],'use':")
exec(compile(code,'preflight-completed-from-recorded-successful-checks','exec'))
diagnosis={'failure_class':'IMPLEMENTATION_FAILED','failure_scope':'Verifier-local preflight implementation only','original_script':'preflight.py','original_receipt':'receipts/20261112T160557119162Z-preflight-driver.json','incorrect_assumption':"Top-level audit.state == 'accepted'",'actual_protocol':"Top-level audit.state == 'source-reviewed' and child source_review.state == 'accepted'",'correction':'complete_preflight.py validates the actual two-layer schema while reusing and re-hashing the already successful original preflight command receipts.','formal_gates_executed_before_correction':0,'canonical_files_changed':False,'mathematical_or_source_failure':False}
(ROOT/'preflight-implementation-failure-diagnosis.json').write_text(json.dumps(diagnosis,indent=2)+'\n')
