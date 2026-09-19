
from dataclasses import dataclass
from typing import Any, Callable
from app.tools.paypal_tools import (
    create_invoice,
    get_sales_report,
    check_dispute,
    send_payment,
)

from app.tools.rag_tool import search_knowledge_base
from app.tools.system_search import search_system

@dataclass
class ToolDefinition:
    name: str
    description: str
    category: str
    parameters: dict[str, Any]
    function: Callable


class ToolRegistry:
    def __init__(self):
        self.tools: dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition):
        self.tools[tool.name] = tool

    def get_tool(self, name: str) -> ToolDefinition | None:
        return self.tools.get(name)

    def get_all_tools(self) -> list[ToolDefinition]:
        return list(self.tools.values())

from app.tools.paypal_tools import (
    create_invoice,
    get_sales_report,
    check_dispute,
    send_payment,
)


def create_paypal_registry():
    registry = ToolRegistry()

    registry.register(
        ToolDefinition(
            name="create_invoice",
            description="Create an invoice for a customer with a specified amount.",
            category="paypal.invoice",
            parameters={
                "customer": "string",
                "amount": "number",
            },
            function=create_invoice,
        )
    )

    registry.register(
        ToolDefinition(
            name="get_sales_report",
            description="Get the total sales report for a specific month.",
            category="paypal.reports",
            parameters={
                "month": "string",
            },
            function=get_sales_report,
        )
    )

    registry.register(
        ToolDefinition(
            name="check_dispute",
            description="Check whether a customer has an open dispute.",
            category="paypal.disputes",
            parameters={
                "user_id": "string",
            },
            function=check_dispute,
        )
    )

    registry.register(
        ToolDefinition(
            name="send_payment",
            description="Send a payment to a customer.",
            category="paypal.payments",
            parameters={
                "customer": "string",
                "amount": "number",
            },
            function=send_payment,
        )
    )
    registry.register(
            ToolDefinition(
                name="search_knowledge_base",
                description="Search the knowledge base for relevant information.",
                category="rag",
                parameters={
                    "query": "string",
                },
                function=search_knowledge_base,
            )
        )
    
    registry.register(
            ToolDefinition(
                name="search_system",
                description="Search system capabilities, tools, services, and status.",
                category="system",
                parameters={
                    "query": "string",
                },
                function=search_system,
            )
        )

    return registry
   