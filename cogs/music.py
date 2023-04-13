
import discord
from discord.ext import commands

import os
import asyncio

from cogs.utils.link_processing import LinkProcessing
from cogs.utils.song_queue import Song, Queue
from cogs.utils.downloader import Downloader
from cogs.utils.embed_templates import EmbedTemplates


# ♫

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.ffmpeg_path = "ffmpeg"
        if os.path.isfile("cogs/utils/ffmpeg.exe"):
            self.ffmpeg_path = "cogs/utils/ffmpeg.exe"

        self.vc = None
        self.id = 0 
        self.playing = False

        self.DLer = Downloader()
        self.queue = Queue()

    async def remove_file(self, file_name):
        if os.path.exists(f"{self.DLer.download_path}{file_name}"):
            await asyncio.sleep(2)
            os.remove(f"{self.DLer.download_path}{file_name}")


    @commands.command()
    async def join_vc(self, ctx):
        if self.vc == None or not self.vc.is_connected():   
            if ctx.author.voice:
                voice_channel = ctx.message.author.voice.channel
                self.vc = await voice_channel.connect()    
            else:
                await ctx.channel.send(
                    embed=EmbedTemplates.generic_text("❗ You have to be in voice chat", 'red')
                )
                return False
        return True


    @commands.command(aliases=['p'])
    async def play(self, ctx, *args, next=False):
        connected = await self.join_vc(ctx)
        if not connected:
            return
    
        if len(args) < 1:
            await ctx.channel.send(
                embed=EmbedTemplates.generic_text("❗ No arguments for !play", 'red'))
            return

        output = LinkProcessing.process(args)

    
        self.id += 1

        try:
            info, file = self.DLer.download(link=output, name=str(self.id))
        except Exception:
            await ctx.channel.send(embed=EmbedTemplates.generic_text("❗ Source isn't available", 'red'))

        author = ctx.message.author
        song = Song(
                    file=file, 
                    url=output, 
                    info=info, 
                    author_nick=author.name, 
                    author_avatar_url=author.avatar
                )
        
        self.queue.add(song, first=next)

        await ctx.channel.send(embed=EmbedTemplates.song_large(
            song=song, queue=self.queue))

        if self.playing == False:
            await self.song_loop(ctx)


    @commands.command()
    async def song_loop(self, ctx, file_to_delete=""):
        if file_to_delete != "":
            asyncio.run_coroutine_threadsafe(self.remove_file(file_to_delete), self.bot.loop)

        if not self.vc == None and self.vc.is_connected():
            self.playing = True
            if 0 < self.queue.lenght():
                song = self.queue.pop(0)
                # after func must be corutine running in bot main loop (must be awaiten)
                self.vc.play(discord.FFmpegPCMAudio(
                        executable=self.ffmpeg_path, 
                        source=f"{self.DLer.download_path}{song.file}"),
                        after = lambda e: asyncio.run_coroutine_threadsafe(
                    self.song_loop(ctx, file_to_delete=song.file), self.bot.loop)
                )
            else:
                self.playing = False
        else:
            self.playing = False


    @commands.command(aliases=['s'])
    async def skip(self, ctx):
        if not self.vc == None and self.vc.is_connected():
            self.vc.stop()

            await ctx.send(embed=EmbedTemplates.generic_text(
                    "⏭️ Skipping", "green"))


    @commands.command()
    async def pause(self, ctx):
        if not self.vc == None and self.vc.is_connected():
            if not self.vc.is_paused():
                self.vc.pause()
                await ctx.send(embed=EmbedTemplates.generic_text(
                    "⏸️  Paused", "green"))
            else:
                self.vc.resume()
                await ctx.send(embed=EmbedTemplates.generic_text(
                    "▶️  Resumed", "green"))


    @commands.command()
    async def resume(self, ctx):
        if not self.vc == None and self.vc.is_connected():
            if self.vc.is_paused():
                self.vc.resume()

                await ctx.send(embed=EmbedTemplates.generic_text(
                    "▶️  Resumed", "green"))


    @commands.command(aliases=['rm_last'])
    async def remove_last(self, ctx):
        if self.queue.lenght() > 0:
            song = self.queue.pop(-1)
            await ctx.send(embeds=[
                EmbedTemplates.generic_text("🗑️ Song succesfuly removed from queue", "green"),
                EmbedTemplates.song_small(song),
                ]
                )
        else:
            await ctx.send(embed=EmbedTemplates.generic_text(
                "🗑️ Queue is empty", "red"))


    @commands.command(aliases=['info'])
    async def help(self, ctx):
        await ctx.send(embed=EmbedTemplates.help())


async def setup(bot):
    await bot.add_cog(Music(bot))
