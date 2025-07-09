import logging
import re
from typing import List
import xml.etree.ElementTree as ET

from .filters import is_academic, is_pharma_biotech

# Function to extract PubMed ID
def get_pubmed_id(root: ET.Element, pubmed_id: str) -> str:
    """Extracts the PubMed ID from the given input.

    Args:
        root (ET.Element): The XML root element containing the paper's metadata.
        pubmed_id (str): The PubMed ID to return or extract.

    Returns:
        str: The provided PubMed ID.
    """
    logging.debug(f"Extracting PubMed ID: {pubmed_id}")
    return pubmed_id

# Function to extract the title of the paper
def get_title(root: ET.Element) -> str:
    """Extracts the title of a paper from the given XML element.

    Args:
        root (ET.Element): The XML root element containing the paper's metadata.

    Returns:
        str: The title of the paper if found, otherwise "N/A".
    """
    title_tag = root.find(".//ArticleTitle")
    if title_tag is not None:
        logging.info(f"Title extracted: {title_tag.text}")
        return title_tag.text
    else:
        logging.warning("Title not found in the XML.")
        return "N/A"

# Function to extract the publication date
def get_publication_date(root: ET.Element) -> str:
    """Extracts the publication date of a paper from the given XML element.

    Args:
        root (ET.Element): The XML root element containing the paper's metadata.

    Returns:
        str: The publication date in the format "YYYY-MM-DD" if found, otherwise "N/A".
    """
    pub_date_tag = root.find(".//PubDate")
    if pub_date_tag is not None:
        year = pub_date_tag.find("Year")
        month = pub_date_tag.find("Month")
        day = pub_date_tag.find("Day")
        if year is not None and month is not None and day is not None:
            date = f"{year.text}-{month.text}-{day.text}"
            logging.info(f"Publication date extracted: {date}")
            return date
        else:
            logging.warning("Incomplete publication date found (missing year, month, or day).")
            return "N/A"
    else:
        logging.warning("Publication date not found in the XML.")
        return "N/A"
    

# Function to extract authors
def get_authors(root: ET.Element, academic_keywords: List[str]) -> List[str]:
    """Extracts authors from the given XML data, filtering out academic authors based on their affiliation.

    This function searches for the <AuthorList> and <Author> tags in the XML, retrieving the last name,
    first name, and affiliation information for each author. If an author has a non-academic affiliation, 
    they are included in the result. If no affiliation is found, the author is considered non-academic by default.

    Args:
        root (ET.Element):The XML root element containing the paper's metadata.
        academic_keywords (List[str]): A list of keywords that help identify academic affiliations. Authors with academic affiliations are excluded from the result.

    Returns:
        List[str]: A list of authors' names who are considered non-academic based on their affiliation, or ["N/A"] if no authors are found or all are academic.
    """
    logging.debug("Extracting authors from the XML data.")

    authors_tag = root.findall(".//AuthorList/Author")
    authors = []
    for author in authors_tag:
        last_name = author.find("LastName")
        fore_name = author.find("ForeName")
        affiliation_info = author.findall(".//AffiliationInfo/Affiliation")
        
        logging.debug(f"Processing author: {fore_name.text if fore_name is not None else 'N/A'} {last_name.text if last_name is not None else 'N/A'}")

        # Get the affiliations and check if they are non-academic
        if affiliation_info:
            for aff in affiliation_info:
                logging.debug(f"Checking affiliation: {aff.text if aff is not None else 'N/A'}")
                if aff is not None and not is_academic(aff.text, academic_keywords):
                    if last_name is not None and fore_name is not None:
                        author_name = f"{fore_name.text} {last_name.text}"
                        logging.info(f"Adding author: {author_name}")
                        authors.append(author_name)
                    break
        else:
            # If no affiliation is found, consider it as non-academic
            if last_name is not None and fore_name is not None:
                author_name = f"{fore_name.text} {last_name.text}"
                logging.info(f"Adding author: {author_name}")
                authors.append(author_name)
    
    if authors:
        logging.debug(f"Authors extracted: {authors}")
    else:
        logging.debug("No authors found.")

    return authors if authors else ["N/A"]


email_pattern = r"[\w\.-]+@[\w\.-]+"

def get_pharma_biotech_affiliations(root: ET.Element, pharma_biotech_keywords: List[str], academic_keywords: List[str]) -> List[str]:
    """Extracts non-academic pharma/biotech affiliations from the given XML data.
    
    This function searches the XML for authors' affiliations and filters out those related to pharma or 
    biotech industries, while excluding academic affiliations. The function also cleans the affiliation 
    text by removing any email addresses.

    Args:
        root (ET.Element): The XML root element containing the paper's metadata.
        pharma_biotech_keywords (List[str]): A list of keywords identifying pharma/biotech-related affiliations.
        academic_keywords (List[str]): A list of keywords identifying academic affiliations. Authors with these affiliations are excluded.

    Returns:
        List[str]: A list of non-academic pharma/biotech affiliations, or ["N/A"] if no such affiliations are found.
    """
    logging.debug("Extracting pharma/biotech affiliations from the XML data.")
    pharma_biotech_affiliations = []
    authors_tag = root.findall(".//AuthorList/Author")
    
    for author in authors_tag:
        aff_info = author.findall(".//AffiliationInfo/Affiliation")
        for aff in aff_info:
            if aff is not None:
                logging.debug(f"Checking affiliation: {aff.text}")
                
                if is_pharma_biotech(aff.text, pharma_biotech_keywords) and not is_academic(aff.text, academic_keywords):
                    # Remove email from affiliation text
                    clean_affiliation = re.sub(email_pattern, '', aff.text).strip()
                    
                    if clean_affiliation:  # Ensure there's something left after removing emails
                        logging.info(f"Adding pharma/biotech affiliation: {clean_affiliation}")
                        pharma_biotech_affiliations.append(clean_affiliation)
    
    if pharma_biotech_affiliations:
        logging.debug(f"Pharma/Biotech affiliations extracted: {pharma_biotech_affiliations}")
    else:
        logging.debug("No pharma/biotech affiliations found.")

    return list(set(pharma_biotech_affiliations)) if pharma_biotech_affiliations else ["N/A"]


# Function to extract corresponding author email
def get_corresponding_email(root: ET.Element, academic_keywords: List[str]) -> List[str]:
    """Extracts the corresponding author's email from the XML data, excluding academic affiliations.

    This function iterates through the authors' affiliations and attempts to extract an email address 
    from a non-academic affiliation. It assumes that the email is the last part of the affiliation text 
    and checks if the affiliation is not academic before selecting the email as the corresponding author's.

    Args:
        root (ET.Element): The XML root element containing the paper's metadata, including authors' affiliations.
        academic_keywords (List[str]): A list of keywords identifying academic affiliations. Emails from academic affiliations are excluded.

    Returns:
        List[str]: The corresponding author's email if found, or "N/A" if no corresponding email is found.
    """
    logging.debug("Extracting corresponding email from the XML data.")
    corresponding_email = None
    
    authors_tag = root.findall(".//AuthorList/Author")
    for author in authors_tag:
        aff_info = author.findall(".//AffiliationInfo/Affiliation")
        for aff in aff_info:
            if aff is not None:
                # Split the affiliation text and get the last part (email)
                email = aff.text.split()[-1] if aff.text else "N/A"
                
                logging.debug(f"Checking affiliation: {aff.text} for email.")
                
                if "@" in email:
                    # Check if the affiliation belongs to a non-academic institution
                    if not is_academic(aff.text, academic_keywords):
                        corresponding_email = email
                        logging.info(f"Corresponding email found: {corresponding_email}")
                        break  # Exit after finding the first non-academic email
    
    if corresponding_email:
        logging.debug(f"Corresponding email extracted: {corresponding_email}")
    else:
        logging.debug("No corresponding email found.")

    return corresponding_email if corresponding_email else "N/A"
