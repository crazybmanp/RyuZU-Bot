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
        self.load_cogs()

    def load_extension(self, name, core_cog=False):
        """Thin wrapper to make packaged life easier"""
        if core_cog:
            super().load_extension("RyuZU.{}".format(name))
        else:
            super().load_extension(name)

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

    def load_cogs(self):
        """Called on initialization. This isn't for dynamic loading/unloading of cogs"""
        core_cogs = ["Admin", "Util"]

        print("Loading core cogs...")
        for extension in core_cogs:
            try:
                self.load_extension(extension, core_cog=True)
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load Core Cog: {}, we will now shut down\n{}'.format(extension, exc))
                exit()

        ext_cogs = []
        print("Loading Extension cogs...")
        for extension in self.config['startup_extensions']:
            try:
                self.load_extension(extension)
                ext_cogs.append(extension)
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load cog {}\n{}'.format(extension, exc))
        print("Loaded the following cogs: {}".format(ext_cogs))


class Cog:
    def __init__(self, bot, version, settings=None):
        self.bot = bot
        self.__version__ = version
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