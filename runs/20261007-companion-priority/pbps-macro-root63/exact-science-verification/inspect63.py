from verify63 import *

mode=sys.argv[1]
if mode=='core':
    for name in ['math-freeze.json','math-freeze.presentation-supplement-v2.json','preproof-admission.json','proved-local.json']:
        x=read(RUN/name)
        print(name)
        if name=='math-freeze.json': print(json.dumps(x,ensure_ascii=False,indent=2))
        elif name=='preproof-admission.json': print(json.dumps({k:x[k] for k in ['headers','native_run','native_lease','named_payload','whole_run_sha256','named_preproof_RAW_payload_sha256','source_graph','source_coverage','proof_search_started','scope']},ensure_ascii=False,indent=2))
        else: print(json.dumps({k:v for k,v in x.items() if k not in ['current30','qualified_original58_history','statement_seal','source_proof_coverage','proof_digestion','purification']},ensure_ascii=False,indent=2))
elif mode=='source':
    x=read(RUN/'independent-source63/review.payload.json')
    print(json.dumps({k:v for k,v in x.items() if k not in ['binding_checks','presentation_review','source_proof_coverage','review_evidence']},ensure_ascii=False,indent=2))
elif mode=='native':
    for sub,fn in [('independent-math63','run.json'),('independent-source63','run.json'),('anonymous-decoder','native.run.json')]:
        x=read(RUN/sub/fn); print(sub)
        print(json.dumps({k:v for k,v in x.items() if k not in ['inputs','sealed_support_outputs','complete_decision','complete_mathematical_review','complete_publication_binding_issue','full_semantic_review','candidate_input_manifest','artifacts_before_finalization','owned_artifacts_before_finalization']},ensure_ascii=False,indent=2))
        print('LEASE',json.dumps(read(RUN/sub/'lease.json'),ensure_ascii=False,indent=2))
        p=RUN/sub/'output.manifest.json'
        if p.exists():
            m=read(p); print('MANIFEST_SHAPE',list(m.keys()) if isinstance(m,dict) else ('list',len(m))); print(json.dumps(m[:1] if isinstance(m,list) else {k:v[:1] if isinstance(v,list) else v for k,v in m.items()},ensure_ascii=False,indent=2))
elif mode=='headers':
    x=read(RUN/'preproof-admission.json')
    for row in x['headers']:
        print(row)
        p=aspath(row['path']) if isinstance(row,dict) else aspath(row)
        if p: print(p.read_text(encoding='utf-8'))
elif mode=='lesson':
    p=ROOT/'website/content/declaration_lessons/pbps-unique-positive-macroscopic-defect-root.json';x=read(p)
    print(list(x.keys()))
    print(json.dumps(x,ensure_ascii=False,indent=2))
elif mode=='shapes':
    for sub in ['independent-math63','independent-source63','anonymous-decoder']:
        print(sub)
        for fn in ['lease.json','native.receipt.json','output.manifest.json']:
            if not (RUN/sub/fn).exists(): continue
            x=read(RUN/sub/fn)
            print(fn,{k:('dict',len(v),list(v.keys())[:6]) if isinstance(v,dict) else ('list',len(v),v[:1]) if isinstance(v,list) else v for k,v in x.items()})
    for fn in ['presentation-step3-repair63/root.presentation-repair63.json','root.math63.adoption.json','math-freeze.presentation-supplement-v2.json','preproof-admission.json']:
        x=read(RUN/fn);print(fn)
        for k in ['raw_snapshot_mappings','exact_historical_negative_resolutions','qualified_original58_history','finite_negative_history_maps','effective_negative_history_resolutions']:
            if k in x:print(k,x[k][:1] if isinstance(x[k],list) else x[k])
