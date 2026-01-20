# Google Drive Upload Instructions

## Quick Method (Recommended)

### Step 1: Find Your Google Drive Folder

Google Drive for Desktop typically syncs to one of these locations:

1. **G:\My Drive\** (most common)
2. **C:\Users\wtfau\Google Drive\**
3. Or check the Google Drive system tray icon → Settings → Preferences to see your sync location

### Step 2: Update the Batch Script

1. Open `copy_to_google_drive.bat` in Notepad
2. Find this line near the top:
   ```batch
   SET GDRIVE_PATH=G:\My Drive\Production.Studio\AI_Influencer_Agency
   ```
3. Update it to match YOUR Google Drive path
4. Save the file

### Step 3: Run the Script

1. Double-click `copy_to_google_drive.bat`
2. It will create this folder structure:

```
Production.Studio/
└── AI_Influencer_Agency/
    ├── README.md
    ├── 01_Business_Documents/
    │   ├── BUSINESS_OVERVIEW_HIGH_LEVEL.md
    │   ├── FINANCIAL_ANALYSIS_AND_FORECASTS.md
    │   ├── INDUSTRY_AND_PEER_ANALYSIS.md
    │   └── BUSINESS_PLAN_REVIEW_AND_ENHANCEMENTS.md
    │
    ├── 02_Technical_Documentation/
    │   ├── DISCORD_SETUP_COMPLETE.md
    │   ├── DISCORD_BOT_GUIDE.md
    │   ├── DISCORD_QUICK_REF.md
    │   ├── GHL_INTEGRATION_GUIDE.md
    │   ├── SESSION_SUMMARY.md
    │   └── COMPLETE_SESSION_SUMMARY.md
    │
    ├── 03_Code_and_Systems/
    │   ├── discord_bot/
    │   │   └── bot.py
    │   ├── agents/
    │   │   └── news_agents.py
    │   ├── orchestrator/
    │   │   ├── persona_manager.py
    │   │   ├── llm_router.py
    │   │   └── ghl_integration.py
    │   ├── setup_discord.py
    │   ├── demo_prompt_enhancement.py
    │   └── test_generation.py
    │
    ├── 04_Personas/
    │   ├── CDS001_cristiedesouza/
    │   │   └── persona_config.yaml
    │   └── LFX001_lexifairfax/
    │       └── persona_config.yaml
    │
    └── 05_Master_Templates/
        └── (empty - for future templates)
```

3. Google Drive will automatically sync these files to the cloud
4. Check your Google Drive web interface to confirm

---

## Alternative Method: Manual Copy/Paste

If the batch script doesn't work:

### Step 1: Open File Explorer

1. Navigate to: `C:\Users\wtfau\influencer_lora_pipeline\`
2. Open Google Drive in another window

### Step 2: Create Folders

In your Google Drive → Production.Studio, create:
- AI_Influencer_Agency
  - 01_Business_Documents
  - 02_Technical_Documentation
  - 03_Code_and_Systems
    - discord_bot
    - agents
    - orchestrator
  - 04_Personas
    - CDS001_cristiedesouza
    - LFX001_lexifairfax
  - 05_Master_Templates

### Step 3: Copy Files

**From `C:\Users\wtfau\influencer_lora_pipeline\docs\`**
→ Copy to `01_Business_Documents/`:
- BUSINESS_OVERVIEW_HIGH_LEVEL.md
- FINANCIAL_ANALYSIS_AND_FORECASTS.md
- INDUSTRY_AND_PEER_ANALYSIS.md
- BUSINESS_PLAN_REVIEW_AND_ENHANCEMENTS.md

**From `C:\Users\wtfau\influencer_lora_pipeline\`**
→ Copy to `02_Technical_Documentation/`:
- DISCORD_SETUP_COMPLETE.md
- DISCORD_BOT_GUIDE.md
- DISCORD_QUICK_REF.md
- GHL_INTEGRATION_GUIDE.md
- SESSION_SUMMARY.md
- COMPLETE_SESSION_SUMMARY.md

**From `C:\Users\wtfau\influencer_lora_pipeline\discord_bot\`**
→ Copy to `03_Code_and_Systems/discord_bot/`:
- bot.py

**From `C:\Users\wtfau\influencer_lora_pipeline\agents\`**
→ Copy to `03_Code_and_Systems/agents/`:
- news_agents.py

**From `C:\Users\wtfau\influencer_lora_pipeline\orchestrator\`**
→ Copy to `03_Code_and_Systems/orchestrator/`:
- persona_manager.py
- llm_router.py
- ghl_integration.py

**From `C:\Users\wtfau\influencer_lora_pipeline\`**
→ Copy to `03_Code_and_Systems/`:
- setup_discord.py
- demo_prompt_enhancement.py
- test_generation.py

**From `C:\Users\wtfau\influencer_lora_pipeline\personas\CDS001_cristiedesouza\`**
→ Copy to `04_Personas/CDS001_cristiedesouza/`:
- persona_config.yaml

**From `C:\Users\wtfau\influencer_lora_pipeline\personas\LFX001_lexifairfax\`**
→ Copy to `04_Personas/LFX001_lexifairfax/`:
- persona_config.yaml

---

## Verify Upload

1. Open Google Drive web interface: https://drive.google.com
2. Navigate to Production.Studio → AI_Influencer_Agency
3. Confirm all folders and files are there
4. Check file sizes match originals

---

## What Gets Uploaded

**Total Files:** 20+
**Total Size:** ~1-2 MB (all text/code files)

### File Breakdown:
- **Business Documents:** 4 files (2,000+ lines)
- **Technical Docs:** 6 files (2,500+ lines)
- **Code Files:** 8 files (2,500+ lines)
- **Persona Configs:** 2 files (1,300+ lines)
- **README:** 1 file (summary)

---

## Important Notes

⚠️ **DO NOT UPLOAD:**
- `.env` file (contains API keys - NEVER upload to cloud)
- Any files with actual API tokens
- Private keys or credentials

✅ **SAFE TO UPLOAD:**
- All .md documentation files
- All .py code files
- All .yaml configuration files
- README files

All uploaded files are marked **CONFIDENTIAL** and contain no secrets.

---

## Troubleshooting

### "Access Denied" Error
- Make sure Google Drive for Desktop is running
- Check you're logged into will@chufty.digital account
- Verify you have write permissions to Production.Studio folder

### "Path Not Found" Error
- Update `GDRIVE_PATH` in the batch script to your actual Google Drive location
- Right-click Google Drive system tray icon → Settings to find your sync folder

### Files Not Syncing
- Check Google Drive icon in system tray - should show syncing
- Click icon → View Progress to see upload status
- May take a few minutes for large uploads

### Script Doesn't Run
- Right-click `copy_to_google_drive.bat` → Run as Administrator
- Or use the manual copy/paste method instead

---

## After Upload

Once files are uploaded:

1. **Share with team** (if applicable)
   - Right-click folder in Google Drive
   - Get link → Restricted
   - Share with specific people

2. **Create backup**
   - Google Drive is already backed up
   - Consider downloading a local copy quarterly
   - Or use Google Takeout for offline backup

3. **Keep updated**
   - Re-run script whenever documents are updated
   - Or enable Google Drive Desktop sync for auto-updates

---

## Google Drive Organization Tips

### Version Control
- Google Drive keeps version history automatically
- Right-click file → Version history to see changes
- Can restore previous versions if needed

### Access Control
- Keep this folder **Private** or **Restricted**
- Only share with trusted team members
- Never make public (contains business strategy)

### Naming Convention
- Use dates in filenames for major revisions
- Example: `FINANCIAL_ANALYSIS_2026-01-20.md`
- Keep original filenames for easy reference

---

## Quick Reference

### Files You'll Reference Most:

**For Investors/Banks:**
- `01_Business_Documents/BUSINESS_OVERVIEW_HIGH_LEVEL.md`
- `01_Business_Documents/FINANCIAL_ANALYSIS_AND_FORECASTS.md`

**For Operations:**
- `02_Technical_Documentation/DISCORD_SETUP_COMPLETE.md`
- `02_Technical_Documentation/COMPLETE_SESSION_SUMMARY.md`

**For Development:**
- `03_Code_and_Systems/` (all code files)

**For New Personas:**
- `04_Personas/` (use as templates)

---

**Upload Status:**
- [ ] Batch script updated with correct path
- [ ] Script executed successfully
- [ ] Files visible in Google Drive web interface
- [ ] Folder structure matches expected layout
- [ ] README.md created in root
- [ ] No .env or secrets uploaded

---

**Last Updated:** January 20, 2026
**Total Files:** 20+
**Total Lines:** 9,800+
**Classification:** CONFIDENTIAL
