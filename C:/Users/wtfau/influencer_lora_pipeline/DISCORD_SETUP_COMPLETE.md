# Complete Discord Bot Setup Guide

## Step 1: Create Discord Bot (5 minutes)

### 1.1 Create Application

1. Go to https://discord.com/developers/applications
2. Click **"New Application"**
3. Name it: **"Influencer Pipeline Bot"** (or your choice)
4. Click **"Create"**

### 1.2 Create Bot User

1. In left sidebar, click **"Bot"**
2. Click **"Add Bot"**
3. Confirm by clicking **"Yes, do it!"**

### 1.3 Configure Bot Settings

1. **Bot Username:** Set to "Pipeline Manager" or similar
2. **Bot Icon:** Upload an icon if desired

3. **Enable Privileged Gateway Intents:**
   - ✅ Check **"Presence Intent"**
   - ✅ Check **"Server Members Intent"**
   - ✅ Check **"Message Content Intent"**
   - Click **"Save Changes"**

4. **Copy Bot Token:**
   - Click **"Reset Token"** (if needed)
   - Click **"Copy"** to copy your bot token
   - ⚠️ **KEEP THIS SECRET!** Never share it publicly

### 1.4 Set Bot Permissions

1. In left sidebar, click **"OAuth2"** → **"URL Generator"**

2. **Select Scopes:**
   - ✅ `bot`
   - ✅ `applications.commands`

3. **Select Bot Permissions:**
   - ✅ Read Messages/View Channels
   - ✅ Send Messages
   - ✅ Send Messages in Threads
   - ✅ Embed Links
   - ✅ Attach Files
   - ✅ Read Message History
   - ✅ Add Reactions
   - ✅ Use Slash Commands

4. **Copy Generated URL** at bottom of page

### 1.5 Invite Bot to Your Server

1. Open the copied URL in a new browser tab
2. Select your server from dropdown
3. Click **"Authorize"**
4. Complete the CAPTCHA
5. Bot should now appear in your server's member list (offline for now)

---

## Step 2: Get Your Server ID (2 minutes)

### 2.1 Enable Developer Mode

1. In Discord, click ⚙️ **User Settings** (bottom left)
2. Go to **"Advanced"** (in left sidebar)
3. Enable **"Developer Mode"** toggle
4. Close settings

### 2.2 Copy Server ID

1. Right-click your server icon (in left sidebar)
2. Click **"Copy Server ID"**
3. Save this for later

---

## Step 3: Configure Environment Variables (3 minutes)

### 3.1 Open .env File

Navigate to your pipeline directory and open `.env` file

### 3.2 Add Discord Settings

Add these lines (replace with your actual values):

```env
# ===========================================
# Discord Bot Configuration
# ===========================================
DISCORD_BOT_TOKEN=your_discord_bot_token_here
DISCORD_GUILD_ID=987654321098765432

# Discord channel IDs for news delivery (optional - configure later)
DISCORD_NEWS_CHANNEL_ID=
```

Replace:
- `DISCORD_BOT_TOKEN` with your actual bot token from Step 1.3
- `DISCORD_GUILD_ID` with your server ID from Step 2.2

⚠️ **NEVER commit .env file to git!**

---

## Step 4: Verify Setup (1 minute)

### 4.1 Run Setup Verification Script

```bash
cd C:/Users/wtfau/influencer_lora_pipeline
python setup_discord.py
```

This will check:
- ✅ Bot token is set
- ✅ Dependencies installed
- ✅ Persona configs exist
- ✅ API keys configured
- ✅ GHL setup (optional)

### 4.2 Expected Output

```
======================================================================
DISCORD BOT SETUP VERIFICATION
======================================================================

1. Checking environment variables...
✅ DISCORD_BOT_TOKEN found (your_token...)
✅ DISCORD_GUILD_ID found (987654321098765432)

2. Checking dependencies...
✅ discord.py installed (version 2.6.4)
✅ pyyaml installed

3. Checking persona configurations...
✅ Found: CDS001_cristiedesouza
✅ Found: LFX001_lexifairfax

✅ Total personas found: 2

4. Checking API keys for chat commands...
✅ Anthropic API key found (Claude)
✅ xAI API key found (Grok)

5. Checking GHL integration...
✅ GHL configured (CRM commands available)

======================================================================
SETUP SUMMARY
======================================================================

✅ READY TO START BOT!

To start the bot:
   python discord_bot/bot.py

Bot will sync commands automatically.
In Discord, type /help to see all available commands.
======================================================================
```

---

## Step 5: Start the Bot (1 minute)

### 5.1 Start Bot

```bash
cd C:/Users/wtfau/influencer_lora_pipeline
python discord_bot/bot.py
```

### 5.2 Expected Console Output

```
🤖 Starting Influencer Pipeline Bot...
📊 Loaded 2 personas
🚀 Bot starting...
2026-01-20 11:30:45 INFO Bot logged in as Pipeline Manager#1234
2026-01-20 11:30:45 INFO Connected to 1 guilds
2026-01-20 11:30:46 INFO Synced commands to guild 987654321098765432
```

### 5.3 Check Discord

1. Bot should now show as **🟢 Online** in member list
2. Bot should have "Playing" status: **"Watching content generation | /help"**

---

## Step 6: Test Commands (5 minutes)

### 6.1 Open Discord

Go to your server where you invited the bot

### 6.2 Test Basic Commands

In any text channel, type `/` and you should see all bot commands appear:

**Test these in order:**

1. **Check bot is responsive:**
   ```
   /ping
   ```
   Should respond with: "🏓 Pong! Bot latency: XXms"

2. **View help:**
   ```
   /help
   ```
   Should show command categories and list

3. **Check personas:**
   ```
   /personas
   ```
   Should show CDS001 (Cristie) and LFX001 (Lexi)

4. **Check status:**
   ```
   /status
   ```
   Should show pipeline dashboard

5. **View vault:**
   ```
   /vault CDS001
   ```
   Should show vault levels for all lanes

6. **Preview prompt:**
   ```
   /preview CDS001 sfw
   ```
   Should show an example prompt

7. **Get persona info:**
   ```
   /info LFX001
   ```
   Should show Lexi's full details

8. **Select persona:**
   ```
   /select CDS001
   ```
   Should set Cristie as active

9. **Test chat (if API key configured):**
   ```
   /chat Hey there!
   ```
   Should get response in Cristie's personality

---

## Step 7: Configure News Channel (Optional - 2 minutes)

### 7.1 Create News Channel

1. In your Discord server, create a new text channel
2. Name it: **#content-news** (or your choice)
3. Right-click the channel → **"Copy Channel ID"**

### 7.2 Add to .env

```env
DISCORD_NEWS_CHANNEL_ID=123456789012345678
```

This will be used by the news agents we're about to create.

---

## Step 8: Keep Bot Running (Production Setup)

### Option A: Keep Terminal Open (Simple)

Just leave the terminal window open with bot running.

**Pros:** Simple
**Cons:** Stops if you close terminal or restart computer

### Option B: Background Process (Better)

**Windows:**
```bash
start /B python discord_bot/bot.py
```

**Linux/Mac:**
```bash
nohup python discord_bot/bot.py &
```

### Option C: Process Manager (Best)

Install PM2 (requires Node.js):
```bash
npm install -g pm2
pm2 start discord_bot/bot.py --name "pipeline-bot" --interpreter python
pm2 save
pm2 startup
```

**Pros:** Auto-restart, logs, monitoring
**Cons:** Requires Node.js

### Option D: Run as Service (Production)

Create a Windows Service or systemd service for automatic startup on boot.

---

## Troubleshooting

### Bot Shows Offline

**Causes:**
- Bot token incorrect
- Python script crashed
- Internet connection lost

**Solutions:**
1. Check console for error messages
2. Verify token in .env matches Discord Developer Portal
3. Restart bot

### Commands Not Appearing

**Causes:**
- Commands not synced yet (wait 1 minute)
- Bot missing permissions
- Discord cache issue

**Solutions:**
1. Wait 1-2 minutes after bot starts
2. Re-invite bot with correct permissions
3. Try in a different channel
4. Restart Discord client

### "/help shows nothing"

**Cause:** Commands haven't synced

**Solution:**
1. Wait up to 1 hour (global sync)
2. OR use guild-specific sync (faster):
   - Ensure DISCORD_GUILD_ID is set in .env
   - Restart bot
   - Should sync in < 1 minute

### Chat Commands Not Working

**Causes:**
- No API keys configured
- API key invalid or out of credits
- Network issue

**Solutions:**
1. Check .env has at least one LLM API key
2. Verify API key is valid
3. Check console for error messages

### GHL Commands Not Working

**Cause:** GHL not configured

**Solution:**
Add to .env:
```env
GHL_API_KEY=your_key_here
GHL_LOCATION_ID=your_location_id
```

### Permission Errors

**Cause:** Bot missing Discord permissions

**Solution:**
1. Right-click bot in member list → Roles
2. Ensure bot role has required permissions
3. Or re-invite bot with correct permission URL from Step 1.4

---

## Command Quick Reference

Once bot is running, you can use these commands in Discord:

### Status
- `/status` - Overview dashboard
- `/personas` - List all models
- `/vault [model_id]` - Check vault levels
- `/analytics [model_id]` - View metrics

### Generate
- `/generate [model] [lane] [count]` - Generate 1-10 images
- `/fill_vault [model] [lane]` - Auto-fill vault
- `/batch [model]` - Fill all lanes
- `/preview [model] [lane]` - Preview prompts

### Persona
- `/select [model]` - Set active persona
- `/info [model]` - Detailed info
- `/chat [message]` - Chat with persona

### System
- `/help` - Show all commands
- `/ping` - Check bot
- `/reload` - Reload configs

---

## Next Steps

✅ Bot is now fully set up and running!

**Recommended:**
1. Test all commands to familiarize yourself
2. Configure news agents (next section)
3. Set up scheduled tasks
4. Create dashboards

---

## Support

If you encounter issues:

1. **Check console output** - Error messages appear here
2. **Run verification:** `python setup_discord.py`
3. **Check .env file** - Ensure all tokens are correct
4. **Restart bot** - Often fixes issues
5. **Check Discord status** - https://discordstatus.com

---

## Security Notes

⚠️ **Important Security Practices:**

1. **Never share your bot token**
   - It's like a password to control your bot
   - If leaked, regenerate it immediately

2. **Never commit .env to git**
   - Already in .gitignore
   - Contains all your secrets

3. **Use environment variables**
   - Never hardcode API keys in code
   - Always use .env file

4. **Restrict bot permissions**
   - Only give permissions bot actually needs
   - Principle of least privilege

5. **Monitor bot activity**
   - Check logs regularly
   - Set up alerts for errors

---

**Setup Complete! 🎉**

Your Discord bot is now running and ready to manage your content pipeline!
