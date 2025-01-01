import re
import discord
from logging import getLogger
from datetime import datetime
logger = getLogger(__name__)

from ..dto.GithubEvent import GithubEvent

class DiscordView:
    async def sendSearchResult(self, ctx, results):
        try:
            await ctx.send(f'まん３に関する検索結果が{len(results)}件ヒットしました')
            for result in results:
                snippet = re.findall('(?<=\().+?(?=\))', result["snippet"])
                embedMsg = discord.Embed(
                    title=result["title"],
                    url=result["link"],
                    description=f'\
                        {result["snippet"]}',
                    color=discord.Colour.green()
                )

                await ctx.send(embed=embedMsg)

        except Exception as e:
            logger.error(f"Error: {e}")
            await ctx.send('取得に失敗しました')

    async def sendGithubActivity(self, ctx, events: list[GithubEvent]):
        try:
            await ctx.send(f"まん３のGitHubアクティビティが{len(events)}件ヒットしました")
            for event in events:
                embedMsg = discord.Embed(
                    title=event.title,
                    description=event.message,
                    url=event.url
                )
                embedMsg.set_author(name=event.author.name, url=event.author.url, icon_url=event.author.avatar_url)
                dt = event.created_at
                formatted_dt = dt.strftime("%Y/%m/%d %H:%M:%S")
                embedMsg.set_footer(text=formatted_dt)
                await ctx.send(embed=embedMsg)
        except Exception as e:
            logger.error(f"Error: {e}")
            await ctx.send("取得に失敗しました")
