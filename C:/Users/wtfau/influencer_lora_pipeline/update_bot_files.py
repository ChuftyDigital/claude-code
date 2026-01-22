"""
Update Bot Files - Ensures all files match repository
Run this to update your local files with the latest versions
"""

import os
from pathlib import Path

print("=" * 70)
print("UPDATING BOT FILES")
print("=" * 70)
print()

base_dir = Path(__file__).parent

# Update discord_bot/bot.py with correct intents
bot_file = base_dir / "discord_bot" / "bot.py"

print(f"Checking: {bot_file}")

if bot_file.exists():
    with open(bot_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if the fix is already applied
    if 'intents.members = True' in content and 'intents.presences = True' in content:
        print("✅ bot.py already has the correct intents!")
    else:
        print("❌ bot.py needs to be updated!")
        print()
        print("PLEASE UPDATE MANUALLY:")
        print("1. Open: discord_bot/bot.py in Notepad")
        print("2. Find the __init__ function (around line 62)")
        print("3. Make sure it has these lines:")
        print()
        print("    def __init__(self):")
        print("        intents = discord.Intents.default()")
        print("        intents.message_content = True")
        print("        intents.members = True           # ← ADD THIS LINE")
        print("        intents.presences = True         # ← ADD THIS LINE")
        print()
        print("4. Save and run: python discord_bot\\bot.py")
else:
    print(f"❌ File not found: {bot_file}")
    print("   The bot.py file is missing!")

print()
print("=" * 70)
print()

# Check other critical files
print("Checking other critical files:")
print("-" * 70)

files_to_check = [
    "orchestrator/persona_manager.py",
    "orchestrator/ghl_integration.py",
    "orchestrator/llm_router.py",
    "agents/news_agents.py",
]

for file_path in files_to_check:
    full_path = base_dir / file_path
    if full_path.exists():
        size = full_path.stat().st_size
        print(f"✓ {file_path:40} ({size:,} bytes)")
    else:
        print(f"✗ {file_path:40} MISSING!")

print()
print("=" * 70)
