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

## Bind actual private prose tasks before delivering prompts

The schema-1 review above covers reservation metadata. It does **not** let an
operator hand questions to a model. For an offline **prose-only** evaluation
input, store an additional private JSON object with `schema_version: 1`,
`split: "private-test"`, and `tasks` containing exactly the reserved task IDs.
Each row has these fields:

| Fields | Contract |
| --- | --- |
| `id`, `family` | Exact reservation IDs, one row per task. |
| `domain`, `level`, `skills` | Names from the current Bench curriculum; level is provisional, skills are a nonempty list. |
| `assumptions`, `question` | Complete hypothesis strings and question; the gate recomputes the normalized reservation fingerprint. |
| `retrieval_profile`, `allowed_tools` | `closed-book` or `open-library`, plus the declared tool list; not a tool sandbox. |
| `source_notes`, `proof_steps`, `rubric` | Private source/rights and dependency notes, complete formula proof as a list of steps, four distinct one-point criteria. |

Keep the reservation, task packet and all outputs in a private directory with
appropriate local access controls (preferably outside any checkout or sync
folder). The tool checks that paths in this repository stay in ignored `.astis`
and creates new files with owner-only POSIX permissions. It does not manage
directory permissions, Windows ACLs or other repositories/sync folders.
Use a new output file in an existing private directory. No existing file will
be overwritten. Do not put payloads in shell arguments or CI.

1. Add `--prose-packet TASKS.json --prose-review-request REQUEST.json` to the
   reservation command with exact known public tips. The request has one
   **unsigned** entry per family. The reviewer must inspect the actual packet
   and reservation, not just the request. They complete each entry's `review`
   object (schema 2, including `prose_packet_sha256`) and save that object in
   their own file. A local parser cannot authenticate this person or verify the
   claims in their review. The proof, rubric, source notes, exact prompt and
   tool policy all participate in the family packet digest. JSON layout and
   task-row ordering do not.
2. Bind the raw bytes of each completed review in the corresponding
   reservation row as before. Use the same public tips and packet. Replace
   `--prose-review-request REQUEST.json` with `--review-file REVIEW.json`
   (repeat once per family) and `--prose-prompts PROMPTS.jsonl`. Schema-1
   metadata-only reviews are rejected in this mode. A stale review, changed
   proof/rubric, unreserved task or known public collision cannot emit prompts.
3. Only send the resulting `PROMPTS.jsonl` to the model during the declared
   evaluation. Each row has task ID, assumption and question text, the tool
   policy, track/split, and a digest of **only the prompt fields**. No answer,
   answer-derived digest, family label or reviewer fields are generated; the
   reviewer must also check that free-text prompt fields contain no answer.
   Keep the output private; releasing it makes the questions exposed. The private
   source/solution/rubric is for operators and graders, never the tested model.

This gate does not register a real private family by itself, execute a model,
score responses, claim unseen generalization, or support private Lean/graph
tasks. The public prose scorer and training exports must not consume these
files. Repository tests use synthetic packets only.
