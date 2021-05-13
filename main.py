import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashCommandOptionType, SlashContext

from web import keep_alive

token = os.environ['discord']

client = discord.Client()
slash = SlashCommand(client, sync_commands = True)

channel = client.get_channel("794028287428132884")

options = [
  {
    "name": "Character",
    "description": "The name of the person behind the voice.",
    "required": True,
    "type": 3
  },
  {
    "name": "Source",
    "description": "The name of the show / source where the voice originates from.",
    "required": True,
    "type": 3
  },
  {
    "name": "Image_URL",
    "description": "OPTIONAL Image url of the subject.",
    "required": False,
    "type": 3
  },
  {
    "name": "YT_Clip",
    "description": "OPTIONAL Youtube link for the voice clips.",
    "required": False,
    "type": 3
  }
]

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@slash.slash(name="voice_suggest", description="Suggest a voice to be added or to be made.", guild_ids[644989802696933387, 768215836665446480], options = options)
async def guess(ctx: SlashContext, Character = None, Source = None, Image_URL = None, YT_Clip = None):
  if Character != None and Source != None:
    embed=discord.Embed(title="-", color=0xfff714)
    embed.set_author(name=Character)
    embed.add_field(name="Source", value=Source, inline=True)
    embed.add_field(name="Voice Clip", value=YT_Clip, inline=True)
    embed.add_field(name="Suggested by:", value=ctx.message.author.mention, inline=False)
    embed.set_footer(text="👋 Thumbs up or Thumbs down this message to vote!")
    msg = await channel.send(embed=embed)
    msg.add_reaction("👍")
    msg.add_reaction("👎")
  else:
    await ctx.reply("You are missing the Character name or Source!", mention_author=True)

keep_alive()

client.run(token)
