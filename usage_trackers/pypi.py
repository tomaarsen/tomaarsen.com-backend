
from datetime import date
from typing import Dict
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
import pypistats
import json

from usage_trackers.base import Tracker

class PyPITracker(Tracker):
    def merge(self, fetched_data, metadata):
        old_data, old_metadata = self.read()
        data = {**old_data}
        for day, stats in fetched_data.items():
            data[day] = {**old_data.get(day, {}), **stats}
        return {**old_metadata, **(metadata or {}), "data": data}

    def add_empty_days(self, data):
        return data

    @property
    def data_title(self) -> str:
        return "pypi"

    def fetch(self) -> Dict[str, Dict[Literal["downloads"], int]]:
        stats_str = pypistats.overall(self.package_name, mirrors=True, total=True, format="json")
        stats = json.loads(stats_str)["data"]
        # Skip all dates before "2026-05-01"
        stats = [day for day in stats if date.fromisoformat(day["date"]) >= date(2026, 5, 1)]
        # YYYY-MM-DD
        return {
            day["date"]: {"downloads": day["downloads"]}
            for day in stats
        }
