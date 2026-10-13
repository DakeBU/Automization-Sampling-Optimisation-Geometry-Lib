from pathlib import Path
import copy,hashlib,json
root=Path.cwd();r=root/'runs/20261007-companion-priority/pbps-centered-root64';out=r/'stale-cell-metadata-overlay64'
out.mkdir(exist_ok=False)
p=root/'research-wiki/frontier-cells/ASTIS-SHARED-l2-real-positive-square-order.json';b=p.read_bytes();before=json.loads(b);after=copy.deepcopy(before)
assert before['source_anchor']=='PBPS2609.06905v1 AppendixD1 square-root monotonicity; ASTIS real-L2 consequence for actual B15'
assert before['evidence']['truth_boundary']=='Arbitrary-real-L2 positive-square-order auxiliary result, with actual B15 consumer; independent reviews pending.'
after['source_anchor']='ASTIS auxiliary arbitrary-real-L2 positive-square-order consequence via pinned Mathlib CFC monotonicity, consumed by PBPSv1 AppendixB15; AppendixD1 supplies spectral and unique-nonnegative-root background, not this printed theorem.'
after['evidence']['truth_boundary']='Arbitrary-real-L2 positive-square-order auxiliary with genuine actual B15 consumer; SCI64 independently VERIFIED at59fff63, INT64 locally integrated and independently accepted with bounded reader debt at0aef19c. Full Exposition/PURIFIED, merged/live and whole-paper completion remain unclaimed.'
(out/'cell.before.exactraw.snapshot.json').write_bytes(b)
(out/'cell.after.proposed.json').write_text(json.dumps(after,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
assert {k for k in before if before[k]!=after[k]}=={'source_anchor','evidence'}
assert {k for k in before['evidence'] if before['evidence'][k]!=after['evidence'][k]}=={'truth_boundary'}
proposal=dict(scope='Exactly two stale attribution/process metadata fields; no theorem, header, source review, compiled input, proof, dependency or canonical write.',canonical_path=p.relative_to(root).as_posix(),canonical_before_RAW_sha256=hashlib.sha256(b).hexdigest(),changed_fields=['source_anchor','evidence.truth_boundary'],evidence=[(r/'repository-exposition64/review.json').relative_to(root).as_posix(),(r/'root.repository-exposition64.adoption.json').relative_to(root).as_posix(),(r/'root.source64.overlay-adoption.json').relative_to(root).as_posix(),'website/content/publications/real-l2-positive-square-order.json'],apply_policy='Only after separate independent overlay acceptance; root at next serialized65 stabilization.',canonical_applied=False)
(out/'proposal.json').write_text(json.dumps(proposal,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Prepared exact two-field metadata overlay64; canonical untouched, independent review pending.')
