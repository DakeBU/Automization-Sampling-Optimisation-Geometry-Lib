The independently closed reader69 bundle has 335 original local files. One 167233478-byte complete named payload exceeds the Git hosting single-file limit. Its original local RAW file and CLOSED lease remain unchanged.

Git retains every other native file and this deterministic gzip representation. The manifest binds both compressed and original RAW bytes. This is an explicit transport representation, not a claim that the oversized original is a Git RAW object. No JSON content is reserialized or removed.

Run `materialize-outside-native-tree.py FRESH_OUTPUT_FILE` to recover the exact original outside the closed native directory, then use that RAW artifact for the manifest entry named in manifest.json. Original close receipts establish the original chronology; a new checkout/materialization does not replay timestamps or the original postclose event. Never overwrite or rewrite the original CLOSED bundle.
