# utils.py

import logging
import csv
from typing import List, Dict

def setup_logging(debug: bool = False) -> None:
    """Configures the logging settings for the application.

    This function sets the logging level based on the `debug` flag. 
    If `debug` is True, the logging level is set to DEBUG for verbose output. 
    Otherwise, it is set to INFO for standard informational messages.

    Args:
        debug (bool): Flag to enable verbose logging. Default is False.
    """
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)

def save_paper_details_to_csv(papers: List[Dict[str, str]], filename: str) -> None:
    """Saves a list of paper detail dictionaries to a CSV file.

    This function writes the data of all paper dictionaries into a CSV file, 
    with the first row as headers and the subsequent rows as paper details.

    Args:
        papers (List[Dict[str, str]]): A list of dictionaries, where each dictionary contains the details of a paper.
        filename (str): The name of the CSV file to write to.
    """
    if not papers:
        return
    keys = papers[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(papers)