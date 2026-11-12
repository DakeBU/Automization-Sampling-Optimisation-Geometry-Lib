# Exercise 4.1 local reader and graph checkpoint

The Lean source and exact-interface test are unchanged from the independent
source review. The clean port on main base 90e7f58e6 passed the root Tests
and ASTIS gate (9664 jobs). The canonical site Lean-gate recorder passed
for proof commit 856361169 and source digest
a1191479a33d01366613665748703f0fb708d2534ea64b6cbd1e6c154ef4afdd.
The local source-bound graph projects the exact declaration as compiled;
its module-to-declaration relation is structural, the Chapter 4 link is
source correspondence, and the source review attaches separately.

Browser regression: one theorem covers three source obligations. The
reader now lists all three obligations and links to the owned theorem once.
A long first-order remainder display is split at its top-level equality
and inequality in the reader only; the reviewed mathematical record is
unchanged. The Chrome desktop/mobile smoke check passed for sogb-049:
same-origin rendered formulas fit, the exact Lean answer folds, copy and
download match source, and the prompt-only package excludes answer code.
The mobile math screenshot was inspected after the fix. The structural
graph check and [bounded compiler proof probe](proof-occurrences.md) are
separate from visual checks and add no graph QA.

No deployed site or full runtime pass is asserted here. The local v0.34
catalog has 48 mathematical cores, 74 math views, 10 graph tasks, and five
numbered exercises. This is an editorially checked public-dev catalog,
not a private test set or a model result.
