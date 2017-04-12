from random import choice

import requests
from discord.ext import commands

from RyuZU.Core import Cog
from .helpers import prune_respects


class Memes(Cog):
    f_server_db = {}

    async def on_ready(self):
        print('mounting Memes dbs')
        for server in self.bot.servers:
            print("mounting {}'s DB".format(server.name))
            self.f_server_db[server.id] = self.get_cog_db("respects-{}".format(server.id))

    @commands.command()
    async def bass(self):
        await self.bot.say("THE FUCKIN :fish:BASS:fish: IS FUCKIN **RAW**! https://puu.sh/kPpgM.webm")

    @commands.command()
    async def brainpower(self):
        options = [
            "O-oooooooooo AAAAE-A-A-I-A-U- JO-oooooooooooo AAE-O-A-A-U-U-A- E-eee-ee-eee AAAAE-A-E-I-E-A- JO-ooo-oo-oo-oo EEEEO-A-AAA-AAAA",
            "∀∀∀∀-∀∀∀-∀-OƎƎƎƎ oo-oo-oo-ooo-Oſ -∀-Ǝ-I-Ǝ-∀-Ǝ∀∀∀∀ ǝǝǝ-ǝǝ-ǝǝǝ-Ǝ -∀-∩-∩-∀-∀-O-Ǝ∀∀ oooooooooooo-Oſ -∩-∀-I-∀-∀-Ǝ∀∀∀∀ oooooooooo-O",
            "𝓞-𝓸𝓸𝓸𝓸𝓸𝓸𝓸𝓸𝓸𝓸 𝓐𝓐𝓐𝓐𝓔-𝓐-𝓐-𝓘-𝓐-𝓤- 𝓙𝓞-𝓸𝓸𝓸𝓸𝓸𝓸𝓸𝓸𝓸𝓸𝓸𝓸 𝓐𝓐𝓔-𝓞-𝓐-𝓐-𝓤-𝓤-𝓐- 𝓔-𝒆𝒆𝒆-𝒆𝒆-𝒆𝒆𝒆 𝓐𝓐𝓐𝓐𝓔-𝓐-𝓔-𝓘-𝓔-𝓐-𝓙𝓞-𝓸𝓸𝓸-𝓸𝓸-𝓸𝓸-𝓸𝓸 𝓔𝓔𝓔𝓔𝓞-𝓐-𝓐𝓐𝓐-𝓐𝓐𝓐𝓐𝓐𝓐"]

        await self.bot.say("{0} https://www.youtube.com/watch?v=h-mUGj41hWA".format(choice(options)))

    @commands.command(aliases=["neko"])
    async def cat(self):
        """Gets a random cat picture."""
        r = requests.get("https://random.cat/meow").json()
        await self.bot.say(r['file'])

    @commands.command(aliases=["nekofact"])
    async def catfact(self):
        """A random fact about cats."""
        cat_emoji = (
        ":cat:", ":scream_cat:", ":heart_eyes_cat:", ":smirk_cat:", ":kissing_cat:", ":pouting_cat:", ":joy_cat:",
        ":smile_cat:")
        r = requests.get("http://catfacts-api.appspot.com/api/facts").json()
        await self.bot.say("{0} {1} {2}".format(choice(cat_emoji), r['facts'][0], choice(cat_emoji)))

    @commands.command(pass_context=True)
    async def feelsbadman(self, ctx):
        await self.bot.delete_message(ctx.message)
        await self.bot.say("https://openclipart.org/image/2400px/svg_to_png/222252/feels.png")

    @commands.command(pass_context=True)
    async def lenny(self, ctx):
        await self.bot.delete_message(ctx.message)
        await self.bot.say("( ͡° ͜ʖ ͡°)")

    @commands.command()
    async def mybrand(self):
        await self.bot.say("https://www.youtube.com/watch?v=V-fRuoMIfpw")

    @commands.command()
    async def oceanman(self):
        await self.bot.say(
            "OCEAN MAN 🌊 😍 Take me by the hand ✋ lead me to the land that you understand 🙌 🌊 OCEAN MAN 🌊 😍 The voyage 🚲 to the corner of the 🌎 globe is a real trip 👌 🌊 OCEAN MAN 🌊 😍 The crust of a tan man 👳 imbibed by the sand 👍 Soaking up the 💦 thirst of the land 💯 https://www.youtube.com/watch?v=6E5m_XtCX3c")

    @commands.command(pass_context=True)
    async def reeee(self, ctx):
        await self.bot.delete_message(ctx.message)
        await self.bot.say("http://i1.kym-cdn.com/entries/icons/original/000/017/830/b49.gif")

    @commands.command()
    async def spaghetti(self):
        await self.bot.say(
            "His palms :spaghetti:, knees weak, arms :spaghetti:. There's vomit on his :spaghetti: already; mom's :spaghetti:. He's nervous, but on the surface he looks calm :spaghetti:. To drop :spaghetti:, but he keeps on :spaghetti: what he wrote down, the whole crowd goes :spaghetti:, he opens his mouth, but :spaghetti: won't come out, he's choking, how? Everybody's joking now! The :spaghetti:'s run out, time's up, over - BLAOW! https://www.youtube.com/watch?v=SW-BU6keEUw")

    @commands.command(pass_context=True, aliases=["f"])
    async def payrespects(self, ctx):
        sdb = self.f_server_db[ctx.message.server.id]
        prune_respects(sdb)
        sdb.insert({'timestamp': ctx.message.timestamp.strftime('%b %d %Y %I:%M%p')})
        await self.bot.say("{} people have paid respects today. o7".format(len(sdb)))


def setup(bot):
    bot.add_cog(Memes(bot))
