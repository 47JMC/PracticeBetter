import discord
import sqlite3
from discord.ext import commands
from discord import app_commands

connection = sqlite3.connect("databases/mod.db")
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS modlogs(
               id INTEGER PRIMARY KEY,
               user_id INTEGER,
               mod_id INTEGER,
               guild_id INTEGER,
               punish_type TEXT,
               timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
               reason TEXT)""")

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mute", description="Mute a user in the server")
    async def user_ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        if interaction.user.guild_permissions.mute_members:
            guild = interaction.guild
            mod = interaction.user
            punish_type = "Mute"
            muted_role = discord.utils.get(guild.roles, name="Muted")

            if muted_role is None:
                await interaction.response.send_message("Please create a muted role")
            else:
                if muted_role not in member.roles:
                    await member.add_roles(muted_role)
                    embed = discord.Embed(title=f"You were muted in {guild.name}")
                    embed.add_field(name=f"You were muted in {guild.name} for {reason}")
                    await member.send(embed=embed)
                    cursor.execute("INSERT INTO modlogs (user_id, mod_id, guild_id, punish_type, reason) VALUES (?,?,?,?,?)", (member.id, mod.id, guild.id, punish_type, reason))
                    connection.commit()
                    if reason:
                        await interaction.response.send_message(f"{member.mention} has been muted for {reason}.", ephemeral=True)
                    else:
                        await interaction.response.send_message(f"{member.mention} has been muted.", ephemeral=True)
                else:
                    await member.remove_roles(muted_role)
                    embed = discord.Embed(title=f"You were unmuted in {guild.name}")
                    embed.add_field(name=f"You were unmuted in {guild.name}")
                    await member.send(embed=embed)
                    await interaction.response.send_message(f"{member.mention} has been unmuted.", ephemeral=True)
        else:
            await interaction.response.send_message(content="You don't have the permission to mute members.", ephemeral=True)

        @app_commands.command(name="warn", description="Warn a user in the server")
        async def user_warn(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
            if interaction.user.guild_permissions.mute_members:
                guild = interaction.guild
                mod = interaction.user
                punish_type = "Warn"

                # Send the user the warning message
                embed = discord.Embed(title=f"You were warned in {guild.name}")
                embed.add_field(name=f"You were warned in {guild.name} for {reason}")
                await member.send(embed=embed)

                # Add the warning to the database
                cursor.execute("INSERT INTO modlogs (user_id, mod_id, guild_id, punish_type, reason) VALUES (?,?,?,?,?)", (member.id, mod.id, guild.id, punish_type, reason))
                connection.commit()
            else:
                await interaction.response.send_message(content="You don't have the permission to warn members.", ephemeral=True)

    @app_commands.command(name="punishments", description="Shows list of punishments of a member")
    async def list_punishments(self, interaction: discord.Interaction, member: discord.Member):
        cursor.execute("SELECT * FROM modlogs WHERE user_id =?", (member.id,))
        punishments = cursor.fetchall()

        if not punishments:
            await interaction.response.send_message(f"{member.mention} has no recorded punishments.")
        else:
            embed = discord.Embed(title=f"{member.display_name}'s Punishments", color=discord.Color.blurple())
            for punishment in punishments:
                embed.add_field(name=f"{punishment[4]} | {punishment[5]}", value=f"<@{punishment[1]}> was punished by <@{punishment[2]}> for {punishment[6]}", inline=False)
            await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Moderation(bot))