import os
import discord
from discord.ext import commands, tasks
from discord_slash import SlashCommand, SlashCommandOptionType, SlashContext
import requests
import json
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

options2 = [
  {
    "name": "character",
    "description": "The name of the person behind the voice.",
    "required": True,
    "type": 3
  },
  {
    "name": "url",
    "description": "The URL you are hosting your dataset on. Example: Google drive, Mega.nz, or Dropbox.",
    "required": True,
    "type": 3
  },
  {
    "name": "image",
    "description": "OPTIONAL Image url of the subject.",
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

statusOptions = [
  {
    "name": "api",
    "description": "1 = GREEN, 2 = YELLOW, 3 = RED (offline)",
    "required": True,
    "type": 4
  },
  {
    "name": "website",
    "description": "1 = GREEN, 2 = RED (offline)",
    "required": True,
    "type": 4
  }
]

voiceOptions = [
  {
    "name": "channel",
    "description": "The channel to send the embed to.",
    "required": True,
    "type": 7
  }
]

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    change_status.start()

    
@tasks.loop(seconds=300)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))
""""
@client.event
async def on_member_join(member):
    await member.send('👋 **Welcome!**')
    await member.send(\"\"\"This is uberduck.ai's official discord community, here you can expect to talk about this project, request new voices onto the site, and maybe even learn a few things!
**FAQ**
> You can view our most asked questions about the website / project in the #faq channel in our server.
    \"\"\")
"""
@client.event
async def on_message(message):
    mention = f'<@!{client.user.id}>'
    if mention in message.content:
        await message.channel.send("Uberduck agent, reporting for duty!")


@slash.slash(name="voicesuggest", description="Suggest a voice to be added or to be made.", options=options, guild_ids = [768215836665446480])
async def voicesuggest(ctx: SlashContext, character = None, source = None, image = "https://media.discordapp.net/attachments/842511714406629376/842850806922870804/Titelloses_700_20210514205956.png?width=661&height=596", clip = "(none provided)"):

  role = discord.utils.get(ctx.guild.roles, name="Agreed")

  sup = discord.utils.get(ctx.guild.roles, name="Supporter")

  if sup in ctx.author.roles:
    color = 0xFF00E8
  elif ctx.author in ctx.guild.premium_subscribers:
    color = 0x00FFF2
  else:
    color = 0xfff714

  if role in ctx.author.roles:
    channel = client.get_channel(842496586361339914)
    embed=discord.Embed(title=character, color=color)
    embed.set_author(name="👋 Suggest a voice with /voicesuggest")
    try:
      embed.set_thumbnail(url=image)
    except:
      ctx.send("You inputted an invalid url (for the image) Using default instead.")
      embed.set_thumbnail(url="https://media.discordapp.net/attachments/842511714406629376/842850806922870804/Titelloses_700_20210514205956.png?width=661&height=596")
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

@slash.slash(name="dataset_request", description="Request that your dataset be trained.", options=options2, guild_ids = [768215836665446480])
async def dataset_request(ctx: SlashContext, character = None, url = None, image = "https://media.discordapp.net/attachments/842511714406629376/842850806922870804/Titelloses_700_20210514205956.png?width=661&height=596"):

  role = discord.utils.get(ctx.guild.roles, name="Agreed")

  if role in ctx.author.roles:
    channel = client.get_channel(843619158834020393)
    embed=discord.Embed(title=character, color=0x808080)
    embed.set_author(name="👋 Request your dataset with /dataset_request. Click the green checkmark to notify you are training on the dataset!")
    if image != None:
      embed.set_thumbnail(url=image)
    embed.add_field(name="URL", value=url, inline=True)
    embed.add_field(name="Requested by:", value=ctx.author.mention, inline=True)
    embed.add_field(name="Worked on by:", value="No one yet.", inline=True)
    msg = await channel.send(embed=embed)
    await msg.add_reaction("✅")
    await ctx.send("Sent training request!")
  else:
    await ctx.send("You are missing the Agreed role! Do so in <#842148452464853002>")

@slash.slash(name="voice_update", description="Staff only! It makes an embed onto the channel.", options=voiceOptions, guild_ids = [768215836665446480])
async def voice_update(ctx: SlashContext, channel = None):

  role = discord.utils.get(ctx.guild.roles, name="Staff")

  if role in ctx.author.roles:

    store = open("store.txt", "r+")
    update = open("update.txt", "r+")
    response = requests.get("https://api.uberduck.ai/voices")
    json_data = json.loads(response.text)
    update.truncate(0)

    with open("update.txt", "a") as fl:
      for name in json_data:
        fl.write(name["display_name"] + "\n")
      fl.close()


    change = []

    if os.stat("store.txt").st_size == 0:
      print("Empty, storing instead")
      with open("store.txt", "a") as fl:
        for name in json_data:
          fl.write(name["display_name"] + "\n")
      fl.close()
    else:
      count = 0
      updatelines = update.read().splitlines()
      storelines = store.read().splitlines()
      for line in updatelines:
        if line not in storelines:
          print("Different!")
          change.append(line)
          

      store.truncate(0)

      with open("store.txt", "a") as fl:
        for name in json_data:
          fl.write(name["display_name"] + "\n")
      

        count += 1

    if change == []:
      await ctx.send("It appears no new voices has been added onto the site.")

    else:
      

      for char in change:
        print("+ " + char)
      

      final = [change[x:x+8] for x in range(0, len(change),8)]

      for i in final:
        print (i)
        sendMsg = ["```diff\n"]

        for chars in i:
          print (chars)
          sendMsg.append("+ "+ chars + "\n")

        sendMsg.append("```")

        embed=discord.Embed(title="The following changes were made:", color=0xFFFF00)
        embed.set_author(name="👋 Voice updates!")
        embed.set_thumbnail(url="https://uberduck.ai/_next/image?url=%2Fuberduck.jpg&w=384&q=75")
        embed.add_field(name="-", value=''.join(sendMsg), inline=True)
        await channel.send(embed=embed)
      change.clear()
      sendMsg.clear()
      await ctx.send("Sent the update!")
  else:
    await ctx.send("You arent staff.")

@slash.slash(name="why_isnt_the_site_working", description="run this command to find out", guild_ids = [768215836665446480])
async def why_isnt_the_site_working(ctx: SlashContext):
  await ctx.send(ctx.author.mention + " Look near the bottom of: <#841422801965416538>")


@slash.slash(name="status", description="Moderators only!", guild_ids = [768215836665446480], options=statusOptions)
async def changeStatus(ctx: SlashContext, api = None, website = None):

  role = discord.utils.get(ctx.guild.roles, name="Staff")

  if role in ctx.author.roles:

    color = 0x45FF00

    statusChannel = client.get_channel(842838618511114280)

    if api == 3:
      api = "🔴 Offline"
      color = 0xC30000
      await statusChannel.edit(name = "🔴status")
    elif api == 2:
      api = "🟡 Slow"
      color = 0xF1FF00
      await statusChannel.edit(name = "🟡status")
    else:
      api = "🟢 Healthy"
      await statusChannel.edit(name = "🟢status")

    if website == 2:
      website = "🔴 Offline"
    else:
      website = "🟢 Online"

    await statusChannel.purge()

    embed=discord.Embed(title="Website / API status", color=color)

    embed.set_author(name="ℹ️ Status")

    embed.add_field(name="API", value=api, inline=True)

    embed.add_field(name="Website", value=website, inline=True)

    embed.set_footer(text="ℹ️ Status updated by staff.")

    await statusChannel.send(embed=embed)

    await ctx.send("Updated!")

  else:

    await ctx.send("You aren't apart of staff.")

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
          #await user.send("You need to be a member of the patreon to do this!")
  
  elif message.channel == client.get_channel(843619158834020393):
    if user != client.user:

      embed_dict = message.embeds[0]

      for i, item in enumerate(embed_dict.fields):

        if i == 2:
          print(item)
          if user.mention == item.value:
            
            #await user.send("You have stopped work on training.")
            embed_dict.set_field_at(index=2, name=item.name, inline=item.inline, value="No one yet.")

            embed_dict.color = 0x808080

            await message.edit(embed=embed_dict)
            await message.remove_reaction(payload.emoji, user)

            break


          else:

            embed_dict.color = 0x00FF00

            embed_dict.set_field_at(index=2, name=item.name, inline=item.inline, value=user.mention)

            #await user.send("You have chosen that you are training the dataset! If this is a mistake, uncheck the checkmark!")

            await message.edit(embed=embed_dict)
            await message.remove_reaction(payload.emoji, user)

            break


keep_alive()


client.run(token)
