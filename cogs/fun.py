import discord
from discord.ext import commands
from replit import db
from random import choice
import os
from private import *


class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    @commands.Cog.listener()
    async def on_message_delete(self, ctx):
        snipe_target = db["snipe_target"]
        if ctx.author.id in snipe_target:
            send_webhook(ctx.content, ctx.author, await fetch_webhook(ctx.channel))

        db["snipes"][ctx.channel.id] = {
        "author": ctx.author.id,
        "content": ctx.content
        }

    # Commands

    @commands.command()
    async def frame(self, ctx, user: discord.Member, *, content):

        banned = db["banned"]

        if await commands.Bot.is_owner(client, ctx.author) or (
                (user.id not in safe) and (ctx.author.id not in banned)):
            if content != "":
              
              send_webhook(content, user, await fetch_webhook(ctx.channel))
        else:
            send_webhook(content, ctx.author, await fetch_webhook(ctx.channel))


def setup(client):
    client.add_cog(Fun(client))
