from aiohttp import request
import discord
from discord.ext import commands
from discord.guild import Guild
from discord import app_commands
from discord.invite import Invite
from discord.ui import View, Button, button, Select
import os
import requests
import datetime

# Bot settings
BOT_TOKEN = "BOT_TOKEN_HERE"
BOT_PREFIX = "!"
BOT_LEAVE_WEBHOOK = "WEBHOOK_HERE"
BOT_JOIN_WEBHOOK = "WEBHOOK_HERE"
BOT_OWNER = "OWNER_NAME"
BOT_SUPPORTSERVER = "http://discord.gg/invite/example"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)
bot.remove_command("help")
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    synctree= await bot.tree.sync()
    print(f"Synced {len(synctree)} commands")
    print(f"https://discord.com/oauth2/authorize?client_id={bot.user.id}&permissions=8&integration_type=0&scope=bot")
    if not os.path.exists('./cogs'):
        os.makedirs('./cogs')
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
        else:
            print("No Cogs Found/Or Unable To Load Them")
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)
    
@bot.event
async def on_guild_join(guild):
    channel = guild.text_channels[0]
    invite = await channel.create_invite(max_age=3600)
    embed = {
        "title": f"{bot.user.name} has Joined A Server",
        "fields": [
            {
                "name": "Server Name",
                "value": f"{guild.name}",
                "inline": False
            },
            {
                "name": "Server id",
                "value": f"`{guild.id}`",
                "inline": False
            },
            {
                "name": "Member Count",
                "value": f"{guild.member_count}",
                "inline": False
            },
            {
                "name": "Server Count",
                "value": f"{len(bot.guilds)}",
                "inline": False
            },
            {
                "name": "Server Invite",
                "value": f"{invite.url}",
                "inline": False
            },
            
        ],
        "footer": {
            "text": f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        },
        "color": discord.Color.random().value
    }
    data = {
        "embeds": [embed],
        "username": f"{bot.user.name} Join Tracker"
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(BOT_JOIN_WEBHOOK, json=data, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
@bot.event
async def on_guild_remove(guild):
    
    embed = {
        "title": f"{bot.user.name} has been remove/left a server",
        "fields": [
            {
                "name": "Server Name",
                "value": f"{guild.name}",
                "inline": False
            },
            {
                "name": "Server Count",
                "value": f"{len(bot.guilds)}",
                "inline": False
            },
            
        ],
        "footer": {
            "text": f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        },
        "color": discord.Color.random().value
    }
    data = {
        "embeds": [embed],
        "username": f"{bot.user.name} Leave Tracker"
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(BOT_LEAVE_WEBHOOK, json=data, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    
# Basic commands
@bot.command(name="ping", description="Check the bot's latency")
async def ping(ctx):
    await ctx.send(f"Pong! ({bot.latency:.2f}ms)")

@bot.command(name="hello", description="Say hello to the bot")
async def hello(ctx):
    await ctx.send(f"Hello, {ctx.author.mention}!")

# Slash commands
@bot.tree.command(name="echo", description="Echo a message")
async def echo(interaction: discord.Interaction, *, message: str):
    await interaction.response.send_message(message)


class TestView(View):

  def __init__(self):
    super().__init__()
    self.add_item(
        Button(
            label="Bot Invite",
            url=f"https://discord.com/oauth2/authorize?client_id={bot.user.id}&permissions=8&integration_type=0&scope=bot",
            style=discord.ButtonStyle.link
        ))
    self.add_item(
        Button(
            label="Bot Support/Main Server",
            url=f"{BOT_SUPPORTSERVER}",
            style=discord.ButtonStyle.link
        ))

@bot.tree.command(name="serverinfo", description="Displays information about the server")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild

    embed = discord.Embed(title=f"Server Info: {guild.name}", color=discord.Color.random())

    embed.set_thumbnail(url=guild.icon.url)

    embed.add_field(name="Member Count", value=guild.member_count, inline=False)
    embed.add_field(name="Creation Date", value=guild.created_at.strftime("%B %d, %Y at %I:%M %p"), inline=False)
    embed.add_field(name="Owner", value=guild.owner.mention, inline=False)

    if guild.banner:
        embed.add_field(name="Server Banner", value=f"[Click to view]({guild.banner.url})", inline=False)

    invites = await guild.invites()
    invite = invites[0] if invites else None
    if invite:
        embed.add_field(name="Server Invite", value=f"[Click to join]({invite.url})", inline=False)
    else:
        try:
            invite = await guild.create_invite(max_age=300, max_uses=1)
            embed.add_field(name="Server Invite", value=f"[Click to join]({invite.url})", inline=False)
        except discord.Forbidden:
            embed.add_field(name="Server Invite", value="No invites available", inline=False)

    embed.add_field(name="Role Count", value=len(guild.roles), inline=False)
    embed.add_field(name="Channel Count", value=len(guild.channels), inline=False)
    embed.add_field(name="Emoji Count", value=len(guild.emojis), inline=False)
    embed.add_field(name="Boost Level", value=guild.premium_tier, inline=False)
    embed.add_field(name="Verification Level", value=guild.verification_level, inline=False)
    embed.add_field(name="Creds:", value="[Glitched Studios](https://glitchedstudiosdiscordinvite.vercel.app/) (MADE BOT TEMPLATE)", inline=False)

    await interaction.response.send_message(embed=embed)
@bot.tree.command(name='botinfo', description='About the bot')
async def botinfo(interaction: discord.Interaction):
  embed = discord.Embed(
      title="About Me",
      description="This is a embeded message about me the bot",
      color=discord.Color.random())
  embed.add_field(name="Name", value=bot.user.name, inline=False)
  embed.add_field(name="ID", value=bot.user.id, inline=False)
  embed.add_field(name="Owner", value=BOT_OWNER, inline=False)
  embed.add_field(name="Prefix", value=BOT_PREFIX, inline=False)
  embed.add_field(name="Library", value="discord.py", inline=False)
  embed.add_field(name="Created At", value=f"{bot.user.created_at.strftime('%Y/%m/%d')}", inline=False)
  embed.add_field(name="Language", value="English", inline=False)
  embed.add_field(name="Servers", value=len(bot.guilds), inline=False)
  bot_commands = [
      command.name for command in bot.commands if command.name != "botinfo"
  ]

  embed.add_field(name="Prefix Commands",
                  value=f"{len(bot_commands)}",
                  inline=False)
  slash_commands = [
      command.name for command in bot.tree.walk_commands()
      if not command.name.startswith('_')
  ]
  embed.add_field(name="Slash Commands",
                  value=len(slash_commands) - 2,
                  inline=False)
  embed.add_field(name="Creds:", value="[Glitched Studios](https://glitchedstudiosdiscordinvite.vercel.app/) (MADE BOT TEMPLATE)", inline=False)
  await interaction.response.send_message(embed=embed, view=TestView())

@bot.tree.command(name='commandlist', description='List of available slash commands')
@commands.cooldown(1, 5, commands.BucketType.user)
async def cmdlist(interaction: discord.Interaction):
    embed = discord.Embed(title='Slash Commands List', description='List of available slash commands', color=discord.Color.random())

    for command in [c for c in bot.tree.get_commands() if c.name!= 'cmdlist']:
        embed.add_field(name=f"{command.name}", value=f"{command.description}", inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=False)


@bot.command(description="Send This Message")
@commands.cooldown(1, 5, commands.BucketType.user)
async def cmdlist(ctx):
    command_list = []
    for command in bot.commands:
        if command.name!= 'hiddencommand':
            command_list.append((command.name, command.description))

    embed = discord.Embed(title='Command List', description='List of available commands', color=discord.Color.random())
    for cmd_name, cmd_desc in command_list:
        embed.add_field(name=cmd_name, value=cmd_desc, inline=False)
    await ctx.send(embed=embed)


bot.run(BOT_TOKEN)
