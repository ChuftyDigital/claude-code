"""
Discord Bot Setup Script
========================
Run this to verify your Discord bot setup.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

print("\n" + "="*70)
print("DISCORD BOT SETUP VERIFICATION")
print("="*70)

# Load environment
load_dotenv()

print("\n1. Checking environment variables...")

DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
GUILD_ID = os.getenv("DISCORD_GUILD_ID", "")

if not DISCORD_TOKEN:
    print("❌ DISCORD_BOT_TOKEN not found in .env")
    print("\nTo fix:")
    print("1. Go to https://discord.com/developers/applications")
    print("2. Select your application")
    print("3. Go to 'Bot' section")
    print("4. Copy the token")
    print("5. Add to .env file:")
    print("   DISCORD_BOT_TOKEN=your_token_here")
    sys.exit(1)
else:
    print(f"✅ DISCORD_BOT_TOKEN found ({DISCORD_TOKEN[:20]}...)")

if not GUILD_ID:
    print("⚠️  DISCORD_GUILD_ID not set (optional but recommended)")
    print("\nTo add (for faster command sync):")
    print("1. Enable Developer Mode in Discord (Settings → Advanced)")
    print("2. Right-click your server → Copy ID")
    print("3. Add to .env:")
    print("   DISCORD_GUILD_ID=your_server_id")
else:
    print(f"✅ DISCORD_GUILD_ID found ({GUILD_ID})")

print("\n2. Checking dependencies...")

try:
    import discord
    print(f"✅ discord.py installed (version {discord.__version__})")
except ImportError:
    print("❌ discord.py not installed")
    print("\nTo fix:")
    print("   pip install discord.py")
    sys.exit(1)

try:
    import yaml
    print("✅ pyyaml installed")
except ImportError:
    print("⚠️  pyyaml not installed")
    print("   pip install pyyaml")

print("\n3. Checking persona configurations...")

personas_dir = Path("./personas")
if not personas_dir.exists():
    print(f"❌ Personas directory not found: {personas_dir}")
    sys.exit(1)

persona_count = 0
for persona_dir in personas_dir.iterdir():
    if persona_dir.is_dir():
        config_file = persona_dir / "persona_config.yaml"
        if config_file.exists():
            persona_count += 1
            print(f"✅ Found: {persona_dir.name}")

if persona_count == 0:
    print("❌ No persona configurations found")
    sys.exit(1)

print(f"\n✅ Total personas found: {persona_count}")

print("\n4. Checking API keys for chat commands...")

anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
xai_key = os.getenv("XAI_API_KEY", "")
openai_key = os.getenv("OPENAI_API_KEY", "")

chat_available = False

if anthropic_key:
    print("✅ Anthropic API key found (Claude)")
    chat_available = True
if xai_key:
    print("✅ xAI API key found (Grok)")
    chat_available = True
if openai_key:
    print("✅ OpenAI API key found (ChatGPT)")
    chat_available = True

if not chat_available:
    print("⚠️  No LLM API keys found")
    print("   Chat commands will not work without at least one API key")
    print("   Add to .env: ANTHROPIC_API_KEY or XAI_API_KEY or OPENAI_API_KEY")

print("\n5. Checking GHL integration...")

ghl_api = os.getenv("GHL_API_KEY", "")
ghl_location = os.getenv("GHL_LOCATION_ID", "")

if ghl_api and ghl_location:
    print("✅ GHL configured (CRM commands available)")
elif ghl_api or ghl_location:
    print("⚠️  GHL partially configured")
    print("   Need both GHL_API_KEY and GHL_LOCATION_ID")
else:
    print("⚠️  GHL not configured (optional)")
    print("   CRM commands will not be available")

print("\n" + "="*70)
print("SETUP SUMMARY")
print("="*70)

if DISCORD_TOKEN and persona_count > 0:
    print("\n✅ READY TO START BOT!")
    print("\nTo start the bot:")
    print("   python discord_bot/bot.py")
    print("\nBot will sync commands automatically.")
    print("In Discord, type /help to see all available commands.")
else:
    print("\n❌ SETUP INCOMPLETE")
    print("\nFix the issues above and run this script again.")

print("\n" + "="*70 + "\n")
