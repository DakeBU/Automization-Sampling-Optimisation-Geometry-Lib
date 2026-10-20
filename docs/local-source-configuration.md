# Local source configuration

Public code carries no machine-specific source directory. Optional source-index
commands read `ASTIS_SALD_SOURCE_ROOT`, `ASTIS_EXTERNAL_REPOS_ROOT` and
`ASTIS_EXTERNAL_PAPERS_ROOT` from the environment. Their defaults are, respectively,
`local_sources/sald` under the checkout and `external_repos` / `external_papers`
beside it. Set these variables in your local shell before indexing a source.
Do not commit private source contents or personal absolute paths.

Local source availability, compiled Lean, independent source review, and published
reader delivery are separate checks. Removing an unused planned case does not
prove a theorem or erase Git history. Historical sealed evidence is preserved.
