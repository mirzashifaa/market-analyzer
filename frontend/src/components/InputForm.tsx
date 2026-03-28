import { useState } from "react";
import type { AnalysisRequest } from "../types";
import "./InputForm.css";

interface Props {
  onSubmit: (request: AnalysisRequest) => void;
  loading: boolean;
}

export function InputForm({ onSubmit, loading }: Props) {
  const [company, setCompany] = useState("");
  const [market, setMarket] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (company.trim() && market.trim()) {
      onSubmit({ company: company.trim(), market: market.trim() });
    }
  };

  const canSubmit = company.trim().length >= 2 && market.trim().length >= 2 && !loading;

  return (
    <form className="input-form" onSubmit={handleSubmit}>
      <div className="input-group">
        <label className="input-label">Company</label>
        <input
          className="input-field"
          type="text"
          value={company}
          onChange={(e) => setCompany(e.target.value)}
          placeholder="e.g. Shopify"
          disabled={loading}
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
          placeholder="e.g. HR software"
          disabled={loading}
        />
      </div>

      <button
        className="submit-btn"
        type="submit"
        disabled={!canSubmit}
      >
        {loading ? (
          <span className="btn-loading">
            <span className="loading-dot" />
            <span className="loading-dot" />
            <span className="loading-dot" />
          </span>
        ) : (
          "Analyze Market"
        )}
      </button>
    </form>
  );
}
