import random

from discord.ext import commands
from tinydb import TinyDB, Query


class Quotes:
    db = TinyDB('Quote-servers.json')
    server_db = {}

    def __init__(self, bot):
        self.bot = bot

    async def on_ready(self):
        print('mounting Quote dbs')
        server_record = Query()
        for server in self.bot.servers:
            r = self.db.search(server_record.sid == server.id)
            if len(r) == 0:
                print("No records for {}... creating.".format(server.name))
                self.db.insert(
                    {'name': server.name, 'sid': server.id, 'dbFile': 'Quote-{}.json'.format(server.id),
                     'announceChannel': None})
                r = self.db.search(server_record.name == server.name)
            print("mounting {}'s DB".format(server.name))
            self.server_db[server.id] = TinyDB(r[0]['dbFile'])

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
        sdb = self.server_db[ctx.message.server.id]
        sdb.remove(eid=quotenum)
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
        line = ""
        for quote in quotes:
            qnum = quote.eid
            if quote["category"] is None:
                line += "{}:`{}`\r\n".format(qnum, quote["quote"])
            else:
                line += "{}({}):`{}`\r\n".format(qnum, quote["category"], quote["quote"])
        msgs = [line[i:i + 2000] for i in range(0, len(line), 2000)]
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
    bot.add_cog(Quotes(bot))
