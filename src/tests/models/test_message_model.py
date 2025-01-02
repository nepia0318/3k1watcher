import pytest
import requests
from pytest_mock import MockerFixture

from src.app.dto.search_results import SearchResults
from src.app.dto.search_result import SearchResult
from src.app.dto.github_event import GithubEvent


class TestMessageModel:
    @pytest.fixture
    def message_model(self):
        from src.app.models.message_model import MessageModel
        instance = MessageModel()
        instance.BING_SEARCH_SUBSCRIPTION_KEY = "bing_search_subscription_key"
        instance.BING_SEARCH_API_URL = "bing_search_api_url"
        instance.GITHUB_USERNAME = "github_user"
        instance.GITHUB_API_TOKEN = "github_api_token"
        instance.GITHUB_API_URL = "github_api_url"
        return instance

    @pytest.fixture
    def mock_search_response(self):
        return {
            "webPages": {
                "webSearchUrl": "https://example.com/search?q=3k1",
                "totalEstimatedMatches": 2,
                "value": [
                    {
                        "name": "title1",
                        "url": "https://example.com/article1",
                        "snippet": "description1",
                        "dateLastCrawled": "2023-12-30T03:19:00.0000000Z"
                    },
                    {
                        "name": "title2",
                        "url": "https://example.com/article2",
                        "snippet": "description2",
                        "dateLastCrawled": "2024-05-17T06:20:00.0000000Z"
                    }
                ]
            }
        }

    @pytest.fixture
    def mock_search_results(self, mock_search_response):
        results = []
        for item in mock_search_response["items"]:
            results.append(
                SearchResult(
                    title=item["title"],
                    url=item["link"],
                    snippet=item["snippet"]
                )
            )
        return results

    @pytest.fixture
    def mock_github_activities_response(self):
        return [
            {"foo": "bar"},
            {"foo": "baz"}
        ]

    def test_get_search_results_success(
            self, mocker: MockerFixture, message_model,
            mock_search_response):
        response = requests.models.Response()
        response.status_code = 200
        response.json = mocker.Mock(return_value=mock_search_response)

        mock_requests_get = mocker.patch("requests.get", return_value=response)
        mocker.patch("src.app.models.message_model.SearchResults.from_json", return_value=SearchResults())

        query = "3k1"
        results = message_model.get_search_results(query)
        assert results.web_search_url == ""
        assert results.total == 0
        assert results.items == []

        mock_requests_get.assert_called_once()
        assert mock_requests_get.call_args.kwargs["params"]["q"] == query

    def test_get_search_results_api_error(self, mocker: MockerFixture, message_model):
        response = requests.models.Response()
        response.status_code = 500

        with pytest.raises(Exception) as e:
            query = "3k1"
            message_model.get_search_results(query)

        assert str(e.value) == "Request error."

    def test_get_github_activities_api_success(self, mocker: MockerFixture, message_model, mock_github_activities_response):
        response = requests.models.Response()
        response.status_code = 200
        response.json = mocker.Mock(return_value=mock_github_activities_response)

        mocker.patch("requests.get", return_value=response)
        mocker.patch("src.app.models.message_model.GithubEvent.from_json", return_value=GithubEvent())

        results = message_model.get_github_activities()
        assert len(results) == len(mock_github_activities_response)

    def test_get_github_activities_api_request_error(self, mocker: MockerFixture, message_model):
        response = requests.models.Response()
        response.status_code = 500

        with pytest.raises(Exception) as e:
            message_model.get_github_activities()

        assert str(e.value) == "Request error."

    def test_get_github_activities_api_parse_error(self, mocker: MockerFixture, message_model, mock_github_activities_response):
        response = requests.models.Response()
        response.status_code = 200
        response.json = mocker.Mock(return_value=mock_github_activities_response)

        mocker.patch("requests.get", return_value=response)
        mocker.patch("src.app.models.message_model.GithubEvent.from_json", side_effect=Exception("DTO error."))

        with pytest.raises(Exception) as e:
            message_model.get_github_activities()

        assert str(e.value) == "JSON parsing error."
