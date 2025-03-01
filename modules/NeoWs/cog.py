import aiohttp
from nextcord.ext import commands, menus
from nextcord.ui import Select
from datetime import datetime, timedelta
import nextcord
from nextcord import Interaction, SlashOption

testingServerID = 864780873257975810
testingServerID2 = 832881541582553108
testingServerID3 = 899552421578162177

class NeoWs(commands.Cog, name="NeoWs"):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids=[testingServerID, testingServerID2, testingServerID3], name="neows", description="Get information about Near Earth Objects")
    async def neows(self, interaction: Interaction, start_date: str = SlashOption(description="Enter the start date",required=False), end_date: str = SlashOption(description="Enter the end date", required=False)):
        await interaction.response.defer()  # Defer the interaction to avoid timeout

        api_url = "https://api.nasa.gov/neo/rest/v1/feed"
        api_key = "z4VtSw6jVJcvt1FkXsusOPRpwHLatDWirJFvgY7K"  # Replace this with your actual NASA API key

        if start_date is None:
            start_date = datetime.today().strftime('%Y-%m-%d')
        if end_date is None:
            end_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")

        api_params = {"start_date": start_date, "end_date": end_date, "api_key": api_key}

        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=api_params) as response:
                if response.status == 200:
                    data = await response.json()
                    embed_description = ""  # Initialize an empty string to store all asteroid messages
                    for date, asteroids in data['near_earth_objects'].items():
                        for asteroid in asteroids:
                            name = asteroid['name']
                            close_approach_date = asteroid['close_approach_data'][0]['close_approach_date']
                            embed_description += f"Asteroid {name} has a close approach date of {close_approach_date}\n"

                    # Use a single Embed with all asteroid messages
                    if embed_description:  # Check if there's any description to add
                        em = nextcord.Embed(title="NeoWs - Near Earth Objects", description=embed_description, type="rich", colour=0x7649fe)
                        await interaction.followup.send(embed=em)
                    else:
                        await interaction.followup.send("No asteroids found.", ephemeral=True)
                else:
                    await interaction.followup.send("Failed to fetch data from the API.", ephemeral=True)

def setup(bot):
    bot.add_cog(NeoWs(bot))