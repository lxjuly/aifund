"""Minimal governed research demo for AIfund.

This demo shows the intended platform flow:

    intent -> semantic plan -> dry-run validation -> recommendation trace

It is intentionally lightweight. The goal is to demonstrate the architecture
before connecting the flow to live market data, model inference, or trading
workflows.
"""

from dataclasses import asdict, dataclass, field
from typing import List


@dataclass
class SemanticPlan:
    intent: str
    subject: str
    candidate_universe: List[str]
    agents: List[str]
    entities: List[str]
    metrics: List[str]


@dataclass
class DryRunResult:
    approved: bool
    policy_checks: List[str]
    entities_touched: List[str]
    metrics_touched: List[str]
    risk_notes: List[str] = field(default_factory=list)


@dataclass
class Recommendation:
    asset: str
    score: float
    rationale: str
    provenance: List[str]


class PortfolioMixer:
    """Coordinates candidate retrieval, semantic validation, and selection."""

    def plan(self, intent: str, subject: str) -> SemanticPlan:
        return SemanticPlan(
            intent=intent,
            subject=subject,
            candidate_universe=["AMD", "AVGO", "TSM", "MSFT"],
            agents=["fundamental_agent", "sentiment_agent", "technical_agent", "risk_agent"],
            entities=["company", "security", "earnings_report", "news_item", "sector"],
            metrics=["revenue_growth", "momentum_score", "sentiment_score", "volatility"],
        )

    def dry_run(self, plan: SemanticPlan) -> DryRunResult:
        policy_checks = [
            "semantic_entities_registered",
            "metrics_registered",
            "recommendation_requires_provenance",
            "risk_agent_required_for_selection",
        ]

        return DryRunResult(
            approved=True,
            policy_checks=policy_checks,
            entities_touched=plan.entities,
            metrics_touched=plan.metrics,
            risk_notes=["portfolio concentration check required before execution"],
        )

    def select(self, plan: SemanticPlan, dry_run: DryRunResult) -> Recommendation:
        if not dry_run.approved:
            raise RuntimeError("Plan was rejected by governed dry run")

        return Recommendation(
            asset="AVGO",
            score=0.84,
            rationale=(
                "Selected as a high-conviction NVDA-adjacent candidate based on "
                "fundamental quality, semiconductor exposure, momentum, and manageable risk."
            ),
            provenance=[
                f"intent:{plan.intent}",
                "source:candidate_universe",
                "agent:fundamental_agent",
                "agent:sentiment_agent",
                "agent:technical_agent",
                "agent:risk_agent",
                "policy:recommendation_requires_provenance",
                "dry_run:approved",
            ],
        )


if __name__ == "__main__":
    mixer = PortfolioMixer()

    plan = mixer.plan(
        intent="Find attractive NVDA alternatives",
        subject="NVDA",
    )
    dry_run = mixer.dry_run(plan)
    recommendation = mixer.select(plan, dry_run)

    print("=== Semantic Plan ===")
    print(asdict(plan))
    print("\n=== Governed Dry Run ===")
    print(asdict(dry_run))
    print("\n=== Recommendation ===")
    print(asdict(recommendation))
