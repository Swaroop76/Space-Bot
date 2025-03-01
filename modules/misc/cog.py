import nextcord
from nextcord import Interaction, ButtonStyle, Embed
from nextcord.ext import commands
from nextcord.ui import Button, View
from nextcord import Intents


class Misc(commands.Cog, name="Misc"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith('stfu'):
            await message.channel.send("Me? or Carl bot??")
        if message.content.startswith('#bump'):
            await message.channel.send("/bump")

    @commands.command()
    async def hello(self, ctx):
        await ctx.channel.send('Hello!')

    @commands.command()
    async def introduce(self, ctx):
        await ctx.channel.send("Hi! I'm Space Bot. My purpose is to share some knowledge of Space and Astronomy. I'm currently being developed,so please don't mind if my services aren't working.I too have fun commands for you guys.")

    @commands.command()
    async def ping(self, ctx):
        await ctx.channel.send(f'pong! {round(ctx.bot.latency*1000)}ms')


    @commands.command()
    async def embed(self, ctx):
        embed = nextcord.Embed(title="test", description="working")
        embed.add_field(name= "h", value="o", inline=True)
        embed.set_image(url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Black_hole_-_Messier_87_crop_max_res.jpg/240px-Black_hole_-_Messier_87_crop_max_res.jpg")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Misc(bot))