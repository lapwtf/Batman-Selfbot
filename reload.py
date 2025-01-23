import discord
from discord.ext import commands
import os
import sys
import json
import asyncio
import aiohttp

def load_config(file_path='config.json'):
    with open(file_path, 'r') as f:
        return json.load(f)

class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.restart_message_id = None
        self.restart_channel_id = None

    async def check_password(self, ctx):
        config = load_config()
        if not config['password']:
            await ctx.send("Please enter the security key using `$verify <key>`")
            return False
        return True

    async def get_command_help(self, command: str):
        command = command.lower()
        return self.command_help.get(command, "```Command help not available```")

    @commands.command()
    async def reload(self, ctx):
        if not await self.check_password(ctx):
            return
            
        msg = await ctx.send("```restarting```")
        try:
            with open("restart_info.txt", "w") as f:
                f.write(f"{msg.id}\n{ctx.channel.id}")
            
            await asyncio.sleep(1)
            python = sys.executable
            os.execv(python, ['python'] + sys.argv)
        except Exception as e:
            await ctx.send(f"```Error during restart: {str(e)}```")

    @commands.Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(2)
        
        try:
            if os.path.exists("restart_info.txt"):
                try:
                    with open("restart_info.txt", "r") as f:
                        lines = f.readlines()
                        if len(lines) >= 2:
                            msg_id = int(lines[0].strip())
                            channel_id = int(lines[1].strip())
                            
                            config = load_config()
                            headers = {
                                "Authorization": f"{config['token']}",
                                "Content-Type": "application/json"
                            }
                            
                            async with aiohttp.ClientSession() as session:
                                url = f"https://discord.com/api/v10/channels/{channel_id}/messages/{msg_id}"
                                async with session.patch(url, headers=headers, json={"content": "```restarted```"}) as response:
                                    if response.status == 200:
                                        print("-")
                                    else:
                                        print(f"Failed to edit message: {response.status}")
                except Exception as e:
                    print(f"Error reading restart_info.txt: {str(e)}")
                finally:
                    try:
                        os.remove("restart_info.txt")
                    except:
                        pass
        except Exception as e:
            print(f"Error in on_ready: {str(e)}")

def setup(bot):
    bot.add_cog(Reload(bot))
