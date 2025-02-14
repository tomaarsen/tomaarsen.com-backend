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
        data = defaultdict(lambda: defaultdict(lambda: 0))
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
            if date in ("2022-03-02", "2022-03-03") and self.package_name == "sentence-transformers":
                # Skip this particular date for sentence-transformers.
                # This approach lists 379 models there, but these are models from before this date,
                # that are also included in the data.
                continue
            if self.package_name == "sentence-transformers":
                if model.author == "tomaarsen":
                    # Skip myself to prevent bias
                    continue
                if model.author == "fine-tuned":
                    # Jina's "fine-tuned" models are spamming models
                    continue
                if model.author == "ILKT" and model.modelId.startswith("ILKT/2024"):
                    # ILKT has uploaded a lot of models that are just e.g. "ILKT/2024-06-24_22-31-28_epoch_35",
                    # let's ignore those
                    continue
            data[date][model.author] += 1

            last_date_time = (
                created_at
                if last_date_time is None
                else max(last_date_time, created_at)
            )
        data = {
            date: {"models": sum(min(models, 3) for models in models_authors.values())}
            for date, models_authors in data.items()
        }
        return data, {"last_datetime": last_date_time.strftime(DATE_TIME_FMT)}
