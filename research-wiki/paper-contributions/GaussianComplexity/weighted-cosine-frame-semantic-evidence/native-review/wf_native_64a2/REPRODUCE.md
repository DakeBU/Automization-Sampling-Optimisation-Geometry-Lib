Original execution evidence is the preserved receipts, not a replay label.

The native checks require macOS arm64, the exact Lean4.33.0 executable SHA256 in input-manifest.json, and all nine exact clean dependency checkouts and their existing pinned Mathlib/dependency caches under a supplied ASTIS-GC repository. No ASTIS olean cache is used.

The optional standalone recipe is:

    python3 replay_native.py --repo /absolute/path/to/ASTIS-GC --output /absolute/path/to/a/new-empty-output

It recompiles the frozen six sources in topological order, reapplies the two literal statement-seal propositions, and reexports native44-constant types, bodies, axiom closures and owned reachability. The new output directory must not exist. This recipe was syntax-checked; the original build was executed by build.py, advance_checks.py and InspectNativeV2.lean, with raw argv/exit/stdout/stderr under receipts/.

Static reader execution used reader_static.py with the current production render_unit, export_sources and render_source_module functions. The renderer source snapshots are in runtime/, with their exact SHA256s in reader-static.json; the renderer resolved only the six frozen source modules. The canonical theme reference was copied read-only from the current generated textbook index solely for source export. No shared whole-site generation occurred. Reader-static.json explicitly lists unexercised browser/mobile/graph/copy/download/public scopes.

The portable manifest carries bounded sources, driver history and critical native/static/environment receipts. Large local native proof-body exports are hashed references, deliberately not copied into the portable bundle. All44 types and bodies remain locally retained in the verifier directory.
