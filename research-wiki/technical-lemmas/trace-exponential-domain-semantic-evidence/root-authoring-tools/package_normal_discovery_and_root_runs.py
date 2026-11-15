from pathlib import Path
import json,hashlib,gzip,io
r=Path.cwd();w=r/'.astis/huanjian-gc-trace-mgf-domain-20261115'
e=r/'research-wiki/technical-lemmas/trace-exponential-domain-semantic-evidence'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=r/'.astis/semantic-neutral-20261115/trace_exp_fresh_source_51c8/normal-discovery-validation'
manifest=s/'public-leaf-manifest.json';assert sha(manifest)=='a1c050c1da323c67623031a116d8fb2f4844757cf1ee9d5bfb3dcf0bd8fd1302'
m=json.loads(manifest.read_text());assert m['actual_normal_API_calls']==1 and m['all18_preservation_checks_pass'] is True
dest=e/'normal-discovery-validation/trace_exp_fresh_source_51c8';assert not dest.exists();dest.mkdir(parents=True)
rows=[]
for x in m['public_leaves']:
    p=r/x['path'];assert p.is_relative_to(s) and p.parent==s and sha(p)==x['sha256']
    q=dest/p.name;q.write_bytes(p.read_bytes());rows.append({'original':x['path'],'portable':str(q.relative_to(r)),'sha256':sha(q)})
(dest/manifest.name).write_bytes(manifest.read_bytes())
(dest/'ROOT-byte-exact-custody.v1.json').write_text(json.dumps({
 'kind':'ROOT-later-exact-allowlist-copy','files':rows,
 'execution_evidence_qualification':'The original independent driver-process.receipt.json is the actor-authored exact transcript of actual exec/poll tool observations and real exit0, not an OS-generated process recorder. The separate normal-validation.receipt.json was written by the executed driver. No ROOT execution or original-actor-created-container claim.',
 'private_exclusions':'All complete guards/maps/index/raw global ledgers/API logs/driver/preparation excluded. This is conceptual mechanism validation, not proof V or transport.'},ensure_ascii=False,indent=2)+'\n')
cp=r/'research-wiki/frontier-cells/ASTIS-SHARED-REAL-TRACE-EXPONENTIAL-DOMAIN.json';c=json.loads(cp.read_text())
c['conceptual_mirror_audit']['scope']='Raw typed Discovery plus one real independent normal validation; source/CM actor51c8 differs from creator. No formal transport/global graph or proofV.'
c['conceptual_mirror_audit']['independent_normal_validation']={'actor':'trace_exp_fresh_source_51c8','actual_calls':1,
 'exact_append_sha256':'08bdafdd44953cb0541b028a555004e3786de1b7737463afcbc73f3bc8ed16d5',
 'receipt':str((dest/'normal-validation.receipt.json').relative_to(r)),'all18_preservation_checks_pass':True}
c['graph_contribution']['classification_qualification']='One typed conceptual mechanism independently normal-validated under the existing bounded-single-variable-laplace family. Actual native P/T parents confirmed. Global graph stabilization remains held; validation is not a formal implication or proofV.'
cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
mem=e/'local-cycle-memory.json';v=json.loads(mem.read_text());v['conceptual_Discovery']='validated once by independent source/CM reviewer; no formal transport';mem.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
runroot=r/'.astis/huanjian-resume-20261103';target=e/'root-postproof-actual-runs';target.mkdir(exist_ok=True)
selected=[]
for p in sorted(runroot.glob('20261115T08*-gc-trace-exp*.receipt.json')):
    v=json.loads(p.read_text());log=Path(v['log']);assert sha(log)==v['log_sha256']
    # Only this packet's explicitly prefixed own postproof runs; no global API snapshots.
    if p.name.startswith('20261115T08') and ('gc-trace-exp-' in p.name or 'gc-trace-exponential-domain-apply-authored-v3-' in p.name):
        (target/p.name).write_bytes(p.read_bytes())
        buf=io.BytesIO()
        with gzip.GzipFile(fileobj=buf,mode='wb',filename='',mtime=0) as gz:gz.write(log.read_bytes())
        q=target/(log.name+'.gz');q.write_bytes(buf.getvalue())
        assert hashlib.sha256(gzip.decompress(q.read_bytes())).hexdigest()==v['log_sha256']
        selected.append({'receipt':str((target/p.name).relative_to(r)),'receipt_sha256':sha(p),
            'lossless_log':str(q.relative_to(r)),'decoded_log_sha256':v['log_sha256'],'actual_exit_code':v['exit_code'],
            'actual_HEAD_before':v['head_before'],'actual_HEAD_after':v['head_after']})
(target/'ROOT-later-original-receipt-log-custody.v1.json').write_text(json.dumps({
 'kind':'ROOT-later-exact-original-receipts-and-lossless-logs','records':selected,
 'boundary':'All actual failures retained, never relabelled PASS. Receipt HEADs describe execution time; no future metadata/public identity is retroactively claimed built.'},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'independent_normal_Discovery':'validated once; proofV0','selected_bounded_D_originals':4,
 'root_actual_records':len(selected),'normal_PL_calls':0,'Root_V_calls':0}))
