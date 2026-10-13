from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, sys

root = Path.cwd()
r = Path('runs/20261007-companion-priority/pbps-reflection-intertwining69')
load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()

def pin(p):
    p = Path(p); b = p.read_bytes()
    return dict(path=p.as_posix(), bytes=len(b), raw_sha256=sha(b),
                lf_sha256=sha(b.replace(b'\r\n', b'\n')))

def write(p, x):
    p = Path(p); assert not p.exists(), p
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')

def gate(label):
    p = r/'integration69'/label/'receipt.json'; x = load(p)
    assert x['exit_code'] == 0 and x['terminal_closed'], label
    return dict(label=label, receipt=pin(p), stdout=x['stdout'], stderr=x['stderr'])

plan = load(r/'publication-plan.json')
proof = load(r/'root.exact-verification69.adoption.json')
assert proof['native_verified']
head = proof['verified_commit']
base_labels = ['mandatory-astis-check-final', 'python-compile', 'contributor',
               'publication', 'semantic-cli', 'frontier-cli', 'website-ci-build',
               'official-graph-before-visual', 'reader-cdp-capture', 'reader-copy-download']
checks = [gate(label) for label in base_labels]
jobs = [int(s) for s in re.findall(r'Build completed successfully \((\d+) jobs\)',
         (r/'integration69/mandatory-astis-check-final/stdout.log').read_text(encoding='utf-8'))]
assert len(jobs) == 2
mode = sys.argv[1]
if mode == 'admin':
    visual = Path('.astis/pbps-sharp-energy68/visual69-cdp')
    copy = Path('.astis/pbps-sharp-energy68/visual69-copy')
    capture = load(visual/'capture.json')
    assert capture['ownedBrowserExit']['code'] == 0 and len(capture['records']) == 8
    assert load(copy/'capture.json')['ownedBrowserExit']['code'] == 0
    publication_evidence = []
    for i, slug in enumerate(plan['slugs']):
        probe = load(copy/f'unit{i}-copy-and-download.inspect.json')
        lesson = load(Path('website/content/declaration_lessons')/(slug+'.json'))['units'][0]
        assert probe['initialFolded'] and probe['physicalOSClipboardTest'] is False
        assert len(probe['panels']) == len(probe['downloads']) == 3
        assert all(x['callbackCalled'] and x['copiedExactly'] and x['status'] == 'Copied' for x in probe['panels'])
        assert len(probe['steps']) == len(lesson['steps']) == 6
        for x, step in zip(probe['steps'], lesson['steps']):
            assert x['lean'] == step['lean'] and x['initiallyFolded']
        source = Path(load(r/'claim.json')['proposed_files'][i]).read_bytes()
        assert all(x['status'] == 200 and x['text'].encode() == source for x in probe['downloads'])
        publication_evidence.append(dict(publication=slug, panels=3, steps=len(lesson['steps']),
                                         downloads=3, source_RAW_sha256=sha(source)))
    dest = r/'integration69/visual69'; dest.mkdir(exist_ok=False); pins = []
    for folder, prefix in [(visual, 'render'), (copy, 'copy'), (Path('.astis/pbps-sharp-energy68/visual69-contacts'), 'inspection')]:
        for p in folder.iterdir():
            if p.is_file():
                q = dest/(prefix+'-'+p.name); q.write_bytes(p.read_bytes()); pins.append(pin(q))
    debts = ['Whole-paper/Chapter1.3 Exposition Seal and postmerge purification remain open.',
             'Dense inherited graph labels and full-statement Unicode/underscore notation remain bounded reader debt.',
             'The complete literal private Prop is also present in the existing adjacent proof helper fold; it remains a representation, not a proof provider or full Exposition Seal.',
             'Copy callbacks are isolated page probes, not a physical OS clipboard or live deployment test.']
    write(r/'visual.inspection.json', dict(status='SCOPED_LOCAL_RENDER_COPY_DOWNLOAD_INSPECTED',
          viewed_by_root=True, actual_root_pid=os.getpid(), capture_files=pins, capture=capture,
          publications=publication_evidence, observations=['One complete attributed statement, all six formula/BODY proof steps, complete private-Prop helper and exact actual branch inspected.',
          'Statement/proof/step Lean initially folded; three copy callbacks and three RAW production source downloads exact.'],
          debts=debts, full_exposition_seal=False, merged_live_purified=False))
    for i, cid in enumerate(plan['active_cells']):
        p = Path('research-wiki/frontier-cells')/(cid+'.json'); cell = load(p)
        assert cell['status'] == 'independently_verified'
        (r/f'integration69/cell.{i}.before-final-admin.exactraw.snapshot.json').write_bytes(p.read_bytes())
        cell['evidence']['serialized_shared_gate'] = dict(evidence=(r/'integration69/mandatory-astis-check-final/receipt.json').as_posix(),
            root_jobs=jobs[0], test_jobs=jobs[1], registry_count=517, status='PASS', proof_commit=head,
            scope='Exact SCI69 and serialized local aggregate only; independent repository/reader, remoteCI, main/live/PURIFIED remain distinct.')
        cell['graph_contribution']['visual_review'] = (r/'visual.inspection.json').as_posix()
        cell['blocked'] = dict(status=False, reason='Focused and independent math/decoder/source/exact-commit, reviewed metadata and local aggregate accepted within full-micro intertwining scope.')
        p.write_text(json.dumps(cell, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
    p = Path('docs/companion-papers-handoff.md'); raw = p.read_bytes(); text = raw.decode().replace('\r\n','\n')
    anchor = 'Serialized Registry517/imports/Tests and current reader/graph gates are pending\nagainst final admin state; exact science verification is separate from these\naggregate admissions and from remote CI.'
    assert text.count(anchor) == 1
    text = text.replace(anchor, f'Serialized local aggregate69: root{jobs[0]}, Tests{jobs[1]}, Registry517;238 publication units.\nOne complete statement, six formula/BODY steps, full private-Prop helper and actual\nbranch inspected; three isolated copy callbacks and three RAW downloads exact.\nCurrent graph regeneration follows these final cell writes; final gates are recorded\nin existing69 integration.notes.json. Python296 evidence is reused from INT64 against\nunchanged tools/site scripts. Independent repository/reader, remoteCI/main/live and\nfull Exposition/PURIFIED remain separate.')
    p.write_bytes(text.replace('\n', '\r\n' if b'\r\n' in raw else '\n').encode())
    write(r/'integration69/final-admin.json', dict(status='FINAL_CELL_ADMIN_WRITTEN_BEFORE_FINAL_GRAPH',
          proof_commit=head, cells=[pin(Path('research-wiki/frontier-cells')/(cid+'.json')) for cid in plan['active_cells']],
          root_jobs=jobs[0], test_jobs=jobs[1], registry_count=517, publication_units=238,
          final_graph_checks_pending=True, prior66_graph_freshness_withheld_preserved=True))
    print('PASS final admin69 written; final graph regeneration MUST follow. No cell writes after final graph checks.')
elif mode == 'final':
    for label in ['official-graph-final-admin', 'graph-check-actual-final',
                  'site-check-final', 'publication-final-admin', 'frontier-final-admin',
                  'contributor-final-admin', 'semantic-final-admin']:
        checks.append(gate(label))
    visual = load(r/'visual.inspection.json'); assert visual['viewed_by_root']
    final_admin = load(r/'integration69/final-admin.json')
    for x in final_admin['cells']:
        assert sha(Path(x['path']).read_bytes()) == x['raw_sha256'], x['path']
    sys.path.insert(0, str(Path('tools').resolve()))
    sys.path.insert(0, str(Path('website/scripts').resolve()))
    import publication_reader, underlying_lean_graph
    g = load('_site/data/underlying-lean-graph.json')
    assert g['publication_inputs_sha256'] == publication_reader.graph_input_digest()
    assert all(any(n.get('id') == 'decl:'+decl for n in g['nodes']) for decl in plan['mathematical_declarations'])
    underlying_lean_graph.validate(Path('_site'), g)
    baseline = '0aef19ca2711159eeaec86d42c9be142a94fa402'
    assert not subprocess.check_output(['git','diff','--name-only',baseline,'--','tools','website/scripts'], text=True).strip()
    regression = Path('runs/20261007-companion-priority/pbps-centered-root64/integration64/python-regression-suite/receipt.json')
    assert load(regression)['exit_code'] == 0
    write(r/'integration.notes.json', dict(status='SERIALIZED_SHARED_AGGREGATE69_AND_CURRENT_GRAPH_PASS_NOT_MAIN_NOT_PURIFIED',
          utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), proof_commit=head,
          registry_count=517, root_jobs=jobs[0], test_jobs=jobs[1], publication_units=238, checks=checks,
          visual_inspection=(r/'visual.inspection.json').as_posix(), final_cells=final_admin['cells'],
          current_graph=pin('_site/data/underlying-lean-graph.json'), retired_root_CLI_attempts=['integration69/semantic PID47776 EXIT2: wrong astis.py subcommand; corrected semantic-cli PID33732 EXIT0','integration69/frontier PID46100 EXIT2: wrong astis.py subcommand; corrected frontier-cli PID49036 EXIT0'], publication_inputs_sha256=g['publication_inputs_sha256'],
          prior66_graph_freshness_withheld_preserved=True,
          reused_python_tests=dict(count=296, exact_unchanged_tools_and_site_scripts=True, prior_receipt=pin(regression), rerun=False),
          graph_delta='One same-actual PBPS full-micro intertwining production theorem, one literal proposition representation and one module card; real existing parents with same-U adapter, no invented Test consumer or conceptual formal edge.',
          remaining=visual['debts']+['Actual projected rotation/mean preservation and B21 corrector change,H1/B4 dynamics/invariance/nonexplosion/main/errors/caps/expectedquerycost/actual-input composition remain open.'],
          sole_stabilization_owner='ASTIS-SA-20261005-SPHMCImplementedPhaseKernel', self_VERIFIED=False, Goal_complete=False))
    print('PASS local aggregate69 with FINAL cell hashes/current official graph,238publication units,517Registry; no post-graph cell mutations.')
else:
    raise ValueError(mode)
