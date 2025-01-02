import discord
from logging import getLogger

from ..dto.search_result import SearchResult
from ..dto.github_event import GithubEvent

logger = getLogger(__name__)


class DiscordView:
    async def send_search_results(self, ctx, results: list[SearchResult]):
        try:
            await ctx.send(f"まん３に関する検索結果が{len(results)}件ヒットしました")
            for result in results:
                embedMsg = discord.Embed(
                    title=result.title,
                    url=result.url,
                    description=result.snippet,
                    color=discord.Colour.green()
                )

                await ctx.send(embed=embedMsg)

        except Exception as e:
            logger.error(f"Error: {e}")
            await ctx.send("取得に失敗しました")

    async def send_github_activities(self, ctx, events: list[GithubEvent]):
        try:
            await ctx.send(f"まん３のGitHubアクティビティが{len(events)}件ヒットしました")
            for event in events:
                embedMsg = discord.Embed(
                    title=event.title,
                    url=event.url,
                    description=event.message
                )

                if event.author is not None:
                    embedMsg.set_author(name=event.author.name, url=event.author.url, icon_url=event.author.avatar_url)

                if event.created_at is not None:
                    dt = event.created_at
                    formatted_dt = dt.strftime("%Y/%m/%d %H:%M:%S")
                    embedMsg.set_footer(text=formatted_dt)

                await ctx.send(embed=embedMsg)

        except Exception as e:
            logger.error(f"Error: {e}")
            await ctx.send("取得に失敗しました")
