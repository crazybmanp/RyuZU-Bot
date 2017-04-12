from RyuZU import bot

core_cogs = ["Admin", "Util"]

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
