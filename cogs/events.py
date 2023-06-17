import disnake
from disnake.ext import commands


class Events(commands.Cog):
    def __init__(self, bot=commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready.")


def setup(bot: commands.Bot):
    bot.add_cog((Events(bot)))
    print(f">Extension {__name__} is ready")
