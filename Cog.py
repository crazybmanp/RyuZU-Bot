from os import makedirs
from os.path import join, exists

from tinydb import TinyDB


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

    def get_cog_db(self, databasename: str):
        """
        Mounts a db for a cog (handling naming)
        :param databasename: the name of the database to fetch for your cog
        :return: TinyDB database
        """
        directory = join("Databases", self.__class__.__name__)
        if not exists(directory):
            makedirs(directory)
        return TinyDB(join("Databases", self.__class__.__name__, "{}.json".format(databasename)))
