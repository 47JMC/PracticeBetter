import discord
import requests
from discord.ext import commands
from discord import app_commands

class ServerStatusCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def get_status(ip, server_port = 25565):
        url = f"https://api.mcsrvstat.us/3/{ip}:{server_port}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data


    @commands.hybrid_command(name="serverstatus",description="checks the server status")
    @app_commands.allowed_installs(guilds=False, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def server_status(self, ctx, server_ip: str, port: int = 25565):
        data = self.get_status(ip=server_ip, server_port=port)
        online = data.get("online")

        if online == True:
            port =  data.get("port")
            motd = data.get("motd")
            players = data.get("players")
            software = data.get("software")
            version = data.get("version")
            eula_blocked = data.get("eula_blocked")
            motd_clean = motd.get("clean")
            motd_raw = motd.get("raw")
            online_players = players.get("online")
            max_players = players.get("max")

            embed = discord.Embed(title="Server Status",color=discord.Color.random())
            embed.add_field(name="Server IP", value=f"||{server_ip}||",inline=True)
            embed.add_field(name="Port", value=f"||{port}||", inline=True)
            embed.add_field(name="Motd", value=f"`{motd_clean}`", inline=False)
            embed.add_field(name="Raw Motd", value=f"`{motd_raw}`",inline=False)
            embed.add_field(name="Players", value=f"{online_players}/{max_players}",inline=False)
            embed.add_field(name="Version",value=f"{software} {version}",inline=False)
            embed.add_field(name="Blocked by Mojang", value=f"{eula_blocked}",inline=False)
            embed.set_thumbnail(url=f"https://eu.mc-api.net/v3/server/favicon/{server_ip}:{port}")

            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Server Not Found or Server Oflline", color=discord.Color.red())
            embed.add_field(name="Error", value="The server is doesnt exist or its currently offline.")
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ServerStatusCommand(bot))