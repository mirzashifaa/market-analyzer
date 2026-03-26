from pydantic import BaseModel
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