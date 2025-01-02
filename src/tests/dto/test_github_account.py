import pytest

from src.app.dto.github_account import GithubAccount
class TestGithubAccount:
    @pytest.fixture
    def mock_json(self) -> dict:
        return {
            "display_login" : "user1",
            "url" : "https://example.com/user1",
            "avatar_url": "https://example.com/user1/avatar_url"
        }

    def test_from_json(self, mock_json):
        result = GithubAccount.from_json(mock_json)

        assert result.name == "user1"
        assert result.url == "https://example.com/user1"
        assert result.avatar_url == "https://example.com/user1/avatar_url"
