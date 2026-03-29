import { useState } from "react";
import type { AnalysisRequest } from "../types";
import "./InputForm.css";

interface Props {
  onSubmit: (request: AnalysisRequest) => void;
}

// Keep in sync with BROAD_MARKET_INPUTS in backend/main.py
const BROAD_MARKETS = new Set([
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
]);

const isTooBroad = (market: string): boolean =>
  BROAD_MARKETS.has(market.toLowerCase().trim());

export function InputForm({ onSubmit }: Props) {
  const [company, setCompany] = useState("");
  const [market, setMarket] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (company.trim() && market.trim()) {
      onSubmit({ company: company.trim(), market: market.trim() });
    }
  };

  const canSubmit =
  company.trim().length >= 2 &&
  market.trim().length >= 2 &&
  !isTooBroad(market);

  return (
    <div className="input-form-wrapper">
      <form className="input-form" onSubmit={handleSubmit}>
        <div className="input-group">
          <label className="input-label">Company</label>
          <input
            className="input-field"
            type="text"
            value={company}
            onChange={(e) => setCompany(e.target.value)}
            placeholder="e.g. Shopify"
            disabled={false}
            autoFocus
          />
        </div>

        <div className="input-divider">
          <span className="input-arrow">→</span>
        </div>

        <div className="input-group">
          <label className="input-label">Market</label>
          <input
            className="input-field"
            type="text"
            value={market}
            onChange={(e) => setMarket(e.target.value)}
            placeholder="e.g. payroll software"
            disabled={false}
          />
        </div>

        <button
          className="submit-btn"
          type="submit"
          disabled={!canSubmit}
        >
        Analyze Market
        </button>
      </form>

      {isTooBroad(market) && (
        <div className="input-warning">
          ⚠ Market is too broad — try "payroll software" or "video editing software"
        </div>
      )}
    </div>
  );
}
