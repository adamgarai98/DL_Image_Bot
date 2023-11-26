"""
Top comment
"""

import os
import urllib.request

import cv2
import discord
import matplotlib.pyplot as plt
import numpy as np
import torch
from discord.ext import commands
from segment_anything import SamAutomaticMaskGenerator, SamPredictor, sam_model_registry


def show_anns(anns):
    if len(anns) == 0:
        return
    sorted_anns = sorted(anns, key=(lambda x: x["area"]), reverse=True)
    ax = plt.gca()
    ax.set_autoscale_on(False)

    img = np.ones((sorted_anns[0]["segmentation"].shape[0], sorted_anns[0]["segmentation"].shape[1], 4))
    img[:, :, 3] = 0
    for ann in sorted_anns:
        m = ann["segmentation"]
        color_mask = np.concatenate([np.random.random(3), [0.35]])
        img[m] = color_mask
    ax.imshow(img)


def write_masks_to_png(masks: list[dict[str]], image) -> None:
    plt.figure(figsize=(8, 4))
    plt.imshow(image)
    show_anns(masks)
    plt.axis("off")
    plt.savefig("/code/src/dlim/masks.png")
    plt.close()
    return


class GeneralSam(commands.Cog):
    """
    Middle comment
    """

    def __init__(self, bot):
        self.bot = bot
        self.mask_generator = None

    @commands.command()
    async def load_sam(self, ctx):
        """
        Third comment
        """
        try:
            await ctx.send("Loading SAM")
            sam_checkpoint = "/code/src/dlim/cogs/Model_Checkpoints/sam_vit_h_4b8939.pth"
            model_type = "vit_h"

            device = "cpu"

            sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
            sam.to(device=device)

            self.mask_generator = SamAutomaticMaskGenerator(model=sam, points_per_batch=8)
            await ctx.send("SAM loaded")
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    async def sam(self, ctx, url):
        """
        Third comment
        """
        await ctx.send("Getting image")
        req = urllib.request.urlopen(url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        image = cv2.imdecode(arr, -1)  # 'Load it as it is'

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        plt.figure(figsize=(8, 4))
        plt.imshow(image)
        plt.axis("off")
        plt.show()
        plt.savefig("/code/src/dlim/original.png")
        await ctx.send("Got image")
        await ctx.send(file=discord.File("/code/src/dlim/original.png"))
        # await ctx.send("Loading model")
        # try:
        #     sam_checkpoint = "/code/src/dlim/cogs/Model_Checkpoints/sam_vit_h_4b8939.pth"
        #     model_type = "vit_h"

        #     device = "cpu"

        #     sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
        #     sam.to(device=device)

        #     mask_generator = SamAutomaticMaskGenerator(model=sam, points_per_batch=8)
        #     await ctx.send("Model loaded")
        # except Exception as e:
        #     await ctx.send(e)
        if self.mask_generator == None:
            await ctx.send("Please first load SAM using /load_sam")
            return

        try:
            await ctx.send("Generating masks (may take a while)")
            masks = self.mask_generator.generate(image)
        except Exception as e:
            await ctx.send(e)

        await ctx.send("Masks generated")
        await ctx.send("Writing image")
        write_masks_to_png(masks, image)
        await ctx.send(file=discord.File("/code/src/dlim/masks.png"))

    @commands.command()
    async def hello(self, ctx):
        """
        Third comment
        """
        # await self.bot.tree.sync()
        try:
            with open("/code/src/dlim/racoon_in_suit.jpg", "rb") as f:
                picture = discord.File(f)
                await ctx.send(file=picture)
        except Exception as e:
            await ctx.send(e)
        # await ctx.send("Hello")

    @commands.command()
    async def getguild(self, ctx):
        id = ctx.message.guild.id
        await ctx.send(id)


async def setup(bot):
    """
    Required.
    """
    await bot.add_cog(GeneralSam(bot))
