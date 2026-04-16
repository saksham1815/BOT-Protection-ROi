# 🛡️ Bot Protection ROI Dashboard

A modern **Streamlit-based ROI calculator** built to estimate the financial impact of bot attacks and measure the return on investment (ROI) from deploying bot mitigation solutions.

This dashboard helps security, product, fraud, and business teams quantify business value across multiple attack vectors.

---

## 🚀 Supported Modules

- 🎟️ **Ticket Booking / Seat Spinning**
- 🕷️ **Scraping Attacks**
- 🔐 **Account Takeover (ATO)**

---

# 📊 Core ROI Logic

Used across all modules:

```math
Net ROI = Revenue Recovered + Infra Savings - Protection Cost
````

```math
ROI Ratio = (Revenue Recovered + Infra Savings) / Protection Cost
```

# 🎟️ Ticket Booking / Seat Spinning ROI

## Use Cases

* Ticketing platforms
* Airlines
* Hotels
* Events
* Inventory hoarding bots
* Seat spinning attacks

## Inputs

| Parameter                | Description                     |
| ------------------------ | ------------------------------- |
| Total Seats              | Available inventory             |
| Avg Ticket Price         | Revenue per booking             |
| Normal Conversion Rate   | Conversion under normal traffic |
| Attack Conversion Rate   | Conversion during bot attack    |
| % Blocked by Bots        | Seats locked/held by bots       |
| Mitigation %             | Protection effectiveness        |
| Infra Cost / 1K Requests | Infrastructure cost             |
| Protection Cost          | Vendor/tool cost                |

## Formulas

```math
Expected = Seats × Price × NormalConv × Multiplier
```

```math
AttackRevenue = Seats × (1 - Blocked%) × Price × AttackConv × Multiplier
```

```math
Loss = Expected - AttackRevenue
```

```math
Recovered = Loss × Mitigation%
```

```math
InfraSavings = (Seats × Multiplier / 1000) × InfraCost
```

```math
ROI = Recovered + InfraSavings - ProtectionCost
```

---

# 🕷️ Scraping ROI

## Use Cases

* E-commerce pricing theft
* OTA fare scraping
* Competitive monitoring
* Lead theft
* API data abuse

## Models

```math
RevenueSaved = (Requests × Impact / L2B) × Value
```

```math
RevenueSaved = Requests × Value × Impact
```

```math
RevenueSaved = Requests × ConversionDrop% × AOV
```

```math
RevenueSaved = TotalRevenue × PriceImpact%
```

```math
Leads = Requests × DataExtractionRate
```

```math
RevenueSaved = Leads × LeadConversionRate × DealValue
```

```math
InfraSavings = (Requests / 1000) × InfraCost
```

```math
ROI = RevenueSaved + InfraSavings - ProtectionCost
```

---

# 🔐 Account Takeover (ATO) ROI

## Use Cases

* Credential stuffing
* Loyalty fraud
* Banking fraud
* User account compromise

## Formulas

```math
Attacks = LoginAttempts × AttackRate%
```

```math
Successful = Attacks × SuccessRate%
```

```math
LossPerAccount = AccountValue + FraudLoss + RecoveryCost
```

```math
TotalLoss = Successful × LossPerAccount
```

```math
Prevented = Successful × DetectionRate × MitigationRate
```

```math
Recovered = Prevented × LossPerAccount
```

```math
InfraSavings = (LoginAttempts / 1000) × InfraCost
```

```math
ROI = Recovered + InfraSavings - ProtectionCost
```

---

# 📅 Period Multipliers

| Period      | Multiplier |
| ----------- | ---------- |
| Monthly     | 1          |
| Quarterly   | 3          |
| Half Yearly | 6          |
| Yearly      | 12         |

---

# 📈 ROI Interpretation

| ROI Ratio | Meaning       |
| --------- | ------------- |
| < 1x      | Negative ROI  |
| 1x – 2x   | Positive ROI  |
| 2x – 5x   | Strong ROI    |
| 5x+       | Excellent ROI |

---

# ▶️ Run Locally

```bash
pip install streamlit
streamlit run app.py
```

---

# 🔮 Future Modules

* Promo Abuse
* Fake Signup Bots
* Carding Fraud
* Checkout Bots
* API Abuse
* Inventory Denial
* Reseller Bots

```
```
