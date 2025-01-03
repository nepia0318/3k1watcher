import textwrap
from dataclasses import dataclass
from datetime import datetime

from .github_account import GithubAccount


@dataclass
class GithubEvent:
    title: str = ""
    url: str = ""
    message: str = ""
    author: GithubAccount = None
    created_at: datetime = None

    @classmethod
    def from_json(cls, json: dict):
        event = GithubEvent()
        match json["type"]:
            case "CreateEvent":
                event.parse_github_create_event(json)
            case "PushEvent":
                event.parse_github_push_event(json)
            case "ForkEvent":
                event.parse_github_fork_event(json)
                pass
            case "IssuesEvent":
                event.parse_github_issues_event(json)
                pass
            case _:
                event.parse_github_other_event(json)
                pass

        event.author = GithubAccount.from_json(json["actor"])
        event.created_at = datetime.strptime(json["created_at"], "%Y-%m-%dT%H:%M:%SZ")

        return event

    def get_html_url_from_api_url(self, url) -> str:
        return url.replace("api.github.com", "github.com").replace("/repos/", "/")

    def parse_github_create_event(self, json) -> None:
        self.title = json["repo"]["name"]
        self.url = self.get_html_url_from_api_url(json["repo"]["url"])
        self.message = textwrap.dedent("""\
            リポジトリを作成しました\
        """).strip()

    def parse_github_push_event(self, json) -> None:
        commits_num = len(json["payload"]["commits"])
        commits_string = ""
        for commit in json["payload"]["commits"]:
            commits_string += f"- {commit["message"]},\n"
        commits_string = commits_string[:-2]

        self.title = json["repo"]["name"]
        self.url = self.get_html_url_from_api_url(json["repo"]["url"])
        self.message = textwrap.dedent(f"""\
            {commits_num}件のcommitをpushしました
            \n{commits_string}\
        """).strip()

    def parse_github_fork_event(self, json) -> None:
        self.title = json["payload"]["forkee"]["full_name"]
        self.url = json["payload"]["forkee"]["html_url"]
        self.message = textwrap.dedent(f"""\
            [{json["repo"]["name"]}]({self.get_html_url_from_api_url(json["repo"]["url"])})をforkしました\
        """).strip()

    def parse_github_issues_event(self, json) -> None:
        ACTIONS = {
            "opened": "オープン",
            "edited": "変更",
            "reopend": "再オープン",
            "assigned": "アサイン",
            "unassigned": "アサイン解除",
            "labeled": "ラベル付与",
            "unlabeled": "ラベル削除"
        }

        self.title = json["repo"]["name"]
        self.url = self.get_html_url_from_api_url(json["repo"]["url"])
        self.message = textwrap.dedent(f"""\
            issueを{ACTIONS[json["payload"]["action"]]}しました

            - [{json["payload"]["issue"]["title"]}]({json["payload"]["issue"]["html_url"]})
        """).strip()

    def parse_github_other_event(self, json) -> None:
        self.title = json["repo"]["name"]
        self.url = self.get_html_url_from_api_url(json["repo"]["url"])
        self.message = json["type"]
