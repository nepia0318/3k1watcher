from dataclasses import dataclass
from multiprocessing import Value

from src.app.dto.search_result import SearchResult


@dataclass
class SearchResults:
    web_search_url: str
    total: int
    results: list[SearchResult]

    @classmethod
    def from_json(cls, json: dict):
        values = []
        for value in json["value"]:
            values.append(SearchResult.from_json(value))
        return cls(
            web_search_url=json["webSearchUrl"],
            total=json["totalEstimatedMatches"],
            results=values
        )
