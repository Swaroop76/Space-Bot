import nextcord
import aiohttp
from nextcord.ext import commands
from datetime import datetime
from dateutil import parser
from nextcord import Interaction, SlashOption, ChannelType, Embed

class APOD(commands.Cog, name="APOD"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def apod(self, ctx: commands.Context, date: str = None):
        api_url = "https://api.nasa.gov/planetary/apod"
        api_key = "z4VtSw6jVJcvt1FkXsusOPRpwHLatDWirJFvgY7K"  # Replace this with your actual NASA API key

        if date is not None:
            # Try to parse the date in various formats using dateutil.parser
            try:
                parsed_date = parser.parse(date).strftime("%Y-%m-%d")
            except ValueError:
                await ctx.send("Invalid date format. Please enter the date in a valid format.")
                return

            api_params = {"api_key": api_key, "date": parsed_date}
        else:
            api_params = {"api_key": api_key}

        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=api_params) as api:
                data = await api.json()

                if "code" in data:
                    await ctx.send(f"Error: {data['msg']}")
                    return

                apod_title = data.get("title", "APOD Data Unavailable")
                apod_date = data["date"]
                apod_text = data["explanation"]
                apod_img = data.get("url")
                apod_hqimg = data.get("hdurl")

                em = nextcord.Embed(title=apod_title, description=apod_text, type="rich", colour=0x7649fe)
                em.add_field(name=apod_date, value="")
                em.add_field(name="You can get the high-quality picture from this link below", value=apod_hqimg, inline=False)

                if apod_img:
                    em.set_image(url=apod_img)

                await ctx.send(embed=em)

    testingServerID = 864780873257975810
    testingServerID2 = 832881541582553108
    testingServerID3 = 899552421578162177
    
    @nextcord.slash_command(guild_ids=[testingServerID, testingServerID2, testingServerID3],description="Get the Astronomy Picture of the Day (APOD)")            
    async def apod(self, interaction: Interaction, date: str = SlashOption(description="Enter the date in YYYY-MM-DD format.")):
        api_url = "https://api.nasa.gov/planetary/apod"
        api_key = "z4VtSw6jVJcvt1FkXsusOPRpwHLatDWirJFvgY7K"  # Replace this with your actual NASA API key

        if date is not None:
            # Try to parse the date in various formats using dateutil.parser
            try:
                parsed_date = parser.parse(date).strftime("%Y-%m-%d")
            except ValueError:
                await interaction.response.send_message("Invalid date format. Please enter the date in a valid format.", ephemeral=True)
                return

            api_params = {"api_key": api_key, "date": parsed_date}
        else:
            api_params = {"api_key": api_key}

        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=api_params) as api:
                data = await api.json()

                apod_title = data.get("title", "APOD Data Unavailable")
                apod_date = data["date"]
                apod_text = data["explanation"]
                apod_img = data.get("url")
                apod_hqimg = data.get("hdurl")

                em = nextcord.Embed(title=apod_title, description=apod_text, type="rich", colour=0x7649fe)
                em.add_field(name=apod_date, value="")
                em.add_field(name="You can get the high-quality picture from this link below", value=apod_hqimg, inline=False)

                if apod_img:
                    em.set_image(url=apod_img)

                await interaction.response.send_message(embed=em)

def setup(bot):
    bot.add_cog(APOD(bot))


