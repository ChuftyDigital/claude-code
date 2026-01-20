# Discord Bot Quick Reference Card

## 🚀 Most Used Commands

### Daily Operations
```
/status                              Check overall pipeline status
/vault [model_id]                    Check specific model vault
/fill_vault [model_id] [lane]       Fill low vault automatically
/analytics [model_id]                View performance metrics
```

### Content Generation
```
/generate [model] [lane] [count]     Generate 1-10 images
/batch [model_id]                    Fill all lanes at once
/preview [model] [lane]              Preview prompts before generating
```

### Persona & Chat
```
/select [model_id]                   Set active persona
/chat [message]                      Chat with active persona
/info [model_id]                     View full persona details
```

### System
```
/help                                Show all commands
/ping                                Check bot status
/reload                              Reload configs after edits
```

---

## 📋 Command Cheat Sheet

| Command | What It Does | Example |
|---------|--------------|---------|
| `/status` | Dashboard overview | `/status` |
| `/personas` | List all models | `/personas` |
| `/vault CDS001` | Check Cristie's vault | `/vault CDS001` |
| `/generate CDS001 sfw 5` | Generate 5 SFW images | `/generate CDS001 sfw 5` |
| `/fill_vault LFX001 spicy` | Fill Lexi's spicy vault | `/fill_vault LFX001 spicy` |
| `/preview CDS001 sfw` | Preview SFW prompts | `/preview CDS001 sfw` |
| `/select LFX001` | Set Lexi as active | `/select LFX001` |
| `/chat Hey there!` | Chat with active model | `/chat Hey there!` |
| `/info CDS001` | Cristie's full info | `/info CDS001` |
| `/sync_model CDS001` | Sync to GHL | `/sync_model CDS001` |

---

## 🎯 Quick Workflows

### Morning Check
```
/status → /vault CDS001 → /fill_vault CDS001 spicy
```

### Test New Content
```
/preview CDS001 sfw → /generate CDS001 sfw 2 → Review quality
```

### Chat Test
```
/select LFX001 → /chat Hello! → Review response
```

### Weekly Review
```
/analytics CDS001 → /analytics LFX001 → Compare & adjust
```

---

## 🔑 Model IDs
- **CDS001** - Cristie Desouza (Beach/Fitness)
- **LFX001** - Lexi Fairfax (Equestrian/Society)

## 🎨 Lanes
- **sfw** - Public social media
- **spicy** - Teaser content
- **nsfw** - Subscriber exclusive

---

## ⏱️ Time Estimates
- Single image: ~5-10 seconds
- Fill vault (20-40 images): ~2-7 minutes
- Batch all lanes: ~3-8 minutes
- Chat response: ~2-5 seconds

---

## 🚨 Troubleshooting
| Issue | Solution |
|-------|----------|
| Bot not responding | `/ping` to check connection |
| Commands missing | Re-invite bot with correct permissions |
| Generation failing | Check ComfyUI/A1111 is running |
| Chat not working | Verify API keys in .env |
| GHL not syncing | Run `/ghl_status` |

---

## 📞 Need Help?
Run `/help` for full command list with descriptions!

---

**Print this card and keep it handy! 📄**
