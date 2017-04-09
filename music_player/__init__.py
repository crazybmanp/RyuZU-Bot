import asyncio
import math
import platform

import discord
from discord.ext import commands

if not discord.opus.is_loaded() and platform.system() == "Windows":
    discord.opus.load_opus('opus')


class PlaylistEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        return self.player.title

    @property
    def video_info(self):
        fmt = '*{0.title}* uploaded by {0.uploader} and requested by {1.display_name}'
        duration = self.player.duration
        if duration:
            fmt = fmt + ' [length: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return fmt.format(self.player, self.requester)


class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set()  # a set of user_ids that voted
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get()
            await self.bot.send_message(self.current.channel, ":notes:Now playing {0}:notes:".format(self.current.video_info))
            self.current.player.start()
            await self.play_next_song.wait()


class MusicPlayer:
    """Type !help music for a list of subcommands"""
    def __init__(self, bot):
        self.bot = bot
        self.channel = None
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state

        return state

    async def create_voice_client(self, channel):
        voice = await self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass

    @commands.group(pass_context=True)
    async def music(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    @music.command(name="join", pass_context=True)
    async def join(self, ctx):
        """The bot joins your current voice channel"""
        target = ctx.message.author.voice_channel

        if target is None:
            await self.bot.say('You are not in a voice channel.')
            return False

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = await self.bot.join_voice_channel(target)
        else:
            await state.voice.move_to(target)
        self.channel = ctx.message.author.voice.voice_channel
        return True

    @music.command(name="playlist", pass_context=True)
    async def playlist(self, ctx):
        """Shows the current playlist."""
        state = self.get_voice_state(ctx.message.server)
        msg = "```css\n{0}'s Playlist\n\n".format(self.bot.user.name)

        for s in state.songs._queue:
            msg = msg + "{0} : {1}\n".format(state.songs._queue.index(s) + 1, s)

        msg = msg + "```"

        await self.bot.say(msg)

    @music.command(name="q", pass_context=True)
    async def queue(self, ctx, *, song):
        """
        Starts playing audio. Joins your audio channel if it isn't there already. Adds your song to the queue if a song is already playing.
        """
        state = self.get_voice_state(ctx.message.server)
        opts = {'default_search': "auto", 'quiet': True}

        if state.voice is None:
            success = await ctx.invoke(self.join)
            if not success:
                return

        try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:
            await self.bot.delete_message(ctx.message)
            player.volume = 0.6
            entry = PlaylistEntry(ctx.message, player)
            await self.bot.say(entry.video_info)
            await state.songs.put(entry)

    @music.command(name="skip", pass_context=True)
    async def vote_skip(self, ctx):
        """Vote to skip the current song."""
        member_count = len(self.channel.voice_members) - 1  # total number of members in the channel, minus the bot
        state = self.get_voice_state(ctx.message.server)

        if member_count == 2 or member_count == 1:
            vote_req = 1
        else:
            vote_req = math.floor(member_count / 2)

        if not state.is_playing():
            await self.bot.say('Not playing any music right now...')
            return

        voter = ctx.message.author
        if voter == state.current.requester:
            await self.bot.say('Requester requested skipping song...')
            state.skip()
        elif voter.id not in state.skip_votes:
            state.skip_votes.add(voter.id)
            total_votes = len(state.skip_votes)
            if total_votes >= vote_req:
                await self.bot.say('Skip vote passed, skipping song...')
                state.skip()
            else:
                await self.bot.say('Skip vote added, currently at [{}/{}]'.format(total_votes, vote_req))
        else:
            await self.bot.say('You have already voted to skip this song.')

    @music.command(name="stop", pass_context=True)
    async def stop(self, ctx):
        """Stops playing audio and leaves the voice channel. This also clears the queue."""
        server = ctx.message.server
        state = self.get_voice_state(server)

        if state.is_playing():
            player = state.player
            player.stop()

        try:
            state.audio_player.cancel()
            del self.voice_states[server.id]
            await state.voice.disconnect()
        except:
            pass

    @music.command(name="volume", pass_context=True)
    async def volume(self, ctx, value: int):
        """Sets the volume of the currently playing song."""

        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.volume = value / 100
            await self.bot.say('Set the volume to {:.0%}'.format(player.volume))


def setup(bot):
    bot.add_cog(MusicPlayer(bot))
