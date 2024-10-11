from enum import Enum
import feedparser

# ---- Constants ---- #

API_URL = "https://export.arxiv.org/api/query"


class QUERY_TYPES(str, Enum):
    ID = "id_list"
    SEARCH = "search_query"

    def __str__(self) -> str:
        return str.__str__(self)


# ---- Query Utils ---- #


def build_id_query(id_list, kwargs={}):
    query_str = ",".join(id_list)
    arg_strs = [f"{k}={v}" for k, v in kwargs.items()]
    query_str = f"{API_URL}?{QUERY_TYPES.ID}={query_str}"
    return "&".join([query_str, *arg_strs])


def build_author_query(author, kwargs={}):
    sanitized_author = author.replace(" ", "%20")
    query_str = f'{API_URL}?{QUERY_TYPES.SEARCH}=au:"{sanitized_author}"'
    all_kwargs = {
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        **kwargs,
    }
    kwarg_strs = [f"{k}={v}" for k, v in all_kwargs.items()]
    return "&".join([query_str, *kwarg_strs])


def query_api(query_str):
    parsed_feed = feedparser.parse(query_str)
    return parsed_feed["entries"]


# ---- Parsing Utils ---- #


def parse_paper_entry(p_feed):
    pdf_link = None
    for ldict in p_feed["links"]:
        if ldict.get("title", "") == "pdf":
            pdf_link = ldict["href"]
    return {
        "title": p_feed["title"],
        "abstract": p_feed["summary"],
        "published": p_feed["published"],
        "updated": p_feed["updated"],
        "authors": [a["name"] for a in p_feed["authors"]],
        "pdf_link": pdf_link,
    }
