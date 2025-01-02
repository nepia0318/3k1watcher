import pytest
import requests
from googleapiclient.errors import HttpError

from src.app.dto.search_result import SearchResult
from src.app.dto.github_event import GithubEvent

class TestMessageModel:
    @pytest.fixture
    def message_model(self):
        from src.app.models.message_model import MessageModel
        instance = MessageModel()
        instance.GOOGLE_SEARCH_API_KEY = "google_search_api_key"
        instance.GOOGLE_SEARCH_ENGINE_ID = "google_search_engine_id"
        instance.GITHUB_USERNAME = "github_user"
        instance.GITHUB_API_TOKEN = "github_api_token"
        instance.GITHUB_API_URL = "github_api_url"
        return instance

    @pytest.fixture
    def mock_search_response(self):
        return {
            "items":
                [
                    {
                        "title": "title1",
                        "link" : "https://exmaple.com/1",
                        "snippet": "description1"
                    },
                    {
                        "title": "title2",
                        "link" : "https://exmaple.com/2",
                        "snippet": "description2"
                    },
                ],
            "searchInformation": {
                "totalResults": 2
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
            {"foo" : "bar"},
            {"foo" : "baz"}
        ]

    def test_get_search_results_success(
            self, mocker, message_model,
            mock_search_response, mock_search_results):
        mock_service = mocker.MagicMock()
        mock_service.cse().list().execute.return_value = mock_search_response
        mocker.patch("src.app.models.message_model.build", return_value=mock_service)

        query = "3k1"
        results = message_model.get_search_results(query)

        assert results == mock_search_results
        mock_service.cse().list.assert_called_with(
            q=query,
            cx=message_model.GOOGLE_SEARCH_ENGINE_ID,
            lr='lang_ja',
            filter=0,
            num=10,
            start=1
        )

    def test_get_search_results_api_error(self, mocker, message_model):
        mock_service = mocker.MagicMock()
        mock_service.cse().list().execute.side_effect = HttpError(
            mocker.MagicMock(status=500),
            b'API Error'
        )

        mocker.patch("src.app.models.message_model.build", return_value=mock_service)

        with pytest.raises(Exception) as e:
            message_model.get_search_results("3k1")

        assert str(e.value) == "Request error."

    def test_get_github_activities_api_success(self, mocker, message_model, mock_github_activities_response):
        response = requests.models.Response()
        response.status_code = 200
        response.json = mocker.Mock(return_value=mock_github_activities_response)

        mocker.patch("requests.get", return_value=response)
        mocker.patch("src.app.models.message_model.GithubEvent.from_json", return_value=GithubEvent())

        results = message_model.get_github_activities()
        assert len(results) == len(mock_github_activities_response)

    def test_get_github_activities_api_request_error(self, mocker, message_model):
        response = requests.models.Response()
        response.status_code = 500

        with pytest.raises(Exception) as e:
            message_model.get_github_activities()

        assert str(e.value) == "Request error."

    def test_get_github_activities_api_parse_error(self, mocker, message_model, mock_github_activities_response):
        response = requests.models.Response()
        response.status_code = 200
        response.json = mocker.Mock(return_value=mock_github_activities_response)

        mocker.patch("requests.get", return_value=response)
        mocker.patch("src.app.models.message_model.GithubEvent.from_json", side_effect=Exception("DTO error."))

        with pytest.raises(Exception) as e:
            message_model.get_github_activities()

        assert str(e.value) == "JSON parsing error."
