import discord
from discord.ext import commands
import asyncio
import json
import random
import os
from datetime import datetime, timedelta

black = "\033[30m"
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
magenta = "\033[35m"
cyan = "\033[36m"
white = "\033[37m"
reset = "\033[0m"

class OwoHunt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_hunters = {}
        self.config_file = 'data/owohunt_config.json'
        self.load_config()
        self.commands = [
            "owo hunt",
            "owo battle",
            "owo pray",
            "owo curse",
            "owo cf 1000",
            "owo sell all"
        ]
        self.custom_responses = [
            "uwu",
            "owo",
            ";w;",
            ">w<",
            "^w^"
        ]

    def load_config(self):
        if not os.path.exists('data'):
            os.makedirs('data')
            
        default_config = {
            'hunt_delay': 16,
            'pray_interval': 301,
            'battle_interval': 181,
            'sell_interval': 601,
            'coinflip_interval': 121,
            'typing_speed': {
                'min': 100,
                'max': 200
            },
            'human_like_delay': {
                'min': 1,
                'max': 3
            }
        }
            
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                saved_config = json.load(f)
                self.config = default_config.copy()
                self.config.update(saved_config)
        else:
            self.config = default_config
            
        self.save_config()

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    async def simulate_typing(self, channel, text):
        async with channel.typing():
            delay = len(text) / random.randint(
                self.config['typing_speed']['min'],
                self.config['typing_speed']['max']
            )
            await asyncio.sleep(delay)

    async def send_command(self, ctx, command):
        await self.simulate_typing(ctx.channel, command)
        await ctx.send(command)
        await asyncio.sleep(random.uniform(
            self.config['human_like_delay']['min'],
            self.config['human_like_delay']['max']
        ))

    async def hunt_loop(self, ctx, user_id):
        last_pray = datetime.now()
        last_battle = datetime.now()
        last_sell = datetime.now()
        last_coinflip = datetime.now()

        while user_id in self.active_hunters:
            try:
                await self.send_command(ctx, "owo hunt")
                
                await asyncio.sleep(self.config['hunt_delay'])
                
                if random.random() < 0.3:
                    await asyncio.sleep(random.uniform(1, 2))
                    await self.send_command(ctx, random.choice(self.custom_responses))

                if (datetime.now() - last_pray).seconds >= self.config['pray_interval']:
                    await self.send_command(ctx, "owo pray")
                    await asyncio.sleep(1)
                    last_pray = datetime.now()

                if (datetime.now() - last_battle).seconds >= self.config['battle_interval']:
                    await self.send_command(ctx, "owo battle")
                    await asyncio.sleep(1)
                    last_battle = datetime.now()

                if (datetime.now() - last_sell).seconds >= self.config['sell_interval']:
                    await self.send_command(ctx, "owo sell all")
                    await asyncio.sleep(1)
                    last_sell = datetime.now()

                if (datetime.now() - last_coinflip).seconds >= self.config['coinflip_interval']:
                    await self.send_command(ctx, "owo cf 1000")
                    await asyncio.sleep(1)
                    last_coinflip = datetime.now()

            except Exception as e:
                print(f"Error in hunt loop: {str(e)}")
                await asyncio.sleep(5)

    @commands.group(invoke_without_command=True)
    async def autohunt(self, ctx):
        if ctx.author.id in self.active_hunters:
            await ctx.send(f"""```ansi
{black}[ {red}BATMAN AUTO HUNT {black}]
{black}[{white}Error{black}]
{black}⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
{black}[{white}Message{black}] {white}Auto hunt is already running
{black}[{white}Info{black}] {white}Use $autohunt stop to end the session```""")
            return

        await ctx.send(f"""```ansi
{black}[ {red}BATMAN AUTO HUNT {black}]
{black}[{white}Starting{black}]
{black}⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
{black}[{white}Status{black}] {white}Initializing auto hunt...
{black}[{white}Hunt Delay{black}] {white}{self.config['hunt_delay']} seconds
{black}[{white}Info{black}] {white}Use $autohunt stop to end the session```""")

        self.active_hunters[ctx.author.id] = True
        asyncio.create_task(self.hunt_loop(ctx, ctx.author.id))

    @autohunt.command(name='stop')
    async def stop_hunt(self, ctx):
        if ctx.author.id not in self.active_hunters:
            await ctx.send(f"""```ansi
{black}[ {red}BATMAN AUTO HUNT {black}]
{black}[{white}Error{black}]
{black}⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
{black}[{white}Message{black}] {white}No active auto hunt session```""")
            return

        del self.active_hunters[ctx.author.id]
        await ctx.send(f"""```ansi
{black}[ {red}BATMAN AUTO HUNT {black}]
{black}[{white}Success{black}]
{black}⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
{black}[{white}Message{black}] {white}Auto hunt stopped```""")

    @autohunt.command(name='settings')
    async def show_settings(self, ctx):
        settings_text = f"""```ansi
{black}[ {red}BATMAN AUTO HUNT SETTINGS {black}]

{black}[{white}Intervals{black}]
{black}⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
{black}[{white}Hunt Delay{black}] {white}{self.config['hunt_delay']}s
{black}[{white}Pray Interval{black}] {white}{self.config['pray_interval']}s
{black}[{white}Battle Interval{black}] {white}{self.config['battle_interval']}s
{black}[{white}Sell Interval{black}] {white}{self.config['sell_interval']}s
{black}[{white}Coinflip Interval{black}] {white}{self.config['coinflip_interval']}s

{black}[{white}Typing Settings{black}]
{black}⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
{black}[{white}Speed{black}] {white}{self.config['typing_speed']['min']}-{self.config['typing_speed']['max']} CPM
{black}[{white}Human Delay{black}] {white}{self.config['human_like_delay']['min']}-{self.config['human_like_delay']['max']}s```"""
        await ctx.send(settings_text)

    @autohunt.command(name='set')
    async def set_setting(self, ctx, setting: str, value: float):
        setting = setting.lower()
        
        if setting not in ['hunt_delay', 'pray', 'battle', 'sell', 'coinflip']:
            await ctx.send(f"""```ansi
{black}[ {red}BATMAN AUTO HUNT {black}]
{black}[{white}Error{black}]
{black}⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
{black}[{white}Message{black}] {white}Invalid setting
{black}[{white}Valid Settings{black}] {white}hunt_delay, pray, battle, sell, coinflip```""")
            return

        if setting == 'hunt_delay':
            self.config['hunt_delay'] = value
        elif setting == 'pray':
            self.config['pray_interval'] = value
        elif setting == 'battle':
            self.config['battle_interval'] = value
        elif setting == 'sell':
            self.config['sell_interval'] = value
        elif setting == 'coinflip':
            self.config['coinflip_interval'] = value

        self.save_config()
        await ctx.send(f"""```ansi
{black}[ {red}BATMAN AUTO HUNT {black}]
{black}[{white}Success{black}]
{black}⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
{black}[{white}Setting{black}] {white}{setting}
{black}[{white}New Value{black}] {white}{value}```""")

def setup(bot):
    bot.add_cog(OwoHunt(bot))
