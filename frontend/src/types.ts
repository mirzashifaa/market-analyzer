export interface Incumbent {
    name: string;
    product: string;
    target_customer: string;
    positioning: string;
    key_features: string[];
    strength: string;
    weakness: string;
  }
  
  export interface IncumbentsOutput {
    players: Incumbent[];
    market_leader: string;
    positioning_gaps: string;
    summary: string;
  }
  
  export interface EmergingCompetitor {
    name: string;
    focus: string;
    differentiator: string;
    stage: "Seed" | "Series A" | "Series B" | "Unknown";
    funding: string;
    why_it_matters: string;
  }
  
  export interface EmergingCompetitorsOutput {
    competitors: EmergingCompetitor[];
    recent_funding: string[];
    capital_velocity: "high" | "medium" | "low";
    velocity_reasoning: string;
    trend_summary: string;
    summary: string;
  }
  
  export interface MarketSizingOutput {
    tam: string;
    sam: string;
    growth_rate: string;
    projection: string;
    key_drivers: string[];
    key_risks: string[];
    sources: string[];
    sizing_confidence: "high" | "medium" | "low";
  }
  
  export interface SynthesisOutput {
    recommendation: "GO" | "NO-GO";
    confidence: "high" | "medium" | "low";
    white_space_assessment: string;
    competitive_pressure: string;
    market_attractiveness: string;
    reasoning: string;
    key_opportunities: string[];
    key_risks: string[];
  }
  
  export interface AnalysisResponse {
    company: string;
    market: string;
    incumbents: IncumbentsOutput;
    emerging_competitors: EmergingCompetitorsOutput;
    market_sizing: MarketSizingOutput;
    synthesis: SynthesisOutput;
  }
  
  export interface AnalysisRequest {
    company: string;
    market: string;
  }