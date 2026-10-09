import datetime,hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent;run=out.parent;repo=pathlib.Path(r'E:\Samplinglib')
pre=repo/'runs/20261007-companion-priority/pbps-reflection-rotation-preproof69';old=pre/'independent-primary69'
def sha(b):return hashlib.sha256(b).hexdigest()
def put(n,d):(out/n).write_text(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
inputs=[]
def copy(n,p,role):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');(out/n).write_bytes(b);(out/(n+'.LF')).write_bytes(lf)
 inputs.append(dict(name=n,original_path=str(p),role=role,RAW_bytes=len(b),RAW_sha256=sha(b),LF_bytes=len(lf),LF_sha256=sha(lf)));return b
mf=json.loads(copy('current.math-freeze.theorem-only69.RAW.json',run/'math-freeze.theorem-only69.json','current-mathematics-freeze-no-source-verdict'))
pf=json.loads(copy('current.publication-freeze69.RAW.json',run/'publication-freeze69.json','current-publication-freeze-no-source-verdict'))
paths=[('current.ReflectionIntertwining.RAW.lean',repo/'AutoSamplingTheory/ExampleCases/ProximalBPS/ReflectionIntertwining.lean','FULL-current-module-including-private-Prop-public-callers-and-entire-proof'),
 ('current.publication.RAW.json',repo/'website/content/publications/pbps-actual-reflection-intertwining.json','current-attributed-reader-publication; authored classifications-not-evidence'),
 ('current.lesson.RAW.json',repo/'website/content/declaration_lessons/pbps-actual-reflection-intertwining.json','current-complete-reader-lesson-and-six-exact-BODY-steps'),
 ('current.frontier-cell.RAW.json',repo/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-reflection-intertwining.json','current-bounded-frontier-cell'),
 ('current.lean-toolchain.RAW',repo/'lean-toolchain','pinned-toolchain'),('current.lake-manifest.RAW.json',repo/'lake-manifest.json','pinned-dependency-manifest'),
 ('current.focused.receipt.RAW.json',run/'focused69-v2/receipt.json','actual-focused-compiler-receipt'),
 ('current.focused.stdout.RAW.log',run/'focused69-v2/stdout.log','actual-focused-compiler-output'),
 ('current.focused.stderr.RAW.log',run/'focused69-v2/stderr.log','actual-focused-compiler-stderr')]
all_expected={x['path']:x for x in mf['inputs']+pf['inputs']}
for n,p,r in paths:
 b=copy(n,p,r);x=all_expected[str(p).replace('\\','/')]
 assert len(b)==x['raw_bytes'] and sha(b)==x['raw_sha256'] and sha(b.replace(b'\r\n',b'\n'))==x['lf_sha256']
for n in ['source-proof-graph.json','source-expectations.json','source-coverage-inventory.json','source-input-regions.json','literal-formulas-and-conditions.json','lease.final.json','owned-manifest.json']:
 copy('frozen-source.'+n,old/n,'immutable-source-first-only-evidence; no-old-source-candidate-verdict')
assert sha((old/'lease.final.json').read_bytes())=='2d168d568a260f2cc18fba260a5bd7c1ac45cb41602f6a359df3d16b387aec93'
assert sha((old/'source-proof-graph.json').read_bytes())=='1b464d9452b722abbaa6e274872366d8771780f96bc263dfeeb86322c2e88b8c'
assert sha((old/'source-expectations.json').read_bytes())=='c4580c95682580e8a3a0bc68585efa98c9c659e52c928a0a6dbfdbaa6dcc62cf'
for p in sorted(old.glob('source.*.RAW.html')):copy(p.name,p,'immutable-fixed-primary-RAW-source-region')
for n in ['header0-expanded.lean','header0-public.lean','statement0.definition.lean','existing-parent67-statement.exactraw.fragment.lean','existing-parent67-statement.fragment-map.json']:
 copy('sealed.'+n,pre/n,'literal-current-input-seal-or-parent-header-only; no-acceptance-verdict')
copy('protocol.semantic-roundtrip.SKILL.RAW.md',repo/'.agents/skills/astis-semantic-roundtrip/SKILL.md','applicable-workflow-control')
copy('protocol.theorem-publication.RAW.md',repo/'docs/theorem-publication-protocol.md','applicable-workflow-control')
module=(out/'current.ReflectionIntertwining.RAW.lean').read_text(encoding='utf-8')
(out/'current.module.numbered.txt').write_text(''.join('%04d %s\n'%(i,l) for i,l in enumerate(module.splitlines(),1)),encoding='utf-8')
put('current-input-manifest.json',dict(schema='source69-current-snapshot-before-final-packet-v1',inputs=inputs,count=len(inputs),
 LF_recipe='replace only CRLF byte pairs by LF; preserve every other byte',reviewer_packet_received=False,blind_reconstruction_received=False,
 no_68_review_decoder_body_read=True,no_prior_semantic_slots_deltas_verdicts_or_repairs_read=True,
 source_native_CLOSED82_unmodified=True,header_native_CLOSED84_unmodified=True))
put('source-review.open.json',dict(schema='source69-open-prepacket-review-v1',actual_pid=os.getpid(),start_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 owner='/root/independent_primary69',status='OPEN_WAITING_CANONICAL_PACKET_WHILE_REVIEWING_CURRENT_BODY',owned_path=str(out),final_source_verdict=False))
print(json.dumps(dict(actual_pid=os.getpid(),input_count=len(inputs),module_RAW_sha256=sha((out/'current.ReflectionIntertwining.RAW.lean').read_bytes()),module_lines=len(module.splitlines()),
 source_regions=len(list(out.glob('source.*.RAW.html'))),final_verdict=False),sort_keys=True))
