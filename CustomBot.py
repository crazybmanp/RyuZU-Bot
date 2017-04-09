from discord.ext import commands


class CustomBot(commands.Bot):
    def __init__(self, config):
        super().__init__(command_prefix=config['command_string'], description=config['description'])
        self.config = config
