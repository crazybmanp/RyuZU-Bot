import random

from discord.ext import commands


class Util():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, dice: str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except ValueError:
            await self.bot.say('Format has to be in NdN!')
            return

        if rolls > 100 or limit > 1000000:
            await self.bot.say("You cannot roll more than 100 dice, or dice bigger than 1 Million.")
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await self.bot.say(result)

    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, *choices: str):
        """Chooses between multiple choices."""
        if len(choices) < 1:
            await self.bot.say("You need to specify one or more choices.")
            return
        await self.bot.say(random.choice(choices))


def setup(bot):
    bot.add_cog(Util(bot))
