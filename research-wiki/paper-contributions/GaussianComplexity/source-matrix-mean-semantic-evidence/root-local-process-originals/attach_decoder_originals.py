"""Carry immutable anonymous reconstruction and export the fresh anti-anchored packet."""
from pathlib import Path

old = Path('.astis/huanjian-gc-source-row-independence-20261112/attach_decoder_originals.py').read_text()
code = old.replace('source-row-independence', 'source-matrix-mean')
code = code.replace('n_decode_9e31', 'n_decode_38df').replace('neutral_decode_9e31', 'neutral_decode_38df')
code = code.replace('f5946852ce343bfd40c2c44aaf93a282cbcc29f68bc2c11f175b4d75212718fb',
                    'c02e83f479f013440c6da7708d5a018a8dc38dba870cb7335932fe5656bd8383')
code = code.replace('608361f0c4c0832a2724c49b2febc2733e87050dca19b18746a1b6012b7a2a8c',
                    '34b56baf21f85e6b49de73db76ad1e95ee14c56bb5602ac1fc6c9fb89bb0b358')
code = code.replace('6dea1b9d1fc2f203c16642cffd76ff0df8a29813121e51f157554dab3abf500a',
                    'e1dcc94907868ac4f28f0a0959d80947404cb7596451ec1ae90fe593d83f67e9')
code = code.replace("run['actor']['agent_task_path']", "run['decoder_identity']")
code = code.replace("assert len(run['input_manifest']) == 1 and run['input_manifest'][0]['raw_input_sha256'] == sha(input_raw)",
                    "assert run['mathematical_evidentiary_input_count'] == 1 and run['sole_input']['raw_sha256'] == sha(input_raw)")
code = code.replace("run['canonical_packet']['sha256']", "run['sole_input']['packet_sha256_recomputed']")
code = code.replace("run['input_manifest'][0]['anonymous_statement_sha256']", "run['sole_input']['anonymous_statement_sha256_recomputed']")
code = code.replace("assert run['exposure_manifest']['source_identity_visible'] is False",
                    "assert run['inputs_and_exposure']['original_source_text_or_identity_read'] is False")
code = code.replace("assert run['exposure_manifest']['repository_protocol_or_AGENTS_read'] is False",
                    "assert run['inputs_and_exposure']['AGENTS_md_read'] is False\nassert not run['reconstruction']['abridged']\nassert run['output_contract']['reconstructed_theorem_text'] == text_raw.decode()")
code = code.replace('The exact full frozen reconstruction.md including seven-slot discussion is the canonical reconstruction. The run separately quotes an abridged main theorem in its output contract and binds the full reconstruction file by its exact byte hash.',
                    'The exact full frozen reconstruction.md is the canonical reconstruction. The run embeds that complete text without abridgment and binds its complete bytes. Final externally hashed run is carried without rewriting or an invented self-hash.')
generated = Path(__file__).resolve().parent / 'attach_decoder_originals.generated.py'
with generated.open('x') as out:
    out.write(code)
exec(compile(code, str(generated), 'exec'))
