import re
import discord
from logging import getLogger
from datetime import datetime
logger = getLogger(__name__)

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

    async def sendGithubActivity(self, ctx, results):
        try:
            await ctx.send(f"まん３のGitHubアクティビティが{len(results)}件ヒットしました")
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
                        embedMsg = parseGithubOtherEvent(result)
                        pass

                embedMsg.set_author(name=result["actor"]["display_login"], url=result["actor"]["url"], icon_url=result["actor"]["avatar_url"])
                await ctx.send(embed=embedMsg)
        except Exception as e:
            logger.error(f"Error: {e}")
            await ctx.send("取得に失敗しました")

def getHtmlUrlFromApiUrl(url):
    return url.replace("api.github.com", "github.com").replace("/repos/", "/")

def parseGithubCreateEvent(data):
    dt = datetime.strptime(data["created_at"], "%Y-%m-%dT%H:%M:%SZ")
    formatted_dt = dt.strftime("%Y/%m/%d %H:%M:%S")
    embedMsg = discord.Embed(
        title=data["repo"]["name"],
        description=f"\
            リポジトリを作成しました\n\
            \n[{formatted_dt}]",
        url=getHtmlUrlFromApiUrl(data["repo"]["url"]),
        color=discord.Colour.green()
    )

    return embedMsg

def parseGithubPushEvent(data):
    commits_num = len(data["payload"]["commits"])
    commits_string = ""
    for commit in data["payload"]["commits"]:
        commits_string += f"- {commit["message"]},\n"
    commits_string = commits_string[:-2]
    dt = datetime.strptime(data["created_at"], "%Y-%m-%dT%H:%M:%SZ")
    formatted_dt = dt.strftime("%Y/%m/%d %H:%M:%S")
    embedMsg = discord.Embed(
        title=data["repo"]["name"],
        description=f"\
            {commits_num}件のcommitをpushしました\n\
            \n{commits_string}\
            \n\n[{formatted_dt}]", # 何故か上の行の\nが認識されない
        url=getHtmlUrlFromApiUrl(data["repo"]["url"]),
        color=discord.Colour.green()
    )

    return embedMsg

def parseGithubForkEvent(data):
    dt = datetime.strptime(data["created_at"], "%Y-%m-%dT%H:%M:%SZ")
    formatted_dt = dt.strftime("%Y/%m/%d %H:%M:%S")
    embedMsg = discord.Embed(
        title=data["payload"]["forkee"]["full_name"],
        description=f"\
            [{data["repo"]["name"]}]({getHtmlUrlFromApiUrl(data["repo"]["url"])})をforkしました\n\
            \n[{formatted_dt}]",
        url=data["payload"]["forkee"]["html_url"],
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

    dt = datetime.strptime(data["created_at"], "%Y-%m-%dT%H:%M:%SZ")
    formatted_dt = dt.strftime("%Y/%m/%d %H:%M:%S")
    embedMsg = discord.Embed(
        title=data["repo"]["name"],
        description=f"\
            issueを{ACTIONS[data["payload"]["action"]]}しました\n\
            \n[{data["payload"]["issue"]["title"]}]({data["payload"]["issue"]["html_url"]})\n\
            \n[{formatted_dt}]",
        url=getHtmlUrlFromApiUrl(data["repo"]["url"]),
        color=discord.Colour.green()
    )

    return embedMsg

def parseGithubOtherEvent(data):
    dt = datetime.strptime(data["created_at"], "%Y-%m-%dT%H:%M:%SZ")
    formatted_dt = dt.strftime("%Y/%m/%d %H:%M:%S")

    embedMsg = discord.Embed(
        title=data["type"],
        description=f"\n[{formatted_dt}]",
        url=getHtmlUrlFromApiUrl(data["repo"]["url"]),
        color=discord.Colour.green()
    )
    return None
