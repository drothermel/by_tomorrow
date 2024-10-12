import logging
import re
from pathlib import Path

import bytom.arxiv_utils as xu

# --- Info Gathering Functions --- #


def get_author_papers(author, kwargs={}):
    logging.info(f">> Getting papers from arxiv api for author: {author}")
    # First get all the recent papers by this author, ordered by date
    query = xu.build_author_query(author, kwargs=kwargs)
    entries = xu.query_api(query)

    logging.info(f">> Total number papers: {len(entries)}")
    structured_responses = [xu.parse_paper_entry(pent) for pent in entries]
    return structured_responses


# --- Data Inspect Functions --- #


def list_authors_with_summaries(cfg, version=None):
    if version is not None:
        assert False, "version specification isn't defined  yet"

    profs = set()
    author_data_path = Path(cfg.author_summaries_dir)
    for fn in author_data_path.iterdir():
        rmatch = re.match(cfg.author_summary_file_pattern, fn.stem)
        profs.add(rmatch.group("professor_name").replace("_", " ").title())
    return list(profs)
