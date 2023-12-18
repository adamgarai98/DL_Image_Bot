"""
Top comment
"""
import gc
import os
import platform
import sys
import time
import urllib.request

import cv2
import discord
import matplotlib.pyplot as plt
import numpy as np
import torch
from discord.ext import commands
from PIL import Image
from segment_anything import SamAutomaticMaskGenerator, SamPredictor, sam_model_registry

PATH_TO_IMG = "/code/src/dlim/images/segmentedimage.png"


def get_masks(anns):
    if len(anns) == 0:
        return

    sorted_anns = sorted(anns, key=(lambda x: x["area"]), reverse=True)
    img = np.ones((sorted_anns[0]["segmentation"].shape[0], sorted_anns[0]["segmentation"].shape[1], 4))
    img[:, :, 3] = 0
    for ann in sorted_anns:
        m = ann["segmentation"]
        color_mask = np.concatenate([np.random.random(3), [0.35]])
        img[m] = color_mask
    return img


class GeneralSam(commands.Cog):
    """
    Middle comment
    """

    def __init__(self, bot):
        self.bot = bot
        self.mask_generator = None

    @commands.command()
    async def load_sam(self, ctx, batch_size: int):
        """
        Third comment
        """
        try:
            await ctx.send("Loading SAM")
            if self.mask_generator:
                await ctx.send("Reloading SAM and running garbage collection")
                self.mask_generator = None
                gc.collect()
                await ctx.send("Garbage collection done")
            sam_checkpoint = "/code/src/dlim/cogs/Model_Checkpoints/sam_vit_h_4b8939.pth"
            model_type = "vit_h"
            device = "cuda"
            sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
            sam.to(device=device)
            # def batch size 32
            self.mask_generator = SamAutomaticMaskGenerator(model=sam, points_per_batch=batch_size)

            await ctx.send(f"Loaded SAM on device: {device}")
            await print(f"Loaded SAM on device: {device}")
        except Exception as e:
            await print(e)
            await ctx.send(e)
            return

    @commands.command()
    async def sam(self, ctx, url):
        """
        Third comment
        """
        try:
            await ctx.send("Getting image")
            req = urllib.request.urlopen(url)
            arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
            image = cv2.imdecode(arr, -1)  # 'Load it as it is'

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # For testing size
            input_image = Image.fromarray(image)
            input_image.save(PATH_TO_IMG)
            resized_input = False
            if (os.path.getsize(PATH_TO_IMG) / (1024 * 1024)) >= 8:
                await ctx.send("Input image is too big and may cause OutOfMemory Errors. Compressing image.")
                resized_input = True
                compression_counter = 1
                while (os.path.getsize(PATH_TO_IMG) / (1024 * 1024)) >= 8:
                    await ctx.send(f"Compression try {compression_counter}")
                    input_image = Image.open(PATH_TO_IMG)
                    input_image = input_image.resize(
                        (int(input_image.size[0] * 0.9), int(input_image.size[1] * 0.9)), Image.Resampling.LANCZOS
                    )
                    input_image.save(PATH_TO_IMG)
                    compression_counter += 1
            # Check if it was resized
            if resized_input:
                image = Image.open(PATH_TO_IMG)
                image = np.asarray(image)
                await ctx.send("Converted image back after compression")
            await ctx.send("Recieved image")
        except Exception as e:
            await ctx.send(e)
            return

        if self.mask_generator == None:
            await ctx.send("Please first load SAM using /load_sam")
            return

        try:
            await ctx.send("Generating masks (may take a while)")
            masks = self.mask_generator.generate(image)
            image = Image.fromarray(image)
            image_masks = Image.fromarray(np.uint8(get_masks(masks) * 255))
            image.paste(image_masks, (0, 0), image_masks)
            image.save(PATH_TO_IMG)
            # file_size_megabytes = file_size_bytes / (1024 * 1024)
            if (os.path.getsize(PATH_TO_IMG) / (1024 * 1024)) >= 8:
                await ctx.send("Image too big to return. Compressing image.")

                compression_counter = 1
                while (os.path.getsize(PATH_TO_IMG) / (1024 * 1024)) >= 8:
                    await ctx.send(f"Compression try {compression_counter}")
                    image = Image.open(PATH_TO_IMG)
                    image = image.resize((int(image.size[0] * 0.9), int(image.size[1] * 0.9)), Image.Resampling.LANCZOS)
                    image.save(PATH_TO_IMG)
                    compression_counter += 1

            await ctx.send("Sending segmentated image")
            await ctx.send(file=discord.File(PATH_TO_IMG))
        except Exception as e:
            await ctx.send(e)
            e_type, e_object, e_traceback = sys.exc_info()
            e_line_number = e_traceback.tb_lineno
            await ctx.send(f"exception line number: {e_line_number}")
            return

    @commands.command()
    async def hello(self, ctx):
        """
        Third comment
        """
        # await self.bot.tree.sync()
        try:
            with open("/code/src/dlim/images/racoon_in_suit.jpg", "rb") as f:
                picture = discord.File(f)
                await ctx.send(torch.cuda.is_available())
                await ctx.send("Python version")
                await ctx.send(sys.version)
                await ctx.send("Version info.")
                await ctx.send(sys.version_info)
                # await ctx.send(platform.python_build())
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
