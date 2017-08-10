from fetch_local import FetchLocal
from fetch_http import FetchHttp
from fetch_git import FetchGit

FETCH_CLASS = {
    "FetchLocal": FetchLocal,
    "FetchHttp": FetchHttp,
    "FetchGit": FetchGit
}
__all__ = ["FetchLocal", "FetchHttp", "FetchGit"]
