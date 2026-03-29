import "./LoadingState.css";

interface Props {
  company: string;
  market: string;
}

export function LoadingState({ company, market }: Props) {
  return (
    <div className="loading-state">
      <div className="loading-header">
        <div className="loading-label">Analyzing</div>
        <div className="loading-query">
          {company} <span className="loading-arrow">→</span> {market}
        </div>
      </div>

      <div className="loading-steps">
        <div className="loading-step">
          <div className="step-indicator active" />
          <div className="step-text">Researching incumbent landscape</div>
        </div>
        <div className="loading-step">
          <div
            className="step-indicator active"
            style={{ animationDelay: "0.3s" }}
          />
          <div className="step-text">
            Scanning emerging competitors & funding
          </div>
        </div>
        <div className="loading-step">
          <div
            className="step-indicator active"
            style={{ animationDelay: "0.6s" }}
          />
          <div className="step-text">Estimating market size & growth</div>
        </div>
        <div className="loading-step">
          <div
            className="step-indicator active"
            style={{ animationDelay: "0.9s" }}
          />
          <div className="step-text">Synthesizing opportunity assessment</div>
        </div>
      </div>

      <div className="loading-note">
        This analysis typically takes 30–60 seconds
      </div>
    </div>
  );
}
