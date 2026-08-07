from .normalization import clean_text_for_matching, normalize_drug_name, normalize_gene_name, normalize_protein_name
from .pmc_xml import extract_pmc_sections

normalize_drug = normalize_drug_name
normalize_gene = normalize_gene_name
normalize_protein = normalize_protein_name
normalize_text = clean_text_for_matching
read_pmc = extract_pmc_sections

__all__ = [
    "clean_text_for_matching",
    "extract_pmc_sections",
    "normalize_drug",
    "normalize_drug_name",
    "normalize_gene",
    "normalize_gene_name",
    "normalize_protein",
    "normalize_protein_name",
    "normalize_text",
    "read_pmc",
]
