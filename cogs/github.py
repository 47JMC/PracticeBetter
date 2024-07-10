import discord
import requests
from discord.ext import commands
from discord import app_commands

class Github(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    github_group = app_commands.Group(name="github", description="Commands related to github",
                                      allowed_installs=app_commands.AppInstallationType(guild=False, user=True),
                                      allowed_contexts=app_commands.AppCommandContext(guild=True, dm_channel=True, private_channel=True))
    
    @staticmethod
    def fetch_data(url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None

    @github_group.command(name="user", description="Gives data about a github user")
    @app_commands.allowed_installs(guilds=False, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.describe(username="The username of the github account you're searching for")
    async def fetch_user_data(self, interaction: discord.Interaction, username: str):
        data = self.fetch_data(f"https://api.github.com/users/{username}")
        repo_data = self.fetch_data(f"https://api.github.com/users/{username}/repos")
        
        if data is None or data.get("message") == "Not Found":
            embed = discord.Embed(title="User Not Found", color=discord.Color.red())
            embed.add_field(name="Error", value="The user you're looking for doesn't exist.")
            await interaction.response.send_message(embed=embed)
            return
        
        # User information

        username = data.get("name") or data.get("login")
        avatar_img = data.get("avatar_url")
        bio = data.get("bio")
        company = data.get("company")
        email = data.get("email")
        public_repos = data.get("public_repos")
        public_gists = data.get("public_gists")
        followers = data.get("followers")
        following = data.get("following")

        repos = []
        # Repository information
        for repo in range(len(repo_data)):
            repo_name = repo_data[repo].get("name")
            repo_url = repo_data[repo].get("html_url")
            repos.append(f"[{repo_name}]({repo_url})")

        embed = discord.Embed(title=f"{username}'s Github profile", color=discord.Color.brand_green())
        embed.add_field(name="Bio", value=bio)
        embed.add_field(name="Email", value=email, inline=False)
        embed.add_field(name="Company", value=company, inline=False)
        embed.add_field(name="Followers", value=followers, inline=True)
        embed.add_field(name="Following", value=following, inline=True)
        embed.add_field(name="Public Repositories", value=public_repos, inline=False)
        embed.add_field(name="Public Gists", value=public_gists, inline=False)
        embed.set_thumbnail(url=avatar_img)

        repo_embed = discord.Embed(title=f"{username}'s Repositories", description=" | ".join(repos))
        await interaction.response.send_message(embed=embed)
        await interaction.followup.send(embed=repo_embed)

    @github_group.command(name="repo", description="Check information about a github repository")
    @app_commands.allowed_installs(guilds=False, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.describe(owner="The username of the owner of the repository", repo_name="The name of the repository")
    async def repo_info(self, interaction: discord.Interaction, owner: str, repo_name: str):
        data = self.fetch_data(f"https://api.github.com/repos/{owner}/{repo_name}")
        commits = self.fetch_data(f"https://api.github.com/repos/{owner}/{repo_name}/commits/main")
        
        if data is None or data.get("message") == "Not Found":
            embed = discord.Embed(title="Repository Not Found", color=discord.Color.red())
            embed.add_field(name="Error", value="The repository you're looking for doesn't exist.")
            await interaction.response.send_message(embed=embed)
            return

        owner = data.get("owner")
        login = owner.get("login")
        created_at = data.get("created_at")
        updated_at = data.get("updated_at")
        pushed_at = data.get("pushed_at")
        visibility = data.get("visibility")
        forks = data.get("forks")
        open_issues = data.get("open_issues")
        watchers = data.get("watchers")
        subscribers_count = data.get("subscribers_count")
        is_fork = data.get("fork")
        description = data.get("description")
        git_url = data.get("git_url")
        ssh_url = data.get("ssh_url")
        has_pages = data.get("has_pages")

        latest_commit_author = commits.get("commit").get("author").get("name")
        latest_commit_date = commits.get("commit").get("committer").get("date")
        latest_commit_message = commits.get("commit").get("message")
        latest_commit_html_url = commits.get("html_url")

        embed = discord.Embed(title=f"{repo_name} Repository Info", color=discord.Color.blue())
        embed.add_field(name="Owner", value=login, inline=True)
        embed.add_field(name="Visibility", value=visibility, inline=True)
        embed.add_field(name="Description", value=description, inline=False)
        embed.add_field(name="Created At", value=created_at, inline=True)
        embed.add_field(name="Updated At", value=updated_at, inline=True)
        embed.add_field(name="Pushed At", value=pushed_at, inline=True)
        embed.add_field(name="Forks", value=forks, inline=True)
        embed.add_field(name="Open Issues", value=open_issues, inline=True)
        embed.add_field(name="Watchers", value=watchers, inline=True)
        embed.add_field(name="Subscribers Count", value=subscribers_count, inline=True)
        embed.add_field(name="Has Pages", value=has_pages, inline=True)
        embed.add_field(name="Is Fork", value=is_fork, inline=True)
        embed.add_field(name="Git URL", value=git_url, inline=False)
        embed.add_field(name="SSH URL", value=ssh_url, inline=False)
        embed.add_field(name="Latest Commit", value=f"[{latest_commit_message}]({latest_commit_html_url})", inline=False)
        embed.add_field(name="Latest Commit Author", value=latest_commit_author, inline=True)
        embed.add_field(name="Latest Commit Date", value=latest_commit_date, inline=True)
        embed.set_thumbnail(url=owner.get("avatar_url"))

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Github(bot))
