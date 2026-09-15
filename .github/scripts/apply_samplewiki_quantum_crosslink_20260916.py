from pathlib import Path

path = Path("website/scripts/samplewiki_reader_contract.py")
text = path.read_text(encoding="utf-8")
anchor = '''  </header>
  <section><div class="sw-reader-step">Choose a mathematical regime</div><div class="sw-setting-book-list">{''.join(cards)}</div></section>
  {focus}
</article>
"""


def progress_main('''
replacement = '''  </header>
  <section class="sw-overview-focus" id="cross-library-state-preparation">
    <div class="sw-reader-step">Cross-library worked problem · sampling structure meets quantum state preparation</div>
    <h2>Smooth auxiliary states for Schrödingerisation of PDEs</h2>
    <p>Jin–Liu–Ma’s Schrödingerisation construction for PDEs with physical boundary or interface conditions introduces a smooth auxiliary \(p\)-register initial state. If its \(2^{n_p}\) grid amplitudes are treated as unrelated data, generic loading is exponential in the register width. QuantumComputinglib/ASPBE instead exploits the exact Hermite–Bernstein/tensor-train representation and proves a constructive circuit bound</p>
    <div class="formula sw-casebook-formula">\\[G\\le 48n_p(2k+6)^3,\\qquad q=\\lceil\\log_2(2k+6)\\rceil.\\]</div>
    <p>Thus, for fixed smoothness order \(k\), the gate count is <strong>linear in \(n_p\)</strong>, rather than the generic \(\Theta(2^{n_p})\) amplitude-loading dependence. This is a SampleWiki-style lesson beyond sampling itself: the decisive question is often whether analytical structure exposes a bounded-memory representation before one accepts a black-box oracle or dense table.</p>
    <p class="sw-primary-source"><a href="https://arxiv.org/abs/2403.19123v3">Jin–Liu–Ma: source PDE / Schrödingerisation construction</a> · <a href="https://arxiv.org/abs/2005.04351">Holmes–Matsuura: prior smooth-function-to-MPS state-preparation route</a></p>
    <p><a class="button" href="https://dakebu.github.io/Quantum-Computing-Block-Encoding/example-cases/hermite-smooth-state-preparation/index.html">Open the Lean-verified QuantumComputinglib construction and proof →</a></p>
    <p class="sw-provenance-code">Cross-library pointer only: Samplinglib does not claim this quantum theorem as a local Lean result, and the general function-to-MPS idea is prior art.</p>
  </section>
  <section><div class="sw-reader-step">Choose a mathematical regime</div><div class="sw-setting-book-list">{''.join(cards)}</div></section>
  {focus}
</article>
"""


def progress_main('''
if 'id="cross-library-state-preparation"' not in text:
    if text.count(anchor) != 1:
        raise SystemExit("SampleWiki overview anchor changed")
    text = text.replace(anchor, replacement, 1)
path.write_text(text, encoding="utf-8")
