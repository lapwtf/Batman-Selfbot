import discord
from discord.ext import commands
import os
import json
import shutil
import subprocess
import asyncio

def load_config(file_path='config.json'):
    with open(file_path, 'r') as f:
        return json.load(f)

class HostCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.restricted_commands = [
            "nuke", "massban", "masschannels", "massroles",
            "spam", "webhook", "massdm", "tokenspam"
        ]

    def is_hosted_instance(self):
        return os.path.exists("hosted_instance.flag")

    async def check_command_permission(self, ctx, command_name):
        if self.is_hosted_instance() and command_name in self.restricted_commands:
            await ctx.send("```This command is restricted in hosted instances```")
            return False
        return True

    async def validate_token(self, token):
        try:
            test_client = discord.Client()
            async with test_client:
                await test_client.login(token)
                return True
        except:
            return False
        finally:
            await test_client.close()

    @commands.group(invoke_without_command=True)
    async def host(self, ctx):
        await ctx.send("""```
Host Commands:
$host create <token> <name> - Create a new hosted instance
$host launch - Launch the most recent instance
$host tokens clear - Clear tokens from hosted instance
$host tokens add <token> - Add token to hosted instance
$host restrict <command> - Add command to restricted list
$host unrestrict <command> - Remove command from restricted list
$host list - List all restricted commands```""")

    @host.command(name="create")
    async def host_create(self, ctx, token: str = None, name: str = None):
        if not token or not name:
            await ctx.send("```Usage: $host create <discord_token> <name>```")
            return
            
        try:
            msg = await ctx.send("```Validating token...```")
            
            if not await self.validate_token(token):
                await msg.edit(content="```Error: Invalid Discord token```")
                return

            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            new_dir = os.path.join(parent_dir, name)
            
            await msg.edit(content="```Creating new instance...```")
            
            if os.path.exists(new_dir):
                await msg.edit(content="```Error: Directory with that name already exists```")
                return
                
            shutil.copytree(current_dir, new_dir)
            
            with open(os.path.join(new_dir, "hosted_instance.flag"), "w") as f:
                f.write("")
            
            config_path = os.path.join(new_dir, 'config.json')
            if os.path.exists(config_path):
                config = {'token': token, 'verify': False}
                with open(config_path, 'w') as f:
                    json.dump(config, f, indent=4)
            
            with open(os.path.join(new_dir, 'token.txt'), 'w') as f:
                f.write(token)
            
            await msg.edit(content=f"""```ansi
\u001b[0;32mNew instance created successfully\u001b[0m
Location: {new_dir}
Use $host launch to start the instance```""")
            
        except Exception as e:
            await ctx.send(f"```Error creating instance: {str(e)}```")

    @host.command(name="launch")
    async def host_launch(self, ctx):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            
            dirs = [d for d in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, d))]
            if not dirs:
                await ctx.send("```No hosted instances found```")
                return
                
            newest_dir = max([os.path.join(parent_dir, d) for d in dirs], key=os.path.getctime)
            script_path = os.path.join(newest_dir, 'phantom.py')
            
            if not os.path.exists(script_path):
                await ctx.send("```Error: phantom.py not found in instance directory```")
                return
                
            msg = await ctx.send("```Launching instance...```")
            
            subprocess.Popen(['python', script_path], 
                            creationflags=subprocess.CREATE_NEW_CONSOLE,
                            cwd=newest_dir)
            
            await msg.edit(content=f"""```ansi
\u001b[0;32mInstance launched successfully\u001b[0m
Location: {newest_dir}```""")
            
        except Exception as e:
            await ctx.send(f"```Error launching instance: {str(e)}```")

    @host.group(name="tokens")
    async def host_tokens(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("```Usage: $host tokens <clear/add>```")

    @host_tokens.command(name="clear")
    async def tokens_clear(self, ctx):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            
            dirs = [d for d in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, d))]
            if not dirs:
                await ctx.send("```No hosted instances found```")
                return
                
            newest_dir = max([os.path.join(parent_dir, d) for d in dirs], key=os.path.getctime)
            tokens_file = os.path.join(newest_dir, 'token.txt')
            
            if not os.path.exists(tokens_file):
                await ctx.send("```No token.txt found in host directory```")
                return
                
            with open(tokens_file, 'w') as f:
                f.write('')
                
            await ctx.send("""```ansi
\u001b[0;32mTokens cleared successfully\u001b[0m```""")
            
        except Exception as e:
            await ctx.send(f"```Error clearing tokens: {str(e)}```")

    @host_tokens.command(name="add")
    async def tokens_add(self, ctx, token: str = None):
        if not token:
            await ctx.send("```Usage: $host tokens add <token>```")
            return
            
        try:
            msg = await ctx.send("```Validating token...```")
            
            if not await self.validate_token(token):
                await msg.edit(content="```Error: Invalid Discord token```")
                return

            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            
            dirs = [d for d in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, d))]
            if not dirs:
                await ctx.send("```No hosted instances found```")
                return
                
            newest_dir = max([os.path.join(parent_dir, d) for d in dirs], key=os.path.getctime)
            tokens_file = os.path.join(newest_dir, 'token.txt')
            
            if not os.path.exists(tokens_file):
                with open(tokens_file, 'w') as f:
                    f.write(token)
                await msg.edit(content="""```ansi
\u001b[0;32mToken added as first line\u001b[0m```""")
                return
                
            with open(tokens_file, 'r') as f:
                tokens = f.read().splitlines()
                
            if not tokens or not tokens[0].strip():
                tokens = [token]
            else:
                tokens.append(token)
                
            with open(tokens_file, 'w') as f:
                f.write('\n'.join(tokens))
                
            await msg.edit(content=f"""```ansi
\u001b[0;32mToken added successfully\u001b[0m
Position: {'First line' if len(tokens) == 1 else f'Line {len(tokens)}'}```""")
            
        except Exception as e:
            await ctx.send(f"```Error adding token: {str(e)}```")

    @host.command(name="restrict")
    async def host_restrict(self, ctx, command: str):
        if command not in self.restricted_commands:
            self.restricted_commands.append(command)
            await ctx.send(f"```Added {command} to restricted commands```")
        else:
            await ctx.send("```Command already restricted```")

    @host.command(name="unrestrict")
    async def host_unrestrict(self, ctx, command: str):
        if command in self.restricted_commands:
            self.restricted_commands.remove(command)
            await ctx.send(f"```Removed {command} from restricted commands```")
        else:
            await ctx.send("```Command not in restricted list```")

    @host.command(name="list")
    async def host_list(self, ctx):
        if not self.restricted_commands:
            await ctx.send("```No commands are currently restricted```")
            return
            
        commands_list = "\n".join(self.restricted_commands)
        await ctx.send(f"""```
Restricted Commands:
{commands_list}```""")

def setup(bot):
    bot.add_cog(HostCog(bot))
