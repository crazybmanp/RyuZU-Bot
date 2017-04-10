import random

from discord.ext import commands

from Cog import Cog


class Util(Cog):
    @commands.command()
    async def roll(self, *dice: str):
        """Rolls a dice in NdN format."""
        if len(dice) < 1:
            dice = ["1d6"]
        rolls = []
        limits = []
        i = 1
        try:
            for d in dice:
                r, l = map(int, d.split('d'))
                if r > 100 or l > 1000000:
                    await self.bot.say("You cannot roll more than 100 dice, or dice bigger than 1 million sides.")
                    return
                if l == 1:  # handle this cases separately for fun.
                    await self.bot.say("How do i roll a one sided die?")
                    return
                if r < 1 or l < 1:
                    await self.bot.say("Rolling less than one die or rolling a die with less than 2 sides makes no "
                                       "sense.")
                    return
                rolls.append(r)
                limits.append(l)
        except ValueError:
            await self.bot.say('Format has to be in NdN!')
            return
        total = 0
        result = ""
        for r, l in zip(rolls, limits):
            linerolls = []
            for i in range(0, r):
                linerolls.append(random.randint(1, l))
            linetotal = sum(linerolls)
            if r == 1:
                result += str(linerolls[0]) + "\r\n"
            else:
                result += str(linetotal) + " = " + " + ".join(str(x) for x in linerolls) + "\r\n"
            total += linetotal
        if len(rolls) != 1:
            result += "Total: " + str(total)
        await self.bot.say(result)

    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, *choices: str):
        """Chooses between multiple choices."""
        if len(choices) < 1:
            await self.bot.say("You need to specify one or more choices.")
            return
        await self.bot.say(random.choice(choices))

    @commands.command()
    async def ping(self):
        """Gives a pong message as quickly as it can."""
        await self.bot.say("PONG!")


def setup(bot):
    bot.add_cog(Util(bot))
