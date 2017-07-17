from github_repository_control import GithubRepositoryControl
from local_repository_control import LocalRepositoryControl

# dict of core repository controllers packaged with linchpin

REPOSITORY_CONTROL = {
    "github" : GithubRepositoryControl,
    "local" : LocalRepositoryControl
}
