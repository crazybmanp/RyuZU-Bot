import json

import discord

from RyuZU.Core import Bot
from RyuZU.Core.helpers import is_owner

settings = None

try:
    settings = json.load(open("settings.json"))
except FileNotFoundError:
    print("You need to create a settings file!")
    exit()

bot = Bot(settings)


@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name="Spooling up..."))
    print('------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    if 'dev_mode' in bot.config and bot.config['dev_mode']:
        game = "[DevMode]"
    else:
        game = "Being a useless bot"

    await bot.change_presence(game=discord.Game(name=game))


@bot.command(pass_context=True, hidden=True)
async def load(ctx, extension_name: str):
    """Loads an extension."""
    if not is_owner(ctx.message.author):
        await bot.say("You must be {0}'s owner to do this.".format(bot.user.name))
        return
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} loaded.".format(extension_name))


@bot.command(pass_context=True, hidden=True)
async def unload(ctx, extension_name: str):
    """Unloads an extension."""
    if not is_owner(ctx.message.author):
        await bot.say("You must be {0}'s owner to do this.".format(bot.user.name))
        return
    bot.unload_extension(extension_name)
    await bot.say("{} unloaded.".format(extension_name))


@bot.command(pass_context=True, hidden=True)
async def shutdown(ctx):
    """Shuts down the bot"""
    if not is_owner(ctx.message.author):
        await bot.say("You must be {0}'s owner to do this.".format(bot.user.name))
        return
    await bot.change_presence(game=discord.Game(name="Shutting down"))
    print("Shutting down...")
    await bot.logout()


@bot.command(aliases=["bug", "suggest"])
async def issue():
    """Gives a link to report any issues or give us suggestions"""
    await bot.say("Find a problem or have a suggestion? Let us know here: https://github.com/crazybmanp/RyuZU/issues/new")
