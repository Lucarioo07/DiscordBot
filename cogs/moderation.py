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
            db["warns"][str(ctx.guild.id)][str(warned.id)][str(ctx.message.id)] = {"staff": ctx.author.id, "reason": reason, "channel": ctx.channel.id}

        except:
          try:
            db["warns"][str(ctx.guild.id)][str(warned.id)] = {str(ctx.message.id): {"staff": ctx.author.id, "reason": reason, "channel": ctx.channel.id}}
          except:
            db["warns"][str(ctx.guild.id)] = {str(warned.id): {str(ctx.message.id): {"staff": ctx.author.id, "reason": reason, "channel": ctx.channel.id}}}

        embed = discord.Embed(
            description=f"***{str(warned)}** was warned by **{str(ctx.author)}** for* **`{reason}`**",
            color=cyan
        )
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.is_owner()
    async def delwarn(self, ctx, user: discord.User, warn_id):
      try:
        if warn_id in db["warns"][str(ctx.guild.id)][str(user.id)].keys():
          embed = discord.Embed(
            description=f"The warn with ID `{warn_id}` has been deleted.",
            color=cyan
          )
          del db["warns"][str(ctx.guild.id)][str(user.id)][warn_id]
        else:
          embed = discord.Embed(
            description=f"A warn for this user with ID `{warn_id}` couldnt't be found.",
            color=cyan
          )
      except:
        embed = discord.Embed(
            description=f"A warn for this user with ID `{warn_id}` couldnt't be found.",
            color=cyan
          )
      await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def clearwarn(self, ctx, user: discord.User):
      try:
        del db["warns"][str(ctx.guild.id)][str(user.id)]
      except:
        pass

    @commands.command(aliases=["warnings", "oopsies"])
    async def warns(self, ctx, user: discord.User= None):

        if user is None:
          user = ctx.author

        try:
          warns = db["warns"][str(ctx.guild.id)][str(user.id)]

        except Exception as e:
          await ctx.send(embed=discord.Embed(description="dam this guy has no warns lmao what", color=cyan))
          return
        
        
        if warns == {}:
          await ctx.send(embed=discord.Embed(description="dam this guy has no warns lmao what", color=cyan))
        else:
          embed = discord.Embed(title=f"__Warns for {user}__", color=cyan)
          description = "**Context Menu:** \n"
          for value in warns.values():
              warn_id = get_key(value, warns)
              reason = value["reason"]
              embed.add_field(
                name=f"ID: `{warn_id}` \n",
                
                value=f"Staff: `{await client.fetch_user(value['staff'])}` \n"
                      f"Reason: \n"
                      f"> **`{reason}`**"
              )
              if len(reason) <= 20:
                description += f'> [**{reason}**](https://discord.com/channels/{ctx.guild.id}/{value["channel"]}/{warn_id} "Warn ID: {warn_id}") \n'
              else:
                description += f'> [**{reason[0:20]}...**](https://discord.com/channels/{ctx.guild.id}/{value["channel"]}/{warn_id} "Warn ID: {warn_id}") \n'
          embed.description = description
          await ctx.send(embed=embed)
        

def setup(client):
    client.add_cog(Moderation(client))
