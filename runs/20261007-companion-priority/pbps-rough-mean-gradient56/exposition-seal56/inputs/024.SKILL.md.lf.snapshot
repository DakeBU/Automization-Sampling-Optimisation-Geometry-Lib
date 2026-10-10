---
name: astis-semantic-roundtrip
description: Audit whether a compiled Lean declaration preserves its source theorem and propose source-reviewable minimal theorem repairs.
---

# ASTIS Semantic Round-Trip Skill

Use this skill for every source-facing Chewi, SampleWiki, or paper theorem after its exact Lean declaration compiles. Lean compilation proves the formal proposition; it does not prove that the proposition is the one the source intended.

## Truth boundary

Keep these claims separate:

1. **Lean truth:** the pinned declaration compiles without fake closure.
2. **Reconstruction evidence:** an independent decoder reconstructs the theorem from the Lean statement while source text, source identity, theorem number, prior audit, and repair proposals are hidden.
3. **Source fidelity:** an independent source reviewer compares the original and reconstruction slot by slot using a packet-bound review run.
4. **Repair status:** a proposed denoising repair remains an overlay until a separate exact-proposal repair review accepts it. It never overwrites the pinned source theorem automatically.

A proving/formalizing Worker must not act as its own blind decoder or source-facing reviewer.

## Required workflow

For new/changed declarations, also read `docs/theorem-publication-protocol.md`.
The bounded publication packet supplies a `publication_binding_sha256`; record
it on the canonical audit to bind current code, source, assumptions and authored
proof explanation. It is coordinator metadata, **never blind decoder input**.
Reuse an unchanged review; changed inputs invalidate it. The Harness and CI
enforce admission automatically but never invent a decoder/reviewer verdict.

1. Pin the source ID, exact anchor, verbatim or licensed ASTIS source restatement, and SHA-256.
2. Pin the Lean declaration, file, fully elaborated statement available to the decoder, statement SHA-256, and compiler evidence.
3. Create or update an audit in `research-wiki/semantic-roundtrip/registry.json` in `draft` state.
4. Record only the minimal definition context needed to interpret the Lean proposition. Each context item must be a plain non-empty string. The gate scans these strings for exact source text, source/audit/anchor identity, Lean file/declaration identity, and repair material; a detected leak blocks packet generation.
5. Generate the anonymous decoder-only input. The exported packet contains no audit ID, source identity, theorem number, source anchor, Lean file/declaration identity, prior audit, or repair proposal:

   ```bash
   python3 tools/astis_semantic_roundtrip.py decoder-packet \
     --audit-id ASTIS-RT-... \
     --output runs/semantic-roundtrip/ASTIS-RT-....decoder.json
   ```

6. Give that packet—not the registry, source text, or source-facing Lean card—to an independent decoder. Record `source_text_visible=false`, the canonical decoder-packet hash, exact input artifacts, decoder identity/run hash, and reconstructed-theorem hash.
7. Generate a fresh anti-anchored source review packet:

   ```bash
   python3 tools/astis_semantic_roundtrip.py reviewer-packet \
     --audit-id ASTIS-RT-... \
     --output runs/semantic-roundtrip/ASTIS-RT-....review.json
   ```

   Give it to a reviewer distinct from both formalizer and decoder. The packet contains source and reconstruction but omits all earlier semantic slots, deltas, verdicts, and repairs. Record both the exact reviewer-packet hash and reviewer-run hash.
8. Compare all seven semantic slots: objects, domains, quantifiers, assumptions, conclusion, scopes/senses, and constant dependencies. Text or embedding similarity is not evidence of equivalence.
9. Classify every delta and issue a fidelity verdict. Exact/equivalent verdicts require no blocking delta; source-facing acceptance requires an independent reviewer distinct from the formalizer and decoder.
10. When formalization exposes a possible missing condition, create a separate repair proposal with a reconstructed statement, justification, minimality evidence, and a rigorous reference or counterexample. Classify whether it is mathematically necessary, source implicit, uncertain, or a formalization-artifact risk.
11. Before marking a repair `source-reviewed` or `accepted`, generate its own exact-proposal review packet:

   ```bash
   python3 tools/astis_semantic_roundtrip.py repair-reviewer-packet \
     --audit-id ASTIS-RT-... \
     --repair-id ASTIS-REPAIR-... \
     --output runs/semantic-roundtrip/ASTIS-REPAIR-....review.json
   ```

   The repair reviewer may inspect the source, Lean statement, blind reconstruction, and exact repair proposal, but the packet hides earlier fidelity verdicts, semantic-delta classifications, theorem source-review decisions, and earlier repair-review decisions. Record the independent reviewer identity, review-run hash, reviewer-packet hash, and `proposal_sha256`. Any later change to the source-facing proposal payload invalidates that review.
12. A formalization-artifact risk cannot be accepted as a source repair. In `faithfulPaper` mode, never add an assumption merely to close the current proof route.
13. Run:

   ```bash
   python3 tools/astis_semantic_roundtrip.py check
   python3 tools/astis_semantic_roundtrip.py summary
   ```

The website build projects accepted evidence, pending mismatches, and repair proposals into the `Semantic fidelity & repair` view of the Underlying Lean Graph.

## Hard rejects

Reject an audit when any of the following occurs:

- the decoder saw the source theorem, source/source-anchor/audit/declaration identity, theorem number, prior semantic audit, or repair proposal;
- approved definition context contains an exact known source/audit/declaration/repair secret or an unscanned structured object;
- one of the seven semantic slots is absent or only asserted without evidence;
- the formalizer, decoder, and source-facing reviewers are not independent where required;
- a completed source review is not bound to the canonical reviewer packet and reviewer run;
- a green Lean build is used as evidence of source fidelity;
- an accepted repair lacks minimality evidence and a reference or counterexample;
- a reviewed/accepted repair lacks its own packet-bound independent repair review;
- a reviewed repair's proposal payload changed after review;
- a repair silently changes the canonical source statement;
- a source-facing theorem is marked assimilated before both Lean compilation and source review pass.
