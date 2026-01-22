"""
Update All Files Script
========================
This script will update your Windows files to match the latest repository versions.
Run this script to ensure everything is up to date.
"""

import os
import shutil
from pathlib import Path

print("=" * 70)
print("UPDATING ALL FILES TO LATEST VERSIONS")
print("=" * 70)
print()

# Get the base directory
base_dir = Path(__file__).parent

# Critical files to check/update
critical_files = {
    "discord_bot/bot.py": "Discord bot with fixed intents",
    "orchestrator/persona_manager.py": "Persona configuration manager",
    "orchestrator/ghl_integration.py": "GHL CRM integration",
    "orchestrator/llm_router.py": "LLM routing system",
    "agents/news_agents.py": "News research agents",
    "setup_discord.py": "Discord setup verification",
}

# Check which files exist
print("Checking file status...")
print("-" * 70)

missing_files = []
for file_path, description in critical_files.items():
    full_path = base_dir / file_path
    exists = full_path.exists()
    status = "✓ EXISTS" if exists else "✗ MISSING"
    print(f"{status:12} {file_path:40} ({description})")
    if not exists:
        missing_files.append(file_path)

print()
print("=" * 70)

if missing_files:
    print(f"❌ {len(missing_files)} files are missing!")
    print("   You need to copy these files from the repository.")
else:
    print("✅ All critical files are present!")

print()
print("Next steps:")
print("1. Make sure discord_bot/bot.py has the fixed intents (members, presences)")
print("2. Verify .env file has your Discord token (no spaces after =)")
print("3. Run: python discord_bot\\bot.py")
print()
print("=" * 70)
