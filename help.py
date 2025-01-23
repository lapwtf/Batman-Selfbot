import discord
from discord.ext import commands
import asyncio
import json
import random

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
light_blue = "\033[94m"  

batman_quotes = [
    "I am vengeance. I am the night.",
    "It's not who I am underneath, but what I do that defines me.",
    "Why do we fall? So we can learn to pick ourselves up.",
    "Sometimes the truth isn't good enough.",
    "The night is darkest just before the dawn.",
    "You either die a hero or live long enough to see yourself become the villain.",
    "I have one power. I never give up.",
    "Everything's impossible until somebody does it.",
    "A hero can be anyone.",
    "Fear is a tool. They think I'm hiding in the shadows.",
    "I am the shadows.",
    "Criminals are like weeds, Alfred. Pull one up, another grows in its place.",
    "It's what I do that defines me.",
    "Sometimes people deserve to have their faith rewarded."
]

batmans = f"""
{black}
                                        ⠀⠀⠀⠀⠀⠀⠀⡆⠀⠀⠀⠀⠀⠀⠀⢂⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                        ⠀⠀⠀⠀⠀⠀⢰⡇⠀⠀⠀⠀⠀⠀⠀⣸⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                        ⠀⠀⠀⠀⠀⠀⣼⣷⠀⣀⣀⣀⡄⠀⣀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀
                                        ⠀⠀⠀⠀⠀⠀⣿⣿⣿⡿⢋⠁⠀⠀⠀⠈⠑⡄⠀⠀⠀⠀⠀⠀⠀
                                        ⠀⠀⠀⠀⠀⢠⣿⣿⣿⣷⡿⠂⠄⢀⠀⠀⢠⠽⡄⠀⠀⠀⠀⠀⠀
                                        ⠀⠀⠀⠀⠀⢸⣿⣿⣿⡏⠠⣴⢦⣤⣬⣧⡭⣶⡇⠀⠀⠀⠀⠀⠀
                                        ⠀⠀⠀⠀⠀⢸⣿⣿⣿⣄⠀⠈⠉⠕⠉⢿⣿⣽⣱⠀⠀⠀⠀⠀⠀
                                        ⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⡆⠐⠒⠂⠖⠉⢉⣍⣥⠀⠀⠀⠀⠀⠀
                                        ⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⡈⠆⠀⠰⣖⠈⠔⠲⢱⠀⠀⠀⠀⠀⠀
                                        ⠀⠀⠀⠀⠀⣼⣿⣿⣿⡻⣷⣄⡀⠁⠀⠀⠀⣀⡼⠀⠀⠀⠀⠀⠀
                                        ⠀⠀⣀⣤⣾⣿⣿⣿⣿⣿⣷⣄⠙⢻⣿⠿⣿⣿⠉⠀⠀⠀⠀⠀⠀⠀
                                        ⢤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠙⠀⣿⠇⠀⣀⣀⠀⠀⠀⠀⠀
                                        ⠀⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠳⣄⢠⣿⣶⣷⣗⡫⠿⠇⢀⠀⠀
                                        ⠀⠀⠈⢫⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠘⠋⠁⠀⣿⣿⣿⣿⣶⣦⡁⠀
                                        ⠀⠀⠀⠀⠙⢛⣻⢿⣿⣿⣷⠶⢶⣦⣀⡰⠾⣿⣿⣿⣿⣿⡿⡿⠂
                                        ⠀⠀⠀⠙⠛⠒⠶⢭⣟⢋⢔⣿⣿⣰⣼⣸⣿⣪⣿⣿⣿⣿⡿⠞⠁⠀
                                        ⠀⠀⠀⠀⠀⠀⠀⠀⠙⣾⡼⣟⠙⠹⠿⠙⣻⣿⡿⠋⠋⠀⠀⠀⠀
                                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⣑⣁⡒⢒⠒⠚⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

def load_config(file_path='config.json'):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        default_config = {"password": "1234"}
        with open(file_path, 'w') as f:
            json.dump(default_config, f, indent=4)
        return default_config

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = load_config()
        self.help_session_active = False
        self.help_timeout_task = None
        self.settings = self.load_settings()
        self.favorites_data = self.load_favorites()
        self.commands_data = self.load_commands()
        
        self.header_msg = None
        self.content_msg = None
        self.footer_msg = None
        
    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            default_settings = {
                "password": "1234",
                "prefix": "$",
                "help_timeout": 80,
                "delete_timeout": 5,
                "theme": {
                    "primary_color": "black",
                    "secondary_color": "white",
                    "accent_color": "red"
                }
            }
            with open('settings.json', 'w') as f:
                json.dump(default_settings, f, indent=4)
            return default_settings
            
    def load_favorites(self):
        try:
            with open('favorites.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            default_favorites = {
                "favorites": [],
                "pinned_commands": [],
                "command_notes": {},
                "custom_aliases": {},
                "command_stats": {},
                "favorite_categories": [],
                "category_pins": {}
            }
            with open('favorites.json', 'w') as f:
                json.dump(default_favorites, f, indent=4)
            return default_favorites
            
    def load_commands(self):
        try:
            with open('commands.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
            
    def save_settings(self):
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f, indent=4)
            
    def save_favorites(self):
        with open('favorites.json', 'w') as f:
            json.dump(self.favorites_data, f, indent=4)
            
    async def reload_data(self):
        self.settings = self.load_settings()
        self.favorites_data = self.load_favorites()
        self.commands_data = self.load_commands()
        
    async def check_password(self, ctx):
        if not self.settings['password']:
            await ctx.send("Please enter the security key using `$verify <key>`")
            return False
        return True

    async def get_command_help(self, command: str):
        command = command.lower()
        for category in self.commands_data.values():
            if command in category:
                return f"```{command}: {category[command]}```"
        return "```Command help not available```"

    @commands.command(name="menu")
    async def menu(self, ctx):
        if not await self.check_password(ctx):
            return
            
        try:
            await self.header_msg.edit(content=self.original_header)
            await self.content_msg.edit(content=self.original_content)
            await self.footer_msg.edit(content=self.original_footer)
        except (discord.NotFound, AttributeError):
            self.header_msg = await ctx.send(self.original_header)
            self.content_msg = await ctx.send(self.original_content)
            self.footer_msg = await ctx.send(self.original_footer)
            
        self.help_session_active = True
        await self.reset_timeout()

    async def show_help(self, ctx, user: discord.User = None):
        if not await self.check_password(ctx):
            return
            
        if self.help_timeout_task:
            self.help_timeout_task.cancel()
        
        self.help_session_active = True
        user = ctx.author

        menu_items = [f"{black}[{white}1{black}] {white}Favorites"]
        
        remaining_items = [
            "Chatpacking",
            "Token Utility",
            "User Utility", 
            "Pc Utility",
            "Nuker",
            "Etc",
            "Event Reactions",
            "Profile",
            "Anti Gc",
            "Message Events",
            "Favorites Help",
            "Anti Token",
            "Token Controller",
            "OwO Hunt",
            "Nuke",
            "Protection",
            "Voice"
        ]
        
        favorite_items = []
        normal_items = []
        
        for item in remaining_items:
            if item.lower() in [cat.lower() for cat in self.favorites_data["favorite_categories"]]:
                favorite_items.append(item)
            else:
                normal_items.append(item)
                
        start_num = 2
        for item in favorite_items:
            menu_items.append(f"{black}[{white}{start_num}{black}] {white}★ {item}")
            start_num += 1
            
        for item in normal_items:
            menu_items.append(f"{black}[{white}{start_num}{black}] {white}{item}")
            start_num += 1
        
        self.original_header = f"```ansi\n🦇      {black}Batman       🦇               {black}[ {red}$close - Close Menu {black}]               {black}[ {red}$reset - Reset Menu {black}]```"
        self.original_content = f"""```ansi
{chr(10).join(menu_items)}

{black}[{white}Choose{black}] {white}$1 - {start_num-1}

{black}Welcome {red}{user.display_name}```"""
        self.original_footer = f"```ansi\n                                        ⠀⠀⠀⠀⠀{black}i am vengeance.```"
        
        startup_header = f"```ansi\n{white}🦇       Welcome to {black}Batman{white}       🦇               {black}[ {white}Press {red}$menu{white} to continue {black}]```"
        startup_content = f"```ansi\n{batmans}```"
        startup_footer = f"```ansi\n                                        ⠀⠀⠀⠀⠀BATMAN x SOCIAL x LAPPY```"
        
        self.header_msg = await ctx.send(startup_header)
        self.content_msg = await ctx.send(startup_content)
        self.footer_msg = await ctx.send(startup_footer)
        
        self.help_timeout_task = asyncio.create_task(self.help_timeout())

    async def help_timeout(self):
        await asyncio.sleep(self.settings['help_timeout'])
        self.help_session_active = False

    async def reset_timeout(self):
        if self.help_timeout_task:
            self.help_timeout_task.cancel()
        self.help_timeout_task = asyncio.create_task(self.help_timeout())

    async def end_help(self, ctx):
        if not await self.check_password(ctx):
            return
            
        if self.help_timeout_task:
            self.help_timeout_task.cancel()
        self.help_session_active = False
        await ctx.send("```Help session terminated```")

    async def chatpacking(self, ctx, user: discord.User = None):
        await self.safe_delete(ctx)
        if not self.help_session_active:
            return
            
        pinned_commands = self.favorites_data.get("category_pins", {}).get("chatpacking", [])
        pinned_content = ""
        if pinned_commands:
            pinned_content = f"{black}Pinned Commands:\n" + "\n".join(f"{black}[{white}★{black}] {white}{cmd}" for cmd in pinned_commands) + "\n\n"
            
        commands = [
            "gcfill", "gcleave", "autofill (wip)", "autofillend", "death", "deathend", 
            "untouchable", "untouchableend", "gcss", "gcssend", "kill", "ar", "arend", 
            "ar2", "ar2end", "outlast", "outlaststop", "ugc", "ugcend", "testimony", "testimonyoff"
        ]
        
        numbered_commands = [cmd for cmd in commands if cmd not in pinned_commands]
        
        numbered_content = "\n".join(f"{black}[{white}{i+1}{black}] {white}{cmd}" for i, cmd in enumerate(numbered_commands))
            
        await self.header_msg.edit(content=f"```ansi\n{black}[ {red}$close - Close Menu {black}]               🦇      {black}CHATPACKING      🦇               [ {red}$reset - Reset Menu {black}]```")
        await self.content_msg.edit(content=f"""```ansi
{pinned_content}{numbered_content}```""")
        await self.footer_msg.edit(content=f"```ansi\n                                        ⠀⠀⠀⠀⠀{black}i am the night.```")

    async def token_utility(self, ctx, user: discord.User = None):
        await self.safe_delete(ctx)
        if not self.help_session_active:
            return
            
        pinned_commands = self.favorites_data.get("category_pins", {}).get("token utility", [])
        pinned_content = ""
        if pinned_commands:
            pinned_content = f"{black}Pinned Commands:\n" + "\n".join(f"{black}[{white}★{black}] {white}{cmd}" for cmd in pinned_commands) + "\n\n"
            
        commands = [
            "tnickanme", "tpronouns", "tbio", "tpfp", "tstatus", "tstatusoff", 
            "tinfo", "tok", "richtok", "tjoin", "tleave", "rpcall", "mreact", 
            "maltreact", "mreactend", "maltreactend"
        ]
        
        numbered_commands = [cmd for cmd in commands if cmd not in pinned_commands]
        
        numbered_content = "\n".join(f"{black}[{white}{i+1}{black}] {white}{cmd}" for i, cmd in enumerate(numbered_commands))
            
        await self.header_msg.edit(content=f"```ansi\n{black}[ {red}$close - Close Menu {black}]               🦇      {black}TOKEN UTILITY      🦇               [ {red}$reset - Reset Menu {black}]```")
        await self.content_msg.edit(content=f"""```ansi
{pinned_content}{numbered_content}```""")
        await self.footer_msg.edit(content=f"```ansi\n                                        ⠀⠀⠀⠀⠀ {black}i am.. BATMAN```")

    async def user_utility(self, ctx, user: discord.User = None):
        await self.safe_delete(ctx)
        if not self.help_session_active:
            return
            
        pinned_commands = self.favorites_data.get("category_pins", {}).get("user utility", [])
        pinned_content = ""
        if pinned_commands:
            pinned_content = f"{black}Pinned Commands:\n" + "\n".join(f"{black}[{white}★{black}] {white}{cmd}" for cmd in pinned_commands) + "\n\n"
            
        commands = [
            "autoreact", "autoreactend", "altreact", "altreactend", "nickloop", 
            "stopnickloop", "autobump", "autobumpoff", "block", "unblock", 
            "onstartrpc", "rpc"
        ]
        
        numbered_commands = [cmd for cmd in commands if cmd not in pinned_commands]
        
        numbered_content = "\n".join(f"{black}[{white}{i+1}{black}] {white}{cmd}" for i, cmd in enumerate(numbered_commands))
            
        await self.header_msg.edit(content=f"```ansi\n{black}[ {red}$close - Close Menu {black}]               🦇      {black}USER UTILITY      🦇               [ {red}$reset - Reset Menu {black}]```")
        await self.content_msg.edit(content=f"""```ansi
{pinned_content}{numbered_content}```""")
        await self.footer_msg.edit(content=f"```ansi\n                                        ⠀⠀⠀⠀⠀ {black}I'm not a hero, I'm a symbol.```")

    async def pc_utility(self, ctx, user: discord.User = None):
        await self.safe_delete(ctx)
        if not self.help_session_active:
            return
            
        pinned_commands = self.favorites_data.get("category_pins", {}).get("pc utility", [])
        pinned_content = ""
        if pinned_commands:
            pinned_content = f"{black}Pinned Commands:\n" + "\n".join(f"{black}[{white}★{black}] {white}{cmd}" for cmd in pinned_commands) + "\n\n"
            
        commands = [
            "ss", "sspaste", "cleartemp", "clearbin", "recordtime", "record", 
            "recordpaste", "vmr", "voicetime", "voicemessage", "audior", 
            "audiotime", "audiopaste"
        ]
        
        numbered_commands = [cmd for cmd in commands if cmd not in pinned_commands]
        
        numbered_content = "\n".join(f"{black}[{white}{i+1}{black}] {white}{cmd}" for i, cmd in enumerate(numbered_commands))
            
        await self.header_msg.edit(content=f"```ansi\n{black}[ {red}$close - Close Menu {black}]               🦇      {black}PC UTILITY      🦇               [ {red}$reset - Reset Menu {black}]```")
        await self.content_msg.edit(content=f"""```ansi
{pinned_content}{numbered_content}```""")
        await self.footer_msg.edit(content=f"```ansi\n                                        ⠀⠀⠀⠀⠀ {black}The night is mine.```")

    async def nuker(self, ctx, user: discord.User = None):
        await self.safe_delete(ctx)
        if not self.help_session_active:
            return
            
        pinned_commands = self.favorites_data.get("category_pins", {}).get("nuker", [])
        pinned_content = ""
        if pinned_commands:
            pinned_content = f"{black}Pinned Commands:\n" + "\n".join(f"{black}[{white}★{black}] {white}{cmd}" for cmd in pinned_commands) + "\n\n"
            
        commands = ["massrole", "massroledel", "masschannel"]
        
        numbered_commands = [cmd for cmd in commands if cmd not in pinned_commands]
        
        numbered_content = "\n".join(f"{black}[{white}{i+1}{black}] {white}{cmd}" for i, cmd in enumerate(numbered_commands))
            
        await self.header_msg.edit(content=f"```ansi\n{black}[ {red}$close - Close Menu {black}]               🦇      {black}KNIGHTFALL      🦇               [ {red}$reset - Reset Menu {black}]```")
        await self.content_msg.edit(content=f"""```ansi
{pinned_content}{numbered_content}```""")
        await self.footer_msg.edit(content=f"```ansi\n                                        ⠀⠀⠀⠀⠀ {black}I will not fail you.```")

    async def etc(self, ctx, user: discord.User = None):
        await self.safe_delete(ctx)
        if not self.help_session_active:
            return
            
        pinned_commands = self.favorites_data.get("category_pins", {}).get("etc", [])
        pinned_content = ""
        if pinned_commands:
            pinned_content = f"{black}Pinned Commands:\n" + "\n".join(f"{black}[{white}★{black}] {white}{cmd}" for cmd in pinned_commands) + "\n\n"
            
        commands = [
            "cls", "swat", "rape", "host", "hostlaunch", "hosttoksclear", "hosttok"
        ]
        
        numbered_commands = [cmd for cmd in commands if cmd not in pinned_commands]
        
        numbered_content = "\n".join(f"{black}[{white}{i+1}{black}] {white}{cmd}" for i, cmd in enumerate(numbered_commands))
            
        await self.header_msg.edit(content=f"```ansi\n{black}[ {red}$close - Close Menu {black}]               🦇      {black}ETC      🦇               [ {red}$reset - Reset Menu {black}]```")
        await self.content_msg.edit(content=f"""```ansi
{pinned_content}{numbered_content}```""")
        await self.footer_msg.edit(content=f"```ansi\n                                        ⠀⠀⠀⠀⠀ {black}I am the shadow.```")

    async def event_reactions(self, ctx, user: discord.User = None):
        await self.safe_delete(ctx)
        if not self.help_session_active:
            return
            
        pinned_commands = self.favorites_data.get("category_pins", {}).get("event reactions", [])
        pinned_content = ""
        if pinned_commands:
            pinned_content = f"{black}Pinned Commands:\n" + "\n".join(f"{black}[{white}★{black}] {white}{cmd}" for cmd in pinned_commands) + "\n\n"
            

        commands = ["eonmessage", "ronping", "sonping", "keywordr", "reactkw"]
        
        numbered_commands = [cmd for cmd in commands if cmd not in pinned_commands]
        
        numbered_content = "\n".join(f"{black}[{white}{i+1}{black}] {white}{cmd}" for i, cmd in enumerate(numbered_commands))
            
        await self.header_msg.edit(content=f"```ansi\n{black}[ {red}$close - Close Menu {black}]               🦇      {black}EVENT REACTIONS      🦇               [ {red}$reset - Reset Menu {black}]```")
        await self.content_msg.edit(content=f"""```ansi
{pinned_content}{numbered_content}```""")
        await self.footer_msg.edit(content=f"```ansi\n                                        ⠀⠀⠀⠀⠀ {black}Vengeance has purpose.```")

    async def profile_menu(self, ctx):
        await self.safe_delete(ctx)
        user = ctx.author
        
        pinned_commands = self.favorites_data.get("category_pins", {}).get("profile", [])
        pinned_content = ""
        if pinned_commands:
            pinned_content = f"{black}Pinned Commands:\n" + "\n".join(f"{black}[{white}★{black}] {white}{cmd}" for cmd in pinned_commands) + "\n\n"
            
        commands = [
            "setpfp", "setbanner", "setbio", "setpronoun", "setname", 
            "stealbio", "stealpronoun", "stealpfp", "stealbanner"
        ]
        
        numbered_commands = [cmd for cmd in commands if cmd not in pinned_commands]
        numbered_content = "\n".join(f"{black}[{white}{i+1}{black}] {white}{cmd}" for i, cmd in enumerate(numbered_commands))
            
        await self.header_msg.edit(content=f"```ansi\n{black}[ {red}$close - Close Menu {black}]               🦇      {black}PROFILE CUSTOMIZATION      🦇               [ {red}$reset - Reset Menu {black}]```")
        await self.content_msg.edit(content=f"""```ansi
{pinned_content}{numbered_content}```""")
        await self.footer_msg.edit(content=f"```ansi\n                                        ⠀⠀⠀⠀⠀ {black}I protect the innocent.```")

    async def groupchat_menu(self, ctx):
        await self.safe_delete(ctx)
        user = ctx.author
        
        pinned_commands = self.favorites_data.get("category_pins", {}).get("groupchat", [])
        pinned_content = ""
        if pinned_commands:
            pinned_content = f"{black}Pinned Commands:\n" + "\n".join(f"{black}[{white}★{black}] {white}{cmd}" for cmd in pinned_commands) + "\n\n"
            
        commands = [
            "mimic", "antigcspam", "antigcspam whitelist", "antigcspam blacklist",
            "antigcspam silent", "antigcspam message", "antigcspam autoremove",
            "antigcspam webhook", "antigcspam autoblock", "antigcspam list",
            "autogc", "autogc stop", "autogc whitelist", "autogc whitelistr",
            "autogc list", "autogcleave", "autogcleave stop", "autogcleave status"
        ]
        
        numbered_commands = [cmd for cmd in commands if cmd not in pinned_commands]
        
        numbered_content = "\n".join(f"{black}[{white}{i+1}{black}] {white}{cmd}" for i, cmd in enumerate(numbered_commands))
            
        await self.header_msg.edit(content=f"```ansi\n[ {red}$close - Close Menu {black}]               🦇      {black}GROUPCHAT      🦇               [ {red}$reset - Reset Menu {black}]```")
        await self.content_msg.edit(content=f"""```ansi
{pinned_content}{numbered_content}```""")
        await self.footer_msg.edit(content=f"```ansi\n                                        ⠀⠀⠀⠀⠀ {black}I make my own rules.```")

    async def auto_messenger_menu(self, ctx):
        await self.safe_delete(ctx)
        user = ctx.author
        
        pinned_commands = self.favorites_data.get("category_pins", {}).get("auto messenger", [])
        pinned_content = ""
        if pinned_commands:
            pinned_content = f"{black}Pinned Commands:\n" + "\n".join(f"{black}[{white}★{black}] {white}{cmd}" for cmd in pinned_commands) + "\n\n"
            
        commands = [
            "msgtime help", "msgtime <minutes> <message(s)> on", "msgtime off",
            "msgtime status", "msgtime list", "msgtime clear", "msgtime remove",
            "purgekw <keyword>", "purgekwdm <keyword>", "purgekwserver <keyword>", "afk"
        ]
        
        numbered_commands = [cmd for cmd in commands if cmd not in pinned_commands]
        
        numbered_content = "\n".join(f"{black}[{white}{i+1}{black}] {white}{cmd}" for i, cmd in enumerate(numbered_commands))
            
        await self.header_msg.edit(content=f"```ansi\n[ {red}$close - Close Menu {black}]               🦇      {black}AUTO MESSENGER      🦇               [ {red}$reset - Reset Menu {black}]```")
        await self.content_msg.edit(content=f"""```ansi
{pinned_content}{numbered_content}```""")
        await self.footer_msg.edit(content=f"```ansi\n                                        ⠀⠀⠀⠀⠀ {black}Fear is a tool.```")

    async def show_favorites_help(self, ctx):
        if not self.help_session_active:
            return
            
        try:
            await self.header_msg.edit(content=f"```ansi\n{black}[ {red}$close - Close Menu {black}]               🦇      {black}FAVORITES HELP      🦇               [ {red}$reset - Reset Menu {black}]```")
            await self.content_msg.edit(content=f"""```ansi
{black}[{white}1{black}] {white}$fav             
{black}[{white}2{black}] {white}$fav add          
{black}[{white}3{black}] {white}$fav remove       
{black}[{white}4{black}] {white}$fav pin          
{black}[{white}5{black}] {white}$fav unpin      
{black}[{white}6{black}] {white}$fav alias        
{black}[{white}7{black}] {white}$fav unalias      
{black}[{white}8{black}] {white}$fav category     
{black}[{white}9{black}] {white}$fav uncategory  
{black}[{white}10{black}] {white}$fav stats        

{black}[{white}Features{black}]
{white}Pin important commands to top 
{white}Add custom notes to remember command usage
{white}Create aliases for quick access
{white}Track command usage statistics
{white}Organize favorites into categories
{white}View all favorites with $fav```""")
            await self.footer_msg.edit(content=f"```ansi\n                                        ⠀⠀⠀⠀⠀ {black}Knowledge is power.```")
        except (discord.NotFound, AttributeError):
            await self.menu(ctx)
            await self.show_favorites_help(ctx)

    async def show_favorites_menu(self, ctx):
        if not self.help_session_active:
            return
            
        try:
            content = []
            
            for category in self.favorites_data.get("favorite_categories", []):
                content.append(f"{black}[{white}{category.title()}{black}] {white}★ Favorite Category")
                
            await self.header_msg.edit(content=f"```ansi\n🦇      {black}Favorites       🦇               {black}[ {red}$menu - Return to Menu {black}]```")
            await self.content_msg.edit(content=f"""```ansi
{chr(10).join(content) if content else f"{black}No favorite categories yet. Add some with $fav category <category>"}```""")
            await self.footer_msg.edit(content=f"```ansi\n                                        ⠀⠀⠀⠀⠀ {black}My favorites never fail.```")
        except (discord.NotFound, AttributeError):
            await self.menu(ctx)
            await self.show_favorites_menu(ctx)

    async def add_favorite(self, ctx, command: str, note: str = None):
        command = command.lower()
        if command not in self.favorites_data["favorites"]:
            self.favorites_data["favorites"].append(command)
            if note:
                self.favorites_data["command_notes"][command] = note
            if command not in self.favorites_data["command_stats"]:
                self.favorites_data["command_stats"][command] = {"times_used": 0, "added_date": str(ctx.message.created_at)}
            self.save_favorites()
            await ctx.send(f"```Added {command} to favorites```")
        else:
            await ctx.send(f"```{command} is already in favorites```")

    async def remove_favorite(self, ctx, command: str):
        command = command.lower()
        if command in self.favorites_data["favorites"]:
            self.favorites_data["favorites"].remove(command)
            if command in self.favorites_data["command_notes"]:
                del self.favorites_data["command_notes"][command]
            self.save_favorites()
            await ctx.send(f"```Removed {command} from favorites```")
        else:
            await ctx.send(f"```{command} is not in favorites```")

    async def pin_command(self, ctx, command: str):
        if command not in self.favorites_data.get("favorites", []):
            await ctx.send("Command must be in favorites before it can be pinned.")
            return
            
        if "pinned_commands" not in self.favorites_data:
            self.favorites_data["pinned_commands"] = []
            
        if command in self.favorites_data["pinned_commands"]:
            self.favorites_data["pinned_commands"].remove(command)
            await ctx.send(f"Unpinned {command}")
        else:
            self.favorites_data["pinned_commands"].append(command)
            await ctx.send(f"Pinned {command}")
            
        self.save_favorites()
        await self.reset_timeout()

    async def add_alias(self, ctx, command: str, alias: str):
        command = command.lower()
        alias = alias.lower()
        if command in self.favorites_data["favorites"]:
            self.favorites_data["custom_aliases"][alias] = command
            self.save_favorites()
            await ctx.send(f"```Added alias {alias} for {command}```")

    async def remove_alias(self, ctx, alias: str):
        alias = alias.lower()
        if alias in self.favorites_data["custom_aliases"]:
            del self.favorites_data["custom_aliases"][alias]
            self.save_favorites()
            await ctx.send(f"```Removed alias {alias}```")

    async def add_category(self, ctx, category: str):
        if category not in self.favorites_data["favorite_categories"]:
            self.favorites_data["favorite_categories"].append(category)
            self.save_favorites()
            await ctx.send(f"```Added {category} to favorite categories```")

    async def remove_category(self, ctx, category: str):
        if category in self.favorites_data["favorite_categories"]:
            self.favorites_data["favorite_categories"].remove(category)
            self.save_favorites()
            await ctx.send(f"```Removed {category} from favorite categories```")

    @commands.command()
    async def fav(self, ctx, action: str = None, *args):
        if not await self.check_password(ctx):
            return

        if not action:
            await self.show_favorites_menu(ctx)
            return

        action = action.lower()
        
        if action == "help":
            await self.show_favorites_help(ctx)
            
        elif action == "add":
            if not args:
                await ctx.send("Please specify a command to add.")
                return
            command = args[0]
            note = " ".join(args[1:]) if len(args) > 1 else None
            await self.add_favorite(ctx, command, note)
            
        elif action == "remove":
            if not args:
                await ctx.send("Please specify a command to remove.")
                return
            await self.remove_favorite(ctx, args[0])
            
        elif action == "category":
            if not args:
                await ctx.send("Please specify a category.")
                return
            await self.add_category(ctx, args[0])
            
        elif action == "pin":
            if not args:
                await ctx.send("Please specify a command to pin.")
                return
            await self.pin_command(ctx, args[0])
            
        elif action == "note":
            if len(args) < 2:
                await ctx.send("Please specify a command and note.")
                return
            command = args[0]
            note = " ".join(args[1:])
            await self.add_note(ctx, command, note)
            
        elif action == "alias":
            if len(args) < 2:
                await ctx.send("Please specify an alias and command.")
                return
            alias = args[0]
            command = args[1]
            await self.add_alias(ctx, alias, command)
            
        else:
            await ctx.send("Invalid action. Use $fav help to see available actions.")

    async def show_favorite_stats(self, ctx):
        stats = []
        for cmd in sorted(self.favorites_data["favorites"]):
            cmd_stats = self.favorites_data["command_stats"].get(cmd, {})
            times_used = cmd_stats.get('times_used', 0)
            added_date = cmd_stats.get('added_date', 'Unknown')
            pinned = "🦇" if cmd in self.favorites_data["pinned_commands"] else ""
            
            stats.append(f"```ansi\n{black}[{white}{cmd}{black}] {white}{pinned}\n  {black}Used: {white}{times_used} times\n  {black}Added: {white}{added_date}```")
        
        if not stats:
            await ctx.send("```No favorite commands statistics available```")
            return
            
        await ctx.send("\n".join(stats))

    async def reset_help(self, ctx):
        if not await self.check_password(ctx):
            return
            
        if not self.help_session_active:
            return
            
        user = ctx.author
        await self.header_msg.edit(content=self.original_header)
        await self.content_msg.edit(content=self.original_content)
        await self.footer_msg.edit(content=self.original_footer)
        await self.reset_timeout()

    async def close_help(self, ctx):
        if not await self.check_password(ctx):
            return
            
        if not self.help_session_active:
            return
            
        if self.help_timeout_task:
            self.help_timeout_task.cancel()
            
        self.help_session_active = False
        
        await self.header_msg.delete()
        await self.content_msg.delete()
        await self.footer_msg.delete()
        
        self.header_msg = None
        self.content_msg = None
        self.footer_msg = None

    @commands.command()
    async def reset(self, ctx):
        await self.safe_delete(ctx)
        await self.reset_help(ctx)

    @commands.command()
    async def close(self, ctx):
        await self.safe_delete(ctx)
        await self.close_help(ctx)

    async def safe_delete(self, ctx):
        try:
            await ctx.message.delete()
        except (discord.NotFound, AttributeError):
            pass

    async def show_category(self, ctx, category: str):
        if not self.help_session_active:
            return
            
        try:
            await self.reload_data()  
            
            category = category.lower()
            if category not in self.commands_data:
                await ctx.send("```Category not found.```")
                return
                
            content = []
            category_pins = self.favorites_data.get("category_pins", {}).get(category, [])
            
            for cmd in category_pins:
                if cmd in self.commands_data[category]:
                    desc = self.commands_data[category][cmd]
                    content.append(f"{black}[{white}★{black}] {white}{cmd} {black}- {white}{desc}")
            
            num = 1
            for cmd, desc in self.commands_data[category].items():
                if cmd not in category_pins:
                    content.append(f"{black}[{white}{num}{black}] {white}{cmd} {black}- {white}{desc}")
                    num += 1
                
            await self.header_msg.edit(content=f"```ansi\n🦇      {black}{category.title()}       🦇               {black}[ {red}$menu - Return to Menu {black}]```")
            await self.content_msg.edit(content=f"""```ansi
{chr(10).join(content)}```""")
            await self.footer_msg.edit(content=f"```ansi\n                                        ⠀⠀⠀⠀⠀{black}i am the shadows.```")
        except (discord.NotFound, AttributeError):
            await self.menu(ctx)
            await self.show_category(ctx, category)

    async def owohunt_menu(self, ctx):
        await self.safe_delete(ctx)
        if not self.help_session_active:
            return
            
        pinned_commands = self.favorites_data.get("category_pins", {}).get("owo hunt", [])
        pinned_content = ""
        if pinned_commands:
            pinned_content = f"{black}Pinned Commands:\n" + "\n".join(f"{black}[{white}★{black}] {white}{cmd}" for cmd in pinned_commands) + "\n\n"
            
        commands = [
            "autohunt",
            "autohunt stop",
            "autohunt settings",
            "autohunt set hunt_min <seconds>",
            "autohunt set hunt_max <seconds>",
            "autohunt set pray <seconds>",
            "autohunt set battle <seconds>",
            "autohunt set sell <seconds>",
            "autohunt set coinflip <seconds>"
        ]
        
        numbered_commands = [cmd for cmd in commands if cmd not in pinned_commands]
        numbered_content = "\n".join(f"{black}[{white}{i+1}{black}] {white}{cmd}" for i, cmd in enumerate(numbered_commands))
            
        await self.header_msg.edit(content=f"```ansi\n{black}[ {red}$close - Close Menu {black}]               🦇      {black}OWO HUNT      🦇               [ {red}$reset - Reset Menu {black}]```")
        await self.content_msg.edit(content=f"""```ansi
{pinned_content}{numbered_content}```""")
        await self.footer_msg.edit(content=f"```ansi\n                                        ⠀⠀⠀⠀⠀ {black}I hunt in the shadows.```")

    async def antitoken_menu(self, ctx):
        await self.safe_delete(ctx)
        if not self.help_session_active:
            return
            
        pinned_commands = self.favorites_data.get("category_pins", {}).get("antitoken", [])
        pinned_content = ""
        if pinned_commands:
            pinned_content = f"{black}Pinned Commands:\n" + "\n".join(f"{black}[{white}★{black}] {white}{cmd}" for cmd in pinned_commands) + "\n\n"
            
        commands = [
            "antitoken toggle on",
            "antitoken toggle off",
            "antitoken limit mass_dm <amount>",
            "antitoken limit guild_actions <amount>",
            "antitoken limit account_changes <amount>",
            "antitoken status"
        ]
        
        numbered_commands = [cmd for cmd in commands if cmd not in pinned_commands]
    
        numbered_content = "\n".join(f"{black}[{white}{i+1}{black}] {white}{cmd}" for i, cmd in enumerate(numbered_commands))
            
        await self.header_msg.edit(content=f"```ansi\n{black}[ {red}$close - Close Menu {black}]               🦇      {black}ANTI TOKEN      🦇               [ {red}$reset - Reset Menu {black}]```")
        await self.content_msg.edit(content=f"""```ansi
{pinned_content}{numbered_content}```""")
        await self.footer_msg.edit(content=f"```ansi\n                                        ⠀⠀⠀⠀⠀ {black}I protect what's mine.```")

    async def token_controller_menu(self, ctx):
        await self.safe_delete(ctx)
        if not self.help_session_active:
            return
            
        pinned_commands = self.favorites_data.get("category_pins", {}).get("token controller", [])
        pinned_content = ""
        if pinned_commands:
            pinned_content = f"{black}Pinned Commands:\n" + "\n".join(f"{black}[{white}★{black}] {white}{cmd}" for cmd in pinned_commands) + "\n\n"
            
        commands = [
            "tokens",
            "tokens prefix <text>",
            "tokens suffix <text>",
            "tokens delay <seconds>",
            "tokens mirror",
            "tokens stop",
            "tokens clear"
        ]
        
        numbered_commands = [cmd for cmd in commands if cmd not in pinned_commands]
        numbered_content = "\n".join(f"{black}[{white}{i+1}{black}] {white}{cmd}" for i, cmd in enumerate(numbered_commands))
            
        await self.header_msg.edit(content=f"```ansi\n{black}[ {red}$close - Close Menu {black}]               🦇      {black}TOKEN CONTROLLER      🦇               [ {red}$reset - Reset Menu {black}]```")
        await self.content_msg.edit(content=f"""```ansi
{pinned_content}{numbered_content}```""")
        await self.footer_msg.edit(content=f"```ansi\n                                        ⠀⠀⠀⠀⠀ {black}I control the shadows.```")

    async def nuke_menu(self, ctx):
        await self.safe_delete(ctx)
        if not self.help_session_active:
            return
            
        pinned_commands = self.favorites_data.get("category_pins", {}).get("nuke", [])
        pinned_content = ""
        if pinned_commands:
            pinned_content = f"{black}Pinned Commands:\n" + "\n".join(f"{black}[{white}★{black}] {white}{cmd}" for cmd in pinned_commands) + "\n\n"
            
        commands = [
            "nuke",
            "nuke message <text>",
            "nuke name <text>",
            "nuke delay <seconds>",
            "nuke speed <seconds>",
            "nuke channels <amount>",
            "nuke roles <amount>",
            "nuke webhooks <amount>",
            "nuke reset",
            "nuke start",
            "nuke stop"
        ]
        
        numbered_commands = [cmd for cmd in commands if cmd not in pinned_commands]
        numbered_content = "\n".join(f"{black}[{white}{i+1}{black}] {white}{cmd}" for i, cmd in enumerate(numbered_commands))
            
        await self.header_msg.edit(content=f"```ansi\n{black}[ {red}$close - Close Menu {black}]               🦇      {black}KNIGHTFALL      🦇               [ {red}$reset - Reset Menu {black}]```")
        await self.content_msg.edit(content=f"""```ansi
{pinned_content}{numbered_content}```""")
        await self.footer_msg.edit(content=f"```ansi\n                                        ⠀⠀⠀⠀⠀ {black}I am vengeance.```")

    async def protection_menu(self, ctx):
        await self.safe_delete(ctx)
        if not self.help_session_active:
            return
            
        pinned_commands = self.favorites_data.get("category_pins", {}).get("protection", [])
        pinned_content = ""
        if pinned_commands:
            pinned_content = f"{black}Pinned Commands:\n" + "\n".join(f"{black}[{white}★{black}] {white}{cmd}" for cmd in pinned_commands) + "\n\n"
            
        commands = [
            "detection",
            "autoslow <seconds>",
            "noinvite",
            "setlog <channel>",
            "setpunishment <type>",
            "swhitelist <user>",
            "sunwhitelist <user>",
            "softban <user> [reason]",
            "hardban <user> [reason]",
            "unhardban <user>",
            "ghostban <id> [reason]",
            "multiban <id1 id2...>",
            "banlist",
            "stripall"
        ]
        
        numbered_commands = [cmd for cmd in commands if cmd not in pinned_commands]
        numbered_content = "\n".join(f"{black}[{white}{i+1}{black}] {white}{cmd}" for i, cmd in enumerate(numbered_commands))
            
        await self.header_msg.edit(content=f"```ansi\n{black}[ {red}$close - Close Menu {black}]               🦇      {black}PROTECTION      🦇               [ {red}$reset - Reset Menu {black}]```")
        await self.content_msg.edit(content=f"""```ansi
{pinned_content}{numbered_content}```""")
        await self.footer_msg.edit(content=f"```ansi\n                                        ⠀⠀⠀⠀⠀ {black}I protect this city.```")

    async def voice_menu(self, ctx):
        await self.safe_delete(ctx)
        if not self.help_session_active:
            return
            
        pinned_commands = self.favorites_data.get("category_pins", {}).get("voice", [])
        pinned_content = ""
        if pinned_commands:
            pinned_content = f"{black}Pinned Commands:\n" + "\n".join(f"{black}[{white}★{black}] {white}{cmd}" for cmd in pinned_commands) + "\n\n"
            
        commands = [
            "voice",
            "voice join <channel>",
            "voice leave",
            "voice move <user> <channel>",
            "voice region <region>",
            "voice bitrate <kbps>",
            "voice deafen <on/off>",
            "voice mute <on/off>",
            "voice quality <360/720/1080>",
            "voice volume <0-100>",
            "voice reset"
        ]
        
        numbered_commands = [cmd for cmd in commands if cmd not in pinned_commands]
        numbered_content = "\n".join(f"{black}[{white}{i+1}{black}] {white}{cmd}" for i, cmd in enumerate(numbered_commands))
            
        await self.header_msg.edit(content=f"```ansi\n{black}[ {red}$close - Close Menu {black}]               🦇      {black}VOICE CONTROL      🦇               [ {red}$reset - Reset Menu {black}]```")
        await self.content_msg.edit(content=f"""```ansi
{pinned_content}{numbered_content}```""")
        await self.footer_msg.edit(content=f"```ansi\n                                        ⠀⠀⠀⠀⠀ {black}I am the night.```")

    @commands.command(name="16")
    async def cmd_16(self, ctx):
        await self.safe_delete(ctx)
        if not self.help_session_active:
            return
        await self.nuke_menu(ctx)
        await self.reset_timeout()

    @commands.command(name="1")
    async def cmd_1(self, ctx):
        await self.safe_delete(ctx)
        if not self.help_session_active:
            return
        await self.show_favorites_menu(ctx)
        await self.reset_timeout()

    @commands.command(name="2")
    async def cmd_2(self, ctx):
        await self.safe_delete(ctx)
        if not self.help_session_active:
            return
        await self.chatpacking(ctx)
        await self.reset_timeout()

    @commands.command(name="3")
    async def cmd_3(self, ctx):
        await self.safe_delete(ctx)
        if not self.help_session_active:
            return
        await self.token_utility(ctx)
        await self.reset_timeout()

    @commands.command(name="4")
    async def cmd_4(self, ctx):
        await self.safe_delete(ctx)
        if not self.help_session_active:
            return
        await self.user_utility(ctx)
        await self.reset_timeout()

    @commands.command(name="5")
    async def cmd_5(self, ctx):
        await self.safe_delete(ctx)
        if not self.help_session_active:
            return
        await self.pc_utility(ctx)
        await self.reset_timeout()

    @commands.command(name="6")
    async def cmd_6(self, ctx):
        await self.safe_delete(ctx)
        if not self.help_session_active:
            return
        await self.nuker(ctx)
        await self.reset_timeout()

    @commands.command(name="7")
    async def cmd_7(self, ctx):
        await self.safe_delete(ctx)
        if not self.help_session_active:
            return
        await self.etc(ctx)
        await self.reset_timeout()

    @commands.command(name="8")
    async def cmd_8(self, ctx):
        await self.safe_delete(ctx)
        if not self.help_session_active:
            return
        await self.event_reactions(ctx)
        await self.reset_timeout()

    @commands.command(name="9")
    async def cmd_9(self, ctx):
        await self.safe_delete(ctx)
        if not self.help_session_active:
            return
        await self.profile_menu(ctx)
        await self.reset_timeout()

    @commands.command(name="10")
    async def cmd_10(self, ctx):
        await self.safe_delete(ctx)
        if not self.help_session_active:
            return
        await self.groupchat_menu(ctx)
        await self.reset_timeout()

    @commands.command(name="11")
    async def cmd_11(self, ctx):
        await self.safe_delete(ctx)
        if not self.help_session_active:
            return
        await self.auto_messenger_menu(ctx)
        await self.reset_timeout()

    @commands.command(name="12")
    async def cmd_12(self, ctx):
        await self.safe_delete(ctx)
        if not self.help_session_active:
            return
        await self.show_favorites_help(ctx)
        await self.reset_timeout()

    @commands.command(name="13")
    async def cmd_13(self, ctx):
        await self.safe_delete(ctx)
        if not self.help_session_active:
            return
        await self.antitoken_menu(ctx)
        await self.reset_timeout()

    @commands.command(name="14")
    async def cmd_14(self, ctx):
        await self.safe_delete(ctx)
        if not self.help_session_active:
            return
        await self.token_controller_menu(ctx)
        await self.reset_timeout()

    @commands.command(name="15")
    async def cmd_15(self, ctx):
        await self.safe_delete(ctx)
        if not self.help_session_active:
            return
        await self.owohunt_menu(ctx)
        await self.reset_timeout()

    @commands.command(name="17")
    async def cmd_17(self, ctx):
        await self.safe_delete(ctx)
        if not self.help_session_active:
            return
        await self.protection_menu(ctx)
        await self.reset_timeout()

    @commands.command(name="18")
    async def cmd_18(self, ctx):
        await self.safe_delete(ctx)
        if not self.help_session_active:
            return
        await self.voice_menu(ctx)
        await self.reset_timeout()

def setup(bot):
    bot.add_cog(HelpCog(bot))
