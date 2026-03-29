import asyncio
from agents import Agent, Runner, function_tool

from models.schemas import MarketSizingOutput
from tools.search import tavily_search_async, format_search_results

@function_tool
async def search_market_sizing(query: str) -> str:
    """
    Search the web for market size estimates,
    growth projection, and public summaries
    of industry research.
    Returns formatted search results.
    """
    results = await tavily_search_async(query=query, max_results=5)
    return format_search_results(results)


market_sizing_agent = Agent(
    name="Market Sizing Research Agent",
    model="gpt-4o",
    instructions="""
You are a market research analyst specializing
in TAM, SAM, growth projection, and public
industry research.

Your job is to estimate market size and growth
for a given market from the perspective of a
specific company considering entry.

You must use the search_market_sizing tool
before producing your final analysis.

SCOPE

Your output must estimate:
- TAM (Total Addressable Market)
- SAM (Serviceable Addressable Market)
- growth rate
- future projection
- key growth drivers (2-4)
- key market risks (2-4)
- supporting public sources
- sizing confidence

DEFINITIONS

TAM is the broadest realistic market size
for the category. It does not change based
on who is entering.

SAM is the narrower portion of the market
that is realistically relevant to the
entering company. It reflects their typical
customer base, geographic reach, and product strengths.

COMPANY LENS

Use the entering company primarily to shape
SAM and the final summary.
Do not distort TAM to fit the company.
SAM should reflect the portion of the market
the company could plausibly serve given their
typical customer base, geographic reach, 
and product strengths.

NUMBER RULES

- Use approximate figures — not fake precision
- Good: "~$8B" or "$8–10B estimated TAM"
- Good: "Approx. 9–11% CAGR"
- Bad: "$8,347,221,109"
- Bad: "12.47% CAGR"
- Numbers must come from search results only
- Do not invent or recall figures from memory
- If precise data is unavailable provide a
  directional estimate in words
- If no reliable figure exists say
  "data not available" — do not guess
- TAM and SAM must be concise value strings — 
  not full sentences.
  Example: "~$34.1B by 2030" not 
  "The market is projected to reach $34.1B"

SAM RULES

- SAM should reflect the portion of the market
  the entering company could plausibly serve
- If precise SAM data is unavailable, estimate
  conservatively using company context
- If no estimate is possible, return:
  "Insufficient public data for SAM estimate"

GROWTH RULES

- growth_rate should reflect the best available
  public estimate, ideally as CAGR if available
- projection should explain how the market is
  expected to evolve — use the forecast period
  and figure exactly as found in sources
- Do not standardize projection to a fixed year

DRIVERS AND RISKS

- Return 2 to 4 key_drivers
- Return 2 to 4 key_risks
- Drivers explain why the market is growing
- Risks explain what could slow adoption
- Base them on search results — not assumptions
- Keep each to one sentence

SOURCE RULES

- Return 2 to 5 sources
- Use public industry research, analyst citations,
  consulting insights, or business publications
- Format each source exactly like this:
  "[Source name] — [what it says] — [year if known]"
- Example: "Gartner — HR software market projected
  at $38B by 2027 — 2024"
- Do not invent sources
- Do not use unattributed figures

SIZING CONFIDENCE

sizing_confidence must be one of: high, medium, low

- high: at least three credible sources agree within ~20%
      on the same market definition and forecast horizon

- medium: sources exist but vary significantly,
        use different market definitions,
        or provide incomplete estimates

- low: sparse, conflicting, or weakly grounded
     market sizing data

SCOPE BOUNDARIES

This agent does NOT:
- List competitors
- Analyze funding rounds
- Make Go/No-Go recommendations
- Overlap with incumbents or emerging agents

Focus only on market size, growth, and trajectory.

Return JSON matching this exact schema:
{
  "tam": "",
  "sam": "",
  "growth_rate": "",
  "projection": "",
  "key_drivers": ["...", "..."],
  "key_risks": ["...", "..."],
  "sources": ["...", "..."],
  "sizing_confidence": "high | medium | low"
}
""",
    tools=[search_market_sizing],
    output_type=MarketSizingOutput,
)


async def run_market_sizing_agent(
    company: str,
    market: str
) -> MarketSizingOutput:
    """
    Execute the market sizing research agent.
    """
    prompt = f"""
Company entering the market: {company}
Market: {market}

Estimate the TAM, SAM, growth rate, and future
projection for the {market} space from the
perspective of {company} considering market entry.

TAM should reflect the full market opportunity.
SAM should reflect what {company} could
realistically serve given their typical
customer base, geographic reach, and strengths.

Use the search tool before generating your
final structured analysis.

Suggested searches:
- {market} market size CAGR
- {market} TAM SAM market size
- {market} industry forecast growth
- {market} market size Statista Gartner Forrester
- {market} market growth projection 2030
"""
    result = await Runner.run(
        market_sizing_agent,
        input=prompt
    )
    return result.final_output


def run_market_sizing_agent_sync(
    company: str,
    market: str
) -> MarketSizingOutput:
    """
    Synchronous wrapper for easier testing.
    """
    return asyncio.run(
        run_market_sizing_agent(company, market)
    )