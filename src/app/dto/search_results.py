from dataclasses import dataclass, field
from typing import Self

from src.app.dto.search_result import SearchResult


@dataclass
class SearchResults:
    web_search_url: str = ""
    total: int = 0
    items: list[SearchResult] = field(default_factory=list)

    @classmethod
    def from_json(cls, json: dict) -> Self:
        values = []
        for value in json["value"]:
            values.append(SearchResult.from_json(value))
        return cls(
            web_search_url=json["webSearchUrl"],
            total=json["totalEstimatedMatches"],
            items=values
        )
