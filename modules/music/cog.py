import nextcord
import os
from nextcord.ext import commands
import wavelink
from wavelink.ext import spotify

class Music(commands.Cog, name="Music"):
    def __init__(self, bot):
        self.bot = bot 

    @commands.command()
    async def play(self, ctx: commands.Context, *, search: wavelink.YouTubeMusicTrack):
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        elif ctx.author.voice is None:
            return await ctx.send("JOIN A VC SO THAT I CAN SEE YOU")
        else:
            vc: wavelink.Player = ctx.voice_client
        if vc.queue.is_empty and not vc.is_playing():
            await vc.play(search)
            await ctx.send(f"Now playing {search.title}")
        else:
            await vc.queue.put_wait(search)
            await ctx.send(f"Added '{search.title}' to the queue ")
        vc.ctx = ctx
        setattr(vc, "loop", False)
        
    @commands.command()
    async def pause(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("Nothing is playing right now")
        elif ctx.author.voice is None:
            return await ctx.send("JOIN A VC SO THAT I CAN SEE YOU")
        else:
            vc: wavelink.Player = ctx.voice_client
        await vc.pause()
        await ctx.send("Paused.")

    @commands.command()
    async def resume(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("Nothing is playing right now")
        elif ctx.author.voice is None:
            return await ctx.send("Please join a vc before playing the music.")
        else:
            vc: wavelink.Player = ctx.voice_client
        await vc.resume()
        await ctx.send("Resumed.")

    @commands.command()
    async def stop(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("Nothing is playing right now")
        elif ctx.author.voice is None:
            return await ctx.send("Please join a vc before playing the music.")
        else:
            vc: wavelink.Player = ctx.voice_client
        await vc.stop()
        await ctx.send("The music has been stopped.")

    @commands.command()
    async def disconnect(self, ctx: commands.Context):
        if ctx.author.voice is None:
            return await ctx.send("JOIN A VC SO THAT I CAN SEE YOU")
        else:
            vc: wavelink.Player = ctx.voice_client
        await vc.disconnect()
        await ctx.send("Disconnected Successfully.")

    @commands.command()
    async def is_looping(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx
        
    @commands.command()
    async def splay(self,ctx: commands.Context, *, search: str):
        if not ctx.voice_client:
            vc: wavelink.Player=await ctx.author.voice.channel.connect(cls=wavelink.Player)
        elif ctx.author.voice is None:
            return await ctx.send("JOIN A VC SO THAT I CAN SEE YOU")
        else:
            vc: wavelink.Player=ctx.voice_client
        if vc.queue.is_empty and not vc.is_playing():
            try:
                track= await spotify.SpotifyTrack.search(query=search,return_first=True)
                await vc.play(track)
                await ctx.send(f"Now playing {track.title}")
            except Exception as e:
                await ctx.send("Please enter a spotify **song url**.")
                return print(e)            
        else:
            await vc.queue.put_wait(search)
            await ctx.send(f"Added '{search.title}' to the queue ")    
        vc.ctx=ctx
        if vc.is_looping:
            return
        setattr(vc,"loop",False)
    
    @commands.command()
    async def skip(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("Nothing is playing right now")
        elif ctx.author.voice is None:
            return await ctx.send("JOIN A VC SO THAT I CAN SEE YOU")
        else:
            vc: wavelink.Player = ctx.voice_client
        if vc.is_playing():
            await vc.pause()
            if not vc.queue.is_empty:
                search = await vc.queue.get()
                tracks = await self.bot.wavelink.get_tracks(f'ytsearch:{search.query}')
                await vc.play(tracks[0])
                await ctx.send(f"Now playing {tracks[0].title}")
            else:
                await ctx.send("The queue is empty. Disconnecting...")
                await vc.disconnect()
            await vc.resume()
        else:
            await ctx.send("Nothing is playing right now")
        vc.ctx = ctx
        if vc.is_looping:
            return
        setattr(vc, "is_looping", False)



    @commands.command()
    async def queue(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("Im not even in a vc")
        elif not ctx.author.voice:
            return await ctx.send("join a vc please")
        else:
            vc: wavelink.Player=ctx.voice_client

        if vc.queue.is_empty:
            return await ctx.send("Queue is empty")

        em=nextcord.Embed(title="Queue")
        queue=vc.queue.copy()
        song_count=0
        for song in queue:
            song_count+=1
            em.add_field(name=f"Song Num {song_count}",value=f"'{song.title}'")

        return await ctx.send(embed=em)
          
def setup(bot):
    bot.add_cog(Music(bot))
