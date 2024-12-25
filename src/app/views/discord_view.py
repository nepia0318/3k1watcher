import re
import discord
from logging import getLogger

logger = getLogger(__name__)

class DiscordView:
    async def sendSearchResult(self, ctx, results):
        try:
            await ctx.send(f'まん３に関する検索結果は{len(results)}件でした')
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
