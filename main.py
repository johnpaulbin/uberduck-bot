import os
import discord
from discord.ext import commands, tasks
from discord_slash import SlashCommand, SlashCommandOptionType, SlashContext
import itertools
from web import keep_alive

token = os.environ['discord']
activity = discord.Activity(name='over you!', type=discord.ActivityType.watching)

status = itertools.cycle(['uberduck.ai','with voice synthesizers'])

client = commands.Bot(command_prefix="!", intents=discord.Intents.all(), activity=activity)
slash = SlashCommand(client, sync_commands = True)


options = [
  {
    "name": "character",
    "description": "The name of the person behind the voice.",
    "required": True,
    "type": 3
  },
  {
    "name": "source",
    "description": "The name of the show / source where the voice originates from.",
    "required": True,
    "type": 3
  },
  {
    "name": "image",
    "description": "OPTIONAL Image url of the subject.",
    "required": False,
    "type": 3
  },
  {
    "name": "clip",
    "description": "OPTIONAL Youtube link for the voice clips.",
    "required": False,
    "type": 3
  }
]

announcement = [
  {
    "name": "title",
    "description": "Title of the announcement",
    "required": True,
    "type": 3
  },
  {
    "name": "body",
    "description": "Body of the announcement",
    "required": True,
    "type": 3
  },
  {
    "name": "channel",
    "description": "channel",
    "required": True,
    "type": 7
  }
]

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    change_status.start()
    
@tasks.loop(seconds=10)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))

@slash.slash(name="voicesuggest", description="Suggest a voice to be added or to be made.", options=options, guild_ids = [768215836665446480])
async def voicesuggest(ctx: SlashContext, character = None, source = None, image = None, clip = None):

  role = discord.utils.get(ctx.guild.roles, name="Agreed")

  if role in ctx.author.roles:
    channel = client.get_channel(842496586361339914)
    embed=discord.Embed(title=character, color=0xfff714)
    embed.set_author(name="👋 Suggest a voice with /voicesuggest")
    if image != None:
      embed.set_thumbnail(url=image)
    embed.add_field(name="Source", value=source, inline=True)
    embed.add_field(name="Voice Clip", value=clip, inline=True)
    embed.add_field(name="Suggested by:", value=ctx.author.mention, inline=False)
    embed.set_footer(text="👋 Thumbs up or Thumbs down this message to vote!")
    msg = await channel.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")
    await msg.add_reaction("<:patreon:843022446675886110>")
    await ctx.send("Sent voice request!")
  else:
    await ctx.send("You are missing the Agreed role! Do so in <#842148452464853002>")

@slash.slash(name="announce", description="Moderators only", options=announcement, guild_ids = [768215836665446480])
async def announce(ctx: SlashContext, title = None, body = None, channel = None):

  role = discord.utils.get(ctx.guild.roles, name="Staff")

  if role in ctx.author.roles:



    #channel = client.get_channel(channel)
    embed=discord.Embed(title=title, color=0xfff714)
    embed.set_author(name="ℹ️ Announcement")
    if channel != None:
      embed.add_field(name="-", value=body, inline=True)
      embed.set_footer(text="ℹ️ Announcement created by staff.")
      await channel.send(embed=embed)
      await ctx.send("Sent!")
    else:
      ctx.send("Missing channel")
  else:
    await ctx.send("You aren't apart of staff.")

@client.event
async def on_raw_reaction_add(payload):

  channel = client.get_channel(payload.channel_id)
  message = await channel.fetch_message(payload.message_id)
  user = message.guild.get_member(payload.user_id)


  patreon = client.get_emoji(843022446675886110)

  role = discord.utils.get(message.guild.roles, name="Supporter")

  if message.channel == client.get_channel(842496586361339914):
    if user != client.user:
      if payload.emoji == patreon:
        if role in user.roles:
          pass
        else:
          await message.remove_reaction(payload.emoji, user)
          await user.send("You need to be a member of the patreon to do this!")

keep_alive()


client.run(token)
