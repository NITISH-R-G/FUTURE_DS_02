import json
import os
from datetime import datetime

def update_readme():
    # Load inputs
    stats = {}
    if os.path.exists('repo_stats.json'):
        with open('repo_stats.json', 'r') as f:
            stats = json.load(f)

    ai_summary = {}
    if os.path.exists('ai_summary.json'):
        with open('ai_summary.json', 'r') as f:
            ai_summary = json.load(f)

    diagram = ""
    if os.path.exists('docs/architecture.md'):
        with open('docs/architecture.md', 'r') as f:
            diagram = f.read()

    # Construct the README
    content = []

    # Header and Status Badges
    content.append("# Repository")
    content.append("![CI/CD](https://github.com/placeholder/repo/actions/workflows/ci-cd.yml/badge.svg)")
    content.append("![Repo Automation](https://github.com/placeholder/repo/actions/workflows/repo-automation.yml/badge.svg)")
    content.append("\n*This README is automatically generated and maintained.*")

    # Overview
    content.append("## Overview")
    content.append(ai_summary.get("overview", "A self-documenting repository."))

    # Key Features
    content.append("## Key Features")
    content.append("- Automated architecture discovery")
    content.append("- Continuous documentation generation")
    content.append("- Interactive dependency diagrams")
    content.append("- AI-powered repository summaries")
    content.append("- CI/CD integrations for tests and security")

    # Technology Stack
    content.append("## Technology Stack")
    if stats.get("languages"):
        langs = [f"- **{lang}**: {count} files" for lang, count in stats["languages"].items()]
        content.append("\n".join(langs))
    else:
        content.append("Stack detection pending.")

    # System Architecture
    content.append("## System Architecture")
    content.append(ai_summary.get("architecture", "Architecture documentation pending."))
    content.append("\n### Components")
    content.append(ai_summary.get("components", "Component documentation pending."))

    # Diagrams
    content.append("## Interactive Architecture Diagrams")
    content.append(diagram if diagram else "Diagrams pending.")

    # Repository Structure
    content.append("## Repository Stats")
    content.append(f"- **Total Files Analyzed**: {stats.get('files_count', 0)}")
    content.append(f"- **Total Lines of Code**: {stats.get('total_lines', 0)}")

    # Setup, Deployment, Env Vars, API
    content.append("## Setup Instructions")
    content.append("1. Clone the repository")
    content.append("2. Install dependencies (e.g., `pip install -r scripts/requirements.txt`)")
    content.append("3. Run the automation scripts locally if desired.")

    content.append("## Deployment Instructions")
    content.append("This repository relies heavily on GitHub Actions. Ensure Actions are enabled in your repository settings.")

    content.append("## Environment Variables")
    content.append("- `OPENAI_API_KEY`: Required for the AI Documentation Agent to summarize changes.")

    content.append("## API Documentation")
    content.append("No external APIs are currently exposed.")

    content.append("## Contribution Guide")
    content.append("Please submit Pull Requests. The CI pipeline will automatically run linting, tests, security scans, and update the architecture diagrams and documentation upon merge.")

    # Changelog Summaries
    content.append("## Recent Changes")
    content.append(ai_summary.get("recent_changes", "No recent changes detected."))

    content.append(f"\n---\n*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

    # Write to README.md
    with open('README.md', 'w') as f:
        f.write("\n\n".join(content))

    print("README.md updated successfully.")

if __name__ == "__main__":
    update_readme()
