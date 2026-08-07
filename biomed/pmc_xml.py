"""Utilities for extracting coarse article sections from PubMed Central XML."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterable, Mapping

DEFAULT_SECTION_ALIASES: dict[str, tuple[str, ...]] = {
    "Introduction": ("introduction", "background", "context", "aim", "purpose"),
    "Methods": (
        "methods", "methodology", "materials and methods", "materials & methods",
        "experimental procedures", "experimental methods", "experimental section",
        "statistical analysis",
    ),
    "Results": ("results", "findings", "experimental results", "observations", "outcome"),
    "Discussion": (
        "discussion", "conclusion", "conclusions", "summary and conclusion",
        "outlook", "limitations",
    ),
}


def local_name(tag: str) -> str:
    """Return an XML tag without its namespace."""
    return tag.rsplit("}", 1)[-1]


def element_text(element: ET.Element) -> str:
    """Recursively collect text while preserving readable spacing."""
    return " ".join(part.strip() for part in element.itertext() if part and part.strip())


def _title(section: ET.Element) -> str:
    for child in section:
        if local_name(child.tag) == "title":
            return element_text(child).strip()
    return ""


def _section_matches(title: str, aliases: Iterable[str]) -> bool:
    normalized = " ".join(title.lower().split())
    return any(alias.lower() in normalized for alias in aliases)


def extract_pmc_sections(
    xml_path: str | Path,
    *,
    section_aliases: Mapping[str, Iterable[str]] = DEFAULT_SECTION_ALIASES,
    combine_repeated: bool = True,
) -> dict[str, str]:
    """Extract Abstract and broad body sections from JATS/PMC XML.

    Matching is intentionally heuristic because section titles vary widely across
    journals. Nested ``sec`` elements are traversed recursively. Repeated matched
    sections are concatenated by default rather than silently discarding later
    sections.
    """
    path = Path(xml_path)
    if not path.exists():
        raise FileNotFoundError(path)

    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        raise ValueError(f"Invalid XML: {path}") from exc

    output: dict[str, str] = {}

    abstract = root.find(".//{*}abstract")
    if abstract is not None:
        text = element_text(abstract)
        if text:
            output["Abstract"] = text

    body = root.find(".//{*}body")
    if body is None:
        return output

    for section in body.iter():
        if local_name(section.tag) != "sec":
            continue
        title = _title(section)
        if not title:
            continue
        for canonical, aliases in section_aliases.items():
            if not _section_matches(title, aliases):
                continue
            text = element_text(section)
            if not text:
                break
            if combine_repeated and canonical in output:
                output[canonical] = f"{output[canonical]}\n\n{text}"
            elif canonical not in output:
                output[canonical] = text
            break

    return output
