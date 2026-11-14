from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

REPO = Path('/Users/zhouhuanjian/ASTIS-GC')
OUT = REPO / '.astis/semantic-neutral-20261112/ri_src_5ab9'
source_rel = '.astis/huanjian-resume-20261103/2610.20492v1.html'
instructions = [
    'AGENTS.md',
    'docs/contributor-codex-contract.md',
    'docs/theorem-publication-protocol.md',
    'docs/proof-digestion-protocol.md',
    'docs/evidence-routed-memory-protocol.md',
    '.agents/skills/astis-semantic-roundtrip/SKILL.md',
]

def digest(path):
    b = path.read_bytes()
    return {'path': str(path.relative_to(REPO)), 'utf8_bytes': len(b),
            'sha256': hashlib.sha256(b).hexdigest()}

source = (REPO / source_rel).read_bytes()
source_text = source.decode('utf-8')
locators = json.loads((OUT / 'source_locators.json').read_text(encoding='utf-8'))
assert locators['source_sha256'] == hashlib.sha256(source).hexdigest()
for item in locators['items']:
    a, z = item['utf8_byte_start_0'], item['utf8_byte_end_exclusive_0']
    ca, cz = item['unicode_char_start_0'], item['unicode_char_end_exclusive_0']
    raw = (OUT / item['raw_extract_file']).read_bytes()
    assert raw == source[a:z] == source_text[ca:cz].encode('utf-8')
    assert hashlib.sha256(raw).hexdigest() == item['raw_extract_sha256']
    assert source[:a].count(b'\n') + 1 == item['lf_line_start_1']
    assert source[:z-1].count(b'\n') + 1 == item['lf_line_end_inclusive_1']
premise = next(x for x in locators['items'] if x['id']=='S4.Thmtheorem4.p1.1')
assert '2q+1<d' in premise['readable_source_text']
assert 'independent' in premise['readable_source_text']

exposure = {
    'reviewer_id': '/root/row_indep_fresh_source_5ab9',
    'phase': 'raw-source-only, before sealed-types comparison',
    'scope_input': {
        'kind': 'explicit parent assignment',
        'content_summary': 'Pinned raw-source hash, intended actual coordinate-row joint-independence subclaim, actual C.2 truncated-matrix measurability/independence consumer, exact formulas and scope boundaries. Assignment supplied mathematical framing before source reading; reviewer is source-independent from implementation, not blind to task framing.',
        'original_message_available_in_agent_transcript': True,
    },
    'required_instruction_inputs': [digest(REPO / p) for p in instructions],
    'raw_source_input': digest(REPO / source_rel),
    'source_read_method': [
        'Direct fixed-path source read and SHA-256 check.',
        'Narrow regex probes on pinned source for assigned IDs, gamma/independence, cutoff and angle grid.',
        'HTMLParser ingestion of pinned source to recover exact raw spans; readable excerpts displayed only for selected source elements.',
        'No source retrieval, publication tool, Lean tool, graph or registry command was run.',
    ],
    'incidental_raw_source_exposure': [
        'One bounded rg scan displayed raw snippets outside the eventual review boundary: other q/n source contexts; the preceding conversion to independent standard Gaussians; C.2 expectation, norm, tail/bias, variance, concentration and final-bound snippets; and an angle-grid recall in C.3. These were raw-source excerpts only and supply no review/coverage/acceptance claim.',
        'The complete Lemma 4.4 statement was read to separate standing premises from its later tau condition/main conclusion.',
        'Equation S4.E11 also exposes lambda_i and Lambda; A3.SS2.p1 also exposes the B row construction. Both remain excluded context.',
        'Required AGENTS.md contains unrelated process handoff context. It was read solely as explicitly required instruction input.',
    ],
    'probe_and_transcription_notes': [
        'Literal filename ending .html951991B did not exist. No contents were returned. Correct fixed .html filename matched the exact assigned hash and 951991-byte count.',
        'An initial generated readable transcription unescaped < inside math before stripping tags, thereby dropping a portion of the standing premise. Raw excerpts were unaffected. Extraction code was corrected with protected math placeholders and all source-derived outputs were regenerated before this freeze. The strict inequality and Gaussian-column premise were reread in the corrected output.',
        'Initial batched instruction display was truncated by the output budget. AGENTS.md, contributor contract, theorem-publication protocol, and proof-digestion protocol were reread in complete bounded outputs; evidence-routed-memory and semantic-roundtrip skill were already complete in the first output.',
    ],
    'not_exposed_at_freeze': {
        'sealed_lean_types_or_signatures': True,
        'implementation_lean_or_proof_code': True,
        'current_lessons_or_publication_binding': True,
        'existing_source_graph_or_topology_judgments': True,
        'old_source_audits_or_fidelity_verdicts': True,
        'blind_decoder_input_or_reconstruction': True,
        'compiler_receipts_or_build_output': True,
    },
    'mutations': {
        'allowed_output_directory': str(OUT.relative_to(REPO)),
        'only_private_output_files_created': True,
        'shared_registry_graph_ledger_control_plane_mutated': False,
        'git_mutated_or_inspected': False,
        'goal_created_or_updated': False,
        'background_astis_or_proof_search': False,
        'permission_or_publication_status_granted': False,
    },
    'next_phase': 'Stop; await exact separately supplied sealed types. Later code-only and anti-anchored packet comparisons have not begun.',
}
(OUT / 'input_exposure_manifest.json').write_text(json.dumps(exposure, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
artifact_names = ['source_reading_freeze.md', 'source_locators.json', 'input_exposure_manifest.json',
                  'extract_raw_source.py', 'seal_raw_freeze.py'] + [i['raw_extract_file'] for i in locators['items']]
manifest = {
    'reviewer_id': '/root/row_indep_fresh_source_5ab9',
    'phase': 'RAW_SOURCE_READING_FROZEN',
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'source_input': digest(REPO / source_rel),
    'artifact_hashes': [digest(OUT / p) for p in artifact_names],
    'verification': 'Every raw excerpt exactly matches both its original UTF-8 byte range and Unicode-character range; SHA-256 and LF line endpoints match; corrected standing-premise transcription retains 2q+1<d and column independence.',
    'scope_notice': 'No type/code/source-fidelity verdict or proof/topology/publication status is granted by this raw-source freeze.',
}
(OUT / 'freeze_bundle_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
for p in ['source_reading_freeze.md','source_locators.json','input_exposure_manifest.json','freeze_bundle_manifest.json']:
    print(json.dumps(digest(OUT / p), ensure_ascii=False))
