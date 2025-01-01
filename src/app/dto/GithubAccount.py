from dataclasses import dataclass

@dataclass
class GithubAccount:
    name: str
    url: str
    icon_url: str

    @classmethod
    def from_json(cls, json):
        return cls(
            name=json["display_login"],
            url=json["url"],
            icon_url=json["icon_url"]
        )
