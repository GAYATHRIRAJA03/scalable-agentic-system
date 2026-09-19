def search_knowledge_base(query: str):
    knowledge_base = {
        "invoice": "Invoices can be created for customers using the PayPal invoice API.",
        "payment": "Payments can be sent to customers using the PayPal payment API.",
        "dispute": "A dispute represents a payment issue raised by a customer.",
        "sales": "Sales reports provide information about transaction volume for a given period.",
    }

    query_lower = query.lower()

    results = []

    for topic, information in knowledge_base.items():
        if topic in query_lower:
            results.append(information)

    if not results:
        return {
            "status": "success",
            "results": ["No relevant knowledge found."]
        }

    return {
        "status": "success",
        "results": results
    }