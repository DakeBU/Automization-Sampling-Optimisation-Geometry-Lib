# Bind private-family review evidence

This supplements the [family isolation policy](../benchmarks/samplingoptimisationgeometrybench/FAMILY_ISOLATION.md).
All checked-in tasks are still public development material. The steps below
do not release a private split, authenticate a reviewer, compile a Lean answer,
or establish that a model has not seen an item.

1. Run the offline exposure inventory over the exact declared public tips,
   including exposed PR and retired tips. Keep the returned
   `public_history_sha256`. A shallow checkout provides observation only;
   a reservation requires available non-shallow history and its catalog objects.
   The [v0.27 public receipt](../benchmarks/samplingoptimisationgeometrybench/reviews/exposure-v027/README.md)
   is a reproducible example using exact declared tips and a blob-filtered
   acquisition of the missing history. Recompute exposure for any actual
   reservation; do not use that dated receipt as an exhaustive tip list.
2. Prepare the reservation outside the repository or in ignored `.astis`.
   A distinct reviewer examines the actual private prompts, solutions, source
   and public-family comparisons. The reviewer records the binding and four
   checks below in a separate local JSON file. Do not publish either file,
   paste private contents into CI or issues, or send these files to a learner.
3. Put the SHA-256 of the review file's **raw bytes** into the family's
   `provenance.review_sha256`. The family digest is
   `tools.sog_bench_split_guard.family_review_binding(family_row)`: canonical
   UTF-8 JSON of the exact family row with only `review_sha256` excluded. This
   avoids a circular hash while binding the author, reviewer, source references,
   lineage, task IDs and the declared prompt/target fingerprints.
4. Re-run the guard with one `--review-file` per family. The same exact
   public-history digest and unchanged family row must be used.

A report has this shape (all values below are synthetic examples, not evidence):

```json
{
  "schema_version": 1,
  "scope": "private-family editorial review; not identity authentication",
  "reviewer": "example-independent-reviewer",
  "public_history_sha256": "1111111111111111111111111111111111111111111111111111111111111111",
  "family_binding_sha256": "2222222222222222222222222222222222222222222222222222222222222222",
  "verdict": "accept",
  "checks": {
    "originality": "Explain the original task and why this is not a public variant.",
    "public_lineage": "Record the actual comparison with the declared public exposure.",
    "rights": "Record the applicable original-material rights and restricted-source exclusion.",
    "target_alignment": "Check the actual private prompt and fixed target, or note the absence of a Lean target."
  }
}
```

```text
python tools/sog_bench_split_guard.py --public-tip PUBLIC_RELEASE_SHA --public-tip PUBLIC_PR_SHA --reservation PRIVATE_RESERVATION_JSON --review-file PRIVATE_REVIEW_JSON
```

A successful evidence check requires both no known public conflict and
`private_review_check.all_review_files_bound: true`. Without review files, the
command remains a metadata-only preflight and says so in its output. Exact
review bytes cannot be reused across families; changes to the reviewed
family or declared public history require a fresh review. A rejected verdict
is never an acceptance. Reports are capped at 64 KiB each, up to 128 in one
local check. Output is aggregate only: no private paths, prompt hashes, notes
or family IDs are printed.

This is consistency evidence for the declared scope, not a secrecy guarantee,
a reviewer signature, a certificate of independence from all public content,
or a substitute for source fidelity and fixed-target compiler tests.
