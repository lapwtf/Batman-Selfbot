import json

def load_config(file_path='config.json'):
    with open(file_path, 'r') as f:
        return json.load(f)

def check_password(password, config):
    return password == config.get('password')
import discord
from discord.ext import commands
import asyncio
import datetime
import random

black = "\x1b[30m"
white = "\x1b[37m"
red = "\x1b[31m"

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.region_list = [
            "brazil", "hongkong", "india", "japan", "rotterdam", 
            "russia", "singapore", "southafrica", "sydney", "us-central",
            "us-east", "us-south", "us-west"
        ]
        self.active_soundboards = {}
        self.load_settings()
        self.voice_states = {}

    def load_settings(self):
        try:
            with open('data/voice_settings.json', 'r') as f:
                self.settings = json.load(f)
        except:
            self.settings = {
                'default_bitrate': 96000,
                'default_region': 'us-east',
                'auto_deafen': True,
                'auto_mute': False,
                'stream_quality': 720,
                'soundboard_volume': 50
            }
            self.save_settings()

    def save_settings(self):
        with open('data/voice_settings.json', 'w') as f:
            json.dump(self.settings, f, indent=4)

    async def join_voice_channel(self, channel: discord.VoiceChannel):
        try:
            if channel.guild.voice_client:
                await channel.guild.voice_client.disconnect(force=True)
                await asyncio.sleep(0.5) 
            
            voice_client = await channel.connect(timeout=30, reconnect=True)
            if voice_client and voice_client.is_connected():
                try:
                    await asyncio.sleep(0.5)
                    voice_client.self_mute = self.settings['auto_mute']
                    voice_client.self_deaf = self.settings['auto_deafen']
                except Exception as e:
                    print(f"Error updating voice state: {str(e)}")
                return True
            return False
        except Exception as e:
            print(f"Error joining voice channel: {str(e)}")
            try:
                if channel.guild.voice_client:
                    await channel.guild.voice_client.disconnect(force=True)
            except:
                pass
            return False

    async def leave_voice_channel(self, guild: discord.Guild):
        success = True
        try:
            if guild.voice_client:
                try:
                    voice_client = guild.voice_client
                    voice_client.self_mute = False
                    voice_client.self_deaf = False
                except Exception as e:
                    print(f"Error resetting voice state: {str(e)}")
                
                try:
                    await guild.voice_client.disconnect(force=True)
                except Exception as e:
                    print(f"Error disconnecting: {str(e)}")
                    success = False
        except Exception as e:
            print(f"Error leaving voice channel: {str(e)}")
            success = False
        
        await asyncio.sleep(0.5)
        
        if guild.voice_client is None:
            success = True
            
        return success

    async def move_user(self, member: discord.Member, channel: discord.VoiceChannel):
        try:
            await member.move_to(channel)
            return True
        except Exception as e:
            print(f"Error moving user: {str(e)}")
            return False

    @commands.group(invoke_without_command=True)
    async def voice(self, ctx):
        await ctx.send(f"""```ansi
{black}[ {red}BATMAN VOICE {black}]
{black}⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯

{black}[{white}Settings{black}]
{black}[{white}Bitrate{black}] {white}{self.settings['default_bitrate']/1000}kbps
{black}[{white}Region{black}] {white}{self.settings['default_region']}
{black}[{white}Auto Deafen{black}] {white}{self.settings['auto_deafen']}
{black}[{white}Auto Mute{black}] {white}{self.settings['auto_mute']}
{black}[{white}Stream Quality{black}] {white}{self.settings['stream_quality']}p
{black}[{white}Soundboard Volume{black}] {white}{self.settings['soundboard_volume']}%

{black}[{white}Commands{black}]
{black}[{white}1{black}] {white}join <channel> {black}- Join voice channel
{black}[{white}2{black}] {white}leave {black}- Leave voice channel
{black}[{white}3{black}] {white}move <user> <channel> {black}- Move user
{black}[{white}4{black}] {white}region <region> {black}- Set voice region
{black}[{white}5{black}] {white}bitrate <kbps> {black}- Set bitrate
{black}[{white}6{black}] {white}deafen <on/off> {black}- Toggle auto deafen
{black}[{white}7{black}] {white}mute <on/off> {black}- Toggle auto mute
{black}[{white}8{black}] {white}quality <360/720/1080> {black}- Set stream quality
{black}[{white}9{black}] {white}volume <0-100> {black}- Set soundboard volume
{black}[{white}0{black}] {white}reset {black}- Reset all settings```""")

    @voice.command()
    async def join(self, ctx, channel: discord.VoiceChannel):
        success = await self.join_voice_channel(channel)
        
        if success:
            await ctx.send(f"""```ansi
{black}[ {red}BATMAN VOICE {black}]
{black}[{white}Success{black}] {white}Joined {channel.name}```""")
        else:
            await ctx.send(f"""```ansi
{black}[ {red}BATMAN VOICE {black}]
{black}[{white}Error{black}] {white}Failed to join channel```""")

    @voice.command()
    async def leave(self, ctx):
        success = await self.leave_voice_channel(ctx.guild)
        if success:
            await ctx.send(f"""```ansi
{black}[ {red}BATMAN VOICE {black}]
{black}[{white}Success{black}] {white}Left voice channel```""")
        else:
            print("Failed to leave voice channel")
    @voice.command()
    async def move(self, ctx, user: discord.Member, channel: discord.VoiceChannel):
        success = await self.move_user(user, channel)
        if success:
            await ctx.send(f"""```ansi
{black}[ {red}BATMAN VOICE {black}]
{black}[{white}Success{black}] {white}Moved {user.name} to {channel.name}```""")
        else:
            await ctx.send(f"""```ansi
{black}[ {red}BATMAN VOICE {black}]
{black}[{white}Error{black}] {white}Failed to move user```""")

    @voice.command()
    async def region(self, ctx, region: str):
        region = region.lower()
        if region not in self.region_list:
            regions = ", ".join(self.region_list)
            await ctx.send(f"""```ansi
{black}[ {red}BATMAN VOICE {black}]
{black}[{white}Error{black}] {white}Invalid region
{black}[{white}Valid Regions{black}] {white}{regions}```""")
            return

        self.settings['default_region'] = region
        self.save_settings()
        await ctx.send(f"""```ansi
{black}[ {red}BATMAN VOICE {black}]
{black}[{white}Success{black}] {white}Voice region set to {region}```""")

    @voice.command()
    async def bitrate(self, ctx, kbps: int):
        if not 8 <= kbps <= 384:
            await ctx.send(f"""```ansi
{black}[ {red}BATMAN VOICE {black}]
{black}[{white}Error{black}] {white}Bitrate must be between 8 and 384 kbps```""")
            return

        self.settings['default_bitrate'] = kbps * 1000
        self.save_settings()
        await ctx.send(f"""```ansi
{black}[ {red}BATMAN VOICE {black}]
{black}[{white}Success{black}] {white}Voice bitrate set to {kbps}kbps```""")

    @voice.command()
    async def deafen(self, ctx, state: str):
        state = state.lower()
        if state not in ['on', 'off']:
            await ctx.send(f"""```ansi
{black}[ {red}BATMAN VOICE {black}]
{black}[{white}Error{black}] {white}Use 'on' or 'off'```""")
            return

        self.settings['auto_deafen'] = state == 'on'
        self.save_settings()
        
        if ctx.guild.voice_client and ctx.guild.voice_client.is_connected():
            try:
                voice_client = ctx.guild.voice_client
                voice_client.self_deaf = self.settings['auto_deafen']
                
                await asyncio.sleep(0.5)
                if voice_client.self_deaf == self.settings['auto_deafen']:
                    await ctx.send(f"""```ansi
{black}[ {red}BATMAN VOICE {black}]
{black}[{white}Success{black}] {white}Auto deafen turned {state} and applied```""")
                    return
            except Exception as e:
                print(f"Error updating deafen state: {str(e)}")
            
        await ctx.send(f"""```ansi
{black}[ {red}BATMAN VOICE {black}]
{black}[{white}Success{black}] {white}Auto deafen turned {state}```""")

    @voice.command()
    async def mute(self, ctx, state: str):
        state = state.lower()
        if state not in ['on', 'off']:
            await ctx.send(f"""```ansi
{black}[ {red}BATMAN VOICE {black}]
{black}[{white}Error{black}] {white}Use 'on' or 'off'```""")
            return

        self.settings['auto_mute'] = state == 'on'
        self.save_settings()
        
        if ctx.guild.voice_client and ctx.guild.voice_client.is_connected():
            try:
                voice_client = ctx.guild.voice_client
                voice_client.self_mute = self.settings['auto_mute']
                
                await asyncio.sleep(0.5)
                if voice_client.self_mute == self.settings['auto_mute']:
                    await ctx.send(f"""```ansi
{black}[ {red}BATMAN VOICE {black}]
{black}[{white}Success{black}] {white}Auto mute turned {state} and applied```""")
                    return
            except Exception as e:
                print(f"Error updating mute state: {str(e)}")
            
        await ctx.send(f"""```ansi
{black}[ {red}BATMAN VOICE {black}]
{black}[{white}Success{black}] {white}Auto mute turned {state}```""")

    @voice.command()
    async def quality(self, ctx, quality: int):
        if quality not in [360, 720, 1080]:
            await ctx.send(f"""```ansi
{black}[ {red}BATMAN VOICE {black}]
{black}[{white}Error{black}] {white}Quality must be 360, 720, or 1080```""")
            return

        self.settings['stream_quality'] = quality
        self.save_settings()
        await ctx.send(f"""```ansi
{black}[ {red}BATMAN VOICE {black}]
{black}[{white}Success{black}] {white}Stream quality set to {quality}p```""")

    @voice.command()
    async def volume(self, ctx, volume: int):
        if not 0 <= volume <= 100:
            await ctx.send(f"""```ansi
{black}[ {red}BATMAN VOICE {black}]
{black}[{white}Error{black}] {white}Volume must be between 0 and 100```""")
            return

        self.settings['soundboard_volume'] = volume
        self.save_settings()
        await ctx.send(f"""```ansi
{black}[ {red}BATMAN VOICE {black}]
{black}[{white}Success{black}] {white}Soundboard volume set to {volume}%```""")

    @voice.command()
    async def reset(self, ctx):
        self.settings = {
            'default_bitrate': 96000,
            'default_region': 'us-east',
            'auto_deafen': True,
            'auto_mute': False,
            'stream_quality': 720,
            'soundboard_volume': 50
        }
        self.save_settings()
        await ctx.send(f"""```ansi
{black}[ {red}BATMAN VOICE {black}]
{black}[{white}Success{black}] {white}Voice settings reset to default```""")

def setup(bot):
    bot.add_cog(Voice(bot))
