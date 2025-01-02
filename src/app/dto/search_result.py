import re
from datetime import datetime
from dataclasses import dataclass


@dataclass
class SearchResult:
    title: str = ""
    url: str = ""
    snippet: str = ""
    last_crawled: datetime = None

    @classmethod
    def from_json(cls, json: dict):
        time_str = re.compile(r"\.[0-9]{7}Z").sub("Z", json["dateLastCrawled"])
        return cls(
            title=json["name"],
            url=json["url"],
            snippet=json["snippet"],
            last_crawled=datetime.strptime(
                time_str,
                "%Y-%m-%dT%H:%M:%SZ"
            )
        )
