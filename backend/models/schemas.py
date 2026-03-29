from pydantic import BaseModel, Field
from typing import Literal

# --- Incumbents ---


class Incumbent(BaseModel):
    name: str
    product: str
    target_customer: str
    positioning: str
    key_features: list[str]
    strength: str
    weakness: str


class IncumbentsOutput(BaseModel):
    players: list[Incumbent]
    market_leader: str
    positioning_gaps: str
    summary: str


# --- Emerging Competitors ---


class EmergingCompetitor(BaseModel):
    name: str
    focus: str
    differentiator: str
    stage: Literal["Seed", "Series A", "Series B", "Unknown"]
    funding: str
    why_it_matters: str


class EmergingCompetitorsOutput(BaseModel):
    competitors: list[EmergingCompetitor]
    recent_funding: list[str]
    capital_velocity: Literal["high", "medium", "low"]
    velocity_reasoning: str
    trend_summary: str
    summary: str


# --- Market Sizing ---


class MarketSizingOutput(BaseModel):
    tam: str
    sam: str
    growth_rate: str
    projection: str
    key_drivers: list[str]
    key_risks: list[str]
    sources: list[str]
    sizing_confidence: Literal["high", "medium", "low"]


# --- Synthesis ---


class SynthesisOutput(BaseModel):
    recommendation: Literal["GO", "NO-GO"]
    confidence: Literal["high", "medium", "low"]
    white_space_assessment: str
    competitive_pressure: str
    market_attractiveness: str
    reasoning: str
    key_opportunities: list[str]
    key_risks: list[str]


# --- API Request / Response ---


class AnalysisRequest(BaseModel):
    company: str = Field(min_length=2, max_length=100)
    market: str = Field(min_length=2, max_length=200)


class AnalysisResponse(BaseModel):
    company: str
    market: str
    incumbents: IncumbentsOutput
    emerging_competitors: EmergingCompetitorsOutput
    market_sizing: MarketSizingOutput
    synthesis: SynthesisOutput
