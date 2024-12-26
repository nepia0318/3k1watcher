import os
import json
import requests
from dotenv import load_dotenv
from logging import getLogger
from googleapiclient.discovery import build

logger = getLogger(__name__)

class MessageModel:
    def __init__(self):
        load_dotenv()
        self.GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
        self.GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
        self.GITHUB_USERNAME = os.getenv("3K1_GIT_USERNAME")
        self.GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN")
        self.GITHUB_API_URL = f"https://api.github.com/users/{self.GITHUB_USERNAME}/events"

    def getSearchResponse(self, query):
        service = build("customsearch", "v1", developerKey=self.GOOGLE_SEARCH_API_KEY)
        try:
            response = (
                service.cse()
                .list(
                    q=query,
                    cx=self.GOOGLE_SEARCH_ENGINE_ID,
                    lr='lang_ja',
                    filter=0,
                    num=10,
                    start=1
                ).execute()
            )
        except Exception as e:
            logger.error(e)
            raise Exception("Request error.")

        results = response["items"]
        logger.info(f"Number of results: {response["searchInformation"]["totalResults"]}")

        return results

    def getGitHubActivity(self):
        print(self.GITHUB_API_URL)
        url = self.GITHUB_API_URL
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.GITHUB_API_TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        params = {
            "per_page": 10,
            "page": 1
        }

        try:
            response = requests.get(url=url, headers=headers, params=params)
            response.raise_for_status()
            results = json.loads(response.text)
            # print(f"type: {results[0]["type"]}, name: {results[0]["payload"]["forkee"]["name"]}, full_name: {results[0]["payload"]["forkee"]["full_name"]}")
        except Exception as e:
            logger.error(e)
            raise Exception("Request error.")

        return results
