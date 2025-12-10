# proxy/mcp_bridge.py

import json
import asyncio
import sys


class MCPBridge:
    def __init__(self, cmd, cwd=None):
        self.cmd = cmd
        self.cwd = cwd
        self.process = None

    async def start(self):
        print("[DEBUG] Starting MCP subprocess:", self.cmd, "cwd=", self.cwd)

        self.process = await asyncio.create_subprocess_exec(
            *self.cmd,
            cwd=self.cwd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # 開啟 background stderr logger
        asyncio.create_task(self._log_stderr())

        print("[DEBUG] MCP subprocess started. PID =", self.process.pid)

    async def _log_stderr(self):
        """持續讀取並印出 MCP server 的 stderr"""
        while True:
            line = await self.process.stderr.readline()
            if not line:
                continue
            print("[MCP STDERR] ", line.decode().rstrip(), file=sys.stderr)

    async def send(self, payload: dict):
        body = json.dumps(payload)

        print("\n[DEBUG] Sending JSON to MCP server:")
        print(body)

        self.process.stdin.write((body + "\n").encode())
        await self.process.stdin.drain()

        return await self._read_line_json()

    async def _read_line_json(self):
        while True:
            line = await self.process.stdout.readline()

            if not line:
                continue

            decoded = line.decode().strip()

            print("[DEBUG][STDOUT]", decoded)

            # MCP server 會一行一個 JSON
            try:
                return json.loads(decoded)
            except:
                print("[DEBUG] Not a full JSON, waiting more...")
                continue
                
    async def _read_response(self):
        """讀取 Content-Length framing response"""

        print("[DEBUG] Waiting for MCP response header...")

        # 讀到空行前都算 header
        content_length = None
        while True:
            line = await self.process.stdout.readline()
            if not line:
                continue

            decoded = line.decode().rstrip()
            print("[DEBUG][STDOUT] ", decoded)

            if decoded.lower().startswith("content-length"):
                content_length = int(decoded.split(":")[1].strip())

            if decoded == "":
                break  # header 結束

        if content_length is None:
            raise RuntimeError("MCP server 回應中沒有 Content-Length")

        print(f"[DEBUG] MCP response Content-Length = {content_length}")

        # 讀 body
        body = await self.process.stdout.read(content_length)
        decoded_body = body.decode()

        print("[DEBUG] === MCP Response Body ===")
        print(decoded_body)
        print("[DEBUG] ==========================\n")

        return json.loads(decoded_body)
