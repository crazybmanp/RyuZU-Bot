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
                print(d)
                r, l = map(int, d.split('d'))
                print("{} \ {}".format(r, l))
                if r > 100 or l > 1000000:
                    await self.bot.say("You cannot roll more than 100 dice, or dice bigger than 1 million sides.")
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
            print("Rolling {}d{}".format(r, l))
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

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """Gives a pong message as quickly as it can."""
        m = await self.bot.say("PONG!")
        td = m.timestamp - ctx.message.timestamp
        await self.bot.edit_message(m, new_content="PONG! ({})".format(td))


def setup(bot):
    bot.add_cog(Util(bot))
