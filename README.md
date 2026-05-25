# 🏦 Discovery Bank AI Financial Assistant
<div align="center">

![Discovery Bank](https://img.shields.io/badge/Discovery-Bank-E31C79?style=for-the-badge&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-F55036?style=for-the-badge&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**An end-to-end AI-powered banking assistant prototype built for Discovery Bank South Africa.**  
Built with Flask · Groq AI (LLaMA 3.3 70B) · Vanilla HTML/CSS/JS · Deployed on Render

[Live Demo](http://discovery-9efs.onrender.com/) · [Report Bug](https://github.com/Hackerx10111/Discoverybank/issues) · [Request Feature](https://github.com/Hackerx10111/Discoverybank/issues)

</div>

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Use Cases](#-use-cases)
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [UML Diagrams](#-uml-diagrams)
- [SDLC Methodology](#-sdlc-methodology)
- [Agile Process](#-agile-process)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [API Reference](#-api-reference)
- [Project Structure](#-project-structure)
- [Deployment](#-deployment)
- [Security](#-security)
- [Future Roadmap](#-future-roadmap)

---

## 🎯 Project Overview

The **Discovery Bank AI Financial Assistant** is an end-to-end AI solution for the financial services industry. It simulates a fully functional digital banking portal with an intelligent conversational AI assistant capable of answering account queries, providing spending insights, explaining Vitality rewards, and offering personalised financial advice.

This project was developed as part of an **Individual AI Solution Project** for the finance industry, demonstrating how large language models can be integrated into real-world banking workflows.

### 🏆 Problem Statement

> Traditional banking chatbots are rigid, rule-based, and frustrating. Customers must navigate complex menus to find basic account information. There is no personalised financial advice at scale.

### ✅ Solution

An AI-first banking interface that understands natural language, has full context of the customer's financial profile, and delivers instant, accurate, personalised responses — 24/7.

---

## 🎭 Use Cases

### UC-01: Check Account Balance
| Field | Description |
|---|---|
| **Actor** | Authenticated Bank Customer |
| **Goal** | View current balance across all accounts |
| **Precondition** | Customer is logged in |
| **Main Flow** | Customer asks "What's my balance?" → AI retrieves balance data → Returns formatted balance for all accounts |
| **Alternate Flow** | Customer asks for a specific account → AI returns that account's balance only |
| **Postcondition** | Balance displayed with timestamp |

### UC-02: Spending Analysis
| Field | Description |
|---|---|
| **Actor** | Authenticated Bank Customer |
| **Goal** | Understand monthly spending patterns |
| **Precondition** | Transaction history exists |
| **Main Flow** | Customer asks about spending → AI analyses categories → Returns breakdown with insights |
| **Alternate Flow** | Customer asks about a specific category → AI filters and returns category-specific data |
| **Postcondition** | Spending summary displayed with recommendations |

### UC-03: Vitality Rewards Query
| Field | Description |
|---|---|
| **Actor** | Authenticated Bank Customer |
| **Goal** | Check Vitality points, status and available rewards |
| **Precondition** | Customer has a Vitality profile |
| **Main Flow** | Customer asks about Vitality → AI returns status, points, active rewards, and how to reach next tier |
| **Exception** | Vitality not linked → AI advises how to link |
| **Postcondition** | Vitality dashboard updated |

### UC-04: Transfer Money
| Field | Description |
|---|---|
| **Actor** | Authenticated Bank Customer |
| **Goal** | Transfer funds to a beneficiary |
| **Precondition** | Sufficient funds available |
| **Main Flow** | Customer selects beneficiary → Enters amount & reference → Confirms → Transfer processed |
| **Exception** | Insufficient funds → Error shown, transfer blocked |
| **Postcondition** | Transaction recorded, balance updated |

### UC-05: Financial Advice
| Field | Description |
|---|---|
| **Actor** | Authenticated Bank Customer |
| **Goal** | Receive personalised financial guidance |
| **Precondition** | Customer is authenticated |
| **Main Flow** | Customer asks for advice → AI analyses profile → Provides tailored recommendations |
| **Postcondition** | Recommendations presented; optional actions suggested |

### UC-06: Credit Score Inquiry
| Field | Description |
|---|---|
| **Actor** | Authenticated Bank Customer |
| **Goal** | Understand current credit score and how to improve it |
| **Main Flow** | Customer asks about credit score → AI returns score with contextual advice |
| **Postcondition** | Credit score and improvement tips displayed |

---

## ✨ Features

- 🤖 **AI Chat Assistant** — Groq-powered LLaMA 3.3 70B with full account context
- 🏠 **Homepage** — Marketing landing page with Discovery branding
- 📝 **3-Step Sign Up** — Personal → Identity (FICA) → Security credentials
- 🔑 **Secure Login** — Session-based authentication with demo mode
- 📊 **Dashboard** — Spending charts, recent transactions, Vitality banner
- 🧾 **Transaction History** — Searchable, filterable transaction table
- 💸 **Pay & Transfer** — Beneficiary management and fund transfers
- 🏆 **Vitality Portal** — Status, rewards, and Platinum upgrade path
- 🔒 **Server-Side API Key** — Groq key never exposed to browser
- 📱 **Fully Responsive** — Mobile, tablet, and desktop support

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        BROWSER (Client)                     │
│  ┌──────────┐  ┌──────────┐  ┌───────────┐  ┌──────────┐  │
│  │ Homepage │  │ Sign Up  │  │   Login   │  │ Bank App │  │
│  └──────────┘  └──────────┘  └───────────┘  └──────────┘  │
│         HTML / CSS / Vanilla JavaScript                     │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP / HTTPS
                            │ POST /api/chat
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   FLASK SERVER (server.py)                  │
│                                                             │
│  GET  /          → serve discovery-bank-final.html         │
│  POST /api/chat  → Groq proxy (key stored server-side)     │
│  GET  /health    → health check for Render/Railway         │
│  GET  /api/models → available Groq models                  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  python-dotenv → reads GROQ_API_KEY from .env        │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTPS
                            │ Bearer token (server-side only)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              GROQ API  (api.groq.com)                       │
│         Model: llama-3.3-70b-versatile                      │
│         Context: Full account data via system prompt        │
└─────────────────────────────────────────────────────────────┘
```

---

## 📐 UML Diagrams

### Use Case Diagram

```
                    ┌─────────────────────────────────────────┐
                    │         Discovery Bank System           │
                    │                                         │
  ┌──────────┐      │  ○ Check Balance                        │
  │          │──────┼─►○ View Transactions                    │
  │ Customer │      │  ○ Transfer Money                       │
  │          │──────┼─►○ Chat with AI Assistant               │
  └──────────┘      │  ○ View Vitality Rewards                │
        │           │  ○ Get Financial Advice                 │
        │           │  ○ Check Credit Score                   │
  ┌─────▼────┐      │  ○ Sign Up / Register                   │
  │          │      │  ○ Login / Logout                       │
  │  System  │      └─────────────────────────────────────────┘
  │  (Groq)  │
  └──────────┘
```

### Class Diagram

```
┌─────────────────────┐       ┌─────────────────────┐
│      Customer       │       │      Account        │
├─────────────────────┤       ├─────────────────────┤
│ - name: string      │1    * │ - accountNumber:str │
│ - email: string     ├───────│ - balance: float    │
│ - idNumber: string  │       │ - accountType: str  │
│ - creditScore: int  │       ├─────────────────────┤
├─────────────────────┤       │ + getBalance()      │
│ + login()           │       │ + getStatement()    │
│ + logout()          │       └──────────┬──────────┘
│ + getAccounts()     │                  │
└──────────┬──────────┘            ┌─────┴──────────────┐
           │                       │                    │
           │1        *┌────────────▼──────┐  ┌──────────▼────┐
           └──────────│  Transaction      │  │  VitalityCard  │
                      ├───────────────────┤  ├───────────────┤
                      │ - amount: float   │  │ - status: str │
                      │ - date: datetime  │  │ - points: int │
                      │ - category: str   │  │ - rewards:[]  │
                      │ - type: str       │  ├───────────────┤
                      ├───────────────────┤  │ + getStatus() │
                      │ + getDetails()    │  │ + addPoints() │
                      └───────────────────┘  └───────────────┘
```

### Sequence Diagram — AI Chat Flow

```
Customer        Browser         Flask Server      Groq API
   │               │                 │               │
   │──ask query───►│                 │               │
   │               │──POST /api/chat►│               │
   │               │                 │──system prompt│
   │               │                 │  + messages──►│
   │               │                 │               │
   │               │                 │◄──AI reply────│
   │               │◄──JSON reply────│               │
   │◄──display─────│                 │               │
   │               │                 │               │
```

### Activity Diagram — Login Flow

```
        ┌─────────────┐
        │    Start    │
        └──────┬──────┘
               │
        ┌──────▼──────┐
        │ Enter creds │
        └──────┬──────┘
               │
        ┌──────▼──────────┐   No   ┌─────────────────┐
        │ Valid username  ├────────►  Show error msg  │
        │ and password?   │        └────────┬────────┘
        └──────┬──────────┘                 │
               │ Yes                        │
        ┌──────▼──────┐                     │
        │ Create      │◄────────────────────┘
        │ session     │
        └──────┬──────┘
               │
        ┌──────▼──────┐
        │  Load app   │
        │  dashboard  │
        └──────┬──────┘
               │
        ┌──────▼──────┐
        │     End     │
        └─────────────┘
```

### State Diagram — Chat Session

```
         ┌──────────────┐
         │    Idle      │◄────────────────────────┐
         └──────┬───────┘                         │
                │ user types                       │
         ┌──────▼───────┐                         │
         │   Sending    │                         │
         └──────┬───────┘                         │
                │ request sent                     │
         ┌──────▼───────┐                         │
         │   Awaiting   │                         │
         │   Response   │                         │
         └──────┬───────┘                         │
         ┌──────┴────────┐                        │
         │               │                        │
  ┌──────▼──────┐  ┌──────▼──────┐               │
  │   Success   │  │    Error    │               │
  │  (display   │  │  (display   │               │
  │   reply)    │  │  error msg) │               │
  └──────┬──────┘  └──────┬──────┘               │
         └────────┬────────┘                      │
                  └───────────────────────────────┘
```

### ER Diagram

```
┌──────────────┐       ┌───────────────────┐       ┌──────────────────┐
│   CUSTOMER   │       │     ACCOUNT       │       │   TRANSACTION    │
├──────────────┤       ├───────────────────┤       ├──────────────────┤
│ PK customer_id│──────│ PK account_id     │──────│ PK transaction_id │
│ first_name   │  1:N  │ FK customer_id    │  1:N  │ FK account_id     │
│ last_name    │       │ account_type      │       │ amount           │
│ email        │       │ balance           │       │ description      │
│ id_number    │       │ account_number    │       │ category         │
│ credit_score │       │ created_at        │       │ transaction_date │
└──────────────┘       └───────────────────┘       │ type (CR/DR)     │
       │                                            └──────────────────┘
       │ 1:1
┌──────▼───────┐
│   VITALITY   │
├──────────────┤
│ PK vitality_id│
│ FK customer_id│
│ status       │
│ points       │
│ target_points│
└──────────────┘
```

---

## 🔄 SDLC Methodology

This project followed an **Agile SDLC** with 2-week sprints across 4 phases:

### Phase 1 — Planning & Requirements (Week 1)
- Defined project scope: AI-powered banking assistant for Discovery Bank
- Identified stakeholders: students, lecturers, banking users
- Created user stories and acceptance criteria
- Selected tech stack: Flask + Groq AI + Vanilla JS
- Risk assessment: API rate limits, CORS issues, data security

### Phase 2 — Design (Week 1–2)
- Designed UI wireframes matching Discovery Bank's pink/white branding
- Architected server-side API proxy to protect Groq key
- Designed system prompt with full account context
- Created UML diagrams: use case, class, sequence, ER
- Defined REST API contract for `/api/chat`

### Phase 3 — Development & Testing (Week 2–4)
- Sprint 1: Homepage, login, sign-up flow
- Sprint 2: Banking dashboard, transactions, transfer
- Sprint 3: AI chat integration with Groq
- Sprint 4: Vitality portal, purple card design, bug fixes
- Unit tested all Flask routes; integration tested AI responses

### Phase 4 — Deployment & Maintenance (Week 4+)
- Deployed to Render.com (free tier)
- Configured environment variables (GROQ_API_KEY)
- Set up GitHub auto-deploy from main branch
- Documented API, setup instructions, and architecture

---

## 🏃 Agile Process

### Methodology: Scrum

| Ceremony | Frequency | Duration | Purpose |
|---|---|---|---|
| Sprint Planning | Every 2 weeks | 1 hour | Define sprint goals and tasks |
| Daily Standup | Daily | 15 min | Progress updates, blockers |
| Sprint Review | Every 2 weeks | 30 min | Demo completed features |
| Retrospective | Every 2 weeks | 30 min | Process improvements |
| Backlog Refinement | Weekly | 30 min | Groom and prioritise backlog |

### Sprint Backlog

| Sprint | User Story | Story Points | Status |
|---|---|---|---|
| 1 | As a user, I want to see a Discovery Bank homepage | 3 | ✅ Done |
| 1 | As a user, I want to sign up with a 3-step form | 5 | ✅ Done |
| 1 | As a user, I want to log in securely | 3 | ✅ Done |
| 2 | As a user, I want to see my account balances | 3 | ✅ Done |
| 2 | As a user, I want to view my transaction history | 5 | ✅ Done |
| 2 | As a user, I want to transfer money to beneficiaries | 5 | ✅ Done |
| 3 | As a user, I want to chat with an AI assistant | 8 | ✅ Done |
| 3 | As a user, I want the AI to know my account details | 5 | ✅ Done |
| 4 | As a user, I want to see my Vitality rewards | 3 | ✅ Done |
| 4 | As a user, I want the UI to match Discovery's branding | 5 | ✅ Done |

### Definition of Done
- ✅ Feature is coded and working
- ✅ No console errors in browser
- ✅ Responsive on mobile and desktop
- ✅ Code pushed to GitHub
- ✅ Deployed successfully on Render

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | HTML5, CSS3, Vanilla JS | Single-page banking app |
| Backend | Python 3.11, Flask 3.0 | REST API server + static hosting |
| AI Model | Groq — LLaMA 3.3 70B | Natural language understanding |
| Styling | Custom CSS (Discovery brand) | Pink/white brand theme |
| Fonts | DM Sans, DM Serif Display | Discovery-matching typography |
| Deployment | Render.com | Free cloud hosting |
| Version Control | GitHub | Source code management |
| Environment | python-dotenv | Secure API key management |
| WSGI Server | Gunicorn | Production server |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- A free Groq API key from [console.groq.com](https://console.groq.com/keys)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Hackerx10111/Discoverybank.git
cd Discoverybank

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Open .env and add your Groq API key:
# GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx

# 4. Run the server
python server.py
```

Open your browser at **http://localhost:3000**

### Demo Login
Use any username and password, or click **"Try Demo Account"** to skip login.

---

## 📡 API Reference

### `POST /api/chat`

Sends a message to the AI assistant and returns a response.

**Request Body:**
```json
{
  "messages": [
    { "role": "user", "content": "What is my balance?" }
  ],
  "system": "You are a Discovery Bank assistant...",
  "temperature": 0.7,
  "max_tokens": 1024
}
```

**Response:**
```json
{
  "reply": "Your Transaction Account balance is R 24,380.50...",
  "model": "llama-3.3-70b-versatile",
  "usage": {
    "prompt_tokens": 450,
    "completion_tokens": 85,
    "total_tokens": 535
  }
}
```

**Error Response:**
```json
{
  "error": "Invalid Groq API key. Check your GROQ_API_KEY."
}
```

### `GET /health`
```json
{ "status": "ok", "app": "Discovery Bank AI Assistant", "api_ready": true }
```

---

## 📁 Project Structure

```
Discoverybank/
├── discovery-bank-final.html  # Complete single-file frontend app
├── server.py                  # Flask server + Groq AI proxy
├── requirements.txt           # Python dependencies
├── Procfile                   # Heroku/Render start command
├── render.yaml                # Render.com auto-deploy config
├── runtime.txt                # Python version pin
├── .env.example               # Environment variable template
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

---

## ☁️ Deployment

### Render.com (Recommended)

1. Push code to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your GitHub repo
4. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn server:app`
5. Add environment variable: `GROQ_API_KEY=gsk_xxx`
6. Deploy

### Local
```bash
pip install -r requirements.txt && python server.py
```

---

## 🔒 Security

- ✅ **Groq API key** stored in `.env` — never in the browser or committed to git
- ✅ **`.gitignore`** excludes `.env` from version control
- ✅ **HTTPS** enforced on Render deployment
- ✅ **CORS** configured via `flask-cors`
- ✅ **Input validation** on all API endpoints
- ✅ **No sensitive data** stored client-side

---

## 🗺️ Future Roadmap

- [ ] Real Discovery Bank API integration (OAuth 2.0)
- [ ] Biometric authentication (Face ID / fingerprint)
- [ ] Push notifications for transactions
- [ ] AI-powered budgeting and savings goals
- [ ] Real-time fraud detection alerts
- [ ] Multi-language support (Zulu, Xhosa, Afrikaans)
- [ ] Mobile app (React Native)
- [ ] Two-factor authentication (OTP via SMS)

---

## 👤 Author

**Thamsanqa Nzimande**  
Individual Project — AI Solution for Finance Industry

---

## 📄 License

This project is licensed under the MIT License.  
*This is an academic prototype — not affiliated with or endorsed by Discovery Bank Limited.*

---

<div align="center">
Built with ❤️ for Discovery Bank · Powered by Groq AI · Deployed on Render
</div>
