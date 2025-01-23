import discord
from discord.ext import commands
import json
import asyncio
from typing import Optional, List
import datetime
import aiohttp

class ServerProtection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.whitelist = set()
        self.detection_enabled = False
        self.autoslow_enabled = False
        self.noinvite_enabled = False
        self.spam_counter = {}
        self.headers = {
            'Authorization': self.bot.http.token,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.owner_id = 1255185280604962898
        self.punishment_type = "ban"  
        self.hard_banned_users = set()  
        self.log_channel = None  
        self.restricted_role = None  
        self.load_whitelist()
        self.load_settings()

    def load_whitelist(self):
        try:
            with open('whitelist.json', 'r') as f:
                data = json.load(f)
                self.whitelist = set(data['whitelist'])
        except FileNotFoundError:
            with open('whitelist.json', 'w') as f:
                json.dump({'whitelist': []}, f)

    def load_settings(self):
        try:
            with open('protection_settings.json', 'r') as f:
                data = json.load(f)
                self.punishment_type = data.get('punishment', 'ban')
                self.hard_banned_users = set(data.get('hard_banned', []))
                self.log_channel_id = data.get('log_channel', None)
        except FileNotFoundError:
            self.save_settings()

    def save_settings(self):
        with open('protection_settings.json', 'w') as f:
            json.dump({
                'punishment': self.punishment_type,
                'hard_banned': list(self.hard_banned_users),
                'log_channel': self.log_channel.id if self.log_channel else None
            }, f)

    def save_whitelist(self):
        with open('whitelist.json', 'w') as f:
            json.dump({'whitelist': list(self.whitelist)}, f)

    async def log_action(self, message: str, color: int = 0xFF0000):
        if self.log_channel:
            embed = discord.Embed(
                description=message,
                color=color,
                timestamp=datetime.datetime.now()
            )
            try:
                await self.log_channel.send(embed=embed)
            except:
                pass

    @commands.command()
    async def setlog(self, ctx, channel: discord.TextChannel = None):
        if ctx.author.id != self.owner_id:
            return await ctx.send("```You are not authorized to use this command.```")

        if channel is None:
            self.log_channel = None
            await ctx.send("```Logging has been disabled```")
        else:
            self.log_channel = channel
            await ctx.send(f"```Logging channel set to #{channel.name}```")
            await self.log_action("🔧 Logging channel has been set", color=0x00FF00)
        self.save_settings()

    async def ensure_restricted_role(self, guild):
        if not self.restricted_role:
            role = discord.utils.get(guild.roles, name="Restricted")
            if not role:
                permissions = discord.Permissions()
                permissions.update(
                    send_messages=False,
                    add_reactions=False,
                    view_channel=True,
                    read_message_history=True
                )
                role = await guild.create_role(
                    name="Restricted",
                    permissions=permissions,
                    color=discord.Color.dark_gray(),
                    reason="Protection: Create restricted role"
                )
                positions = {role: 1}
                await guild.edit_role_positions(positions)
            self.restricted_role = role
        return self.restricted_role

    @commands.command()
    async def swhitelist(self, ctx, member: discord.Member):
        if ctx.author.id != self.owner_id:
            return await ctx.send("```You are not authorized to use this command.```")
        
        self.whitelist.add(member.id)
        self.save_whitelist()
        await ctx.send(f"```{member.name} has been added to the whitelist.```")

    @commands.command()
    async def sunwhitelist(self, ctx, member: discord.Member):
        if ctx.author.id != self.owner_id:
            return await ctx.send("```You are not authorized to use this command.```")
            
        if member.id in self.whitelist:
            self.whitelist.remove(member.id)
            self.save_whitelist()
            await ctx.send(f"```{member.name} has been removed from the whitelist.```")
        else:
            await ctx.send(f"```{member.name} is not in the whitelist.```")

    @commands.command()
    async def setpunishment(self, ctx, punishment_type: str):
        if ctx.author.id != self.owner_id:
            return await ctx.send("```You are not authorized to use this command.```")
        
        valid_types = ['ban', 'kick', 'timeout', 'strip', 'none']
        if punishment_type.lower() not in valid_types:
            return await ctx.send(f"```Invalid punishment type. Choose from: {', '.join(valid_types)}```")
        
        self.punishment_type = punishment_type.lower()
        self.save_settings()
        await ctx.send(f"```Punishment type set to: {punishment_type}```")
        await self.log_action(f"🔧 Punishment type changed to: {punishment_type}", color=0x00FF00)

    @commands.command()
    async def softban(self, ctx, user: discord.User, *, reason="No reason provided"):
        if ctx.author.id != self.owner_id:
            return await ctx.send("```You are not authorized to use this command.```")
        
        try:
            await ctx.guild.ban(user, reason=f"Softban: {reason}", delete_message_days=7)
            await asyncio.sleep(1) 
            await ctx.guild.unban(user, reason="Softban complete")
            await ctx.send(f"```Successfully softbanned {user.name}#{user.discriminator}```")
        except Exception as e:
            await ctx.send(f"```Error: {str(e)}```")

    @commands.command()
    async def hardban(self, ctx, user: discord.User, *, reason="No reason provided"):
        if ctx.author.id != self.owner_id:
            return await ctx.send("```You are not authorized to use this command.```")
        
        try:
            self.hard_banned_users.add(user.id)
            self.save_settings()
            await ctx.guild.ban(user, reason=f"Hardban: {reason}")
            await ctx.send(f"```Successfully hardbanned {user.name}#{user.discriminator}```")
        except Exception as e:
            await ctx.send(f"```Error: {str(e)}```")

    @commands.command()
    async def unhardban(self, ctx, user: discord.User):
        if ctx.author.id != self.owner_id:
            return await ctx.send("```You are not authorized to use this command.```")
        
        if user.id in self.hard_banned_users:
            self.hard_banned_users.remove(user.id)
            self.save_settings()
            await ctx.send(f"```Removed {user.name}#{user.discriminator} from hardban list```")
        else:
            await ctx.send("```User is not hardbanned```")

    @commands.command()
    async def ghostban(self, ctx, user_id: str, *, reason="No reason provided"):
        if ctx.author.id != self.owner_id:
            return await ctx.send("```You are not authorized to use this command.```")
        
        try:
            user_id = int(user_id.strip('<@!>'))
            
            endpoint = f"https://discord.com/api/v10/guilds/{ctx.guild.id}/bans/{user_id}"
            
            async with aiohttp.ClientSession() as session:
                user_endpoint = f"https://discord.com/api/v10/users/{user_id}"
                async with session.get(user_endpoint, headers=self.headers) as resp:
                    if resp.status == 404:
                        return await ctx.send("```User not found```")
                    user_data = await resp.json()
                    
                ban_check = f"https://discord.com/api/v10/guilds/{ctx.guild.id}/bans/{user_id}"
                async with session.get(ban_check, headers=self.headers) as resp:
                    if resp.status == 200:
                        return await ctx.send(f"```{user_data.get('username')} is already banned```")
                
                payload = {
                    "delete_message_days": "7",
                    "reason": f"Ghostban: {reason}"
                }
                async with session.put(endpoint, headers=self.headers, json=payload) as resp:
                    if resp.status == 204:
                        await ctx.send(f"```Successfully ghostbanned {user_data.get('username')}#{user_data.get('discriminator')}```")
                        await self.log_action(f"Ghostbanned {user_data.get('username')} ({user_id}) - Reason: {reason}")
                    elif resp.status == 403:
                        await ctx.send("```Error: Missing permissions to ban this user```")
                    elif resp.status == 404:
                        await ctx.send("```Error: User or guild not found```")
                    else:
                        error_data = await resp.json()
                        await ctx.send(f"```Error: {error_data.get('message', 'Unknown error')}```")
                        
        except ValueError:
            await ctx.send("```Invalid user ID```")
        except Exception as e:
            await ctx.send(f"```Error: {str(e)}```")

    @commands.command()
    async def multiban(self, ctx, *, user_ids: str):
        if ctx.author.id != self.owner_id:
            return await ctx.send("```You are not authorized to use this command.```")
        
        user_ids = user_ids.split()
        banned = []
        failed = []
        
        for user_id in user_ids:
            try:
                user_id = int(user_id.strip('<@!>'))
                user = await self.bot.fetch_user(user_id)
                await ctx.guild.ban(user, reason="Mass ban")
                banned.append(f"{user.name}#{user.discriminator}")
            except:
                failed.append(user_id)
        
        result = "Mass ban results:\n"
        if banned:
            result += f"Banned: {', '.join(banned)}\n"
        if failed:
            result += f"Failed: {', '.join(map(str, failed))}"
        
        await ctx.send(f"```{result}```")

    @commands.command()
    async def banlist(self, ctx):
        if ctx.author.id != self.owner_id:
            return await ctx.send("```You are not authorized to use this command.```")
        
        bans = [entry async for entry in ctx.guild.bans()]
        if not bans:
            return await ctx.send("```No banned users```")
        
        ban_list = "\n".join(f"{ban.user.name}#{ban.user.discriminator} ({ban.user.id}): {ban.reason or 'No reason'}" 
                            for ban in bans)
        
        chunks = [ban_list[i:i+1990] for i in range(0, len(ban_list), 1990)]
        for chunk in chunks:
            await ctx.send(f"```{chunk}```")

    @commands.command()
    async def stripall(self, ctx):
        if ctx.author.id != self.owner_id:
            return await ctx.send("```You are not authorized to use this command.```")
        
        async with ctx.typing():
            for role in ctx.guild.roles:
                if role.permissions.administrator:
                    try:
                        await ctx.send(f"```Checking role: {role.name}```")
                        for member in role.members:
                            if member.id not in self.whitelist:
                                try:
                                    await member.remove_roles(role)
                                    await ctx.send(f"```Removed admin role from {member.name}```")
                                except discord.Forbidden:
                                    await ctx.send(f"```Cannot remove role from {member.name} due to permissions```")
                            else:
                                await ctx.send(f"```Skipped {member.name} (Whitelisted)```")
                    except discord.Forbidden:
                        await ctx.send(f"```Cannot access role {role.name} due to permissions```")
        
        await ctx.send("```Finished stripping admin permissions```")

    async def punish_user(self, user, guild, reason):
        try:
            roles_removed = []
            for role in user.roles:
                if role.permissions.administrator or role.permissions.ban_members or role.permissions.manage_guild:
                    roles_removed.append(role)
                    try:
                        await user.remove_roles(role, reason=f"Protection: {reason}")
                    except:
                        pass

            if self.punishment_type == "ban":
                await guild.ban(user, reason=f"Protection: {reason}")
                await self.log_action(f"Banned {user.name} ({user.id}) for {reason}")
            elif self.punishment_type == "kick":
                await guild.kick(user, reason=f"Protection: {reason}")
                await self.log_action(f" Kicked {user.name} ({user.id}) for {reason}")
            elif self.punishment_type == "timeout":
                await user.timeout(datetime.timedelta(hours=1), reason=f"Protection: {reason}")
                await self.log_action(f" Timed out {user.name} ({user.id}) for {reason}")
            elif self.punishment_type == "strip":
                for role in user.roles[1:]:  
                    try:
                        await user.remove_roles(role, reason=f"Protection: {reason}")
                    except:
                        pass
                restricted_role = await self.ensure_restricted_role(guild)
                await user.add_roles(restricted_role, reason=f"Protection: {reason}")
                await self.log_action(f" Stripped roles from {user.name} ({user.id}) for {reason}")

            if roles_removed:
                await self.log_action(f"Removed dangerous roles from {user.name} ({user.id})")

        except Exception as e:
            await self.log_action(f" Failed to punish {user.name} ({user.id}): {str(e)}", color=0xFF0000)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        if user.id in self.hard_banned_users:
            try:
                await guild.ban(user, reason="Hard ban enforcement")
            except:
                pass

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        if not self.detection_enabled:
            return
            
        try:
            async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create):
                if entry.user.id not in self.whitelist and entry.user.id != self.owner_id:
                    try:
                        await channel.delete()
                        await self.punish_user(entry.user, channel.guild, "unauthorized channel creation")
                    except:
                        pass
                break
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        if not self.detection_enabled:
            return
            
        try:
            async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
                if entry.user.id not in self.whitelist and entry.user.id != self.owner_id:
                    try:
                        new_channel = await channel.clone()
                        await new_channel.edit(position=channel.position)
                        await self.punish_user(entry.user, channel.guild, "unauthorized channel deletion")
                    except:
                        pass
                break
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        if not self.detection_enabled:
            return
            
        try:
            async for entry in role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_create):
                if entry.user.id not in self.whitelist and entry.user.id != self.owner_id:
                    try:
                        await role.delete()
                        await self.punish_user(entry.user, role.guild, "unauthorized role creation")
                    except:
                        pass
                break
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        if not self.detection_enabled:
            return
            
        try:
            async for entry in role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete):
                if entry.user.id not in self.whitelist and entry.user.id != self.owner_id:
                    try:
                        new_role = await role.guild.create_role(
                            name=role.name,
                            permissions=role.permissions,
                            colour=role.colour,
                            hoist=role.hoist,
                            mentionable=role.mentionable
                        )
                        await self.punish_user(entry.user, role.guild, "unauthorized role deletion")
                    except:
                        pass
                break
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        if not self.detection_enabled:
            return
            
        try:
            async for entry in after.audit_logs(limit=1, action=discord.AuditLogAction.guild_update):
                if entry.user.id not in self.whitelist and entry.user.id != self.owner_id:
                    try:
                        if before.name != after.name:
                            await after.edit(name=before.name)
                        if before.icon != after.icon:
                            await after.edit(icon=before.icon)
                        if before.banner != after.banner:
                            await after.edit(banner=before.banner)
                        if before.vanity_url_code != after.vanity_url_code:
                            await after.edit(vanity_code=before.vanity_url_code)
                        await self.punish_user(entry.user, after, "unauthorized server changes")
                    except:
                        pass
                break
        except:
            pass

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        if not self.detection_enabled:
            return
            
        try:
            async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
                if entry.user.id not in self.whitelist and entry.user.id != self.owner_id:
                    try:
                        await guild.unban(user)
                        await self.punish_user(entry.user, guild, "unauthorized ban")
                    except:
                        pass
                break
        except:
            pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if not self.detection_enabled:
            return
            
        try:
            async for entry in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
                if entry.user.id not in self.whitelist and entry.user.id != self.owner_id:
                    try:
                        await self.punish_user(entry.user, member.guild, "unauthorized kick")
                    except:
                        pass
                break
        except:
            pass

    @commands.Cog.listener() 
    async def on_message(self, message):
        if not self.detection_enabled:
            return

        if message.author.id in self.whitelist or message.author.id == self.owner_id:
            return

        try:
            if message.mention_everyone:
                try:
                    await message.delete()
                    await self.punish_user(message.author, message.guild, "unauthorized mention")
                except:
                    pass

            if len(message.mentions) > 5:
                try:
                    await message.delete()
                    await self.punish_user(message.author, message.guild, "mass mentions")
                except:
                    pass
        except:
            pass

    @commands.command()
    async def detection(self, ctx, state: str = None):
        if ctx.author.id != self.owner_id:
            return await ctx.send("```You are not authorized to use this command.```")
        
        if state is None:
            self.detection_enabled = not self.detection_enabled
        else:
            self.detection_enabled = state.lower() == 'on'
        
        await ctx.send(f"```Raid detection is now {'enabled' if self.detection_enabled else 'disabled'}.```")

    @commands.command()
    async def autoslow(self, ctx, seconds: int = None):
        if ctx.author.id != self.owner_id:
            return await ctx.send("```You are not authorized to use this command.```")
        
        self.autoslow_enabled = not self.autoslow_enabled if seconds is None else True
        self.slowmode_seconds = seconds or 30
        
        await ctx.send(f"```Auto slowmode is now {'enabled' if self.autoslow_enabled else 'disabled'}"
                      f"{f' with {self.slowmode_seconds} seconds' if self.autoslow_enabled else ''}```")

    @commands.command()
    async def noinvite(self, ctx):
        if ctx.author.id != self.owner_id:
            return await ctx.send("```You are not authorized to use this command.```")
        
        self.noinvite_enabled = not self.noinvite_enabled
        await ctx.send(f"```Invite blocking is now {'enabled' if self.noinvite_enabled else 'disabled'}.```")

def setup(bot):
    bot.add_cog(ServerProtection(bot))
