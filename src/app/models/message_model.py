import os
import json
from dotenv import load_dotenv
from logging import getLogger
from googleapiclient.discovery import build

logger = getLogger(__name__)

class MessageModel:
    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv("GOOGLE_API_KEY")
        self.ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

    def getSearchResponse(self, query):
        service = build("customsearch", "v1", developerKey=self.API_KEY)
        try:
            response = (
                service.cse()
                .list(
                    q=query,
                    cx=self.ENGINE_ID,
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
