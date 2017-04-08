import random

import discord
from discord.ext import commands

import config

description = 'A possibly useless bot.'
bot = commands.Bot(command_prefix='!', description=description)


@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name="Spooling up..."))
    print('------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name="Being a useless bot"))


@bot.command()
async def load(extension_name: str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} loaded.".format(extension_name))


@bot.command()
async def unload(extension_name: str):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await bot.say("{} unloaded.".format(extension_name))


@bot.command()
async def roll(dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(*choices: str):
    """Chooses between multiple choices."""
    await bot.say(random.choice(choices))


@bot.command(pass_context=True)
async def purge(ctx, messages=100):
    """Purges all (100 by default) previous messages from chat."""
    if not ctx.message.author.permissions_in(ctx.message.channel).administrator:
        await bot.say("Only Admins are allowed to purge the chat.")
        return
    await bot.say("purging {} messages".format(messages))
    messages += 2  # account for command and feedback
    await bot.purge_from(ctx.message.channel, limit=messages)


@bot.command(pass_context=True)
async def clean(ctx, messages=100):
    """Cleans all posts from this bot and any commands."""
    await bot.say("Cleaning...")
    message = ctx.message
    deleted = await bot.purge_from(message.channel, limit=messages, check=is_me)
    deleted += await bot.purge_from(message.channel, limit=messages, check=is_command)
    await bot.say('Deleted {} message(s)'.format(len(deleted)))


def is_me(m):
    return m.author == bot.user


def is_command(m):
    return m.content.startswith('!')


if __name__ == "__main__":
    for extension in config.startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(config.key)
