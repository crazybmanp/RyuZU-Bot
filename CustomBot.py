import json

from discord.ext import commands


class CustomBot(commands.Bot):
    def __init__(self, config):
        super().__init__(command_prefix=config['command_string'], description=config['description'])
        self.config = config

    def update_config(self):
        """Writes the running config to the json file"""
        json.dump(self.config, open("settings.json", "w"))
