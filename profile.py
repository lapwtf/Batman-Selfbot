import json
import discord
from discord.ext import commands
import aiohttp
import base64
import requests
from tls_client import Session

def load_config(file_path='config.json'):
    with open(file_path, 'r') as f:
        return json.load(f)

sesh = Session(client_identifier="chrome_115", random_tls_extension_order=True)

class ProfileCog(commands.Cog, name="Profile"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setpfp(self, ctx, url: str):
        headers = {
            "authority": "discord.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": self.bot.http.token,
            "content-type": "application/json",
            "origin": "https://discord.com",
            "referer": "https://discord.com/channels/@me",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-super-properties": "eyJvcyI6Ik1hYyBPUyBYIiwiYnJvd3NlciI6IlNhZmFyaSIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDEwXzE1XzcpIEFwcGxlV2ViS2l0LzYwNS4xLjE1IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi8xNi41IFNhZmFyaS82MDUuMS4xNSIsImJyb3dzZXJfdmVyc2lvbiI6IjE2LjUiLCJvc192ZXJzaW9uIjoiMTAuMTUuNyIsInJlZmVycmVyIjoiIiwicmVmZXJyaW5nX2RvbWFpbiI6IiIsInJlZmVycmVyX2N1cnJlbnQiOiIiLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiIiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyNTA2ODQsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    image_b64 = base64.b64encode(image_data).decode()
                    
                    content_type = response.headers.get('Content-Type', '')
                    if 'gif' in content_type:
                        image_format = 'gif'
                    else:
                        image_format = 'png'

                    payload = {
                        "avatar": f"data:image/{image_format};base64,{image_b64}"
                    }

                    response = sesh.patch("https://discord.com/api/v9/users/@me", json=payload, headers=headers)
                    
                    if response.status_code == 200:
                        await ctx.send("```Successfully set profile picture```")
                    else:
                        await ctx.send(f"```Failed to update profile picture: {response.status_code}```")
                else:
                    await ctx.send("```Failed to download image from URL```")

    @commands.command()
    async def setbanner(self, ctx, url: str):
        headers = {
            "authority": "discord.com",
            "method": "PATCH",
            "scheme": "https",
            "accept": "/",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US",
            "authorization": self.bot.http.token,
            "origin": "https://discord.com/",
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

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    image_b64 = base64.b64encode(image_data).decode()
                    
                    content_type = response.headers.get('Content-Type', '')
                    if 'gif' in content_type:
                        image_format = 'gif'
                    else:
                        image_format = 'png'

                    payload = {
                        "banner": f"data:image/{image_format};base64,{image_b64}"
                    }

                    response = sesh.patch("https://discord.com/api/v9/users/@me", json=payload, headers=headers)
                    
                    if response.status_code == 200:
                        await ctx.send("```Successfully set banner```")
                    else:
                        await ctx.send(f"```Failed to update banner: {response.status_code}```")
                else:
                    await ctx.send("```Failed to download image from URL```")

    @commands.command()
    async def setbio(self, ctx, *, bio_text: str):
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.bot.http.token
        }

        new_bio = {
            "bio": bio_text
        }

        url_api_info = "https://discord.com/api/v9/users/%40me/profile"
        
        try:
            response = sesh.patch(url_api_info, headers=headers, json=new_bio)

            if response.status_code == 200:
                await ctx.send("```Bio updated successfully!```")
            else:
                await ctx.send(f"```Failed to update bio: {response.status_code} - {response.json()}```")

        except Exception as e:
            await ctx.send(f"```An error occurred: {e}```")

    @commands.command()
    async def setpronoun(self, ctx, *, pronoun: str):
        headers = {
            "Authorization": self.bot.http.token,
            "Content-Type": "application/json"
        }

        new_name = {
            "pronouns": pronoun
        }

        url_api_info = "https://discord.com/api/v9/users/%40me/profile"

        try:
            response = sesh.patch(url_api_info, headers=headers, json=new_name)

            if response.status_code == 200:
                await ctx.send(f"```pronoun updated to: {pronoun}```")
            else:
                await ctx.send(f"```Failed to update pronoun : {response.status_code} - {response.json()}```")

        except Exception as e:
            await ctx.send(f"```An error occurred: {e}```")

    @commands.command()
    async def setname(self, ctx, *, name: str = None):
        if not name:
            await ctx.send("```Please provide a name to set```")
            return

        headers = {
            "authority": "discord.com",
            "method": "PATCH",
            "scheme": "https",
            "accept": "/",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US",
            "authorization": self.bot.http.token,
            "origin": "https://discord.com/",
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

        payload = {
            "global_name": name
        }

        response = sesh.patch("https://discord.com/api/v9/users/@me", json=payload, headers=headers)
        
        if response.status_code == 200:
            await ctx.send(f"```Successfully set global name to: {name}```")
        else:
            await ctx.send(f"```Failed to update global name: {response.status_code}```")

    @commands.command()
    async def stealbio(self, ctx, member: discord.User):
        url = f"https://discord.com/api/v9/users/{member.id}/profile?with_mutual_guilds=true&with_mutual_friends=true"
        headers = {
            "Authorization": self.bot.http.token
        }

        try:
            response = sesh.get(url, headers=headers)
            data = response.json()

            if response.status_code == 200:
                target_bio = data.get("user", {}).get("bio", None)

                if target_bio:
                    set_bio_url = "https://discord.com/api/v9/users/@me/profile"
                    new_bio = {"bio": target_bio}

                    update_response = sesh.patch(set_bio_url, headers=headers, json=new_bio)

                    if update_response.status_code == 200:
                        await ctx.send("```Bio updated!```")
                    else:
                        await ctx.send(f"```Failed: {update_response.status_code} - {update_response.json()}```")
                else:
                    await ctx.send("```user does not have a bio to copy.```")
            else:
                await ctx.send(f"```Failed: {response.status_code} - {data}```")

        except Exception as e:
            await ctx.send(f"```{e}```")

    @commands.command()
    async def stealpronoun(self, ctx, member: discord.User):
        url = f"https://discord.com/api/v9/users/{member.id}/profile?with_mutual_guilds=true&with_mutual_friends=true"
        headers = {
            "Authorization": self.bot.http.token
        }

        try:
            response = sesh.get(url, headers=headers)
            data = response.json()

            if response.status_code == 200:
                target_pronouns = data.get("user_profile", {}).get("pronouns", None)

                if target_pronouns:
                    set_pronoun_url = "https://discord.com/api/v9/users/%40me/profile"
                    new_pronoun = {"pronouns": target_pronouns}

                    update_response = sesh.patch(set_pronoun_url, headers=headers, json=new_pronoun)

                    if update_response.status_code == 200:
                        await ctx.send("```Pronouns stolen successful.```")
                    else:
                        await ctx.send(f"```Failed: {update_response.status_code} - {update_response.json()}```")
                else:
                    await ctx.send("```user does not have pronouns set to copy.```")
            else:
                await ctx.send(f"```Failed: {response.status_code} - {data}```")

        except Exception as e:
            await ctx.send(f"```{e}```")

    @commands.command()
    async def stealpfp(self, ctx, user: discord.Member = None):
        if not user:
            await ctx.send("```Please mention a user to steal their profile picture```")
            return

        headers = {
            "authority": "discord.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": self.bot.http.token,
            "content-type": "application/json",
            "origin": "https://discord.com",
            "referer": "https://discord.com/channels/@me",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-super-properties": "eyJvcyI6Ik1hYyBPUyBYIiwiYnJvd3NlciI6IlNhZmFyaSIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDEwXzE1XzcpIEFwcGxlV2ViS2l0LzYwNS4xLjE1IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi8xNi41IFNhZmFyaS82MDUuMS4xNSIsImJyb3dzZXJfdmVyc2lvbiI6IjE2LjUiLCJvc192ZXJzaW9uIjoiMTAuMTUuNyIsInJlZmVycmVyIjoiIiwicmVmZXJyaW5nX2RvbWFpbiI6IiIsInJlZmVycmVyX2N1cnJlbnQiOiIiLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiIiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyNTA2ODQsImNsaWVudF9ldmVyc2lvbiI6IjIyLjMuMjYiLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsLCJkZXNpZ25faWQiOjB9"
        }
        avatar_format = "gif" if user.is_avatar_animated() else "png"
        avatar_url = str(user.avatar_url_as(format=avatar_format))

        async with aiohttp.ClientSession() as session:
            async with session.get(avatar_url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    image_b64 = base64.b64encode(image_data).decode()

                    payload = {
                        "avatar": f"data:image/{avatar_format};base64,{image_b64}"
                    }

                    response = sesh.patch("https://discord.com/api/v9/users/@me", json=payload, headers=headers)
                    
                    if response.status_code == 200:
                        await ctx.send(f"```Successfully stole {user.name}'s profile picture```")
                    else:
                        await ctx.send(f"```Failed to update profile picture: {response.status_code}```")
                else:
                    await ctx.send("```Failed to download the user's profile picture```")

    @commands.command()
    async def stealbanner(self, ctx, user: discord.Member = None):
        if not user:
            await ctx.send("```Please mention a user to steal their banner```")
            return

        headers = {
            "authority": "discord.com",
            "method": "PATCH",
            "scheme": "https",
            "accept": "/",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US",
            "authorization": self.bot.http.token,
            "origin": "https://discord.com/",
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

        profile_url = f"https://discord.com/api/v9/users/{user.id}/profile"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(profile_url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    banner_hash = data.get("user", {}).get("banner")
                    
                    if not banner_hash:
                        await ctx.send("```This user doesn't have a banner```")
                        return
                    
                    banner_format = "gif" if banner_hash.startswith("a_") else "png"
                    banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_hash}.{banner_format}?size=1024"
                    
                    async with session.get(banner_url) as banner_response:
                        if banner_response.status == 200:
                            banner_data = await banner_response.read()
                            banner_b64 = base64.b64encode(banner_data).decode()
                            
                            payload = {
                                "banner": f"data:image/{banner_format};base64,{banner_b64}"
                            }
                            
                            response = sesh.patch("https://discord.com/api/v9/users/@me", json=payload, headers=headers)
                            
                            if response.status_code == 200:
                                await ctx.send(f"```Successfully stole {user.name}'s banner```")
                            else:
                                await ctx.send(f"```Failed to update banner: {response.status_code}```")
                        else:
                            await ctx.send("```Failed to download the user's banner```")
                else:
                    await ctx.send("```Failed to fetch user profile```")

def setup(bot):
    bot.add_cog(ProfileCog(bot))
