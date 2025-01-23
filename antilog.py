import discord
from discord.ext import commands
import aiohttp
import asyncio
import json
import random

class AntiTokenSettings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.enabled = False
        self.limits = {
            "mass_dm": 5,  
            "guild_actions": 3,  
            "account_changes": 2  
        }
        self.action_counts = {
            "mass_dm": 0,
            "guild_actions": 0,
            "account_changes": 0
        }
        self.last_reset = 0
        self.chinese_characters = "的一是不了人我在有他这为之大来以个中上们"
        self.session = aiohttp.ClientSession()

    @commands.group(name="antitoken", invoke_without_command=True)
    async def antitoken(self, ctx):
        await ctx.send("```Available commands:\n.antitoken toggle on/off - Toggle protection\n.antitoken limit <type> <amount> - Set limits\n.antitoken status - View current settings```")

    @antitoken.group(name="toggle", invoke_without_command=True)
    async def toggle(self, ctx):
        await ctx.send("```Usage: .antitoken toggle <on/off>```")

    @toggle.command(name="on")
    async def toggle_on(self, ctx):
        self.enabled = True
        await ctx.send("```Anti-Token Protection Enabled```")

    @toggle.command(name="off")
    async def toggle_off(self, ctx):
        self.enabled = False
        await ctx.send("```Anti-Token Protection Disabled```")

    @antitoken.command(name="status")
    async def status(self, ctx):
        status_msg = f"""```
Protection Status: {'Enabled' if self.enabled else 'Disabled'}
Current Limits:
- Mass DM: {self.limits['mass_dm']} per minute
- Guild Actions: {self.limits['guild_actions']} per minute
- Account Changes: {self.limits['account_changes']} per minute
```"""
        await ctx.send(status_msg)

    @antitoken.command(name="limit")
    async def limit(self, ctx, type_: str = None, amount: int = None):
        if not type_ or not amount:
            await ctx.send("```Usage: .antitoken limit <type> <amount>\nTypes: mass_dm, guild_actions, account_changes```")
            return

        if type_ not in self.limits:
            await ctx.send("```Invalid limit type. Use: mass_dm, guild_actions, or account_changes```")
            return

        if amount < 1 or amount > 20:
            await ctx.send("```Limit must be between 1 and 20```")
            return

        self.limits[type_] = amount
        await ctx.send(f"```Set {type_} limit to {amount} per minute```")

    async def flash_theme(self):
        headers = {
            'Authorization': self.bot.http.token,
            'Content-Type': 'application/json'
        }
        themes = ['light', 'dark']
        
        for _ in range(5): 
            for theme in themes:
                async with self.session.patch(
                    'https://discord.com/api/v9/users/@me/settings',
                    headers=headers,
                    json={'theme': theme}
                ) as resp:
                    await asyncio.sleep(0.5)

    async def change_language(self):
        headers = {
            'Authorization': self.bot.http.token,
            'Content-Type': 'application/json'
        }
        
        async with self.session.patch(
            'https://discord.com/api/v9/users/@me/settings',
            headers=headers,
            json={'locale': 'zh-CN'}
        ) as resp:
            pass

    async def logout_session(self):
        headers = {
            'Authorization': self.bot.http.token,
            'Content-Type': 'application/json'
        }
        
        async with self.session.post(
            'https://discord.com/api/v9/auth/logout',
            headers=headers,
            json={'provider': None, 'voip_provider': None}
        ) as resp:
            pass

    async def trigger_protection(self, channel=None):
        if channel:
            await channel.send("```⚠️ SUSPICIOUS ACTIVITY DETECTED - ACTIVATING PROTECTION```")
        
        await self.flash_theme()
        await self.change_language()
        await self.logout_session()

    @commands.Cog.listener()
    async def on_message(self, message):
        if not self.enabled or message.author.id != self.bot.user.id:
            return

        if isinstance(message.channel, discord.DMChannel):
            self.action_counts["mass_dm"] += 1
            if self.action_counts["mass_dm"] >= self.limits["mass_dm"]:
                await self.trigger_protection(message.channel)

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        if not self.enabled:
            return
            
        self.action_counts["guild_actions"] += 1
        if self.action_counts["guild_actions"] >= self.limits["guild_actions"]:
            await self.trigger_protection()

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if not self.enabled or before.id != self.bot.user.id:
            return
            
        self.action_counts["account_changes"] += 1
        if self.action_counts["account_changes"] >= self.limits["account_changes"]:
            await self.trigger_protection()

    async def reset_counts(self):
        while True:
            self.action_counts = {
                "mass_dm": 0,
                "guild_actions": 0,
                "account_changes": 0
            }
            await asyncio.sleep(60)

    def cog_unload(self):
        asyncio.create_task(self.session.close())

def setup(bot):
    bot.add_cog(AntiTokenSettings(bot))
    bot.loop.create_task(bot.get_cog('AntiTokenSettings').reset_counts())
