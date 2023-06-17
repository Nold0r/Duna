import disnake
from disnake.ext import commands
from utils.data_handler import DataHandler


class SetMainChannel(commands.Cog):
    def __init__(self, bot=commands.Bot):
        self.bot = bot

    @commands.slash_command(name='set_main_channel')
    @commands.has_guild_permissions()
    async def setmainchannel(self, inter: disnake.ApplicationCommandInteraction, channel: disnake.VoiceChannel):
        data = DataHandler.load_data()
        guild_id = inter.guild.id
        main_channel_id = channel.id

        if str(guild_id) in data:
            await inter.send('Канал на этом сервере уже задан ❌', ephemeral=True)
        else:
            data.update({guild_id:
                             {"main_channel_id": main_channel_id,
                              "voice_channel_id": []
                              }
                         })
            DataHandler.save_data(data)
            await inter.send('вы успешно зарегистрировали сервер ✔', ephemeral=True)
            print(data)


def setup(bot: [commands.Bot]):
    bot.add_cog(SetMainChannel(bot))
    print(f"> Extension {__name__} is ready")
