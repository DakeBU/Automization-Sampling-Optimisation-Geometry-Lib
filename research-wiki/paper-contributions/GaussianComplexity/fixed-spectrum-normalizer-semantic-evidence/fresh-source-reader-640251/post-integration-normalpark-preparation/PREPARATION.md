# Post-integration normalpark preparation — no execution authorization

This is a frozen candidate helper, not permission to release STAB. No API, build, browser, network or model call was executed while preparing it. No new source verdict was made. The observed current baseline is reference metadata only, not an accepted future core or reader receipt.

The actual normal API permits `STABILIZING -> VERIFIED`. It still requires the VERIFIED actor to equal evidence.verifier_id and differ from the proof owner. The original source verifier must personally execute the future task: `/root/norm_fresh_source_640251`. Root may authorize but may not run as that actor. A Python actor field is an audit guard, not authentication of the human/agent session.

The helper requires a **new** root authorization of kind `ASTIS-normalpark-STABILIZING-to-VERIFIED-v1`, `authorization_state=authorized`, a raw64hex authorization hash supplied on the command line, a post-preparation issuance time, exact helper hash, full future immutable core, exact before-ledger hash and explicit owned output roots. The old source-V authorization and the included template cannot be used. The full sourceDigest must be supplied by future accepted evidence; the helper does not invent its algorithm from the reported92a908 prefix.

Before any API call it requires:

- exact future HEAD and a tracked worktree matching that core except the explicitly guarded advance ledger;
- unchanged producer/Test/own lesson/publication hashes and original bindingb2f41e36..., unchanged accepted canonical audit8fa833..., unchanged normal API6281ff33...;
- the original PROVED_LOCAL->VERIFIED append unique and byte-exact630b6125..., no prior STABILIZING->VERIFIED park for this advance, own uniquely occupied STAB and exact integration owner;
- independently accepted reader, eligible normalpark,46 actual original-image reviews with nonempty findings and hash-bound raw images, and9 actual completed passing checks on the future exact core, joined by raw hashes;
- all283 foreign replayed states,442 foreign frontier hashes and discovery ledger equal the original source-V preservation baseline; all443 current raw frontier JSONs, current README/model/config files and all old owned frozen evidence are snapshotted for before/after preservation.

Only public artifact paths under research-wiki/ or runs/ are accepted for the future integration artifacts. Other actors' .astis artifacts and ATLAS are not opened. Hashing source/model/config files is read-only. The normalized receipt contract is in `future-input-contract.json`; its examples are not acceptance assertions. If raw receipt formats differ, obtain a faithful, hash-bound public export/projection of the actual independent findings. Do not fabricate a decision to satisfy a field.

The future event deep-copies **all original V evidence**. In particular verifier_id, verified_commit813268bc..., gate, source_audit, fake_closure_scan, lean_declarations and publication_declarations retain their original values exactly. Future core/reader/eligibility/46image/9check references are added only under `post_integration_normalpark`. The future integration core does not overwrite the mathematical source's original verified_commit. No canonical audit is copied or changed and no sourceV is repeated.

The only shared mutation is one normal `astis_advance.transition_advance(..., 'VERIFIED', worker_id=original_source_verifier, ...)` append from STABILIZING. API child execution is synchronous. A persistent one-shot marker is written before the call; success is recorded immediately on return. A real completed subprocess command/time/log/returncode receipt is saved. Before/after ledgers are preserved losslessly, exactly one append and the unchanged whole old prefix are checked, foreign states/frontiers/discovery/README/models/frozen files are checked, proof owner remains unchanged, and STAB must become empty. The helper never edits even its own frontier; root may project own frontier metadata only after the completed receipt.

No-API preflight, only after separate future authorization and only by the real independent actor:

    python3 <normalpark_helper.py> --actor /root/norm_fresh_source_640251 --authorization <PUBLIC_NEW_AUTHORIZATION> --authorization-sha256 <EXACT64HEX>

Actual one-time normalpark, only when separately authorized in the conversation:

    python3 <normalpark_helper.py> --actor /root/norm_fresh_source_640251 --authorization <PUBLIC_NEW_AUTHORIZATION> --authorization-sha256 <EXACT64HEX> --execute

After an already successful API, packaging recovery uses the existing16hex authorization prefix and never calls the API:

    python3 <normalpark_helper.py> --actor /root/norm_fresh_source_640251 --package-only <AUTH_SHA_FIRST16>

Do not rerun --execute after any attempted call or success, even if later packaging fails. Preserve original failure/logs and repair only owned packaging with the existing append. If actual subprocess completion evidence is unavailable, report that exact limitation rather than inventing exit0. The strict helper refuses further API attempts.

Future owned execution outputs are under the two explicit `post-integration-normalpark-execution` roots in the authorization template. This preparation directory stays immutable. No STAB release, integration acceptance,9-check PASS or46-image acceptance is claimed now. The old automatic v5 success and current HOLD cannot satisfy this helper.
