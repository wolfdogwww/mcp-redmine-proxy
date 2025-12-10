FROM python:3.11-slim

WORKDIR /app

# 安裝 Python 套件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製 proxy 程式碼
COPY proxy ./proxy

# 複製 MCP Redmine Server 套件（你放在 mcp-redmine 資料夾內）
COPY mcp-redmine/mcp_redmine ./mcp_redmine
COPY mcp-redmine/mcp_redmine/redmine_openapi.yml ./mcp_redmine/redmine_openapi.yml

EXPOSE 8000

CMD ["uvicorn", "proxy.main:app", "--host", "0.0.0.0", "--port", "8000"]
