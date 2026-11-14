<div align="center">

# 🤖 AgentApply AI
### Autonomous Multi-Agent Job Discovery, Scoring & Application Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Playwright](https://img.shields.io/badge/Playwright-1.40%2B-2EAD33?logo=playwright&logoColor=white)](https://playwright.dev/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Engineered & Maintained by [Tharun Chowdary](https://github.com/tharun1150) · [LinkedIn](https://www.linkedin.com/in/tharunchwdry) · [Portfolio](https://allatharun.onrender.com/)**

---

</div>

## 📌 Executive Summary

**AgentApply AI** is an enterprise-grade autonomous system that automates the end-to-end technical job application lifecycle. Traditional browser bots frequently get rate-limited or account-banned because they scrape consumer-facing frontends. AgentApply AI solves this by:

1. **Direct ATS Ingestion**: Querying official REST endpoints across 50+ enterprise ATS providers (Greenhouse, Lever) and RemoteOK using 15-thread concurrent execution.
2. **Experience-Aware Scoring**: Evaluating job requisitions using heuristic NLP token matching, strictly penalizing overqualified senior/lead roles (-40 pts) and prioritizing entry/mid-level positions.
3. **Stealth Form Automation**: Applying via headless **Playwright** with Chrome DevTools Protocol (CDP) evasion, dynamic question resolution, resume PDF injection, and automated 2FA OTP retrieval via IMAP.
4. **Dual Multi-Agent Orchestration**: Out-of-the-box support for **CrewAI** (role-based specialization) and **LangGraph** (stateful cyclic decision graphs).

---

## 🏛️ System Architecture

```
                                  [ TARGET ATS ENDPOINTS ]
                     (Greenhouse API · Lever API · RemoteOK Public Feeds)
                                             │
                                             ▼
                     ┌──────────────────────────────────────────────┐
                     │           1. INGESTION ENGINE                │
                     │  • SafeJobScraperAgent (15 parallel threads) │
                     │  • 300+ postings ingested in < 2 minutes     │
                     └──────────────────────┬───────────────────────┘
                                             │
                                             ▼
                     ┌──────────────────────────────────────────────┐
                     │          2. EVALUATION & SCORING             │
                     │  • Resume tokenization & skill matching      │
                     │  • -40 pt senior penalty / +15 pt junior bump│
                     │  • Filters out 90%+ irrelevant job listings  │
                     └──────────────────────┬───────────────────────┘
                                             │
                                             ▼
                     ┌──────────────────────────────────────────────┐
                     │         3. AUTOMATED FORM APPLIER            │
                     │  • Playwright Chromium Engine (Stealth mode) │
                     │  • EEO compliance & demographic resolution   │
                     │  • Resume PDF attachment & field answering   │
                     │  • IMAP OTP code retrieval for 2FA portals   │
                     └──────────────────────┬───────────────────────┘
                                             │
                                             ▼
                     ┌──────────────────────────────────────────────┐
                     │          4. AUDITING & PERSISTENCE           │
                     │  • Thread-safe JSON database (jobs_db.json)  │
                     │  • Formatted Excel report (openpyxl)         │
                     │  • SMTP HTML email dispatches with proof URLs│
                     └──────────────────────────────────────────────┘
```

---

## 🤖 The Multi-Agent Architecture

The system features dedicated autonomous components collaborating across the pipeline:

| Agent | Responsibility | Core Technology |
| :--- | :--- | :--- |
| **Scraper Agent** | Queries career board REST APIs simultaneously across 50+ tech companies | `ThreadPoolExecutor`, `Requests` |
| **Matcher Agent** | Evaluates candidate resume skills against job requisitions; enforces seniority filters | `Regex`, `Heuristic Tokenization` |
| **Applier Agent** | Drives headless Chromium browser to fill forms, attach resumes, and submit applications | `Playwright`, `CDP Evasion` |
| **Tracker Agent** | Manages persistent application states and exports color-coded Excel audit sheets | `OpenPyXL`, `JSON DB Locks` |
| **Notifier Agent** | Assembles and dispatches structured HTML summary reports and proof links | `SMTP`, `MIME Multipart` |
| **2FA OTP Reader** | Connects to inbox over SSL to extract verification codes in real-time | `imaplib`, `Regex` |

---

## 🔄 Orchestration Engines

AgentApply AI provides three independent execution modes:

```
                               [ ORCHESTRATION MODES ]
         ┌──────────────────────────────┼──────────────────────────────┐
         ▼                              ▼                              ▼
  【 Native CLI 】              【 CrewAI Team 】             【 LangGraph Graph 】
  Sequential execution         Role-based specialists:       Cyclic state machine:
  via custom Python            • Scout Agent                 • scrape_node
  coordinator                  • Evaluator Agent             • match_node
  (agents/orchestrator.py)     • Submitter Agent             • conditional routing
                               • Auditor Agent               • apply_node
                               (agents/crewai_workflow.py)   (agents/langgraph_workflow.py)
```

1. **Native Pipeline (`orchestrator.py`)**: Ultra-lightweight, zero extra dependencies.
2. **CrewAI Workflow (`crewai_workflow.py`)**: Assigns distinct personas, goals, and backstories to agents passing execution context.
3. **LangGraph Workflow (`langgraph_workflow.py`)**: Stateful graph featuring conditional edges that skip launching browsers when zero jobs meet eligibility criteria.

---

## 📊 Heuristic Scoring Model

Job requisitions are scored between `0` and `100` before application slots are allocated:

$$\text{Final Score} = \text{Skill Overlap} (0\text{--}80) + \text{Title Match} (0\text{--}20) + \text{Core Stack Bonus} (0\text{--}20) + \text{Seniority Adjustment}$$

### Seniority Adjustments
* **Auto-Penalize Senior Roles**: `-40 points` for `Senior`, `Staff`, `Principal`, `Lead`, `Manager`, `Director`.
* **Prioritize Early/Mid Career**: `+15 points` for `Junior`, `Entry Level`, `Associate`, `New Grad`, `Intern`.
* **Experience Requirement Penalty**: `-20 points` for 3+ years required; `-40 points` for 5+ years required.
* **Core Stack Multipliers**: `+5 points` each for `Python`, `FastAPI`, `React`, `Docker`, `PostgreSQL`, `AWS` (up to `+20 points`).
* **Threshold**: Applications are submitted only when $\text{Score} \ge 60$.

---

## ⚡ Performance & Benchmarks

| Metric | Measured Value | Description |
| :--- | :--- | :--- |
| **ATS Platforms Covered** | 50+ | Greenhouse, Lever, RemoteOK endpoints |
| **Ingestion Throughput** | 300+ jobs in < 2 mins | Utilizing 15-thread concurrent API requests |
| **Irrelevant Role Rejection** | 90%+ | Automated elimination of senior/lead openings |
| **Submission Speed** | ~30 seconds / job | Headless Playwright form-fill and submission |
| **Anti-Bot Stealth** | 100% | `navigator.webdriver = undefined` via CDP injection |

---

## 🚀 Getting Started

### 1. Prerequisites
* **Python**: `3.10+`
* **Node.js**: `18+` (optional, for frontend dashboard)
* **Docker & Docker Compose**: (optional, for containerized run)

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/tharun1150/autoo--apply.git
cd autoo--apply

# Set up virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
playwright install chromium
```

### 3. Environment Configuration

```bash
# Initialize configuration from example
cp .env.example .env
```

Open `.env` and configure your target search preferences and personal contact info:
```ini
FIRST_NAME=YourFirstName
LAST_NAME=YourLastName
PERSONAL_EMAIL=your.email@example.com
PERSONAL_PHONE=+10000000000
RESUME_PATH=resume.pdf
HEADLESS=true
```

---

## 🛠️ Execution Options

### Option A: Command Line Runner
```bash
# Run the complete autonomous pipeline
python -m agents.orchestrator

# Run via CrewAI role-based multi-agent workflow
python -m agents.orchestrator --crewai

# Run via LangGraph state-machine graph workflow
python -m agents.orchestrator --langgraph

# Run individual pipeline stages
python -m agents.orchestrator --scrape    # Scrape career boards only
python -m agents.orchestrator --apply     # Apply to eligible jobs only
python -m agents.orchestrator --stats     # View current database statistics
```

### Option B: Docker Compose (Port 8002)
Run containerized headless environments with pre-configured Chromium runtimes:

```bash
# Run CrewAI stack
docker compose -f docker-compose.crewai.yml up --build -d

# Run LangGraph stack
docker compose -f docker-compose.langgraph.yml up --build -d

# View live agent logs
docker compose -f docker-compose.crewai.yml logs -f

# Check API health
curl http://localhost:8002/api/stats
```

### Option C: Developer Makefile
```bash
make up-crewai       # Start CrewAI container stack
make up-langgraph    # Start LangGraph container stack
make logs-crewai     # Stream logs
make down-crewai     # Gracefully stop containers
```

---

## 📂 Repository Structure

```
job-auto-apply/
├── agents/
│   ├── orchestrator.py          # Unified CLI coordinator
│   ├── crewai_workflow.py       # CrewAI multi-agent implementation
│   ├── langgraph_workflow.py    # LangGraph state machine graph
│   ├── agent_scraper_v2.py      # High-concurrency 15-thread ATS scraper
│   ├── agent_applier_v3.py      # Playwright form automation engine
│   ├── agent_excel_tracker.py   # openpyxl spreadsheet synchronization
│   ├── agent_email_notifier.py  # SMTP HTML email reporting
│   ├── agent_job_fit.py         # Match explainability and skill gap analysis
│   ├── agent_interview_prep.py  # Interview guide generator
│   ├── agent_profile_marketer.py# Resume & profile optimization suggestions
│   ├── job_matcher.py           # Seniority and tech stack scoring engine
│   ├── resume_parser.py         # PDF text extraction and skill tokenization
│   ├── gmail_otp_reader.py      # Automated 2FA OTP extraction via IMAP
│   └── job_database.py          # Thread-safe atomic JSON database
├── dashboard/
│   ├── server.py                # FastAPI backend API & background tasks
│   └── frontend/                # Next.js control dashboard
├── Dockerfile.backend           # Multi-stage Playwright + Python image
├── docker-compose.crewai.yml    # Standalone CrewAI Compose stack
├── docker-compose.langgraph.yml # Standalone LangGraph Compose stack
├── docker-compose.yml           # Base Compose configuration
├── requirements-crewai.txt      # CrewAI extended dependencies
├── requirements-langgraph.txt   # LangGraph extended dependencies
├── requirements.txt             # Core runtime dependencies
├── Makefile                     # Developer operations CLI
└── README.md                    # System documentation
```

---

## 🔒 Security & Privacy Engineering

* **Zero Hardcoded Secrets**: All authentication keys and personal info are loaded strictly through environment variables.
* **Anti-Bot Spoofing**: Overrides `navigator.webdriver` via CDP scripts to bypass automated headless browser detection.
* **Thread-Safe File Locking**: Prevents database race conditions when reading and writing jobs during parallel thread cycles.
* **Strict `.gitignore` Standards**: Credentials (`.env*`), generated audit logs, local database records, and PDF resumes are barred from version control.

---

## 📜 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

<div align="center">
Built with dedication by <strong>Tharun Chowdary</strong>
</div>
