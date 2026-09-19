from app.tool_registry import create_paypal_registry
from app.tool_selector import ToolSelector


registry = create_paypal_registry()

selector = ToolSelector(registry)


queries = [
    "Create an invoice for a customer",
    "Send a payment to John",
    "Check an open dispute",
    "Show my sales report",
]


for query in queries:

    print("=" * 60)
    print(f"Query: {query}")

    tools = selector.select_tools(query, top_k=3)

    print("Selected tools:")

    for tool in tools:
        print(
            f"- {tool.name} "
            f"| {tool.category}"
        )