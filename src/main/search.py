import os
import json
from dotenv import load_dotenv
from logging import getLogger
from googleapiclient.discovery import build

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

def getSearchResponse(query):
    logger = getLogger(__name__)

    service = build("customsearch", "v1", developerKey=API_KEY)

    try:
        response = (
            service.cse()
            .list(
                q=query,
                cx=ENGINE_ID,
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
    # for v in response["items"]:
    #     logger.info(f"Title: {v["title"]}")
    #     logger.info(f"Snippet: {v["snippet"]}")

    return results
