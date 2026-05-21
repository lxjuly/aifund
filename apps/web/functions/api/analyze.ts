type SemanticPlan = {
  intent: string;
  subject: string;
  candidateUniverse: string[];
  agents: string[];
  entities: string[];
  metrics: string[];
};

type DryRunResult = {
  approved: boolean;
  policyChecks: string[];
  entitiesTouched: string[];
  metricsTouched: string[];
  riskNotes: string[];
};

type Recommendation = {
  asset: string;
  score: number;
  rationale: string;
  provenance: string[];
};

type AnalyzeResponse = {
  semanticPlan: SemanticPlan;
  dryRun: DryRunResult;
  recommendation: Recommendation;
};

const jsonHeaders = {
  "content-type": "application/json; charset=utf-8",
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "GET, POST, OPTIONS",
  "access-control-allow-headers": "content-type",
};

function buildSemanticPlan(intent: string, subject: string): SemanticPlan {
  return {
    intent,
    subject,
    candidateUniverse: ["AMD", "AVGO", "TSM", "MSFT"],
    agents: [
      "fundamental_agent",
      "sentiment_agent",
      "technical_agent",
      "risk_agent",
    ],
    entities: ["company", "security", "earnings_report", "news_item", "sector"],
    metrics: [
      "revenue_growth",
      "momentum_score",
      "sentiment_score",
      "volatility",
    ],
  };
}

function dryRun(plan: SemanticPlan): DryRunResult {
  return {
    approved: true,
    policyChecks: [
      "semantic_entities_registered",
      "metrics_registered",
      "recommendation_requires_provenance",
      "risk_agent_required_for_selection",
    ],
    entitiesTouched: plan.entities,
    metricsTouched: plan.metrics,
    riskNotes: ["portfolio concentration check required before execution"],
  };
}

function selectRecommendation(
  plan: SemanticPlan,
  validation: DryRunResult,
): Recommendation {
  if (!validation.approved) {
    throw new Error("Plan was rejected by governed dry run");
  }

  return {
    asset: "AVGO",
    score: 0.84,
    rationale:
      "Selected as a high-conviction NVDA-adjacent candidate based on fundamental quality, semiconductor exposure, momentum, and manageable risk.",
    provenance: [
      `intent:${plan.intent}`,
      "source:candidate_universe",
      "agent:fundamental_agent",
      "agent:sentiment_agent",
      "agent:technical_agent",
      "agent:risk_agent",
      "policy:recommendation_requires_provenance",
      "dry_run:approved",
    ],
  };
}

async function parseRequest(request: Request): Promise<{ intent: string; subject: string }> {
  if (request.method === "GET") {
    const url = new URL(request.url);
    return {
      intent: url.searchParams.get("intent") || "Find attractive NVDA alternatives",
      subject: url.searchParams.get("subject") || "NVDA",
    };
  }

  const body = await request.json().catch(() => ({})) as Partial<{
    intent: string;
    subject: string;
  }>;

  return {
    intent: body.intent || "Find attractive NVDA alternatives",
    subject: body.subject || "NVDA",
  };
}

export const onRequest: PagesFunction = async ({ request }) => {
  if (request.method === "OPTIONS") {
    return new Response(null, { headers: jsonHeaders });
  }

  if (!["GET", "POST"].includes(request.method)) {
    return new Response(
      JSON.stringify({ error: "Method not allowed" }),
      { status: 405, headers: jsonHeaders },
    );
  }

  try {
    const { intent, subject } = await parseRequest(request);
    const semanticPlan = buildSemanticPlan(intent, subject);
    const dryRunResult = dryRun(semanticPlan);
    const recommendation = selectRecommendation(semanticPlan, dryRunResult);

    const response: AnalyzeResponse = {
      semanticPlan,
      dryRun: dryRunResult,
      recommendation,
    };

    return new Response(JSON.stringify(response, null, 2), {
      headers: jsonHeaders,
    });
  } catch (error) {
    return new Response(
      JSON.stringify({
        error: "Failed to analyze request",
        detail: error instanceof Error ? error.message : String(error),
      }),
      { status: 500, headers: jsonHeaders },
    );
  }
};
