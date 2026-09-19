from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentState:
    user_query: str

    # Current selected tool
    selected_tool: str | None = None

    # Parameters for the current tool
    parameters: dict[str, Any] = field(default_factory=dict)

    # Result from the current tool
    tool_result: Any = None

    # Track multiple tools used in a workflow
    executed_tools: list[str] = field(default_factory=list)

    # Store results from each step
    step_results: list[dict[str, Any]] = field(default_factory=list)

    # Error information
    error: str | None = None

    # Current workflow step
    current_step: int = 0