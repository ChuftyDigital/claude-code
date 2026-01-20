# Go High Level Integration Guide

## Overview

The GHL integration creates a comprehensive CRM system for tracking:
- **Model Performance**: Content stats, earnings, platform followers
- **Customer Interactions**: All messages, purchases, preferences
- **Revenue Attribution**: Link sales to specific content/models
- **Personalization Data**: Build detailed customer profiles

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Content Pipeline                         │
│  (Orchestrator, Generators, Discord Bot, Social Platforms)  │
└───────────────────┬─────────────────────────────────────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │  GHLDataManager      │  ◄── Proactive Agent
         │  (ghl_integration.py)│
         └──────────┬───────────┘
                    │
         ┌──────────┴──────────┐
         ▼                     ▼
   ┌──────────┐         ┌──────────┐
   │  Model   │         │ Customer │
   │ Records  │         │ Records  │
   └──────────┘         └──────────┘
         │                     │
         └──────────┬──────────┘
                    ▼
         ┌─────────────────────┐
         │  Go High Level CRM  │
         │  (Contacts + Notes) │
         └─────────────────────┘
```

## Setup Instructions

### 1. Get GHL API Credentials

1. Log into your GHL account: https://app.gohighlevel.com
2. Go to **Settings** → **Integrations** → **API Keys**
3. Create a new API key with these permissions:
   - `contacts.read`
   - `contacts.write`
   - `notes.write`
   - `tags.write`
4. Copy the API key

5. Get your Location ID:
   - Settings → Company Info → Location ID
   - Copy the location ID

6. Update `.env` file:
   ```env
   GHL_API_KEY=your_api_key_here
   GHL_LOCATION_ID=your_location_id_here
   ```

### 2. Set Up Custom Fields in GHL

Go to **Settings** → **Custom Fields** and create these fields:

#### For Model Contacts:
- `model_id` (Text)
- `model_niche` (Text)
- `model_age` (Number)
- `model_location` (Text)
- `total_content` (Number)
- `total_earnings` (Currency)
- `total_interactions` (Number)
- `total_customers` (Number)
- `created_at` (Date)
- `last_content` (Date)
- `last_interaction` (Date)

#### For Customer Contacts:
- `customer_id` (Text)
- `platform` (Dropdown: Instagram, Twitter, OnlyFans, Fansly)
- `username` (Text)
- `total_interactions` (Number)
- `total_purchases` (Currency)
- `average_purchase` (Currency)
- `engagement_score` (Number 0-100)
- `models_interacted` (Text)
- `preferred_content` (Text)
- `preferred_niches` (Text)
- `first_interaction` (Date)
- `last_interaction` (Date)

### 3. Set Up Tags

Create these tags in GHL for automatic categorization:

**Model Tags:**
- `AI Model`
- `Status:Active`
- `Status:Paused`
- `Status:Archived`
- `Niche:Beach Lifestyle`
- `Niche:Equestrian`
- (Add more as needed)

**Customer Tags:**
- `Customer`
- `Platform:Instagram`
- `Platform:Twitter`
- `Platform:OnlyFans`
- `Platform:Fansly`
- `Status:Active`
- `Status:VIP`
- `Status:Inactive`
- `Engagement:High` (80-100)
- `Engagement:Medium` (50-79)
- `Engagement:Low` (0-49)

## Usage

### Initialize the GHL Manager

```python
from orchestrator.ghl_integration import GHLDataManager, ModelRecord, CustomerRecord

# Initialize manager
manager = GHLDataManager(
    api_key=os.getenv("GHL_API_KEY"),
    location_id=os.getenv("GHL_LOCATION_ID")
)
```

### Sync a Model to GHL

```python
import asyncio
from datetime import datetime

async def sync_model():
    cristie = ModelRecord(
        model_id="CDS001",
        model_name="Cristie Desouza",
        niche="Beach Lifestyle / Fitness / Beachclub DJ",
        age=27,
        location="Brazil and Miami",
        status="active",
        total_content_generated=0,
        total_earnings=0.0,
        created_at=datetime.now().isoformat()
    )

    await manager.sync_model(cristie)
    print("Model synced to GHL!")

asyncio.run(sync_model())
```

### Log Customer Interaction

```python
from orchestrator.ghl_integration import InteractionRecord

async def log_interaction():
    # First sync the customer
    customer = CustomerRecord(
        customer_id="ig_beachfan123",
        platform="instagram",
        username="beachfan123",
        email="beachfan123@example.com",
        first_interaction=datetime.now().isoformat()
    )

    await manager.sync_customer(customer)

    # Then log the interaction
    interaction = InteractionRecord(
        interaction_id=f"int_{datetime.now().timestamp()}",
        timestamp=datetime.now().isoformat(),
        model_id="CDS001",
        customer_id="ig_beachfan123",
        platform="instagram",
        interaction_type="message",
        message_content="Hey Cristie! Love your beach workout videos!",
        customer_sentiment="positive",
        topics_discussed=["beach", "fitness", "workout"]
    )

    await manager.log_interaction(interaction)
    print("Interaction logged!")

asyncio.run(log_interaction())
```

### Record a Purchase

```python
async def record_purchase():
    await manager.update_customer_purchase(
        customer_id="ig_beachfan123",
        amount=29.99,
        model_id="CDS001",
        content_type="bikini_photoshoot"
    )
    print("Purchase recorded!")

asyncio.run(record_purchase())
```

## Integration Points in Pipeline

### 1. Content Generation Hook

```python
# In batch_generator.py or oneoff.py
from orchestrator.ghl_integration import on_content_generated

async def generate_content(...):
    # ... generate content ...

    # Log to GHL
    await on_content_generated(
        model_id=persona.model_id,
        content_type=prompt_type,
        ghl_manager=ghl_manager
    )
```

### 2. Discord Bot Hook

```python
# In discord_bot/bot.py
from orchestrator.ghl_integration import on_customer_interaction

@bot.command()
async def chat(ctx, *, message: str):
    # ... chat logic ...

    # Log interaction
    await on_customer_interaction(
        model_id=current_model_id,
        customer_id=f"discord_{ctx.author.id}",
        platform="discord",
        message=message,
        ghl_manager=ghl_manager
    )
```

### 3. Social Platform Hook

```python
# In your social media integrations
from orchestrator.ghl_integration import on_customer_purchase

async def process_onlyfans_purchase(purchase_data):
    await on_customer_purchase(
        model_id=purchase_data.model_id,
        customer_id=purchase_data.customer_id,
        amount=purchase_data.amount,
        content_type=purchase_data.content_type,
        ghl_manager=ghl_manager
    )
```

## Data Flow Example

### Scenario: Customer purchases content from Cristie

1. **Customer browses OnlyFans** → Views Cristie's beach bikini photo
2. **Customer purchases photo** ($29.99)
3. **Pipeline detects purchase** → Triggers webhook
4. **GHLDataManager activates**:
   - Creates/updates customer contact in GHL
   - Adds tags: `Customer`, `Platform:OnlyFans`, `Model:CDS001`
   - Logs purchase as note
   - Updates customer's `total_purchases`: $29.99
   - Increments customer's `engagement_score`
   - Updates Cristie's `total_earnings`: +$29.99
   - Updates Cristie's `total_customers`: +1
   - Adds content preference: `bikini_photos`
5. **Next interaction** → Chat agent retrieves customer preferences
   - Knows customer likes: bikini photos, beach content
   - Personalizes conversation accordingly
   - Higher chance of repeat purchase

## Advanced: Proactive Agent Behavior

The `GHLDataManager` should run as a background service:

```python
# In orchestrator/main.py or a dedicated service
import asyncio
from orchestrator.ghl_integration import GHLDataManager

async def ghl_background_sync():
    """Proactive sync every 5 minutes"""
    manager = GHLDataManager(
        api_key=os.getenv("GHL_API_KEY"),
        location_id=os.getenv("GHL_LOCATION_ID")
    )

    while True:
        # Sync all models
        for model in get_all_models():
            await manager.sync_model(model)

        # Check for stale customer data
        # Update engagement scores
        # Flag inactive customers

        await asyncio.sleep(300)  # 5 minutes

# Run in background
asyncio.create_task(ghl_background_sync())
```

## Personalization Strategy

### Customer Engagement Scoring

```python
def calculate_engagement_score(customer: CustomerRecord) -> int:
    """Calculate 0-100 engagement score"""
    score = 0

    # Interaction frequency (0-40 points)
    if customer.total_interactions > 50:
        score += 40
    elif customer.total_interactions > 20:
        score += 30
    elif customer.total_interactions > 5:
        score += 20
    else:
        score += 10

    # Purchase history (0-40 points)
    if customer.total_purchases > 500:
        score += 40
    elif customer.total_purchases > 200:
        score += 30
    elif customer.total_purchases > 50:
        score += 20
    else:
        score += 10

    # Recency (0-20 points)
    last_interaction = datetime.fromisoformat(customer.last_interaction)
    days_since = (datetime.now() - last_interaction).days

    if days_since < 7:
        score += 20
    elif days_since < 30:
        score += 15
    elif days_since < 90:
        score += 10
    else:
        score += 5

    return min(score, 100)
```

### Chat Agent Personalization

```python
async def get_personalized_response(customer_id: str, message: str) -> str:
    """Use GHL data to personalize chat response"""

    # Fetch customer from GHL
    customer = await ghl_manager.get_customer_preferences(customer_id)

    if not customer:
        return "Hey! Thanks for messaging! 💕"

    # Personalize based on preferences
    if "beach" in customer.preferred_content_types:
        response = "Hey beach babe! Just got back from shooting some waves 🏄‍♀️"
    elif "fitness" in customer.preferred_content_types:
        response = "Hey! Just finished an intense workout 💪"
    else:
        response = "Hey! Thanks for reaching out! 💕"

    # Add VIP treatment for high spenders
    if customer.total_purchases > 500:
        response += " You're one of my favorites! 😘"

    return response
```

## Monitoring & Analytics

### Key Metrics to Track

**Per Model:**
- Content generation rate (images/day)
- Earnings trend ($/day, $/week, $/month)
- Engagement rate (interactions per content piece)
- Customer acquisition (new customers/week)
- Customer retention (repeat purchase rate)

**Per Customer:**
- Lifetime value (total purchases)
- Average order value
- Purchase frequency
- Content preferences
- Best engagement times

### GHL Reporting

Use GHL's built-in reporting to create dashboards:
1. **Model Performance Dashboard**
   - Top earning models
   - Most popular niches
   - Content generation trends

2. **Customer Analytics Dashboard**
   - High-value customers (VIPs)
   - At-risk customers (inactive)
   - Conversion rates

3. **Revenue Dashboard**
   - Daily/weekly/monthly revenue
   - Revenue by model
   - Revenue by content type

## Enhancements & Roadmap

### Short-term (Next Sprint):
- [ ] Implement webhook listeners for real-time sync
- [ ] Add sentiment analysis to interaction logging
- [ ] Create GHL workflows for automated follow-ups
- [ ] Build customer segmentation (VIP, regular, at-risk)

### Medium-term:
- [ ] Predictive analytics (which customers likely to purchase)
- [ ] A/B testing for content types
- [ ] Automated win-back campaigns for inactive customers
- [ ] Revenue forecasting per model

### Long-term:
- [ ] Full marketing automation integration
- [ ] Multi-model collaboration tracking
- [ ] Referral program tracking
- [ ] Advanced customer journey mapping

## Troubleshooting

### Common Issues:

**1. API Key Invalid**
```
Error: 401 Unauthorized
```
- Verify API key in GHL dashboard
- Check key permissions include contacts.write
- Regenerate key if needed

**2. Custom Fields Not Updating**
```
Error: Custom field 'model_id' not found
```
- Ensure custom fields are created in GHL
- Check field names match exactly (case-sensitive)
- Verify field types are correct

**3. Rate Limiting**
```
Error: 429 Too Many Requests
```
- GHL has rate limits (varies by plan)
- Implement exponential backoff
- Batch updates where possible

## Support

For GHL API questions: https://highlevel.stoplight.io/
For pipeline questions: Check project README or contact team

---

**Last Updated:** January 2026
