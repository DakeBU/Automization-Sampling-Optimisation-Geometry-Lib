"""Independent raw-source/inventory check; does not inspect implementation Lean."""
from collections import Counter
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import sys


class Node:
    def __init__(self, tag, attrs, line):
        self.tag, self.attrs, self.line = tag, dict(attrs), line
        self.children = []

    def descendants(self):
        for child in self.children:
            if isinstance(child, Node):
                yield child
                yield from child.descendants()

    def text(self):
        if self.tag == "math":
            return "$" + self.attrs.get("alttext", "") + "$"
        return "".join(c.text() if isinstance(c, Node) else c for c in self.children)


class RawParser(HTMLParser):
    void = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self):
        super().__init__()
        self.root = Node("ROOT", [], 0)
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.getpos()[0])
        self.stack[-1].children.append(node)
        if tag not in self.void:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.stack[-1].children.append(Node(tag, attrs, self.getpos()[0]))

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def main():
    version = sys.argv[1] if len(sys.argv) > 1 else "v1"
    if version not in {"v1", "v2"}:
        raise ValueError("Expected v1 or v2")
    base = Path("research-wiki/paper-contributions/GaussianComplexity")
    source_path = Path(".astis/huanjian-resume-20261103/2610.20492v1.html")
    inventory_name = "raw-source-inventory.freeze.json" if version == "v1" else "raw-source-inventory.v2.json"
    graph_name = "source-proof-graph.freeze.json" if version == "v1" else "source-proof-graph.v2.json"
    inventory_path = base / "product-density-semantic-evidence/source-only-review" / inventory_name
    graph_path = base / "product-density-semantic-evidence/source-only-review" / graph_name
    seal_path = base / "product-density-statement-seal.json"
    paths = [source_path, inventory_path, graph_path, seal_path]
    digests = {str(p): sha256(p.read_bytes()).hexdigest() for p in paths}
    parser = RawParser()
    parser.feed(source_path.read_text())
    raw = {n.attrs["id"]: n for n in parser.root.descendants() if "id" in n.attrs}
    inventory = json.loads(inventory_path.read_text())
    graph = json.loads(graph_path.read_text())
    items = inventory["items"]
    item_ids = {i["id"] for i in items}
    raw_missing = []
    raw_links = []
    for scope in ["S2", "S3.SS1", "A2.SS2"]:
        for node in raw[scope].descendants():
            node_id = node.attrs.get("id")
            if node.tag == "a" and "ltx_ref" in node.attrs.get("class", "").split():
                raw_links.append((node.attrs.get("href"), " ".join(node.text().split())))
            if not node_id or node.tag not in ["p", "table", "math"]:
                continue
            if node.tag == "p" and any(c.tag == "p" for c in node.descendants()):
                continue
            if node.tag == "table" and not {"ltx_equation", "ltx_equationgroup"}.intersection(node.attrs.get("class", "").split()):
                continue
            if node_id not in item_ids:
                raw_missing.append({"scope": scope, "tag": node.tag, "id": node_id, "line": node.line})
    formula_mismatches = []
    line_mismatches = []
    for item in items:
        if item["id"] not in raw:
            continue
        node = raw[item["id"]]
        if node.line != item["line"]:
            line_mismatches.append(item["id"])
        if item["kind"] == "formula-occurrence" and item["text"] != node.text():
            formula_mismatches.append(item["id"])
    inventory_links = [(i.get("href"), i["text"]) for i in items if i["kind"] == "citation-occurrence"]
    nodes = {n["id"] for n in graph["nodes"]}
    incidence_ancestors = {graph["root"]}
    while True:
        previous = set(incidence_ancestors)
        for edge in graph["edges"]:
            if edge["to"] in incidence_ancestors:
                incidence_ancestors.update(edge["from"])
        if previous == incidence_ancestors:
            break
    ancestors = {graph["root"]}
    while True:
        previous = set(ancestors)
        for edge in graph["edges"]:
            if edge["to"] in ancestors:
                ancestors.update(edge["from"])
                if edge.get("omitted_bridge"):
                    ancestors.add(edge["omitted_bridge"])
                ancestors.update(edge.get("omitted_bridges", []))
        if previous == ancestors:
            break
    result = {
        "reviewed_version": version,
        "inputs_sha256": digests,
        "implementation_lean_read": False,
        "extractor_private_rationale_read": False,
        "inventory_item_count": len(items),
        "disposition_counts": dict(Counter(i["kind"] + ":" + i["disposition"] for i in items)),
        "duplicate_item_ids": [k for k, v in Counter(i["id"] for i in items).items() if v > 1],
        "missing_raw_leaf_paragraph_display_or_math_ids": raw_missing,
        "raw_line_mismatches": line_mismatches,
        "raw_formula_alttext_mismatches": formula_mismatches,
        "raw_citation_link_count": len(raw_links),
        "citation_multiset_missing_from_inventory": list((Counter(raw_links) - Counter(inventory_links)).elements()),
        "citation_multiset_extra_in_inventory": list((Counter(inventory_links) - Counter(raw_links)).elements()),
        "unclassified_or_unreasoned_items": [i["id"] for i in items if i["disposition"] not in ["NODE", "EXCLUDED"] or not i.get("reason")],
        "graph_unknown_edge_endpoints": sorted({x for e in graph["edges"] for x in [*e["from"], e["to"], e.get("omitted_bridge"), *e.get("omitted_bridges", [])] if x is not None} - nodes),
        "graph_node_count": len(graph["nodes"]),
        "graph_edge_count": len(graph["edges"]),
        "incidence_only_root_ancestors": sorted(incidence_ancestors - {graph["root"]}),
        "listed_boundary_missing_incidence_path": sorted(set(graph["root_ancestor_boundary"]) - incidence_ancestors),
        "incidence_ancestor_missing_from_listed_boundary": sorted(incidence_ancestors - {graph["root"]} - set(graph["root_ancestor_boundary"])),
        "ex70_root_ancestors_including_typed_gaps": sorted(ancestors - {graph["root"]}),
        "listed_root_boundary_without_dependency_path": sorted(set(graph["root_ancestor_boundary"]) - ancestors),
        "scope_warning": "This checks source inventory and graph shape only. The separate independent mathematical review supplies the verdict."
    }
    output = base / "product-density-semantic-evidence/topology-review" / ("independent-mechanical-check." + version + ".json")
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
