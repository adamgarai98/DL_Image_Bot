# import cv2
# import discord
# import matplotlib.pyplot as plt
# import numpy as np
# import responses
# import torch

# # from cogs import general_sam
# from discord.ext import commands
# from segment_anything import SamAutomaticMaskGenerator, SamPredictor, sam_model_registry

# # async def send_message(message, user_message, is_private):
# #     try:
# #         response = responses.get_response(user_message)
# #         if response is None:
# #             return
# #         else:
# #             await message.author.send(response) if is_private else await message.channel.send(response)


# #     except Exception as e:
# #         print(e)


# def run_discord_bot():
#     # TOKEN = 0  # Token here
#     intents = discord.Intents.default()
#     intents.message_content = True
#     # client = discord.Client(intents=intents)
#     bot = commands.Bot(command_prefix="/", intents=intents)
#     bot.remove_command("help")
#     bot.load_extension("cogs.general_sam")
#     # @commands.command()
#     # async def sam(ctx):
#     #     print(torch.cuda.is_available())
#     #     await ctx.send("Hello")

#     # @client.event
#     # async def on_read():
#     #     print(f"{client.user} is now running!")

#     # @client.event
#     # async def on_message(message):
#     #     if message.author == client.user:
#     #         return

#     #     username = str(message.author)
#     #     user_message = str(message.content)
#     #     channel = str(message.channel)

#     #     print(f"{username} said {user_message} in {channel}")

#     #     if user_message[0] == "?":
#     #         user_message = user_message[1:]
#     #         await send_message(message, user_message, is_private=True)
#     #     else:
#     #         await send_message(message, user_message, is_private=False)

#     # client.run(OSError.getenv("DISCORD_TOKEN"))
#     # bot.add_cog(hello(bot))
#     # bot.add_command(sam)
