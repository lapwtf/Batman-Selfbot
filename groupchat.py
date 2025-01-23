import json

def load_config(file_path='config.json'):
    with open(file_path, 'r') as f:
        return json.load(f)

def check_password(password, config):
    return password == config.get('password')

import discord
from discord.ext import commands
import asyncio
import aiohttp
import json

class GroupChatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not hasattr(bot, 'mimic_tasks'):
            bot.mimic_tasks = {}
        if not hasattr(bot, 'gc_config'):
            bot.gc_config = {
                "enabled": False,
                "whitelist": [],
                "blacklist": [],
                "silent": True,
                "leave_message": "Goodbye.",
                "remove_blacklisted": True,
                "webhook_url": None,
                "auto_block": False
            }
            self.save_gc_config()
            
        self.autogc_enabled = False
        self.autoleave_enabled = False
        self.gc_whitelist = set()
        self.load_whitelist()

    def save_gc_config(self):
        with open('gc_config.json', 'w') as f:
            json.dump(self.bot.gc_config, f, indent=4)

    def load_gc_config(self):
        try:
            with open('gc_config.json', 'r') as f:
                self.bot.gc_config.update(json.load(f))
        except FileNotFoundError:
            self.save_gc_config()

    def save_whitelist(self):
        with open('gc_whitelist.json', 'w') as f:
            json.dump(list(self.gc_whitelist), f)
            
    def load_whitelist(self):
        try:
            with open('gc_whitelist.json', 'r') as f:
                self.gc_whitelist = set(json.load(f))
        except FileNotFoundError:
            self.save_whitelist()

    @commands.command()
    async def mimic(self, ctx, user: discord.Member):
        if user.id in self.bot.mimic_tasks:
            self.bot.mimic_tasks[user.id].cancel()
            del self.bot.mimic_tasks[user.id]
            await ctx.send(f"```Stopped mimicking {user.name}```")
            return

        headers = {
            "authorization": self.bot.http.token,
            "content-type": "application/json"
        }

        last_message_id = None
        cached_messages = {}
        
        blocked_content = [
            "underage", "minor", "year old", "yo", "years old",
            "10", "11", "9", "8", "7", "6", "5", "4", "3", "1", "2",
            "12", "13", "14", "mute", "/kick", "/mute", ".kick", ".mute",
            "-kick", "-mute", "$kick", "ban", "two", "three", "four", 
            "five", "six", "seven", "eight", "nine", "ten", "eleven", 
            "twelve", "thirteen", "self-bot", "self bot", "nsfw", 
            "porn", "hentai", "nude", "nudes"
        ]

        async def mimic_task():
            nonlocal last_message_id
            while user.id in self.bot.mimic_tasks:
                try:
                    params = {'after': last_message_id} if last_message_id else {'limit': 1}
                    async with aiohttp.ClientSession() as session:
                        async with session.get(
                            f"https://discord.com/api/v9/channels/{ctx.channel.id}/messages",
                            headers=headers,
                            params=params
                        ) as response:
                            if response.status == 200:
                                messages = await response.json()
                                for msg in reversed(messages):
                                    if msg['author']['id'] == str(user.id):
                                        content = msg.get('content', '').lower()
                                        if any(word in content for word in blocked_content):
                                            continue
                                        
                                        content = msg.get('content', '')
                                        while content.startswith('.'):
                                            content = content[1:].lstrip()
                                            
                                        if not content:
                                            continue
                                            
                                        if content[:3].count('.') > 1:
                                            continue

                                        if content.startswith(('!', '?', '-', '$', '/', '>', '<')):
                                            continue
                                        
                                        if not content and msg.get('referenced_message'):
                                            content = f"Reply to: {msg['referenced_message'].get('content', '[Content Hidden]')}"
                                        elif not content and msg.get('mentions'):
                                            content = f"Mentioned: {', '.join(m['username'] for m in msg['mentions'])}"
                                        elif not content:
                                            if msg.get('embeds'):
                                                embed = msg['embeds'][0]
                                                content = embed.get('description', embed.get('title', '[Embed]'))
                                            elif msg.get('attachments'):
                                                content = '[' + ', '.join(a['filename'] for a in msg['attachments']) + ']'
                                            else:
                                                continue
                                                
                                        if any(word in content.lower() for word in blocked_content):
                                            continue
                                        
                                        if msg['id'] not in cached_messages:
                                            cached_messages[msg['id']] = True
                                            
                                            payload = {
                                                "content": content,
                                                "tts": False
                                            }
                                            
                                            if msg.get('embeds'):
                                                payload['embeds'] = msg['embeds']
                                            
                                            async with session.post(
                                                f"https://discord.com/api/v9/channels/{ctx.channel.id}/messages",
                                                headers=headers,
                                                json=payload
                                            ) as _:
                                                pass
                                            
                                            await asyncio.sleep(0.5)
                                        
                                        last_message_id = msg['id']
                except Exception as e:
                    print(f"Mimic Error: {e}")
                await asyncio.sleep(1)

        task = self.bot.loop.create_task(mimic_task())
        self.bot.mimic_tasks[user.id] = task
        await ctx.send(f"```Started mimicking {user.name}```")

    @commands.group(invoke_without_command=True)
    async def antigcspam(self, ctx):
        if ctx.invoked_subcommand is None:
            self.bot.gc_config["enabled"] = not self.bot.gc_config["enabled"]
            self.save_gc_config()
            
            status = f"""```ansi
Anti GC-Spam Status
Enabled: {self.bot.gc_config["enabled"]}
Silent Mode: {self.bot.gc_config["silent"]}
Auto Remove Blacklisted: {self.bot.gc_config["remove_blacklisted"]}
Auto Block: {self.bot.gc_config["auto_block"]}
Whitelisted Users: {len(self.bot.gc_config["whitelist"])}
Blacklisted Users: {len(self.bot.gc_config["blacklist"])}
Webhook: {"Set" if self.bot.gc_config["webhook_url"] else "Not Set"}
Leave Message: {self.bot.gc_config["leave_message"]}```"""
            await ctx.send(status)

    @antigcspam.command(name="whitelist")
    async def gc_whitelist(self, ctx, user: discord.User):
        if user.id not in self.bot.gc_config["whitelist"]:
            self.bot.gc_config["whitelist"].append(user.id)
            self.save_gc_config()
            await ctx.send(f"```{user.name} can now add you to group chats```")
        else:
            await ctx.send(f"```{user.name} is already allowed to add you to group chats```")

    @antigcspam.command(name="unwhitelist")
    async def gc_unwhitelist(self, ctx, user: discord.User):
        if user.id in self.bot.gc_config["whitelist"]:
            self.bot.gc_config["whitelist"].remove(user.id)
            self.save_gc_config()
            await ctx.send(f"```Removed {user.name} from whitelist```")
        else:
            await ctx.send(f"```{user.name} is not whitelisted```")

    @antigcspam.command(name="blacklist")
    async def gc_blacklist(self, ctx, user: discord.User):
        if user.id not in self.bot.gc_config["blacklist"]:
            self.bot.gc_config["blacklist"].append(user.id)
            self.save_gc_config()
            headers = {
                'Authorization': self.bot.http.token,
                'Content-Type': 'application/json'
            }
            
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.delete(
                        f'https://discord.com/api/v9/users/@me/relationships/{user.id}',
                        headers=headers
                    ) as resp:
                        if resp.status == 204:
                            await ctx.send(f"```Added {user.name} to blacklist and removed friend```")
                            return
                            
            except Exception as e:
                print(f"Error removing friend: {e}")
                
            await ctx.send(f"```Added {user.name} to blacklist```")
        else:
            await ctx.send(f"```{user.name} is already blacklisted```")

    @antigcspam.command(name="unblacklist")
    async def gc_unblacklist(self, ctx, user: discord.User):
        if user.id in self.bot.gc_config["blacklist"]:
            self.bot.gc_config["blacklist"].remove(user.id)
            self.save_gc_config()
            await ctx.send(f"```Removed {user.name} from blacklist```")
        else:
            await ctx.send(f"```{user.name} is not blacklisted```")

    @antigcspam.command(name="silent")
    async def gc_silent(self, ctx, mode: bool):
        self.bot.gc_config["silent"] = mode
        self.save_gc_config()
        await ctx.send(f"```Silent mode {'enabled' if mode else 'disabled'}```")

    @antigcspam.command(name="message")
    async def gc_message(self, ctx, *, message: str):
        self.bot.gc_config["leave_message"] = message
        self.save_gc_config()
        await ctx.send(f"```Leave message set to: {message}```")

    @antigcspam.command(name="autoremove")
    async def gc_autoremove(self, ctx, mode: bool):
        self.bot.gc_config["remove_blacklisted"] = mode
        self.save_gc_config()
        await ctx.send(f"```Auto-remove blacklisted users {'enabled' if mode else 'disabled'}```")

    @antigcspam.command(name="webhook")
    async def gc_webhook(self, ctx, url: str = None):
        self.bot.gc_config["webhook_url"] = url
        self.save_gc_config()
        if url:
            await ctx.send("```Webhook URL set```")
        else:
            await ctx.send("```Webhook removed```")

    @antigcspam.command(name="autoblock")
    async def gc_autoblock(self, ctx, mode: bool):
        self.bot.gc_config["auto_block"] = mode
        self.save_gc_config()
        await ctx.send(f"```Auto-block {'enabled' if mode else 'disabled'}```")

    @antigcspam.command(name="list")
    async def gc_list(self, ctx):
        whitelisted = "\n".join([f"• {self.bot.get_user(uid).name}" for uid in self.bot.gc_config["whitelist"] if self.bot.get_user(uid)])
        blacklisted = "\n".join([f"• {self.bot.get_user(uid).name}" for uid in self.bot.gc_config["blacklist"] if self.bot.get_user(uid)])
        
        status = f"""```ansi
Whitelisted Users:
{whitelisted if whitelisted else "None"}

Blacklisted Users:
{blacklisted if blacklisted else "None"}```"""
        await ctx.send(status)

    @commands.group(invoke_without_command=True)
    async def autogc(self, ctx):
        self.autogc_enabled = True
        await ctx.send("```ansi\nAuto group chat enabled```")

    @autogc.command(name="stop")
    async def autogc_stop(self, ctx):
        self.autogc_enabled = False
        await ctx.send("```ansi\nAuto group chat disabled```")

    @autogc.command(name="whitelist")
    async def autogc_whitelist(self, ctx, user: discord.User):
        self.gc_whitelist.add(user.id)
        self.save_whitelist()
        await ctx.send(f"```ansi\nAdded {user.name} to whitelist```")

    @autogc.command(name="whitelistr")
    async def autogc_whitelist_remove(self, ctx, user: discord.User):
        if user.id in self.gc_whitelist:
            self.gc_whitelist.remove(user.id)
            self.save_whitelist()
            await ctx.send(f"```Removed {user.name} from whitelist```")
        else:
            await ctx.send("```ansi\nUser not in whitelist```")

    @autogc.command(name="list")
    async def autogc_list(self, ctx):
        if not self.gc_whitelist:
            await ctx.send("```ansi\nNo users in whitelist```")
            return
        
        users = []
        for user_id in self.gc_whitelist:
            try:
                user = await self.bot.fetch_user(user_id)
                users.append(f"• {user.name}")
            except:
                users.append(f"• Unknown User ({user_id})")
        
        await ctx.send(f"```Whitelisted Users:\n\n{chr(10).join(users)}```")

    @commands.group(invoke_without_command=True)
    async def autogcleave(self, ctx):
        if ctx.invoked_subcommand is None:
            self.autoleave_enabled = True
            await ctx.send("```ansi\nAuto leave enabled```")

    @autogcleave.command(name="stop")
    async def autogcleave_stop(self, ctx):
        self.autoleave_enabled = False
        await ctx.send("```ansi\nAuto leave disabled```")

    @autogcleave.command(name="status")
    async def autogcleave_status(self, ctx):
        status = "enabled" if self.autoleave_enabled else "disabled"
        await ctx.send(f"```ansi\nAuto leave is currently {status}```")

def setup(bot):
    bot.add_cog(GroupChatCog(bot))
