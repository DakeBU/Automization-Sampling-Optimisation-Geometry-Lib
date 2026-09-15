from pathlib import Path

path = Path("website/scripts/samplewiki_reader_contract.py")
text = path.read_text(encoding="utf-8")
replacements = {
    r"its \(2^{n_p}\) grid": r"its \(2^{{n_p}}\) grid",
    r"generic \(\Theta(2^{n_p})\)": r"generic \(\Theta(2^{{n_p}})\)",
}
for old, new in replacements.items():
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected one cross-library TeX occurrence, found {count}: {old}")
    text = text.replace(old, new, 1)
path.write_text(text, encoding="utf-8")
