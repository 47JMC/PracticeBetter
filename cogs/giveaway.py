import discord
import asyncio
import random
from discord.ext import commands

class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="giveawaycreate", description="Create a giveaway!")
    async def giveaway_create(self, ctx, title: str, duration: int, prize: str, sponsor: discord.Member):
        guild = ctx.guild
        channel = ctx.channel
        duration_min = duration * 60

        if discord.utils.get(guild.roles, name="Giveaways") is None:
            await guild.create_role(name="Giveaways")
        if discord.utils.get(guild.roles, name="Sponsors") is None:
            await guild.create_role(name="Sponsors")

        embed = discord.Embed(title=" 🎉 **Giveaway Started** 🎉", color=0x2980B9)
        embed.description = "React with 🎉 to enter!"
        embed.add_field(name="Title", value=title, inline=False)
        embed.add_field(name="Prize", value=prize, inline=False)
        embed.add_field(name="Duration", value=f"{duration} Minutes", inline=False)
        embed.add_field(name="Sponsor", value=sponsor.mention, inline=False)

        await ctx.send(embed=embed)
        giveaway_message = await ctx.send(embed=embed)
        await giveaway_message.add_reaction("🎉")

        # Wait for the giveaway to end
        await asyncio.sleep(duration_min)

        message = await channel.fetch_message(giveaway_message.id)
        for reaction in message.reactions:
            if reaction.emoji == "🎉":
                users = [user async for user in reaction.users()]
                users.remove(self.bot.user)  # Remove the bot from the list of users

                if users:
                    winner = random.choice(users)
                    winner_embed = discord.Embed(title="🎉 **Giveaway Ended** 🎉", color=0x2980B9)
                    winner_embed.add_field(name="**Winner**", value=winner.mention, inline=False)
                    winner_embed.add_field(name="**Prize**", value=f"{prize}", inline=False)
                    winner_embed.set_footer(text="Congratulations!")
                    await channel.send(embed=winner_embed)
                    await message.edit(embed=winner_embed)
                else:
                    await channel.send("No participants for the giveaway.")
                break

async def setup(bot):
    await bot.add_cog(Giveaway(bot))
