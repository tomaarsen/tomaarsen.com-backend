
from .base import Tracker
from .pypi import PyPITracker
from .hf_models import HfHubTracker
from .github import GitHubCommentTracker, GitHubIssueTracker, GitHubStarTracker

PACKAGES = [
    ("span_marker", "tomaarsen", "SpanMarkerNER"),
    ("setfit", "huggingface", "setfit"),
    ("sentence-transformers", "UKPLab", "sentence-transformers"),
]
TRACKERS = [
    lambda package_name, owner, repo: GitHubStarTracker(package_name, owner, repo),
    lambda package_name, owner, repo: GitHubIssueTracker(package_name, owner, repo),
    lambda package_name, owner, repo: GitHubCommentTracker(package_name, owner, repo),
    lambda package_name, owner, repo: PyPITracker(package_name),
    lambda package_name, owner, repo: HfHubTracker(package_name),
]

def run_all():
    for tracker in TRACKERS:
        for package in PACKAGES:
            tracker(*package)()
