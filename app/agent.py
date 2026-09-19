import re

from app.router import Router
from app.tool_registry import create_paypal_registry
from app.tool_selector import ToolSelector
from app.validator import ParameterValidator
from app.executor import ToolExecutor
from app.state import AgentState


class Agent:

    def __init__(self):
        self.registry = create_paypal_registry()
        self.router = Router()
        self.tool_selector = ToolSelector(self.registry)
        self.validator = ParameterValidator()
        self.executor = ToolExecutor()

    def extract_parameters(
        self,
        query: str,
        tool_name: str
    ) -> dict:
        parameters = {}

        # --------------------------------
        # Amount extraction
        # --------------------------------
        if tool_name in ["create_invoice", "send_payment"]:
            amount_match = re.search(
                r"(?:\$|USD\s*)\s*(\d+(?:\.\d+)?)"
                r"|\b(\d+(?:\.\d+)?)\s*(?:dollars?|USD)\b",
                query,
                re.IGNORECASE
            )

            if amount_match:
                amount = (
                    amount_match.group(1)
                    if amount_match.group(1) is not None
                    else amount_match.group(2)
                )

                parameters["amount"] = float(amount)

        # --------------------------------
        # Customer extraction
        # --------------------------------
        if tool_name in ["create_invoice", "send_payment"]:
            customer_match = re.search(
                r"(?:for|to)\s+([A-Za-z]+)",
                query,
                re.IGNORECASE
            )

            if customer_match:
                parameters["customer"] = (
                    customer_match.group(1)
                )

        # --------------------------------
        # User ID extraction
        # --------------------------------
        if tool_name == "check_dispute":
            user_match = re.search(
                r"(user_[A-Za-z0-9]+)",
                query,
                re.IGNORECASE
            )

            if user_match:
                parameters["user_id"] = (
                    user_match.group(1)
                )

        # --------------------------------
        # Month extraction
        # --------------------------------
        if tool_name == "get_sales_report":
            month_match = re.search(
                r"\b(?:for|in|during)\s+"
                r"(January|February|March|April|May|June|"
                r"July|August|September|October|November|December)"
                r"\b",
                query,
                re.IGNORECASE
            )

            if month_match:
                parameters["month"] = (
                    month_match.group(1)
                )

        return parameters

    # ==============================================
    # MULTI-STEP WORKFLOW
    # ==============================================

    def run_workflow(
        self,
        workflow: list[tuple[str, dict]]
    ):
        tool_workflow = []

        for tool_name, parameters in workflow:

            # Find the tool in the registry
            tool = self.registry.get_tool(tool_name)

            if not tool:
                return {
                    "status": "error",
                    "message": f"Tool not found: {tool_name}",
                }

            # Validate parameters before execution
            validation = self.validator.validate(
                tool,
                parameters
            )

            if not validation["valid"]:
                return {
                    "status": "error",
                    "tool": tool.name,
                    "message": (
                        "Required parameters are missing."
                    ),
                    "missing_parameters": (
                        validation["missing_parameters"]
                    ),
                }

            # Add validated tool to workflow
            tool_workflow.append(
                (tool, parameters)
            )

        # Execute all steps sequentially
        return self.executor.execute_workflow(
            tool_workflow
        )

    # ==============================================
    # MAIN AGENT
    # ==============================================

    def run(
        self,
        query: str,
        parameters: dict | None = None
    ):
        state = AgentState(
            user_query=query
        )

        route = self.router.route(query)

        # --------------------------------
        # Unknown request
        # --------------------------------
        if route == "unknown":
            state.error = (
                "I could not determine which service "
                "can handle this request."
            )

            return {
                "status": "error",
                "route": route,
                "message": state.error,
            }

        # --------------------------------
        # RAG route
        # --------------------------------
        if route == "rag":
            tool = self.registry.get_tool(
                "search_knowledge_base"
            )

            result = self.executor.execute(
                tool,
                {
                    "query": query
                }
            )

            return {
                "status": "success",
                "route": route,
                "tool": tool.name,
                "result": result,
            }

        # --------------------------------
        # System route
        # --------------------------------
        if route == "system":
            tool = self.registry.get_tool(
                "search_system"
            )

            result = self.executor.execute(
                tool,
                {
                    "query": query
                }
            )

            return {
                "status": "success",
                "route": route,
                "tool": tool.name,
                "result": result,
            }

        # --------------------------------
        # PayPal route
        # --------------------------------
        selected_tools = self.tool_selector.select_tools(
            query
        )

        if not selected_tools:
            return {
                "status": "error",
                "route": route,
                "message": (
                    "No suitable PayPal tool found."
                ),
            }

        tool = selected_tools[0]

        state.selected_tool = tool.name

        # Extract parameters automatically
        if parameters is None:
            parameters = self.extract_parameters(
                query,
                tool.name
            )

        state.parameters = parameters

        # Validate parameters
        validation = self.validator.validate(
            tool,
            parameters
        )

        if not validation["valid"]:
            return {
                "status": "error",
                "route": route,
                "tool": tool.name,
                "message": (
                    "Required parameters are missing."
                ),
                "missing_parameters": (
                    validation["missing_parameters"]
                ),
            }

        # Execute selected tool
        result = self.executor.execute(
            tool,
            parameters
        )

        state.tool_result = result

        state.executed_tools.append(
            tool.name
        )

        state.step_results.append({
            "step": 1,
            "tool": tool.name,
            "parameters": parameters,
            "result": result,
        })

        state.current_step = 1

        return {
            "status": "success",
            "route": route,
            "tool": tool.name,
            "parameters": parameters,
            "result": result,
        }