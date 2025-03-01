import nextcord
from nextcord import Interaction
from nextcord.ui import button
from nextcord.ext import commands

class Hello(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @button(label="click me", style=nextcord.ButtonStyle.green)
    async def hi(self, button, interaction: Interaction):
        await interaction.response.send_message("yo wassup", ephemeral = True)
        self.value = True
        self.stop()

class Buttons(commands.Cog, name="Buttons"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        view = Hello()
        await ctx.send("hi", view=view)
        await view.wait()
        if view.value is None:
            return
        elif view.value:
            await ctx.send("sup")
        else:
            await ctx.send("hello")

def setup(bot):
    bot.add_cog(Buttons(bot))