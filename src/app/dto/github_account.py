from dataclasses import dataclass

@dataclass
class GithubAccount:
    name: str
    url: str
    avatar_url: str

    @classmethod
    def from_json(cls, json: dict):
        return cls(
            name=json["display_login"],
            url=json["url"],
            avatar_url=json["avatar_url"]
        )
