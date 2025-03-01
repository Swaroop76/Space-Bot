import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, ChannelType, Embed

class Slash(commands.Cog, name="Slash"):
    def __init__(self, bot):
        self.bot = bot

    testingServerID = 864780873257975810
    testingServerID2 = 832881541582553108
    testingServerID3 = 899552421578162177

    @nextcord.slash_command(guild_ids=[testingServerID, testingServerID2, testingServerID3], description="returns the ping")
    async def ping(self, interaction):
        await interaction.response.send_message(f'pong! {round(interaction.client.latency*1000)}ms')

    @nextcord.slash_command(guild_ids=[testingServerID, testingServerID2, testingServerID3], description="repeats the message you enter")
    async def echo(self, interaction, message:str):
        await interaction.response.send_message("echo sent!", ephemeral = True)
        await interaction.channel.send(message)
        embed = nextcord.Embed(description=f"**Echo sent in #{interaction.channel.name}**\n{message}")
        embed.set_author(name=f"{interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.display_avatar.url)
        await self.bot.get_guild(832881541582553108).get_channel(969982232334839848).send(embed=embed)

def setup(bot):
    bot.add_cog(Slash(bot))