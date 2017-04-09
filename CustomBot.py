from discord.ext import commands


class CustomBot(commands.Bot):
    def __init__(self, description, config):
        super().__init__(command_prefix=config['command_string'], description=description)
        self.config = config
