import type { SynthesisOutput } from "../types";
import "./SynthesisCard.css";

interface Props {
  data: SynthesisOutput;
  company: string;
  market: string;
}

export function SynthesisCard({ data, company, market }: Props) {
  const isGo = data.recommendation === "GO";

  return (
    <div className={`synthesis-card ${isGo ? "go" : "nogo"}`}>
      <div className="synthesis-header">
        <div className="synthesis-meta">
          <span className="synthesis-label">Opportunity Assessment</span>
          <span className="synthesis-query">
            {company} → {market}
          </span>
        </div>
        <div className="synthesis-verdict">
          <div className={`verdict-text ${isGo ? "go" : "nogo"}`}>
            {data.recommendation}
          </div>
          <div className={`confidence-badge ${data.confidence}`}>
            {data.confidence.toUpperCase()} CONFIDENCE
          </div>
        </div>
      </div>

      <div className="synthesis-reasoning">
        <p>{data.reasoning}</p>
      </div>

      <div className="synthesis-signals">
        <div className="signal-block">
          <div className="signal-label">White Space</div>
          <div className="signal-value">{data.white_space_assessment}</div>
        </div>
        <div className="signal-block">
          <div className="signal-label">Competitive Pressure</div>
          <div className="signal-value">{data.competitive_pressure}</div>
        </div>
        <div className="signal-block">
          <div className="signal-label">Market Attractiveness</div>
          <div className="signal-value">{data.market_attractiveness}</div>
        </div>
      </div>

      <div className="synthesis-lists">
        <div className="synthesis-list">
          <div className="list-header opportunities">Key Opportunities</div>
          <ul>
            {data.key_opportunities.map((item, i) => (
              <li key={i}>{item}</li>
            ))}
          </ul>
        </div>

        <div className="synthesis-list">
          <div className="list-header risks">Key Risks</div>
          <ul>
            {data.key_risks.map((item, i) => (
              <li key={i}>{item}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
