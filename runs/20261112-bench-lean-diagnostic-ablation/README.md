# Paired Lean diagnostic-text replay · public-dev

On 2026-11-12, the operator recorded two new second-turn generations from
the pinned Qwen2.5-0.5B-Instruct CPU model for `sogb-015`. Both used the
same proof prefix, recorded first response, failed check status, decoding
and runtime. The only message change was whether the archived diagnostic
text was included or replaced by a fixed withheld marker. The
[preselected plan](plan.json) was written before inference. There was
no new live tool call or provider API call.

| Second-turn condition | Input tokens | Output tokens |
| --- | ---: | ---: |
| Status only | 410 | 21 |
| Status and diagnostic text | 731 | 21 |

The generated token IDs and the unedited proof body are identical.
Both candidate files also match byte-for-byte the final submission in
[the original live archive](../20261110-bench-local-lean-first/README.md),
whose isolated outcome was `proof-rejected`. The
[comparison](comparison.json) reuses that one recorded native outcome; it
does not count two new Lean runs or two independent score observations.
A different candidate would remain unverified, even if its tokens or
content seemed equivalent.

From the repository root, audit the exact records without a model or Lean:

```bash
python tools/sog_bench_pilot_ablation.py replay --run runs/20261112-bench-lean-diagnostic-ablation
```

The raw candidate files are untrusted output data, not proof sources or
training examples. Do not execute them on the host or give this archive
to a model as benchmark context. No model weights are redistributed.
This is one operator-recorded public task, not authenticated model
provenance, autonomous tool use, calibration, or a general estimate of
feedback effectiveness.
