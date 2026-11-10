# Keep held-out families separate

All existing Bench tasks are **public development material**. A new ID,
translation, paraphrase, alternate Lean target, or graph view of a public
exercise does not make it a held-out task. Put variants in the same family.
Genuinely independent tasks may still share library prerequisites. See the
[public evaluation workflow](EVALUATION.md) for running admitted tasks.

## Inventory known public exposure

Use a local repository with the public Bench history and objects available.
Collect the exact commit IDs of known exposed releases, public PR revisions,
and retired tips, including public histories no longer reachable from `main`.
Only supply commits known to have been public; never pass a private task branch.
From the repository root, replace the placeholders below with full commit IDs
and repeat `--public-tip` as needed (Python 3.11+, Windows or Linux):

```text
python tools/sog_bench_split_guard.py --public-tip PUBLIC_RELEASE_SHA --public-tip PUBLIC_PR_SHA
```

The guard reads the tracked public-dev catalog, exercise mappings attached to
Bench questions, and graph task IDs and families at the available revisions.
This includes catalog entries first introduced by a merge resolution and later
removed from the current catalog.
It does not fetch. A shallow checkout permits only a partial inventory,
labelled `shallow-observation-only`; no private file is read in that mode.
The public history hash identifies the exact observed inputs, not completeness.

## Reserve a new private-test family

An independent reviewer should inspect the actual question, mathematical
mechanism and source correspondence against the public families before signing
off. Keep tasks, answers, review notes and their reservation outside the
repository (preferred), or in an ignored `.astis` directory. Do not upload them
to GitHub Actions, website exports, agent prompts for development, or a public
issue. Never add them to `cores.json`. This is the reservation format, illustrated
with invented IDs and hashes, not a real task or an attestation:

```json
{
  "schema_version": 1,
  "split": "private-test",
  "families": [{
    "family": "example-private-family",
    "aliases": [],
    "derived_from_families": [],
    "source_exercise_ids": [],
    "numbered_sources": [],
    "tasks": [{
      "id": "example-private-task",
      "nl_prompt_sha256": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"
    }],
    "provenance": {
      "author": "example-author",
      "reviewer": "example-independent-reviewer",
      "review_sha256": "dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",
      "rights": "project-original",
      "uses_restricted_material": false,
      "original_independent_family_attested": true
    }
  }]
}
```

Record all known aliases, family derivations, exercise IDs and numbered source
coordinates where applicable (`pdf_sha256`, `chapter` and `number` strings).
A derivation from a public family is ineligible; if two private variants are
related, group them under one family. A task carries the natural-language
prompt digest, the exact qualified `lean_answer_declaration`, or both. The
digest is computed by `prompt_digest(assumptions, question)` from
`tools.sog_bench_split_guard`: it normalizes Unicode and whitespace, sorts the
assumptions, and preserves case. Compute it locally, without putting private
prompts in shell history. Record only an actual answer target as the Lean
declaration, not every reused prerequisite. Graph-only reservations are not
supported by this format. The hash of the private review record is a binding,
not proof of review or a rights grant.

```text
python tools/sog_bench_split_guard.py --public-tip PUBLIC_RELEASE_SHA --public-tip PUBLIC_PR_SHA --reservation PRIVATE_METADATA_PATH
```

Exit `0` means no known conflict within the declared inputs; `1` means a
collision or provenance-policy failure; `2` means the check did not produce a
decision. Output contains only aggregate counts, public history evidence and
conflict categories. The guard cannot discover undeclared public exposure,
recognize all paraphrases, match editions automatically, verify reviewer
identity, or certify model-training contamination or secrecy. There is no
released held-out split, automated score, or model result from this check.
