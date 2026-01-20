@echo off
REM Copy all documentation to Google Drive
REM Adjust the GDRIVE_PATH below to match your Google Drive location

REM =============================================================================
REM CONFIGURATION - UPDATE THIS PATH TO YOUR GOOGLE DRIVE
REM =============================================================================
REM Common locations:
REM - G:\My Drive\Production.Studio
REM - C:\Users\wtfau\Google Drive\Production.Studio
REM - Or check where Google Drive Desktop syncs to

SET GDRIVE_PATH=G:\My Drive\Production.Studio\AI_Influencer_Agency

REM =============================================================================
REM Create folder structure
REM =============================================================================
echo Creating folder structure in Google Drive...
mkdir "%GDRIVE_PATH%" 2>nul
mkdir "%GDRIVE_PATH%\01_Business_Documents" 2>nul
mkdir "%GDRIVE_PATH%\02_Technical_Documentation" 2>nul
mkdir "%GDRIVE_PATH%\03_Code_and_Systems" 2>nul
mkdir "%GDRIVE_PATH%\03_Code_and_Systems\discord_bot" 2>nul
mkdir "%GDRIVE_PATH%\03_Code_and_Systems\agents" 2>nul
mkdir "%GDRIVE_PATH%\03_Code_and_Systems\orchestrator" 2>nul
mkdir "%GDRIVE_PATH%\04_Personas" 2>nul
mkdir "%GDRIVE_PATH%\04_Personas\CDS001_cristiedesouza" 2>nul
mkdir "%GDRIVE_PATH%\04_Personas\LFX001_lexifairfax" 2>nul
mkdir "%GDRIVE_PATH%\05_Master_Templates" 2>nul

REM =============================================================================
REM Copy Business Documents
REM =============================================================================
echo.
echo Copying Business Documents...
copy "C:\Users\wtfau\influencer_lora_pipeline\docs\BUSINESS_OVERVIEW_HIGH_LEVEL.md" "%GDRIVE_PATH%\01_Business_Documents\" /Y
copy "C:\Users\wtfau\influencer_lora_pipeline\docs\FINANCIAL_ANALYSIS_AND_FORECASTS.md" "%GDRIVE_PATH%\01_Business_Documents\" /Y
copy "C:\Users\wtfau\influencer_lora_pipeline\docs\INDUSTRY_AND_PEER_ANALYSIS.md" "%GDRIVE_PATH%\01_Business_Documents\" /Y
copy "C:\Users\wtfau\influencer_lora_pipeline\docs\BUSINESS_PLAN_REVIEW_AND_ENHANCEMENTS.md" "%GDRIVE_PATH%\01_Business_Documents\" /Y

REM =============================================================================
REM Copy Technical Documentation
REM =============================================================================
echo.
echo Copying Technical Documentation...
copy "C:\Users\wtfau\influencer_lora_pipeline\DISCORD_SETUP_COMPLETE.md" "%GDRIVE_PATH%\02_Technical_Documentation\" /Y
copy "C:\Users\wtfau\influencer_lora_pipeline\DISCORD_BOT_GUIDE.md" "%GDRIVE_PATH%\02_Technical_Documentation\" /Y
copy "C:\Users\wtfau\influencer_lora_pipeline\DISCORD_QUICK_REF.md" "%GDRIVE_PATH%\02_Technical_Documentation\" /Y
copy "C:\Users\wtfau\influencer_lora_pipeline\GHL_INTEGRATION_GUIDE.md" "%GDRIVE_PATH%\02_Technical_Documentation\" /Y
copy "C:\Users\wtfau\influencer_lora_pipeline\SESSION_SUMMARY.md" "%GDRIVE_PATH%\02_Technical_Documentation\" /Y
copy "C:\Users\wtfau\influencer_lora_pipeline\COMPLETE_SESSION_SUMMARY.md" "%GDRIVE_PATH%\02_Technical_Documentation\" /Y

REM =============================================================================
REM Copy Code and Systems
REM =============================================================================
echo.
echo Copying Code Files...
copy "C:\Users\wtfau\influencer_lora_pipeline\discord_bot\bot.py" "%GDRIVE_PATH%\03_Code_and_Systems\discord_bot\" /Y
copy "C:\Users\wtfau\influencer_lora_pipeline\agents\news_agents.py" "%GDRIVE_PATH%\03_Code_and_Systems\agents\" /Y
copy "C:\Users\wtfau\influencer_lora_pipeline\orchestrator\persona_manager.py" "%GDRIVE_PATH%\03_Code_and_Systems\orchestrator\" /Y
copy "C:\Users\wtfau\influencer_lora_pipeline\orchestrator\llm_router.py" "%GDRIVE_PATH%\03_Code_and_Systems\orchestrator\" /Y
copy "C:\Users\wtfau\influencer_lora_pipeline\orchestrator\ghl_integration.py" "%GDRIVE_PATH%\03_Code_and_Systems\orchestrator\" /Y
copy "C:\Users\wtfau\influencer_lora_pipeline\setup_discord.py" "%GDRIVE_PATH%\03_Code_and_Systems\" /Y
copy "C:\Users\wtfau\influencer_lora_pipeline\demo_prompt_enhancement.py" "%GDRIVE_PATH%\03_Code_and_Systems\" /Y
copy "C:\Users\wtfau\influencer_lora_pipeline\test_generation.py" "%GDRIVE_PATH%\03_Code_and_Systems\" /Y

REM =============================================================================
REM Copy Persona Configurations
REM =============================================================================
echo.
echo Copying Persona Configurations...
copy "C:\Users\wtfau\influencer_lora_pipeline\personas\CDS001_cristiedesouza\persona_config.yaml" "%GDRIVE_PATH%\04_Personas\CDS001_cristiedesouza\" /Y
copy "C:\Users\wtfau\influencer_lora_pipeline\personas\LFX001_lexifairfax\persona_config.yaml" "%GDRIVE_PATH%\04_Personas\LFX001_lexifairfax\" /Y

REM =============================================================================
REM Create README in root
REM =============================================================================
echo.
echo Creating README...
(
echo # AI Influencer Content Agency - Master Archive
echo.
echo **Date:** %date% %time%
echo **Version:** 1.0
echo **Classification:** CONFIDENTIAL
echo.
echo ## Folder Structure
echo.
echo - **01_Business_Documents/** - High-level overview, financials, industry analysis, business plan
echo - **02_Technical_Documentation/** - Discord bot setup, GHL integration, session summaries
echo - **03_Code_and_Systems/** - All Python code, Discord bot, agents, orchestrator
echo - **04_Personas/** - Persona configurations (CDS001, LFX001)
echo - **05_Master_Templates/** - Blank templates for new personas and workflows
echo.
echo ## Quick Links
echo.
echo **For Executive Summary:** See `01_Business_Documents/BUSINESS_OVERVIEW_HIGH_LEVEL.md`
echo **For Financial Models:** See `01_Business_Documents/FINANCIAL_ANALYSIS_AND_FORECASTS.md`
echo **For Setup Instructions:** See `02_Technical_Documentation/DISCORD_SETUP_COMPLETE.md`
echo **For Complete Summary:** See `02_Technical_Documentation/COMPLETE_SESSION_SUMMARY.md`
echo.
echo ## Key Stats
echo.
echo - **3-Year Revenue Projection:** $21.35M
echo - **3-Year Profit Projection:** $14.52M (68%% margin)
echo - **LTV/CAC Ratio:** 14:1
echo - **Business Plan Grade:** 9/10
echo - **Market Opportunity:** $97B adult content industry
echo - **Competitive Position:** No scaled AI competitor
echo.
echo ## Next Steps
echo.
echo 1. Complete Discord bot setup (15 minutes)
echo 2. Generate training images
echo 3. Train LoRAs
echo 4. Launch first 2 profiles
echo 5. Begin revenue generation
echo.
echo ---
echo **CONFIDENTIAL - FOR INTERNAL USE ONLY**
) > "%GDRIVE_PATH%\README.md"

REM =============================================================================
REM Done
REM =============================================================================
echo.
echo ============================================================================
echo COPY COMPLETE!
echo ============================================================================
echo.
echo All files copied to: %GDRIVE_PATH%
echo.
echo Folder structure:
echo   01_Business_Documents (4 files)
echo   02_Technical_Documentation (6 files)
echo   03_Code_and_Systems (8 files)
echo   04_Personas (2 configs)
echo   05_Master_Templates (empty, for future use)
echo.
echo Total: 20+ files copied
echo.
echo Google Drive will now sync these files to the cloud.
echo ============================================================================
echo.
pause
