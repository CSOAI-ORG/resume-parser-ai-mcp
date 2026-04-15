# Resume Parser Ai

> By [MEOK AI Labs](https://meok.ai) — Parse resumes to extract skills, match against jobs, and score candidates.

MEOK AI Labs — resume-parser-ai-mcp MCP Server. Parse resumes and extract skills, experience, and contact info.

## Installation

```bash
pip install resume-parser-ai-mcp
```

## Usage

```bash
# Run standalone
python server.py

# Or via MCP
mcp install resume-parser-ai-mcp
```

## Tools

### `parse_resume`
Parse resume text and extract structured information: contact, skills, education, experience.

**Parameters:**
- `text` (str)

### `extract_skills`
Extract and categorize all skills from resume text with proficiency estimates.

**Parameters:**
- `text` (str)

### `match_job`
Match a resume against job requirements and return a compatibility report.

**Parameters:**
- `resume_text` (str)
- `job_requirements` (str)

### `score_resume`
Score a resume on completeness, formatting indicators, and content quality (0-100).

**Parameters:**
- `text` (str)


## Authentication

Free tier: 15 calls/day. Upgrade at [meok.ai/pricing](https://meok.ai/pricing) for unlimited access.

## Links

- **Website**: [meok.ai](https://meok.ai)
- **GitHub**: [CSOAI-ORG/resume-parser-ai-mcp](https://github.com/CSOAI-ORG/resume-parser-ai-mcp)
- **PyPI**: [pypi.org/project/resume-parser-ai-mcp](https://pypi.org/project/resume-parser-ai-mcp/)

## License

MIT — MEOK AI Labs
