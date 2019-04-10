from .fetch_http import FetchHttp
from .fetch_git import FetchGit

FETCH_CLASS = {
    "FetchHttp": FetchHttp,
    "FetchGit": FetchGit
}
__all__ = ["FetchHttp", "FetchGit"]
