import discord
from discord.ext import commands
from replit import db
from private import *


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @commands.is_owner()
    async def warn(self, ctx, warned: discord.User, *, reason):
        try:
            db["warns"][str(ctx.guild.id)][str(warned)][str(ctx.message.id)] = {"staff": str(ctx.author), "reason": reason}

        except:
          try:
            db["warns"][str(ctx.guild.id)][str(warned)] = {str(ctx.message.id): {"staff": str(ctx.author), "reason": reason}}
          except:
            db["warns"][str(ctx.guild.id)] = {str(warned): {str(ctx.message.id): {"staff": str(ctx.author), "reason": reason}}}

        embed = discord.Embed(
            description=f"***{str(warned)}** was warned by **{str(ctx.author)}** for* **`{reason}`**",
            color=cyan
        )
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Moderation(client))
