from typing import Dict, Any
from .pubmed_fetcher import fetch_paper_ids_from_pubmed, fetch_xml_data
from .metadata_extractor import *
from .filters import *

# Main function to orchestrate the extraction
def fetch_paper_details(pubmed_id: str) -> Dict[str, Any]:
    """Orchestrates the extraction of paper details from PubMed using a provided PubMed ID.

    This function coordinates the extraction of various paper details such as PubMed ID, title, 
    publication date, authors, company affiliations (pharma/biotech), and the corresponding author's email. 
    It fetches XML data from PubMed, processes it, and returns the extracted details in a dictionary.

    Args:
        pubmed_id (str): The PubMed ID for the paper whose details are to be fetched.

    Returns:
        Dict[str, Any]: A dictionary containing the extracted paper details. The dictionary includes:
            - "PubMedID": The PubMed ID of the paper.
            - "Title": The title of the paper.
            - "PublicationDate": The publication date of the paper in "YYYY-MM-DD" format.
            - "Authors": A list of authors of the paper who are affiliated with non-academic institutions.
            - "CompanyAffiliations": A set of pharma/biotech company affiliations (non-academic).
            - "CorrespondingAuthorEmail": The email of the corresponding author, if available.

    Notes:
        - The function returns an empty dictionary if any error occurs during the extraction process.
        - The function relies on helper functions like `get_pubmed_id`, `get_title`, `get_publication_date`, 
          `get_authors`, `get_pharma_biotech_affiliations`, and `get_corresponding_email` to extract specific details.
    """
    logging.debug(f"Starting to fetch paper details for PubMed ID: {pubmed_id}")

    # Get XML data from PubMed
    root = fetch_xml_data(pubmed_id)
    
    if root is None:
        logging.error(f"Failed to fetch XML data for PubMed ID: {pubmed_id}")
        return {}

    paper_details = {}
    
    try:
        # Extracting paper details
        paper_details['PubMedID'] = get_pubmed_id(root, pubmed_id)
        logging.debug(f"PubMed ID: {paper_details['PubMedID']} extracted.")
        
        paper_details['Title'] = get_title(root)
        logging.debug(f"Title: {paper_details['Title']} extracted.")
        
        paper_details['PublicationDate'] = get_publication_date(root)
        logging.debug(f"Publication Date: {paper_details['PublicationDate']} extracted.")
        
        paper_details['Authors'] = get_authors(root, academic_keywords)
        logging.debug(f"Authors: {paper_details['Authors']} extracted.")
        
        paper_details['CompanyAffiliations'] = get_pharma_biotech_affiliations(root, pharma_biotech_keywords, academic_keywords)
        logging.debug(f"Company Affiliations: {paper_details['CompanyAffiliations']} extracted.")
        
        paper_details['CorrespondingAuthorEmail'] = get_corresponding_email(root, academic_keywords)
        logging.debug(f"Corresponding Author Email: {paper_details['CorrespondingAuthorEmail']} extracted.")
        
    except Exception as e:
        logging.error(f"Error occurred while fetching paper details for PubMed ID {pubmed_id}: {e}")
        return {}

    logging.info(f"Successfully fetched paper details for PubMed ID: {pubmed_id}")
    return paper_details


# Function to fetch all paper details based on a query
def fetch_all_papers(query: str, max_results: int = 10, debug: bool = False) -> List[Dict[str, Any]]:
    """Fetches details of multiple papers from PubMed based on a query.

    This function retrieves a list of paper IDs from PubMed using the provided search query, then fetches detailed information 
    (such as title, authors, publication date, etc.) for each paper. The function returns the paper details in a list of dictionaries.

    Args:
        query (str): The search query to be used to fetch paper IDs from PubMed.
        max_results (int, optional): The maximum number of papers to fetch (default is 10). 
        debug (bool, optional): If set to True, logging level is set to DEBUG for detailed output. Default is False.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing the details for each paper. Each dictionary includes:
            - 'PubMedID': The PubMed ID of the paper.
            - 'Title': The title of the paper.
            - 'PublicationDate': The publication date of the paper in "YYYY-MM-DD" format.
            - 'Authors': A list of authors of the paper who are affiliated with non-academic institutions.
            - 'CompanyAffiliations': A set of pharma/biotech company affiliations (non-academic).
            - 'CorrespondingAuthorEmail': The email of the corresponding author, if available.

    Notes:
        - If no paper IDs are found, the function returns an empty list.
        - The function fetches paper details using `fetch_paper_details` for each paper ID.
        - Logging level is set to `DEBUG` if `debug=True` for detailed logs.
        - The number of paper results is limited by `max_results`.
    """
    # Set logging level based on the debug flag
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    logging.debug(f"Starting to fetch papers for query: {query}")
    
    # Fetch the paper IDs
    paper_ids = fetch_paper_ids_from_pubmed(query, max_results)
    
    if not paper_ids:
        logging.warning(f"No paper IDs found for query: {query}")
        return []
    
    logging.debug(f"Fetched {len(paper_ids)} paper IDs for query: {query}")

    # Fetch the details for each paper using the paper IDs
    all_paper_details = []
    for pubmed_id in paper_ids:
        logging.debug(f"Fetching details for PubMed ID: {pubmed_id}")
        paper_details = fetch_paper_details(pubmed_id)
        
        if paper_details:
            all_paper_details.append(paper_details)
            logging.debug(f"Successfully fetched details for PubMed ID: {pubmed_id}")
        else:
            logging.error(f"Failed to fetch details for PubMed ID: {pubmed_id}")
    
    logging.info(f"Successfully fetched details for {len(all_paper_details)} papers out of {len(paper_ids)} paper IDs.")
    
    return all_paper_details