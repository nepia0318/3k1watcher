import os
import requests
from dotenv import load_dotenv
from logging import getLogger

from src.app.dto.github_event import GithubEvent
from src.app.dto.search_results import SearchResults

logger = getLogger(__name__)


class MessageModel:
    def __init__(self):
        load_dotenv()
        self.BING_SEARCH_SUBSCRIPTION_KEY = os.getenv(key="BING_SUBSCRIPTION_KEY")
        self.BING_SEARCH_API_URL = "https://api.bing.microsoft.com/v7.0/search"
        self.GITHUB_USERNAME = os.getenv("3K1_GIT_USERNAME")
        self.GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN")
        self.GITHUB_API_URL = f"https://api.github.com/users/{self.GITHUB_USERNAME}/events"

    def get_search_results(self, query) -> SearchResults:

        try:
            assert self.BING_SEARCH_SUBSCRIPTION_KEY

            headers = {"Ocp-Apim-Subscription-Key": self.BING_SEARCH_SUBSCRIPTION_KEY}
            params = {"q": query, "textDecorations": True, "textFormat": "HTML"}
            response = requests.get(self.BING_SEARCH_API_URL, headers=headers, params=params)
            response.raise_for_status()
            response = response.json()

        except Exception as e:
            logger.error(e)
            raise Exception("Request error.")

        logger.info(f"Number of results: {response["webPages"]["totalEstimatedMatches"]}")

        results = SearchResults.from_json(response["webPages"])

        return results

    def get_github_activities(self) -> list[GithubEvent]:
        url = self.GITHUB_API_URL
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.GITHUB_API_TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        params = {
            "per_page": 30,
            "page": 1
        }

        try:
            response = requests.get(url=url, headers=headers, params=params)
            response.raise_for_status()
            response = response.json()

        except Exception as e:
            logger.error(e)
            raise Exception("Request error.")

        events = []
        try:
            for item in response:
                events.append(GithubEvent.from_json(item))

        except Exception as e:
            logger.error(f"Error: {e}")
            raise Exception("JSON parsing error.")
        return events
