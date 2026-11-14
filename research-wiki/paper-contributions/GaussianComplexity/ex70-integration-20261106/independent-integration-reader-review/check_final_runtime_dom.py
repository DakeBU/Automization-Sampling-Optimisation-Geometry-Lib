"""Check already-run root/build receipts and final static DOM; no UI claims."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urljoin, urlsplit

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
SITE = ROOT / "_site"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "website/scripts"))
import astis_site
import inline_lean

CORE = "e566930dccfa74a50fd86b743a3b8eddda21798b"
DIGEST = "5a2978a955ea15d1c1de0cec1c4d201b9d005040ae8018be6d8068b4de04583d"
TARGET = "AutoSamplingTheory.ExampleCases.GaussianComplexity.ProductDensity.actual_product_density"
MODULE = "AutoSamplingTheory.ExampleCases.GaussianComplexity.ProductDensity"
PRODUCTION = "AutoSamplingTheory/ExampleCases/GaussianComplexity/ProductDensity.lean"
INTEGRATION = "research-wiki/paper-contributions/GaussianComplexity/ex70-integration-20261106/"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def raw(rel: str) -> bytes:
    return (ROOT / rel).read_bytes()


def read(rel: str) -> object:
    return json.loads(raw(rel))


def check_receipt(rel: str, expected_log: str) -> dict:
    receipt = read(rel)
    log = Path(receipt["log"]).read_bytes()
    assert sha(log) == expected_log == receipt["log_sha256"]
    assert receipt["exit_code"] == 0 and receipt["head_before"] == receipt["head_after"] == CORE
    return {"receipt": rel, "receipt_raw_sha256": sha(raw(rel)), "actual_head": CORE,
            "command": receipt["command"], "started_utc": receipt["started_utc"],
            "elapsed_seconds": receipt["elapsed_seconds"], "log": receipt["log"],
            "raw_log_sha256": sha(log), "raw_log_bytes": len(log), "exit_code": 0}


def soup(rel: str) -> BeautifulSoup:
    return BeautifulSoup((SITE / rel).read_text(), "html.parser")


def main() -> None:
    assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() == CORE
    root = check_receipt(".astis/huanjian-resume-20261103/20261106T150954568404Z-ex70-canonical-root-lean-gate.receipt.json",
                         "7af0a68340c7990ef991f8d2327c399823524336e07161967217e2fb86e5c6cd")
    build = check_receipt(".astis/huanjian-resume-20261103/20261106T151235864382Z-ex70-final-root-bound-site-build.receipt.json",
                          "dc809178a6a4158802a8bc6f2c5ec837be97811da798b941b55b08b01ece9c5a")
    log = Path(root["log"]).read_text()
    assert "Build completed successfully (9642 jobs)." in log
    assert "ATLAS memory check passed:" in log and "ASTIS check passed" in log
    assert "lake build Tests" in log and "Recorded current Lean gate evidence" in log
    assert "Tests.GaussianComplexityProductDensity" in log
    assert re.search(r"actual_product_density' depends on axioms: \[propext,\s*Classical.choice,\s*Quot.sound\]", log)
    gate = read(".astis/site-lean-gate.json")
    metadata = json.loads((SITE / "data/build-metadata.json").read_text())
    assert gate["passed"] and gate["commit"] == CORE and gate["source_digest"] == DIGEST
    assert astis_site.source_digest() == DIGEST
    assert raw(".astis/site-lean-gate.json") == raw(INTEGRATION + "actual-root-gate-at-core-commit.json")
    assert metadata["git"]["commit"] == CORE and metadata["source_digest"] == DIGEST
    assert metadata["gate"]["passed"] and metadata["gate"]["current"]
    assert metadata["gate"]["commit"] == CORE and metadata["gate"]["source_digest"] == DIGEST
    assert not metadata["git"]["public_source_links"] and not metadata["git"]["commit_published"]
    rows = json.loads((SITE / "data/declaration-exposition.json").read_text())
    row = next(row for row in rows if row["declaration"] == TARGET)
    assert row["lean_status"] == "Compiled" and row["exposition"] == "authored"
    declaration = inline_lean.declarations()[TARGET]
    exact = inline_lean.display_source(declaration.source_text)
    signature, _ = inline_lean.split_statement(exact)
    pages = []
    for route in [row["page"], "proofs/source-huanjian-product-density.html"]:
        dom = soup(route)
        articles = dom.select('article[data-authored-declaration="' + TARGET + '"]')
        assert len(articles) == 1
        article = articles[0]
        assert not article.select("details[open]")
        assert len(article.select("details.reader-proof-disclosure")) == 5
        statement = article.select_one('details.inline-lean-statement[data-inline-lean="' + TARGET + '"]')
        proof = article.select_one('details.inline-lean-proof[data-inline-lean="' + TARGET + '"]')
        assert statement.select_one("code.language-lean").get_text() == signature
        assert proof.select_one("code.language-lean").get_text() == exact
        assert len(article.select(".reader-first-pass details.inline-lean-statement")) == 1
        assert len(article.select(".lean-verification details.inline-lean-proof")) >= 1
        module = next(a for a in proof.find_all("a") if a.get_text() == "Exact module and namespace context")
        module_url = urljoin("https://own-site.invalid/" + route, module["href"])
        assert urlsplit(module_url).netloc == "own-site.invalid"
        download = proof.find("a", download=True)
        download_url = urljoin("https://own-site.invalid/" + route, download["href"])
        downloadable = SITE / urlsplit(download_url).path.lstrip("/")
        immutable_bytes = subprocess.check_output(["git", "show", CORE + ":" + PRODUCTION], cwd=ROOT)
        assert downloadable.read_bytes() == raw(PRODUCTION) == immutable_bytes
        module_route = urlsplit(module_url).path.lstrip("/")
        full = soup(module_route).select_one("#complete-module-source")
        assert full.select_one("code.language-lean").get_text() == raw(PRODUCTION).decode()
        assert not full.select("details[open]")
        text = article.get_text(" ", strip=True)
        for term in ["every-point", "zero", "L1", "Ex71", "Ex72", "expected-cost", "main lower bounds"]:
            assert term in text, term
        pages.append({"route": route, "raw_html_sha256": sha((SITE / route).read_bytes()),
                      "canonical_articles": 1, "proof_steps": 5, "initial_open_details": 0,
                      "source_adjacent_exact_statement_and_proof": True, "complete_module_byte_exact": True,
                      "download_byte_exact": True, "immutable_Gitobject_byte_exact": True,
                      "module_link_branch": "site-local", "immutable_GitHub_URL_check": None,
                      "GitHub_URL_branch": "not_executed", "external_GitHub_HTML_checked": False})
    case_route = "example-cases/samplewiki/companions/gaussian-sampling-complexity.html"
    case = soup(case_route)
    boundary = case.select_one("#paper-main-results").get_text(" ", strip=True)
    for term in ["worst-case deterministic query cap", "not an expected-cost lower bound without a separate reduction",
                 "scalar", "Ex70", "Ex71", "Ex72", "volume", "Both main", "hidden"]:
        assert term in (boundary + case.get_text(" ", strip=True)), term
    index = case.select_one("#paper-lean-progress")
    unit = index.select('details.paper-verified-unit[data-publication-item="huanjian-product-density"]')
    assert len(unit) == 1
    links = unit[0].select('a[href$="source-huanjian-product-density.html"]')
    assert len(links) == 1
    assert (SITE / urlsplit(urljoin("https://own-site.invalid/" + case_route, links[0]["href"])).path.lstrip("/")).is_file()
    graph_raw = (SITE / "data/underlying-lean-graph.json").read_bytes()
    graph = json.loads(graph_raw)
    ident = "decl:" + TARGET
    nodes = [node for node in graph["nodes"] if node["id"] == ident]
    assert len(nodes) == 1 and nodes[0]["status"] == "compiled"
    edges = [edge for edge in graph["edges"] if edge["source"] == ident or edge["target"] == ident]
    assert {"source": "module:" + MODULE, "target": ident, "relation": "declares"} in edges
    refs = [edge for edge in edges if edge["relation"] == "source reference (scanner)"]
    assert len(refs) == 4
    assert all(edge["target"] == ident for edge in refs)
    assert not any(edge["relation"] in {"implies", "formal theorem dependency"} for edge in refs)
    report = {
        "kind": "independent-final-root-build-static-DOM-review",
        "recorded_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "reviewer": "/root/ex70_integration_reader_review", "core_commit": CORE,
        "source_digest_independently_recomputed": DIGEST,
        "actual_root_receipt": root, "actual_site_build_receipt": build,
        "actual_root_result": "Lake/root Tests9642 including ProductDensity consumers, ASTIS fake-closure gate and ATLAS memory check passed. Standard producer axioms only. Receipt/raw log independently checked; not an extra rerun.",
        "actual_gate_copy_byte_equal": True, "site_metadata_raw_sha256": sha((SITE / "data/build-metadata.json").read_bytes()),
        "site_metadata": metadata, "static_pages": pages,
        "case_source_index": {"route": case_route, "canonical_Ex70_units": 1, "focused_source_links": 1,
                              "raw_html_sha256": sha((SITE / case_route).read_bytes()),
                              "boundary": "Ex70 accepted; scalar power is identified as scalar; Ex71/72, oracle/precision/deterministic cap/expectedcost, hidden eigenbasis and both main bounds remain open."},
        "generated_graph": {"raw_sha256": sha(graph_raw), "canonical_target_nodes": 1,
                            "node": nodes[0], "bounded_one_hop_edges": edges,
                            "scanner_reference_count": 4, "scanner_reference_semantics": "Incomplete source-name signals; overlays, not formal theorem implication. Actual isotropic Gaussian use remains recorded in the authored dependencies even though this name scanner does not capture it.",
                            "formal_structure": "Owning module declares the unique target; imports/declares use formal structure; visual styling requires actual browser graph inspection."},
        "status": "ACTUAL_ROOT_AND_FINAL_BUILD_STATIC_DOM_ACCEPTED",
        "pending": ["Actual final site-check and graph-check receipts", "Actual Chrome interactions and all14 original PNGs independently viewed", "Separate later authorized lease parking"],
        "actual_browser_acceptance": False, "final_integration_acceptance": False,
        "source_link_scope": "Own-site complete module/download and immutable e566 Git object verified statically. No HTTP or browser claim from this script. GitHub blob URL branch not executed; no external HTML200 asserted.",
        "new_source_verdict_or_build": False
    }
    assert astis_site.source_digest() == DIGEST
    output = OUT / "candidate-e566930d-root-build-static-DOM-review.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"report": str(output.relative_to(ROOT)), "raw_sha256": sha(output.read_bytes()),
                      "status": report["status"], "root_jobs": 9642, "final_browser_pending": True}, ensure_ascii=False))


if __name__ == "__main__":
    main()
