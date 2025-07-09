import requests
import logging
from typing import List, Optional
import xml.etree.ElementTree as ET

def fetch_paper_ids_from_pubmed(query: str, max_results: int = 10) -> List[str]:
    """Fetches a list of PubMed paper IDs based on a search query.

    This function sends a request to the PubMed E-utilities API to search for papers based on the provided query, and returns the list of PubMed IDs for the found papers.

    Args:
        query (str): The search query used to fetch the PubMed papers.
        max_results (int, optional): The maximum number of paper IDs to return. Default is 10. The API returns the top results based on the query.

    Returns:
        List[str]: A list of PubMed paper IDs as strings. If no results are found or an error occurs, an empty list is returned.

    Notes:
        - The function uses the E-utilities API to fetch the data in XML format and parses the XML to extract paper IDs.
        - The `retmax` parameter limits the number of results, and `usehistory` is set to 'y' to support retrieving large result sets.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        'db': 'pubmed',
        'term': query,
        'retmax': max_results,  # Limit the number of results
        'usehistory': 'y',      # Use history for retrieving large result sets
        'retmode': 'xml'
    }

    logging.debug(f"Fetching PubMed IDs for query: {query} with parameters: {params}")

    try:
        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            logging.info(f"Successfully fetched paper IDs for query: {query}")
            
            # Parse the XML response to extract paper IDs
            root = ET.fromstring(response.content)
            
            # Extract the list of paper IDs from the XML response
            id_list = [id_tag.text for id_tag in root.findall(".//Id")]

            logging.debug(f"Fetched {len(id_list)} paper IDs")
            return id_list
        else:
            logging.error(f"Error fetching paper IDs: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        # Log the error if the request fails
        logging.error(f"Request failed: {e}")
        return []


def fetch_xml_data(pubmed_id: str) -> Optional[ET.Element]:
    """ Fetches detailed XML data for a specific PubMed paper based on its PubMed ID.

    This function sends a request to the PubMed E-utilities API to retrieve detailed information about a paper in XML format based on the provided PubMed ID. It returns the XML root element if the request is successful, or `None` if there is an error.

    Args:
        pubmed_id (str): The PubMed ID of the paper to fetch details for.

    Returns:
        Optional[ET.Element]: The root XML element of the paper's detailed data if the request is successful, or `None` if the request fails or no data is found.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        'db': 'pubmed',
        'id': pubmed_id,
        'retmode': 'xml'
    }

    logging.debug(f"Fetching XML data for PubMed ID: {pubmed_id} with parameters: {params}")

    try:
        # Send the request to fetch detailed paper information
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        if response.status_code == 200:
            logging.info(f"Successfully fetched XML data for PubMed ID: {pubmed_id}")
            return ET.fromstring(response.content)  # Return the XML root element
        else:
            logging.error(f"Error fetching paper details for PubMed ID {pubmed_id}: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed for PubMed ID {pubmed_id}: {e}")
        return None