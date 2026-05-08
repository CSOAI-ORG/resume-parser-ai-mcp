<div align="center">

# Resume Parser Ai MCP

**MCP server for resume parser ai mcp operations**

[![PyPI](https://img.shields.io/pypi/v/meok-resume-parser-ai-mcp)](https://pypi.org/project/meok-resume-parser-ai-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Resume Parser Ai MCP provides AI-powered tools via the Model Context Protocol (MCP).

## Tools

| Tool | Description |
|------|-------------|
| `parse_resume` | Parse resume text and extract structured information: contact, skills, education |
| `extract_skills` | Extract and categorize all skills from resume text with proficiency estimates. |
| `match_job` | Match a resume against job requirements and return a compatibility report. |
| `score_resume` | Score a resume on completeness, formatting indicators, and content quality (0-10 |

## Installation

```bash
pip install meok-resume-parser-ai-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "resume-parser-ai": {
      "command": "python",
      "args": ["-m", "meok_resume_parser_ai_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 4 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
