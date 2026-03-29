import type { MarketSizingOutput } from "../types";
import "./ResearchCard.css";

interface Props {
  data: MarketSizingOutput;
}

export function MarketSizingCard({ data }: Props) {
  return (
    <div className="research-card">
      <div className="research-card-header">
        <div className="card-title-group">
          <span className="card-number">03</span>
          <h2 className="card-title">Market Sizing</h2>
        </div>
        <div className="card-meta">
          <span className={`meta-tag confidence-${data.sizing_confidence}`}>
            {data.sizing_confidence.toUpperCase()} CONFIDENCE
          </span>
        </div>
      </div>

      <div className="market-metrics">
        <div className="metric-block">
          <div className="metric-label">TAM</div>
          <div className="metric-value">{data.tam}</div>
        </div>
        <div className="metric-block">
          <div className="metric-label">SAM</div>
          <div className="metric-value">{data.sam}</div>
        </div>
        <div className="metric-block">
          <div className="metric-label">Growth Rate</div>
          <div className="metric-value growth">{data.growth_rate}</div>
        </div>
      </div>

      <div className="projection-block">
        <div className="projection-label">Projection</div>
        <div className="projection-text">{data.projection}</div>
      </div>

      <div className="drivers-risks">
        <div className="drivers-col">
          <div className="dr-label positive">Growth Drivers</div>
          <ul className="dr-list">
            {data.key_drivers.map((d, i) => (
              <li key={i}>{d}</li>
            ))}
          </ul>
        </div>
        <div className="risks-col">
          <div className="dr-label negative">Market Risks</div>
          <ul className="dr-list">
            {data.key_risks.map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>
        </div>
      </div>

      <div className="sources-section">
        <div className="sources-label">Sources</div>
        <div className="sources-list">
          {data.sources.map((s, i) => (
            <div key={i} className="source-item">
              {s}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
