@echo off
REM This script creates a Python file that will update all your files
REM Run this to generate the update script, then run the update script

echo Creating file updater...

(
echo import os
echo from pathlib import Path
echo.
echo print("Updating discord_bot/bot.py with fixed intents...")
echo.
echo # The fixed bot.py content will be inserted here
echo # This is a placeholder - the actual update will be done manually
echo.
echo print("✅ To complete the update:")
echo print("1. Open discord_bot/bot.py in Notepad")
echo print("2. Find line 62-68 ^(the __init__ function^)")
echo print("3. Make sure these lines exist:")
echo print("   intents.message_content = True")
echo print("   intents.members = True")
echo print("   intents.presences = True")
echo print^("")
echo print("4. Save the file")
echo print("5. Run: python discord_bot\\bot.py")
) > check_files.py

echo.
echo ✓ Created check_files.py
echo.
echo Run: python check_files.py
echo.
pause
