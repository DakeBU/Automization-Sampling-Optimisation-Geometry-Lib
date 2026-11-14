import collections,gzip,hashlib,json,pathlib,re,sys
from record import ROOT,REPO,COMMIT,run,sha
C=ROOT/'candidate'
sys.path[:0]=[str(C/'tools'),str(C/'website/scripts')]
import astis_site as base
closure=json.loads((ROOT/'closure.json').read_text());audit=json.loads((C/'kernel-audit.json').read_text())
scan=[]
for mod in closure['topological_order']:
    p=mod.replace('.','/')+'.lean';data=(C/p).read_text();clean=base.sanitize_lean(data)
    found=sorted(set(re.findall(r'\b(?:axiom|sorry|admit)\b|Prop\s*:=\s*True|:=\s*trivial\b',clean)))
    assert not found,(p,found)
    scan.append({'module':mod,'sha256':sha((C/p).read_bytes()),'forbidden_tokens':found})
decls=audit['declarations'];assert len(decls)==46
assert all(d['type_closed'] and d['body_present'] and d['body_closed_and_kernel_checked'] for d in decls)
sp=[d for d in decls if d['module'].endswith(('RealMatrixPositiveIntegral','FixedSpectrumSourceMatrixVariance'))]
assert len(sp)==4
rootreach=set().union(*(set(r['actual_reachable_ASTIS']) for r in audit['roots']))
assert all(d['name'] in rootreach for d in sp)
allnames={d['name'] for d in decls};reachnames=allnames&rootreach
unreached=sorted(allnames-rootreach)
summary={'candidate_commit':COMMIT,'empty_initial_ASTIS_outputs':True,'all_nine_modules_compiled':True,'closure_declarations':len(decls),'all_declaration_types_and_bodies_closed_and_kernel_checked':True,'all_declaration_bodies_present':True,'standard_axiom_allowlist':['propext','Classical.choice','Quot.sound'],'new_SP_declarations':[{k:d[k] for k in ['name','module','kind','axioms','actual_ASTIS_type_and_body_calls']} for d in sp],'new_SP_handwritten':2,'new_SP_generated':2,'new_SP_unreachable':[],'union_actual_root_reachable_ASTIS_count':len(reachnames),'prior_imported_closure_declarations_not_reachable_from_SP_roots':unreached,'literal_actual_root_proof_value_applications':[{k:l[k] for k in ['name','level_params','expanded_actual_root_proof_value_kernel_checked']} for l in audit['literals']],'source_fake_closure_scan':scan,'types_bodies_dump':{},'truth_boundary':'Only shared positivity S and actual uncentered second-moment P. No fullR9 centered/weighted T implementation or credit; no canonical source-fidelity verdict, normalV, state transition, publication or shared integration.'}
for f in [C/'full-types-bodies.dump',ROOT/'attempts/full-types-bodies.attempt2.dump']:
    h=hashlib.sha256();n=0;z=f.with_suffix(f.suffix+'.gz')
    with f.open('rb') as src,z.open('wb') as dst:
        with gzip.GzipFile(filename='',mode='wb',fileobj=dst,compresslevel=1,mtime=0) as out:
            for chunk in iter(lambda:src.read(1024*1024),b''):h.update(chunk);n+=len(chunk);out.write(chunk)
    verify=hashlib.sha256()
    with gzip.open(z,'rb') as src:
        for chunk in iter(lambda:src.read(1024*1024),b''):verify.update(chunk)
    assert verify.hexdigest()==h.hexdigest()
    summary['types_bodies_dump'][str(f.relative_to(ROOT))]={'uncompressed_bytes':n,'uncompressed_sha256':h.hexdigest(),'lossless_gzip':str(z.relative_to(ROOT)),'gzip_sha256':sha(z.read_bytes()),'gzip_bytes':z.stat().st_size,'roundtrip_verified':True}
    f.unlink() # task-generated duplicate raw bytes are retained losslessly in the verified gzip
(ROOT/'native-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ['source_fake_closure_scan','new_SP_declarations','prior_imported_closure_declarations_not_reachable_from_SP_roots']},indent=2))
