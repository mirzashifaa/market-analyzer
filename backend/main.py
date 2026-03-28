from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import logging
from typing import Iterable

from tenacity import retry, stop_after_attempt, wait_exponential
from openai import RateLimitError

from models.schemas import (
    AnalysisRequest,
    AnalysisResponse,
    SynthesisOutput,
)
from agent_modules.incumbents import run_incumbents_agent
from agent_modules.emerging import run_emerging_agent
from agent_modules.market_sizing import run_market_sizing_agent
from agent_modules.synthesis import run_synthesis_agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def normalize_name(value: str) -> str:
    return "".join(
        ch.lower() for ch in value if ch.isalnum() or ch.isspace()
    ).strip()

BROAD_MARKET_INPUTS = {
    "enterprise software",
    "ai software",
    "business software",
    "productivity tools",
    "productivity software",
    "software",
    "technology",
    "saas",
    "ai tools",
    "tech",
    "digital tools",
    "cloud software",
    "business tools",
}

def is_market_too_broad(market: str) -> bool:
    return normalize_name(market) in BROAD_MARKET_INPUTS

def is_company_already_in_market(
    company: str,
    market_leader: str,
    player_names: Iterable[str],
) -> bool:
    company_norm = normalize_name(company)
    market_leader_norm = normalize_name(market_leader)

    if (
        company_norm == market_leader_norm
        or company_norm in market_leader_norm
        or market_leader_norm in company_norm
    ):
        return True

    for name in player_names:
        name_norm = normalize_name(name)
        if (
            company_norm == name_norm
            or company_norm in name_norm
            or name_norm in company_norm
        ):
            return True

    return False


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=5, max=30),
    reraise=True,
)
async def run_analysis(
    company: str,
    market: str,
):
    incumbents, emerging, market_sizing = await asyncio.gather(
        run_incumbents_agent(company, market),
        run_emerging_agent(company, market),
        run_market_sizing_agent(company, market),
    )

    return incumbents, emerging, market_sizing


app = FastAPI(
    title="Market Analyzer",
    description="AI-powered competitive intelligence for market entry decisions",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalysisResponse, tags=["analysis"])
async def analyze(request: AnalysisRequest) -> AnalysisResponse:
    """
    Run full market analysis for a company entering a target market.
    Executes research agents in parallel and synthesizes results.
    """
    if is_market_too_broad(request.market):
        raise HTTPException(
            status_code=400,
            detail=(
                f"'{request.market}' is too broad for accurate analysis. "
                "Please provide a specific market category — "
                "for example: 'payroll software', 'video editing software', "
                "or 'applicant tracking software'."
            ),
        )
        
    logger.info(
        "Starting analysis: %s → %s",
        request.company,
        request.market,
    )

    try:
        logger.info("Running research agents with retry wrapper...")
        incumbents, emerging, market_sizing = await run_analysis(
            request.company,
            request.market,
        )

        already_in_market = is_company_already_in_market(
            company=request.company,
            market_leader=incumbents.market_leader,
            player_names=[player.name for player in incumbents.players],
        )

        if already_in_market:
            logger.info(
                "Already-in-market guardrail triggered for %s → %s",
                request.company,
                request.market,
            )

            return AnalysisResponse(
                company=request.company,
                market=request.market,
                incumbents=incumbents,
                emerging_competitors=emerging,
                market_sizing=market_sizing,
                synthesis=SynthesisOutput(
                    recommendation="NO-GO",
                    confidence="high",
                    reasoning=(
                        f"{request.company} already competes in the "
                        f"{request.market} category as an established player. "
                        "This is not a new market entry scenario; it is better "
                        "understood as expansion, defense, or repositioning "
                        "within an existing market."
                    ),
                    white_space_assessment=(
                        "Company already operates in this category. "
                        "Fresh market-entry white space does not apply."
                    ),
                    competitive_pressure=(
                        "The company is already an incumbent or category participant, "
                        "so this is not a standard entry-versus-incumbents scenario."
                    ),
                    market_attractiveness=(
                        "The market may still be attractive, but the decision is not "
                        "about entering a new category."
                    ),
                    key_opportunities=[
                        "Expand product capabilities within the category",
                        "Defend position against emerging competitors",
                        "Strengthen differentiation in adjacent sub-segments",
                    ],
                    key_risks=[
                        "Incumbent pressure from adjacent or niche competitors",
                        "Need to keep pace with category innovation",
                        "Risk of misframing expansion as new market entry",
                    ],
                ),
            )

        logger.info("Research complete. Running synthesis...")

        synthesis = await run_synthesis_agent(
            company=request.company,
            market=request.market,
            incumbents=incumbents,
            emerging=emerging,
            market_sizing=market_sizing,
        )

        logger.info(
            "Analysis complete: %s",
            synthesis.recommendation,
        )

        return AnalysisResponse(
            company=request.company,
            market=request.market,
            incumbents=incumbents,
            emerging_competitors=emerging,
            market_sizing=market_sizing,
            synthesis=synthesis,
        )

    except RateLimitError:
        logger.warning(
            "Rate limit hit for %s → %s",
            request.company,
            request.market,
        )
        raise HTTPException(
            status_code=429,
            detail="Rate limit reached. Please wait 30 seconds and try again.",
        )

    except Exception as e:
        logger.exception(
            "Analysis failed for %s → %s",
            request.company,
            request.market,
        )
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}",
        ) from e