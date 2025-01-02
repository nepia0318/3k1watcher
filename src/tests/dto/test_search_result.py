import pytest
from datetime import datetime

from src.app.dto.search_result import SearchResult


class TestSearchResult:
    @pytest.fixture
    def mock_json(self) -> dict:
        return {
            "name": "title1",
            "url": "https://example.com/article1",
            "snippet": "description1",
            "dateLastCrawled": "2023-12-30T03:19:00.0000000Z"
        }

    def test_from_json(self, mock_json):
        result = SearchResult.from_json(mock_json)

        assert result.title == "title1"
        assert result.url == "https://example.com/article1"
        assert result.snippet == "description1"
        assert result.last_crawled == datetime(
            year=2023, month=12, day=30,
            hour=3, minute=19, second=0
        )
