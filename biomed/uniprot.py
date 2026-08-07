"""UniProt gene/accession mapping helpers.

The high-level API is optimized for the common case of mapping human gene
symbols to reviewed UniProtKB accessions and back. The organism and review
filters are explicit and can be changed when needed.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import time
from typing import Any, Iterable, Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


DEFAULT_BASE_URL = "https://rest.uniprot.org"
DEFAULT_ORGANISM_ID = 9606


class CacheLike(Protocol):
    def get(self, key: str, default: Any = None) -> Any: ...
    def set(self, key: str, value: Any) -> Any: ...


@dataclass(frozen=True)
class UniProtRecord:
    accession: str
    gene_name: str | None
    entry_name: str | None
    organism_id: int | None
    reviewed: bool | None
    protein_name: str | None = None

    @classmethod
    def from_api(cls, item: dict[str, Any]) -> "UniProtRecord":
        gene_name = None
        genes = item.get("genes") or []
        if genes:
            gene_name = (genes[0].get("geneName") or {}).get("value")

        protein_name = None
        protein = item.get("proteinDescription") or {}
        recommended = protein.get("recommendedName") or {}
        full_name = recommended.get("fullName") or {}
        protein_name = full_name.get("value")
        if protein_name is None:
            submission_names = protein.get("submissionNames") or []
            if submission_names:
                protein_name = (submission_names[0].get("fullName") or {}).get("value")

        organism = item.get("organism") or {}
        entry_type = str(item.get("entryType", ""))
        reviewed = None
        if entry_type:
            reviewed = "reviewed" in entry_type.lower() and "unreviewed" not in entry_type.lower()

        return cls(
            accession=str(item.get("primaryAccession", "")),
            gene_name=gene_name,
            entry_name=item.get("uniProtkbId"),
            organism_id=organism.get("taxonId"),
            reviewed=reviewed,
            protein_name=protein_name,
        )


class UniProtClient:
    """Small dependency-free client for UniProtKB gene/accession lookup."""

    def __init__(
        self,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 20.0,
        retries: int = 3,
        backoff: float = 0.75,
        cache: CacheLike | None = None,
        user_agent: str = "research-toolbox/0.1",
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retries = retries
        self.backoff = backoff
        self.cache = cache
        self.user_agent = user_agent

    def gene_to_records(
        self,
        gene: str,
        *,
        organism_id: int | None = DEFAULT_ORGANISM_ID,
        reviewed: bool | None = True,
        size: int = 25,
    ) -> list[UniProtRecord]:
        """Return UniProtKB records matching an exact gene name.

        ``organism_id=9606`` and ``reviewed=True`` are intentional defaults for
        the common human/Swiss-Prot use case. Set either to ``None`` to remove
        that filter.
        """
        gene = _clean_required(gene, "gene")
        query_parts = [f"gene_exact:{_quote_query(gene)}"]
        if organism_id is not None:
            query_parts.append(f"organism_id:{int(organism_id)}")
        if reviewed is not None:
            query_parts.append(f"reviewed:{str(reviewed).lower()}")
        query = " AND ".join(query_parts)
        data = self._search(query, size=size)
        return [UniProtRecord.from_api(item) for item in data.get("results", [])]

    def gene_to_uniprot(
        self,
        gene: str,
        *,
        organism_id: int | None = DEFAULT_ORGANISM_ID,
        reviewed: bool | None = True,
        all_matches: bool = False,
    ) -> str | list[str] | None:
        """Map a gene name to UniProtKB accession(s)."""
        records = self.gene_to_records(
            gene,
            organism_id=organism_id,
            reviewed=reviewed,
        )
        accessions = [record.accession for record in records if record.accession]
        if all_matches:
            return accessions
        return accessions[0] if accessions else None

    def genes_to_uniprot(
        self,
        genes: Iterable[str],
        *,
        organism_id: int | None = DEFAULT_ORGANISM_ID,
        reviewed: bool | None = True,
        all_matches: bool = False,
    ) -> dict[str, str | list[str] | None]:
        """Map multiple gene names while preserving input names as keys."""
        return {
            gene: self.gene_to_uniprot(
                gene,
                organism_id=organism_id,
                reviewed=reviewed,
                all_matches=all_matches,
            )
            for gene in genes
        }

    def uniprot_to_record(self, accession: str) -> UniProtRecord | None:
        """Return the UniProtKB record for an accession, or ``None`` if absent."""
        accession = _clean_required(accession, "accession").upper()
        query = f"accession:{_quote_query(accession)}"
        data = self._search(query, size=1)
        results = data.get("results", [])
        return UniProtRecord.from_api(results[0]) if results else None

    def uniprot_to_gene(self, accession: str) -> str | None:
        """Map a UniProtKB accession to its primary gene name."""
        record = self.uniprot_to_record(accession)
        return record.gene_name if record else None

    def uniprots_to_gene(self, accessions: Iterable[str]) -> dict[str, str | None]:
        """Map multiple UniProtKB accessions to primary gene names."""
        return {accession: self.uniprot_to_gene(accession) for accession in accessions}

    def _search(self, query: str, *, size: int) -> dict[str, Any]:
        params = urlencode({"query": query, "format": "json", "size": int(size)})
        url = f"{self.base_url}/uniprotkb/search?{params}"
        cache_key = f"uniprot:{url}"
        if self.cache is not None:
            cached = self.cache.get(cache_key, None)
            if cached is not None:
                return cached

        request = Request(url, headers={"Accept": "application/json", "User-Agent": self.user_agent})
        last_error: Exception | None = None
        for attempt in range(self.retries + 1):
            try:
                with urlopen(request, timeout=self.timeout) as response:
                    data = json.loads(response.read().decode("utf-8"))
                if self.cache is not None:
                    self.cache.set(cache_key, data)
                return data
            except HTTPError as exc:
                last_error = exc
                if exc.code not in {429, 500, 502, 503, 504} or attempt >= self.retries:
                    raise RuntimeError(f"UniProt request failed with HTTP {exc.code}: {url}") from exc
            except URLError as exc:
                last_error = exc
                if attempt >= self.retries:
                    raise RuntimeError(f"UniProt request failed: {url}") from exc
            time.sleep(self.backoff * (2**attempt))

        raise RuntimeError(f"UniProt request failed: {url}") from last_error


def gene_to_uniprot(
    gene: str,
    *,
    organism_id: int | None = DEFAULT_ORGANISM_ID,
    reviewed: bool | None = True,
    all_matches: bool = False,
    client: UniProtClient | None = None,
) -> str | list[str] | None:
    """Convenience wrapper for :meth:`UniProtClient.gene_to_uniprot`."""
    return (client or UniProtClient()).gene_to_uniprot(
        gene,
        organism_id=organism_id,
        reviewed=reviewed,
        all_matches=all_matches,
    )


def genes_to_uniprot(
    genes: Iterable[str],
    *,
    organism_id: int | None = DEFAULT_ORGANISM_ID,
    reviewed: bool | None = True,
    all_matches: bool = False,
    client: UniProtClient | None = None,
) -> dict[str, str | list[str] | None]:
    """Convenience wrapper for mapping multiple genes."""
    return (client or UniProtClient()).genes_to_uniprot(
        genes,
        organism_id=organism_id,
        reviewed=reviewed,
        all_matches=all_matches,
    )


def uniprot_to_gene(accession: str, *, client: UniProtClient | None = None) -> str | None:
    """Convenience wrapper mapping one UniProtKB accession to a gene name."""
    return (client or UniProtClient()).uniprot_to_gene(accession)


def uniprots_to_gene(
    accessions: Iterable[str],
    *,
    client: UniProtClient | None = None,
) -> dict[str, str | None]:
    """Convenience wrapper mapping multiple accessions to gene names."""
    return (client or UniProtClient()).uniprots_to_gene(accessions)


def _clean_required(value: str, name: str) -> str:
    cleaned = " ".join(str(value).strip().split())
    if not cleaned:
        raise ValueError(f"{name} must not be empty")
    return cleaned


def _quote_query(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


__all__ = [
    "DEFAULT_ORGANISM_ID",
    "UniProtClient",
    "UniProtRecord",
    "gene_to_uniprot",
    "genes_to_uniprot",
    "uniprot_to_gene",
    "uniprots_to_gene",
]
