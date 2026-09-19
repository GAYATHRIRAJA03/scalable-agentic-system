from app.tool_registry import ToolDefinition


class ParameterValidator:
    def validate(
        self,
        tool: ToolDefinition,
        parameters: dict
    ) -> dict:
        required_parameters = tool.parameters

        missing_parameters = []

        for parameter in required_parameters:
            if parameter not in parameters:
                missing_parameters.append(parameter)

        if missing_parameters:
            return {
                "valid": False,
                "missing_parameters": missing_parameters,
            }

        return {
            "valid": True,
            "missing_parameters": [],
        }