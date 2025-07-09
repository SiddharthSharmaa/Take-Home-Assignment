import argparse
import logging
from .processor import fetch_all_papers
from .utils import setup_logging, save_paper_details_to_csv

def main():
    parser = argparse.ArgumentParser(
        description="Fetch and analyze PubMed articles with pharma/biotech affiliation filtering."
    )
    parser.add_argument("query", type=str, help="Query to search on PubMed")
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable debug mode"
    )
    parser.add_argument(
        "-f", "--file", type=str, help="Filename to save results as CSV"
    )

    args = parser.parse_args()

    # Setup logging
    setup_logging(debug=args.debug)
    logging.debug(f"Arguments: {args}")

    # Fetch and process papers
    try:
        logging.info(f"Fetching papers for query: {args.query}")
        papers = fetch_all_papers(args.query, debug=args.debug)
        logging.info(f"Found {len(papers)} relevant papers.")

        if args.file:
            save_paper_details_to_csv(papers, args.file)
            logging.info(f"Results saved to {args.file}")
        else:
            for paper in papers:
                print(paper)

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()