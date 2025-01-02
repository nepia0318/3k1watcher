import pytest

from src.app.dto.search_result import SearchResult


class TestSearchResult:
    @pytest.fixture
    def mock_json(self) -> dict:
        return {
            "title": "title1",
            "link": "https://example.com/article1",
            "snippet": "description1"
        }

    def test_from_json(self, mock_json):
        result = SearchResult.from_json(mock_json)

        assert result.title == "title1"
        assert result.url == "https://example.com/article1"
        assert result.snippet == "description1"
