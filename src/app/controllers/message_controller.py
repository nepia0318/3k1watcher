import os
import re
import discord
from dotenv import load_dotenv
from logging import getLogger

from ..models.message_model import MessageModel
from ..views.discord_view import DiscordView


logger = getLogger(__name__)

class MessageController:
    def __init__(self):
        load_dotenv()
        self.query = os.getenv("3K1_QUERY")
        self.model = MessageModel()
        self.view = DiscordView()

    async def searchResult(self, ctx):
        try:
            results = self.model.getSearchResponse(self.query)
            await self.view.sendSearchResult(ctx, results)

        except Exception as e:
            logger.error(f"Error: {e}")
            await ctx.send('取得に失敗しました')

    async def githubResult(self, ctx):
        try:
            results = self.model.getGitHubActivity()
            await self.view.sendGitHubActivity(ctx, results)

        except Exception as e:
            await ctx.send("取得に失敗しました")
