from app.tool_registry import ToolRegistry, ToolDefinition


class ToolSelector:

    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def select_tools(
        self,
        query: str,
        top_k: int = 3
    ) -> list[ToolDefinition]:
        """
        Select relevant tools using:

        1. Service/category filtering
        2. Tool name matching
        3. Category matching
        4. Description matching
        5. Top-K selection

        This reduces the number of tools considered by
        the agent as the tool ecosystem grows.
        """

        query_words = self._extract_keywords(query)

        # -----------------------------------------
        # STEP 1: Detect relevant categories
        # -----------------------------------------

        candidate_tools = self._filter_by_category(
            query_words
        )

        # If category filtering finds nothing,
        # fall back to the complete registry.
        if not candidate_tools:
            candidate_tools = self.registry.get_all_tools()

        # -----------------------------------------
        # STEP 2: Score candidate tools
        # -----------------------------------------

        scored_tools = []

        for tool in candidate_tools:

            score = self._calculate_score(
                query_words,
                tool
            )

            if score > 0:
                scored_tools.append(
                    (score, tool)
                )

        # -----------------------------------------
        # STEP 3: Rank tools
        # -----------------------------------------

        scored_tools.sort(
            key=lambda item: item[0],
            reverse=True
        )

        # -----------------------------------------
        # STEP 4: Return only Top-K
        # -----------------------------------------

        return [
            tool
            for score, tool in scored_tools[:top_k]
        ]

    # ==========================================
    # CATEGORY FILTER
    # ==========================================

    def _filter_by_category(
        self,
        query_words: set[str]
    ) -> list[ToolDefinition]:

        category_map = {
            "invoice": "paypal.invoice",
            "invoices": "paypal.invoice",

            "payment": "paypal.payments",
            "payments": "paypal.payments",
            "pay": "paypal.payments",

            "dispute": "paypal.disputes",
            "disputes": "paypal.disputes",

            "sales": "paypal.reports",
            "report": "paypal.reports",
            "reports": "paypal.reports",

            "knowledge": "rag",
            "explain": "rag",

            "system": "system",
            "health": "system",
            "capabilities": "system",
        }

        categories = {
            category_map[word]
            for word in query_words
            if word in category_map
        }

        if not categories:
            return []

        return [
            tool
            for tool in self.registry.get_all_tools()
            if tool.category in categories
        ]

    # ==========================================
    # KEYWORD EXTRACTION
    # ==========================================

    def _extract_keywords(
        self,
        query: str
    ) -> set[str]:

        stop_words = {
            "a",
            "an",
            "the",
            "is",
            "are",
            "was",
            "were",
            "my",
            "me",
            "for",
            "to",
            "of",
            "in",
            "on",
            "from",
            "what",
            "how",
            "can",
            "i",
            "please",
            "do",
            "does",
            "did",
            "show",
            "tell",
            "give",
        }

        words = query.lower().split()

        return {
            word.strip(".,?!")
            for word in words
            if word.strip(".,?!")
            not in stop_words
        }

    # ==========================================
    # TOOL SCORING
    # ==========================================

    def _calculate_score(
        self,
        query_words: set[str],
        tool: ToolDefinition
    ) -> int:

        tool_name = tool.name.lower()
        category = tool.category.lower()
        description = tool.description.lower()

        score = 0

        for word in query_words:

            # Strong signal
            if word in tool_name:
                score += 5

            # Medium signal
            if word in category:
                score += 3

            # Supporting signal
            if word in description:
                score += 1

        return score