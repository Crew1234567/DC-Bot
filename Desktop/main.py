import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread
import random
import asyncio

# === Keep-Alive Server ===
app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"
def run():
    app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

# === Bot Setup ===
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# === Moderation Cog ===
class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kick(self, ctx, member: discord.Member):
        await member.kick()
        await ctx.send(f"Kicked {member.mention}")

    @commands.command()
    async def removerole(self, ctx, member: discord.Member = None, role: discord.Role = None):
        if role is None:
            await ctx.send("❌ You must mention a role.")
            return
        target = member or ctx.author
        if role not in target.roles:
            await ctx.send(f"⚠️ {target.mention} doesn't have the role **{role.name}**.")
            return
        try:
            await target.remove_roles(role)
            await ctx.send(f"✅ Removed role **{role.name}** from {target.mention}")
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to remove that role.")
        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")

# === Engagement Cog ===
class Engagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.balance = {}

    @commands.command()
    async def coinflip(self, ctx, choice: str):
        result = random.choice(["heads", "tails"])
        if choice.lower() == result:
            await ctx.send(f"You won! It was {result}.")
        else:
            await ctx.send(f"You lost! It was {result}.")

    @commands.command()
    async def balance(self, ctx):
        user_id = ctx.author.id
        bal = self.balance.get(user_id, 100)
        await ctx.send(f"{ctx.author.mention}, your balance is ${bal}")

# === Utility Cog ===
class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def remindme(self, ctx, time_in_sec: int, *, message):
        await ctx.send(f"⏰ Reminder set for {time_in_sec} seconds.")
        await asyncio.sleep(time_in_sec)
        await ctx.send(f"{ctx.author.mention}, reminder: {message}")

# === Load Cogs ===
bot.add_cog(Moderation(bot))
bot.add_cog(Engagement(bot))
bot.add_cog(Utility(bot))

@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

# === Run Bot ===
keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))
