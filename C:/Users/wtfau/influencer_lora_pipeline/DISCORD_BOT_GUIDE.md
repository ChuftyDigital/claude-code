# Discord Bot Command Guide

## 🚀 Quick Start

### Setting Up the Bot

1. **Create a Discord Bot**
   - Go to https://discord.com/developers/applications
   - Click "New Application"
   - Give it a name (e.g., "Influencer Pipeline Bot")
   - Go to "Bot" section
   - Click "Add Bot"
   - Copy the bot token

2. **Set Bot Permissions**
   - In the "Bot" section, enable these intents:
     - ✅ Presence Intent
     - ✅ Server Members Intent
     - ✅ Message Content Intent

3. **Invite Bot to Your Server**
   - Go to "OAuth2" → "URL Generator"
   - Select scopes:
     - ✅ bot
     - ✅ applications.commands
   - Select bot permissions:
     - ✅ Send Messages
     - ✅ Embed Links
     - ✅ Attach Files
     - ✅ Read Message History
   - Copy the generated URL and open it to invite the bot

4. **Configure .env File**
   ```bash
   DISCORD_BOT_TOKEN=your_bot_token_here
   DISCORD_GUILD_ID=your_server_id_here  # Optional, for faster sync
   ```

5. **Install Dependencies**
   ```bash
   pip install discord.py python-dotenv
   ```

6. **Run the Bot**
   ```bash
   cd C:/Users/wtfau/influencer_lora_pipeline
   python discord_bot/bot.py
   ```

---

## 📖 Complete Command Reference

### 📊 Status Commands

#### `/status`
**Description:** Shows overall pipeline status for all models

**Use Case:**
- Check which models need content replenishment
- Get a quick overview of all vaults
- See which persona is currently active

**Example:**
```
You: /status
Bot: Shows dashboard with:
     • Total personas: 2
     • Needs replenishment: 1
     • Vault levels for each model
     • Active persona
```

**When to use:**
- First thing in the morning to check what needs attention
- Before planning content generation
- After batch generation to confirm vaults are filled

---

#### `/personas`
**Description:** Lists all available AI models/personas

**Use Case:**
- See what models you have configured
- Check their niches and pricing tiers
- Quick reference for model IDs

**Example:**
```
You: /personas
Bot: Shows list:
     • CDS001 - Cristie Desouza (Beach Lifestyle)
     • LFX001 - Lexi Fairfax (Equestrian / High Society)
```

**When to use:**
- When you forget a model ID
- Showing someone what personas you have
- Before creating new content

---

#### `/vault [model_id]`
**Description:** Detailed vault status for a specific model

**Parameters:**
- `model_id` - Model ID like CDS001 or LFX001

**Use Case:**
- Deep dive into a specific model's content inventory
- See which lanes need replenishment
- Check vault fill percentages

**Example:**
```
You: /vault CDS001
Bot: Shows:
     ✅ SFW Lane: 45/50 (90%) - 3 images below threshold
     ⚠️ Spicy Lane: 12/40 (30%) - NEEDS REPLENISHMENT
     ✅ NSFW Lane: 28/30 (93%)
```

**When to use:**
- Before generating content for a specific model
- When planning content posting schedule
- To prioritize which lane to generate for

---

#### `/analytics [model_id]`
**Description:** View performance analytics for a model

**Parameters:**
- `model_id` - Model ID

**Use Case:**
- Check earnings and subscriber counts
- View engagement metrics
- Track growth over time

**Example:**
```
You: /analytics CDS001
Bot: Shows:
     • Total Earnings: $12,450
     • Subscribers: 850
     • Content Generated: 450 images
     • Engagement Rate: 8.5%
```

**When to use:**
- Weekly performance reviews
- Comparing model performance
- Making business decisions

---

### 🎨 Content Generation Commands

#### `/generate [model_id] [lane] [count]`
**Description:** Generate images for a specific model and lane

**Parameters:**
- `model_id` - Model ID (CDS001, LFX001)
- `lane` - Content lane (sfw, spicy, nsfw)
- `count` - Number of images (1-10, default: 1)

**Use Case:**
- Quick generation of specific content
- Testing new prompts
- Filling specific content needs

**Example:**
```
You: /generate CDS001 sfw 5
Bot: 🎨 Generating Content
     Model: Cristie Desouza
     Lane: SFW
     Count: 5

     [Progress updates]

     ✅ Generation Complete
```

**When to use:**
- Need specific content type urgently
- Testing prompt quality
- Small batch generation

**Time estimate:** 5-10 seconds per image

---

#### `/fill_vault [model_id] [lane]`
**Description:** Automatically fills vault to minimum threshold

**Parameters:**
- `model_id` - Model ID
- `lane` - Which lane to fill (sfw, spicy, nsfw)

**Use Case:**
- Quick replenishment when vault is low
- Automated restocking
- Preparing for posting schedule

**Example:**
```
You: /fill_vault LFX001 spicy
Bot: 🔄 Filling Vault - Lexi Fairfax
     Lane: SPICY
     Current: 12
     Target: 40
     Needed: 28 images
     Estimated Time: 3.7 minutes

     🚀 Starting generation of 28 images...
```

**When to use:**
- Vault hits replenishment threshold
- Preparing for heavy posting day
- After analyzing vault with `/vault`

**Time estimate:** Varies based on needed images (~5-10 sec/image)

---

#### `/batch [model_id]`
**Description:** Generate batch content for all lanes

**Parameters:**
- `model_id` - Model ID

**Use Case:**
- Fill all vaults at once
- Weekly bulk generation
- Initial vault setup

**Example:**
```
You: /batch CDS001
Bot: 🔄 Batch Generation - Cristie Desouza
     SFW: 10 images
     Spicy: 8 images
     NSFW: 5 images
     Total: 23 images
     Estimated: 3-5 minutes
```

**When to use:**
- Sunday night prep for the week
- All vaults are low
- Setting up a new model

**Time estimate:** 3-8 minutes depending on needs

---

#### `/preview [model_id] [lane]`
**Description:** Preview what a generated prompt would look like

**Parameters:**
- `model_id` - Model ID
- `lane` - Content lane

**Use Case:**
- Test prompt quality before generating
- See what prompts are being used
- Verify LoRA trigger words
- Check negative prompts

**Example:**
```
You: /preview CDS001 sfw
Bot: 👁️ Prompt Preview - Cristie Desouza

     Lane: SFW - Public-facing content
     LoRA Trigger: CDS001woman

     Base Prompt:
     "Cristie on the beach at sunset, wearing white
     crop top and denim shorts, golden hour lighting"

     Enhanced Prompt:
     "CDS001woman, Cristie on the beach at sunset..."

     Negative: "low quality, blurry, nsfw, nude"

     LLM: CLAUDE (professional, vibrant)
```

**When to use:**
- Before generating a batch
- Testing new prompt categories
- Debugging generation issues
- Learning how prompts are structured

---

### 👤 Persona Management Commands

#### `/select [model_id]`
**Description:** Set active persona for chat commands

**Parameters:**
- `model_id` - Model ID to make active

**Use Case:**
- Switch between personas for chat testing
- Set default model for commands
- Role-play as different personas

**Example:**
```
You: /select LFX001
Bot: ✅ Persona Selected
     Lexi Fairfax is now the active persona

     Niche: Equestrian / High Society
     Location: Cotswolds and London
     Chat Tone: Sophisticated, witty
```

**When to use:**
- Before testing chat responses
- When switching focus to different model
- Before batch chat testing

---

#### `/info [model_id]`
**Description:** Show comprehensive persona information

**Parameters:**
- `model_id` - Model ID

**Use Case:**
- See full persona details
- Reference physical description
- Check monetization settings
- View brand guidelines

**Example:**
```
You: /info CDS001
Bot: 📋 Cristie Desouza (CDS001)
     Beach Lifestyle / Fitness / DJ

     📌 Basic Info
     Age: 27
     Heritage: Brazilian
     Location: Brazil and Miami

     👤 Physical
     Build: Tall, fit and toned
     Hair: Dark Brown, long, wavy

     💫 Personality
     Energetic beach babe with infectious energy
     • Energetic and vibrant
     • Free-spirited
     • Confident and playful

     🎯 Hobbies
     • House music DJ at beach clubs
     • Surfing
     • Beach volleyball

     💰 Monetization
     OnlyFans: $19.99/month
     Chat: Flirty, fun, energetic
```

**When to use:**
- Learning about a persona
- Before writing content for them
- Checking correct physical descriptions
- Reference during prompt writing

---

#### `/chat [message]`
**Description:** Chat with the currently selected persona

**Parameters:**
- `message` - Your message to the persona

**Use Case:**
- Test chat personality
- See how persona responds
- Practice conversation flows
- Quality check before production

**Example:**
```
You: /chat Hey! Just saw your beach workout video!
Bot: 💬 Cristie Desouza says:
     "Heyy beach babe! 🌴 So glad you liked it!
     Those sunrise burpees were killer today lol.
     You do beach workouts too? We should totally
     meet up sometime! 😘"

     Chatting as CDS001
```

**When to use:**
- Testing chat responses
- Training your chat team
- Showing clients how persona "talks"
- Debugging personality issues

**Note:** Requires Claude API key

---

#### `/test_chat [model_id] [message]`
**Description:** Test chat without selecting persona first

**Parameters:**
- `model_id` - Model to test
- `message` - Message to send

**Use Case:**
- Quick chat test
- Comparing responses between models
- No need to select first

**Example:**
```
You: /test_chat LFX001 What are you up to today?
Bot: 💬 Lexi Fairfax says:
     "Hello darling! Just back from a lovely morning
     hack across the estate. The autumn colors are
     simply stunning. Planning to hit the track this
     afternoon - nothing beats the adrenaline of a
     proper drive. How's your day treating you? x"
```

**When to use:**
- A/B testing responses
- Quick checks without switching
- Demonstrating different personalities

---

### 💾 GHL Integration Commands

#### `/sync_model [model_id]`
**Description:** Sync model data to Go High Level CRM

**Parameters:**
- `model_id` - Model to sync

**Use Case:**
- Initial setup of model in GHL
- Update model stats
- Ensure CRM is current

**Example:**
```
You: /sync_model CDS001
Bot: ✅ Model Synced to GHL
     Cristie Desouza has been synced to Go High Level CRM

     Synced data:
     • Model information
     • Content statistics
     • Platform accounts
     • Monetization tiers
```

**When to use:**
- First time setting up GHL
- After major updates to persona
- Weekly sync for accuracy

**Requires:** GHL_API_KEY and GHL_LOCATION_ID in .env

---

#### `/ghl_status`
**Description:** Check GHL connection status

**Use Case:**
- Verify GHL is configured
- Test connection
- Troubleshoot sync issues

**Example:**
```
You: /ghl_status
Bot: ✅ GHL Connected
     Location ID: abc123...
     API Status: Active
     Last Sync: 5 minutes ago
```

**When to use:**
- Setting up GHL for first time
- Troubleshooting sync failures
- Verifying credentials

---

#### `/customer_info [customer_id]`
**Description:** View customer data from GHL

**Parameters:**
- `customer_id` - Customer ID (e.g., ig_john123)

**Use Case:**
- Check customer purchase history
- View interaction log
- See preferences for personalization

**Example:**
```
You: /customer_info ig_beachfan123
Bot: 👤 Customer: beachfan123
     Platform: Instagram

     💰 Spending
     Total: $145.99
     Average: $24.33
     Purchases: 6

     ❤️ Engagement
     Score: 85/100 (High)
     Interactions: 42

     🎯 Preferences
     • Beach content
     • Fitness videos
     • Bikini photos
```

**When to use:**
- Before responding to customer
- Personalizing offers
- Identifying VIP customers

---

### ⚙️ System Commands

#### `/ping`
**Description:** Check bot response time

**Use Case:**
- Verify bot is running
- Check connection quality
- Basic health check

**Example:**
```
You: /ping
Bot: 🏓 Pong!
     Bot latency: 42ms
```

**When to use:**
- Bot seems slow
- Testing if bot is online
- Regular health checks

---

#### `/reload`
**Description:** Reload persona configurations from disk

**Use Case:**
- After editing persona YAML files
- Fixing configuration errors
- Adding new personas

**Example:**
```
You: /reload
Bot: 🔄 Personas Reloaded
     Successfully reloaded 2 personas

     CDS001 - Cristie Desouza
     LFX001 - Lexi Fairfax
```

**When to use:**
- After editing persona_config.yaml
- Adding a new model
- Fixing errors in config

**Note:** No need to restart bot!

---

#### `/help`
**Description:** Show all available commands

**Use Case:**
- Reference when you forget commands
- Show new users how to use bot
- Quick command lookup

**Example:**
```
You: /help
Bot: [Shows complete command list with categories]
```

**When to use:**
- Learning the bot
- Training team members
- Quick reference

---

## 🎯 Common Workflows

### Morning Routine
```
1. /status                          # Check what needs attention
2. /vault CDS001                    # Check Cristie's vault
3. /fill_vault CDS001 spicy        # Fill low vault
4. /analytics CDS001                # Review yesterday's performance
```

### Content Generation Session
```
1. /vault LFX001                    # Check current levels
2. /preview LFX001 sfw             # Verify prompts look good
3. /batch LFX001                    # Generate for all lanes
4. /status                          # Confirm vaults filled
```

### Testing New Persona
```
1. /reload                          # Load new persona config
2. /personas                        # Verify it loaded
3. /info NEW001                     # Check all details
4. /select NEW001                   # Set as active
5. /chat Hey there!                # Test chat personality
6. /preview NEW001 sfw             # Check prompts
7. /generate NEW001 sfw 1          # Generate test image
```

### Customer Service
```
1. /customer_info ig_john123       # Look up customer
2. /select CDS001                   # Select their favorite model
3. /chat Thanks for your purchase! # Get personalized response
[Copy response to actual chat platform]
```

### Weekly Analytics Review
```
1. /analytics CDS001
2. /analytics LFX001
3. /status
[Compare performance, adjust strategy]
```

---

## 💡 Pro Tips

### Efficiency Tips
- **Use Tab completion** - Discord auto-completes commands
- **Save common commands** - Create text shortcuts
- **Batch operations** - Use `/batch` instead of multiple `/generate`
- **Preview first** - Always `/preview` before large batches

### Best Practices
- **Check status daily** - Morning `/status` becomes routine
- **Preview before generating** - Avoid wasting compute
- **Reload after edits** - No need to restart bot
- **Test chat responses** - Quality check personalities

### Troubleshooting
- **Bot not responding?** → `/ping` to check
- **Commands not showing?** → Re-invite bot with correct permissions
- **Generation failing?** → Check backend (ComfyUI/A1111) is running
- **Chat not working?** → Verify API keys in .env
- **GHL not syncing?** → Check `/ghl_status`

---

## 🚨 Important Notes

### Rate Limits
- Discord has rate limits (50 commands/second)
- Generation commands take time (5-10 sec/image)
- Don't spam commands

### API Keys Required
- **Chat commands** → Need Claude/Grok/ChatGPT API key
- **GHL commands** → Need GHL_API_KEY and GHL_LOCATION_ID
- **Generation** → Need image generation backend running

### Permissions Needed
- Bot needs "Send Messages" permission
- Bot needs "Embed Links" permission
- Bot needs "Attach Files" for future image sending

---

## 🔧 Setup Checklist

Before using the bot, make sure you have:

- [ ] Discord bot created and invited to server
- [ ] DISCORD_BOT_TOKEN in .env
- [ ] discord.py installed (`pip install discord.py`)
- [ ] Persona configs in personas/ directory
- [ ] At least one API key for chat (Claude/Grok/ChatGPT)
- [ ] (Optional) GHL_API_KEY and GHL_LOCATION_ID for CRM
- [ ] (Optional) Image generation backend running for `/generate`

---

## 📞 Getting Help

If you encounter issues:

1. **Check bot logs** - Look for error messages
2. **Verify .env** - Ensure all keys are set correctly
3. **Test API keys** - Run `python orchestrator/llm_router.py`
4. **Check permissions** - Bot needs proper Discord permissions
5. **Reload configs** - Use `/reload` after changes

---

## 🎓 Learning Path

**Beginner:**
1. Start with `/help` and `/personas`
2. Use `/info` to learn about each model
3. Try `/preview` to see prompts
4. Test `/chat` to see personalities

**Intermediate:**
5. Use `/generate` for small batches
6. Try `/fill_vault` for automation
7. Check `/vault` regularly
8. Review `/analytics` weekly

**Advanced:**
9. Set up GHL integration
10. Use `/sync_model` for CRM
11. Implement custom workflows
12. Batch generation strategies

---

## 📊 Command Summary Table

| Command | Time | API Key Needed | Use Frequency |
|---------|------|----------------|---------------|
| `/status` | Instant | No | Daily |
| `/personas` | Instant | No | As needed |
| `/vault` | Instant | No | Daily |
| `/analytics` | Instant | GHL (optional) | Weekly |
| `/generate` | 5-10s/img | No* | As needed |
| `/fill_vault` | Varies | No* | When low |
| `/batch` | 3-8 min | No* | Weekly |
| `/preview` | Instant | No | Before batches |
| `/select` | Instant | No | As needed |
| `/info` | Instant | No | Learning |
| `/chat` | 2-5s | Yes (LLM) | Testing |
| `/test_chat` | 2-5s | Yes (LLM) | Testing |
| `/sync_model` | 2-5s | Yes (GHL) | Setup/Weekly |
| `/ghl_status` | Instant | Yes (GHL) | Troubleshooting |
| `/customer_info` | 1-2s | Yes (GHL) | Pre-chat |
| `/ping` | Instant | No | Troubleshooting |
| `/reload` | Instant | No | After config edits |
| `/help` | Instant | No | Reference |

*Requires image generation backend (ComfyUI/A1111) running

---

**Happy content generating! 🎨**
