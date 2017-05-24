import random

from discord.ext import commands
from tinydb import Query

from RyuZU.Core import Cog

FileVersion = "1.0"


class Quotes(Cog):
    server_db = {}

    async def on_ready(self):
        print('mounting Quote dbs')
        for server in self.bot.servers:
            print("mounting {}'s DB".format(server.name))
            self.server_db[server.id] = self.get_cog_db(server.id)

    @commands.group(pass_context=True)
    async def quote(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say("Please use sub-commands: give, list, add, or delete.")

    @quote.command(pass_context=True)
    async def give(self, ctx, param=None):
        """Gives you a quote either randomly, or given a category or quote number
        :param: Either the quote number to quote, or a category to grab a quote randomly from.
        """
        sdb = self.server_db[ctx.message.server.id]
        q = Query()
        try:
            qnum = int(param)
        except (ValueError, TypeError):
            l = sdb.search(q.category == param)
            if len(l) < 1:
                await self.bot.say("That category does not exist")
                return
            quote = random.choice(l)
            await self.SayQuote(quote.eid, quote)
            return

        quote = sdb.get(eid=qnum)
        await self.SayQuote(qnum, quote)

    @quote.command(pass_context=True)
    async def add(self, ctx, quote, category=None):
        """ adds a quote to the database
        :quote: The quote to add, wrap it in quotes
        :category: an optional category to place the quote under.
        """
        sdb = self.server_db[ctx.message.server.id]
        q = Query()
        if len(sdb.search(q.quote == quote)) > 0:
            await self.bot.say("\"{}\" is already a quote.".format(quote))
            return
        qnum = sdb.insert({'quote': quote, 'category': category})
        await self.bot.say("Added quote {}({}):\"{}\"".format(qnum, category, quote))

    @quote.command(pass_context=True)
    async def delete(self, ctx, quotenum):
        """Deletes the quote at the given quote index.
        :quotenum: The number of the quote to be deleted
        """
        if not ctx.message.author.permissions_in(ctx.message.channel).manage_messages:
            await self.bot.say("Only Admins are allowed to delete quotes.")
            return
        try:
            q = int(quotenum)
        except ValueError:
            # Handle the exception
            await self.bot.say("The quote number must actually be a number.")
            return

        sdb = self.server_db[ctx.message.server.id]
        try:
            sdb.remove(eids=[q])
        except KeyError:
            await self.bot.say("That key does not exist.")
            return
        await self.bot.say("Removed quote #{}".format(quotenum))

    @quote.command(pass_context=True)
    async def list(self, ctx, category=None):
        """Lists all quotes or all quotes of a given category
        :category: The [Optional] category to list quotes from.
        """
        sdb = self.server_db[ctx.message.server.id]
        q = Query()
        if category is None:
            quotes = sdb.all()
        elif category == "None":
            quotes = sdb.search(q.category == None)
        else:
            quotes = sdb.search(q.category == category)
        if len(quotes) < 1:
            await self.bot.say("No quotes found, are you sure you have the right category?")
        msgs = []
        line = ""
        for quote in quotes:
            qnum = quote.eid
            if quote["category"] is None:
                l = "{}:`{}`\r\n".format(qnum, quote["quote"])
            else:
                l = "{}({}):`{}`\r\n".format(qnum, quote["category"], quote["quote"])
            if len(line) + len(l) > 2000:
                msgs.append(line)
                line = ""
            line += l
        msgs.append(line)
        for m in msgs:
            await self.bot.say(m)

    @quote.command(pass_context=True)
    async def categories(self, ctx):
        """
        Lists all quote categories.
        """
        sdb = self.server_db[ctx.message.server.id]
        quotes = sdb.all()
        categories = []
        for quote in quotes:
            if quote["category"] not in categories:
                categories.append(quote["category"])
        line = "Categories: \r\n"
        for c in categories:
            line += "\r\n{}".format(c)
        await self.bot.say(line)

    async def SayQuote(self, qnum, quote):
        if quote["category"] is None:
            await self.bot.say("{}:\"{}\"".format(qnum, quote["quote"]))
        else:
            await self.bot.say("{}({}):\"{}\"".format(qnum, quote["category"], quote["quote"]))


def setup(bot):
    bot.add_cog(Quotes(bot, FileVersion))
