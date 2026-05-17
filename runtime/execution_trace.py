from dataclasses import dataclass, field
from typing import List


@dataclass
class ExecutionTrace:
    intent: str
    agents: List[str] = field(default_factory=list)
    entities: List[str] = field(default_factory=list)
    metrics: List[str] = field(default_factory=list)
    policy_checks: List[str] = field(default_factory=list)
    approved: bool = False

    def summarize(self) -> str:
        return (
            f"Intent={self.intent}, "
            f"Approved={self.approved}, "
            f"Agents={self.agents}, "
            f"Entities={self.entities}"
        )
