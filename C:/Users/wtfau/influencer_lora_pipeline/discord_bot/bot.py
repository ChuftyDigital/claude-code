"""
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
            "`/status` - Show overall pipeline status\n"
            "`/personas` - List all available personas\n"
            "`/vault [model_id]` - Check vault levels for a model\n"
            "`/analytics [model_id]` - View model analytics"
        ),
        inline=False
    )

    embed.add_field(
        name="🎨 **Content Generation**",
        value=(
            "`/generate [model_id] [lane] [count]` - Generate images\n"
            "`/fill_vault [model_id] [lane]` - Fill vault to minimum\n"
            "`/batch [model_id]` - Generate batch for all lanes\n"
            "`/preview [model_id] [lane]` - Preview a prompt"
        ),
        inline=False
    )

    embed.add_field(
        name="👤 **Persona Management**",
        value=(
            "`/select [model_id]` - Select active persona\n"
            "`/info [model_id]` - Show detailed persona info\n"
            "`/chat [message]` - Chat with selected persona\n"
            "`/test_chat [model_id] [message]` - Test chat response"
        ),
        inline=False
    )

    embed.add_field(
        name="💾 **GHL Integration**",
        value=(
            "`/sync_model [model_id]` - Sync model to GHL\n"
            "`/ghl_status` - Check GHL connection\n"
            "`/customer_info [customer_id]` - View customer data"
        ),
        inline=False
    )

    embed.add_field(
        name="⚙️ **System Commands**",
        value=(
            "`/ping` - Check bot latency\n"
            "`/reload` - Reload persona configs\n"
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
        value=f"**Personas:** {total_personas}\n**Needs Replenishment:** {len(needs_replenishment)}",
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
            value="\n".join(vault_status),
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
                f"**Niche:** {persona.niche}\n"
                f"**Location:** {persona.location}\n"
                f"**Age:** {persona.age}\n"
                f"{' | '.join(social_links)}"
            ),
            inline=False
        )

    embed.set_footer(text="Use /info [model_id] for detailed information")

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="vault", description="Check vault levels for a model")
@app_commands.describe(model_id="Model ID (e.g., CDS001, LFX001)")
async def vault(interaction: discord.Interaction, model_id: str):
    """Check vault status"""

    persona = persona_manager.get_persona(model_id.upper())

    if not persona:
        await interaction.response.send_message(
            f"❌ Persona '{model_id}' not found. Use `/personas` to see available personas.",
            ephemeral=True
        )
        return

    embed = discord.Embed(
        title=f"📦 Vault Status - {persona.model_name}",
        color=discord.Color.gold()
    )

    for lane_name in ["sfw", "spicy", "nsfw"]:
        lane = persona.get_lane(lane_name)
        if lane:
            needs_replenishment = lane.needs_replenishment()
            emoji = "⚠️" if needs_replenishment else "✅"

            percentage = (lane.vault_current / lane.vault_max) * 100
            bar_length = 10
            filled = int(percentage / 10)
            bar = "█" * filled + "░" * (bar_length - filled)

            embed.add_field(
                name=f"{emoji} {lane_name.upper()} Lane",
                value=(
                    f"**Current:** {lane.vault_current}/{lane.vault_max}\n"
                    f"**Threshold:** {lane.replenishment_threshold}\n"
                    f"**Status:** {bar} {percentage:.0f}%\n"
                    f"**Platforms:** {', '.join(lane.platforms[:3])}"
                ),
                inline=False
            )

    embed.set_footer(text=f"Use /fill_vault {model_id} [lane] to replenish")

    await interaction.response.send_message(embed=embed)


# ============================================================================
# CONTENT GENERATION COMMANDS
# ============================================================================

@bot.tree.command(name="generate", description="Generate content for a model")
@app_commands.describe(
    model_id="Model ID (e.g., CDS001)",
    lane="Content lane (sfw, spicy, nsfw)",
    count="Number of images to generate (default: 1)"
)
async def generate(
    interaction: discord.Interaction,
    model_id: str,
    lane: str,
    count: int = 1
):
    """Generate content"""

    await interaction.response.defer()

    persona = persona_manager.get_persona(model_id.upper())
    if not persona:
        await interaction.followup.send(f"❌ Persona '{model_id}' not found.")
        return

    lane_config = persona.get_lane(lane.lower())
    if not lane_config:
        await interaction.followup.send(f"❌ Lane '{lane}' not found for {model_id}.")
        return

    if count < 1 or count > 10:
        await interaction.followup.send("❌ Count must be between 1 and 10.")
        return

    # Create status embed
    embed = discord.Embed(
        title=f"🎨 Generating Content",
        description=f"**Model:** {persona.model_name}\n**Lane:** {lane.upper()}\n**Count:** {count}",
        color=discord.Color.blue()
    )

    await interaction.followup.send(embed=embed)

    # Simulate generation (in real implementation, call your generator)
    for i in range(count):
        # Get random prompt
        base_prompt = lane_config.get_example_prompt()

        # Enhance prompt
        trigger = persona.get_lora_trigger_word(lane)
        enhanced = f"{trigger}, {base_prompt}"

        # Update status
        progress_embed = discord.Embed(
            title=f"🎨 Generating Image {i+1}/{count}",
            description=f"**Prompt:** {enhanced[:200]}...",
            color=discord.Color.orange()
        )

        await interaction.channel.send(embed=progress_embed)

        # Simulate generation time
        await asyncio.sleep(2)

    # Completion
    complete_embed = discord.Embed(
        title="✅ Generation Complete",
        description=f"Generated {count} images for {persona.model_name} ({lane.upper()} lane)",
        color=discord.Color.green()
    )

    await interaction.channel.send(embed=complete_embed)


@bot.tree.command(name="preview", description="Preview a generated prompt")
@app_commands.describe(
    model_id="Model ID",
    lane="Content lane"
)
async def preview(interaction: discord.Interaction, model_id: str, lane: str):
    """Preview a prompt"""

    persona = persona_manager.get_persona(model_id.upper())
    if not persona:
        await interaction.response.send_message(f"❌ Persona '{model_id}' not found.", ephemeral=True)
        return

    lane_config = persona.get_lane(lane.lower())
    if not lane_config:
        await interaction.response.send_message(f"❌ Lane '{lane}' not found.", ephemeral=True)
        return

    # Get example prompt
    base_prompt = lane_config.get_example_prompt()
    trigger = persona.get_lora_trigger_word(lane)

    embed = discord.Embed(
        title=f"👁️ Prompt Preview - {persona.model_name}",
        color=discord.Color.purple()
    )

    embed.add_field(
        name="Lane",
        value=f"{lane.upper()} - {lane_config.description}",
        inline=False
    )

    embed.add_field(
        name="LoRA Trigger",
        value=f"`{trigger}`",
        inline=False
    )

    embed.add_field(
        name="Base Prompt",
        value=base_prompt,
        inline=False
    )

    embed.add_field(
        name="Enhanced Prompt (Example)",
        value=f"{trigger}, {base_prompt}, {lane_config.quality_tags}",
        inline=False
    )

    embed.add_field(
        name="Negative Prompt",
        value=lane_config.negative_prompt,
        inline=False
    )

    embed.add_field(
        name="LLM",
        value=f"{lane_config.llm.upper()} ({lane_config.style})",
        inline=False
    )

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="fill_vault", description="Fill vault to minimum level")
@app_commands.describe(
    model_id="Model ID",
    lane="Content lane to fill"
)
async def fill_vault(interaction: discord.Interaction, model_id: str, lane: str):
    """Fill vault to minimum"""

    await interaction.response.defer()

    persona = persona_manager.get_persona(model_id.upper())
    if not persona:
        await interaction.followup.send(f"❌ Persona '{model_id}' not found.")
        return

    lane_config = persona.get_lane(lane.lower())
    if not lane_config:
        await interaction.followup.send(f"❌ Lane '{lane}' not found.")
        return

    # Calculate needed
    needed = max(0, lane_config.vault_min - lane_config.vault_current)

    if needed == 0:
        await interaction.followup.send(
            f"✅ Vault already at minimum level ({lane_config.vault_current}/{lane_config.vault_min})"
        )
        return

    # Estimate time
    avg_time_per_image = 8  # seconds
    estimated_time = (needed * avg_time_per_image) / 60

    embed = discord.Embed(
        title=f"🔄 Filling Vault - {persona.model_name}",
        description=(
            f"**Lane:** {lane.upper()}\n"
            f"**Current:** {lane_config.vault_current}\n"
            f"**Target:** {lane_config.vault_min}\n"
            f"**Needed:** {needed} images\n"
            f"**Estimated Time:** {estimated_time:.1f} minutes"
        ),
        color=discord.Color.orange()
    )

    await interaction.followup.send(embed=embed)
    await interaction.channel.send(f"🚀 Starting generation of {needed} images...")

    # In real implementation, call your batch generator here


# ============================================================================
# PERSONA COMMANDS
# ============================================================================

@bot.tree.command(name="select", description="Select active persona")
@app_commands.describe(model_id="Model ID to select")
async def select(interaction: discord.Interaction, model_id: str):
    """Select active persona"""

    persona = persona_manager.get_persona(model_id.upper())
    if not persona:
        await interaction.response.send_message(f"❌ Persona '{model_id}' not found.", ephemeral=True)
        return

    bot.current_persona = persona

    embed = discord.Embed(
        title=f"✅ Persona Selected",
        description=f"**{persona.model_name}** is now the active persona",
        color=discord.Color.green()
    )

    embed.set_thumbnail(url="https://via.placeholder.com/150")  # Replace with actual image

    embed.add_field(name="Niche", value=persona.niche, inline=True)
    embed.add_field(name="Location", value=persona.location, inline=True)
    embed.add_field(name="Chat Tone", value=persona.chat_tone, inline=True)

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="info", description="Show detailed persona information")
@app_commands.describe(model_id="Model ID")
async def info(interaction: discord.Interaction, model_id: str):
    """Show persona info"""

    persona = persona_manager.get_persona(model_id.upper())
    if not persona:
        await interaction.response.send_message(f"❌ Persona '{model_id}' not found.", ephemeral=True)
        return

    embed = discord.Embed(
        title=f"📋 {persona.model_name} ({persona.model_id})",
        description=persona.niche,
        color=discord.Color.blue()
    )

    # Basic info
    embed.add_field(
        name="📌 Basic Info",
        value=(
            f"**Age:** {persona.age}\n"
            f"**Heritage:** {persona.heritage}\n"
            f"**Location:** {persona.location}\n"
            f"**Height:** {persona.height_cm}cm"
        ),
        inline=True
    )

    # Physical
    embed.add_field(
        name="👤 Physical",
        value=(
            f"**Build:** {persona.build}\n"
            f"**Hair:** {persona.hair}\n"
            f"**Eyes:** {persona.eyes}\n"
            f"**Skin:** {persona.skin}"
        ),
        inline=True
    )

    # Personality
    embed.add_field(
        name="💫 Personality",
        value=f"{persona.personality_vibe}\n\n" + "\n".join([f"• {t}" for t in persona.personality_traits[:3]]),
        inline=False
    )

    # Hobbies
    if persona.hobbies:
        embed.add_field(
            name="🎯 Hobbies",
            value=" • " + "\n • ".join(persona.hobbies[:4]),
            inline=False
        )

    # Monetization
    if persona.monetization:
        of_info = persona.monetization.get("onlyfans", {})
        price = of_info.get("subscription_price", "N/A")
        embed.add_field(
            name="💰 Monetization",
            value=f"**OnlyFans:** ${price}/month\n**Chat:** {persona.chat_tone}",
            inline=False
        )

    # Brand
    embed.add_field(
        name="🎨 Brand Aesthetic",
        value=persona.brand_aesthetic,
        inline=False
    )

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="chat", description="Chat with selected persona")
@app_commands.describe(message="Your message")
async def chat(interaction: discord.Interaction, message: str):
    """Chat with persona"""

    if not bot.current_persona:
        await interaction.response.send_message(
            "❌ No persona selected. Use `/select [model_id]` first.",
            ephemeral=True
        )
        return

    await interaction.response.defer()

    persona = bot.current_persona

    # Create chat context
    chat_instruction = f"""You are {persona.model_name}, a {persona.age}yo {persona.heritage} woman.

Personality: {persona.personality_vibe}
Tone: {persona.chat_tone}
Topics you love: {', '.join(persona.chat_preferred_topics[:5])}

Respond to this message in character: "{message}"

Guidelines:
- Use one of these greetings if appropriate: {persona.chat_greetings[0] if persona.chat_greetings else 'Hey!'}
- Keep it natural and conversational
- Be flirty but not explicit
- Stay in character
- 2-3 sentences max
"""

    try:
        # Use LLM to generate response
        response = await llm_router.generate(
            messages=[{"role": "user", "content": chat_instruction}],
            llm="claude",
            max_tokens=200,
            temperature=0.9
        )

        if response:
            embed = discord.Embed(
                title=f"💬 {persona.model_name} says:",
                description=response,
                color=discord.Color.pink()
            )
            embed.set_footer(text=f"Chatting as {persona.model_id}")
        else:
            embed = discord.Embed(
                title="❌ Error",
                description="Failed to generate response. Check API keys.",
                color=discord.Color.red()
            )

        await interaction.followup.send(embed=embed)

    except Exception as e:
        await interaction.followup.send(f"❌ Error: {e}")


# ============================================================================
# GHL COMMANDS
# ============================================================================

@bot.tree.command(name="sync_model", description="Sync model to GHL")
@app_commands.describe(model_id="Model ID to sync")
async def sync_model(interaction: discord.Interaction, model_id: str):
    """Sync model to GHL"""

    if not ghl_manager:
        await interaction.response.send_message(
            "❌ GHL not configured. Set GHL_API_KEY and GHL_LOCATION_ID in .env",
            ephemeral=True
        )
        return

    await interaction.response.defer()

    persona = persona_manager.get_persona(model_id.upper())
    if not persona:
        await interaction.followup.send(f"❌ Persona '{model_id}' not found.")
        return

    # Create model record
    model_record = ModelRecord(
        model_id=persona.model_id,
        model_name=persona.model_name,
        niche=persona.niche,
        age=persona.age,
        location=persona.location,
        status="active",
        created_at=datetime.now().isoformat()
    )

    # Sync to GHL
    success = await ghl_manager.sync_model(model_record)

    if success:
        embed = discord.Embed(
            title="✅ Model Synced to GHL",
            description=f"{persona.model_name} has been synced to Go High Level CRM",
            color=discord.Color.green()
        )
    else:
        embed = discord.Embed(
            title="❌ Sync Failed",
            description="Failed to sync model. Check logs for details.",
            color=discord.Color.red()
        )

    await interaction.followup.send(embed=embed)


@bot.tree.command(name="ghl_status", description="Check GHL connection")
async def ghl_status(interaction: discord.Interaction):
    """Check GHL status"""

    if not ghl_manager:
        embed = discord.Embed(
            title="❌ GHL Not Configured",
            description="Set GHL_API_KEY and GHL_LOCATION_ID in your .env file",
            color=discord.Color.red()
        )
    else:
        embed = discord.Embed(
            title="✅ GHL Connected",
            description=f"Location ID: {ghl_location_id[:8]}...",
            color=discord.Color.green()
        )

    await interaction.response.send_message(embed=embed)


# ============================================================================
# SYSTEM COMMANDS
# ============================================================================

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


@bot.tree.command(name="reload", description="Reload persona configurations")
async def reload(interaction: discord.Interaction):
    """Reload personas"""

    await interaction.response.defer()

    global persona_manager
    persona_manager = PersonaManager("./personas")

    personas = persona_manager.get_all_personas()

    embed = discord.Embed(
        title="🔄 Personas Reloaded",
        description=f"Successfully reloaded {len(personas)} personas",
        color=discord.Color.green()
    )

    for persona in personas:
        embed.add_field(
            name=persona.model_id,
            value=persona.model_name,
            inline=True
        )

    await interaction.followup.send(embed=embed)


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
