import textwrap
from dataclasses import dataclass


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str

    @classmethod
    def from_json(cls, json: dict):
        return cls(
            title=json["title"],
            url=json["link"],
            snippet=textwrap.dedent(f"""\
                {json["snippet"]}\
            """).strip()
        )
