# Observed public Bench history at v0.27

The [frozen public receipt](receipt.json) records the declared origins and
exact commit IDs for `main` and the 17 then-observed public Bench branches.
The offline guard returned `not-shallow-declared-tips-only`. This inventory
includes retired catalog entries reachable from those tips; it does not
enumerate every public draft, fork, old branch head or possible paraphrase.
No private reservation or model result is attached.

Use the exact commit IDs in the receipt, not the mutable branch names:

```powershell
$receipt = Get-Content benchmarks/samplingoptimisationgeometrybench/reviews/exposure-v027/receipt.json -Raw | ConvertFrom-Json
$tips = foreach ($tip in $receipt.public_tips) { '--public-tip'; $tip.commit }
python tools/sog_bench_split_guard.py @tips
```

This observed repository was already a blob-filtered partial clone. A
fetch of `main` with `--unshallow --filter=blob:none --no-tags` removed its
single shallow boundary without changing the worktree or retrieving the
historical proof/log blobs. The subsequent guard ran offline against
available catalog objects. Missing objects fail the guard; fetch only
missing public evidence before trying again. Update the *declared* public
tips separately for any future reservation; the frozen receipt is a
replay baseline, not a current contamination certificate.
