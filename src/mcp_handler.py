from mcp import MCPHandlerBase
from .stats_engine import StatsEngine
from .utils.auth import authenticate_request

class MCPHandler(MCPHandlerBase):
    def __init__(self):
        super().__init__()
        self.stats_engine = StatsEngine()

    async def handle_request(self, request):
        if not authenticate_request(request):
            return {"error": "Unauthorized", "id": request.get("id")}

        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")

        if method == "run_ttest":
            file_name = params.get("file_name")
            column = params.get("column")
            group_col = params.get("group_col")
            group1 = params.get("group1")
            group2 = params.get("group2")
            if not all([file_name, column, group_col, group1, group2]):
                return {"error": "Missing required parameters", "id": request_id}
            result = self.stats_engine.run_ttest(file_name, column, group_col, group1, group2)
            return {"result": result, "id": request_id}
        elif method == "get_tool_info":
            return {
                "result": {
                    "tools": [
                        {
                            "name": "run_ttest",
                            "description": "Run an independent t-test on a dataset column",
                            "parameters": {
                                "file_name": {"type": "string", "description": "Path to CSV file"},
                                "column": {"type": "string", "description": "Column for analysis"},
                                "group_col": {"type": "string", "description": "Column defining groups"},
                                "group1": {"type": "string", "description": "First group value"},
                                "group2": {"type": "string", "description": "Second group value"}
                            }
                        }
                    ]
                },
                "id": request_id
            }
        else:
            return {"error": f"Unknown method: {method}", "id": request_id}