import logging

import bytom.arxiv_utils as xu


# logging.basicConfig(level=logging.INFO)
def get_author_papers(author, kwargs={}):
    logging.info(f">> Getting papers from arxiv api for author: {author}")
    # First get all the recent papers by this author, ordered by date
    query = xu.build_author_query(author, kwargs=kwargs)
    entries = xu.query_api(query)

    logging.info(f">> Total number papers: {len(entries)}")
    structured_responses = [xu.parse_paper_entry(pent) for pent in entries]
    return structured_responses
