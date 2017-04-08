from discord.ext import commands


class Admin:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def purge(self, ctx, messages=100):
        """Purges all (100 by default) previous messages from chat."""
        if not ctx.message.author.permissions_in(ctx.message.channel).manage_messages:
            await self.bot.say("Only Admins are allowed to purge the chat.")
            return
        await self.bot.say("purging {} messages".format(messages))
        messages += 2  # account for command and feedback
        await self.bot.purge_from(ctx.message.channel, limit=messages)

    @commands.command(pass_context=True)
    async def clean(self, ctx, messages=100):
        """Cleans all posts from this bot and any commands."""
        await self.bot.say("Cleaning...")
        message = ctx.message
        deleted = await self.bot.purge_from(message.channel, limit=messages, check=self.is_me)
        deleted += await self.bot.purge_from(message.channel, limit=messages, check=self.is_command)
        await self.bot.say('Deleted {} message(s)'.format(len(deleted)))

    def is_me(self, m):
        return m.author == self.bot.user

    def is_command(self, m):
        return m.content.startswith('!')


def setup(bot):
    bot.add_cog(Admin(bot))
