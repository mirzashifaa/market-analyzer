# Market Analyzer

A competitive intelligence system that analyzes any market to determine 
whether it is a fit for a given company. Provide a company and market — 
get a structured Go/No-Go recommendation backed by real research.

---

## Architecture
User Input (Company + Market)
        ↓
FastAPI Endpoint
        ↓
 ┌───────────────┬───────────────┬───────────────┐
 │ Incumbents    │ Emerging      │ Market Sizing │
 │ Research      │ Competitors   │ Research      │
 └───────────────┴───────────────┴───────────────┘
        ↓
     Synthesis Agent
        ↓
  GO / NO-GO Recommendation
---

## Agentic Strategy

**Research Orchestration**
Three research agents run in parallel — Incumbents, Emerging Competitors, 
and Market Sizing. Their outputs feed into a Synthesis agent which delivers 
the final recommendation.

**Data Grounding**
All agent outputs are validated against typed Pydantic schemas. 
The LLM cannot return free text — every response must match the 
defined structure or it fails validation.

**Tool Calling**
Each research agent uses Tavily web search to retrieve fresh data 
before reasoning. The agent decides when and what to search — 
the tool is not called manually.

---

## Synthesis Logic

The synthesis agent receives all three research outputs and cross-references 
them to identify white space. A Go recommendation requires:
- A clear positioning gap the entering company can realistically exploit
- A market large enough to justify entry
- Emerging competitor activity that validates demand without saturation

A No-Go is recommended when incumbents dominate without gaps, the market 
is shrinking, or capital velocity signals the window has closed.

---

## Key Design Decisions

**Why OpenAI Agents SDK over raw API calls**
Raw API calls are scripts, not agents. The SDK gives each agent a goal 
and tools — the agent decides how to use them. That is genuine agency.

**Why parallel execution**
Agents 1, 2, and 3 are independent. Parallel execution reduces analysis 
time without any architectural tradeoff.

**Why GPT-4o**
Accuracy matters more than cost for competitive intelligence. GPT-4o 
produces more reliable structured outputs and better reasoning.

**Why Tavily**
Purpose-built for LLM agents. Returns clean structured results designed 
to pass directly as context. Reduces noise compared to raw search APIs.

**Why a range for incumbents (4–6) not a fixed number**
Market structure varies. A fixed number forces padding or truncation. 
A range lets the agent reflect what is actually there.

**Why weakness and positioning_gaps are separate fields**
Weakness is company-specific. Positioning gaps are market-level. 
Mixing them produces vague output. Keeping them separate forces precision.

---

## Technical Tradeoffs

- Used GPT-4o for all agents — prioritized output quality over cost 
  given the assignment timeline
- No streaming implemented — chose full response return for reliability. 
  Streaming is a clear next step.
- LLM knowledge used for incumbents, web search for emerging competitors 
  and market sizing where freshness matters most

  **Search limitations**

Search-based research depends on search engine ranking and may 
occasionally omit niche players or return duplicate entity names. 
Multiple search queries and schema validation are used to reduce 
this risk.

---

## Setup

### Prerequisites
- Python 3.12+
- Node.js 18+
- OpenAI API key
- Tavily API key

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Add `.env` to `backend/`:
```
OPENAI_API_KEY=your_key
TAVILY_API_KEY=your_key
```
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

## Future Roadmap

- Streaming agent updates so frontend populates progressively
- Persistent storage to save and compare analyses over time
- User-provided company context for less well-known companies
- Confidence scoring per data point based on source quality

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI, Pydantic |
| Agent Framework | OpenAI Agents SDK |
| Web Search | Tavily |
| LLM | GPT-4o |
| Frontend | React, TypeScript |