<div align="center">
  <a href="https://youtu.be/8V-EiVDZu98">
    <img src="https://img.youtube.com/vi/8V-EiVDZu98/0.jpg" alt="MiniCPM5-1B + Agent-Reach: Build a Local AI Trend Scout!">
  </a>
  <h3>📺 <a href="https://youtu.be/8V-EiVDZu98">Watch the full tutorial on YouTube</a></h3>
</div>

# MiniCPM5-1B + Agent-Reach: Build a Local AI Trend Scout!

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Ollama](https://img.shields.io/badge/Local%20LLM-Ollama-orange.svg?style=for-the-badge&logo=ollama)](https://ollama.com)
[![GitHub CLI](https://img.shields.io/badge/API-GitHub%20CLI-black.svg?style=for-the-badge&logo=github)](https://cli.github.com)
[![Gradio](https://img.shields.io/badge/UI-Gradio-red.svg?style=for-the-badge)](https://gradio.app)

A minimalist, local **AI Agent** that queries GitHub for trending, newly created open-source repositories, retrieves the founders' bios, and evaluates their potential for funding, acquisition, or sponsorship using local LLMs. 

This tool automates **Deal Sourcing** (the process of finding promising early-stage software projects and solo creators before everyone else does) — a high-value task typically done manually by Venture Capital (VC) scouts.

---

## 🛠️ Tech Stack & Prerequisites

*   **Core Logic:** Python 3.10+
*   **Local LLM Host:** [Ollama](https://ollama.com) (Default: `minicpm5:1b` — lightweight 688MB model)
*   **Data Ingestion:** GitHub CLI (`gh`)
*   **Web Scaffolding:** [Agent Reach](https://github.com/Panniantong/agent-reach) (Enables instant read/search capabilities)
*   **User Interface:** [Gradio](https://gradio.app) for a clean, local dashboard

---

## ⚙️ Setup Instructions (Windows PowerShell)

Ensure you have **Python 3.10+**, **Ollama**, and **GitHub CLI** installed on your system.

> [!NOTE]
> Local environment folders (`.venv/`) and dynamic run caches (`output.json`) are excluded in `.gitignore` to keep the repository clean. They are automatically generated when you follow the setup and run steps below.

### 1. Initialize Project & Install Agent Reach
Run the following commands in your PowerShell terminal to clone/configure dependencies:

```powershell
# Create & activate virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt

# Install Agent Reach from source
pip install https://github.com/Panniantong/agent-reach/archive/main.zip
agent-reach install --env=auto
```

### 2. Authenticate GitHub CLI
Authenticate your GitHub account to enable searching and API capabilities:
```powershell
gh auth login
```
*(Select `GitHub.com`, choose your preferred protocol, and authenticate via browser).*

### 3. Ensure Local LLM is Running
Make sure Ollama is running, then pull the lightweight MiniCPM model:
```powershell
ollama run minicpm5:1b
```

---

## 🏃 Run & Test Steps

### 1. Run via Terminal (Test Run)
To search recent repos and run the analysis directly in your console:
```powershell
python deal_sourcer.py
```

### 2. Run the Gradio Dashboard
To launch the interactive web-based dashboard:
```powershell
python app.py
```
Open **`http://127.0.0.1:7860`** in your browser to interact with the dashboard.

---

## 🔍 Customizing Queries & Testing Different Searches

You can customize the search parameters directly in `deal_sourcer.py` on line 12:

```python
cmd = ["gh", "search", "repos", "created:>2026-05-01 stars:>500", "--json", "name,owner,description,stargazersCount"]
```

### Try These Search Configurations:

1. **Target Specific Tech Stacks (e.g., Rust or Python):**
   Modify the search query term to look for language-specific repos:
   `"language:rust created:>2026-05-01 stars:>100"`
   
2. **Target Niche Keywords (e.g., Database, AI Agents):**
   Add search keywords:
   `"database created:>2026-04-01 stars:>200"`
   `"agent created:>2026-05-01 stars:>300"`
   
3. **Capture Early Breakout Projects:**
   To capture early projects before they hit massive traction, lower the star count requirement:
   `"created:>2026-05-15 stars:>100"`

---

## 🔍 How It Works (`deal_sourcer.py`)

1. **Querying GitHub:** Uses Python's native `subprocess` to call `gh search repos` and fetch metadata for repos created since a specific date (e.g. `2026-05-01`) having `stars:>500`.
2. **Founder Analysis:** Calls `gh api users/{owner}` to retrieve the developer's bio, company affiliation, and location.
3. **LLM Evaluation:** Sends the repository description, star velocity, and founder's bio to the local Ollama model with a specialized system prompt. The model scores the project (0-100) and classifies it:
    *   **High Potential:** Solo developers building high-growth tools with no enterprise affiliation (potential investment or partnership candidate).
    *   **Low Potential:** Established enterprise projects or multi-maintainer corporate initiatives.

---

## 🎯 Use Cases

*   **Early-Stage Sourcing:** Identify breakout open-source projects before they announce funding rounds.
*   **Developer Recruiting & Talent Acquisition:** Track solo developers who consistently build viral software.
*   **Technology Trend Analysis:** Detect shifting tech stacks and popular developer tools in real-time.
*   **Pre-seed Outbound Sourcing:** Automate cold outreach templates using founder bios.
*   **Competitor Landscaping:** Analyze if new repositories are threat signals to existing projects.

---

## 🔮 Future Feature Roadmap

*   **LinkedIn MCP Integration:** Use Agent Reach's LinkedIn MCP server to cross-reference founder profile bios for work history.
*   **Twitter/X Sentiment Tracking:** Track viral tweets mentioning target repositories via Agent Reach's Twitter channel.
*   **Reddit Traction Scan:** Search subreddits like `r/selfhosted` or `r/programming` to evaluate user sentiment.
*   **Automatic Outreach Emailer:** Auto-generate personalized outbound emails from local LLMs to target founders.
*   **SurrealDB Persistence:** Store deals, founder histories, and previous evaluation scores in a local vector database.

---

## Keywords
`minicpm`, `agent-reach`, `github-cli`, `ollama`, `local-llm`, `ai-project-scout`, `deal-sourcing`, `venture-capital`, `python`, `gradio-dashboard`
