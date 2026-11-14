#!/usr/bin/env python3
"""Canonical source-edition validation for the ASTIS Chewi program."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import unicodedata
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "website" / "content"
EDITION_PATH = CONTENT / "source_edition.json"
CHAPTERS_PATH = CONTENT / "chapters.json"
CORRESPONDENCE_PATH = CONTENT / "source_correspondence.json"
CHAPTER_1_MATRIX_PATH = CONTENT / "chapter_1_completion_matrix.json"
CANONICAL_URL = "https://chewisinho.github.io/main.pdf"
CANONICAL_EDITION = "2026-08-09"
PDF_OFFSET = 12
PDF_SHA256 = "9b454ccf44fe700081e13a766ae9cabb83c3530f5fdc532d59ac335f53652597"
DEFAULT_LOCAL_PDF = (
    ROOT.parent
    / "outer_papers"
    / "sampling_theory_sde"
    / "Chewi-Log-Concave-Sampling"
    / "main.pdf"
)

EXPECTED_CHAPTER_1_STATEMENTS = set("""
1.1.1 1.1.4 1.1.8 1.1.11 1.1.12 1.1.13 1.1.15 1.1.16 1.1.17 1.1.19 1.1.22
1.2.1 1.2.2 1.2.3 1.2.4 1.2.5 1.2.6 1.2.7 1.2.8 1.2.9 1.2.10 1.2.12 1.2.13
1.2.14 1.2.15 1.2.17 1.2.19 1.2.20 1.2.21 1.2.22 1.2.23 1.2.25 1.2.26 1.2.27
1.2.28 1.2.29 1.2.30 1.2.31
1.3.1 1.3.3 1.3.4 1.3.6 1.3.8 1.3.12 1.3.13 1.3.14 1.3.15 1.3.16 1.3.17 1.3.19
1.3.20 1.3.23 1.3.25 1.3.26
1.4.1 1.4.2 1.4.5 1.4.6 1.4.12
1.5.1 1.5.2 1.5.3 1.5.4 1.5.5 1.5.6 1.5.7 1.5.8
""".split())
EXPECTED_CHAPTER_1_DISPLAYS = set("""
1.0.1 1.1.2 1.1.3 1.1.5 1.1.6 1.1.7 1.1.9 1.1.10 1.1.14 1.1.18 1.1.20 1.1.21
1.2.11 1.2.16 1.2.18 1.2.24 1.3.2 1.3.5 1.3.7 1.3.9 1.3.10 1.3.11 1.3.18 1.3.21
1.3.22 1.3.24 1.4.3 1.4.4 1.4.7 1.4.8 1.4.9 1.4.10 1.4.11 1.4.13 1.4.14 1.4.15 1.4.16
""".split())

# This table is deliberately independent from website metadata. A mistaken edit
# cannot make the source contract and its checker drift together.
EXPECTED_OUTLINE: tuple[tuple[int, str, int, tuple[tuple[str, str, int], ...]], ...] = (
    (1, "The Langevin Diffusion in Continuous Time", 3, (("1.1", "A Primer on Stochastic Calculus", 3), ("1.2", "Markov Semigroup Theory", 10), ("1.3", "The Geometry of Optimal Transport", 19), ("1.4", "The Langevin SDE as a Wasserstein Gradient Flow", 31), ("1.5", "Overview of the Convergence Results", 36), ("1.bib", "Bibliographical Notes", 40), ("1.ex", "Exercises", 41))),
    (2, "Functional Inequalities", 48, (("2.1", "Overview of the Inequalities", 48), ("2.2", "Proofs via Markov Semigroup Theory", 50), ("2.3", "Operations Preserving Functional Inequalities", 60), ("2.4", "Concentration of Measure and Isoperimetry", 68), ("2.5", "Riemannian Manifolds", 77), ("2.6", "Discrete Space and Time", 84), ("2.bib", "Bibliographical Notes", 85), ("2.ex", "Exercises", 87))),
    (3, "Additional Topics in Stochastic Analysis", 96, (("3.1", "Quadratic Variation", 96), ("3.2", "Change of Measure in Path Space", 100), ("3.3", "Doob's Transform", 104), ("3.4", "Föllmer Drift", 108), ("3.5", "Schrödinger Bridge", 110), ("3.bib", "Bibliographical Notes", 114), ("3.ex", "Exercises", 116))),
    (4, "Analysis of Langevin Monte Carlo", 123, (("4.1", "Proof via Wasserstein Coupling", 124), ("4.2", "Proof via Interpolation Argument", 127), ("4.3", "Proof via Convex Optimization", 131), ("4.4", "Proof via Girsanov's Theorem", 134), ("4.bib", "Bibliographical Notes", 137), ("4.ex", "Exercises", 138))),
    (5, "Faster Low-Accuracy Samplers", 141, (("5.1", "Randomized Midpoint Discretization", 141), ("5.2", "Hamiltonian Monte Carlo", 145), ("5.3", "The Underdamped Langevin Diffusion", 149), ("5.bib", "Bibliographical Notes", 166), ("5.ex", "Exercises", 168))),
    (6, "Convergence in Rényi Divergence", 174, (("6.1", "Analysis of LMC via Interpolation Argument", 174), ("6.2", "Analysis of LMC via Girsanov's Theorem", 178), ("6.3", "Analysis of ULMC via Girsanov's Theorem", 183), ("6.bib", "Bibliographical Notes", 184), ("6.ex", "Exercises", 185))),
    (7, "High-Accuracy Samplers", 189, (("7.1", "Rejection Sampling", 189), ("7.2", "The Metropolis-Hastings Filter", 191), ("7.3", "An Overview of High-Accuracy Samplers", 193), ("7.4", "Markov Chains in Discrete Time", 197), ("7.5", "Analysis of MALA for a Cold Start", 203), ("7.6", "Analysis of MALA for a Warm Start", 206), ("7.bib", "Bibliographical Notes", 209), ("7.ex", "Exercises", 211))),
    (8, "The Proximal Sampler", 214, (("8.1", "Introduction to the Proximal Sampler", 215), ("8.2", "Convergence under Strong Log-Concavity", 216), ("8.3", "Simultaneous Flow and Time Reversal", 218), ("8.4", "Convergence under Log-Concavity", 221), ("8.5", "Convergence under Functional Inequalities", 222), ("8.6", "Implementations of the RGO and Applications", 223), ("8.bib", "Bibliographical Notes", 229), ("8.ex", "Exercises", 230))),
    (9, "Lower Bounds for Sampling", 233, (("9.1", "A Brief Discussion of Query Complexity", 233), ("9.2", "Query Complexity in One Dimension", 234), ("9.3", "Query Complexity in Constant Dimension", 241), ("9.4", "Query Complexity for Gaussians", 243), ("9.bib", "Bibliographical Notes", 245), ("9.ex", "Exercises", 246))),
    (10, "Structured Sampling", 249, (("10.1", "Stochastic Gradients", 249), ("10.2", "Coordinate Methods", 252), ("10.3", "Mirror Langevin", 257), ("10.bib", "Bibliographical Notes", 268), ("10.ex", "Exercises", 269))),
    (11, "Non-Log-Concave Sampling", 272, (("11.1", "Approximate First-Order Stationarity via Fisher Information", 272), ("11.2", "Fisher Information Bounds", 274), ("11.3", "Applications of Fisher Information Bounds", 276), ("11.4", "Lower Bounds", 279), ("11.bib", "Bibliographical Notes", 280), ("11.ex", "Exercises", 280))),
    (12, "Diffusion Generative Models", 283, (("12.1", "Introduction", 283), ("12.2", "Score Matching and Variants", 284), ("12.3", "Discretization Analysis", 288), ("12.bib", "Bibliographical Notes", 295))),
)


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def normalized(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    ascii_text = "".join(char for char in decomposed if not unicodedata.combining(char))
    return re.sub(r"\s+", " ", ascii_text).strip().lower()


def _semantic_source_label_present(page_text: str, source_kind: str, section: str) -> bool:
    label_match = re.match(
        r"^(Definition|Example|Corollary|Theorem|Lemma|Proposition|Remark|Optimization Box)\s+(.+)$",
        source_kind,
    )
    if not label_match:
        return normalized(section) in page_text
    exact = normalized(source_kind)
    if exact in page_text:
        return True
    kind = normalized(label_match.group(1))
    number = normalized(label_match.group(2))
    split_label = rf"\b{re.escape(kind)}\b.{{0,160}}{re.escape(number)}\b"
    return re.search(split_label, page_text) is not None


def expected_chapters() -> list[dict[str, object]]:
    return [
        {
            "number": number,
            "title": title,
            "book_page": page,
            "sections": [
                {"id": section_id, "title": section_title, "book_page": section_page}
                for section_id, section_title, section_page in sections
            ],
        }
        for number, title, page, sections in EXPECTED_OUTLINE
    ]


def _source_page_bounds(edition: dict[str, object]) -> dict[str, tuple[int, int]]:
    bounds: dict[str, tuple[int, int]] = {}
    for raw_chapter in edition["chapters"]:
        chapter = dict(raw_chapter)
        sections = list(chapter["sections"])
        chapter_end = int(chapter["book_page_end"])
        for index, raw_section in enumerate(sections):
            section = dict(raw_section)
            start = int(section["book_page"])
            # A section heading can begin below the preceding section's final
            # theorem on the same printed page, so boundary pages overlap.
            end = int(dict(sections[index + 1])["book_page"]) if index + 1 < len(sections) else chapter_end
            bounds[str(section["id"])] = (start, end)
    return bounds


def _validate_local_pdf(path: Path, correspondence: list[dict[str, object]]) -> list[str]:
    errors: list[str] = []
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != PDF_SHA256:
        return [f"local PDF checksum is {digest}, expected {PDF_SHA256}: {path}"]
    info = subprocess.run(["pdfinfo", str(path)], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    if info.returncode != 0 or not re.search(r"^Pages:\s+329\s*$", info.stdout, re.MULTILINE):
        errors.append(f"local PDF is not the canonical 329-page edition: {path}")
    for row in correspondence:
        page = int(row["pdf_page"])
        result = subprocess.run(
            ["pdftotext", "-layout", "-f", str(page), "-l", str(page), str(path), "-"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        page_text = normalized(result.stdout)
        source_kind = str(row["source_kind"])
        if result.returncode != 0 or not _semantic_source_label_present(
            page_text, source_kind, str(row["section"])
        ):
            errors.append(f"semantic source label not found on PDF page {page}: {row['id']} ({source_kind})")
    return errors


def validate_source_contract(*, pdf_path: Path | None = None, require_pdf: bool = False) -> tuple[list[str], dict[str, object]]:
    errors: list[str] = []
    edition = load_json(EDITION_PATH)
    chapters = load_json(CHAPTERS_PATH)
    correspondence = load_json(CORRESPONDENCE_PATH)
    chapter_1_matrix = load_json(CHAPTER_1_MATRIX_PATH)
    if not isinstance(edition, dict) or not isinstance(chapters, list) or not isinstance(correspondence, list) or not isinstance(chapter_1_matrix, dict):
        return ["source metadata has an invalid top-level shape"], {}

    if chapter_1_matrix.get("edition") != CANONICAL_EDITION:
        errors.append("Chapter 1 completion matrix has the wrong source edition")
    if chapter_1_matrix.get("canonical_url") != CANONICAL_URL:
        errors.append("Chapter 1 completion matrix has the wrong canonical URL")
    if chapter_1_matrix.get("schema_version") != 2:
        errors.append("Chapter 1 completion matrix must use schema version 2")
    items = list(chapter_1_matrix.get("items", []))
    statements = [row for row in items if isinstance(row, dict) and row.get("category") == "statement"]
    displays = [row for row in items if isinstance(row, dict) and row.get("category") == "displayed_identity"]
    exercises = [row for row in items if isinstance(row, dict) and row.get("category") == "exercise"]
    statement_numbers = {str(row.get("number", "")) for row in statements}
    display_numbers = {str(row.get("number", "")) for row in displays}
    exercise_numbers = {str(row.get("number", "")) for row in exercises}
    if statement_numbers != EXPECTED_CHAPTER_1_STATEMENTS or len(statements) != len(statement_numbers):
        errors.append("Chapter 1 statement inventory differs from the audited 67-item source list")
    if display_numbers != EXPECTED_CHAPTER_1_DISPLAYS or len(displays) != len(display_numbers):
        errors.append("Chapter 1 displayed-identity inventory differs from the audited 37-item source list")
    expected_exercises = {f"1.{index}" for index in range(1, 22)}
    if exercise_numbers != expected_exercises or len(exercises) != len(exercise_numbers):
        errors.append("Chapter 1 exercise inventory differs from Exercises 1.1-1.21")
    for category, rows in (
        ("statement", statements),
        ("displayed identity", displays),
        ("exercise", exercises),
    ):
        for row in rows:
            if not isinstance(row, dict):
                errors.append(f"Chapter 1 {category} row has invalid shape: {row!r}")
                continue
            book_page, pdf_page = int(row.get("book_page", -1)), int(row.get("pdf_page", -1))
            if not 3 <= book_page <= 47 or pdf_page != book_page + PDF_OFFSET:
                errors.append(f"Chapter 1 {category} {row.get('number')} has invalid page mapping")
    correspondence_ids = {str(row.get("id", "")) for row in correspondence}
    for row in items:
        if not isinstance(row, dict):
            continue
        source_id = str(row.get("source_correspondence_id", ""))
        if source_id and source_id not in correspondence_ids:
            errors.append(
                f"Chapter 1 matrix route {row.get('number')} references unknown source row {source_id}"
            )

    expected = expected_chapters()
    for key, value in {
        "edition": CANONICAL_EDITION,
        "canonical_url": CANONICAL_URL,
        "body_pdf_page_offset": PDF_OFFSET,
        "pdf_sha256": PDF_SHA256,
        "pdf_pages": 329,
    }.items():
        if edition.get(key) != value:
            errors.append(f"source_edition.{key}={edition.get(key)!r}, expected {value!r}")
    actual_outline = []
    for raw_chapter in edition.get("chapters", []):
        chapter = dict(raw_chapter)
        actual_outline.append({
            "number": chapter.get("number"),
            "title": chapter.get("title"),
            "book_page": chapter.get("book_page"),
            "sections": [
                {"id": row.get("id"), "title": row.get("title"), "book_page": row.get("book_page")}
                for row in chapter.get("sections", [])
            ],
        })
    if actual_outline != expected:
        errors.append("source_edition chapter/section outline differs from the canonical August 9 TOC")

    expected_by_number = {int(row["number"]): row for row in expected}
    for chapter in chapters:
        number = int(chapter["number"])
        canonical = expected_by_number.get(number)
        if canonical is None:
            errors.append(f"chapters.json has unexpected chapter {number}")
            continue
        if chapter.get("title") != canonical["title"]:
            errors.append(f"chapter {number} title differs from canonical TOC")
        expected_sections = [
            f"{row['id']} {row['title']} (p. {row['book_page']})"
            for row in canonical["sections"]
            if re.fullmatch(r"\d+\.\d+", str(row["id"]))
        ]
        if chapter.get("source_sections") != expected_sections:
            errors.append(f"chapter {number} source_sections differ from canonical TOC")
        edition_chapter = dict(edition["chapters"][number - 1])
        expected_range = f"{edition_chapter['book_page']}–{edition_chapter['book_page_end']}"
        if chapter.get("source_pages") != expected_range:
            errors.append(f"chapter {number} source_pages={chapter.get('source_pages')!r}, expected {expected_range!r}")
    if len(chapters) != 12:
        errors.append(f"chapters.json has {len(chapters)} chapters, expected 12")

    bounds = _source_page_bounds(edition)
    labels: list[str] = []
    ids: list[str] = []
    for row in correspondence:
        row_id = str(row.get("id", ""))
        ids.append(row_id)
        if not str(row.get("mathematical_exposition", "")).strip():
            errors.append(f"{row_id}: mathematical_exposition is required for textbook-first rendering")
        section = str(row.get("section", ""))
        book_page = row.get("book_page")
        pdf_page = row.get("pdf_page")
        if row.get("edition") != CANONICAL_EDITION:
            errors.append(f"{row_id}: edition must be {CANONICAL_EDITION}")
        if section not in bounds or not re.fullmatch(r"\d+\.\d+", section):
            errors.append(f"{row_id}: section {section!r} is not a canonical numbered section")
            continue
        if not isinstance(book_page, int) or not isinstance(pdf_page, int):
            errors.append(f"{row_id}: book_page and pdf_page must be integers")
            continue
        start, end = bounds[section]
        if not start <= book_page <= end:
            errors.append(f"{row_id}: book page {book_page} is outside section {section} ({start}–{end})")
        if pdf_page != book_page + PDF_OFFSET:
            errors.append(f"{row_id}: PDF page {pdf_page} must equal book page {book_page} + {PDF_OFFSET}")
        expected_url = f"{CANONICAL_URL}#page={pdf_page}"
        if row.get("source_url") != expected_url:
            errors.append(f"{row_id}: source_url must be {expected_url}")
        expected_display = f"book {book_page} / PDF {pdf_page}"
        if row.get("page") != expected_display:
            errors.append(f"{row_id}: page display must be {expected_display!r}")
        labels.append(str(row.get("source_kind", "")))
    for value, count in Counter(ids).items():
        if not value or count > 1:
            errors.append(f"duplicate or empty source correspondence id: {value!r}")
    semantic_labels = [
        label for label in labels
        if re.match(r"^(Definition|Example|Corollary|Theorem|Lemma|Proposition|Remark|Optimization Box)\s+", label)
    ]
    for value, count in Counter(semantic_labels).items():
        if count > 1:
            errors.append(f"duplicate semantic source label: {value}")

    stale_files = [ROOT / "README.md", ROOT / "website" / "README.md", ROOT / "tools" / "astis_site.py"]
    stale_pattern = re.compile(r"June 12,? 2026|2026-06-12")
    for path in stale_files:
        if path.exists() and stale_pattern.search(path.read_text(encoding="utf-8")):
            errors.append(f"stale June 12 edition reference in public/current source: {path.relative_to(ROOT)}")

    selected_pdf = pdf_path if pdf_path is not None else DEFAULT_LOCAL_PDF
    pdf_checked = False
    if selected_pdf.exists():
        pdf_checked = True
        if all(isinstance(row.get("pdf_page"), int) for row in correspondence):
            errors.extend(_validate_local_pdf(selected_pdf, correspondence))
        else:
            errors.append("source correspondence is missing integer pdf_page fields")
    elif require_pdf:
        errors.append(f"canonical local PDF required but missing: {selected_pdf}")
    stats = {
        "edition": CANONICAL_EDITION,
        "chapters": len(expected),
        "sections": sum(len(row[3]) for row in EXPECTED_OUTLINE),
        "source_anchors": len(correspondence),
        "pdf_checked": pdf_checked,
        "pdf_path": str(selected_pdf),
    }
    return errors, stats


def command_check(args: argparse.Namespace) -> int:
    pdf_path = Path(args.pdf).expanduser().resolve() if args.pdf else None
    errors, stats = validate_source_contract(pdf_path=pdf_path, require_pdf=args.require_pdf)
    if errors:
        print("Chewi source check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    pdf_note = "semantic PDF anchors checked" if stats["pdf_checked"] else "metadata-only (PDF unavailable)"
    print(
        "Chewi source check passed: "
        f"edition {stats['edition']}, {stats['chapters']} chapters, "
        f"{stats['sections']} TOC entries, {stats['source_anchors']} source anchors; {pdf_note}"
    )
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--pdf", default="", help="canonical local PDF to verify")
    result.add_argument("--require-pdf", action="store_true", help="fail if a local PDF is unavailable")
    return result


def main(argv: list[str] | None = None) -> int:
    return command_check(parser().parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main())
