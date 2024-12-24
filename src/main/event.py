import requests
import discord
from logging import getLogger

async def search(ctx):
    logger = getLogger(__name__)

    try:
        embedMsg = discord.Embed(
            title='hoge',
            description=f'\
                fuga: {'mannsyuu3923'}',
            color=discord.Colour.green()
        )

        await ctx.send(embed=embedMsg)

    except requests.RequestException as e:
        logger.info(f"Error: {e}")
        await ctx.send('取得に失敗しました')

    except Exception as e:
        logger.error(f"Error: {e}")
        await ctx.send('取得に失敗しました')
