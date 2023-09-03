import disnake
from disnake.ext import commands


class SelectGames(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(label="Dota 2", value="1099679839318986812", emoji="<:dota:1099626771533537321>"),
            disnake.SelectOption(label="Valorant", value="977507174475513926", emoji="<:valorant:1087339144012910646>"),
            disnake.SelectOption(label="Genshin Impact", value="977507468684976128", emoji="<:genshin:1087378394238431304>"),
            disnake.SelectOption(label="Apex legends", value="1099679412854726666", emoji="<:apex:1099617997548695592>"),
            disnake.SelectOption(label="Overwatch", value="1099677831518244934", emoji="<:overwatch:1099612849229283368>"),
            disnake.SelectOption(label="CS GO", value="1099680118810611812", emoji="<:csgo:1099626898537062420>"),
            disnake.SelectOption(label="League of Legends", value="1087370672776417330", emoji="<:league:1087339933783564398>"),
            disnake.SelectOption(label="Warframe", value="1146826018083057714", emoji="<:warframe:1146825923388244158> ")]

        super().__init__(placeholder="Select a game", options=options, custom_id="games", min_values=0, max_values=7)

    async def callback(self, interaction: disnake.MessageInteraction):
        await interaction.response.defer()
        all_roles = {1087370672776417330, 1099680118810611812, 1099677831518244934, 1099679412854726666, 977507468684976128, 977507174475513926, 1099679839318986812 ,1146826018083057714}
        to_remove = []
        to_add = []

        if not interaction.values:
            for role_id in all_roles:
                role = interaction.guild.get_role(role_id)
                to_remove.append(role)

            await interaction.author.remove_roles(*to_remove, reason="Removed all roles")

        else:
            chosen_roles = {int(value) for value in interaction.values}
            ids_to_remove = all_roles - chosen_roles

            for role_id in ids_to_remove:
                role = interaction.guild.get_role(role_id)
                to_remove.append(role)

            for role_id in chosen_roles:
                role = interaction.guild.get_role(role_id)
                to_add.append(role)

            await interaction.author.remove_roles(*to_remove, reason="Removed roles")
            await interaction.author.add_roles(*to_add, reason="Added roles")


class GameRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistents_views_added = False

    @commands.is_owner()
    @commands.slash_command(name='info_message')
    async def infomessage(self, ctx):
        view = disnake.ui.View(timeout=None)
        view.add_item(SelectGames())
        embed = disnake.Embed(color=0xD77D31)
        embed.set_author(name="Автор :  Нокс")
        embed.description = "```Перед тем, как ты начнешь общение, я хотела бы быстро рассказать о том, как все здесь устроено. После этого, я могу порекомендовать тебе группы по интересам, чтобы тебе было удобнее общаться.```\n" \
                            "**НЕ МНОГО ПРО РОЛИ :**\n" \
                            "**1.** Роли, такие как: <@&977507174475513926>,\n" \
                            "<@&1087370672776417330>, <@&1146826018083057714> и т.д.\n" \
                            "были созданы для удобства коммуникации на сервере и не предоставляют никаких дополнительных полномочий или привилегий.\n" \
                            "Получить эти роли можно ввыподающем меню ниже \n" \
                            "\n" \
                            "**2.** Роли, такие как <@&1107693007362334833>, <@&1100977318987579502>, <@&1107356381113237594> и т.д.\n" \
                            "являются ролями, которые выдаются участникам за участие в определенных событиях на сервере и так же не обладают дополнительными привилегиями"



        embed.set_image(url="https://media.discordapp.net/attachments/1047110597751345255/1102982395579338867/1636290638_looped_1636290638.gif")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1047110597751345255/1144263493646827620/Ellipse_1.png")
        await ctx.send(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_connect(self):
        if self.persistents_views_added:
            return

        view = disnake.ui.View(timeout=None)
        view.add_item(SelectGames())
        self.bot.add_view(view, message_id=1070794323689476178)


def setup(bot):
    bot.add_cog(GameRoles(bot))
