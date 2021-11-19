import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle
from utils import *


class Test(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @slash.slash(description="that relatable moment when the test is test")
    @commands.is_owner()
    async def amogus(self, ctx):
      await ctx.send(embed=discord.Embed(
        description= "test embed"
      ),components=[
        [Button(label="yoooo", style=ButtonStyle.blue, custom_id="bruhk")]
      ])
      
      interaction = client.wait_for("button_click", check= lambda inter: inter.custom_id == "bruhk")

      await interaction.send("ok")

def setup(client):
    client.add_cog(Test(client))
