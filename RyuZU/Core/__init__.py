import json
from os import makedirs
from os.path import exists, join

from discord.ext import commands
from tinydb import TinyDB


class Bot(commands.Bot):
    Databases = {}

    def __init__(self, config):
        super().__init__(command_prefix=config['command_string'], description=config['description'])
        self.config = config

    def update_config(self):
        """Writes the running config to the json file"""
        json.dump(self.config, open("settings.json", "w"))

    def get_global_db(self, databasename: str):
        if databasename in self.Databases:
            return self.Databases[databasename]
        directory = "Databases"
        if not exists(directory):
            makedirs(directory)
        db = TinyDB(join("Databases", "{}.json".format(databasename)))
        self.Databases[databasename] = db
        return db

    def load_extension(self, name):
        """Thin wrapper to make packaged life easier"""
        super().load_extension("RyuZU.{}".format(name))


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