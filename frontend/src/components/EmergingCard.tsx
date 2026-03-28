import type { EmergingCompetitorsOutput } from "../types";
import "./ResearchCard.css";

interface Props {
  data: EmergingCompetitorsOutput;
}

const velocityColor = {
  high: "var(--nogo)",
  medium: "var(--amber)",
  low: "var(--go)",
};

export function EmergingCard({ data }: Props) {
  return (
    <div className="research-card">
      <div className="research-card-header">
        <div className="card-title-group">
          <span className="card-number">02</span>
          <h2 className="card-title">Emerging Competitors</h2>
        </div>
        <div className="card-meta">
          <span
            className="meta-tag velocity"
            style={{ color: velocityColor[data.capital_velocity] }}
          >
            Capital Velocity: {data.capital_velocity}
          </span>
        </div>
      </div>

      <div className="card-summary">{data.trend_summary}</div>

      <div className="competitors-list">
        {data.competitors.map((c) => (
          <div key={c.name} className="competitor-row">
            <div className="competitor-left">
              <div className="competitor-name">{c.name}</div>
              <div className="competitor-focus">{c.focus}</div>
            </div>
            <div className="competitor-middle">
              <span className={`stage-badge ${c.stage.toLowerCase().replace(" ", "-")}`}>
                {c.stage}
              </span>
              <span className="funding-amount">{c.funding}</span>
            </div>
            <div className="competitor-signal">{c.why_it_matters}</div>
          </div>
        ))}
      </div>

      <div className="velocity-section">
        <div className="velocity-label">Velocity Evidence</div>
        <div className="velocity-text">{data.velocity_reasoning}</div>
      </div>

      <div className="funding-signals">
        <div className="signals-label">Recent Funding Signals</div>
        <div className="signals-list">
          {data.recent_funding.map((signal, i) => (
            <div key={i} className="signal-item">{signal}</div>
          ))}
        </div>
      </div>
    </div>
  );
}
