from discord.ext import commands
from discord.commands import slash_command
import discord

from bs4 import BeautifulSoup
import requests

from datetime import datetime
import asyncio

from misc.misc import get_dt_now
from messages.messages import crs_post 

class CRSWebScraper(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    URL = "https://crs.upd.edu.ph/auth/index/announcements"
    DELAY = 1   # check every 1 second

    async def check(self):
        while(1):
            page = requests.get(self.URL)
            soup = BeautifulSoup(page.text, "html.parser")

            list_items = soup.find_all("li")

            if list_items:
                announcement = list_items[0]

                datetime_str = announcement.time.text
                timestamp = datetime.strptime(datetime_str, "%B %d, %Y %H:%M %p")
                datetime_now = get_dt_now().replace(tzinfo=None)

                if timestamp <= datetime_now:
                    body = announcement.find_all("p")[1:]

                    dst_guild = discord.utils.get(self.bot.guilds, id=780619726568947723)
                    dst_channel = dst_guild.get_channel(833541236387479573)

                    await dst_channel.send(crs_post.format(
                        mention = "@everyone",
                        title = announcement.h2.text.strip(),
                        content = ('\n\n'.join([p.text for p in body])).lstrip()[:1500] + "[...Read More](https://crs.upd.edu.ph)",
                        timestamp = datetime.strftime(timestamp, "%B %d, %Y %H:%M %p")
                    ))
                print("Currently updated")
            else:
                print("No new announcements...")

            await asyncio.sleep(self.DELAY)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} ready!')
        self.bot.loop.create_task(self.check())

def setup(bot):
    bot.add_cog(CRSWebScraper(bot))