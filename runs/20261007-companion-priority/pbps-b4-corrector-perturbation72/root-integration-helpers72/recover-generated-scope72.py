from pathlib import Path
import hashlib, json, os, re, subprocess

root = Path.cwd().resolve()
r = root / 'runs/20261007-companion-priority/pbps-b4-corrector-perturbation72/integration72'
dest = r / 'generator-sideeffects'
load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
baseline = load(r / 'before-generator-state.json')
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
assert head == baseline['head']
keep = set(baseline['keep'])
assert not (dest / 'receipt.json').exists()
failed = load(r / 'narrow-generated-scope/receipt.json')
assert failed['terminal_closed'] and failed['exit_code'] == 1
log = (r / 'module-graph-refresh/stdout.log').read_text(encoding='utf8').replace('\\', '/')
candidates = {'MANIFEST.md'}
for line in log.splitlines():
    if line.startswith('- '):
        candidates.add(line[2:].strip())
    elif line.startswith('wrote '):
        candidates.add(line[6:].strip())
tracked = set(subprocess.check_output(['git', 'ls-files'], text=True).splitlines())
possible = sorted(p for p in candidates & tracked if p not in keep and p not in baseline['preexisting_tracked_changes'])
head_backups = sorted(dest.glob('*.HEAD.exactraw.snapshot'))
assert len(head_backups) == 98
matches = []
for q in head_backups:
    matches.append([p for p in possible if sha((root / p).read_bytes()) == sha(q.read_bytes())])
    assert matches[-1], q

# Recover the original sorted path sequence from exact HEAD bytes. Reject ambiguity.
solutions = []
def visit(i, previous, selected):
    if len(solutions) > 1:
        return
    if i == len(matches):
        solutions.append(selected)
        return
    for p in matches[i]:
        if p > previous:
            visit(i + 1, p, selected + [p])
visit(0, '', [])
assert len(solutions) == 1, ('ambiguous-or-incomplete-recovery', len(solutions))
extras = solutions[0]
rows = []
for i, p in enumerate(extras):
    q = dest / f'{i:04d}.generated.exactraw.snapshot'
    h = dest / f'{i:04d}.HEAD.exactraw.snapshot'
    old = subprocess.check_output(['git', 'show', head + ':' + p])
    assert old == h.read_bytes() == (root / p).read_bytes()
    assert q.is_file()
    rows.append(dict(path=p, action='RESTORE_PREVIOUSLY_CLEAN_HEAD_AFTER_EXACT_GENERATED_BACKUP', generated_backup=q.relative_to(root).as_posix(), generated_RAW_sha256=sha(q.read_bytes()), HEAD_backup=h.relative_to(root).as_posix(), HEAD_RAW_sha256=sha(old), recovered_from_unique_sorted_exact_HEAD_match=True))

newcards = sorted(p for p in candidates if p.startswith('research-wiki/sampling-sde-library/cards/') and p.endswith('.md') and p not in tracked and p not in keep and p not in baseline['untracked_cards'])
assert len(newcards) == 443
for i, p in enumerate(newcards, len(extras)):
    q = dest / f'{i:04d}.generated-new-card.exactraw.snapshot'
    assert q.is_file() and not (root / p).exists()
    assert Path(p).stem.encode() in q.read_bytes(), p
    rows.append(dict(path=p, action='PRESERVE_UNUSED_NEW_GENERATED_CARD_IN_EXACT_BACKUP', generated_backup=q.relative_to(root).as_posix(), generated_RAW_sha256=sha(q.read_bytes()), recovered_from_finite_generator_output_and_backup_index=True))

trim = []
names = ['docs/module-graph.svg', 'docs/assets/astis_lean_arsenal_module_graph.svg', 'research-wiki/sampling-sde-library/cards/AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCorrectorPerturbation.md', 'research-wiki/sampling-sde-library/cards/AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorPerturbation.md']
for name in names:
    p = (root / name).resolve()
    assert p.is_relative_to(root) and name in keep
    raw = p.read_bytes()
    clean = b''.join(z.rstrip(b'\r\n').rstrip(b' \t') + (b'\r\n' if z.endswith(b'\r\n') else b'\n' if z.endswith(b'\n') else b'') for z in raw.splitlines(keepends=True))
    if raw == clean:
        continue
    q = dest / ('mutable-generated-' + sha(name.encode()) + '.before.exactraw.snapshot')
    if q.exists():
        assert q.read_bytes() == raw
    else:
        q.write_bytes(raw)
    temp = dest / ('mutable-generated-' + sha(name.encode()) + '.clean.pending')
    assert not temp.exists()
    temp.write_bytes(clean)
    assert p.read_bytes() == raw and temp.read_bytes() == clean
    os.replace(temp, p)
    assert p.read_bytes() == clean
    trim.append(dict(path=name, before_RAW_sha256=sha(raw), after_RAW_sha256=sha(clean), backup=q.relative_to(root).as_posix(), only_trailing_ASCII_space_tab_removed=True, guarded_atomic_replace=True))
assert set(subprocess.check_output(['git', '-c', 'core.autocrlf=false', 'diff', '--name-only'], text=True).splitlines()) <= keep
out = dict(status='BOUNDED72_GENERATED_SCOPE_WITH_EXACT_BACKUPS', actual_PID=os.getpid(), recovered_partial_failure=failed, tracked_generated_restored=len(extras), unused_new_generated_cards_preserved=len(newcards), rows=rows, mutable_generated_ASCII_trims=trim, canonical_Lean_source_review_unchanged=True, old_frontiers_and_untracked_cards_preserved=True)
(dest / 'receipt.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
print('PASS72 partial generator recovery:', len(extras), 'unique exact HEAD paths;', len(newcards), 'preserved cards;', len(trim), 'ASCII trims; no Lean changes')
