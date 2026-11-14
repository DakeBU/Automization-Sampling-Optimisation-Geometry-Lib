"""Check the independent actor's exact original verdict spelling, preserving v1."""
from pathlib import Path

code = (Path(__file__).resolve().parent / 'readback_preproof_reviews.py').read_text()
code = code.replace('NO_GENUINE_TYPE_BINDER_DEFINITION_OR_SOURCE_SCOPE_ISSUE_FOUND', 'NO_GENUINE_BINDER_DEFINITION_TYPE_OR_SOURCE_SCOPE_ISSUE_FOUND')
code = code.replace("'SG_original_verdict': audit['verdict'],", "'root_readback_v1_failure': 'Compared old packet verdict word order; failed before output/admission/proof. V2 checks actual immutable original string; no independent verdict is normalized or rewritten.',\n    'SG_original_verdict': audit['verdict'],")
generated = Path(__file__).resolve().parent / 'readback_preproof_reviews_v2.generated.py'
with generated.open('x') as out:
    out.write(code)
exec(compile(code, str(generated), 'exec'))
