from pathlib import Path
import hashlib, json

W = Path(__file__).parent
sha = lambda b: hashlib.sha256(b).hexdigest()
pi = Path('.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/PiL2.lean')
lp = Path('.lake/packages/mathlib/Mathlib/Analysis/Normed/Lp/PiLp.lean')

def item(path, start, end, kind, context=()):
    raw = path.read_bytes()
    text = raw.decode('utf-8')
    a = text.index(start)
    b = text.index(end, a)
    block = text[a:b].rstrip('\n') + '\n'
    assert 'theorem ' not in block or kind == 'characterization-statement-only'
    return {'file': str(path), 'wholefile_sha256': sha(raw),
            'kind': kind, 'context': list(context),
            'start_line_1based': text[:a].count('\n') + 1,
            'literal': block, 'literal_sha256': sha(block.encode())}

global_context = [
    'variable {ι ι\' 𝕜 : Type*} [RCLike 𝕜]',
    'variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace 𝕜 E]',
    'local notation "⟪" x ", " y "⟫" => inner 𝕜 x y',
]
for context in global_context:
    assert context in pi.read_text()
finite = 'variable [FiniteDimensional 𝕜 E]'
assert finite in pi.read_text()
entries = [
    item(pi, 'abbrev EuclideanSpace (𝕜 : Type*)', '\nsection Notation', 'literal-definition'),
    item(lp, 'abbrev PiLp (p : ℝ≥0∞)', '\n/-The following', 'literal-definition'),
    item(lp, 'instance (p : ℝ≥0∞) {ι : Type*} (α : ι → Type*) : CoeFun', '\ninstance (p : ℝ≥0∞)', 'literal-definition'),
    item(pi, 'theorem inner_eq_star_dotProduct (x y : EuclideanSpace 𝕜 ι)', ' := rfl', 'characterization-statement-only', global_context + ['variable [Fintype ι]', 'namespace EuclideanSpace']),
    item(pi, 'irreducible_def stdOrthonormalBasis :', '\n/-- An orthonormal basis of `ℝ`', 'literal-definition', global_context + [finite, 'variable (𝕜 E)']),
]
out = {'scope': 'Only requested exact Euclidean/PiLp definitions, coordinate coercion definition, inner-product characterization statement without proof, and complete stdOrthonormalBasis definition including its own definition body. No standalone theorem proof, target implementation or review result.', 'definitions': entries}
data = (json.dumps(out, ensure_ascii=False, indent=2) + '\n').encode()
p = W/'minimal-requested-orthonormal-normalization-context.json'
with p.open('xb') as f:
    f.write(data)
p.chmod(0o444)
print(json.dumps({'path': str(p), 'bytes': len(data), 'sha256': sha(data), 'entries': len(entries)}))
