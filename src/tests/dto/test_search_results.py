import pytest
from pytest_mock import MockerFixture
from datetime import datetime

from src.app.dto.search_result import SearchResult
from src.app.dto.search_results import SearchResults


class TestSearchResults:
    @pytest.fixture
    def mock_json(self) -> dict:
        return {
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

    @pytest.fixture
    def mock_search_result1(self) -> SearchResult:
        return SearchResult(
            title="title1",
            url="https://example.com/article1",
            snippet="description1",
            last_crawled=datetime(
                year=2023, month=12, day=30,
                hour=3, minute=19, second=0
            )
        )

    @pytest.fixture
    def mock_search_result2(self) -> SearchResult:
        return SearchResult(
            title="title2",
            url="https://example.com/article2",
            snippet="description2",
            last_crawled=datetime(
                year=2024, month=5, day=17,
                hour=6, minute=20, second=0
            )
        )

    def test_from_json(
            self, mocker: MockerFixture, mock_json,
            mock_search_result1, mock_search_result2):
        mocker.patch(
            "src.app.dto.search_results.SearchResult.from_json",
            side_effect=[mock_search_result1, mock_search_result2]
        )
        results = SearchResults.from_json(mock_json)

        assert results.web_search_url == "https://example.com/search?q=3k1"
        assert results.total == 2

        assert results.results[0].url == "https://example.com/article1"
        assert results.results[0].title == "title1"
        assert results.results[0].snippet == "description1"
        assert results.results[0].last_crawled == datetime(
            year=2023, month=12, day=30,
            hour=3, minute=19, second=0
        )

        assert results.results[1].url == "https://example.com/article2"
        assert results.results[1].title == "title2"
        assert results.results[1].snippet == "description2"
        assert results.results[1].last_crawled == datetime(
            year=2024, month=5, day=17,
            hour=6, minute=20, second=0
        )
