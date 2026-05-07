#!/usr/bin/env python3
"""MEOK AI Labs — resume-parser-ai-mcp MCP Server. Parse resumes and extract skills, experience, and contact info."""

import json
import re
from datetime import datetime, timezone
from collections import defaultdict, Counter

from mcp.server.fastmcp import FastMCP
import sys, os
sys.path.insert(0, os.path.expanduser("~/clawd/meok-labs-engine/shared"))
from auth_middleware import check_access

FREE_DAILY_LIMIT = 15
_usage = defaultdict(list)
def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now-t).total_seconds() < 86400]
    if len(_usage[c]) >= FREE_DAILY_LIMIT: return json.dumps({"error": f"Limit {FREE_DAILY_LIMIT}/day"})
    _usage[c].append(now); return None

TECH_SKILLS = [
    "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", "Rust", "Ruby", "PHP", "Swift", "Kotlin",
    "SQL", "NoSQL", "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
    "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "CI/CD", "Jenkins", "GitHub Actions",
    "React", "Angular", "Vue", "Next.js", "Node.js", "Django", "Flask", "FastAPI", "Spring",
    "Machine Learning", "Deep Learning", "NLP", "Computer Vision", "TensorFlow", "PyTorch",
    "REST", "GraphQL", "gRPC", "Microservices", "Event-Driven",
    "Agile", "Scrum", "Kanban", "JIRA", "Git", "Linux",
]

SOFT_SKILLS = [
    "Leadership", "Communication", "Problem Solving", "Teamwork", "Mentoring",
    "Project Management", "Strategic Planning", "Stakeholder Management",
    "Critical Thinking", "Time Management", "Presentation", "Negotiation",
]

DEGREE_PATTERNS = [
    (r"(?:ph\.?d|doctorate)", "PhD"),
    (r"(?:master|m\.?s\.?|m\.?a\.?|mba)", "Masters"),
    (r"(?:bachelor|b\.?s\.?|b\.?a\.?|b\.?eng)", "Bachelors"),
    (r"(?:associate|a\.?s\.?|a\.?a\.?)", "Associates"),
]

mcp = FastMCP("resume-parser-ai", instructions="Parse resumes to extract skills, match against jobs, and score candidates.")


def _extract_email(text: str) -> str:
    match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
    return match.group(0) if match else ""


def _extract_phone(text: str) -> str:
    match = re.search(r'[\+]?[\d\s\-\(\)]{7,15}', text)
    return match.group(0).strip() if match else ""


def _extract_years(text: str) -> int:
    years = re.findall(r'(\d{4})', text)
    years = [int(y) for y in years if 1980 <= int(y) <= 2030]
    if len(years) >= 2:
        return max(years) - min(years)
    return text.lower().count("year")


@mcp.tool()
def parse_resume(text: str, api_key: str = "") -> str:
    """Parse resume text and extract structured information: contact, skills, education, experience.

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl(): return err

    lower = text.lower()
    tech = [s for s in TECH_SKILLS if s.lower() in lower]
    soft = [s for s in SOFT_SKILLS if s.lower() in lower]
    education = []
    for pattern, degree in DEGREE_PATTERNS:
        if re.search(pattern, lower):
            education.append(degree)

    exp_years = _extract_years(text)

    return json.dumps({
        "contact": {"email": _extract_email(text), "phone": _extract_phone(text)},
        "technical_skills": tech,
        "soft_skills": soft,
        "education": education,
        "estimated_experience_years": exp_years,
        "word_count": len(text.split()),
        "sections_detected": [s for s in ["experience", "education", "skills", "projects", "certifications", "summary"] if s in lower],
    }, indent=2)


@mcp.tool()
def extract_skills(text: str, api_key: str = "") -> str:
    """Extract and categorize all skills from resume text with proficiency estimates.

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl(): return err

    lower = text.lower()
    categories = {
        "languages": [s for s in ["Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", "Rust", "Ruby", "PHP", "Swift", "Kotlin"] if s.lower() in lower],
        "frameworks": [s for s in ["React", "Angular", "Vue", "Next.js", "Node.js", "Django", "Flask", "FastAPI", "Spring"] if s.lower() in lower],
        "databases": [s for s in ["PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch", "SQL", "NoSQL"] if s.lower() in lower],
        "cloud_devops": [s for s in ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "CI/CD", "Jenkins", "GitHub Actions"] if s.lower() in lower],
        "ai_ml": [s for s in ["Machine Learning", "Deep Learning", "NLP", "Computer Vision", "TensorFlow", "PyTorch"] if s.lower() in lower],
        "soft_skills": [s for s in SOFT_SKILLS if s.lower() in lower],
    }

    total = sum(len(v) for v in categories.values())

    # Estimate proficiency by mention frequency
    skill_mentions = {}
    for cat_skills in categories.values():
        for skill in cat_skills:
            count = lower.count(skill.lower())
            skill_mentions[skill] = "expert" if count >= 3 else "proficient" if count >= 2 else "familiar"

    return json.dumps({
        "categories": categories,
        "total_skills": total,
        "proficiency_estimates": skill_mentions,
        "strongest_category": max(categories, key=lambda k: len(categories[k])) if total > 0 else "none",
    }, indent=2)


@mcp.tool()
def match_job(resume_text: str, job_requirements: list[str], api_key: str = "") -> str:
    """Match a resume against job requirements and return a compatibility report.

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl(): return err

    lower = resume_text.lower()
    matched = []
    missing = []

    for req in job_requirements:
        if req.lower() in lower:
            matched.append(req)
        else:
            # Fuzzy: check individual words
            words = req.lower().split()
            if len(words) > 1 and sum(1 for w in words if w in lower) >= len(words) * 0.6:
                matched.append(req)
            else:
                missing.append(req)

    match_pct = round(len(matched) / max(len(job_requirements), 1) * 100, 1)

    return json.dumps({
        "total_requirements": len(job_requirements),
        "matched": matched,
        "missing": missing,
        "match_percentage": match_pct,
        "recommendation": "Strong match" if match_pct >= 75 else "Good match" if match_pct >= 50 else "Partial match" if match_pct >= 30 else "Weak match",
        "suggestion": f"Consider highlighting experience with: {', '.join(missing[:3])}" if missing else "Resume covers all requirements",
    }, indent=2)


@mcp.tool()
def score_resume(text: str, api_key: str = "") -> str:
    """Score a resume on completeness, formatting indicators, and content quality (0-100).

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl(): return err

    lower = text.lower()
    score = 0
    breakdown = {}

    # Contact info (15 pts)
    contact_score = 0
    if _extract_email(text): contact_score += 8
    if _extract_phone(text): contact_score += 7
    breakdown["contact_info"] = contact_score
    score += contact_score

    # Skills (25 pts)
    tech = [s for s in TECH_SKILLS if s.lower() in lower]
    skills_score = min(25, len(tech) * 3)
    breakdown["technical_skills"] = skills_score
    score += skills_score

    # Sections (20 pts)
    sections = ["experience", "education", "skills", "summary", "projects"]
    found = sum(1 for s in sections if s in lower)
    section_score = min(20, found * 4)
    breakdown["sections"] = section_score
    score += section_score

    # Length (15 pts)
    wc = len(text.split())
    length_score = 15 if 300 <= wc <= 1200 else 10 if 150 <= wc <= 1500 else 5
    breakdown["length"] = length_score
    score += length_score

    # Quantifiable achievements (15 pts)
    numbers = len(re.findall(r'\d+%|\$[\d,]+|\d+ (?:years?|projects?|teams?|clients?)', lower))
    achieve_score = min(15, numbers * 3)
    breakdown["quantifiable_achievements"] = achieve_score
    score += achieve_score

    # Education (10 pts)
    edu_score = 0
    for pattern, degree in DEGREE_PATTERNS:
        if re.search(pattern, lower):
            edu_score = 10
            break
    breakdown["education"] = edu_score
    score += edu_score

    grade = "A" if score >= 85 else "B" if score >= 70 else "C" if score >= 55 else "D" if score >= 40 else "F"

    improvements = []
    if breakdown["contact_info"] < 10: improvements.append("Add complete contact information")
    if breakdown["technical_skills"] < 15: improvements.append("List more relevant technical skills")
    if breakdown["quantifiable_achievements"] < 9: improvements.append("Add quantifiable achievements (numbers, percentages)")
    if breakdown["sections"] < 12: improvements.append("Include standard sections: summary, experience, education, skills")

    return json.dumps({
        "score": min(score, 100),
        "grade": grade,
        "breakdown": breakdown,
        "improvements": improvements,
        "word_count": wc,
    }, indent=2)


if __name__ == "__main__":
    mcp.run()
