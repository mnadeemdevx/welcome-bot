from multiprocessing import process
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
# import config
import asyncpg


load_dotenv()

cogs = ['cogs.dev', 'cogs.welcome']

class WelcomeBot(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix, intents=intents, **kwargs)
    
    async def setup_hook(self) -> None:
        try:
            db_config = os.getenv('DB_CONFIG')
            self.db = await asyncpg.create_pool(db_config)
            print("------- Databse is connected -------")
        except Exception as e:
            print(f"Failed to connect to database. {0}".format(e))
            return
        with open("schemas.sql") as f:
            await self.db.execute(f.read())
            print("------- Schemas are created -------")
        
        for cog in cogs:
            await self.load_extension(cog)
            print(f'{cog} is loaded.')
        
    async def on_ready(self):
        print("------ Bot is ready! -------")

if __name__=="__main__":
    token = os.getenv('DISCORD_TOKEN')
    bot = WelcomeBot(owner_id=947795908119109652, command_prefix="!", intents=discord.Intents.all())
    bot.run(token)

        
