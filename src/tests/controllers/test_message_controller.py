import pytest
from pytest_mock import MockerFixture

from src.app.dto.search_result import SearchResult

class TestMessageController:
    @pytest.fixture
    def message_controller(self):
        from src.app.controllers.message_controller import MessageController
        instance = MessageController()
        instance.query = "3k1_query"
        return instance

    @pytest.fixture
    def mock_ctx(self, mocker: MockerFixture):
        mocked = mocker.MagicMock()
        mocked.send = mocker.AsyncMock()
        return mocked

    @pytest.fixture
    def mock_search_results(self):
        return [
            SearchResult(
                title="title1",
                url="https://example.com/1",
                snippet="description1"
            ),
            SearchResult(
                title="title2",
                url="https://example.com/2",
                snippet="description2"
            )
        ]

    @pytest.fixture
    def mock_github_events(self):
        return [
            {"foo" : "bar"},
            {"foo" : "baz"}
        ]

    @pytest.mark.asyncio
    async def test_search_result(self, mocker:MockerFixture, message_controller, mock_search_results):
        mocker.patch(
            "src.app.controllers.message_controller.MessageModel.get_search_results",
            return_value=mock_search_results
        )

    @pytest.mark.asyncio
    async def test_github_activity_success(self, mocker: MockerFixture, message_controller, mock_ctx, mock_github_events):
        mocker.patch(
            "src.app.controllers.message_controller.MessageModel.get_github_activities",
            return_value=mock_github_events
        )
        mock_send_github_activities = mocker.patch(
            "src.app.controllers.message_controller.DiscordView.send_github_activities"
        )

        await message_controller.github_activity(mock_ctx)

        mock_send_github_activities.assert_called_once_with(
            mock_ctx,
            mock_github_events
        )

    @pytest.mark.asyncio
    async def test_github_activity_error(self, mocker: MockerFixture, message_controller, mock_ctx):
        mocker.patch(
            "src.app.controllers.message_controller.MessageModel.get_github_activities",
            side_effect=Exception("GitHub request Error.")
        )
        mocker.patch(
            "src.app.controllers.message_controller.DiscordView.send_github_activities"
        )

        await message_controller.github_activity(mock_ctx)

        mock_ctx.send.assert_called_with("取得に失敗しました")
