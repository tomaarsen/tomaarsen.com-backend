
from typing import Dict
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
import pypistats
import json

from usage_trackers.base import Tracker

class PyPITracker(Tracker):
    @property
    def data_title(self) -> str:
        return "pypi"

    def fetch(self) -> Dict[str, Dict[Literal["downloads"], int]]:
        stats_str = pypistats.overall(self.package_name, mirrors=True, total=True, format="json")
        stats = json.loads(stats_str)["data"]
        # YYYY-MM-DD
        return {
            day["date"]: {"downloads": day["downloads"]}
            for day in stats
        }
