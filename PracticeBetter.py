import discord # Discord API
import os # OS Access
import config # Config
import requests # Requests API
import random # Random
import asyncio # Asyncio Library
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.bans = True
intents.polls = True
intents.guilds = True
intents.members = True
intents.messages = True
intents.reactions = True
intents.dm_messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='pb -', intents=intents)
bot.remove_command("help")


class SuggestionModal(discord.ui.Modal, title="Send us your suggestion!"):
    suggestion_title = discord.ui.TextInput(
        label="Title",
        placeholder="Give your suggestion a title",
        style=discord.TextStyle.short,
        required=True
    )

    suggestion_message = discord.ui.TextInput(
        label="Suggestion",
        placeholder="Enter your suggestion here",
        style=discord.TextStyle.long,
        required=True,
        max_length=2000
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("Thank you for submitting your suggestion!", ephemeral=True)

        user = interaction.user
        status = "Pending"

        embed = discord.Embed(title="New Suggestion Post!", color=discord.Color.dark_green())
        embed.description = "@here"
        embed.add_field(name="Submitted by", value=user.mention, inline=False)
        embed.add_field(name="Title", value=self.suggestion_title.value, inline=False)
        embed.add_field(name="Suggestion", value=self.suggestion_message.value, inline=False)
        embed.add_field(name="Suggestion Status", value=status, inline=False)
        embed.set_thumbnail(url=user.avatar.url)

        view = SuggestionButtons(embed=embed, user=user)
        channel = interaction.guild.get_channel(config.Staff_Channel_ID)
        message = await channel.send(embed=embed, view=view)
        view.message = message

class SuggestionButtons(discord.ui.View):
    def __init__(self, embed, user):
        super().__init__()
        self.embed = embed
        self.message = None
        self.user = user

    @discord.ui.button(label="Accept Suggestion", style=discord.ButtonStyle.green, emoji="✅")
    async def submit(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user.guild_permissions.administrator:
            self.embed.set_field_at(3, name="Suggestion Status", value="Accepted", inline=False)
            await self.message.edit(embed=self.embed)
            await interaction.response.send_message("Suggestion accepted!", ephemeral=True)
            await self.user.send(embed=self.embed)

    @discord.ui.button(label="Deny Suggestion", style=discord.ButtonStyle.red, emoji="❌")
    async def reject(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.guild_permissions.administrator:
            self.embed.set_field_at(3, name="Suggestion Status", value="Denied", inline=False)
            await self.message.edit(embed=self.embed)
            await interaction.response.send_message("Suggestion denied!", ephemeral=True)
            await self.user.send(embed=self.embed)
        else:
            await interaction.response.send_message("You don't have permission to deny this suggestion!", ephemeral=True)

extension_group = app_commands.Group(name="extension", description="Staff only commands")

@bot.event
async def on_ready():
    
    bot.tree.add_command(extension_group)

    await bot.tree.sync()
    print(f"{bot.user} Has Connected To Discord!")

async def is_bot_staff_member(user_id: str):
    App_Info = await bot.application_info() # Get the bot information
    Owner_ID = App_Info.owner.id # Get the owner id

    Staff_IDs = [Owner_ID]
    return user_id in Staff_IDs

async def load():
    for file in os.listdir("./cogs"):
       if file.endswith(".py"):
        await bot.load_extension(f"cogs.{file[:-3]}")

async def main ():
    await load()
    discord.utils.setup_logging()
    await bot.start(config.Bot_Token)

@bot.hybrid_command(name="info", description="Shows information about the bot")
async def bot_info(ctx):
    embed = discord.Embed(title="Bot Info", color=discord.Color.greyple())
    embed.add_field(name="Creator", value="JMC", inline=True)
    embed.add_field(name="Version", value="v1")
    embed.add_field(name="Servers", value=len(bot.guilds) ,inline=False)
    embed.add_field(name="Latency", value=round(bot.latency * 1000), inline=True)
    embed.add_field(name="Github", value="Im finnally open source on [Github!](https://github.com/47JMC/PracticeBetter)")
    embed.set_footer(text="Library -> discord.py", icon_url="https://images.opencollective.com/discordpy/25fb26d/logo/256.png")

    await ctx.send(embed=embed)

@bot.tree.command(name="suggestion", description="Give us some suggestions")
async def suggestion(interaction: discord.Interaction):
    await interaction.response.send_modal(SuggestionModal())

@bot.tree.command(name="massping", description="Mass ping a user")
@app_commands.allowed_installs(guilds=False, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def mass_ping(interaction: discord.Interaction, user: discord.User, times: int):
    if is_bot_staff_member(interaction.user.id):
        if not times > 90:
            await interaction.response.defer()
            message_without_brackets = user.mention * times
            await interaction.followup.send(message_without_brackets)
        else:
            embed = discord.Embed(title="Message Limit Reached", color=discord.Color.dark_embed())
            embed.add_field(name="Error", value="You can't mass ping more than 90 times at once.")
            await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title="Acess denied", color=discord.Color.red())
        embed.add_field(name="Error", value="You do not have permission to use this command.")
        await interaction.response.send_message(embed=embed)

@extension_group.command(name="load", description="Staff only command")
async def exetension_load(interaction: discord.Interaction, extension: str):
    if await is_bot_staff_member(interaction.user.id):
        # User is staff
        await bot.load_extension(f"cogs.{extension.lower()}")
        await interaction.response.send_message(f"Extension {extension} has been loaded.", ephemeral=True)
    else:
        embed = discord.Embed(title="Acess denied", color=discord.Color.red())
        embed.add_field(name="Error", value="You do not have permission to use this command.")
        await interaction.response.send_message(embed=embed)

@extension_group.command(name="unload", description="Staff only command")
async def extension_unload(interaction: discord.Interaction, extension: str):
    if await is_bot_staff_member(interaction.user.id):
        # User is staff
        await bot.unload_extension(f"cogs.{extension.lower()}")
        await interaction.response.send_message(f"Extension {extension} has been unloaded.", ephemeral=True)
    else:
        embed = discord.Embed(title="Acess denied", color=discord.Color.red())
        embed.add_field(name="Error", value="You do not have permission to use this command.")
        await interaction.response.send_message(embed=embed)

@extension_group.command(name="reload", description="Staff only command")
async def reload(interaction: discord.Interaction, extension: str):
    if await is_bot_staff_member(interaction.user.id):
        # User is staff
        await bot.reload_extension(f"cogs.{extension.lower()}")
        await interaction.response.send_message(f"Extension {extension} has been reloaded.", ephemeral=True)
    else:
        embed = discord.Embed(title="Acess denied", color=discord.Color.red())
        embed.add_field(name="Error", value="You do not have permission to use this command.")
        await interaction.response.send_message(embed=embed)

asyncio.run(main())