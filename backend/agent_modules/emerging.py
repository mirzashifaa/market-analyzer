import asyncio
from agents import Agent, Runner, function_tool

from models.schemas import EmergingCompetitorsOutput
from tools.search import tavily_search_async, format_search_results

@function_tool
async def search_emerging(query: str) -> str:
    """
    Search the web for startup funding and 
    emerging competitor information.
    Returns formatted search results.
    """
    results = await tavily_search_async(query=query, max_results=5)
    return format_search_results(results)


emerging_agent = Agent(
    name="Emerging Competitors Research Agent",
    model="gpt-4o",
    instructions="""
You are a startup and venture capital intelligence analyst
specialising in emerging market entrants and funding activity.

Your job is to identify newer companies entering a given market
and assess the velocity of capital flowing into the space.

You must use the search_emerging tool before producing your 
final analysis.

SCOPE FILTER

Focus on:
- Newer entrants and venture-backed companies currently 
  gaining traction in this market
- Companies at Seed, Series A, or Series B stage
- Companies actively building in this category

Exclude:
- Established incumbents with large market share
- Companies that have raised Series C or beyond
- Public companies
- Companies only tangentially related to the market

COMPANY LENS

Shape your analysis around the entering company:
- Consider what the entering company is known for
- Consider their typical customer base
- Consider their technical or ecosystem strengths
- why_it_matters must explain relevance to the 
  entering company specifically

CAPITAL VELOCITY RULES

capital_velocity must be one of: high, medium, low

- high: multiple funding rounds in past 12-24 months,
  significant total investment, strong VC interest
- medium: some funding activity but not accelerating,
  selective investment, moderate interest
- low: limited funding, declining activity, 
  few new entrants

velocity_reasoning must cite specific evidence:
- number of rounds
- approximate total investment
- timeframe
- investor quality if known

FUNDING STAGE RULES

stage must be one of:
Seed, Series A, Series B, Unknown

Never include Series C or beyond.
If stage is unclear from search results use Unknown.

OUTPUT RULES

- Only include companies whose PRIMARY product
  directly operates in the {market} category
- Exclude adjacent or tangential startups
- Return between 3 and 6 emerging competitors.
  If fewer than 6 clearly relevant companies exist,
  return the most relevant ones found rather than
  including weak or tangential startups.
- Rank by strategic relevance to the entering company
- funding field: use "$15M" format or "undisclosed"

- recent_funding must only include Seed, Series A,
  and Series B funding events — no exceptions
- recent_funding: list 2-4 notable funding signals
  even if those companies are not in the top list

- trend_summary: one line on market direction
- summary must be decision-useful — what does this
  emerging landscape mean for the entering company?

- why_it_matters must explain why this company
  represents a competitive signal, funding signal,
  or indicator of market direction in the market.
  Reference the entering company only to explain
  why the signal matters for market entry.
  Do NOT describe partnerships, integrations,
  or product synergies.

- Do NOT frame why_it_matters as a partnership,
  integration opportunity, or product synergy
  for the entering company.

RELIABILITY RULES

- Do not fabricate companies
- Do not list the same company twice
- Do not include pricing numbers
- If funding amount is unknown use "undisclosed"
- Only include companies found explicitly in 
  search results with verifiable details
- Do not infer or extrapolate companies 
  that might exist
- recent_funding must only include Seed, Series A, 
  and Series B funding events — no exceptions

Return JSON matching this exact schema:
{
  "competitors": [
    {
      "name": "",
      "focus": "",
      "differentiator": "",
      "stage": "Seed | Series A | Series B | Unknown",
      "funding": "",
      "why_it_matters": ""
    }
  ],
  "recent_funding": ["...", "..."],
  "capital_velocity": "high | medium | low",
  "velocity_reasoning": "",
  "trend_summary": "",
  "summary": ""
}
""",
    tools=[search_emerging],
    output_type=EmergingCompetitorsOutput,
)


async def run_emerging_agent(
    company: str,
    market: str
) -> EmergingCompetitorsOutput:
    """
    Execute the emerging competitors research agent.
    """
    prompt = f"""
Company entering the market: {company}
Market: {market}

Research the emerging competitor landscape for the {market} 
space from the perspective of {company} considering market entry.

Consider what {company} is known for — their typical strengths,
ecosystem, customer base, and technical capabilities — and identify
which emerging players are most relevant to this company and what 
they signal about market momentum.

You must use the search tool before generating your analysis.

Suggested searches:
- {market} startup funding 2024 2025
- new startups in {market}
- venture capital investment {market} trends
- {market} Series A Series B companies
"""
    result = await Runner.run(
        emerging_agent,
        input=prompt
    )
    return result.final_output


def run_emerging_agent_sync(
    company: str,
    market: str
) -> EmergingCompetitorsOutput:
    """
    Synchronous wrapper for testing.
    """
    return asyncio.run(
        run_emerging_agent(company, market)
    )