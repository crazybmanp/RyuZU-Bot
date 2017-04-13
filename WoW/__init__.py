import discord
from discord.ext import commands
import requests

from RyuZU.Core import Cog
from .constants import *

FileVersion = "0.1"
default_settings = {"api_key": ""}

urls = {"character": "https://us.api.battle.net/wow/character/"}


class WoW(Cog):
    @property
    def has_key(self):
        return not self.bot.config['WoW']['api_key'] == ""

    async def no_key(self):
        await self.bot.say(":no_entry: This cog needs an API key for all operations and none were given. :no_entry:")

    @commands.group(pass_context=True)
    async def wow(self, ctx):
        if not self.has_key:
            await self.no_key()
        elif ctx.invoked_subcommand is None:
            await self.bot.say("Please use {}help wow for more information about the available subcommands.".format(
                self.bot.config['command_string']))

    @wow.command()
    async def character(self, cname, realm):
        if self.has_key:
            params = {"fields": "items,stats,talents", "locale": "en_US", "apikey": self.bot.config['WoW']['api_key']}
            r = requests.get("{}{}/{}".format(urls['character'], realm, cname), params=params)

            if r.status_code == 404:
                await self.bot.say("I could not find a character by that name on that realm.")
            else:
                r = r.json()
                e = discord.Embed(type="rich", title=r['name'],
                                  url="http://us.battle.net/wow/en/character/{}/{}/advanced".format(r['realm'], r['name']),
                                  color=discord.Color(CLASS_COLORS[CLASS_ID_MAP[r['class']]]))
                e.set_thumbnail(url="http://render-api-us.worldofwarcraft.com/static-render/us/{}".format(r['thumbnail']))
                e.add_field(name="Level", value=r['level'])
                e.add_field(name="Race", value=RACE_ID_MAP[r['race']], inline=True)
                e.add_field(name="Class", value=CLASS_ID_MAP[r['class']], inline=True)
                e.add_field(name="Item Level", value=r['items']['averageItemLevelEquipped'], inline=True)
                e.add_field(name="Health", value=r['stats']['health'])
                e.add_field(name="Armor", value=r['stats']['armor'])
                e.add_field(name="Crit", value="%.2f%%" % r['stats']['crit'], inline=True)
                e.add_field(name="Haste", value="%.2f%%" % r['stats']['haste'], inline=True)
                e.add_field(name="Mastery", value="%.2f%%" % r['stats']['mastery'], inline=True)

                await self.bot.say(embed=e)
        else:
            await self.no_key()


def setup(bot):
    bot.add_cog(WoW(bot, FileVersion, default_settings))
