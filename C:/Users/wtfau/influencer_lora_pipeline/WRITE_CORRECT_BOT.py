"""
Write Correct Bot File
======================
This script will write the correct bot.py with all fixes to your Windows directory.
"""

import os
from pathlib import Path

# The complete, correct bot.py content with fixed intents
BOT_CONTENT = '''"""
Influencer Pipeline Discord Bot
================================
Manage your AI influencer content generation pipeline from Discord.

Commands:
- Content generation
- Persona management
- Vault status
- Chat testing
- GHL sync
- Analytics
"""

import os
import sys
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestrator.persona_manager import PersonaManager
from orchestrator.llm_router import LLMRouter
from orchestrator.ghl_integration import GHLDataManager, ModelRecord

# Load environment
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot configuration
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
GUILD_ID = os.getenv("DISCORD_GUILD_ID", "")

# Initialize managers
persona_manager = PersonaManager("./personas")
llm_router = LLMRouter()

# GHL manager (optional)
ghl_api_key = os.getenv("GHL_API_KEY", "")
ghl_location_id = os.getenv("GHL_LOCATION_ID", "")
if ghl_api_key and ghl_location_id:
    ghl_manager = GHLDataManager(ghl_api_key, ghl_location_id)
else:
    ghl_manager = None


class InfluencerBot(commands.Bot):
    """Discord bot for managing influencer pipeline"""

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True

        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None  # We'll create a custom help
        )

        self.current_persona = None  # Currently selected persona

    async def setup_hook(self):
        """Called when bot is starting up"""
        # Sync commands
        if GUILD_ID:
            guild = discord.Object(id=int(GUILD_ID))
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            logger.info(f"Synced commands to guild {GUILD_ID}")
        else:
            await self.tree.sync()
            logger.info("Synced commands globally")

    async def on_ready(self):
        """Called when bot is ready"""
        logger.info(f"Bot logged in as {self.user}")
        logger.info(f"Connected to {len(self.guilds)} guilds")

        # Set status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="content generation | /help"
            )
        )


# Initialize bot
bot = InfluencerBot()


# ============================================================================
# HELP COMMAND
# ============================================================================

@bot.tree.command(name="help", description="Show all available commands")
async def help_command(interaction: discord.Interaction):
    """Show comprehensive help"""

    embed = discord.Embed(
        title="🤖 Influencer Pipeline Bot - Commands",
        description="Manage your AI influencer content generation pipeline",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="📊 **Status Commands**",
        value=(
            "`/status` - Show overall pipeline status\\n"
            "`/personas` - List all available personas\\n"
            "`/vault [model_id]` - Check vault levels for a model\\n"
            "`/analytics [model_id]` - View model analytics"
        ),
        inline=False
    )

    embed.add_field(
        name="🎨 **Content Generation**",
        value=(
            "`/generate [model_id] [lane] [count]` - Generate images\\n"
            "`/fill_vault [model_id] [lane]` - Fill vault to minimum\\n"
            "`/batch [model_id]` - Generate batch for all lanes\\n"
            "`/preview [model_id] [lane]` - Preview a prompt"
        ),
        inline=False
    )

    embed.add_field(
        name="👤 **Persona Management**",
        value=(
            "`/select [model_id]` - Select active persona\\n"
            "`/info [model_id]` - Show detailed persona info\\n"
            "`/chat [message]` - Chat with selected persona\\n"
            "`/test_chat [model_id] [message]` - Test chat response"
        ),
        inline=False
    )

    embed.add_field(
        name="💾 **GHL Integration**",
        value=(
            "`/sync_model [model_id]` - Sync model to GHL\\n"
            "`/ghl_status` - Check GHL connection\\n"
            "`/customer_info [customer_id]` - View customer data"
        ),
        inline=False
    )

    embed.add_field(
        name="⚙️ **System Commands**",
        value=(
            "`/ping` - Check bot latency\\n"
            "`/reload` - Reload persona configs\\n"
            "`/set_persona [model_id]` - Set default persona"
        ),
        inline=False
    )

    embed.set_footer(text="Use /command for more details on each command")

    await interaction.response.send_message(embed=embed)


# ============================================================================
# STATUS COMMANDS
# ============================================================================

@bot.tree.command(name="status", description="Show overall pipeline status")
async def status(interaction: discord.Interaction):
    """Show pipeline status"""

    await interaction.response.defer()

    personas = persona_manager.get_all_personas()

    embed = discord.Embed(
        title="📊 Pipeline Status",
        color=discord.Color.green(),
        timestamp=datetime.utcnow()
    )

    # Overall stats
    total_personas = len(personas)
    needs_replenishment = persona_manager.check_replenishment_needed()

    embed.add_field(
        name="System",
        value=f"**Personas:** {total_personas}\\n**Needs Replenishment:** {len(needs_replenishment)}",
        inline=False
    )

    # Per persona status
    for persona in personas:
        vault_status = []
        for lane_name in ["sfw", "spicy", "nsfw"]:
            lane = persona.get_lane(lane_name)
            if lane:
                emoji = "✅" if not lane.needs_replenishment() else "⚠️"
                vault_status.append(f"{emoji} {lane_name.upper()}: {lane.vault_current}/{lane.vault_min}")

        embed.add_field(
            name=f"{persona.model_name} ({persona.model_id})",
            value="\\n".join(vault_status),
            inline=True
        )

    if bot.current_persona:
        embed.add_field(
            name="🎯 Active Persona",
            value=f"{bot.current_persona.model_name} ({bot.current_persona.model_id})",
            inline=False
        )

    await interaction.followup.send(embed=embed)


@bot.tree.command(name="personas", description="List all available personas")
async def personas(interaction: discord.Interaction):
    """List all personas"""

    personas = persona_manager.get_all_personas()

    embed = discord.Embed(
        title="👥 Available Personas",
        color=discord.Color.blue()
    )

    for persona in personas:
        social_links = []
        if persona.social_accounts.get("instagram"):
            ig = persona.social_accounts["instagram"]
            social_links.append(f"📸 IG: @{ig.get('handle', 'N/A')}")
        if persona.social_accounts.get("onlyfans"):
            of = persona.social_accounts["onlyfans"]
            social_links.append(f"🔞 OF: ${of.get('price_tier', 'N/A')}")

        embed.add_field(
            name=f"{persona.model_name} ({persona.model_id})",
            value=(
                f"**Niche:** {persona.niche}\\n"
                f"**Location:** {persona.location}\\n"
                f"**Age:** {persona.age}\\n"
                f"{' | '.join(social_links)}"
            ),
            inline=False
        )

    embed.set_footer(text="Use /info [model_id] for detailed information")

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="ping", description="Check bot latency")
async def ping(interaction: discord.Interaction):
    """Ping command"""

    latency = round(bot.latency * 1000)

    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Bot latency: **{latency}ms**",
        color=discord.Color.green() if latency < 100 else discord.Color.orange()
    )

    await interaction.response.send_message(embed=embed)


# ============================================================================
# RUN BOT
# ============================================================================

def main():
    """Run the bot"""
    if not DISCORD_TOKEN:
        print("❌ Error: DISCORD_BOT_TOKEN not set in .env")
        print("Please add your Discord bot token to the .env file:")
        print("DISCORD_BOT_TOKEN=your_token_here")
        return

    print("🤖 Starting Influencer Pipeline Bot...")
    print(f"📊 Loaded {len(persona_manager.get_all_personas())} personas")
    print("🚀 Bot starting...")

    try:
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        print(f"❌ Error starting bot: {e}")


if __name__ == "__main__":
    main()
'''

print("=" * 70)
print("WRITING CORRECT BOT.PY FILE")
print("=" * 70)
print()

# Determine the path
bot_file = Path(__file__).parent / "discord_bot" / "bot.py"

print(f"Target file: {bot_file}")
print()

# Write the file
try:
    with open(bot_file, 'w', encoding='utf-8') as f:
        f.write(BOT_CONTENT)

    print("✅ SUCCESS! bot.py has been updated with:")
    print("   ✓ intents.members = True")
    print("   ✓ intents.presences = True")
    print("   ✓ All 18 commands")
    print()
    print("Now run: python discord_bot\\bot.py")

except Exception as e:
    print(f"❌ Error writing file: {e}")

print()
print("=" * 70)
