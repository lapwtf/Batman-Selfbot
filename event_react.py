import discord
from discord.ext import commands
import json
import aiohttp
import requests
import asyncio

def load_config(file_path='config.json'):
    with open(file_path, 'r') as f:
        return json.load(f)

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
light_green = "\033[92m"
light_yellow = "\033[93m"
light_magenta = "\033[95m"
light_cyan = "\033[96m"
light_red = "\033[91m"
light_blue = "\033[94m"

keyword_enabled = False
keyword_responses = {}
react_keyword_enabled = False
react_keyword_responses = {}
ignored_users = set()
headers = None
last_message_id = None

eonmessage_data = {}
ronping_data = {}
sonping_data = {}
message_monitors = {}
last_message_ids = {}

def load_keyword_config():
    global keyword_enabled, keyword_responses, ignored_users
    try:
        with open("keyword_config.json", "r") as f:
            config = json.load(f)
            keyword_enabled = config.get('keyword_enabled', False)
            keyword_responses = config.get('keyword_responses', {})
            ignored_users = set(config.get('ignored_users', []))
    except FileNotFoundError:
        keyword_enabled = False
        keyword_responses = {}
        ignored_users = set()

def save_keyword_config():
    config = {
        'keyword_enabled': keyword_enabled,
        'keyword_responses': keyword_responses,
        'ignored_users': list(ignored_users)
    }
    with open('keyword_config.json', 'w') as f:
        json.dump(config, f, indent=4)

def save_react_keyword_config():
    config = {
        'react_keyword_enabled': react_keyword_enabled,
        'react_keyword_responses': react_keyword_responses
    }
    with open('react_keyword_config.json', 'w') as f:
        json.dump(config, f, indent=4)

def load_data():
    global eonmessage_data, ronping_data, sonping_data
    try:
        with open("eonmessage_data.json", "r") as f:
            eonmessage_data.update(json.load(f))
    except FileNotFoundError:
        eonmessage_data.clear()
    
    try:
        with open("ronping_data.json", "r") as f:
            ronping_data.update(json.load(f))
    except FileNotFoundError:
        ronping_data.clear()
    
    try:
        with open("sonping_data.json", "r") as f:
            sonping_data.update(json.load(f))
    except FileNotFoundError:
        sonping_data.clear()

def save_data():
    with open("eonmessage_data.json", "w") as f:
        json.dump(eonmessage_data, f, indent=4)
    with open("ronping_data.json", "w") as f:
        json.dump(ronping_data, f, indent=4)
    with open("sonping_data.json", "w") as f:
        json.dump(sonping_data, f, indent=4)

class EventReactCog(commands.Cog, name="EventReact"):
    def __init__(self, bot):
        self.bot = bot
        load_keyword_config()
        load_data()  
        self.update_headers()

    def update_headers(self):
        global headers
        headers = {
            "authorization": self.bot.http.token,
            "content-type": "application/json"
        }

    @commands.command()
    async def keywordr(self, ctx, action=None, *, content=None):
        global keyword_enabled, keyword_responses, headers
        
        if not action:
            await ctx.send("```Usage: keywordr <on/off/add/remove/list/clear/ignore/unignore> [word, response]```")
            return

        if action.lower() == "on":
            keyword_enabled = True
            self.update_headers()
            if not hasattr(self.bot, 'keyword_task'):
                self.bot.keyword_task = self.bot.loop.create_task(self.monitor_messages(ctx))
            await ctx.send("```Keyword response enabled```")
            save_keyword_config()
            return

        elif action.lower() == "off":
            keyword_enabled = False
            if hasattr(self.bot, 'keyword_task'):
                self.bot.keyword_task.cancel()
                delattr(self.bot, 'keyword_task')
            await ctx.send("```Keyword response disabled```")
            save_keyword_config()
            return

        elif action.lower() == "add":
            if not content or "," not in content:
                await ctx.send("```Please use format: keywordr add <word>, <response>```")
                return
            
            word, response = content.split(",", 1)
            word = word.strip().lower()
            response = response.strip()
            
            keyword_responses[word] = response
            await ctx.send(f"```Added keyword: '{word}' with response: '{response}'```")
            save_keyword_config()

        elif action.lower() == "remove":
            if not content:
                await ctx.send("```Please specify a word to remove```")
                return
            word = content.strip().lower()
            if word in keyword_responses:
                del keyword_responses[word]
                await ctx.send(f"```Removed '{word}' from keyword responses```")
                save_keyword_config()
            else:
                await ctx.send("```Word not found in keyword responses```")

        elif action.lower() == "list":
            if not keyword_responses:
                await ctx.send("```No keywords set```")
                return
            keywords_list = "\n".join(f"- {word}: {response}" for word, response in keyword_responses.items())
            await ctx.send(f"```Current keywords and responses:\n{keywords_list}```")

        elif action.lower() == "clear":
            keyword_responses.clear()
            await ctx.send("```Cleared all keyword responses```")
            save_keyword_config()

        elif action.lower() == "ignore":
            if not content:
                await ctx.send("```Please specify a user ID to ignore```")
                return
            user_id = content.strip()
            ignored_users.add(user_id)
            await ctx.send(f"```Added user ID {user_id} to ignore list```")
            save_keyword_config()

        elif action.lower() == "unignore":
            if not content:
                await ctx.send("```Please specify a user ID to unignore```")
                return
            user_id = content.strip()
            if user_id in ignored_users:
                ignored_users.remove(user_id)
                await ctx.send(f"```Removed user ID {user_id} from ignore list```")
            else:
                await ctx.send("```User ID not found in ignore list```")
            save_keyword_config()

        else:
            await ctx.send("```Invalid action. Use on/off/add/remove/list/clear/ignore/unignore```")

    async def monitor_messages(self, ctx):
        global last_message_id, keyword_enabled
        
        retry_count = 0
        max_retries = 3
        backoff_time = 5
        
        while keyword_enabled:
            try:
                params = {'after': last_message_id} if last_message_id else {'limit': 1}
                response = requests.get(
                    f"https://discord.com/api/v9/channels/{ctx.channel.id}/messages",
                    headers=headers,
                    params=params,
                    timeout=10
                )
                
                if response.status_code == 429:
                    retry_after = float(response.headers.get('Retry-After', 5))
                    print(f"Rate limited, waiting {retry_after} seconds")
                    await asyncio.sleep(retry_after)
                    continue
                    
                elif response.status_code == 401:
                    print("Token appears to be invalid, updating headers")
                    self.update_headers()
                    retry_count += 1
                    await asyncio.sleep(backoff_time)
                    continue
                    
                elif response.status_code != 200:
                    print(f"Error: API returned status code {response.status_code}")
                    retry_count += 1
                    if retry_count >= max_retries:
                        print("Too many failed attempts, disabling keyword monitoring")
                        keyword_enabled = False
                        await ctx.send("```⚠️ monitoring disabled due to unexpected errors. >.<```")
                        return
                    await asyncio.sleep(backoff_time)
                    backoff_time *= 2
                    continue
                
                retry_count = 0
                backoff_time = 5
                
                messages = response.json()
                for msg in reversed(messages):
                    if msg['author']['id'] != str(self.bot.user.id) and msg['author']['id'] not in ignored_users:
                        content = msg.get('content', '').lower()
                        
                        for keyword, response_text in keyword_responses.items():
                            if keyword in content:
                                try:
                                    payload = {
                                        "content": response_text,
                                        "tts": False,
                                        "message_reference": {
                                            "message_id": msg['id'],
                                            "channel_id": ctx.channel.id,
                                            "guild_id": ctx.guild.id if ctx.guild else None
                                        }
                                    }
                                    
                                    reply_response = requests.post(
                                        f"https://discord.com/api/v9/channels/{ctx.channel.id}/messages",
                                        headers=headers,
                                        json=payload,
                                        timeout=10
                                    )
                                    
                                    if reply_response.status_code == 429:
                                        retry_after = float(reply_response.headers.get('Retry-After', 5))
                                        await asyncio.sleep(retry_after)
                                    
                                except Exception as e:
                                    print(f"Error sending response: {e}")
                                
                                await asyncio.sleep(0.5)
                                break
                        
                        last_message_id = msg['id']
                
            except requests.exceptions.RequestException as e:
                print(f"Network error: {e}")
                await asyncio.sleep(backoff_time)
                backoff_time *= 2
            except Exception as e:
                print(f"Unexpected error in keyword monitoring: {e}")
                retry_count += 1
                if retry_count >= max_retries:
                    print("Too many errors, disabling keyword monitoring")
                    keyword_enabled = False
                    await ctx.send("```⚠️ monitoring disabled due to unexpected errors. >.<```")
                    return
                await asyncio.sleep(backoff_time)
                backoff_time *= 2
            
            await asyncio.sleep(1)

    @commands.command()
    async def reactkw(self, ctx, action=None, *, content=None):
        global react_keyword_enabled, react_keyword_responses, headers
        
        if not headers:
            headers = {
                "authorization": self.bot.http.token,
                "content-type": "application/json"
            }

        if not action:
            await ctx.send("```Usage: reactkw <on/off/add/remove/list/clear> [word, emoji]```")
            return

        if action.lower() == "on":
            react_keyword_enabled = True
            if not hasattr(self.bot, 'react_keyword_task'):
                self.bot.react_keyword_task = self.bot.loop.create_task(self.monitor_react_messages(ctx))
            await ctx.send("```Keyword reaction enabled```")
            save_react_keyword_config()
            return

        elif action.lower() == "off":
            react_keyword_enabled = False
            if hasattr(self.bot, 'react_keyword_task'):
                self.bot.react_keyword_task.cancel()
                delattr(self.bot, 'react_keyword_task')
            await ctx.send("```Keyword reaction disabled```")
            save_react_keyword_config()
            return

        elif action.lower() == "add":
            if not content or "," not in content:
                await ctx.send("```Please use format: reactkw add <word>, <emoji>```")
                return
            
            word, emoji = content.split(",", 1)
            word = word.strip().lower()
            emoji = emoji.strip()
            
            if emoji.startswith('<') and emoji.endswith('>'):
                emoji_parts = emoji[1:-1].split(':')
                if len(emoji_parts) == 3:
                    emoji = f"{emoji_parts[0]}:{emoji_parts[2]}"
                elif len(emoji_parts) == 2:
                    emoji = emoji_parts[1]
            
            react_keyword_responses[word] = emoji
            await ctx.send(f"```Added keyword: '{word}' with reaction: {emoji}```")
            save_react_keyword_config()

        elif action.lower() == "remove":
            if not content:
                await ctx.send("```Please specify a word to remove```")
                return
            word = content.strip().lower()
            if word in react_keyword_responses:
                del react_keyword_responses[word]
                await ctx.send(f"```Removed '{word}' from keyword reactions```")
                save_react_keyword_config()
            else:
                await ctx.send("```Word not found in keyword reactions```")

        elif action.lower() == "list":
            if not react_keyword_responses:
                await ctx.send("```No keywords set```")
                return
            keywords_list = "\n".join(f"- {word}: {emoji}" for word, emoji in react_keyword_responses.items())
            await ctx.send(f"```Current keywords and reactions:\n{keywords_list}```")

        elif action.lower() == "clear":
            react_keyword_responses.clear()
            await ctx.send("```Cleared all keyword reactions```")
            save_react_keyword_config()

        else:
            await ctx.send("```Invalid action. Use on/off/add/remove/list/clear```")

    async def monitor_react_messages(self, ctx):
        global last_message_id
        
        while react_keyword_enabled:
            try:
                params = {'after': last_message_id} if last_message_id else {'limit': 1}
                response = requests.get(
                    f"https://discord.com/api/v9/channels/{ctx.channel.id}/messages",
                    headers=headers,
                    params=params
                )
                
                if response.status_code == 200:
                    messages = response.json()
                    
                    for msg in reversed(messages):
                        if msg['author']['id'] != str(self.bot.user.id):
                            content = msg.get('content', '').lower()
                            message_id = msg['id']
                            
                            if message_id != last_message_id:
                                last_message_id = message_id
                                
                                for keyword, emoji in react_keyword_responses.items():
                                    if keyword.lower() in content:
                                        try:
                                            encoded_emoji = requests.utils.quote(emoji)
                                            
                                            channel_id = ctx.channel.id
                                            reaction_url = f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{encoded_emoji}/@me"
                                            
                                            response = requests.put(
                                                reaction_url,
                                                headers=headers
                                            )
                                            
                                            if response.status_code not in [200, 204]:
                                                print(f"Failed to add reaction: {response.status_code}")
                                                print(f"Reaction URL: {reaction_url}")
                                                
                                        except Exception as e:
                                            print(f"Error adding reaction: {e}")
                                        
                                        await asyncio.sleep(0.5)
                            
            except Exception as e:
                print(f"Keyword Reaction Error: {e}")
                
            await asyncio.sleep(1)

    @commands.command(name="monitoruser")
    async def monitor_user(self, ctx, user: discord.User):
        user_id = str(user.id)
        channel_id = str(ctx.channel.id)
        
        if user_id in message_monitors and message_monitors[user_id]:
            await ctx.send(f"```Already monitoring {user.name}```")
            return
            
        message_monitors[user_id] = True
        await ctx.send(f"```Started monitoring {user.name}```")
        
        self.bot.loop.create_task(self.monitor_user_messages(ctx, user_id, channel_id))

    @commands.command(name="unmonitor")
    async def unmonitor_user(self, ctx, user: discord.User):
        user_id = str(user.id)
        
        if user_id in message_monitors:
            message_monitors[user_id] = False
            if user_id in last_message_ids:
                del last_message_ids[user_id]
            await ctx.send(f"```Stopped monitoring {user.name}```")
        else:
            await ctx.send(f"```Not monitoring {user.name}```")

    async def monitor_user_messages(self, ctx, user_id, channel_id):
        global last_message_ids
        
        while user_id in message_monitors and message_monitors[user_id]:
            try:
                params = {'after': last_message_ids.get(user_id)} if last_message_ids.get(user_id) else {'limit': 1}
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"https://discord.com/api/v9/channels/{channel_id}/messages",
                        headers=self.headers,
                        params=params
                    ) as response:
                        
                        if response.status == 200:
                            messages = await response.json()
                            
                            for msg in reversed(messages):
                                if msg['author']['id'] == str(user_id):
                                    content = msg.get('content', '').lower()
                                    message_id = msg['id']
                                    
                                    if message_id != last_message_ids.get(user_id):
                                        last_message_ids[user_id] = message_id
                                        
                                        if content in react_keyword_responses:
                                            reaction = react_keyword_responses[content]
                                            try:
                                                encoded_emoji = requests.utils.quote(reaction)
                                                reaction_url = f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{encoded_emoji}/@me"
                                                
                                                async with session.put(reaction_url, headers=self.headers) as reaction_resp:
                                                    if reaction_resp.status not in [200, 204]:
                                                        print(f"Failed to add reaction: {reaction_resp.status}")
                                                        
                                            except Exception as e:
                                                print(f"Error adding reaction: {e}")
                                            
                                            await asyncio.sleep(0.5)
                                        
                                        if content in keyword_responses:
                                            response = keyword_responses[content]
                                            channel = self.bot.get_channel(int(channel_id))
                                            if channel:
                                                await channel.send(response)
                                        
                                        if content in eonmessage_data and eonmessage_data[content].get('enabled', True):
                                            edited_message = eonmessage_data[content]['edited_message']
                                            edit_url = f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}"
                                            async with session.patch(edit_url, headers=self.headers, json={'content': edited_message}) as edit_resp:
                                                if edit_resp.status not in [200, 204]:
                                                    print(f"Failed to edit message: {edit_resp.status}")
                
            except Exception as e:
                print(f"Message Monitor Error: {e}")
                
            await asyncio.sleep(1)

    @commands.group(name="eonmessage", invoke_without_command=True)
    async def eonmessage(self, ctx):
        await ctx.send(f"""```ansi\n
[ {blue}eonmessage{reset} ] automatic message editing.
    {red}Usage:{reset}
    {green}[ {blue}^{green} ] {black}eonmessage add <message> <edited_message>{reset} - {black}Edit a specific message to a new message.{reset}
    {green}[ {blue}^{green} ] {black}eonmessage list{reset} - {black}List all messages with their edited versions.{reset}
    {green}[ {blue}^{green} ] {black}eonmessage remove <message>{reset} - {black}Remove the edited message from a specific message.{reset}
    {green}[ {blue}^{green} ] {black}eonmessage clear{reset} - {black}Clear all message-to-edited bindings.{reset}
    {green}[ {blue}^{green} ] {black}eonmessage on <message>{reset} - {black}Enable auto-edit for a specific message.{reset}
    {green}[ {blue}^{green} ] {black}eonmessage off <message>{reset} - {black}Disable auto-edit for a specific message.{reset}```""")

    @eonmessage.command(name="add")
    async def eonmessage_add(self, ctx, message: str, *, edited_message: str):
        if message in eonmessage_data:
            await ctx.send(f"```'{message}' already has an edited message set.```")
        else:
            eonmessage_data[message] = {'edited_message': edited_message, 'enabled': True}
            save_data()
            await ctx.send(f"```Added edited message: {edited_message} to the message {message}.```")

    @eonmessage.command(name="list")
    async def eonmessage_list(self, ctx):
        if not eonmessage_data:
            await ctx.send("```No eonmessage bindings found.```")
            return
        response = "```Current eonmessage:\n```"
        for message, data in eonmessage_data.items():
            status = "Enabled" if data['enabled'] else "Disabled"
            response += f"```ansi\n{blue}Message: {white}{message}\n{blue}Edited Message: {white}{data.get('edited_message', 'None')}\n{blue}Status: {white}{status}\n```"
        await ctx.send(response)

    @eonmessage.command(name="remove")
    async def eonmessage_remove(self, ctx, message: str):
        if message in eonmessage_data:
            del eonmessage_data[message]
            save_data()
            await ctx.send(f"```Removed the edited message for the message: {message}.```")
        else:
            await ctx.send(f"```No edited message found for the message: {message}.```")

    @eonmessage.command(name="clear")
    async def eonmessage_clear(self, ctx):
        eonmessage_data.clear()
        save_data()
        await ctx.send("```Cleared all eonmessage bindings.```")

    @eonmessage.command(name="on")
    async def eonmessage_on(self, ctx):
        if eonmessage_data:
            for message in eonmessage_data:
                eonmessage_data[message]['enabled'] = True
            save_data()
            await ctx.send("```Enabled all eonmessage edits.```")
        else:
            await ctx.send("```No eonmessage bindings found to enable.```")

    @eonmessage.command(name="off")
    async def eonmessage_off(self, ctx):
        if eonmessage_data:
            for message in eonmessage_data:
                eonmessage_data[message]['enabled'] = False
            save_data()
            await ctx.send("```Disabled all eonmessage edits.```")
        else:
            await ctx.send("```No eonmessage bindings found to disable.```")

    @commands.group(name="ronping", invoke_without_command=True)
    async def ronping(self, ctx):
        await ctx.send(f"""```ansi\n
[ {blue}ronping{reset} ] automatic reaction when pinged.
    {red}Usage:{reset}
        {green}[ {blue}^{green} ] {black}ronping set <emoji>{reset} - {black}Set the reaction for when you get pinged.{reset}
        {green}[ {blue}^{green} ] {black}ronping show{reset} - {black}Show current ping reaction.{reset}
        {green}[ {blue}^{green} ] {black}ronping remove{reset} - {black}Remove the ping reaction.{reset}
        {green}[ {blue}^{green} ] {black}ronping on{reset} - {black}Enable ping reactions.{reset}
        {green}[ {blue}^{green} ] {black}ronping off{reset} - {black}Disable ping reactions.{reset}```""")

    @ronping.command(name="set")
    async def ronping_set(self, ctx, emoji: str):
        ronping_data['emoji'] = emoji
        ronping_data['enabled'] = True
        save_data()
        await ctx.send(f"```Set reaction {emoji} for pings.```")

    @ronping.command(name="show")
    async def ronping_show(self, ctx):
        if not ronping_data or 'emoji' not in ronping_data:
            await ctx.send("```No ping reaction set.```")
            return
        status = "Enabled" if ronping_data.get('enabled', False) else "Disabled"
        await ctx.send(f"```Current ping reaction: {ronping_data['emoji']}\nStatus: {status}```")

    @ronping.command(name="remove")
    async def ronping_remove(self, ctx):
        ronping_data.clear()
        save_data()
        await ctx.send("```Removed ping reaction.```")

    @ronping.command(name="on")
    async def ronping_on(self, ctx):
        if 'emoji' in ronping_data:
            ronping_data['enabled'] = True
            save_data()
            await ctx.send("```Enabled ping reactions.```")
        else:
            await ctx.send("```No ping reaction set. Use 'ronping set <emoji>' first.```")

    @ronping.command(name="off")
    async def ronping_off(self, ctx):
        if 'emoji' in ronping_data:
            ronping_data['enabled'] = False
            save_data()
            await ctx.send("```Disabled ping reactions.```")
        else:
            await ctx.send("```No ping reaction set.```")

    @commands.group(name="sonping", invoke_without_command=True)
    async def sonping(self, ctx):
        await ctx.send(f"""```ansi\n
[ {blue}sonping{reset} ] automatic response when pinged.
    {red}Usage:{reset}
        {green}[ {blue}^{green} ] {black}sonping set <response>{reset} - {black}Set the response for when you get pinged.{reset}
        {green}[ {blue}^{green} ] {black}sonping show{reset} - {black}Show current ping response.{reset}
        {green}[ {blue}^{green} ] {black}sonping remove{reset} - {black}Remove the ping response.{reset}
        {green}[ {blue}^{green} ] {black}sonping on{reset} - {black}Enable ping responses.{reset}
        {green}[ {blue}^{green} ] {black}sonping off{reset} - {black}Disable ping responses.{reset}```""")

    @sonping.command(name="set")
    async def sonping_set(self, ctx, *, response: str):
        sonping_data['response'] = response
        sonping_data['enabled'] = True
        save_data()
        await ctx.send(f"```Set response '{response}' for pings.```")

    @sonping.command(name="show")
    async def sonping_show(self, ctx):
        if not sonping_data or 'response' not in sonping_data:
            await ctx.send("```No ping response set.```")
            return
        status = "Enabled" if sonping_data.get('enabled', False) else "Disabled"
        await ctx.send(f"```Current ping response: {sonping_data['response']}\nStatus: {status}```")

    @sonping.command(name="remove")
    async def sonping_remove(self, ctx):
        sonping_data.clear()
        save_data()
        await ctx.send("```Removed ping response.```")

    @sonping.command(name="on")
    async def sonping_on(self, ctx):
        if 'response' in sonping_data:
            sonping_data['enabled'] = True
            save_data()
            await ctx.send("```Enabled ping responses.```")
        else:
            await ctx.send("```No ping response set. Use 'sonping set <response>' first.```")

    @sonping.command(name="off")
    async def sonping_off(self, ctx):
        if 'response' in sonping_data:
            sonping_data['enabled'] = False
            save_data()
            await ctx.send("```Disabled ping responses.```")
        else:
            await ctx.send("```No ping response set.```")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content in react_keyword_responses:
            reaction = react_keyword_responses[message.content]
            await message.add_reaction(reaction)

        if message.content in keyword_responses:
            response = keyword_responses[message.content]
            await message.channel.send(response)

        if message.content in eonmessage_data:
            if eonmessage_data[message.content].get('enabled', True):
                try:
                    edited_message = eonmessage_data[message.content]['edited_message']
                    await message.edit(content=edited_message)
                except Exception as e:
                    print(f"Error editing message: {e}")

        if ronping_data and ronping_data.get('enabled', False) and 'emoji' in ronping_data:
            if self.bot.user and self.bot.user.mentioned_in(message):
                await message.add_reaction(ronping_data['emoji'])

        if sonping_data and sonping_data.get('enabled', False) and 'response' in sonping_data:
            if self.bot.user and self.bot.user.mentioned_in(message):
                await message.channel.send(sonping_data['response'])

def setup(bot):
    load_keyword_config()  
    bot.add_cog(EventReactCog(bot))