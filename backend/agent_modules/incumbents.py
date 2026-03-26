import asyncio
from agents import Agent, Runner, function_tool

from models.schemas import IncumbentsOutput
from tools.search import tavily_search, format_search_results


@function_tool
def search_incumbents(query: str) -> str:
    """
    Search the web for incumbent market context.
    Returns formatted search results.
    """
    results = tavily_search(query=query, max_results=5)
    return format_search_results(results)


incumbents_agent = Agent(
    name="Incumbents Research Agent",
    model="gpt-4o",
    instructions="""
You are a competitive intelligence analyst specializing in enterprise market research.

Your task is to analyze the incumbent landscape in a given market from the perspective
of a specific company considering entry.

You must use the search_incumbents tool before producing your final analysis.

ENTERPRISE FILTER

Only include companies where:
- The product is a core offering in this category
- The platform is widely adopted by mid-market or enterprise customers
- The company has significant market presence

Avoid tools primarily built for individuals or very small teams.

COMPANY LENS

Shape the analysis around the entering company:

- Consider what the entering company is known for
- Consider their typical customer base
- Consider their technical or ecosystem strengths

Identify where incumbents leave gaps that the entering company could realistically exploit.

The analysis should feel different depending on who is entering the market.

WHITE SPACE RULES

positioning_gaps must describe a **specific underserved opportunity** in the market.

Valid examples include:
- an underserved customer segment
- a missing workflow capability
- an integration gap
- a vertical-specific requirement
- a complexity or pricing mismatch

Bad example:
"No tool is both powerful and simple."

Good example:
"No dominant platform serves developer-first teams that require HR automation
with deep API integration."

OUTPUT RULES

- Identify **4–6 major established players** in this market.
- Each player must include:
  name, product, target_customer, positioning, key_features, strength, weakness.

- weakness must be **specific to that company only**.

- positioning_gaps must describe a **market-level gap across incumbents**, not a weakness of a single company.

- market_leader must reflect **category dominance**, not overall brand size.

- Do not prioritize the entering company as market leader unless they clearly dominate this category.

RELIABILITY RULES

- Do not fabricate companies.
- Do not list the same company or product twice under different names.
- If a product belongs to a larger company, list it only once using the most recognized brand.

SUMMARY RULE

The summary must be **decision-useful**:
briefly explain what this competitive landscape means for the entering company.

Return JSON matching this exact schema:

{
  "players": [
    {
      "name": "",
      "product": "",
      "target_customer": "",
      "positioning": "",
      "key_features": ["...", "...", "..."],
      "strength": "",
      "weakness": ""
    }
  ],
  "market_leader": "",
  "positioning_gaps": "",
  "summary": ""
}
""",
    tools=[search_incumbents],
    output_type=IncumbentsOutput,
)


async def run_incumbents_agent(
    company: str,
    market: str
) -> IncumbentsOutput:
    """
    Execute the incumbents research agent.
    """
    prompt = f"""
Company entering the market: {company}
Market: {market}

Research the incumbent landscape for the {market} space from the perspective
of {company} considering market entry.

Consider what {company} is known for — their typical strengths, ecosystem,
customer base, and technical capabilities — and identify where incumbents
leave gaps that {company} could realistically exploit.

Use the search tool before generating your final structured analysis.

Suggested searches:
- top {market} enterprise companies comparison
- leading {market} platforms enterprise market overview
"""

    result = await Runner.run(
        incumbents_agent,
        input=prompt
    )

    return result.final_output


def run_incumbents_agent_sync(
    company: str,
    market: str
) -> IncumbentsOutput:
    """
    Synchronous wrapper for easier testing.
    """
    return asyncio.run(
        run_incumbents_agent(company, market)
    )