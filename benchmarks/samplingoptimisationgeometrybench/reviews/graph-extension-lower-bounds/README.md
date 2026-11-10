# Fixed-step and horizon-dependent quadratic proof slice

[Frozen input](input.json) · [Independent first answer](blind-answer.json) ·
[Independent structural review](source-review.json)

`sogb-g010` is a provisional L2 graph task. It shares the public-dev family
of `sogb-046`, a selected fixed-step distance component of
[Chewi, *Lectures on Optimization*, Exercises 3.2–3.3](https://arxiv.org/html/2605.07006v1#S3).
It does not add a mathematical core, complete a numbered exercise, or establish
a bound for all algorithms in an oracle model.

The [selected nodes](../../compiled_lower_bounds_graph_tasks.json) and
[compiler snapshot](../../compiled-lower-bounds-graph.json) record six
declarations and five direct occurrences. The horizon-dependent value-gap
witness calls the fixed-step distance witness. The latter uses the exact
eigenmode proof and the scalar minimax conclusion of `optimal_gradient_step`.
The one-step endpoint estimate is used by the other conclusion of
`optimal_gradient_step`. This explains why the whole compiled proof body
exhibits a path to the endpoint estimate even though the distance witness
projects the scalar minimax conclusion. The eigenmode branch follows the exact
iterate lemma and has no such path in this slice. A whole-body graph is not a
certificate of indispensable assumptions or of full-closure independence.

The same question can be run with the supplied snapshot or with a bounded
search tool. See [the lookup protocol](../../EVALUATION.md#graph-lookup-without-the-snapshot).
The solver-visible prompt and tool observations exclude the gold, while the
operator retains the first answer and exact replay. The controlled lookup and
scoring checks are software evidence, not a model score or measured difficulty.
