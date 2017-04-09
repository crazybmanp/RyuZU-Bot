import discord
from discord.ext import commands
from tinydb import TinyDB, Query


class Quotes():
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

    @commands.command(pass_context=True)
    async def addquote(self, ctx, quote, category=None):
        sdb = self.server_db[ctx.message.server.id]
        q = Query()
        if len(sdb.search(q.quote == quote)) > 0:
            await self.bot.say("\"{}\" is already a quote.".format(quote))
            return
        sdb.insert({'quote': quote, 'category': category})
        qnum = 0
        await self.bot.say("Added quote {}({}):\"{}\"".format(qnum, category, quote))

    @commands.command(pass_context=True)
    async def deleteqote(self, ctx, quotenum):
        sdb = self.server_db[ctx.message.server.id]
        sdb.remove(eid=quotenum)
        await self.bot.say("Removed quote #{}".format(quotenum))

    @commands.command(pass_context=True)
    async def editquote(self, ctx, quotenum):
        return

    @commands.command(pass_context=True)
    async def listquotes(self, ctx):
        sdb = self.server_db[ctx.message.server.id]
        quotes = sdb.all()
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

    @commands.command(pass_context=True)
    async def quote(self, ctx, param):
        """Gives you a quote either randomly, or given a category or quote number"""
        try:
            qnum = int(param)
        except ValueError:
            await self.bot.say("quote category: {}".format(param))
            return

        await self.bot.say("quote number: {}".format(qnum))
        sdb = self.server_db[ctx.message.server.id]
        quote = sdb.get(eid=qnum)
        if quote["category"] is None:
            await self.bot.say("{}:\"{}\"".format(qnum, quote["quote"]))
        else:
            await self.bot.say("{}({}):\"{}\"".format(qnum, quote["category"], quote["quote"]))



def setup(bot):
    bot.add_cog(Quotes(bot))
