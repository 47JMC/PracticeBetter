import discord
from discord.ext import commands
from discord import app_commands

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Help Command
    @commands.hybrid_command(name="help", description="The help command")
    @app_commands.allowed_installs(guilds=False, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def pb_help(self, ctx):
        main_embed = discord.Embed(title="Help Menu", description="All available commands", color=0x884EA0)
        main_embed.add_field(name="Select a category", value="Please select a category to view the commands")

        # Attach the dropdown and send it
        view = HelpCommandView()
        message = await ctx.send(embed=main_embed, view=view)
        view.message = message

class HelpCommandView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.message = None
        self.add_item(HelpCommandDropDown(self))

class HelpCommandDropDown(discord.ui.Select):
    def __init__(self, parent_view):
        self.parent_view = parent_view
        options = [
            discord.SelectOption(label="Moderation", value="moderation", emoji="🔫"),
            discord.SelectOption(label="Information", value="information", emoji="ℹ️"),
            discord.SelectOption(label="Utility", value="utility", emoji="🛠️"),
            discord.SelectOption(label="Staff Only", value="staff", emoji="❌"),
        ]

        super().__init__(placeholder="Select a category", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        option = self.values[0]
        embed = None

        if option == "moderation":
            embed = discord.Embed(title="Moderation Commands", description="All available moderation commands", color=0x884EA0)
            embed.add_field(name="Coming Soon", value="Coming Soon", inline=False)
        elif option == "information":
            embed = discord.Embed(title="Information Commands", description="All available information commands", color=0x884EA0)
            embed.add_field(name="</info:1258452114611638384>", value="Displays Information about the bot", inline=False)
        elif option == "utility":
            embed = discord.Embed(title="Utility Commands", description="All available utility commands", color=0x884EA0)
            embed.add_field(name="</serverstatus:1259900341080817665>", value="Shows information Minecraft Server Status", inline=False)
            embed.add_field(name="</github user:1259415830739947624>", value="Shows information about a github user", inline=False)
            embed.add_field(name="</github repo:1259415830739947624>", value="Shows information about a github repository", inline=False)
        elif option == "staff":
            embed = discord.Embed(title="Staff Commands", description="All available staff commands", color=0x884EA0)
            embed.add_field(name="</massping:1257879750274453544>", value="Nuclear weapon in discord", inline=False)
            embed.add_field(name="</extension load:1260411190698446951>", value="Staff only command", inline=True)
            embed.add_field(name="</extension unload:1260411190698446951>", value="Staff only command", inline=True)
            embed.add_field(name="</extension reload:1260411190698446951>", value="Staff only command", inline=False)
        else:
            embed = discord.Embed(title="Unknown Category", description="This category is not recognized", color=0x884EA0)

        await self.parent_view.message.edit(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCommand(bot))
