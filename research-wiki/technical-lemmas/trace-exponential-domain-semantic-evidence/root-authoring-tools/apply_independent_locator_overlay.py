from pathlib import Path
import json,hashlib,copy
r=Path.cwd();e=r/'research-wiki/technical-lemmas/trace-exponential-domain-semantic-evidence'
p=r/'.astis/semantic-neutral-20261115/trace_exp_fresh_source_51c8/phase2_correspondence_locator_repair_overlay.v1.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(p)=='03769e8d7ea683d02ee5073186429e4e1780027e381bf5f431a2b9473d9c136f'
overlay=json.loads(p.read_text());before=r/overlay['input_file'];assert sha(before)==overlay['input_sha256']
a=json.loads(before.read_text());v=copy.deepcopy(a)
for x in overlay['corrections']:
    i=x['correspondence_index_0based'];row=v['correspondence'][i]
    assert row['LF_lines_1based_inclusive']==x['original_lines']
    assert row['line_reference_file']==x['line_reference_file']
    lines=(r/x['line_reference_file']).read_text().splitlines(keepends=True)
    for span in x['proposed_span_hashes']:
        first,last=span['lines_inclusive']
        assert hashlib.sha256(''.join(lines[first-1:last]).encode()).hexdigest()==span['sha256']
    row['LF_lines_1based_inclusive']=x['proposed_lines']
v['locator_correction_overlay']={'original_independent_file':str(p.relative_to(r)),'sha256':sha(p),
    'applied_changes':'Exactly three independently proposed locator arrays; no other correspondence/mathematical payload changed.',
    'source_predecessor_file':str(before.relative_to(r)),'source_predecessor_sha256':sha(before),
    'independent_delta_acceptance':'pending'}
out=e/'source-to-lean.correspondence.authored-v3.json';assert not out.exists()
out.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
dest=e/'source-review-locator-overlay.original.v1.json';assert not dest.exists();dest.write_bytes(p.read_bytes())
print(json.dumps({'file':str(out.relative_to(r)),'sha256':sha(out),'mathematical_payload_changed':False,'independent_delta_review_pending':True}))
