import json
from os import makedirs

from os.path import exists, join
from tinydb import TinyDB

from discord.ext import commands


class CustomBot(commands.Bot):
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
