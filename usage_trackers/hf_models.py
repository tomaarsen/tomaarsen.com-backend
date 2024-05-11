from collections import defaultdict
from typing import Any, Dict, Tuple, Union

from usage_trackers.base import DATE_TIME_FMT, DATE_FMT, Tracker
from huggingface_hub import HfApi, ModelFilter
from datetime import datetime


class HfHubTracker(Tracker):
    def __init__(self, package_name: str) -> None:
        super().__init__(package_name)
        self.api = HfApi()

    @property
    def data_title(self) -> str:
        return "hf_models"

    def fetch(
        self,
    ) -> Union[
        Dict[str, Dict[str, Any]], Tuple[Dict[str, Dict[str, Any]], Dict[str, Any]]
    ]:
        data = defaultdict(lambda: {"models": 0})
        last_date_time = None
        for model in self.api.list_models(
            filter=ModelFilter(library=self.package_name.replace("_", "-"))
        ):
            if self.package_name == "sentence-transformers" and "setfit" in model.tags:
                # Skip setfit models for sentence-transformers
                continue
            # The MongoDB ObjectId is created when the Model on the Hub is created,
            # and you can extract the datetime from it
            mongo_db_object_id = model._id
            created_at = datetime.fromtimestamp(int(mongo_db_object_id[:8], 16))
            date = created_at.strftime(DATE_FMT)
            if date == "2022-03-02" and self.package_name == "sentence-transformers":
                # Skip this particular date for sentence-transformers.
                # This approach lists 379 models there, but these are models from before this date,
                # that are also included in the data.
                continue
            if self.package_name == "sentence-transformers" and model.author == "danfeg" and date in ("2024-03-22", "2024-03-23", "2024-03-24"):
                # Skip "danfeg" sentence-transformer models, as he uploaded ~242 models in one day
                # and it's a big outlier in our data.
                continue
            if self.package_name == "sentence-transformers" and model.author == "josejointriple" and date in ("2024-05-07"):
                # Skip "josejointriple" sentence-transformer models, as he uploaded ~55 models in one day
                # and it's a big outlier in our data.
                continue
            data[date]["models"] += 1

            last_date_time = (
                created_at
                if last_date_time is None
                else max(last_date_time, created_at)
            )
        return data, {"last_datetime": last_date_time.strftime(DATE_TIME_FMT)}
