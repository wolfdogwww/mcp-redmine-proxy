from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
from .mcp_bridge import MCPBridge

app = FastAPI()

# ---- Request Models ----

class CallToolRequest(BaseModel):
    name: str
    arguments: dict = {}


# ---- MCP Bridge Setup ----
bridge = MCPBridge(
    cmd=["python3", "/app/mcp_redmine/server.py"],
    cwd="/app"
)


# ---- Startup: Initialize MCP ----
@app.on_event("startup")
async def startup():
    await bridge.start()

    init_payload = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "clientInfo": {
                "name": "mcp-proxy",
                "version": "1.0"
            },
            "capabilities": {
                "experimental": {},
                "roots": {},
                "sampling": {}
            }
        }
    }

    print("[DEBUG] Sending initialize handshake...")
    resp = await bridge.send(init_payload)
    print("[DEBUG] Initialize response:", resp)

# ---- List Tools ----
@app.get("/list_tools")
async def list_tools():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
        "params": {}
    }
    return await bridge.send(payload)


# ---- Call Tool ----
@app.post("/call_tool")
async def call_tool(req: CallToolRequest):
    payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": req.name,
            "arguments": req.arguments
        }
    }
    return await bridge.send(payload)
