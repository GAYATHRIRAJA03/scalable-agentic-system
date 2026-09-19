class Router:
    def route(self, query: str) -> str:
        """
        Decide which part of the agentic system should handle the query.

        Routes:
        - system  -> system tools / capabilities / health
        - rag     -> knowledge-base questions
        - paypal  -> PayPal actions and data
        - unknown -> unsupported or unclear requests
        """

        query_lower = query.lower().strip()

        # -----------------------------
        # 1. SYSTEM ROUTE
        # -----------------------------
        system_keywords = [
            "available tools",
            "tools are available",
            "what tools",
            "list tools",
            "system status",
            "system health",
            "system information",
            "system",
            "health",
            "capabilities",
        ]

        if any(keyword in query_lower for keyword in system_keywords):
            return "system"

        # -----------------------------
        # 2. RAG / KNOWLEDGE ROUTE
        # -----------------------------
        rag_keywords = [
            "what is",
            "what are",
            "explain",
            "meaning",
            "define",
            "how does",
            "how do",
            "tell me about",
            "information about",
            "knowledge",
        ]

        if any(keyword in query_lower for keyword in rag_keywords):
            return "rag"

        # -----------------------------
        # 3. PAYPAL ROUTE
        # -----------------------------
        paypal_keywords = [
            "create invoice",
            "send invoice",
            "invoice for",

            "send payment",
            "make payment",
            "payment",
            "pay",

            "total sales",
            "sales report",
            "sales volume",
            "sales in",
            "sales for",
            "my sales",

            "is there a dispute",
            "check dispute",
            "open dispute",
            "dispute from",

            "refund",
            "transaction",
        ]
        if any(keyword in query_lower for keyword in paypal_keywords):
            return "paypal"

        # -----------------------------
        # 4. UNKNOWN ROUTE
        # -----------------------------
        return "unknown"