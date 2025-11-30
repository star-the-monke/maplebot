import discord, json, os, re, asyncio, random, time, threading
from discord.ext import commands
from dotenv import load_dotenv
from datetime import timedelta
from datetime import datetime
from collections import defaultdict
from discord.ui import Select, View
from discord import app_commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix="m", intents=intents, help_command=None) # change r. with your prefix

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="mhelp | maple")) # change the string to your bot's help command

    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

@bot.command(name="help")
async def help(ctx):
    embed = discord.Embed(
        title="maple's bot menu :D",
        color=discord.Color.from_rgb(210, 180, 140)
    )
    embed.add_field(name="`mhelp`", value="[Display a list of cmds/commands.]", inline=False)
    embed.add_field(name="`mping`", value="[pings maple!]", inline=False)
    embed.add_field(name="`mtiktok`", value="[gets the latest maple tiktok]", inline=False)
    embed.add_field(name="`mtimeout [@user] [duration]`", value="[timesout a bad person]", inline=False)
    embed.add_field(name="`muntimeout [@user]`", value="[untimesout a bad person]", inline=False)
    embed.add_field(name="`mkick [@user]`", value="[kicks  a bad person]", inline=False)
    embed.add_field(name="`mban [@user]`", value="[ban  a bad person]", inline=False)
    embed.add_field(name="`munban [@userid]`", value="[unban  a goodboy]", inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("<@1408154302874255410>")


@bot.command(name="tiktok", aliases=["tt"])
async def tiktok(ctx):
    await ctx.send("https://www.tiktok.com/@captianmaple")

@bot.command(name="timeout")
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, duration: int = 10):
    try:
        match = re.match(r"^(\d+)([smh])$", duration.lower())
        if not match:
            await ctx.send("Invalid duration format. Use s (seconds), m (minutes), or h (hours). Example: 10m for 10 minutes.")
            return
        value, unit = int(match.group(1)), match.group(2)
        if unit == 's':
            delta = timedelta(seconds=value)
        elif unit == 'm':
            delta = timedelta(minutes=value)
        elif unit == 'h':
            delta = timedelta(hours=value)
        
        await member.timeout(delta)
        await ctx.send(f"{member.mention} has been timed out for {value}{unit}.")
    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command(name="untimeout")
@commands.has_permissions(moderate_members=True)
async def untimeout(ctx, member: discord.Member):
    try:
        await member.timeout(None)
        await ctx.send(f"{member.mention} has been untimed out.")
    except Exception as e:
        await ctx.send(f"Error: {e}")


@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member):
    try:
        await member.kick()
        await ctx.send(f"{member.mention} has been kicked from the server.")
    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command(name="ban")
@commands.has_permissions(kick_members=True)
async def ban(ctx, member: discord.Member):
    try:
        await member.ban()
        await ctx.send(f"{member.mention} has been ban from the server.")
    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command(name="unban")
@commands.has_permissions(kick_members=True)
async def unban(ctx, userid: int):
    try:
        id = userid
        await ctx.guild.unban(bot.fetch_user(id))
        await ctx.send(f"<@{userid}>has been unban from the server.")
    except Exception as e:
        await ctx.send(f"Error: {e}")


bot.run(TOKEN)

