import os
import json
import discord
from dotenv import load_dotenv
from logging import getLogger, config, getHandlerByName
from discord.ext import commands

from .controllers.message_controller import MessageController

logger = getLogger(__name__)
logger_disc = getLogger('discord')


class App:
    def __init__(self):
        load_dotenv()
        self.token = os.getenv("DISCORD_APP_TOKEN")
        self.is_dev = os.getenv("IS_DEV")
        self.controller = MessageController()
        with open('src/app/resources/log_config.json', 'r') as f:
            config.dictConfig(json.load(f))

        if self.is_dev:
            logger.info('App is running on development environment.')
        else:
            logger.info('App is running on fly.io environment.')

    def main(self):
        logger_disc.addHandler(getHandlerByName('consoleHandler'))
        logger_disc.addHandler(getHandlerByName('fileHandler'))

        intents = discord.Intents.default()
        intents.message_content = True
        bot = commands.Bot(command_prefix='$', intents=intents)

        @bot.event
        async def on_ready():
            logger.info(f'We have logged in as {bot.user}')

        @bot.command(name=cmd_name('search', self.is_dev))
        async def show_info(ctx):
            await self.controller.search_result(ctx)

        @bot.command(name=cmd_name('github', self.is_dev))
        async def show_info(ctx):
            await self.controller.github_activity(ctx)

        @bot.event
        async def on_command_error(ctx, e):
            cmd = ctx.invoked_with
            if isinstance(e, commands.CommandNotFound):
                logger.info(f'"{cmd}" command not found')

            return

        bot.run(self.token, log_handler=None)


def cmd_name(name, isDev):
    if isDev:
        return f'{name}-dev'
    return name


app = App()


def main() -> None:
    app.main()


if __name__ == "__main__":
    main()
