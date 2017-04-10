import html2text
from discord.ext import commands

from overwatch_api import *

from tinydb import TinyDB, Query


class OWext():
    db = TinyDB('OW-servers.json')
    server_db = {}

    ow = OverwatchAPI('key')
    owRegions = ['us', 'eu', 'kr', 'cn', 'jp', 'global']

    def __init__(self, bot):
        self.bot = bot

    async def on_ready(self):
        print('mounting Overwatch dbs')
        server_record = Query()
        for server in self.bot.servers:
            r = self.db.search(server_record.name == server.name)
            if len(r) == 0:
                print("No records for {}... creating.".format(server.name))
                self.db.insert(
                    {'name': server.name, 'sid': server.id, 'dbFile': 'OW-{}.json'.format(server.id),
                     'announceChannel': None})
                r = self.db.search(server_record.name == server.name)
            print("mounting {}'s DB".format(server.name))
            self.server_db[server.id] = TinyDB(r[0]['dbFile'])

    @commands.command(pass_context=True)
    async def stats(self, ctx, user=None):
        await self.bot.delete_message(ctx.message)
        await self.bot.send_typing(ctx.message.channel)
        if user is not None:
            if len(ctx.message.mentions) == 0:
                await self.bot.say("you must @ one user in this command")
                return
            user = ctx.message.mentions[0].id
        else:
            user = ctx.message.author.id
        sdb = self.server_db[ctx.message.server.id]
        bnetlink = Query()
        u = sdb.search(bnetlink.userid == user)
        if len(u) < 1:
            await self.bot.say("User {} Does not appear to be linked".format(ctx.message.mentions[0].name))
            return
        u = u[0]
        r = self.ow.get_profile(PC, u['bnetregion'], u['bnetid'])['data']
        Statement = "**{}**\r\n".format(r['username'])
        Statement += "Level:\t{}\r\n".format(r['level'])
        Statement += "Rank:\t{} - {}\r\n".format(r['competitive']['rank'], self.getRank(int(r['competitive']['rank'])))
        wins = int(r['games']['competitive']['wins'])
        losses = int(r['games']['competitive']['lost'])
        Statement += "W/L:\t{}/{}\r\n".format(wins, losses)
        Statement += "Win Ratio:\t{}%\r\n".format(int(round((wins / (wins + losses)) * 100)))
        await self.bot.say(Statement)

    @commands.command(pass_context=True)
    async def linkbnet(self, ctx, user, bnet, region):
        await self.bot.delete_message(ctx.message)
        await self.bot.send_typing(ctx.message.channel)
        bnet = bnet.replace('#', '-')
        if region not in self.owRegions:
            await self.bot.say("region must be one of {}".format(self.owRegions))
            return
        if len(ctx.message.mentions) == 0:
            await self.bot.say("you must @ one user in this command")
            return
        sdb = self.server_db[ctx.message.server.id]
        bnetlink = Query()
        if len(sdb.search(bnetlink.userid == ctx.message.mentions[0].id)) > 0:
            await self.bot.say("{} is is already linked to a Bnet account.".format(ctx.message.mentions[0].name))
            return
        try:
            owuser = self.ow.get_profile(PC, region, bnet)
        except:
            await self.bot.say("I cannot find that user.")
            return
        sdb.insert({'userid': ctx.message.mentions[0].id, 'bnetid': bnet, 'bnetregion': region})
        await self.bot.say('user {} linked with Bnet account {}'.format(ctx.message.mentions[0].name, bnet))

    @commands.command(pass_context=True)
    async def unlinkbnet(self, ctx, user):
        await self.bot.delete_message(ctx.message)
        await self.bot.send_typing(ctx.message.channel)
        print("starting unlink")
        bnetlink = Query()
        sdb = self.server_db[ctx.message.server.id]
        sdb.remove(bnetlink.userid == ctx.message.mentions[0].id)
        await self.bot.say('user {} unlinked'.format(ctx.message.mentions[0].name))

    @commands.command(pass_context=True)
    async def patchnotes(self, ctx):
        await self.bot.delete_message(ctx.message)
        await self.bot.send_typing(ctx.message.channel)
        notes = self.ow.get_patch_notes()['patchNotes'][0]
        line = '-----PATCHNOTES----\r\n'
        line += 'Overwatch Version {}\r\n'.format(notes['patchVersion'])
        line += notes['detail']
        line = html2text.html2text(line)
        msgs = [line[i:i + 2000] for i in range(0, len(line), 2000)]
        for m in msgs:
            await self.bot.say(m)

    def getRank(self, rnum: int):
        if rnum < 1500:
            return "Bronze"
        elif rnum < 2000:
            return "Silver"
        elif rnum < 2500:
            return "Gold"
        elif rnum < 3000:
            return "Platinum"
        elif rnum < 3500:
            return "Diamond"
        elif rnum < 4000:
            return "Master"
        elif rnum < 5001:
            return "Grandmaster"
        else:
            "What the fuck is going on here?"


def setup(bot):
    bot.add_cog(OWext(bot))
