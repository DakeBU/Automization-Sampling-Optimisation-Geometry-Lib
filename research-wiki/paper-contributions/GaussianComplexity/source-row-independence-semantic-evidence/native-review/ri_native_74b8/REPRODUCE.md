# Bounded independent replay

The compile credit is exclusively commit `66e0bb9b748d68816a8443d60696656c9340222f`.
The archive includes exact frozen target source, protocols, pins, Python renderer
closure, bounded source/background spans, original 204-member preproof archive,
all generated Lean audits, own scripts, original command streams and receipts.
It does not contain ASTIS `.olean` caches or the large native body dump.

Use the repository with the pinned Lean 4.33.0 native binary, manifest and nine
clean pinned packages. Create a fresh sibling audit directory under
`.astis/semantic-neutral-20261112/` and copy this archive's scripts and `scratch`
Lean audit files there. Keep the delivered directory and its receipts intact.

Run `python3 <fresh>/run.py prepare-replay python3 <fresh>/prepare.py` from the
repository root. That derives and freezes imports from the exact candidate
commit and checks the native binary and all nine packages, including untracked
cleanliness. Run the equivalent `run.py build-replay python3 <fresh>/build.py`;
it compiles each entire ASTIS closure module into a fresh empty `native-olean`
directory. `LEAN_PATH` consists solely of that directory and pinned package
cache directories; no repository ASTIS build cache is reachable.

The exact original generated native inspector is `scratch/InspectAll.lean`.
Run `<fresh>/relocate_inspector.py` to create `InspectAllRelocated.lean`; only its
JSON output path changes. With the `LEAN_PATH` recorded in the new manifest,
run the actual native binary on `InspectAllRelocated.lean`,
`IndependentLiteralCheck.lean`, `StandardApplicability.lean`, and
`KernelMeaning.lean`. Run the unchanged actual author probe too. The inspector
regenerates the omitted full native type/body dump; its delivered local hash is
in `native-summary.json`. The two independent literal Props derive directly
from the frozen Statement Seal, translating the theorem binder/result colon to
the `forall` comma without changing the proposition.

For static replay, freeze the local Python import closure with
`freeze_renderer_deps.py` and run `reader_static.py`, then `static_extra.py`.
These call actual production `render_unit`, `export_sources`, and
`render_source_module`; they do not build the whole site. The local `_site`
textbook shell is only a theme reference and is included under
`inputs/theme-reference.html`. Exact `.lean` download target files are locally
materialized and byte-compared, without a click/download runtime claim.

`locators.py` recomputes every locator using the original raw paper HTML at the
path and SHA recorded in the seal. Only bounded spans are exported here. The
same script re-reads and verifies all 204 members of the preserved bounded
original archive. `history_detail.py` verifies exact failed formation/API
streams; `supplement.py` runs the production fake-closure scanner and prints
the kernel definitions. No prior verifier verdict supplies own native credit.

`relevant-input-binding.json` is the complete tracked input hash list for a later
held metadata carrier comparison. Reusing this evidence requires equality of
every listed byte hash, author probe, binary, manifest and package pin/clean
state. A later carrier does not gain fresh compilation credit.

`reader_static.rejected-import-v1.py` and the exit-1 original streams preserve
the single rejected isolated-renderer setup attempt. Its missing local Python
dependency was repaired by freezing exact production dependencies; it never
implied a theorem failure. Source fidelity, public delivery, global graph/site,
root Tests/full repository checks, integration and purification remain separate.
