# 💰 Zeus Income System

Automated digital product generation and monetization using AI agents.

## 🌟 Overview

The Zeus Income System is a comprehensive platform that uses the 7-agent Zeus workforce to:
1. **Generate** digital products automatically
2. **List** them on Etsy, Gumroad, and other marketplaces
3. **Track** income and analytics

## 🤖 Zeus Agents at Work

| Agent | Role | Task |
|-------|------|------|
| ⚔️ ATHENA | Architect | Plans product strategy |
| 📊 ANALYST | Data Analyst | Researches market trends |
| 💻 DEVELOPER | Developer | Implements products |
| ⚒️ HEPHAESTUS | Builder | Builds infrastructure |
| ⚡ HERMES | Connector | Integrates APIs |
| 🌟 APOLLO | Designer | Creates visuals |
| 🛡️ ARES | Tester | Validates quality |

## 🚀 Quick Start

### 1. Generate Products
```bash
cd zeus-income-system
pip install -r requirements.txt

python orchestrator.py generate 20
```

### 2. List to Marketplaces
```bash
python orchestrator.py list
```

### 3. View Analytics
```bash
python orchestrator.py analytics
```

### 4. Start Dashboard
```bash
python orchestrator.py dashboard
# Open http://localhost:5000
```

### 5. Full Cycle (Generate + List + Track)
```bash
python orchestrator.py run
```

## 📁 Project Structure

```
zeus-income-system/
├── src/
│   ├── product_generator.py    # Zeus agent product creation
│   ├── income_tracker.py       # Revenue & expense tracking
├── automation/
│   └── marketplace.py          # Etsy/Gumroad automation
├── dashboard/
│   └── index.html               # Web dashboard
├── data/
│   ├── generated_products.json
│   └── income_data.json
├── orchestrator.py              # Main CLI
└── requirements.txt
```

## 💡 Features

- **Auto Product Generation**: Creates digital products (brushes, presets, templates, etc.)
- **Multi-Platform Listing**: Lists to Etsy, Gumroad, Creative Market
- **Income Tracking**: Tracks revenue, expenses, projections
- **Analytics Dashboard**: Visual dashboard with charts
- **Agent Workflow**: All 7 Zeus agents participate

## 📊 Supported Products

- Digital Art Brushes (Procreate, Photoshop, Affinity)
- Lightroom/Photo Presets
- UI Templates (Figma, Web)
- Online Courses
- Software Templates
- And more...

## 🔧 Configuration

Set environment variables for marketplace APIs:
```bash
export ETSY_API_KEY="your_etsy_key"
export GUMROAD_TOKEN="your_gumroad_token"
```

## 📈 Income Projections

Based on demo data:
- **Monthly**: $1,000 - $3,000
- **Yearly**: $12,000 - $36,000

(Depends on product quality and marketing)

## 📄 License

MIT License