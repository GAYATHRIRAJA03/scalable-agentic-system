from app.tool_registry import create_paypal_registry
from app.executor import ToolExecutor


registry = create_paypal_registry()
executor = ToolExecutor()


invoice_tool = registry.get_tool("create_invoice")
payment_tool = registry.get_tool("send_payment")


# ==========================================
# TEST 1: SUCCESSFUL WORKFLOW
# ==========================================

workflow_success = [
    (
        invoice_tool,
        {
            "customer": "John",
            "amount": 50
        }
    ),
    (
        payment_tool,
        {
            "customer": "John",
            "amount": 100
        }
    ),
]


result_success = executor.execute_workflow(
    workflow_success
)

print("=" * 60)
print("SUCCESS WORKFLOW:")
print(result_success)


# ==========================================
# TEST 2: FAILURE WORKFLOW
# ==========================================

workflow_failure = [
    (
        invoice_tool,
        {
            "customer": "John",
            "amount": 50
        }
    ),
    (
        payment_tool,
        {
            "customer": "John"
            # amount intentionally missing
        }
    ),
]


result_failure = executor.execute_workflow(
    workflow_failure
)

print("=" * 60)
print("FAILURE WORKFLOW:")
print(result_failure)