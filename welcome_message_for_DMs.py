import discord
from discord.ext import commands
import asyncio
import random

class WelcomeMessageForDMs(commands.Cog):
    """
    A Discord bot cog that sends welcome messages to new members via DM.
    
    Features:
    - Sends welcome message after configurable delay (default: 40 seconds)
    - Checks if member is still in server before sending
    - Handles DM permission errors gracefully
    - Customizable welcome message with emojis
    - Random emoji selection for variety
    - Multiple implementation options
    """
    
    def __init__(self, bot):
        self.bot = bot
        self.loop = bot.loop
        
        # Customize these values for your server
        self.server_name = "YOUR SERVER NAME"  # Change this to your server name
        self.member_title = "homie"      # Change this to your preferred member title
        
        # Default welcome message template, feel free to customize it or add your server emoji markdowns to it
        self.welcome_message = (
            "<a:Siren2:1394591500008034397> **What up @{member_name} welcome to {server_name}!!**\n"
            "We hope you have a grand time in our cozy server!! <a:140:1340167954901241896>\n"
            "Let the {member_title}s welcome ya in and start enjoying your space here"
        )
        
        # Delay before sending welcome message (in seconds)
        self.welcome_delay = 40
        
        # Custom emojis used in the welcome message
        # REPLACE THESE with your own server's emojis or remove them
        self.welcome_emojis = [
            "<a:Siren2:1394591500008034397>",
            "<a:140:1340167954901241896>",
            "<a:131:1340119946843127809>",
            "<a:139:1340167953639014400>",
            "<a:28:1339916429801029663>",
            "<a:130:1340119945127919677>",
            "<a:132:1340119948202213460>",
            "<a:133:1340119989608251494>",
            "<a:134:1340120044675534948>",
            "<a:135:1340120046604652676>",
            "<a:136:1340120049721278464>",
            "<a:141:1340167957665419264>",
            "<a:143:1340167963508211813>",
            "<a:142:1340167961188630548>",
            "<a:146:1340168083536482394>",
            "<a:122:1340119816761249812>",
            "<a:75:1340074791020920853>",
            "<a:1008693015667294239:1392435737999179889>",
            "<a:133:1340119994293555230>",
            "<a:147:1340168085067403380>",
            "<a:76:1340074793105358929>",
            "<a:emoji_169:1391999962677641216>",
            "<a:rainbowfire:1383254800308637807>",
            "<a:Wiz_double_smoke_pack:1355457689714430023>",
            "<:42:1339916582956175403>",
            "<:52:1340071964240252970>",
            "<a:112:1340119597159813233>",
            "<:2_:1339916018906038272>",
            "<:5_:1339916048224358420>",
            "<:98:1340119401093005312>",
            "<a:90:1340074886617497672>"
        ]
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Send welcome message to new members after specified delay"""
        async def send_welcome_message():
            # Wait for the specified delay before sending the message
            await asyncio.sleep(self.welcome_delay)
            
            # Check if the member is still in the server
            try:
                # Try to fetch the member to see if they're still in the server
                await member.guild.fetch_member(member.id)
                
                # Generate the welcome message with the member's name and random emojis
                welcome_message = self.generate_welcome_message(member.name)
                
                try:
                    await member.send(welcome_message)
                    print(f"✅ Sent welcome DM to {member.name}")
                except discord.Forbidden:
                    print(f"❌ Cannot send DM to {member.name} - DMs are closed")
                except Exception as e:
                    print(f"❌ Error sending welcome message to {member.name}: {e}")
                    
            except discord.NotFound:
                # Member left the server before we could send the message
                print(f"ℹ️ Member {member.name} left the server before welcome message could be sent")
            except Exception as e:
                print(f"❌ Error checking if member {member.name} is still in server: {e}")
        
        # Start the welcome message task
        self.loop.create_task(send_welcome_message())
    
    def generate_welcome_message(self, member_name: str) -> str:
        """Generate a welcome message with random emojis"""
        # Select random emojis for variety
        emoji1 = random.choice(self.welcome_emojis)
        emoji2 = random.choice(self.welcome_emojis)
        emoji3 = random.choice(self.welcome_emojis)
        
        # Generate the welcome message with random emojis
        welcome_message = (
            f"{emoji1} **What up @{member_name} welcome to {self.server_name}!!** {emoji1}\n"
            f"We hope you have a grand time in our cozy server!! {emoji2}\n"
            f"Let the {self.member_title}s welcome ya in and start enjoying your space here {emoji3}"
        )
        
        return welcome_message
    
    def set_welcome_message(self, message: str):
        """Set a custom welcome message template"""
        self.welcome_message = message
        print("✅ Welcome message template updated successfully!")
    
    def set_welcome_delay(self, delay: int):
        """Set the delay before sending welcome message (in seconds)"""
        if delay < 0:
            print("❌ Delay cannot be negative!")
            return
        self.welcome_delay = delay
        print(f"✅ Welcome delay updated to {delay} seconds!")
    
    def set_server_name(self, name: str):
        """Set the server name used in welcome messages"""
        self.server_name = name
        print(f"✅ Server name updated to: {name}")
    
    def set_member_title(self, title: str):
        """Set the member title used in welcome messages (e.g., 'homie', 'member', 'player')"""
        self.member_title = title
        print(f"✅ Member title updated to: {title}")
    
    def add_emoji(self, emoji: str):
        """Add a custom emoji to the welcome message emoji list"""
        if emoji not in self.welcome_emojis:
            self.welcome_emojis.append(emoji)
            print(f"✅ Added emoji: {emoji}")
        else:
            print(f"ℹ️ Emoji already exists in the list")
    
    def remove_emoji(self, emoji: str):
        """Remove an emoji from the welcome message emoji list"""
        if emoji in self.welcome_emojis:
            self.welcome_emojis.remove(emoji)
            print(f"✅ Removed emoji: {emoji}")
        else:
            print(f"ℹ️ Emoji not found in the list")
    
    def get_welcome_message(self) -> str:
        """Get the current welcome message template"""
        return self.welcome_message
    
    def get_welcome_delay(self) -> int:
        """Get the current welcome delay"""
        return self.welcome_delay
    
    def get_server_name(self) -> str:
        """Get the current server name"""
        return self.server_name
    
    def get_member_title(self) -> str:
        """Get the current member title"""
        return self.member_title
    
    def get_emoji_count(self) -> int:
        """Get the number of emojis in the list"""
        return len(self.welcome_emojis)
    
    def list_emojis(self) -> list:
        """Get a list of all current emojis"""
        return self.welcome_emojis.copy()

# ALTERNATIVE IMPLEMENTATION FOR BOTS THAT DON'T USE COGS
class WelcomeMessageForDMsBot(commands.Bot):
    """Standalone bot class for DM welcome messages (alternative to Cog implementation)."""
    
    def __init__(self, command_prefix="!", intents=None):
        if intents is None:
            intents = discord.Intents.default()
            intents.members = True  # Required for on_member_join event
        
        super().__init__(command_prefix=command_prefix, intents=intents)
        
        # Initialize welcome message settings
        self.server_name = "YOUR SERVER NAME" # Change this to your server name
        self.member_title = "homie" # Change this to your preferred member title
        self.welcome_delay = 40
        
        # REPLACE THESE with your own server's emojis or remove them
        self.welcome_emojis = [
            "<a:Siren2:1394591500008034397>",
            "<a:140:1340167954901241896>",
            "<a:131:1340119946843127809>",
            "<a:139:1340167953639014400>",
            "<a:28:1339916429801029663>",
            "<a:130:1340119945127919677>",
            "<a:132:1340119948202213460>",
            "<a:133:1340119989608251494>",
            "<a:134:1340120044675534948>",
            "<a:135:1340120046604652676>",
            "<a:136:1340120049721278464>",
            "<a:141:1340167957665419264>",
            "<a:143:1340167963508211813>",
            "<a:142:1340167961188630548>",
            "<a:146:1340168083536482394>",
            "<a:122:1340119816761249812>",
            "<a:75:1340074791020920853>",
            "<a:1008693015667294239:1392435737999179889>",
            "<a:133:1340119994293555230>",
            "<a:147:1340168085067403380>",
            "<a:76:1340074793105358929>",
            "<a:emoji_169:1391999962677641216>",
            "<a:rainbowfire:1383254800308637807>",
            "<a:Wiz_double_smoke_pack:1355457689714430023>",
            "<:42:1339916582956175403>",
            "<:52:1340071964240252970>",
            "<a:112:1340119597159813233>",
            "<:2_:1339916018906038272>",
            "<:5_:1339916048224358420>",
            "<:98:1340119401093005312>",
            "<a:90:1340074886617497672>"
        ]
    
    async def on_ready(self):
        print(f"✅ {self.user} is online and ready!")
        print(f"🤖 DM Welcome message system active!")
        print(f"📧 Server: {self.server_name}")
        print(f"👥 Member title: {self.member_title}")
        print(f"⏱️ Welcome delay: {self.welcome_delay} seconds")
        print(f"😀 Emojis available: {len(self.welcome_emojis)}")
    
    async def on_member_join(self, member):
        """Send welcome message to new members after specified delay"""
        async def send_welcome_message():
            # Wait for the specified delay before sending the message
            await asyncio.sleep(self.welcome_delay)
            
            # Check if the member is still in the server
            try:
                # Try to fetch the member to see if they're still in the server
                await member.guild.fetch_member(member.id)
                
                # Generate the welcome message with the member's name and random emojis
                welcome_message = self.generate_welcome_message(member.name)
                
                try:
                    await member.send(welcome_message)
                    print(f"✅ Sent welcome DM to {member.name}")
                except discord.Forbidden:
                    print(f"❌ Cannot send DM to {member.name} - DMs are closed")
                except Exception as e:
                    print(f"❌ Error sending welcome message to {member.name}: {e}")
                    
            except discord.NotFound:
                # Member left the server before we could send the message
                print(f"ℹ️ Member {member.name} left the server before welcome message could be sent")
            except Exception as e:
                print(f"❌ Error checking if member {member.name} is still in server: {e}")
        
        # Start the welcome message task
        self.loop.create_task(send_welcome_message())
    
    def generate_welcome_message(self, member_name: str) -> str:
        """Generate a welcome message with random emojis"""
        # Select random emojis for variety
        emoji1 = random.choice(self.welcome_emojis)
        emoji2 = random.choice(self.welcome_emojis)
        emoji3 = random.choice(self.welcome_emojis)
        
        # Generate the welcome message with random emojis
        welcome_message = (
            f"{emoji1} **What up @{member_name} welcome to {self.server_name}!!** {emoji1}\n"
            f"We hope you have a grand time in our cozy server!! {emoji2}\n"
            f"Let the {self.member_title}s welcome ya in and start enjoying your space here {emoji3}"
        )
        
        return welcome_message


async def setup(bot):
    """Add the cog to the bot"""
    await bot.add_cog(WelcomeMessageForDMs(bot))

