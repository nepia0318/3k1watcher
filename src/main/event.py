import os
import re
import discord
from dotenv import load_dotenv
from logging import getLogger

from .search import getSearchResponse

load_dotenv()
word = os.getenv("3K1_QUERY")

async def search(ctx):
    logger = getLogger(__name__)

    query = word
    try:
        results = getSearchResponse(query)
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
