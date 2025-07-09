from typing import List
import logging

# List of academic keywords
academic_keywords: List[str] = [
    "University", "College", "Institute", "Academy", "School", 
    "Faculty", "Academician", "PhD", "Professor",
]
    
# Function to check if an affiliation is academic
def is_academic(affiliation: str, academic_keywords: List[str]) -> bool:
    
    """Determines if a given affiliation string is academic based on a list of keywords.

    This function checks whether any of the provided academic keywords are present in the affiliation string (case-insensitive). If a match is found, it returns True. Otherwise, it returns False.

    Args:
        affiliation (str): The affiliation string to check.
        academic_keywords (List[str]): A list of academic-related keywords to search for..

    Returns:
        bool: True if the affiliation is considered academic, False otherwise.
    """
    logging.debug(f"Checking affiliation: {affiliation}")
    for keyword in academic_keywords:
        if keyword.lower() in affiliation.lower():
            return True
        
    logging.info(f"Affiliation '{affiliation}' is not academic.")
    return False


# List of pharmaceutical and biotech-related keywords to identify relevant companies
pharma_biotech_keywords: List[str] = [
    "Pharmaceutical", "Biotech", "Biotechnology", "Pharma", "Biopharma", 
    "Med", "Healthcare", "Bio", "Genetics", "Drug", "Therapeutics", "Vaccine",
    "Diagnostics", "Clinical", "Development", "Manufacturing"
]

# Function to check if an affiliation is related to pharmaceutical or biotech companies
def is_pharma_biotech(affiliation: str, pharma_biotech_keywords: List[str]) -> bool:
    """Checks if the given affiliation is related to the pharmaceutical or biotechnology industry.

    This function iterates over a list of keywords related to pharma/biotech industries
    and returns `True` if any of the keywords is found in the provided affiliation string.
    The comparison is case-insensitive.

    Args:
        affiliation (str): The affiliation string to check.
        pharma_biotech_keywords (List[str], optional): A list of keywords that are typically associated with the pharmaceutical or biotechnology industries. Default is an empty list.

    Returns:
        bool: `True` if the affiliation is related to pharma/biotech, 'False' otherwise.
    """
    logging.debug(f"Checking affiliation: {affiliation}")

    for keyword in pharma_biotech_keywords:
        if keyword.lower() in affiliation.lower():
            return True
        
    logging.info(f"Affiliation is not related to pharma/biotech: {affiliation}")
    return False