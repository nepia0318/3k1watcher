from unittest.mock import MagicMock
import pytest
import discord
from datetime import datetime
from pytest_mock import MockerFixture

from src.app.views.discord_view import DiscordView
from src.app.dto.search_results import SearchResults
from src.app.dto.search_result import SearchResult
from src.app.dto.github_event import GithubEvent, GithubAccount


class TestDiscordView:
    @pytest.fixture
    def discord_view(self) -> DiscordView:
        from src.app.views.discord_view import DiscordView
        return DiscordView()

    @pytest.fixture
    def mock_ctx(self, mocker: MockerFixture) -> MagicMock:
        mocked = mocker.MagicMock()
        mocked.send = mocker.AsyncMock()
        return mocked

    @pytest.fixture
    def mock_search_results(self) -> SearchResults:
        return SearchResults(
            web_search_url="https://example.com/search?q=3k1",
            total=2,
            items=[
                SearchResult(
                    title="title1",
                    url="https://example.com/article1",
                    snippet="description1"
                ),
                SearchResult(
                    title="title2",
                    url="https://example.com/article2",
                    snippet="description2"
                )
            ]
        )

    @pytest.fixture
    def mock_github_events(self) -> list[GithubEvent]:
        return [
            GithubEvent(
                title="title1",
                url="https://example.com/repo1",
                message="description1",
                author=GithubAccount(
                    name="user1",
                    url="https://example.com/user/user1",
                    avatar_url="https://example.com/user/user1/avatar"),
                created_at=datetime(
                    year=2025, month=1, day=2, hour=14, minute=0, second=0
                )
            ),
            GithubEvent(
                title="title2",
                url="https://example.com/repo2",
                message="description2",
                author=GithubAccount(
                    name="user2",
                    url="https://example.com/user/user2",
                    avatar_url="https://example.com/user/user2/avatar"),
                created_at=datetime(
                    year=1919, month=9, day=29, hour=12, minute=15, second=40
                )
            )
        ]

    @pytest.mark.asyncio
    async def test_send_search_results_success(
        self, mocker: MockerFixture, discord_view,
            mock_ctx, mock_search_results):
        await discord_view.send_search_results(mock_ctx, mock_search_results)
        print(f"total_test: {mock_search_results.total}")
        mock_ctx.send.assert_any_call("まん３に関する検索結果が2件ヒットしました")

        calls = mock_ctx.send.call_args_list
        assert len(calls) == 3

        embed_call1 = calls[1].kwargs["embed"]
        assert isinstance(embed_call1, discord.Embed)
        assert embed_call1.title == "title1"
        assert embed_call1.url == "https://example.com/article1"
        assert embed_call1.description == "description1"

        embed_call2 = calls[2].kwargs["embed"]
        assert isinstance(embed_call2, discord.Embed)
        assert embed_call2.title == "title2"
        assert embed_call2.url == "https://example.com/article2"
        assert embed_call2.description == "description2"

    @pytest.mark.asyncio
    async def test_send_search_results_error(self, mocker: MockerFixture, discord_view, mock_ctx):
        mock_ctx.send.side_effect = Exception("View error.")

        with pytest.raises(Exception):
            await discord_view.send_search_results(mock_ctx, [])

        mock_ctx.send.assert_called_with("取得に失敗しました")

    @pytest.mark.asyncio
    async def test_send_github_activities_success(self, mocker: MockerFixture, discord_view, mock_ctx, mock_github_events):
        await discord_view.send_github_activities(mock_ctx, mock_github_events)
        mock_ctx.send.assert_any_call("まん３のGitHubアクティビティが2件ヒットしました")

        calls = mock_ctx.send.call_args_list
        assert len(calls) == 3

        embed_call1 = calls[1].kwargs["embed"]
        assert isinstance(embed_call1, discord.Embed)
        assert embed_call1.title == "title1"
        assert embed_call1.url == "https://example.com/repo1"
        assert embed_call1.description == "description1"

        assert embed_call1.author.name == "user1"
        assert embed_call1.author.url == "https://example.com/user/user1"
        assert embed_call1.author.icon_url == "https://example.com/user/user1/avatar"

        assert embed_call1.footer.text == "2025/01/02 14:00:00"

        embed_call2 = calls[2].kwargs["embed"]
        assert isinstance(embed_call2, discord.Embed)
        assert embed_call2.title == "title2"
        assert embed_call2.url == "https://example.com/repo2"
        assert embed_call2.description == "description2"

        assert embed_call2.author.name == "user2"
        assert embed_call2.author.url == "https://example.com/user/user2"
        assert embed_call2.author.icon_url == "https://example.com/user/user2/avatar"

        assert embed_call2.footer.text == "1919/09/29 12:15:40"

    @pytest.mark.asyncio
    async def test_send_github_activities_error(self, mocker: MockerFixture, discord_view, mock_ctx):
        mock_ctx.send.side_effect = Exception("View error.")

        with pytest.raises(Exception):
            await discord_view.send_github_activities(mock_ctx, [])

        mock_ctx.send.assert_called_with("取得に失敗しました")
