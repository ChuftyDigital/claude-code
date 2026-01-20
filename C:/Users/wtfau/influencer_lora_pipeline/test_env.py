"""Test if .env file is loading correctly"""
import os
from pathlib import Path
from dotenv import load_dotenv

print("=" * 60)
print("Environment Variable Test")
print("=" * 60)

# Show current directory
print(f"\nCurrent directory: {os.getcwd()}")

# Show .env file location
env_path = Path(".env")
print(f".env file exists: {env_path.exists()}")
if env_path.exists():
    print(f".env file path: {env_path.absolute()}")
    print(f".env file size: {env_path.stat().st_size} bytes")

# Load .env
print("\nLoading .env file...")
load_dotenv()

# Check if token is loaded
token = os.getenv("DISCORD_BOT_TOKEN", "")
guild_id = os.getenv("DISCORD_GUILD_ID", "")

print(f"\nDISCORD_BOT_TOKEN loaded: {'YES ✓' if token else 'NO ✗'}")
if token:
    print(f"  Token starts with: {token[:20]}...")
    print(f"  Token length: {len(token)} characters")
else:
    print("  Token is empty or not found!")

print(f"\nDISCORD_GUILD_ID loaded: {'YES ✓' if guild_id else 'NO ✗'}")
if guild_id:
    print(f"  Guild ID: {guild_id}")

# Check if python-dotenv is working
try:
    import dotenv
    print(f"\npython-dotenv version: {dotenv.__version__}")
except:
    print("\n⚠️  python-dotenv not installed correctly!")

print("\n" + "=" * 60)
