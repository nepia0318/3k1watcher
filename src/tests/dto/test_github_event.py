import pytest
import textwrap
from datetime import datetime

from src.app.dto.github_event import GithubEvent


class TestGithubEvent:
    @pytest.fixture
    def mock_create_event_json(self) -> dict:
        return {
            "type": "CreateEvent",
            "actor": {
                "display_login": "user1",
                "url": "https://example.com/user1",
                "avatar_url": "https://example.com/user1/avatar_url"
            },
            "repo": {
                "name": "created repository",
                "url": "https://example.com/repo1"
            },
            "created_at": "2024-10-18T02:37:30Z"
        }

    @pytest.fixture
    def mock_push_event_json(self) -> dict:
        return {
            "type": "PushEvent",
            "actor": {
                "display_login": "user1",
                "url": "https://example.com/user1",
                "avatar_url": "https://example.com/user1/avatar_url"
            },
            "repo": {
                "name": "pushed repository",
                "url": "https://example.com/repo1"
            },
            "payload": {
                "commits": [
                    {
                        "message": "commit message1"
                    },
                    {
                        "message": "commit message2"
                    }
                ]
            },
            "created_at": "2024-10-18T02:37:30Z"
        }

    @pytest.fixture
    def mock_fork_event_json(self) -> dict:
        return {
            "type": "ForkEvent",
            "actor": {
                "display_login": "user1",
                "url": "https://example.com/user1",
                "avatar_url": "https://example.com/user1/avatar_url"
            },
            "repo": {
                "name": "original repository",
                "url": "https://example.com/repo1_original"
            },
            "payload": {
                "forkee": {
                    "full_name": "forked repository",
                    "html_url": "https://example.com/repo1"
                }
            },
            "created_at": "2024-10-18T02:37:30Z"
        }

    @pytest.fixture
    def mock_issues_opened_event_json(self) -> dict:
        return {
            "type": "IssuesEvent",
            "actor": {
                "display_login": "user1",
                "url": "https://example.com/user1",
                "avatar_url": "https://example.com/user1/avatar_url"
            },
            "repo": {
                "name": "issue opened repository",
                "url": "https://example.com/repo1"
            },
            "payload": {
                "action": "opened",
                "issue": {
                    "title": "issue1",
                    "html_url": "https://example.com/repo1/issue1"
                }
            },
            "created_at": "2024-10-18T02:37:30Z"
        }

    @pytest.fixture
    def mock_issues_edited_event_json(self) -> dict:
        return {
            "type": "IssuesEvent",
            "actor": {
                "display_login": "user1",
                "url": "https://example.com/user1",
                "avatar_url": "https://example.com/user1/avatar_url"
            },
            "repo": {
                "name": "issue edited repository",
                "url": "https://example.com/repo1"
            },
            "payload": {
                "action": "edited",
                "issue": {
                    "title": "issue1",
                    "html_url": "https://example.com/repo1/issue1"
                }
            },
            "created_at": "2024-10-18T02:37:30Z"
        }

    @pytest.fixture
    def mock_other_event_json(self) -> dict:
        return {
            "type": "OtherEvent",
            "actor": {
                "display_login": "user1",
                "url": "https://example.com/user1",
                "avatar_url": "https://example.com/user1/avatar_url"
            },
            "repo": {
                "name": "other event repository",
                "url": "https://example.com/repo1"
            },
            "created_at": "2024-10-18T02:37:30Z"
        }

    def test_from_json_create_event(self, mock_create_event_json):
        result = GithubEvent.from_json(mock_create_event_json)

        assert result.title == "created repository"
        assert result.url == "https://example.com/repo1"
        assert result.message == textwrap.dedent("""\
            リポジトリを作成しました\
        """).strip()

        assert result.author.name == "user1"
        assert result.author.url == "https://example.com/user1"
        assert result.author.avatar_url == "https://example.com/user1/avatar_url"

        assert result.created_at == datetime(
            year=2024, month=10, day=18, hour=2, minute=37, second=30
        )

    def test_from_json_push_event(self, mock_push_event_json):
        result = GithubEvent.from_json(mock_push_event_json)

        assert result.title == "pushed repository"
        assert result.url == "https://example.com/repo1"
        assert result.message == textwrap.dedent("""\
            2件のcommitをpushしました

            - commit message1,
            - commit message2\
        """).strip()

        assert result.author.name == "user1"
        assert result.author.url == "https://example.com/user1"
        assert result.author.avatar_url == "https://example.com/user1/avatar_url"

        assert result.created_at == datetime(
            year=2024, month=10, day=18, hour=2, minute=37, second=30
        )

    def test_from_json_fork_event(self, mock_fork_event_json):
        result = GithubEvent.from_json(mock_fork_event_json)

        assert result.title == "forked repository"
        assert result.url == "https://example.com/repo1"
        assert result.message == textwrap.dedent("""\
            [original repository](https://example.com/repo1_original)をforkしました\
        """).strip()

        assert result.author.name == "user1"
        assert result.author.url == "https://example.com/user1"
        assert result.author.avatar_url == "https://example.com/user1/avatar_url"

        assert result.created_at == datetime(
            year=2024, month=10, day=18, hour=2, minute=37, second=30
        )

    def test_from_json_issue_opened_event(self, mock_issues_opened_event_json):
        result = GithubEvent.from_json(mock_issues_opened_event_json)

        assert result.title == "issue opened repository"
        assert result.url == "https://example.com/repo1"
        assert result.message == textwrap.dedent("""\
            issueをオープンしました

            - [issue1](https://example.com/repo1/issue1)\
        """).strip()

        assert result.author.name == "user1"
        assert result.author.url == "https://example.com/user1"
        assert result.author.avatar_url == "https://example.com/user1/avatar_url"

        assert result.created_at == datetime(
            year=2024, month=10, day=18, hour=2, minute=37, second=30
        )

    def test_from_json_issue_edited_event(self, mock_issues_edited_event_json):
        result = GithubEvent.from_json(mock_issues_edited_event_json)

        assert result.title == "issue edited repository"
        assert result.url == "https://example.com/repo1"
        assert result.message == textwrap.dedent("""\
            issueを変更しました

            - [issue1](https://example.com/repo1/issue1)\
        """).strip()

        assert result.author.name == "user1"
        assert result.author.url == "https://example.com/user1"
        assert result.author.avatar_url == "https://example.com/user1/avatar_url"

        assert result.created_at == datetime(
            year=2024, month=10, day=18, hour=2, minute=37, second=30
        )

    def test_from_json_other_event(self, mock_other_event_json):
        result = GithubEvent.from_json(mock_other_event_json)

        assert result.title == "other event repository"
        assert result.url == "https://example.com/repo1"
        assert result.message == "OtherEvent"

        assert result.author.name == "user1"
        assert result.author.url == "https://example.com/user1"
        assert result.author.avatar_url == "https://example.com/user1/avatar_url"

        assert result.created_at == datetime(
            year=2024, month=10, day=18, hour=2, minute=37, second=30
        )
