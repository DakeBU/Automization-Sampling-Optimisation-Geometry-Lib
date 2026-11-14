"""Use the actual independent payload metadata key, keeping v1 and its failed check."""
from pathlib import Path

original = Path(__file__).resolve().parent / 'carry_original_verified.py'
code = original.read_text()
assert "assert payload['held_metadata_HEAD'] == head" in code
code = code.replace("assert payload['held_metadata_HEAD'] == head", "assert payload['verification_metadata_HEAD'] == head")
code = code.replace("'normal_verifier_failures': [],", "'normal_verifier_failures': [],\n    'root_custody_v1_failure_before_writes': 'Assumed R7 payload held_metadata_HEAD key; actual R8 original uses verification_metadata_HEAD. Corrected only the root check after actual ledger readback confirmed one VERIFIED and no custody writes. Original payload and sole normal API unchanged.',")
generated = Path(__file__).resolve().parent / 'carry_original_verified_v2.generated.py'
with generated.open('x') as out:
    out.write(code)
exec(compile(code, str(generated), 'exec'))
