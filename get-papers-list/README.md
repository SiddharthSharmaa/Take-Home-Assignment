
# get-papers-list

`get-papers-list` is a Python CLI tool to fetch research papers from PubMed based on a user query, and identify papers with at least one author affiliated with a pharmaceutical or biotech company.

## Features
- Search PubMed for research papers using a custom query
- Filter papers to include only those with at least one author from a pharmaceutical or biotech company
- Save results to a CSV file
- Optionally enable debug logging

## Installation
1. Clone this repository.
2. Ensure you have Python 3.12 or higher installed.
3. Install dependencies using [Poetry](https://python-poetry.org/):
   ```sh
   poetry install
   ```

## Usage
Run the CLI tool using Poetry:

```sh
poetry run get-papers-list "your pubmed query here" [-f output.csv] [--debug]
```

**Arguments:**
- `query` (str): Query to search on PubMed (required)
- `-f, --file` (str): Filename to save results as CSV (optional)
- `-d, --debug`: Enable debug mode (optional)

**Example:**
```sh
poetry run get-papers-list "machine learning brain" -f results.csv --debug
```

## Project Structure
```
get-papers-list/
├── src/get_papers_list/
│   ├── cli.py
│   ├── processor.py
│   ├── pubmed_fetcher.py
│   ├── metadata_extractor.py
│   ├── filters.py
│   ├── filters_llms.py
│   ├── utils.py
│   └── __init__.py
├── tests/
│   └── __init__.py
├── pyproject.toml
├── poetry.lock
└── README.md
```

## Dependencies
- click
- python-dotenv
- requests

## License
MIT License (add your license here if different)
