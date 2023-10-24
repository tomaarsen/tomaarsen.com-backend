
from abc import ABC, abstractmethod, abstractproperty
import json
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

DATE_TIME_FMT = r"%Y-%m-%dT%H:%M:%SZ"
DATE_FMT = r"%Y-%m-%d"


class Tracker(ABC):
    def __init__(self, package_name: str) -> None:
        self.package_name = package_name
        self.storage_path = Path() / "app" / "static" / "data" / "usage_trackers" / package_name / f"{self.data_title}.json"

    @abstractproperty
    @property
    def data_title(self) -> str:
        pass

    @abstractmethod
    def fetch(self) -> Union[Dict[str, Dict[str, Any]], Tuple[Dict[str, Dict[str, Any]], Dict[str, Any]]]:
        """
        Must return a dict with the "YYYY-MM-DD" date as the key to a dictionary with stats, e.g.
        {
            '2023-09-16': {'downloads': 2295},
            ...
        }
        and optionally some metadata
        """

    def merge(self, fetched_data: Dict[str, Dict[str, int]], metadata: Optional[Dict[str, Any]]) -> Dict[str, Dict[str, int]]:
        old_data, old_metadata = self.read()

        return {
            **old_metadata,
            **(metadata or {}),
            "data": {**old_data, **fetched_data},
        }

    def read(self) -> Tuple[Dict[str, Dict[str, Any]], Dict[str, Any]]:
        """Returns a data-metadata tuple of dictionaries"""
        if not self.storage_path.exists():
            return {}, {}

        with open(self.storage_path, "r", encoding="utf8") as f:
            full_data = json.load(f)
            return full_data.pop("data"), full_data

    def write(self, merged_data: Dict[str, Dict[str, int]]) -> None:
        if not self.storage_path.parent.exists():
            self.storage_path.parent.mkdir(parents=True)
        
        with open(self.storage_path, "w", encoding="utf8") as f:
            json.dump(merged_data, f, indent=4)

    def __call__(self) -> None:
        fetched_data = self.fetch()
        metadata = None
        if isinstance(fetched_data, tuple):
            fetched_data, metadata = fetched_data
        full_data = self.merge(fetched_data, metadata)
        # Sort data by date
        full_data["data"] = dict(sorted(full_data["data"].items()))
        self.write(full_data)