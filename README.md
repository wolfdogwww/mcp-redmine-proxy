

# MCP Redmine Proxy

This project provides a Machine Collaboration Protocol (MCP) server and HTTP bridge for interacting with Redmine through structured MCP tools.

It is designed to allow LLM-based agents or automation systems to query Redmine, inspect API schemas, upload and download attachments, and perform general API operations through a controlled interface.

This implementation is based on and extends the open-source project **mcp-redmine** by Rune Kaagaard:  
https://github.com/runekaagaard/mcp-redmine

The MCP tool server included in this repository is adapted from that project under the terms permitted by the Mozilla Public License 2.0 (MPL-2.0).  
See the "Licensing and Attribution" section for full compliance details.

---

## Features

- MCP-compliant Redmine tool server implemented with `fastmcp`.
- Supports:
  - `redmine_request` for direct API calls.
  - `redmine_paths_list` for listing all endpoints from the OpenAPI specification.
  - `redmine_paths_info` for retrieving API schema details.
  - `redmine_upload` for uploading attachments.
  - `redmine_download` for retrieving attachments.
- Proxy layer (FastAPI-based) providing `/list_tools` and `/call_tool` endpoints.
- Docker-ready for integration into multi-service environments.
- Environment-driven configuration suitable for development and production.

---

## Repository Structure

```

mcp-redmine-proxy/
│
├── proxy/                     # FastAPI proxy exposing /list_tools /call_tool
│   ├── main.py
│   ├── mcp_bridge.py
│   └── __init__.py
│
├── mcp_redmine/               # MCP Redmine server (adapted from mcp-redmine)
│   ├── server.py
│   ├── redmine_openapi.yml
│   └── __init__.py
│
├── requirements.txt
├── Dockerfile
└── README.md

```

---

## Configuration

The following environment variables must be defined:

| Variable | Description |
|---------|-------------|
| `REDMINE_URL` | Base URL of the Redmine instance |
| `REDMINE_API_KEY` | API key for authentication |
| `REDMINE_REQUEST_INSTRUCTIONS` | (Optional) Path to additional instructions appended to the tool description |

Example `.env` file:

```

REDMINE_URL=[https://redmine.example.com/](https://redmine.example.com/)
REDMINE_API_KEY=your_api_key_here

````

---

## Docker Compose Example

```yaml
services:
  mcp_redmine_proxy:
    image: mcp-redmine-proxy:latest
    container_name: mcp-redmine-proxy
    restart: always
    env_file:
      - .env
    ports:
      - "3000:8000"
    networks:
      - default
````

Run:

```bash
docker compose up -d
```

---

## API Testing

### List tools

```bash
curl http://localhost:3000/list_tools
```

### Call a tool

```bash
curl -X POST http://localhost:3000/call_tool \
  -H "Content-Type: application/json" \
  -d '{
    "name": "redmine_paths_list",
    "arguments": {}
  }'
```

### Execute a Redmine request

```bash
curl -X POST http://localhost:3000/call_tool \
  -H "Content-Type: application/json" \
  -d '{
    "name": "redmine_request",
    "arguments": { "path": "/issues.json" }
  }'
```

---

## Architecture Overview

```
[MCP Client / LLM Agent / Automation System]
                 │
                 ▼
           FastAPI Proxy
     (/list_tools, /call_tool)
                 │
                 ▼
  MCP Redmine Server (process-based MCP)
                 │
                 ▼
         Redmine REST API
```

---

## Licensing and Attribution

### Origin of Portions of This Project

Parts of this repository, specifically the MCP Redmine server implementation under ```mcp_redmine/```, are derived from:

**mcp-redmine**
Author: Rune Kaagaard
Repository: [https://github.com/runekaagaard/mcp-redmine](https://github.com/runekaagaard/mcp-redmine)
License: **Mozilla Public License 2.0 (MPL-2.0)**

Modifications have been made to integrate the server into a proxy environment, adjust behaviors, and support additional deployment patterns.

### Compliance with MPL-2.0

MPL-2.0 requires:

* Modified MPL-covered source files must remain under MPL-2.0.
* Only the files containing MPL-covered code are required to be open under MPL.
* You **may** distribute the full project under another license (such as MIT), as long as MPL-covered files retain their original license notice.

You are **not required** to open-source the entire project under MPL, nor are you prohibited from using your own MIT license for your additional code.

This project complies by:

* Preserving MPL-2.0 license headers for derived files.
* Separating MIT-licensed proxy code.

### Project License (MIT)

All original code in this repository (i.e., the proxy layer and new components) is licensed under the MIT License:

```
All original code in this repository is licensed under the MIT License.
See the LICENSE file for the full license text.
```

The MPL-2.0 license for derived components is included in `LICENSE-MPL-2.0`.

---

## Acknowledgements

Special thanks to Rune Kaagaard for developing the original MCP Redmine implementation and releasing it under a permissive open-source license that allows extension and integration.

