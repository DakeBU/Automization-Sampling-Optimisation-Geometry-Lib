"""Correct the custody check for original-source versus exact portable-copy paths."""
from pathlib import Path

original = Path(__file__).resolve().parent / 'carry_original_verified.py'
code = original.read_text()
code = code.replace("assert source == destination and destination.is_relative_to(phase)",
                    "assert not source.is_absolute() and '..' not in source.parts\n    assert destination.is_relative_to(phase)\n    assert not source.is_symlink() and source.read_bytes() == destination.read_bytes()")
code = code.replace("'formalizer_API_pristine': False,\n    'verifier_rejected_prechecks'",
                    "'formalizer_API_pristine': False,\n    'root_custody_v1_rejected_before_writes': 'Assumed manifest original-source path equals portable-copy path; corrected to byte-compare each distinct original and destination. Original script, failed receipt/log and independent successful V remain unchanged. No normal API in either custody script.',\n    'verifier_rejected_prechecks'")
generated = Path(__file__).resolve().parent / 'carry_original_verified_v2.generated.py'
with generated.open('x') as out:
    out.write(code)
exec(compile(code, str(generated), 'exec'))
