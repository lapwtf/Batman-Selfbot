import discord
from discord.ext import commands
import os
import json
import random
import string
import aiohttp
import sys
import asyncio
import base64
import colorama
from colorama import Fore
from help import HelpMenu
from datetime import datetime
from itertools import cycle

with open('config.json') as f:
    config = json.load(f)

def load_tokens(file_path='token.txt'):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    return []
tokens = load_tokens()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='x', self_bot=True, intents=intents)
bot.remove_command('help')

try:
    bot.load_extension('help')
    print(f"{Fore.GREEN}[SUCCESS] Help cog loaded successfully")
except Exception as e:
    print(f"{Fore.RED}[ERROR] Failed to load help cog: {str(e)}")
    os.system('cls')

HELP_PATH = "help.py"
help_process = None

def loads_tokens(file_path='token.txt'):
    with open(file_path, 'r') as file:
        tokens = file.readlines()
    return [token.strip() for token in tokens if token.strip()]


TOKEN_FILE_PATH = "token.txt"
tokens = load_tokens()

black = "\033[30m"
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
magenta = "\033[35m"
cyan = "\033[36m"
white = "\033[37m"
reset = "\033[0m"  
pink = "\033[38;2;255;192;203m"
white = "\033[37m"
blue = "\033[34m"
black = "\033[30m"
light_green = "\033[92m" 
light_yellow = "\033[93m" 
light_magenta = "\033[95m" 
light_cyan = "\033[96m"  
light_red = "\033[91m"  
light_blue = "\033[94m"  



www = Fore.WHITE
mkk = Fore.BLUE
b = Fore.BLACK
ggg = Fore.LIGHTGREEN_EX
y = Fore.LIGHTYELLOW_EX 
pps = Fore.LIGHTMAGENTA_EX
c = Fore.LIGHTCYAN_EX
lr = Fore.LIGHTRED_EX
qqq = Fore.MAGENTA
lbb = Fore.LIGHTBLUE_EX
mll = Fore.LIGHTBLUE_EX
mjj = Fore.RED
yyy = Fore.YELLOW



@bot.event
async def on_ready():
    print(f"dude {bot.user.name}")
    global autoclear_task
    
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    if config.get('autoclear', False):
        autoclear_task = asyncio.create_task(autoclear_loop())
        print(f"{Fore.LIGHTMAGENTA_EX}Autoclear enabled from config")

    if config.get('autofill', False):
        print(f"{Fore.LIGHTMAGENTA_EX}Autofill enabled from config")

    global proxy_enabled
    
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            
        if config.get('proxysupport', False):
            if load_proxies():
                proxy_enabled = True
                print(f"{Fore.LIGHTGREEN_EX}Proxy support enabled from config with {len(proxies)} proxies")
            else:
                print(f"{Fore.RED}Failed to load proxies from config")
    except Exception as e:
        print(f"{Fore.RED}Error loading proxy config: {e}")

    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            
        if config.get('antitrap', False):
            print(f"{Fore.LIGHTMAGENTA_EX}Antitrap enabled from config")
            
            if config['atwhitelist']:
                whitelist_users = []
                for user_id in config['atwhitelist']:
                    try:
                        user = await bot.fetch_user(user_id)
                        whitelist_users.append(f"{user.name} ({user_id})")
                    except:
                        whitelist_users.append(f"Unknown User ({user_id})")
                
                print(f"{Fore.LIGHTGREEN_EX}Antitrap whitelist loaded:")
                for user in whitelist_users:
                    print(f"{Fore.LIGHTGREEN_EX}  • {user}")
            else:
                print(f"{Fore.YELLOW}No users in antitrap whitelist")
                
        if config.get('blockonadd', False):
            print(f"{Fore.LIGHTMAGENTA_EX}Block on add enabled from config")
    except Exception as e:
        print(f"{Fore.RED}Error loading antitrap config: {str(e)}")

@bot.event
async def on_private_channel_create(channel):
    """Event handler for when a new group chat is created"""
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            
        if not isinstance(channel, discord.GroupChannel):
            return

        headers = {
            'Authorization': config['token'],
            'Content-Type': 'application/json'
        }
        
        await asyncio.sleep(2)
        
        try:
            async for msg in channel.history(limit=1):
                creator = msg.author
                print(f"{Fore.YELLOW}[ANTITRAP] GC created by: {creator.name} ({creator.id})")
                
                if config.get('antitrap', False):
                    if config['atwhitelist'] and creator.id in config['atwhitelist']:
                        print(f"{Fore.GREEN}[ANTITRAP] Whitelisted user {creator.name}, allowing GC")
                        
                        if config.get('autofill', False):
                            async with aiohttp.ClientSession() as session:
                                async with session.get(
                                    f'https://discord.com/api/v9/channels/{channel.id}',
                                    headers=headers
                                ) as resp:
                                    if resp.status != 200:
                                        print(f"{Fore.RED}[AUTOFILL] Not in group chat yet, waiting...")
                                        await asyncio.sleep(3)

                            tokens = loads_tokens()
                            limited_tokens = tokens[:12]

                            async def add_token_to_gc(token):
                                try:
                                    headers = {
                                        'Authorization': token.strip(),
                                        'Content-Type': 'application/json'
                                    }
                                    
                                    async with aiohttp.ClientSession() as session:
                                        async with session.put(
                                            f'https://discord.com/api/v9/channels/{channel.id}',
                                            headers=headers
                                        ) as resp:
                                            if resp.status == 204:
                                                print(f"{Fore.GREEN}[AUTOFILL] Added token {token[-4:]} to group")
                                            elif resp.status == 429:
                                                retry_after = float((await resp.json()).get('retry_after', 1))
                                                print(f"{Fore.YELLOW}[AUTOFILL] Rate limited, waiting {retry_after}s...")
                                                await asyncio.sleep(retry_after)
                                                return await add_token_to_gc(token)
                                            elif resp.status == 403:
                                                print(f"{Fore.RED}[AUTOFILL] Token {token[-4:]} failed to join (403)")
                                            else:
                                                print(f"{Fore.RED}[AUTOFILL] Failed to add token {token[-4:]}: Status {resp.status}")
                                                
                                except Exception as e:
                                    print(f"{Fore.RED}[AUTOFILL] Error adding token {token[-4:]}: {e}")

                            for token in limited_tokens:
                                if token != config['token']:
                                    await add_token_to_gc(token)
                                    await asyncio.sleep(0.5)
                        return

                    if config.get('blockonadd', False):
                        async with aiohttp.ClientSession() as session:
                            async with session.put(
                                f'https://discord.com/api/v9/users/@me/relationships/{creator.id}',
                                headers=headers,
                                json={"type": 2}
                            ) as resp:
                                if resp.status == 204:
                                    print(f"{Fore.GREEN}[ANTITRAP] Blocked user: {creator.name}")
                                else:
                                    print(f"{Fore.RED}[ANTITRAP] Failed to block user. Status: {resp.status}")

        except Exception as e:
            print(f"{Fore.YELLOW}[ANTITRAP] Couldn't get creator info: {e}")

        if config.get('antitrap', False):
            async with aiohttp.ClientSession() as session:
                for _ in range(3):
                    try:
                        async with session.delete(
                            f'https://discord.com/api/v9/channels/{channel.id}?silent=true',
                            headers=headers
                        ) as resp:
                            if resp.status == 200:
                                print(f"{Fore.GREEN}[ANTITRAP] Successfully left group chat: {channel.id}")
                                return
                            elif resp.status == 429:
                                retry_after = int(resp.headers.get("Retry-After", 1))
                                print(f"{Fore.YELLOW}[ANTITRAP] Rate limited. Waiting {retry_after} seconds...")
                                await asyncio.sleep(retry_after)
                            else:
                                print(f"{Fore.RED}[ANTITRAP] Failed to leave GC. Status: {resp.status}")
                                await asyncio.sleep(1)
                    except Exception as e:
                        print(f"{Fore.RED}[ANTITRAP] Error during leave attempt: {e}")
                        await asyncio.sleep(1)
        
        elif config.get('autofill', False):
            tokens = loads_tokens()
            limited_tokens = tokens[:12]

            async def add_token_to_gc(token):
                try:
                    headers = {
                        'Authorization': token.strip(),
                        'Content-Type': 'application/json'
                    }
                    
                    async with aiohttp.ClientSession() as session:
                        async with session.put(
                            f'https://discord.com/api/v9/channels/{channel.id}',
                            headers=headers
                        ) as resp:
                            if resp.status == 204:
                                print(f"{Fore.GREEN}[AUTOFILL] Added token {token[-4:]} to group")
                            elif resp.status == 429:
                                retry_after = float((await resp.json()).get('retry_after', 1))
                                await asyncio.sleep(retry_after)
                                return await add_token_to_gc(token)
                            else:
                                print(f"{Fore.RED}[AUTOFILL] Failed to add token {token[-4:]}: Status {resp.status}")
                                
                except Exception as e:
                    print(f"{Fore.RED}[AUTOFILL] Error adding token {token[-4:]}: {e}")

            for token in limited_tokens:
                if token != config['token']:
                    await add_token_to_gc(token)
                    await asyncio.sleep(0.5)
                    
    except Exception as e:
        print(f"{Fore.RED}[ERROR] {str(e)}")

@bot.command(name='help')
async def help(ctx):
    if not hasattr(bot.get_cog('Help'), 'menus'):
        bot.get_cog('Help').menus = {}
        bot.get_cog('Help').menu_messages = {}
    
    bot.get_cog('Help').menus[ctx.author.id] = HelpMenu()
    current_menu = bot.get_cog('Help').menus[ctx.author.id]

    await ctx.send(f"```ansi\n{mjj}Welcome: {bot.user.display_name}{reset}```")
    menu_msg = await ctx.send(current_menu.current_category())
    bot.get_cog('Help').menu_messages[ctx.author.id] = menu_msg
    await ctx.send(f"```ansi\n{mjj}use commands 'next' or 'back' to navigate{reset}```")

autoreplies = [
    "YO JR LETS BOX AGAIN LMFAO",
    "YO FAGGOT ILL LOVE TO RIP YOUR HEART OUT",
    "COME MEET YOUR MATCH PUSSY",
    "wtf is a {user}",
    "idk you random fuck out my face",
    "nigga you suck lets go forever",
    "yo {user} you suck",
    "yo {user} stop touching your nipples",
    "nigga got schizophrenia from his own voice",
    "this nigga got a open minded lisp",
    "yo {user} beg for this forgiveness",
    "maybe ill show mercy and stop hoeing you",
    "this is forever {user}"
]

ar2_replies = [
    "YOU\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nFUCKING\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nSUCK\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nDIE",
    "YO\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nBICH\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nFOCUS\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nUP\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nLOSER",
    "GET\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nYOUR\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nHEAD\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nCHOPPED\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nOFF"
]

autoreply_tasks = {}

@bot.command(name='ar')
async def auto_reply(ctx, user: discord.Member = None, name: str = None):
    if user is None or name is None:
        await ctx.send("```Usage: xar @user name\nExample: xar @john dummy```")
        return
        
    if ctx.author.id in autoreply_tasks:
        await ctx.send("You already have an auto-reply running. Use 'xarmercy' to end it first.")
        return

    used_replies = []
    base_delay = 0.255
    max_delay = 10.0

    async def send_autoreply(message):
        nonlocal used_replies
        current_delay = base_delay
        
        while True:
            try:
                if len(used_replies) >= len(autoreplies):
                    used_replies = []
                
                available_replies = [r for r in autoreplies if r not in used_replies]
                reply = random.choice(available_replies)
                used_replies.append(reply)
                
                reply = reply.replace("{user}", name)
                
                await message.reply(reply)
                print(f"{Fore.GREEN}[SUCCESS] Replied to {user.name}")
                current_delay = base_delay
                break

            except discord.errors.HTTPException as e:
                if e.status == 429:
                    try:
                        print(f"{Fore.YELLOW}[RATELIMIT] Waiting {current_delay:.2f} seconds...")
                        await asyncio.sleep(current_delay)
                        current_delay = min(current_delay + 0.5, max_delay)
                    except:
                        await asyncio.sleep(current_delay)
                else:
                    print(f"{Fore.RED}[ERROR] HTTP Error: {e}, retrying...")
                    await asyncio.sleep(1)
            except Exception as e:
                print(f"{Fore.RED}[ERROR] Failed to send message: {e}")
                await asyncio.sleep(1)

    async def reply_loop():
        def check(m):
            return m.author == user and m.channel == ctx.channel

        while True:
            try:
                message = await bot.wait_for('message', check=check)
                asyncio.create_task(send_autoreply(message))
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"{Fore.RED}[ERROR] Reply loop error: {e}")
                await asyncio.sleep(1)
                continue

    task = bot.loop.create_task(reply_loop())
    autoreply_tasks[ctx.author.id] = task
    await ctx.send(f"```Started auto-replying to {user.name}'s messages```")

@bot.command(name='ar2')
async def auto_reply2(ctx, user: discord.Member = None, token_position: int = None, name: str = None):
    if user is None or token_position is None or name is None:
        await ctx.send("```Usage: xar2 @user position name```")
        return
        
    if ctx.author.id in autoreply_tasks:
        await ctx.send("You already have an auto-reply running. Use 'xarmercy' to end it first.")
        return

    if token_position < 1 or token_position > len(tokens):
        await ctx.send(f"```Invalid token position. Please use a number between 1 and {len(tokens)}```")
        return

    token = tokens[token_position - 1].strip().replace('"', '').replace("'", "")
    used_replies = []
    base_delay = 0.255
    max_delay = 10.0

    async def send_autoreply(message):
        nonlocal used_replies
        current_delay = base_delay
        
        while True:
            try:
                async with await create_proxy_session() as session:
                    headers = {
                        'Authorization': token,
                        'Content-Type': 'application/json'
                    }

                    if len(used_replies) >= len(autoreplies):
                        used_replies = []
                    
                    available_replies = [r for r in autoreplies if r not in used_replies]
                    reply = random.choice(available_replies)
                    used_replies.append(reply)
                    
                    reply = reply.replace("{user}", name)
                    
                    async with session.post(
                        f'https://discord.com/api/v9/channels/{ctx.channel.id}/messages',
                        headers=headers,
                        json={
                            'content': reply,
                            'message_reference': {'message_id': message.id}
                        }
                    ) as resp:
                        if resp.status == 429:
                            print(f"{Fore.YELLOW}[RATELIMIT] Waiting {current_delay:.2f} seconds...")
                            await asyncio.sleep(current_delay)
                            current_delay = min(current_delay + 0.5, max_delay)
                            continue
                        elif resp.status == 403:
                            print(f"{Fore.RED}[ERROR] Token {token_position} received 403 error")
                            return
                        elif resp.status == 200:
                            print(f"{Fore.GREEN}[SUCCESS] Replied to {user.name}")
                            current_delay = base_delay
                            break
                        else:
                            print(f"{Fore.RED}[ERROR] Status {resp.status}")
                            await asyncio.sleep(2)
                            continue

            except Exception as e:
                print(f"{Fore.RED}[ERROR] Failed to send message: {e}")
                await asyncio.sleep(1)

    async def reply_loop():
        def check(m):
            return m.author == user and m.channel == ctx.channel

        while True:
            try:
                message = await bot.wait_for('message', check=check)
                asyncio.create_task(send_autoreply(message))
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"{Fore.RED}[ERROR] Reply loop error: {e}")
                await asyncio.sleep(1)
                continue

    task = asyncio.create_task(reply_loop())
    autoreply_tasks[ctx.author.id] = task
    await ctx.send(f"```Started auto-replying to {user.name} using token {token_position}```")

@bot.command(name='ar3')
async def auto_reply3(ctx, user: discord.Member = None):
    if user is None:
        await ctx.send("```Usage: xar3 @user\nExample: xar3 @john```")
        return
        
    if ctx.author.id in autoreply_tasks:
        await ctx.send("```ay you already hoeing LMFAOO```")
        return

    used_replies = []
    base_delay = 0.255
    max_delay = 10.0

    async def send_autoreply(message):
        nonlocal used_replies
        current_delay = base_delay
        
        while True:
            try:
                if len(used_replies) >= len(ar2_replies):
                    used_replies = []
                
                available_replies = [r for r in ar2_replies if r not in used_replies]
                reply = random.choice(available_replies)
                used_replies.append(reply)
                
                await message.reply(reply)
                print(f"{Fore.GREEN}[SUCCESS] Replied to {user.name}")
                current_delay = base_delay
                break

            except discord.errors.HTTPException as e:
                if e.status == 429:
                    print(f"{Fore.YELLOW}[RATELIMIT] Waiting {current_delay:.2f} seconds...")
                    await asyncio.sleep(current_delay)
                    current_delay = min(current_delay + 0.5, max_delay)
                else:
                    print(f"{Fore.RED}[ERROR] HTTP Error: {e}, retrying...")
                    await asyncio.sleep(1)
            except Exception as e:
                print(f"{Fore.RED}[ERROR] Failed to send message: {e}")
                await asyncio.sleep(1)

    async def reply_loop():
        def check(m):
            return m.author == user and m.channel == ctx.channel

        while True:
            try:
                message = await bot.wait_for('message', check=check)
                asyncio.create_task(send_autoreply(message))
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"{Fore.RED}[ERROR] Reply loop error: {e}")
                await asyncio.sleep(1)
                continue

    task = asyncio.create_task(reply_loop())
    autoreply_tasks[ctx.author.id] = task
    await ctx.send(f"```Started auto-replying to {user.name}'s messages```")

@bot.command(name='armercy')
async def stop_autoreply(ctx):
    if ctx.author.id in autoreply_tasks:
        autoreply_tasks[ctx.author.id].cancel()
        del autoreply_tasks[ctx.author.id]
        await ctx.send("```Stopped auto-replying```")
    else:
        await ctx.send("```No auto-reply task running```")



jokestar = [
    "ill forever punch on you",
    "idk loser",
    "yo freak come meet your match and die",
    "wtf is a {user}"
    "wtf is a {user2}"
    "nigga is scared of his own voice",
    "this nigga got a openminded lisp",
    "yo bitch come lick my cum off your girl",
    "LOOOOOL COME GET YOUR HEAD CHOPPED OFF",
    "NIGGA YOU SUCK LETS BOX AGAIN",
    "yo your bf {user2} is dying LMAFOA",
    "nigga your shut out btw",
    "yo faggot idk you lets beef forever",
    "i dont gain rep from hoeing you {user}",
    "i dont gain rep from hoeing you {user2}",
    "you get killed in your own domain",
    "how you a nobody in your own domain",
    "i own this shitty com btw",
    "your clients suck LMFAO"
]

hoe_tasks = {}
running_hoe = {}

@bot.command()
async def hoe(ctx, user: discord.Member = None, name1: str = None, name2: str = None):
    if user is None or name1 is None:
        await ctx.send("```Usage: xhoe @user name1 name2```")
        return
        
    if ctx.author.id in hoe_tasks:
        await ctx.send("```ay you already hoeing LMFAOO```")
        return

    valid_tasks = []
    running_hoe[ctx.author.id] = True

    async def hoe_task(token):
        headers = {
            'Authorization': token.strip(),
            'Content-Type': 'application/json'
        }

        while running_hoe.get(ctx.author.id, False):
            try:
                available_messages = [msg for msg in jokestar if not ('{user2}' in msg and name2 is None)]
                    
                message = random.choice(available_messages)
                message = message.replace("{user}", name1)
                if name2:
                    message = message.replace("{user2}", name2)
                message = f"{message} {user.mention}"

                proxy = await get_working_proxy() if proxy_enabled else None
                
                async with await create_proxy_session() as session:
                    async with session.post(
                        f'https://discord.com/api/v9/channels/{ctx.channel.id}/messages',
                        headers=headers,
                        json={'content': message},
                        proxy=proxy,
                        ssl=False
                    ) as resp:
                        if resp.status == 429:
                            print(f"Token {token[-4:]} hit rate limit, stopping all tokens")
                            running_hoe[ctx.author.id] = False
                            return
                        elif resp.status in [401, 403]:
                            print(f"Token {token[-4:]} is invalid, skipping")
                            return
                        elif resp.status not in [200, 201, 204]:
                            print(f"Error status {resp.status} for token {token[-4:]}")
                            await asyncio.sleep(2)
                            continue
                            
                await asyncio.sleep(random.uniform(0.225, 0.555))

            except Exception as e:
                print(f"Error in hoe task: {str(e)}")
                if not running_hoe.get(ctx.author.id, False):
                    break
                await asyncio.sleep(1)
                continue

    for token in tokens:
        task = asyncio.create_task(hoe_task(token))
        valid_tasks.append(task)
    
    if valid_tasks:
        hoe_tasks[ctx.author.id] = valid_tasks
        await ctx.send(f"```Started hoeing {user.name} with {len(valid_tasks)} tokens```")
    else:
        await ctx.send("```No valid tokens found```")

@bot.command(name='hoemercy')
async def stop_hoe(ctx):
    if ctx.author.id in hoe_tasks:
        running_hoe[ctx.author.id] = False
        
        for task in hoe_tasks[ctx.author.id]:
            task.cancel()
        
        del hoe_tasks[ctx.author.id]
        if ctx.author.id in running_hoe:
            del running_hoe[ctx.author.id]
            
        await ctx.send("```Stopped hoeing```")
    else:
        await ctx.send("```No active hoe command```")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if ctx.command.name == "hoe":
            await ctx.send("```Usage: xhoe @user name1 name2```")
        if ctx.comamand.name =="hoe":
            await ctx.send("```Usage: xhoe <@user> name1 name2```")

@bot.command()
async def gcfill(ctx):
    tokens_file_path = 'token.txt'
    tokens = loads_tokens(tokens_file_path)

    if not tokens:
        await ctx.send("```No tokens found in the file. Please check the token file.```")
        return

    limited_tokens = tokens[:12]
    group_channel = ctx.channel

    async def add_token_to_gc(token):
        try:
            user_client = discord.Client(intents=intents)
            
            @user_client.event
            async def on_ready():
                try:
                    await group_channel.add_recipients(user_client.user)
                    print(f'Added {user_client.user} to the group chat')
                except Exception as e:
                    print(f"Error adding user with token {token[-4:]}: {e}")
                finally:
                    await user_client.close()

            await user_client.start(token, bot=False)
            
        except Exception as e:
            print(f"Failed to process token {token[-4:]}: {e}")

    tasks = [add_token_to_gc(token) for token in limited_tokens]
    await asyncio.gather(*tasks, return_exceptions=True)
    
    await ctx.send(f"```Attempted to add {len(limited_tokens)} tokens to the group chat```")

@bot.command()
async def gcleave(ctx):
    tokens_file_path = 'token.txt'
    tokens = loads_tokens(tokens_file_path)
    
    if not tokens:
        await ctx.send("```No tokens found in the file```")
        return
        
    channel_id = ctx.channel.id

    async def leave_gc(token):
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                url = f'https://discord.com/api/v9/channels/{channel_id}'
                async with session.delete(url, headers=headers) as response:
                    if response.status == 200:
                        print(f'Token {token[-4:]} left the group chat successfully')
                    elif response.status == 429:
                        retry_after = float((await response.json()).get('retry_after', 1))
                        print(f"Rate limited for token {token[-4:]}, waiting {retry_after}s")
                        await asyncio.sleep(retry_after)
                    else:
                        print(f"Error for token {token[-4:]}: Status {response.status}")
                        
            except Exception as e:
                print(f"Failed to process token {token[-4:]}: {e}")
            
            await asyncio.sleep(0.5) 

    tasks = [leave_gc(token) for token in tokens]
    await asyncio.gather(*tasks, return_exceptions=True)
    
    await ctx.send("```Attempted to make all tokens leave the group chat```")
@bot.command()
async def gcleaveall(ctx):
    tokens_file_path = 'token.txt'
    tokens = loads_tokens(tokens_file_path)
    
    if not tokens:
        await ctx.send("```No tokens found in the file```")
        return

    async def leave_all_gcs(token):
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        left_count = 0
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get('https://discord.com/api/v9/users/@me/channels', headers=headers) as resp:
                    if resp.status == 200:
                        channels = await resp.json()
                        group_channels = [channel for channel in channels if channel.get('type') == 3]
                        
                        for channel in group_channels:
                            try:
                                channel_id = channel['id']
                                async with session.delete(f'https://discord.com/api/v9/channels/{channel_id}', headers=headers) as leave_resp:
                                    if leave_resp.status == 200:
                                        left_count += 1
                                        print(f'Token {token[-4:]} left group chat {channel_id}')
                                    elif leave_resp.status == 429:
                                        retry_after = float((await leave_resp.json()).get('retry_after', 1))
                                        print(f"Rate limited for token {token[-4:]}, waiting {retry_after}s")
                                        await asyncio.sleep(retry_after)
                                    else:
                                        print(f"Error leaving GC {channel_id} for token {token[-4:]}: Status {leave_resp.status}")
                                
                                await asyncio.sleep(0.5)  
                                
                            except Exception as e:
                                print(f"Error processing channel for token {token[-4:]}: {e}")
                                continue
                                
                        return left_count
                    else:
                        print(f"Failed to get channels for token {token[-4:]}: Status {resp.status}")
                        return 0
                        
            except Exception as e:
                print(f"Failed to process token {token[-4:]}: {e}")
                return 0

    status_msg = await ctx.send("```Starting group chat leave operation...```")
    
    tasks = [leave_all_gcs(token) for token in tokens]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    total_left = sum(r for r in results if isinstance(r, int))
    
    await status_msg.edit(content=f"""```ansi
Group Chat Leave Operation Complete
Total tokens processed: {len(tokens)}
Total group chats left: {total_left}```""")


conversation_flow = [
    ("ay bru that nigga nreedo nipples fell off", "ong we not dissing nreedo", "and what if we was LMFAO", "yo ong we can beef bout it all day"),
    ("yo bitch", "yo shizco why you talking to yourself", "LMFAO", "zip your fucking lip??"),
    ("hello", "nigga said hello for no one to respomd ☠️", "HELZP ITS BEEN NOT EVEN A SECOND"),
    ("yall niggas hear massacre a pedo", "ong we all knew bout that", "i didnt wtf massacre is a pedo", "ong he is nigga got his own death bed LMFAO"),
    ("yo pedos your god is back", "LMFAO WHO CLAIJMED YOU AS A GOD", "ong your justa fucking dork", "retarded loser", "this nigga is my bitch who said hes a god"),
    ("wtf lets beef loser", "LMFAO\nYOUR\nTOO\nSLOW\nJR\nLETS\nBOX", "nigga your a robot chat packing", "degraded losers")
]

user_responses = [
    "i could fucking care less {user}",
    "LMFAO CLOCK IT- {user}",
    "and you just ruined the mood {user}",
    "might aswell zip that lip {user}",
    "omg cutie heuy {user}",
    "om,ggg hiiiiii {user}",
    "bitch bye {user}"
]

active_tasks = {}

@bot.command()
async def fakeactivity(ctx):
    if len(tokens) < 2:
        await ctx.send("```Need at least 2 tokens to create fake activity```")
        return

    active_tasks = {}
    conversation_groups = []
    used_tokens = set()

    available_tokens = tokens.copy()
    random.shuffle(available_tokens)
    
    while len(available_tokens) >= 2:
        group_size = min(random.randint(2, 4), len(available_tokens))
        group = []
        for _ in range(group_size):
            token = available_tokens.pop(0)
            group.append(token)
            used_tokens.add(token)
        conversation_groups.append(group)

    async def send_message(token, content, reply_to=None):
        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": token.strip(),
            "content-type": "application/json",
            "origin": "https://discord.com",
            "referer": "https://discord.com/channels/@me",
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIwLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIn0="
        }

        payload = {"content": content}
        if reply_to:
            payload["message_reference"] = {"message_id": reply_to.id}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f'https://discord.com/api/v9/channels/{ctx.channel.id}/messages',
                    headers=headers,
                    json=payload
                ) as resp:
                    if resp.status == 429:
                        retry_after = float((await resp.json()).get('retry_after', 5))
                        print(f"{Fore.YELLOW}[RATELIMIT] Token: {token[-4:]} | Waiting: {retry_after}s")
                        await asyncio.sleep(retry_after)
                        return False
                    elif resp.status == 403:
                        print(f"{Fore.RED}[INVALID] Token invalid: {token[-4:]}")
                        return None
                    elif resp.status == 200:
                        print(f"{Fore.GREEN}[SUCCESS] Message sent with token: {token[-4:]}")
                        return True
                    else:
                        print(f"{Fore.RED}[ERROR] Failed to send message with token: {token[-4:]} (Status: {resp.status})")
                        return False

            except Exception as e:
                print(f"{Fore.RED}[ERROR] Exception for token {token[-4:]}: {str(e)}")
                return False

    async def group_conversation(group_tokens):
        valid_tokens = group_tokens.copy()
        used_convos = []
        
        while True:
            try:
                valid_tokens = [t for t in valid_tokens if t]
                if len(valid_tokens) < 2:
                    print(f"{Fore.RED}[ERROR] Not enough valid tokens in group")
                    return

                if len(used_convos) == len(conversation_flow):
                    used_convos.clear()

                available_conversations = [i for i in range(len(conversation_flow)) if i not in used_convos]
                current_conv_index = random.choice(available_conversations)
                used_convos.append(current_conv_index)
                
                current_conversation = conversation_flow[current_conv_index]
                speakers = random.sample(valid_tokens, min(len(valid_tokens), 3))
                
                for i, message in enumerate(current_conversation):
                    current_speaker = speakers[i % len(speakers)]
                    
                    result = await send_message(current_speaker, message)
                    if result is None:
                        if current_speaker in valid_tokens:
                            valid_tokens.remove(current_speaker)
                        continue
                    elif result:
                        await asyncio.sleep(random.uniform(0.555, 0.888))
                
                if random.random() < 0.2:
                    def check(m):
                        return not m.author.bot and m.channel == ctx.channel
                    
                    try:
                        user_msg = await bot.wait_for('message', timeout=10.0, check=check)
                        if random.random() < 0.3:
                            response = random.choice(user_responses).format(user=user_msg.author.name)
                            random_token = random.choice(valid_tokens)
                            await send_message(random_token, response, reply_to=user_msg)
                    except asyncio.TimeoutError:
                        pass
                
                await asyncio.sleep(random.uniform(15, 30))
                
            except Exception as e:
                print(f"{Fore.RED}[ERROR] Conversation error: {str(e)}")
                await asyncio.sleep(5)

    status_msg = await ctx.send("```Starting fake activity...```")
    
    for group in conversation_groups:
        task = asyncio.create_task(group_conversation(group))
        active_tasks[group[0]] = task
        await asyncio.sleep(1)

    await status_msg.edit(content=f"""```ansi
{white}Fake Activity Started{reset}
{white}Active groupsP{reset}: {len(conversation_groups)}
{white}Tokens involved{reset}: {len(used_tokens)}
{white}Use 'xfakestop' to stop{reset}```""")

@bot.command()
async def fakestop(ctx):
    if active_tasks:
        for task in active_tasks.values():
            task.cancel()
        active_tasks.clear()
        await ctx.send("```Stopped all fake activity```")
    else:
        await ctx.send("```No fake activity running```")

killmsg = [
    "yo slut you suck",
    "LMFAO LETS BEEF ALL DAY",
    "YO JR PICK THEM GLOVES UP LETS GO AGAIN",
    "lets beef forever",
    "getting bullied to an outsider lead you to get hoed by me",
    "aint shit a dream loser",
    "YO PEDO WAKE UP IM RIGHT HERE",
    "ILL BASH YOUR SKULL IN AND RIP OFF YOUR SKIN",
    "ILL TAKE YOUR HEAD AS MY TROPHY LOL",
    "yo deformed toilet paper come whipe my ass",
    "zip\nthat\nfucking\lip\nfor\i\punch\nit\nin",
    "TIRED ALREADY LMFAO"
]

killmsg = [
    "yo slut you suck",
    "LMFAO LETS BEEF ALL DAY",
    "YO JR PICK THEM GLOVES UP LETS GO AGAIN",
    "lets beef forever",
    "getting bullied to an outsider lead you to get hoed by me",
    "aint shit a dream loser",
    "YO PEDO WAKE UP IM RIGHT HERE",
    "ILL BASH YOUR SKULL IN AND RIP OFF YOUR SKIN",
    "ILL TAKE YOUR HEAD AS MY TROPHY LOL",
    "yo deformed toilet paper come whipe my ass",
    "zip\nthat\nfucking\lip\nfor\i\punch\nit\nin",
    "TIRED ALREADY LMFAO"
]

kill_tasks = {}

@bot.command()
async def kill(ctx, user: discord.Member = None):
    if user is None:
        await ctx.send("```Usage: xkill @user```")
        return
        
    if ctx.author.id in kill_tasks:
        await ctx.send("```Already running a kill command```")
        return

    valid_tasks = []
    should_stop = asyncio.Event()

    async def kill_task(token):
        headers = {
                        'Authorization': token.strip(),
                        'Content-Type': 'application/json'
                    }

        while not should_stop.is_set():
            try:
                message = random.choice(killmsg)
                message = f"{message} {user.mention}"

                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        f'https://discord.com/api/v9/channels/{ctx.channel.id}/messages',
                        headers=headers,
                        json={'content': message}
                    ) as resp:
                        if resp.status == 429:
                            print(f"Token {token[-4:]} hit rate limit, stopping all tokens")
                            should_stop.set()
                            return
                        elif resp.status in [401, 403]:
                            print(f"Token {token[-4:]} is invalid, skipping")
                            return
                        elif resp.status != 200:
                            print(f"Error status {resp.status} for token {token[-4:]}")
                            await asyncio.sleep(2)
                            continue
                            
                    await asyncio.sleep(0.005)

            except Exception as e:
                print(f"Error in kill task: {str(e)}")
                await asyncio.sleep(2)
                continue

    for token in tokens:
        task = asyncio.create_task(kill_task(token))
        valid_tasks.append(task)
    
    if valid_tasks:
        kill_tasks[ctx.author.id] = valid_tasks
        await ctx.send(f"```Started killing {user.name} with {len(valid_tasks)} tokens```")
    else:
        await ctx.send("```No valid tokens found```")

@bot.command(name='killstop')
async def stop_kill(ctx):
    if ctx.author.id in kill_tasks:
        for task in kill_tasks[ctx.author.id]:
            task.cancel()
        del kill_tasks[ctx.author.id]
        await ctx.send("```Stopped killing```")
    else:
        await ctx.send("```No active kill command```")

autoclear_task = None

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def update_config(autoclear_enabled):
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    config['autoclear'] = autoclear_enabled
    
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

async def autoclear_loop():
    while True:
        try:
            await asyncio.sleep(120)
            clear_terminal()
            print(f"{Fore.LIGHTMAGENTA_EX}Terminal cleared at {datetime.now().strftime('%H:%M:%S')}")
        except asyncio.CancelledError:
            break

@bot.command()
async def autoclear(ctx):
    global autoclear_task
    
    if autoclear_task and not autoclear_task.cancelled():
        autoclear_task.cancel()
        autoclear_task = None
        update_config(False)
        await ctx.send("```Autoclear disabled```")
    else:
        autoclear_task = asyncio.create_task(autoclear_loop())
        update_config(True)
        await ctx.send("```Autoclear enabled - Terminal will clear every 2 minutes```")


multilastwl = [
    "# > YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF YO BITCH YOU FUCKING SUCK NEVER PRESS AGAIN ON THAT SHITTY SELFBOT ILL SNAP IT IN HALF "
]

multi_tasks = {}
shared_counter = 0

@bot.command()
async def multilast(ctx, user: discord.Member = None):
    if user is None:
        await ctx.send("```Usage: xmultilast @user```")
        return
        
    if ctx.author.id in multi_tasks:
        await ctx.send("```Already running a multilast command```")
        return

    valid_tasks = []
    global shared_counter
    shared_counter = 0

    async def multi_task(token):
        global shared_counter
        headers = {
            "authorization": token.strip(),
            "content-type": "application/json"
        }

        while True:
            try:
                message = f"{random.choice(multilastwl)} {user.mention}\n```{shared_counter + 1}```"

                async with await create_proxy_session() as session:
                    async with session.post(
                        f'https://discord.com/api/v9/channels/{ctx.channel.id}/messages',
                        headers=headers,
                        json={'content': message}
                    ) as resp:
                        if resp.status in [401, 403]:
                            print(f"Token {token[-4:]} is invalid, removing from rotation")
                            return
                        elif resp.status == 200:
                            shared_counter += 1
                            print(f"Token {token[-4:]} sent message #{shared_counter}")
                        else:
                            print(f"Error status {resp.status} for token {token[-4:]}")
                            await asyncio.sleep(1)
                            continue
                            
                await asyncio.sleep(0.005)

            except Exception as e:
                print(f"Error in multi task: {str(e)}")
                await asyncio.sleep(1)
                continue

    for token in tokens:
        task = asyncio.create_task(multi_task(token))
        valid_tasks.append(task)
    
    if valid_tasks:
        multi_tasks[ctx.author.id] = valid_tasks
        await ctx.send(f"```Started multilast on {user.name} with {len(valid_tasks)} tokens```")
    else:
        await ctx.send("```No valid tokens found```")

@bot.command(name='multiend')
async def stop_multi(ctx):
    if ctx.author.id in multi_tasks:
        for task in multi_tasks[ctx.author.id]:
            task.cancel()
        del multi_tasks[ctx.author.id]
        await ctx.send("```Stopped multilast```")
    else:
        await ctx.send("```No active multilast command```")

proxy_enabled = False
proxies = []
proxy_cycle = None

def load_proxies():
    global proxies, proxy_cycle
    try:
        with open('proxies.txt', 'r') as f:
            proxies = [line.strip() for line in f if line.strip()]
        proxy_cycle = cycle(proxies)
        return True
    except Exception as e:
        print(f"Error loading proxies: {e}")
        return False

def get_next_proxy():
    if not proxy_cycle:
        return None
    proxy = next(proxy_cycle)
    return f"http://{proxy}"

def update_proxy_config(enabled: bool):
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        config['proxysupport'] = enabled
        
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(f"Error updating config: {e}")

async def test_proxy(session, proxy):
    try:
        async with session.get('https://discord.com', proxy=proxy, timeout=5) as resp:
            return resp.status == 200
    except:
        return False

def format_proxy(proxy):
    if not proxy.startswith(('http://', 'https://')):
        return f"http://{proxy}"
    return proxy

async def create_proxy_session():
    if proxy_enabled:
        connector = aiohttp.TCPConnector(ssl=False, force_close=True)
        return aiohttp.ClientSession(
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=30)
        )
    return aiohttp.ClientSession()

async def get_working_proxy():
    if not proxy_enabled:
        return None
        
    for _ in range(3):
        proxy = get_next_proxy()
        if proxy:
            proxy = format_proxy(proxy)
            async with aiohttp.ClientSession() as session:
                if await test_proxy(session, proxy):
                    return proxy
    return None

@bot.command()
async def proxys(ctx):
    global proxy_enabled
    
    if proxy_enabled:
        proxy_enabled = False
        update_proxy_config(False)
        await ctx.send("```Proxy support disabled```")
    else:
        if load_proxies():
            proxy_enabled = True
            update_proxy_config(True)
            await ctx.send(f"```Proxy support enabled with {len(proxies)} proxies```")
        else:
            await ctx.send("```Failed to load proxies```")

fhoelist = [
    "{mention}\n# you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name} you fucking suck {name}",
    "{mention}\n# your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch your my bitch",
    "{mention}\n# {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser {name} your a loser",
    "{mention}\n# {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you {name} i dont rate you"
]

fhoe_tasks = {}
running_fhoe = {}

@bot.command()
async def fhoe(ctx, user: discord.Member = None, name: str = None):
    if user is None or name is None:
        await ctx.send("```Usage: xfhoe @user name```")
        return
        
    if ctx.author.id in fhoe_tasks:
        await ctx.send("```your already hoeing LMFAO```")
        return

    valid_tasks = []
    running_fhoe[ctx.author.id] = True

    async def fhoe_task(token):
        headers = {
            'Authorization': token.strip(),
            'Content-Type': 'application/json'
        }

        while running_fhoe.get(ctx.author.id, False): 
            try:
                message = random.choice(fhoelist)
                message = message.replace("{mention}", user.mention)
                message = message.replace("{name}", name)

                proxy = await get_working_proxy() if proxy_enabled else None
                
                async with await create_proxy_session() as session:
                    async with session.post(
                        f'https://discord.com/api/v9/channels/{ctx.channel.id}/messages',
                        headers=headers,
                        json={'content': message},
                        proxy=proxy,
                        ssl=False
                    ) as resp:
                        if resp.status == 429:
                            retry_after = random.uniform(3, 5)
                            print(f"Rate limit hit for token {token[-4:]}, waiting {retry_after}s")
                            await asyncio.sleep(retry_after)
                            continue
                        elif resp.status in [401, 403]:
                            print(f"Token {token[-4:]} is invalid, skipping")
                            return
                        elif resp.status not in [200, 201, 204]:
                            print(f"Error status {resp.status} for token {token[-4:]}")
                            await asyncio.sleep(2)
                            continue
                            
                await asyncio.sleep(random.uniform(0.255, 0.555))

            except Exception as e:
                print(f"Error in fhoe task: {str(e)}")
                if not running_fhoe.get(ctx.author.id, False):
                    break
                await asyncio.sleep(1)
                continue

    for token in tokens:
        task = asyncio.create_task(fhoe_task(token))
        valid_tasks.append(task)
    
    if valid_tasks:
        fhoe_tasks[ctx.author.id] = valid_tasks
        await ctx.send(f"```Started fhoeing {user.name} with {len(valid_tasks)} tokens```")
    else:
        await ctx.send("```No valid tokens found```")

@bot.command(name='fhoemercy')
async def stop_fhoe(ctx):
    if ctx.author.id in fhoe_tasks:
        running_fhoe[ctx.author.id] = False
        
        for task in fhoe_tasks[ctx.author.id]:
            task.cancel()
        
        del fhoe_tasks[ctx.author.id]
        if ctx.author.id in running_fhoe:
            del running_fhoe[ctx.author.id]
            
        await ctx.send("```Stopped fhoeing```")
    else:
        await ctx.send("```No active fhoe command```")

@bot.command()
async def mdm(ctx, num_friends: int = None):
    if num_friends is None:
        await ctx.send("```Usage: xmdm <number>```")
        return
       
    try:
        import massdm
        
        await massdm.mdm(ctx, bot, num_friends)
        
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")
        return

trap_tasks = {}

@bot.command()
async def autotrap(ctx, user: discord.Member = None):
    if user is None:
        await ctx.send("```Usage: xautotrap @user```")
        return
        
    if ctx.author.id in trap_tasks:
        trap_tasks[ctx.author.id] = False
        await ctx.send("```Stopped auto-trapping```")
        return

    async def trap_task():
        headers = {
            "authority": "discord.com",
            "method": "PUT",
            "scheme": "https",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US",
            "authorization": config['token'],
            "origin": "https://discord.com",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9020 Chrome/108.0.5359.215 Electron/22.3.26 Safari/537.36",
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US"
        }

        trap_tasks[ctx.author.id] = True
        
        while trap_tasks.get(ctx.author.id, False):
            try:
                proxy = await get_working_proxy() if proxy_enabled else None
                
                async with await create_proxy_session() as session:
                    async with session.put(
                        f'https://discord.com/api/v9/channels/{ctx.channel.id}/recipients/{user.id}',
                        headers=headers,
                        proxy=proxy,
                        ssl=False
                    ) as resp:
                        if resp.status == 429:
                            retry_after = random.uniform(1.0, 3.0)
                            await asyncio.sleep(retry_after)
                            continue
                        elif resp.status == 403:
                            await ctx.send("```❌ Cannot add user (missing permissions)```")
                            trap_tasks[ctx.author.id] = False
                            return
                            
                await asyncio.sleep(random.uniform(0.1, 0.3))

            except Exception as e:
                print(f"Error in trap task: {str(e)}")
                if not trap_tasks.get(ctx.author.id, False):
                    break
                await asyncio.sleep(1)
                continue

    task = asyncio.create_task(trap_task())
    await ctx.send(f"```Started auto-trapping {user.name}```")

@bot.command(name='trapmercy')
async def stop_trap(ctx):
    if ctx.author.id in trap_tasks:
        trap_tasks[ctx.author.id] = False
        await ctx.send("```Stopped auto-trapping```")
    else:
        await ctx.send("```No active trap command```")

antitrap_task = None

@bot.command()
async def antitrap(ctx):
    """Toggle antitrap protection"""
    try:
        # Load current config
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        # Toggle antitrap setting
        config['antitrap'] = not config.get('antitrap', False)
        
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
            
        status = "enabled" if config['antitrap'] else "disabled"
        await ctx.send(f"```✅ Anti-trap {status}```")
            
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

@bot.command()
async def antitrapb(ctx):
    """Toggle block on add feature for antitrap"""
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        # Toggle blockonadd setting
        config['blockonadd'] = not config.get('blockonadd', False)
        
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
            
        status = "enabled" if config['blockonadd'] else "disabled"
        await ctx.send(f"```✅ Block on add {status}```")
            
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")
@bot.command()
async def antitrapwl(ctx, *, args=None):
    """Manage antitrap whitelist"""
    if not args:
        await ctx.send("```Usage:\nAdd: xantitrapwl id1,id2,id3\nRemove: xantitrapwl remove id\nView: xantitrapwl view```")
        return

    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        if config['atwhitelist'] is None:
            config['atwhitelist'] = []
        
        if args.lower() == 'view':
            if not config['atwhitelist']:
                await ctx.send("```Whitelist is empty```")
                return
            whitelist_str = '\n'.join(str(id) for id in config['atwhitelist'])
            await ctx.send(f"```Whitelisted IDs:\n{whitelist_str}```")
            return
            
        if args.lower().startswith('remove '):
            try:
                id_to_remove = int(args.split('remove ')[1])
                if id_to_remove in config['atwhitelist']:
                    config['atwhitelist'].remove(id_to_remove)
                    with open('config.json', 'w') as f:
                        json.dump(config, f, indent=4)
                    await ctx.send(f"```✅ Removed {id_to_remove} from whitelist```")
                else:
                    await ctx.send("```❌ ID not found in whitelist```")
            except ValueError:
                await ctx.send("```❌ Invalid ID format```")
            return
            
        try:
            new_ids = [int(id.strip()) for id in args.split(',')]
            added = []
            already_exists = []
            
            for id in new_ids:
                if id not in config['atwhitelist']:
                    config['atwhitelist'].append(id)
                    added.append(str(id))
                else:
                    already_exists.append(str(id))
                    
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=4)
                
            response = []
            if added:
                response.append(f"✅ Added to whitelist: {', '.join(added)}")
            if already_exists:
                response.append(f"ℹ️ Already in whitelist: {', '.join(already_exists)}")
                
            await ctx.send(f"```{''.join(response)}```")
            
        except ValueError:
            await ctx.send("```❌ Invalid ID format. Use numbers only, separated by commas```")
            
    except Exception as e:
        await ctx.send(f"```❌ Error: {str(e)}```")

@bot.command()
async def autofill(ctx):
    """Toggle autofill for group chats"""
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)

        config['autofill'] = not config.get('autofill', False)
        
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
            
        status = "enabled" if config['autofill'] else "disabled"
        await ctx.send(f"```✅ Autofill {status}```")
            
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")
        
ring_tasks = {}

@bot.command()
async def gcring(ctx, delay: float = None):
    """Ring spam a group chat"""
    if not isinstance(ctx.channel, discord.GroupChannel):
        await ctx.send("```❌ This command can only be used in group chats```")
        return
        
    if delay is None:
        await ctx.send("```Usage: xgcring <delay in seconds>```")
        return
        
    if delay < 0.5:
        await ctx.send("```❌ Delay must be at least 0.5 seconds```")
        return
        
    if ctx.author.id in ring_tasks:
        ring_tasks[ctx.author.id] = False
        await ctx.send("```✅ Stopped ring spam```")
        return

    headers = {
        "authority": "discord.com",
        "method": "PATCH",
        "scheme": "https",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US",
        "authorization": config['token'],
        "content-type": "application/json",
        "origin": "https://discord.com",
        "referer": f"https://discord.com/channels/@me/{ctx.channel.id}",
        "sec-ch-ua": '"Not/A)Brand";v="99", "Brave";v="115", "Chromium";v="115"',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9020 Chrome/108.0.5359.215 Electron/22.3.26 Safari/537.36",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "X-Debug-Options": "bugReporterEnabled",
        "X-Discord-Locale": "en-US",
        "X-Discord-Timezone": "Asia/Calcutta",
        "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDIwIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0IiwiYXBwX2FyY2giOiJpYTMyIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIGRpc2NvcmQvMS4wLjkwMjAgQ2hyb21lLzEwOC4wLjUzNTkuMjE1IEVsZWN0cm9uLzIyLjMuMjYgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjIyLjMuMjYiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyNDAyMzcsIm5hdGl2ZV9idWlsZF9udW1iZXIiOjM4NTE3LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsLCJkZXNpZ25faWQiOjB9"
    }

    async def ring_spam():
        ring_tasks[ctx.author.id] = True
        
        while ring_tasks.get(ctx.author.id, False):
            try:
                # Join call
                async with aiohttp.ClientSession() as session:
                    async with session.patch(
                        f'https://discord.com/api/v9/channels/{ctx.channel.id}/call',
                        headers=headers,
                        json={
                            "channel_id": str(ctx.channel.id),
                            "self_deaf": False,
                            "self_mute": False,
                            "self_video": False
                        }
                    ) as resp:
                        if resp.status in [200, 204]:
                            print(f"{Fore.GREEN}[RING] Joined call")
                        elif resp.status == 429:
                            retry_after = float((await resp.json()).get('retry_after', 1))
                            print(f"{Fore.YELLOW}[RING] Rate limited, waiting {retry_after}s...")
                            await asyncio.sleep(retry_after)
                            continue
                        else:
                            print(f"{Fore.RED}[RING] Failed to join: Status {resp.status}")
                            text = await resp.text()
                            print(f"{Fore.RED}[RING] Error details: {text}")
                            continue

                await asyncio.sleep(delay)
                
                async with aiohttp.ClientSession() as session:
                    async with session.patch(
                        f'https://discord.com/api/v9/channels/{ctx.channel.id}/call',
                        headers=headers,
                        json={
                            "channel_id": None
                        }
                    ) as resp:
                        if resp.status not in [200, 204, 429]:
                            print(f"{Fore.RED}[RING] Failed to leave: Status {resp.status}")
                            text = await resp.text()
                            print(f"{Fore.RED}[RING] Error details: {text}")
                
                await asyncio.sleep(0.5)
                
            except Exception as e:
                print(f"{Fore.RED}[RING] Error: {str(e)}")
                if not ring_tasks.get(ctx.author.id, False):
                    break
                await asyncio.sleep(1)

    task = asyncio.create_task(ring_spam())
    await ctx.send(f"```Started ring spam with {delay}s delay```")

@bot.command(name='ringend')
async def stop_ring(ctx):
    """Stop ring spam"""
    if ctx.author.id in ring_tasks:
        ring_tasks[ctx.author.id] = False
        await ctx.send("```Stopped ring spam```")
    else:
        await ctx.send("```No active ring spam```")

black = "\033[30m"
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
magenta = "\033[35m"
cyan = "\033[36m"
white = "\033[37m"
reset = "\033[0m"  
pink = "\033[38;2;255;192;203m"
white = "\033[37m"
blue = "\033[34m"
black = "\033[30m"
light_green = "\033[92m" 
light_yellow = "\033[93m" 
light_magenta = "\033[95m" 
light_cyan = "\033[96m"  
light_red = "\033[91m"  
light_blue = "\033[94m"  
@bot.command(name='sendmenu')
async def sendsmenu(ctx):
    await ctx.send(f"""```ansi
                                    {white}LAPPY'S BIRTH MENU {black}[ {magenta}>.< {black}]
                                    {blue}+ - + - + - + - + - + - + - + - +
                                    {black}[ {magenta}>.< {black}] {light_blue}[ {white}PAYMENTS {light_blue}] {light_cyan}- {white}Nitro/Deco/Ltc/Btc
                                    {blue}+ - + - + - + - + - + - + - + - +
                                    {black}[ {magenta}>.< {black}] {light_blue}[ {white}PRODUCTS {light_blue}] {light_cyan}- {white}Custom Selfbots.
                                    {black}[{magenta}>.<{black}] {red}- {white}Custom Bots.
                                    {black}[{magenta}>.<{black}] {red}- {white}Birth SB Hosting.
                                    {black}[{magenta}>.<{black}] {red}- {white}Phantom Sb.
                                    {black}[{magenta}>.<{black}] {red}- {white}Birth Token Gen.
                                    {black}[{magenta}>.<{black}] {red}- {white}Anti Nuke Bots.
                                    {blue}+ - + - + - + - + - + - + - + - +
                                    {black}[ {magenta}>.< {black}] {light_blue}[ {white}SUPPORT {light_blue}] {light_cyan}- {white}Support
                                    {black}[{magenta}>.<{black}] {red} - {white}/wdfw or /roster or dm @mwpv
                                    {blue}+ - + - + - + - + - + - + - + - +
                                    {black}Prices varies depending on your payment method.
                                    {blue}+ - + - + - + - + - + - + - + - +
```""")
token = config['token']
bot.run(token, bot=False)