class Cog:
    def __init__(self, bot, settings=None):
        self.bot = bot
        self.settings = settings

        if self.settings is not None:
            if self.__class__.__name__ in self.bot.config:
                for k, v in self.settings.items():
                    if k not in self.bot.config[self.__class__.__name__]:
                        self.bot.config[self.__class__.__name__][k] = v
            else:
                self.bot.config[self.__class__.__name__] = self.settings

            self.bot.update_config()
