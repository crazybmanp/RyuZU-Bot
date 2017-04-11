import json

import discord

from CustomBot import CustomBot

settings = None

try:
    settings = json.load(open("settings.json"))
except FileNotFoundError:
    print("You need to create a settings file!")
    exit()

bot = CustomBot(settings)
core_cogs = ["Admin", "Util"]


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
    await bot.say(
        "Find a problem or have a suggestion? Let us know here: https://github.com/crazybmanp/RyuZU-Bot/issues/new")


@bot.command()
async def info():
    """Displays the version and other info about the bot"""
    e = discord.Embed(type="rich", title=bot.user.name, url="https://github.com/crazybmanp/RyuZU-Bot/",
                      description="A Discord bot build on modularity via cogs.", color=discord.Color(0xFF00FF))
    e.add_field(name="Version", value="?.?.?")
    e.add_field(name="Developers", value="crazybmanp#9518, raz#9254", inline=True)
    e.add_field(name="Contributors", value="None", inline=True)
    e.add_field(name="Github", value="https://github.com/crazybmanp/RyuZU-Bot/")

    await bot.say(embed=e)


def is_owner(author):
    for owner in bot.config['owner_usernames']:
        p = owner.split("#")
        if p[0] == author.name and p[1] == author.discriminator:
            return True
    return False


if __name__ == "__main__":
    print("Loading core cogs...")
    for extension in core_cogs:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load Core Cog: {}, we will now shut down\n{}'.format(extension, exc))
            exit()
    print("Loading Extension cogs...")
    for extension in bot.config['startup_extensions']:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load cog {}\n{}'.format(extension, exc))

    bot.run(bot.config['key'])
