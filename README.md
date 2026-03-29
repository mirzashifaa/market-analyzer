# Market Analyzer

AI-powered competitive intelligence for market entry decisions.

Provide a company and a market. The system researches incumbents, 
emerging competitors, and market sizing in parallel — then delivers 
a Go / No-Go recommendation with reasoning.

---

## What It Does

Given two inputs — a company name and a target market — the system:

1. Maps the incumbent landscape and identifies positioning gaps
2. Scans emerging competitors and capital velocity (Seed–Series B)
3. Estimates TAM, SAM, growth rate, and market trajectory
4. Synthesizes all three into a Go / No-Go recommendation

---

## Architecture
```
User Input (company + market)
         ↓
   POST /analyze
         ↓
┌─────────────────────────────────┐
│  Parallel Execution             │
│  Agent 1: Incumbents            │
│  Agent 2: Emerging Competitors  │
│  Agent 3: Market Sizing         │
└─────────────────────────────────┘
         ↓
   Agent 4: Synthesis
         ↓
   Go / No-Go + Reasoning
```

This could have been implemented as a single large prompt, but separating the workflow 
into research agents and a synthesis agent improves reliability, observability, 
and traceability. Each research dimension can be validated independently before 
the final recommendation is produced.

**Four agents, each with a single responsibility:**

- **Incumbents Agent** — researches established players, 
  identifies positioning gaps. Uses web search via Tavily.
- **Emerging Competitors Agent** — scans Seed through Series B 
  funding activity and capital velocity. Uses web search.
- **Market Sizing Agent** — estimates TAM/SAM, growth rate, 
  and trajectory from public analyst citations. Uses web search.
- **Synthesis Agent** — receives structured outputs from all 
  three research agents and reasons across them to produce 
  a final recommendation. Has no tools — it cannot do new 
  research, only reason over evidence.

**Tech stack:**
- Backend: Python, FastAPI, OpenAI Agents SDK, Pydantic
- AI: GPT-4o, GPT-4o-mini, Tavily web search
- Frontend: React, TypeScript, Vite, Axios

---

## Key Design Decisions

**Parallel execution for research agents**  
Agents 1, 2, and 3 run concurrently via `asyncio.gather()`. 
Tavily calls are wrapped in `asyncio.to_thread()` to prevent 
blocking the event loop. This reduces total analysis time 
from ~90s sequential to ~30–40s parallel.

Using GPT-4o-mini for research agents also reduces token
cost and rate-limit pressure while preserving output
quality for structured extraction tasks.

**Synthesis agent has no tools**  
The synthesis agent reasons only over structured Pydantic 
outputs from the three research agents. Giving it search 
access would allow it to hallucinate new research to support 
a predetermined conclusion. Keeping it tool-free ensures the 
recommendation is traceable to the evidence.

**Structured outputs via Pydantic throughout**  
Every research agent produces a typed Pydantic model rather 
than an unstructured natural-language summary. This keeps the 
evidence passed into synthesis schema-bound and predictable.

**Model selection per agent**

Research agents (Incumbents, Emerging Competitors, and
Market Sizing) use GPT-4o-mini. These agents primarily
perform structured information extraction, tool calling,
and schema-constrained output generation. GPT-4o-mini is
optimized for instruction-following and provides higher
throughput limits, which allows the three research agents
to run in parallel efficiently.

The Synthesis agent uses GPT-4o. This stage performs the
final reasoning step, weighing potentially conflicting
signals from incumbents, emerging competitors, and market
sizing to produce a GO / NO-GO recommendation. The stronger
reasoning capability of GPT-4o is reserved for this final
decision stage.

**Retry with exponential backoff**  
Research agents use `tenacity` with exponential backoff 
to handle OpenAI rate limits gracefully. The retry scope 
wraps the full parallel batch — if one agent fails, all 
three are retried. Per-agent retry would be more efficient 
in production but adds architectural complexity not 
warranted here.

**Already-in-market guardrail**  
Before running synthesis, the system checks whether the 
entering company appears in the incumbents output as a 
major player. If detected, it returns a deterministic 
NO-GO with a clear explanation rather than running 
synthesis on an invalid market entry scenario.

**Broad market input validation**  
Inputs like "enterprise software" or "SaaS" are rejected 
before analysis runs. These categories are too broad for 
meaningful incumbent or sizing analysis. Both frontend 
(with a warning) and backend (with a 400 response) 
enforce this.

---

## Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API key — [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- Tavily API key — [app.tavily.com](https://app.tavily.com)

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the `backend/` directory:
```
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

See `backend/.env.example` for reference.

Start the server:
```bash
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## Usage

Enter a company name and a specific market category:

| Company | Market | Expected |
|---------|--------|----------|
| Stripe | Payroll Software | GO |
| Canva | Interior Design Software | GO |
| Spotify | Podcast Advertising Software | NO-GO |
| McDonald's | Cloud Computing | NO-GO |
| Apple | Payroll Software | NO-GO |

**Tips for best results:**

- Use specific market categories: "payroll software" not "HR"
- Avoid broad categories: "enterprise software", "SaaS", "AI tools"

---

## API

### Health check
```
GET /health
→ {"status": "ok"}
```

### Run analysis
```
POST /analyze
Content-Type: application/json

{
  "company": "Stripe",
  "market": "payroll software"
}
```

Returns a full `AnalysisResponse` with incumbents, 
emerging competitors, market sizing, and synthesis.

---

## Limitations & Assumptions

**Already-in-market detection uses normalized name matching**  
The guardrail compares normalized company names against incumbent names.
It is reliable for obvious cases but may miss less common aliases or 
product-brand mappings.

**Company-agnostic accuracy varies by fame**  
The system performs best for well-known companies where 
GPT-4o has strong training knowledge. For lesser-known 
companies, analysis quality depends on what can be inferred 
from the company name alone. A Company Profile Agent that 
fetches verified company data before analysis runs would 
improve accuracy significantly for all company types.

**SAM is frequently unavailable**  
Serviceable Addressable Market figures require company-specific 
market data that is rarely available in public web sources. 
Most SAM fields return "Insufficient public data." A production 
version would integrate Crunchbase or PitchBook APIs.

**Market sizing relies on secondary citations**  
Analyst reports from Gartner, Forrester, and Statista are 
paywalled. The market sizing agent surfaces publicly available 
references to these reports rather than accessing them directly. 
Figures should be interpreted as directional estimates rather than investment-grade data.

**Rate limits under heavy load**  
The system depends on external LLM APIs, so repeated analyses in 
quick succession may trigger rate limits. The backend handles transient 
failures with retry and returns a clear error when limits are exceeded.

**Company name as primary company context**

The system assumes the company name alone provides sufficient
context for initial analysis. GPT-4o's training knowledge is
used to infer the company's core business, strengths, and
typical product areas.

In production, this would be replaced with a Company Profile
Agent that retrieves verified company data before running
competitive analysis.

---

## Future Improvements

**Company Profile Agent (highest priority)**  
Add an Agent 0 that fetches verified company data before 
analysis runs. This would ground company-fit reasoning in 
facts rather than LLM inference from the company name — 
directly improving synthesis accuracy for all company types.

**Per-agent retry**  
The current retry decorator wraps the full parallel batch. 
A rate limit on one agent retries all three. Per-agent retry 
would avoid re-running successful research calls and reduce 
latency on failures.

**Crunchbase / PitchBook integration**  
Verified funding data would significantly improve emerging 
competitor accuracy and SAM estimation.

**Native async Tavily client**
The current implementation wraps the synchronous Tavily SDK
in asyncio.to_thread(). Replacing this with a native async
HTTP client using httpx.AsyncClient would eliminate thread
pool overhead and improve efficiency under high concurrency.

**Analysis caching layer**
Each analysis run makes 3–4 LLM calls and multiple Tavily 
searches for the same company/market pair. A caching layer 
using Redis or a simple key-value store keyed on 
(company, market) would eliminate redundant API calls for 
repeated queries, reduce latency to near-zero for seen pairs, 
and significantly cut token costs at scale.

**Smarter frontend validation**
The current frontend validates only basic input quality and broad market categories.
A stronger version would detect likely typos, normalize near-matches, and suggest
more specific market names before the request is sent to the backend. This would
improve usability and reduce failed or low-quality analyses caused by ambiguous input.

**Semantic broad-market detection**
The current broad-market guardrail relies on a static set of normalized category names.
A stronger version would use synonym expansion, fuzzy matching, or an LLM-based
classifier to identify overly broad market inputs more reliably across phrasing
variants such as plurals, aliases, and near-equivalent terms.

---

## Development Constraints

This implementation was intentionally built using **open-access tools and APIs**
so the entire system can run in a **minimum cost development environment**.

Several engineering decisions reflect this constraint while still preserving
the architecture expected for a production-grade system:

- **Open web search (Tavily)** is used instead of paid market intelligence
  platforms such as Crunchbase, PitchBook, or CB Insights.

- **Model selection balances quality and cost efficiency.**
  Lightweight models (GPT-4o-mini) are used for research agents,
  while stronger reasoning models are reserved for synthesis.

- **Funding and market signals are derived from publicly available sources**
  rather than proprietary financial datasets.

- **Concurrency and retry behavior are intentionally conservative**
  to remain compatible with free-tier API limits.

These constraints ensure the project is **fully reproducible without requiring
paid services**, while still demonstrating the agent architecture,
reasoning workflow, and system design expected in a production system.

In a production deployment, these constraints would typically be replaced with:

- verified company intelligence APIs  
- structured market datasets  
- deeper financial data sources  
- stronger model tiers for research depth

## Project Structure
```
market-analyzer/
├── backend/
│   ├── main.py                    # FastAPI app, guardrails, routing
│   ├── config.py                  # API key validation
│   ├── requirements.txt
│   ├── .env.example
│   ├── agent_modules/
│   │   ├── incumbents.py          # Agent 1
│   │   ├── emerging.py            # Agent 2
│   │   ├── market_sizing.py       # Agent 3
│   │   └── synthesis.py           # Agent 4
│   ├── models/
│   │   └── schemas.py             # Pydantic models
│   └── tools/
│       └── search.py              # Tavily async wrapper
└── frontend/
    └── src/
        ├── App.tsx
        ├── api.ts
        ├── types.ts
        └── components/
            ├── InputForm.tsx
            ├── LoadingState.tsx
            ├── SynthesisCard.tsx
            ├── IncumbentsCard.tsx
            ├── EmergingCard.tsx
            └── MarketSizingCard.tsx
```