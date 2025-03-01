import os
import requests 
import nextcord
import logging
import json
import wavelink
from wavelink.ext import spotify
from keep_alive import keep_alive
from replit import db
from nextcord.abc import GuildChannel
from nextcord.ext import commands
from typing import List
from nextcord import Intents

my_intents = Intents.default()
my_intents.message_content = True

bot = commands.Bot(command_prefix='#',intents=my_intents)

@bot.event
async def on_ready():
  print("We logged in as {0.user}".format(bot))
  await node_connect()

@bot.event  
async def node_connect():
  await bot.wait_until_ready()
  await wavelink.NodePool.create_node(bot=bot,host='lavalink.mariliun.ml',port=443,password='lavaliun',https=True, spotify_client=spotify.SpotifyClient(client_id="410e666cc43640c49b846a2d02d75e51", client_secret="0f4497f664c1492abca77279784f6892"))

@bot.event
async def on_wavelink_node_ready(node: wavelink.Node):
  print(f"Node {node.identifier} is ready!")

@bot.event
async def on_wavelink_track_end(player: wavelink.Player, track: wavelink.Track, reason):
   ctx = player.ctx
   vc: player=ctx.voice_client

   if vc.loop:
    return await vc.play(track)
   
   next_song=vc.queue.get()
   await vc.play(next_song)
   await ctx.send(f"Now playing: {next_song.title}")
   
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    
for folder in os.listdir("modules"):
    if os.path.exists(os.path.join("modules", folder, "cog.py")):
        bot.load_extension(f"modules.{folder}.cog")

key='insert_key_here'
keep_alive()
bot.run(key)