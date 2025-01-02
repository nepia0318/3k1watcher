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

    async def search_result(self, ctx):
        try:
            results = self.model.get_search_results(self.query)
            await self.view.send_search_results(ctx, results)

        except Exception as e:
            logger.error(f"Error: {e}")
            await ctx.send('取得に失敗しました')

    async def github_activity(self, ctx):
        try:
            events = self.model.get_github_activities()
            await self.view.send_github_activities(ctx, events)

        except Exception as e:
            logger.error(f"Error: {e}")
            await ctx.send("取得に失敗しました")
