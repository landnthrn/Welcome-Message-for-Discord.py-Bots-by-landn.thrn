import random
import discord
from discord.ext import commands

# Channel where welcome messages are posted
WELCOME_CHANNEL_ID = 1398462946635419719

# Animated/static emojis used in the welcome message
# REPLACE THESE with your own server emojis or use standard Discord emojis below
WELCOME_EMOJIS = [
    "<a:139:1340167953639014400>",
    "<a:28:1339916429801029663>",
    "<a:130:1340119945127919677>",
    "<a:131:1340119946843127809>",
    "<a:132:1340119948202213460>",
    "<a:133:1340119989608251494>",
    "<a:134:1340120044675534948>",
    "<a:135:1340120046604652676>",
    "<a:136:1340120049721278464>",
    "<a:139:1340167953639014400>",
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

# Alternative: Use standard Discord emojis instead of custom ones
# Uncomment the line below and comment out the WELCOME_EMOJIS list above if you prefer standard emojis
# WELCOME_EMOJIS = ["🎉", "👋", "🎊", "✨", "🌟", "💫", "🔥", "💯", "🎯", "🚀", "💎", "⭐", "🎁", "🎈", "🎪", "🎨", "🎭", "🎪", "🎟️", "🎫"]


def generate_welcome_message(member: discord.Member, member_count: int) -> str:
    """Generate a welcome message with random animated emojis and a member mention."""
    # Select two different random emojis for the message
    emoji1, emoji2 = random.sample(WELCOME_EMOJIS, 2)
    
    # Generate the welcome message with the selected emojis and @ mention
    # REPLACE YOURSERVERNAME with your server name
    # REPLACE princess with your preferred member title (e.g., "homie", "member", "player")
    welcome_message = f"# {emoji1} What up {member.mention} {emoji1}\n**{emoji2} Welcome to YOURSERVERNAME!! You are the {member_count}th princess to join** {emoji2}"
    
    return welcome_message


class WelcomeMessageCog(commands.Cog):
    """Posts a styled welcome message in a specific channel when a member joins."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        try:
            channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
            if not channel:
                # Fallback attempt to fetch by ID (in case cache missed it)
                try:
                    channel = await self.bot.fetch_channel(WELCOME_CHANNEL_ID)
                except Exception:
                    channel = None

            if channel:
                member_count = member.guild.member_count
                message = generate_welcome_message(member, member_count)
                # Only mention the joining user; suppress notifications for everyone else
                allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, users=[member])
                await channel.send(
                    message,
                    allowed_mentions=allowed_mentions,
                    silent=True
                )
                print(f"✅ Sent channel welcome message for {member.name} to welcome channel ({WELCOME_CHANNEL_ID})")
            else:
                print(f"❌ Welcome channel with ID {WELCOME_CHANNEL_ID} not found")
        except Exception as e:
            print(f"❌ Error sending channel welcome message for {member.name}: {e}")


async def setup(bot: commands.Bot):
    """Extension entrypoint for bot.load_extension (discord.py 2.x)."""
    await bot.add_cog(WelcomeMessageCog(bot))


# Alternative implementation for bots that don't use Cogs
class WelcomeMessageBot(commands.Bot):
    """Standalone bot class for welcome messages (alternative to Cog implementation)."""
    
    def __init__(self, command_prefix="!", intents=None):
        if intents is None:
            intents = discord.Intents.default()
            intents.members = True  # Required for on_member_join event
        
        super().__init__(command_prefix=command_prefix, intents=intents)
    
    async def on_ready(self):
        print(f"✅ {self.user} is online and ready!")
        print(f"🤖 Welcome message system active for channel: {WELCOME_CHANNEL_ID}")
        print(f"📧 Server: YOURSERVERNAME")
        print(f"👥 Member title: princess")
        print(f"😀 Emojis available: {len(WELCOME_EMOJIS)}")
    
    async def on_member_join(self, member: discord.Member):
        try:
            channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
            if not channel:
                # Fallback attempt to fetch by ID (in case cache missed it)
                try:
                    channel = await self.fetch_channel(WELCOME_CHANNEL_ID)
                except Exception:
                    channel = None

            if channel:
                member_count = member.guild.member_count
                message = generate_welcome_message(member, member_count)
                # Only mention the joining user; suppress notifications for everyone else
                allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, users=[member])
                await channel.send(
                    message,
                    allowed_mentions=allowed_mentions,
                    silent=True
                )
                print(f"✅ Sent channel welcome message for {member.name} to welcome channel ({WELCOME_CHANNEL_ID})")
            else:
                print(f"❌ Welcome channel with ID {WELCOME_CHANNEL_ID} not found")
        except Exception as e:
            print(f"❌ Error sending channel welcome message for {member.name}: {e}")


# Manual integration example (for users who want to copy specific functions)
async def send_welcome_message_manual(bot: commands.Bot, member: discord.Member, channel_id: int):
    """Manual function to send welcome message (for integration into existing bots)."""
    try:
        channel = bot.get_channel(channel_id)
        if not channel:
            channel = await bot.fetch_channel(channel_id)
        
        if channel:
            member_count = member.guild.member_count
            message = generate_welcome_message(member, member_count)
            allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, users=[member])
            await channel.send(message, allowed_mentions=allowed_mentions, silent=True)
            print(f"✅ Sent manual welcome message for {member.name}")
        else:
            print(f"❌ Channel with ID {channel_id} not found")
    except Exception as e:
        print(f"❌ Error sending manual welcome message: {e}")

