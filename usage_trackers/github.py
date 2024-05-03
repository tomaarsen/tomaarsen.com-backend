from collections import defaultdict
from datetime import datetime
import os
from typing import Any, Dict, Optional, Tuple
from ghapi.all import GhApi, paged
from usage_trackers.base import DATE_TIME_FMT, Tracker
from abc import abstractproperty


class GitHubTracker(Tracker):
    def __init__(self, package_name: str, owner: str, repo: str) -> None:
        super().__init__(package_name)
        self.owner = owner
        self.repo = repo

        def limit_remaining_callback(rem, quota) -> None:
            print(
                f"Quota remaining for {self.data_title}, {package_name}: {rem} of {quota}"
            )

        self.api = GhApi(
            owner=owner,
            repo=repo,
            token=os.environ.get("GITHUB_TOKEN"),
            limit_cb=limit_remaining_callback,
        )

    @abstractproperty
    @property
    def data_keys(self) -> Tuple[str]:
        pass

    @abstractproperty
    @property
    def data_generator(self):
        pass

    def merge(
        self,
        fetched_data: Dict[str, Dict[str, int]],
        metadata: Optional[Dict[str, Any]],
    ) -> Dict[str, Dict[str, int]]:
        old_data, _ = self.read()

        dates = set(old_data.keys()) | set(fetched_data.keys())
        data = {}
        for date in dates:
            data[date] = {key: 0 for key in self.data_keys}
            if date in old_data:
                for key in self.data_keys:
                    data[date][key] += old_data[date][key]
            if date in fetched_data:
                for key in self.data_keys:
                    data[date][key] += fetched_data[date][key]
        return {"data": data, **metadata}

    def fetch(self) -> Dict[str, Dict[str, int]]:
        # Read the original metadata
        _, metadata = self.read()
        self.since = metadata.get("last_datetime", None)

        data = defaultdict(lambda: {key: 0 for key in self.data_keys})

        last_date_time = (
            datetime.strptime(self.since, DATE_TIME_FMT) if self.since else None
        )
        for pages in self.data_generator:
            for element in pages:
                date_time = self.element_handler(element, data)
                last_date_time = (
                    max(date_time, last_date_time) if last_date_time else date_time
                )

        return dict(data), {"last_datetime": last_date_time.strftime(DATE_TIME_FMT)}


class GitHubStarTracker(GitHubTracker):
    def __init__(self, package_name: str, owner: str, repo: str) -> None:
        super().__init__(package_name, owner, repo)
        # This header causes the "starred_at" value to be provided
        self.api.headers = {"Accept": "application/vnd.github.star+json"}

    def fetch(self) -> Dict[str, Dict[str, int]]:
        # Read the original metadata
        _, metadata = self.read()
        old_last_page = metadata.get("last_page", 1)
        old_last_datetime = metadata.get("last_datetime", None)

        per_page = 100
        stars_per_day = defaultdict(lambda: {"stars": 0})
        last_page = old_last_page
        date_time = old_last_datetime

        while last_page == old_last_page or stargazers:
            try:
                stargazers = self.api.activity.list_stargazers_for_repo(
                    per_page=per_page, page=last_page
                )
            except:
                # If it fails, e.g. due to rate limit, then just leave it and store what you did fetch
                break
            if not stargazers:
                last_page -= 1
                break

            for stargazer in stargazers:
                date_time = stargazer["starred_at"]
                if old_last_datetime is None or datetime.strptime(
                    date_time, DATE_TIME_FMT
                ) > datetime.strptime(old_last_datetime, DATE_TIME_FMT):
                    # YYYY-MM-DD
                    date = date_time[:10]
                    stars_per_day[date]["stars"] += 1

            if len(stargazers) != per_page:
                break

            last_page += 1

        return dict(stars_per_day), {"last_page": last_page, "last_datetime": date_time}

    @property
    def data_generator(self):
        pass

    @property
    def data_title(self) -> str:
        return "github_stars"

    @property
    def data_keys(self) -> Tuple[str]:
        return ("stars",)


class GitHubIssueTracker(GitHubTracker):
    @property
    def data_generator(self):
        kwargs = {"per_page": 100, "state": "all"}
        if self.since:
            kwargs["since"] = self.since
        return paged(self.api.issues.list_for_repo, **kwargs)

    def element_handler(
        self, element: Dict[str, Any], data: Dict[str, Dict[str, int]]
    ) -> None:
        created_at = element["created_at"]
        date = created_at[:10]
        if self.since is None or datetime.strptime(
            created_at, DATE_TIME_FMT
        ) > datetime.strptime(self.since, DATE_TIME_FMT):
            if "pull_request" in element:
                data[date]["opened_prs"] += 1
            else:
                data[date]["opened_issues"] += 1
        if element["closed_at"]:
            closed_at = element["closed_at"]
            date = closed_at[:10]
            if self.since is None or datetime.strptime(
                closed_at, DATE_TIME_FMT
            ) > datetime.strptime(self.since, DATE_TIME_FMT):
                if "pull_request" in element:
                    data[date]["closed_prs"] += 1
                else:
                    data[date]["closed_issues"] += 1
        return datetime.strptime(element["updated_at"], DATE_TIME_FMT)

    @property
    def data_title(self) -> str:
        return "github_issues"

    @property
    def data_keys(self) -> Tuple[str]:
        return ("opened_prs", "opened_issues", "closed_prs", "closed_issues")


class GitHubCommentTracker(GitHubTracker):
    @property
    def data_generator(self):
        kwargs = {"per_page": 100, "state": "all"}
        if self.since:
            kwargs["since"] = self.since
        for pages in paged(self.api.issues.list_comments_for_repo, **kwargs):
            yield [page for page in pages if page["created_at"] != self.since]

    def element_handler(
        self, element: Dict[str, Any], data: Dict[str, Dict[str, int]]
    ) -> None:
        date_time = element["created_at"]
        date = date_time[:10]
        if element["user"]["login"] != "tomaarsen":
            data[date]["comments_without_me"] += 1
        data[date]["comments"] += 1
        return datetime.strptime(date_time, DATE_TIME_FMT)

    @property
    def data_title(self) -> str:
        return "github_comments"

    @property
    def data_keys(self) -> Tuple[str]:
        return ("comments", "comments_without_me")
