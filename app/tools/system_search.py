def search_system(query: str):
    system_data = {
        "tools": [
            "create_invoice",
            "get_sales_report",
            "check_dispute",
            "send_payment",
        ],
        "services": [
            "PayPal",
            "Knowledge Base",
            "System Search",
        ],
        "status": "All systems operational",
    }

    query_lower = query.lower()

    results = []

    if "tool" in query_lower or "api" in query_lower:
        results.append(
            f"Available tools: {', '.join(system_data['tools'])}"
        )

    if "service" in query_lower:
        results.append(
            f"Available services: {', '.join(system_data['services'])}"
        )

    if "status" in query_lower or "health" in query_lower:
        results.append(system_data["status"])

    if not results:
        results.append("No matching system information found.")

    return {
        "status": "success",
        "results": results,
    }