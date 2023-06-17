import disnake
from disnake.ext import commands
from utils.data_handler import DataHandler
from disnake import ui


class MoveUserDialog(ui.View):
    def __init__(self):
        super().__init__()
        self.result = None

    @ui.button(label='Да', style=disnake.ButtonStyle.green)
    async def yes_button(self, button: ui.Button, interaction: disnake.Interaction):
        self.result = True
        self.stop()

    @ui.button(label='Нет', style=disnake.ButtonStyle.red)
    async def no_button(self, button: ui.Button, interaction: disnake.Interaction):
        self.result = False
        self.stop()


class CreateVoiceChannel(commands.Cog):
    def __init__(self, bot=commands.Bot):
        self.bot = bot

    @commands.slash_command(name='create_voice_channel')
    async def createvoischannel(self, inter: disnake.ApplicationCommandInteraction, name: str, user_limit: int = 0,
                                role: disnake.Role = None):
        guild = inter.guild
        data = DataHandler.load_data()
        dialog = MoveUserDialog()
        if str(guild.id) in data and len(guild.get_channel(data[str(guild.id)]["main_channel_id"]).members) != 0:
            overwrites = {}
            if role:
                overwrites = {
                    guild.default_role: disnake.PermissionOverwrite(connect=False),
                    role: disnake.PermissionOverwrite(connect=True)
                }
            voice_channel = await guild.create_voice_channel(name, user_limit=user_limit, overwrites=overwrites,
                                                             category=guild.get_channel(
                                                                 data[str(guild.id)]["main_channel_id"]).category)

            if user_limit == 0:
                user_limit_text = 'нет ограничения по участникам'
            else:
                user_limit_text = f'лимит участников {user_limit}'
            await inter.send(embed=disnake.Embed(title='КАНАЛ БЫЛ СОЗДАН.',
                                                 description=f'ХОТИТЕ ПЕРЕЙТИ В НЕГО?\n'
                                                             f'Название:\n'
                                                             f'```{name}```\n'
                                                             f'Участники:\n'
                                                             f'```{user_limit_text}```',
                                                 color=disnake.Color.dark_blue()), ephemeral=True, view=dialog)
            data[str(guild.id)]["voice_channel_id"].append(voice_channel.id)
            DataHandler.save_data(data)
            await dialog.wait()
            if dialog.result:
                await inter.user.move_to(voice_channel)
                await inter.send('вы были перенесены в созданный канал', ephemeral=True)

        elif str(guild.id) not in data:
            await inter.send('Кажется этот сервер ещё не зарегистрирован ❌', ephemeral=True)

        elif len(guild.get_channel(data[str(guild.id)]).members) == 0:
            await inter.send('Кажется в канале никого нет ❌', ephemeral=True)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: disnake.Member, before: disnake.VoiceState,
                                    after: disnake.VoiceState):
        guild = member.guild
        data = DataHandler.load_data()
        if before.channel:
            if before.channel.id in data[str(guild.id)]["voice_channel_id"]:
                if len(before.channel.members) == 0:
                    await before.channel.delete()
                    data[str(guild.id)]["voice_channel_id"].remove(before.channel.id)
                    DataHandler.save_data(data)


def setup(bot: [commands.Bot]):
    bot.add_cog(CreateVoiceChannel(bot))
    print(f"> Extension {__name__} is ready")
