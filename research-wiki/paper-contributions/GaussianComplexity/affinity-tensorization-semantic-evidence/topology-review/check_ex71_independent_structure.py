#!/usr/bin/env python3
"""Independent raw-unit, digest and adjacency checks; no Lean or audit input."""
import hashlib
import json
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "research-wiki/paper-contributions/GaussianComplexity/affinity-tensorization-semantic-evidence/source-only-review"
RAW = ROOT / ".astis/huanjian-resume-20261103/2610.20492v1.html"
OUT = Path(__file__).with_name("ex71-independent-structure-receipt-20261107.json")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(name):
    return json.loads((BASE / name).read_text())


class RawUnits(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.units = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        ancestors = [item[1] for item in self.stack]
        node_id = attrs.get("id")
        scoped = (
            "S2" in ancestors
            or "S3.SS1" in ancestors
            or "A2.Thmtheorem7" in ancestors
            or "A2.SS2.SSS3" in ancestors
            or node_id == "A2.SS2.p2.1"
        )
        if tag in {"p", "table"} and scoped:
            self.units.append({"anchor": node_id, "tag": tag, "line_start": self.getpos()[0]})
        if tag not in {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}:
            self.stack.append((tag, node_id))

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_startendtag(self, tag, attrs):
        pass


g = read("independent-sourcegraph-ex71-v1.json")
m = read("exact-seal-sourcegraph-map-ex71-v1.json")
c = read("source-coverage-ex71-v1.json")
raw_bytes = RAW.read_bytes()
raw_lines = raw_bytes.decode().splitlines(keepends=True)
parser = RawUnits()
parser.feed(raw_bytes.decode())
inventory = g["inventory"]
all_nodes = {n["id"] for n in inventory if n["disposition"] == "NODE"} | {n["id"] for n in m["added_nodes"]}
edges = g["use_site_edges"] + m["added_edges"]
incoming = defaultdict(set)
bad_endpoints = []
for e in edges:
    incoming[e["to"]].add(e["from"])
    if e["from"] not in all_nodes or e["to"] not in all_nodes:
        bad_endpoints.append([e["from"], e["to"]])


def closure(root):
    visited = set()
    work = [root]
    while work:
        node = work.pop()
        if node not in visited:
            visited.add(node)
            work.extend(incoming[node] - visited)
    return sorted(visited)


digest_records = []
for item in inventory + c["raw_unit_coverage"]:
    digest_records.append(item)
for e in edges:
    for key in ["consumer_use_site", "source_use_site"]:
        if key in e and "raw_line_slice_sha256" in e[key]:
            digest_records.append(e[key])
bad_raw_slices = []
for item in digest_records:
    actual = sha("".join(raw_lines[item["line_start"] - 1:item["line_end"]]).encode())
    if actual != item["raw_line_slice_sha256"]:
        bad_raw_slices.append({"anchor": item["anchor"], "actual": actual})

covered = {u["anchor"] for u in c["raw_unit_coverage"]}
direct = {u["anchor"] for u in parser.units}
root_receipts = {}
coverage_keys = {
    "ex71": "source_root_closure",
    "sealed.equality-output": "exact_RN_equality_root_closure",
    "sealed.conclusion": "full_sealed_conclusion_root_closure",
}
for root, coverage_key in coverage_keys.items():
    actual = closure(root)
    reported = m["root_closure_tables"][root]
    root_receipts[root] = {
        "count": len(actual),
        "closure": actual,
        "matches_map": actual == sorted(reported),
        "matches_coverage": actual == sorted(c[coverage_key]),
        "forbidden_downstream_ancestors": sorted(set(actual) & {"ex72", "eq25", "b7.statement", "ex69", "bridge.tv-overlap"}),
    }

indegree = Counter({n: 0 for n in all_nodes})
outgoing = defaultdict(set)
for e in edges:
    if e["to"] not in outgoing[e["from"]]:
        outgoing[e["from"]].add(e["to"])
        indegree[e["to"]] += 1
work = [n for n, d in indegree.items() if d == 0]
visited = []
while work:
    node = work.pop()
    visited.append(node)
    for target in outgoing[node]:
        indegree[target] -= 1
        if indegree[target] == 0:
            work.append(target)

receipt = {
    "artifact_kind": "independent-raw-structure-check-not-mathematical-verdict",
    "inputs": {name: sha((BASE / name).read_bytes()) for name in ["independent-sourcegraph-ex71-v1.json", "exact-seal-sourcegraph-map-ex71-v1.json", "source-coverage-ex71-v1.json", "exact-seal-source-review-manifest-ex71-v1.json"]},
    "raw_sha256": sha(raw_bytes),
    "inventory_counts": dict(Counter(n["disposition"] for n in inventory)),
    "added_node_count": len(m["added_nodes"]),
    "base_edge_count": len(g["use_site_edges"]),
    "added_edge_count": len(m["added_edges"]),
    "independently_enumerated_raw_unit_count": len(parser.units),
    "independently_enumerated_raw_units": parser.units,
    "missing_raw_unit_coverage": sorted(direct - covered),
    "extraneous_raw_unit_coverage": sorted(covered - direct),
    "raw_slice_checks": len(digest_records),
    "bad_raw_slices": bad_raw_slices,
    "bad_edge_endpoints": bad_endpoints,
    "all_node_edges_acyclic": len(visited) == len(all_nodes),
    "root_closures": root_receipts,
    "route_group_count": len(g["route_groups"]) + len(m["added_route_groups"]),
    "mathematical_scope": "Closure lists are union-of-routes reachability. OR/AND route meaning, guarded discharge and source coverage content require the independent written review.",
}
receipt["all_structural_checks_pass"] = (
    not bad_raw_slices and not bad_endpoints and direct == covered
    and len(visited) == len(all_nodes)
    and all(r["matches_map"] and r["matches_coverage"] and not r["forbidden_downstream_ancestors"] for r in root_receipts.values())
)
OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"output": str(OUT), "sha256": sha(OUT.read_bytes()), "all_structural_checks_pass": receipt["all_structural_checks_pass"], "raw_units": len(parser.units), "root_counts": {k: v["count"] for k, v in root_receipts.items()}, "missing_raw_units": receipt["missing_raw_unit_coverage"], "extraneous_raw_units": receipt["extraneous_raw_unit_coverage"]}, ensure_ascii=False))
