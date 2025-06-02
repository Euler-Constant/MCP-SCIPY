import asyncio
import logging
import yaml
from mcp import MCPServer
from .mcp_handler import MCPHandler

def load_config(config_path = "config/config.yaml"):
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        return {"host": "localhost", "port": 8080, "data_dir": "data"}

async def start_server():
    config = load_config()
    handler = MCPHandler()
    server = MCPServer(
        host=config["host"],
        port=config["port"],
        handler=handler
    )
    logger.info(f"Starting MCP server on {config['host']}:{config['port']}")
    await server.start()

if __name__ == "__main__":
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")