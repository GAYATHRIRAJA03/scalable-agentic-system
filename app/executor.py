from app.tool_registry import ToolDefinition


class ToolExecutor:

    def execute(
        self,
        tool: ToolDefinition,
        parameters: dict
    ):
        try:
            result = tool.function(**parameters)

            return {
                "status": "success",
                "tool": tool.name,
                "result": result,
            }

        except Exception as error:
            return {
                "status": "error",
                "tool": tool.name,
                "error": str(error),
            }

    def execute_workflow(
        self,
        workflow: list[tuple[ToolDefinition, dict]]
    ):
        results = []

        for step_number, (tool, parameters) in enumerate(
            workflow,
            start=1
        ):
            result = self.execute(
                tool,
                parameters
            )

            results.append({
                "step": step_number,
                "tool": tool.name,
                "parameters": parameters,
                "result": result,
            })

            # Stop immediately if a step fails
            if result["status"] == "error":
                return {
                    "status": "error",
                    "completed_steps": results,
                }

        return {
            "status": "success",
            "completed_steps": results,
        }