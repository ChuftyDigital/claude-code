# Financial Analysis & Revenue Forecasts
## AI Influencer Content Agency

**Document Version:** 1.0
**Date:** January 20, 2026
**Classification:** Confidential - Financial Planning

---

## Table of Contents
1. [Cost Analysis](#cost-analysis)
2. [Revenue Forecasts](#revenue-forecasts)
3. [Unit Economics](#unit-economics)
4. [Cash Flow Projections](#cash-flow-projections)
5. [Break-Even Analysis](#break-even-analysis)
6. [Sensitivity Analysis](#sensitivity-analysis)
7. [ROI Calculations](#roi-calculations)
8. [Platform Distribution](#platform-distribution)

---

## 1. Cost Analysis

### 1.1 Fixed Costs (Monthly)

#### Infrastructure Costs
```
CATEGORY                    | MONTHLY COST | ANNUAL COST | NOTES
----------------------------|--------------|-------------|------------------
GPU Hardware (Amortized)    | $625         | $7,500      | RTX 4090 x2, 5yr life
Storage (NAS + Cloud)       | $200         | $2,400      | 10TB local + backup
Internet/Bandwidth          | $150         | $1,800      | Business fiber
Compute (Cloud - backup)    | $500         | $6,000      | AWS/Azure for scaling
----------------------------|--------------|-------------|------------------
TOTAL INFRASTRUCTURE        | $1,475       | $17,700     |
```

####Software & Services
```
CATEGORY                    | MONTHLY COST | ANNUAL COST | NOTES
----------------------------|--------------|-------------|------------------
Go High Level CRM           | $297         | $3,564      | Agency Pro plan
Discord Nitro (optional)    | $10          | $120        | Better uploads
ComfyUI/A1111 (Free)        | $0           | $0          | Open source
Domain & Hosting            | $50          | $600        | Multiple domains
CDN Services                | $100         | $1,200      | Content delivery
----------------------------|--------------|-------------|------------------
TOTAL SOFTWARE              | $457         | $5,484      |
```

#### Platform Subscription Fees (Base)
```
PLATFORM                    | MONTHLY COST | ANNUAL COST | NOTES
----------------------------|--------------|-------------|------------------
OnlyFans (Free to post)     | $0           | $0          | 20% revenue share only
Fansly (Free to post)       | $0           | $0          | 20% revenue share only
Other platforms (avg)       | $50          | $600        | Varies by platform
----------------------------|--------------|-------------|------------------
TOTAL PLATFORM SUBS         | $50          | $600        |
```

#### **TOTAL FIXED COSTS: $1,982/month | $23,784/year**

---

### 1.2 Variable Costs

#### API Costs (LLM for Chat & Prompts)
```
SERVICE                     | COST STRUCTURE           | MONTHLY (200 profiles)
----------------------------|--------------------------|----------------------
Claude (Anthropic)          | ~$0.015 per 1k tokens    | $3,000
Grok (xAI)                  | ~$0.01 per 1k tokens     | $2,000
ChatGPT (OpenAI)            | ~$0.03 per 1k tokens     | $1,000
----------------------------|--------------------------|----------------------
TOTAL API COSTS             |                          | $6,000/month
```

**Assumptions:**
- Average 20 chat interactions per profile per day
- Average 500 tokens per interaction
- 200 profiles × 20 × 500 × 30 days = 60M tokens/month
- Weighted average: $0.01 per 1k tokens

**Scaling:**
- 50 profiles: $1,500/month
- 100 profiles: $3,000/month
- 200 profiles: $6,000/month
- 400 profiles: $12,000/month

#### Platform Transaction Fees
```
PLATFORM                    | FEE STRUCTURE    | EXAMPLE ON $10k REVENUE
----------------------------|------------------|------------------------
OnlyFans                    | 20%              | $2,000
Fansly                      | 20%              | $2,000
Patreon                     | 5-12%            | $800
Instagram (Meta)            | N/A              | $0 (tips via DM)
Twitter/X                   | 20% (subs)       | $2,000
Other Adult Platforms       | 15-30% avg       | $2,250 (avg 22.5%)
----------------------------|------------------|------------------------
WEIGHTED AVERAGE            | ~20%             | $2,000 per $10k
```

**At Scale:**
- $100k revenue: $20k in platform fees
- $500k revenue: $100k in platform fees
- $1M revenue: $200k in platform fees

---

### 1.3 Marketing & Acquisition Costs

#### Customer Acquisition Cost (CAC) Analysis
```
CHANNEL                     | CAC PER SUB | CONVERSION | COST PER PROFILE
----------------------------|-------------|------------|------------------
Organic Social (unpaid)     | $0-5        | 2-5%       | $100-250/profile
Paid Social Ads             | $20-50      | 1-3%       | $1,000-3,000/profile
Influencer Collabs          | $10-30      | 3-8%       | $400-1,000/profile
SEO/Content Marketing       | $5-15       | 1-4%       | $200-750/profile
Cross-promotion (profiles)  | $0-2        | 10-20%     | $0-100/profile
----------------------------|-------------|------------|------------------
BLENDED CAC                 | $8-20       | 3-8%       | $300-800/profile
```

**Target:** <$15 CAC with >$150 LTV (10:1 ratio)

#### Marketing Budget Allocation
```
STAGE                       | MONTHLY BUDGET | ALLOCATION
----------------------------|----------------|---------------------------
Phase 1 (2-10 profiles)     | $5,000         | 90% organic, 10% paid test
Phase 2 (50 profiles)       | $15,000        | 70% organic, 30% paid
Phase 3 (200 profiles)      | $30,000        | 50% organic, 50% paid
----------------------------|----------------|---------------------------
```

---

### 1.4 Operational Costs

#### Staffing (as business scales)
```
ROLE                        | FTE  | SALARY/YEAR | BENEFITS | TOTAL/YEAR
----------------------------|------|-------------|----------|------------
QA Specialist               | 1    | $50,000     | $10,000  | $60,000
Chat Support/Escalations    | 1    | $45,000     | $9,000   | $54,000
DevOps/Engineer (part-time)| 0.5  | $60,000     | $6,000   | $33,000
Marketing Coordinator       | 0.5  | $40,000     | $4,000   | $22,000
----------------------------|------|-------------|----------|------------
TOTAL (200 profiles)        | 3    |             |          | $169,000/yr
```

**Monthly: $14,083**

**Scaling:**
- 0-25 profiles: $0 (founder only)
- 26-100 profiles: $5,000/month (1 FTE)
- 101-200 profiles: $14,083/month (3 FTE)
- 201-400 profiles: $25,000/month (6 FTE)

---

### 1.5 Total Cost Summary

#### At 200 Profiles (Steady State)
```
COST CATEGORY               | MONTHLY      | ANNUAL
----------------------------|--------------|-------------
Fixed Costs                 | $1,982       | $23,784
API Costs (variable)        | $6,000       | $72,000
Platform Fees (20% of rev)  | $100,000     | $1,200,000
Marketing                   | $30,000      | $360,000
Staff                       | $14,083      | $169,000
----------------------------|--------------|-------------
TOTAL COSTS                 | $152,065     | $1,824,780
```

**On $500k/month revenue:**
- Gross Margin: 69.6% ($347,935/month)
- Net Margin: TBD after taxes, reserves

---

## 2. Revenue Forecasts

### 2.1 Revenue Per Profile Analysis

#### Revenue Streams Per Profile (Monthly Averages)
```
STREAM                      | CONSERVATIVE | MODERATE | AGGRESSIVE
----------------------------|--------------|----------|------------
Subscriptions               | $500         | $1,200   | $2,500
OnlyFans ($15-30/month)     | $300         | $700     | $1,500
Fansly ($10-25/month)       | $150         | $350     | $700
Other platforms             | $50          | $150     | $300
----------------------------|--------------|----------|------------
Pay-Per-View (PPV)          | $200         | $600     | $1,200
Spicy content ($5-10)       | $100         | $300     | $600
NSFW content ($10-25)       | $100         | $300     | $600
----------------------------|--------------|----------|------------
Tips & Donations            | $150         | $400     | $800
Chat tips                   | $100         | $250     | $500
Content appreciation        | $50          | $150     | $300
----------------------------|--------------|----------|------------
Custom Content Requests     | $200         | $600     | $1,500
Custom photosets            | $100         | $300     | $700
Custom videos (if added)    | $100         | $300     | $800
----------------------------|--------------|----------|------------
TOTAL PER PROFILE/MONTH     | $1,050       | $2,800   | $6,000
```

**Baseline Projection:** $2,000/profile/month (between conservative and moderate)

**Factors Affecting Revenue:**
- ✅ Content quality
- ✅ Posting frequency
- ✅ Engagement/chat responsiveness
- ✅ Niche selection
- ✅ Platform diversification
- ⚠️ Competition
- ⚠️ Market saturation

---

### 2.2 Profile Growth Projections

#### Phase 1: Proof of Concept (Months 1-3)
```
MONTH  | PROFILES | AVG REV/PROFILE | TOTAL REVENUE | NOTES
-------|----------|-----------------|---------------|------------------
1      | 2        | $500            | $1,000        | Launch + testing
2      | 5        | $1,200          | $6,000        | Optimization
3      | 10       | $2,000          | $20,000       | Scaling begins
-------|----------|-----------------|---------------|------------------
Q1 AVG | 6        | $1,567          | $9,000/month  | $27k total Q1
```

#### Phase 2: Rapid Growth (Months 4-12)
```
MONTH  | PROFILES | AVG REV/PROFILE | TOTAL REVENUE | CUMULATIVE
-------|----------|-----------------|---------------|------------
4      | 20       | $2,000          | $40,000       | $67k
5      | 35       | $2,000          | $70,000       | $137k
6      | 50       | $2,200          | $110,000      | $247k
7      | 75       | $2,300          | $172,500      | $419.5k
8      | 100      | $2,400          | $240,000      | $659.5k
9      | 125      | $2,500          | $312,500      | $972k
10     | 150      | $2,600          | $390,000      | $1.362M
11     | 175      | $2,700          | $472,500      | $1.834M
12     | 200      | $2,800          | $560,000      | $2.394M
-------|----------|-----------------|---------------|------------
Q2 AVG | 35       | $2,067          | $73,333       | $220k Q2
Q3 AVG | 100      | $2,433          | $274,167      | $822.5k Q3
Q4 AVG | 175      | $2,700          | $474,167      | $1.422M Q4
```

**Year 1 Total Revenue: ~$2.47M**

---

#### Phase 3: Optimization (Year 2)
```
QUARTER | PROFILES | AVG REV/PROFILE | TOTAL REVENUE | CUMULATIVE
--------|----------|-----------------|---------------|------------
Q1      | 200      | $3,000          | $600,000      | $1.8M
Q2      | 200      | $3,200          | $640,000      | $3.72M
Q3      | 200      | $3,300          | $660,000      | $5.7M
Q4      | 200      | $3,500          | $700,000      | $7.8M
--------|----------|-----------------|---------------|------------
YEAR 2  | 200 avg  | $3,250          | $650,000/mo   | $7.8M total
```

**Year 2 Total Revenue: ~$7.8M**

---

#### Phase 4: Scale (Year 3)
```
QUARTER | PROFILES | AVG REV/PROFILE | TOTAL REVENUE | CUMULATIVE
--------|----------|-----------------|---------------|------------
Q1      | 250      | $3,200          | $800,000      | $2.4M
Q2      | 300      | $3,000          | $900,000      | $5.1M
Q3      | 350      | $2,800          | $980,000      | $8.04M
Q4      | 400      | $2,600          | $1,040,000    | $11.16M
--------|----------|-----------------|---------------|------------
YEAR 3  | 325 avg  | $2,900          | $930,000/mo   | $11.16M total
```

**Year 3 Total Revenue: ~$11.16M**

**Note:** Revenue per profile decreases slightly at scale due to:
- Market saturation in best niches
- Some lower-performing profiles
- Increased competition
- BUT: Total revenue increases significantly

---

### 2.3 Platform Distribution (Revenue Split)

#### Expected Revenue by Platform Type
```
PLATFORM CATEGORY           | % OF REVENUE | @ $500k/mo | NOTES
----------------------------|--------------|------------|------------------
OnlyFans                    | 45%          | $225,000   | Primary platform
Fansly                      | 25%          | $125,000   | Secondary main
Other Adult Platforms (13)  | 20%          | $100,000   | Diversification
Social Media (6)            | 10%          | $50,000    | Tips, promotion
----------------------------|--------------|------------|------------------
TOTAL                       | 100%         | $500,000   |
```

#### 15 Adult Content Platforms:
1. **OnlyFans** - Largest, 45% of revenue
2. **Fansly** - Growing, 25% of revenue
3. Patreon - SFW tier, 5%
4. AVN Stars - Industry platform, 3%
5. LoyalFans - Alternative, 3%
6. JustFor.Fans - LGBTQ+ focus, 2%
7. 4Based - Crypto payments, 2%
8. FanCentro - Multi-platform, 2%
9. ManyVids - Clip sales, 2%
10. Clips4Sale - Fetish content, 1%
11. IWantClips - Alternative, 1%
12. ModelCentro - White label, 1%
13. FeetFinder - Niche, 1%
14. AdmireMe - Growing, 1%
15. Unlockd - New platform, 1%

#### 6 Social Media Platforms (Funnel & Tips):
1. **Instagram** - Main funnel, largest audience
2. **Twitter/X** - Engagement, subscriptions
3. **TikTok** - Discovery (SFW only)
4. **Reddit** - Community building, niche subs
5. **Snapchat** - Direct engagement, tips
6. **Pinterest** - Content discovery, SFW

---

## 3. Unit Economics

### 3.1 Customer Lifetime Value (LTV)

#### LTV Calculation Per Subscriber
```
METRIC                      | VALUE        | CALCULATION
----------------------------|--------------|---------------------------
Avg Monthly Subscription    | $20          | Blended across platforms
Avg Monthly Spend (total)   | $35          | Subs + PPV + tips
Avg Subscriber Lifetime     | 6 months     | Industry standard (churn)
Customer Acquisition Cost   | $15          | Blended CAC
----------------------------|--------------|---------------------------
LTV                         | $210         | $35 × 6 months
LTV / CAC Ratio             | 14:1         | $210 / $15
----------------------------|--------------|---------------------------
RESULT                      | EXCELLENT    | Target >3:1, achieving 14:1
```

**Retention Strategies to Extend Lifetime:**
- Personalized chat
- Regular new content
- VIP treatment for high spenders
- Cross-selling to other personas
- Exclusive perks

**If Lifetime Extended to 9 months:**
- LTV: $315
- LTV/CAC: 21:1
- Additional $105/customer

---

### 3.2 Break-Even Analysis

#### Per Profile Break-Even
```
METRIC                      | VALUE        | NOTES
----------------------------|--------------|---------------------------
Monthly Revenue Target      | $2,000       | Conservative baseline
Monthly Costs Per Profile   | $760         | Pro-rated from total costs
Break-Even Revenue          | $760/month   | Covers allocated costs
Margin Above Break-Even     | $1,240       | Profit per profile
----------------------------|--------------|---------------------------
Break-Even Subscribers      | 38 subs      | At $20/sub avg
Profitable at               | 100+ subs    | Good margin
----------------------------|--------------|---------------------------
```

**Time to Break-Even (New Profile):**
- Month 1: -$1,500 (setup, training, initial marketing)
- Month 2: -$200 (still building audience)
- Month 3: +$800 (starting to profit)
- Month 4+: +$1,240/month (steady profit)

**Payback Period:** 2-3 months per profile

---

#### Business-Level Break-Even
```
SCENARIO                    | PROFILES | MONTHLY REV | MONTHLY COSTS | PROFIT
----------------------------|----------|-------------|---------------|--------
Minimum Viable              | 25       | $50,000     | $40,000       | $10,000
Comfortable                 | 50       | $100,000    | $65,000       | $35,000
Optimal                     | 200      | $400,000    | $152,000      | $248,000
Maximum Scale               | 400      | $800,000    | $290,000      | $510,000
```

**Break-Even Point:** ~18-20 profiles at $2,000/profile/month

---

## 4. Cash Flow Projections

### 4.1 Year 1 Cash Flow (Monthly)

```
MONTH | REVENUE  | COSTS    | NET CF   | CUMULATIVE | NOTES
------|----------|----------|----------|------------|------------------
1     | $1,000   | $15,000  | -$14,000 | -$14,000   | Initial investment
2     | $6,000   | $18,000  | -$12,000 | -$26,000   | Heavy setup phase
3     | $20,000  | $22,000  | -$2,000  | -$28,000   | Peak investment
4     | $40,000  | $30,000  | $10,000  | -$18,000   | Turning point
5     | $70,000  | $42,000  | $28,000  | $10,000    | CASH POSITIVE
6     | $110,000 | $58,000  | $52,000  | $62,000    | Accelerating
7     | $172,500 | $78,000  | $94,500  | $156,500   | Strong growth
8     | $240,000 | $98,000  | $142,000 | $298,500   |
9     | $312,500 | $118,000 | $194,500 | $493,000   |
10    | $390,000 | $138,000 | $252,000 | $745,000   |
11    | $472,500 | $148,000 | $324,500 | $1,069,500 |
12    | $560,000 | $158,000 | $402,000 | $1,471,500 |
------|----------|----------|----------|------------|------------------
TOTAL | $2,394,500 | $923,000 | $1,471,500 | | 61.5% margin
```

**Key Milestones:**
- Month 5: Cash flow positive
- Month 8: Recovered initial investment
- Month 12: $1.47M cumulative cash

---

### 4.2 3-Year Cash Flow Summary

```
YEAR | REVENUE    | COSTS      | NET PROFIT | MARGIN | CUMULATIVE
-----|------------|------------|------------|--------|------------
1    | $2,394,500 | $923,000   | $1,471,500 | 61.5%  | $1.47M
2    | $7,800,000 | $2,340,000 | $5,460,000 | 70.0%  | $6.93M
3    | $11,160,000| $3,570,000 | $7,590,000 | 68.0%  | $14.52M
-----|------------|------------|------------|--------|------------
TOTAL| $21,354,500| $6,833,000 | $14,521,500| 68.0%  | $14.52M
```

---

## 5. Sensitivity Analysis

### 5.1 Revenue Sensitivity (200 Profiles)

```
REVENUE/PROFILE | MONTHLY REV | ANNUAL REV  | DIFF FROM BASE
----------------|-------------|-------------|----------------
$1,000 (worst)  | $200,000    | $2,400,000  | -60%
$1,500          | $300,000    | $3,600,000  | -40%
$2,000 (base)   | $400,000    | $4,800,000  | BASE
$2,500          | $500,000    | $6,000,000  | +25%
$3,000 (best)   | $600,000    | $7,200,000  | +50%
```

**Impact on Profitability (at 200 profiles):**
```
SCENARIO        | MONTHLY PROFIT | ANNUAL PROFIT | MARGIN
----------------|----------------|---------------|--------
Worst Case      | $48,000        | $576,000      | 24%
Conservative    | $148,000       | $1,776,000    | 49%
Base Case       | $248,000       | $2,976,000    | 62%
Optimistic      | $348,000       | $4,176,000    | 70%
Best Case       | $448,000       | $5,376,000    | 75%
```

---

### 5.2 Cost Sensitivity

#### Impact of 20% Cost Increase
```
COST CATEGORY           | BASE     | +20%     | IMPACT ON PROFIT
------------------------|----------|----------|------------------
Infrastructure          | $1,475   | $1,770   | -$295/month
API Costs               | $6,000   | $7,200   | -$1,200/month
Marketing               | $30,000  | $36,000  | -$6,000/month
Staff                   | $14,083  | $16,900  | -$2,817/month
------------------------|----------|----------|------------------
TOTAL IMPACT            |          |          | -$10,312/month
NEW PROFIT (200 prof.)  | $248k    | $238k    | -4.2% margin
```

**Conclusion:** Business is relatively resilient to cost increases

---

### 5.3 Scale Sensitivity

#### Profitability at Different Scales
```
PROFILES | REVENUE/MO  | COSTS/MO    | PROFIT/MO   | MARGIN
---------|-------------|-------------|-------------|--------
50       | $100,000    | $60,000     | $40,000     | 40%
100      | $200,000    | $95,000     | $105,000    | 52.5%
150      | $300,000    | $125,000    | $175,000    | 58.3%
200      | $400,000    | $152,000    | $248,000    | 62%
300      | $600,000    | $220,000    | $380,000    | 63.3%
400      | $800,000    | $290,000    | $510,000    | 63.8%
```

**Economies of Scale:**
- Margins improve from 40% → 62% as you scale to 200
- Marginal improvement 200 → 400 (diminishing returns)
- **Optimal scale:** 200-300 profiles

---

## 6. ROI Calculations

### 6.1 Return on Investment

#### Scenario 1: Bootstrap (Minimal Capital)
```
INITIAL INVESTMENT              | AMOUNT
--------------------------------|------------
Equipment (1x GPU)              | $5,000
Software & Setup                | $2,000
Initial Marketing               | $5,000
Working Capital                 | $10,000
--------------------------------|------------
TOTAL INVESTMENT                | $22,000
```

**Returns:**
- Year 1 Profit: $1,471,500
- ROI Year 1: 6,588%
- Payback Period: <1 month (Month 5)

#### Scenario 2: Aggressive Growth (External Capital)
```
INITIAL INVESTMENT              | AMOUNT
--------------------------------|------------
Equipment (2x GPU + Server)     | $15,000
Software & Setup                | $5,000
Marketing Budget (6 months)     | $90,000
Staff (first 6 months)          | $30,000
Working Capital                 | $30,000
Legal, Compliance               | $10,000
--------------------------------|------------
TOTAL INVESTMENT                | $180,000
```

**Returns:**
- Year 1 Profit: $1,471,500
- ROI Year 1: 718%
- Payback Period: 2-3 months

### 6.2 Investor Returns (Hypothetical)

#### If Seeking External Investment: $250k for 20% Equity

```
METRIC                          | VALUE
--------------------------------|------------------
Investment Amount               | $250,000
Equity Given                    | 20%
Post-Money Valuation            | $1,250,000

Year 1 Profit                   | $1,471,500
Investor Share (20%)            | $294,300

Year 2 Profit                   | $5,460,000
Investor Share (20%)            | $1,092,000

Year 3 Profit                   | $7,590,000
Investor Share (20%)            | $1,518,000

3-Year Total to Investor        | $2,904,300
ROI                             | 1,062%
IRR                             | ~400%
```

**Exit Scenario (Year 3):**
- Revenue: $11.16M annually
- Typical SaaS/Agency Multiple: 3-5x revenue
- Exit Valuation: $33-56M
- Investor 20% stake value: $6.6-11.2M
- Return on $250k: 26x-45x

---

## 7. Key Financial Metrics Summary

### 7.1 Target Metrics (at 200 profiles)

```
METRIC                          | TARGET       | STATUS
--------------------------------|--------------|-------------
Revenue per Profile             | $2,000-3,000 | On track
Monthly Revenue                 | $400-600k    | Achievable
Gross Margin                    | >60%         | 62%+ achieved
LTV/CAC Ratio                   | >10:1        | 14:1 achieved
Payback Period                  | <3 months    | <3 months
Cash Flow Positive              | Month 5      | Month 5
Profitability                   | Month 6      | Month 6
```

### 7.2 Red Flags to Monitor

⚠️ **Warning Signs:**
- Revenue per profile drops below $1,500
- CAC rises above $25
- Churn rate exceeds 25%/month
- Platform fees increase above 25%
- API costs exceed 5% of revenue

---

## 8. Conclusion & Recommendations

### Financial Health Assessment: **EXCELLENT**

**Strengths:**
- ✅ High gross margins (60-70%)
- ✅ Exceptional LTV/CAC ratio (14:1)
- ✅ Quick payback period (2-3 months)
- ✅ Scalable with minimal capital
- ✅ Multiple revenue streams
- ✅ Low operational overhead

**Risks:**
- ⚠️ Platform dependency (mitigation: 21 platforms)
- ⚠️ Revenue concentration risk (mitigation: diversify niches)
- ⚠️ AI cost sensitivity (mitigation: optimize API usage)

### Financial Recommendations:

1. **Maintain 6-month cash reserve** (~$900k at 200 profiles)
2. **Reinvest 30% of profits** into growth (marketing, infrastructure)
3. **Optimize at 200 profiles** before scaling to 400
4. **Track unit economics religiously** (LTV, CAC, churn)
5. **Diversify platform mix** to reduce concentration risk

### Growth Funding Options:

**Option A: Bootstrap (Recommended)**
- Use cashflow to fund growth
- Maintains 100% ownership
- Slower but sustainable

**Option B: Debt Financing**
- $100-250k line of credit
- Fund rapid expansion
- Maintain equity

**Option C: Equity Investment**
- $250-500k for 15-20%
- Accelerated growth
- Strategic partner value

**Recommendation:** Bootstrap through Year 1, then evaluate strategic options

---

**Document Status:** Living document - update monthly
**Next Review:** February 2026
**Owner:** will@chufty.digital

---

**CONFIDENTIAL - NOT FOR DISTRIBUTION**
