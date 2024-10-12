from enum import Enum
from datetime import datetime
import logging
import re
from pathlib import Path
import io

import dr_util.file_utils as fu

import bytom.arxiv_utils as xu


class SUMMARY_SOURCE(Enum):
    ABSTRACT = 1
    # NO_APPENDIX = 2
    # FULL_PDF = 3


class SUMMARY_FORMAT(Enum):
    MARKDOWN = 1
    # JSON = 2


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


# --- Profile Writing Functions --- #


def format_response_abstract_to_markdown(response):
    buff = io.StringIO()

    buff.write(f"### **Title:** {response['title']}\n\n")
    buff.write(f"**Publish Date:** {response['published']}\n\n")
    buff.write(f"**First Author:** {response['authors'][0]}\n\n")
    buff.write(f"**Last Author:** {response['authors'][-1]}\n\n")
    if len(response["authors"]) > 2:
        buff.write(f"**Middle Authors:** {', '.join(response['authors'][1:-1])}\n\n")
    buff.write(f"**Abstract:** {response['abstract']}\n\n")
    buff.write(f'{"-"*15}\n\n\n')
    return buff.getvalue()


def make_author_page(
    cfg, author, responses=None, author_info=None, max_papers=100, max_years=20
):
    if author_info is None:
        author_infos = fu.load_file(cfg.author_info_file)
        author_info = author_infos[author]

    if responses is None:
        responses = get_author_papers(author, kwargs={"max_results": max_papers})
    else:
        responses = responses[:max_papers]

    buff = io.StringIO()
    buff.write(f"# Research Summary for **{author}**\n\n")
    buff.write(f"## {author} Bio\n\n")
    buff.write(f"{author_info}\n\n")

    buff.write("## Recent Papers\n\n")
    for resp in responses:
        published = datetime.strptime(resp["published"], "%Y-%m-%d")
        if (datetime.now() - published).days / 365.25 < max_years:
            buff.write(format_response_abstract_to_markdown(resp))
    return buff.getvalue()


def write_author_page(
    cfg, author, version, responses=None, author_info=None, max_papers=100, max_years=20
):
    author_page = make_author_page(
        cfg,
        author,
        responses=responses,
        author_info=author_info,
        max_papers=max_papers,
        max_years=max_years,
    )
    author_str = author.lower().replace(" ", "_")
    fu.dump_file(
        author_page,
        f"{cfg.author_summaries_dir}{author_str}.markdown."
        f"v{version}.maxp{max_papers}.maxy{max_years}.txt",
    )
