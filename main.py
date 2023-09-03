import disnake
from disnake.ext import commands
import os
from webserver import keep_elfve

bot = commands.Bot(command_prefix=".", intents=disnake.Intents.all())
bot.remove_command("help")
bot.owner_id = os.getenv('OWNER_ID')

cogs = [os.path.splitext(file)[0] for file in os.listdir("cogs") if file.endswith(".py")]

for cog in cogs:
    bot.load_extension(f"cogs.{cog}")


@bot.command()
@commands.is_owner()
async def load_extension(inter, extension_name: str):
    if inter.guild is not None:
        try:
            bot.load_extension(f"cogs.{extension_name}")
            await inter.send(f"Расширение '{extension_name}' успешно загружено.")
        except Exception as e:
            await inter.send(f"Ошибка при загрузке расширения: {type(e).__name__} - {e}")
    else:
        await inter.send('Команда должна быть выполнена на сервере.')


@bot.command()
@commands.is_owner()
async def reload_extension(inter, extension_name: str):
    try:
        bot.reload_extension(f"cogs.{extension_name}")
        await inter.send(f"Расширение '{extension_name}' успешно перезагружено.")
    except Exception as e:
        await inter.send(f"Ошибка при перезагрузке расширения: {type(e).__name__} - {e}")


@bot.command()
@commands.is_owner()
async def unload_extension(inter, extension_name: str):
    try:
        bot.unload_extension(f"cogs.{extension_name}")
        await inter.send(f"Расширение '{extension_name}' успешно выгружено.")
    except Exception as e:
        await inter.send(f"Ошибка при выгрузке расширения: {type(e).__name__} - {e}")


if __name__ == "__main__":
    keep_elfve()
    bot.run(os.getenv('TOKEN'))
