from pathlib import Path
import hashlib, json, os, subprocess

root = Path.cwd().resolve()
r = Path('runs/20261007-companion-priority/pbps-reflection-intertwining69')
load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
def pin(p):
    p = Path(p); b = p.read_bytes()
    return dict(path=p.resolve().as_posix(), RAW_bytes=len(b), RAW_sha256=sha(b),
                LF_sha256=sha(b.replace(b'\r\n', b'\n')))

notes = load(r/'integration.notes.json')
assert notes['status'] == 'SERIALIZED_SHARED_AGGREGATE69_AND_CURRENT_GRAPH_PASS_NOT_MAIN_NOT_PURIFIED'
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
assert head == notes['proof_commit'] == '2d286c283a6fb5dfc13180204bb0da54531a5c67'
plan = load(r/'publication-plan.json')
paths = [Path(p) for p in [
    'lean-toolchain', 'lake-manifest.json', 'AutoSamplingTheory/ExampleCases.lean',
    'AutoSamplingTheory/TechnicalLemmas/Registry.lean', 'Tests/Basic.lean',
    'docs/companion-papers-handoff.md', 'website/content/samplewiki_companion_frontiers.json',
    'research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl',
    'runs/substantive_advances.jsonl', 'docs/module-graph.svg',
    'docs/assets/astis_lean_arsenal_module_graph.svg',
    'research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json',
    'research-wiki/sampling-sde-library/lean-leaf-module-graph.md',
    'research-wiki/sampling-sde-library/cards/AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionIntertwining.md',
    'AutoSamplingTheory/ExampleCases/ProximalBPS/ReflectionIntertwining.lean',
    '_site/data/underlying-lean-graph.json',
    '_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html',
]]
for slug, aid, cid in zip(plan['slugs'], plan['audit_ids'], plan['active_cells']):
    paths += [Path('website/content/publications')/(slug+'.json'),
              Path('website/content/declaration_lessons')/(slug+'.json'),
              Path('research-wiki/semantic-roundtrip/audits')/(aid+'.json'),
              Path('research-wiki/frontier-cells')/(cid+'.json')]
paths += [r/p for p in ['claim.json', 'publication-plan.json', 'integration.notes.json',
    'visual.inspection.json', 'integration69/final-admin.json',
    'root.source69.adoption.json', 'root.exact-verification69.adoption.json']]
for check in notes['checks']:
    d = r/'integration69'/check['label']
    paths += [d/p for p in ['receipt.json', 'stdout.log', 'stderr.log']]
paths += sorted(p for p in (r/'integration69/visual69').iterdir() if p.is_file())
for native in ['independent-math69/lease.final.json', 'independent-source69/lease.final.json',
               'exact-science-verification69/lease.final.json', 'anonymous-decoder/lease.json']:
    paths.append(r/native)
paths = list(dict.fromkeys(paths))
assert all(p.is_file() for p in paths)
dest = r/'final-reader-repository-packet69.json'
assert not dest.exists()
packet = dict(status='FROZEN_FINAL69_FOR_INDEPENDENT_REPOSITORY_AND_SCOPED_READER',
    actual_root_pid=os.getpid(), checked_science_commit=head,
    inputs=[pin(p) for p in paths], RAW_authority=True, LF_rule='CRLF to LF only',
    expected=dict(registry_count=517, root_jobs=9179, test_jobs=9479,
                  publication_units=238, statements=1, formula_BODY_steps=6,
                  actual_captures=8, code_copy_callbacks=3, RAW_downloads=3),
    native_science_source_decoder_reviews_reused=True,
    independent_aggregate_reader_verdict_pending=True,
    full_Exposition_Seal=False, PURIFIED=False, main_live=False,
    wholepaper_or_Goal_complete=False)
dest.write_text(json.dumps(packet, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
print(json.dumps(dict(status='FINAL_READER69_PACKET_FROZEN', inputs=len(paths),
                     RAW_sha256=sha(dest.read_bytes()), checked_science_commit=head)))
