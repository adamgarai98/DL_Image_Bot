import asyncio
import os
from typing import Literal, Optional

import bot
import cv2
import discord
import matplotlib.pyplot as plt
import numpy as np
import responses
import torch

# from cogs import general_sam
from discord.ext import commands
from discord.ext.commands import Context, Greedy  # or a subclass of yours
from dotenv import load_dotenv
from segment_anything import SamAutomaticMaskGenerator, SamPredictor, sam_model_registry

load_dotenv()

intents = discord.Intents.all()
intents.message_content = True
# client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="/", intents=intents)
# bot.remove_command("help")
MY_GUILD = discord.Object(id=1176239681021685811)  # replace with your guild id


# In this basic example, we just synchronize the app commands to one guild.
# Instead of specifying a guild to every command, we copy over our global commands instead.
# By doing so, we don't have to wait up to an hour until they are shown to the end-user.


async def setup_hook():
    # This copies the global commands over to your guild.
    bot.tree.copy_global_to(guild=MY_GUILD)
    await bot.tree.sync(guild=MY_GUILD)


# @commands.command()
# async def sync():
#     await bot.tree.sync()


async def load():
    await bot.load_extension("cogs.general_sam")
    bot.setup_hook = setup_hook
    # await bot.tree.sync()


async def main():
    await load()
    await bot.start(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    asyncio.run(main())
