# Checksum-pinned hosted Lean setup

This Linux x86-64 setup is used by the formalization gate, Bench trusted
references, and Bench native isolation trials. It does not replace a
developer's local Elan installation.

The previous setup depended on the current Elan installer release before
it could fetch the pinned compiler or restore the Lake cache. Both downloads
returned HTTP 504 on separate attempts. The local action instead fetches the
[official Lean 4.33.0 distribution](https://github.com/leanprover/lean4/releases/expanded_assets/v4.33.0)
directly. It requires the existing `lean-toolchain` pin, checks the published
archive SHA-256 before extraction, and checks the executable's release commit
and sysroot before publishing its bin directory. Two official HTTPS routes are
allowed on transport failure; unexpected bytes or a changed pin fail closed.

It retains the Lake cache keys tied to toolchain and manifest and still runs
`lake exe cache get`. It does not replace or skip a proof build, a trusted
reference, a publication audit, or any native isolation fixture. The compiler
root is readable to the isolated fixture's distinct UID and the existing
verifier still mounts it read-only.

Run the offline boundary tests with:

```bash
python3 -m unittest discover -s .github/actions/setup-pinned-lean -p 'test_*.py'
```

The unit tests use controlled command fixtures. Actual install and downstream
Linux build acceptance come from the CI job, not those fixtures.
