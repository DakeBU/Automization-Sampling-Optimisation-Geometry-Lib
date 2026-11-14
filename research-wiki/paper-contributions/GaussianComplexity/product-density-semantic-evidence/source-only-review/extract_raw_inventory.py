"""Source-only inventory. Reads pinned HTML only; never reads Lean or reviews."""

from collections import Counter
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SOURCE = ROOT / ".astis/huanjian-resume-20261103/2610.20492v1.html"
EXPECTED = "6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915"
OUT = Path(__file__).resolve().parent


class Node:
    def __init__(self, tag="", attrs=(), line=0, parent=None):
        self.tag, self.attrs, self.line, self.parent = tag, dict(attrs), line, parent
        self.children = []

    def walk(self):
        yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child.walk()

    def text(self):
        if self.tag == "math":
            return "$" + self.attrs.get("alttext", "") + "$"
        return "".join(c.text() if isinstance(c, Node) else c for c in self.children)

    def anchor(self):
        cur = self
        while cur:
            if cur.attrs.get("id"):
                return cur.attrs["id"]
            cur = cur.parent
        return "document"

    def ancestors(self):
        cur = self
        while cur:
            yield cur
            cur = cur.parent


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.root = Node()
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.getpos()[0], self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in {"meta", "link", "img", "br", "hr", "input", "wbr", "source"}:
            self.stack.append(node)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                self.stack = self.stack[:i]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


S2_KEEP = {
    "S2.p1.1": "Standing Euclidean norm, identity, and Loewner-order conventions.",
    "S2.p2.1": "Actual orthogonal group and determinant-conditioned Haar laws.",
    "S2.SS0.SSS0.Px1.p1.1": "Typing/standing precision-class context only; algorithmic motivation is not a premise.",
    "S2.Ex1": "Precision class and spectral normalization for the actual Gaussian target.",
    "S2.SS0.SSS0.Px1.p1.2": "Actual target pi_A=N(0,A^{-1}); oracle clause is excluded as a subregion.",
    "S2.SS0.SSS0.Px3.p1.1": "TV convention, used in consumer Ex69/Ex72 only.",
    "S2.Ex2": "TV density formula, used in consumer Ex69/Ex72 only.",
    "S2.SS0.SSS0.Px3.p1.2": "Common dominating measure convention; bounded-test clause is upstream separation context only.",
}


def disposition(node):
    lineage = list(node.ancestors())
    ids = [a.attrs.get("id", "") for a in lineage]
    # Classify the closest paragraph/display, then its section. Subregion
    # exclusions prevent mixed paragraphs from inventing extra public premises.
    own = node.attrs.get("id", "")
    if own in {"S3.SS1.p1.m4", "S3.SS1.p1.m5", "S3.SS1.p1.m6", "S3.SS1.p1.m7"}:
        return "EXCLUDED", "Main-theorem query-budget specialization n=2T+1; not needed by Ex70/Ex71/Ex72."
    if own.startswith("S2.SS0.SSS0.Px1.p1.m") and own not in {
        "S2.SS0.SSS0.Px1.p1.m1", "S2.SS0.SSS0.Px1.p1.m2", "S2.SS0.SSS0.Px1.p1.m3",
        "S2.SS0.SSS0.Px1.p1.m4", "S2.SS0.SSS0.Px1.p1.m5", "S2.SS0.SSS0.Px1.p1.m7",
    }:
        return "EXCLUDED", "Potential/oracle part of the mixed target/oracle paragraph; no density dependency."
    if node.tag.startswith("h"):
        return "EXCLUDED", "Navigation/title only; mathematical content is covered by its paragraphs and displays."
    if "A2.SS2.SSS1" in ids:
        return "EXCLUDED", "Determinant-cancellation proof is not an ancestor of actual Ex70 or Ex71; upstream proof of the separately cited B.7 is outside this minimal packet."
    if "A2.SS2.SSS2" in ids and not any(a in {"A2.Thmtheorem7", "A2.E19"} for a in ids):
        return "EXCLUDED", "Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context."
    if "S2" in ids:
        for anchor in ids:
            if anchor in S2_KEEP:
                return "NODE", S2_KEEP[anchor]
        return "EXCLUDED", "Oracle/algorithm/query-complexity content has no role in Ex70 density or Ex71/Ex72 integration."
    if "S3.SS1" in ids:
        return "NODE", "Actual source family/prior/product-law construction; query-budget subregion is separately excluded."
    if "A2.SS2.SSS3" in ids:
        if node.text().strip() == "∎":
            return "EXCLUDED", "Proof-ending punctuation only."
        return "NODE", "Complete B.2.3 source step/definition/display or its explicit consumer citation."
    if any(a in {"A2.Thmtheorem5", "A2.E14"} for a in ids):
        return "NODE", "Separation destination context; not a prerequisite of Ex70."
    if any(a in {"A2.Thmtheorem7", "A2.E19"} for a in ids):
        return "NODE", "B.7 statement is a consumer-side input to Eq25 and Ex72, never an ancestor of Ex70."
    if "A2.SS2.p2.1" in ids:
        return "NODE", "Standing n/kappa/Haar conventions and actual p_O/p_b density definitions."
    return "EXCLUDED", "Section introduction/navigation only; target destination is recorded separately."


def main():
    raw = SOURCE.read_bytes()
    assert sha256(raw).hexdigest() == EXPECTED
    parser = Parser()
    parser.feed(raw.decode())
    scope = {"S2", "S3.SS1", "A2.SS2"}
    roots = [n for n in parser.root.walk() if n.attrs.get("id") in scope]
    assert len(roots) == 3
    records, counts, occurrence = [], Counter(), Counter()
    for root in roots:
        for node in root.walk():
            if node.tag not in {"p", "table", "math", "cite", "a", "h2", "h3", "h4", "h5", "h6"}:
                continue
            if node.tag == "a" and not node.attrs.get("href"):
                continue
            kind = ("paragraph" if node.tag == "p" else "display-group" if node.tag == "table"
                    else "formula-occurrence" if node.tag == "math" else "citation-occurrence"
                    if node.tag in {"cite", "a"} else "title")
            disposition_, reason = disposition(node)
            anchor = node.attrs.get("id")
            if not anchor:
                base = node.parent.anchor() if node.parent else "document"
                occurrence[(base, kind)] += 1
                anchor = f"{base}::{kind}-{occurrence[(base, kind)]}"
            record = {
                "id": anchor, "kind": kind, "line": node.line,
                "disposition": disposition_, "reason": reason,
                "text": " ".join(node.text().split()),
            }
            if node.attrs.get("href"):
                record["href"] = node.attrs["href"]
            records.append(record)
            counts[(kind, disposition_)] += 1
    payload = {
        "schema": "source-only-inventory-v1", "source_path": str(SOURCE.relative_to(ROOT)),
        "source_sha256": EXPECTED,
        "bounded_slice": ["entire S2", "entire S3.SS1", "entire A2.SS2 (B.2.1/B.2.2 derivations explicitly excluded item by item)"],
        "extraction_policy": "Every paragraph, display group, mathematical formula occurrence (including all inline definition occurrences), heading, and citation/link occurrence is classified. Display rows are losslessly retained as child math occurrences; inline definitions also receive a semantic registry in source-expectations.freeze.md.",
        "counts": {f"{kind}:{state}": count for (kind, state), count in sorted(counts.items())},
        "items": records,
    }
    (OUT / "raw-source-inventory.freeze.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Raw source bounded inventory", "", f"Source SHA256: `{EXPECTED}`.", "",
             "Generated solely from the pinned HTML; every item has NODE or EXCLUDED(reason).", ""]
    for r in records:
        if r["kind"] in {"paragraph", "display-group", "citation-occurrence"}:
            lines.extend([f"- {r['disposition']} `{r['id']}` (raw line {r['line']}): {r['reason']}", f"  Source: {r['text']}"])
    (OUT / "raw-source-inventory.freeze.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({"source_sha256": EXPECTED, "items": len(records), "counts": payload["counts"]}, indent=2))


if __name__ == "__main__":
    main()
