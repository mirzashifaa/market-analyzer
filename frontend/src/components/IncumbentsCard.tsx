import { useState } from "react";
import type { IncumbentsOutput } from "../types";
import "./ResearchCard.css";

interface Props {
  data: IncumbentsOutput;
}

export function IncumbentsCard({ data }: Props) {
  const [expanded, setExpanded] = useState(false);
  const visible = expanded ? data.players : data.players.slice(0, 3);

  return (
    <div className="research-card">
      <div className="research-card-header">
        <div className="card-title-group">
          <span className="card-number">01</span>
          <h2 className="card-title">Incumbents</h2>
        </div>
        <div className="card-meta">
          <span className="meta-tag">Market Leader: {data.market_leader}</span>
        </div>
      </div>

      <div className="card-summary">{data.summary}</div>

      <div className="gap-highlight">
        <span className="gap-label">Positioning Gap</span>
        <span className="gap-text">{data.positioning_gaps}</span>
      </div>

      <div className="players-table">
        <div className="table-header">
          <span>Company</span>
          <span>Target</span>
          <span>Strength</span>
          <span>Weakness</span>
        </div>
        {visible.map((player) => (
          <div key={player.name} className="table-row">
            <div className="player-name-cell">
              <div className="player-name">{player.name}</div>
              <div className="player-product">{player.product}</div>
            </div>
            <div className="table-cell muted">{player.target_customer}</div>
            <div className="table-cell positive">{player.strength}</div>
            <div className="table-cell negative">{player.weakness}</div>
          </div>
        ))}
      </div>

      {data.players.length > 3 && (
        <button className="expand-btn" onClick={() => setExpanded(!expanded)}>
          {expanded ? "Show less" : `+${data.players.length - 3} more`}
        </button>
      )}
    </div>
  );
}
