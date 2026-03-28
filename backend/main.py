from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import logging

from models.schemas import AnalysisRequest, AnalysisResponse
from agent_modules.incumbents import run_incumbents_agent
from agent_modules.emerging import run_emerging_agent
from agent_modules.market_sizing import run_market_sizing_agent
from agent_modules.synthesis import run_synthesis_agent
from tenacity import retry, stop_after_attempt, wait_exponential
from openai import RateLimitError


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=5, max=30),
    reraise=True
)
async def run_analysis(
    company: str,
    market: str,
) -> AnalysisResponse:
    incumbents, emerging, market_sizing = await asyncio.gather(
        run_incumbents_agent(company, market),
        run_emerging_agent(company, market),
        run_market_sizing_agent(company, market),
    )
    synthesis = await run_synthesis_agent(
        company=company,
        market=market,
        incumbents=incumbents,
        emerging=emerging,
        market_sizing=market_sizing,
    )
    return incumbents, emerging, market_sizing, synthesis

app = FastAPI(
    title="Market Analyzer",
    description="AI-powered competitive intelligence for market entry decisions",
    version="1.0.0"
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
    logger.info(
        "Starting analysis: %s → %s",
        request.company,
        request.market,
    )

    try:
        logger.info("Running research agents in parallel...")
        incumbents, emerging, market_sizing = await asyncio.gather(
            run_incumbents_agent(
                request.company,
                request.market,
            ),
            run_emerging_agent(
                request.company,
                request.market,
            ),
            run_market_sizing_agent(
                request.company,
                request.market,
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
            detail="Rate limit reached. Please wait 30 seconds and try again."
        )

    except Exception as e:
        logger.exception(
            "Analysis failed for %s → %s",
            request.company,
            request.market,
        )
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        ) from e