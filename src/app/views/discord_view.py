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

    async def sendGithubActivity(self, ctx, results):
        try:
            await ctx.send(f"GitHubのアクティビティ: {len(results)}件")
            for result in results:
                match result["type"]:
                    case "CreateEvent":
                        embedMsg = parseGithubCreateEvent(result)
                    case "PushEvent":
                        embedMsg = parseGithubPushEvent(result)
                    case "ForkEvent":
                        embedMsg = parseGithubForkEvent(result)
                        pass
                    case "IssuesEvent":
                        embedMsg = parseGithubIssuesEvent(result)
                        pass
                    case _:
                        embedMsg = discord.Embed(
                            title=result["type"],
                            url=result["repo"]["url"],
                            color=discord.Colour.green()
                        )
                        pass

                embedMsg.set_thumbnail(url=result["actor"]["avatar_url"])
                await ctx.send(embed=embedMsg)
        except Exception as e:
            logger.error(f"Error: {e}")
            await ctx.send("取得に失敗しました")

def parseGithubCreateEvent(data):
    embedMsg = discord.Embed(
        title=data["repo"]["name"],
        description=f"リポジトリ{data["repo"]["name"]}を作成しました",
        url=f"https://github.com/{data["repo"]["name"]}",
        color=discord.Colour.green()
    )

    return embedMsg

def parseGithubPushEvent(data):
    commits_string = ""
    for commit in data["payload"]["commits"]:
        commits_string += f"- {commit["message"]},\n"
    commits_string = commits_string[:-2]
    embedMsg = discord.Embed(
        title=data["repo"]["name"],
        description=f"\
            pushしました\n\
            {commits_string}",
        url=f"https://github.com/{data["repo"]["name"]}",
        color=discord.Colour.green()
    )

    return embedMsg

def parseGithubForkEvent(data):
    embedMsg = discord.Embed(
        title=data["payload"]["forkee"]["full_name"],
        description=f"{data["repo"]["name"]}をforkしました",
        url=f"https://github.com/{data["payload"]["forkee"]["full_name"]}",
        color=discord.Colour.green()
    )

    return embedMsg

def parseGithubIssuesEvent(data):
    ACTIONS = {
        "opened": "オープン",
        "edited": "変更",
        "closed": "クローズ",
        "reopend": "再オープン",
        "assigned": "アサイン",
        "unassigned": "アサイン解除",
        "labeled": "ラベル付与",
        "unlabeled": "ラベル削除"
    }
    embedMsg = discord.Embed(
        title=data["repo"]["name"],
        description=f"\
            Issueを{ACTIONS[data["payload"]["action"]]}しました\n\
            [{data["payload"]["issue"]["title"]}]({data["payload"]["issue"]["html_url"]})",
        url=f"https://github.com/{data["repo"]["name"]}",
        color=discord.Colour.green()
    )

    return embedMsg
