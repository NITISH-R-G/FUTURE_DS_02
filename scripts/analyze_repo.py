import os
import ast
import re
import json
from collections import defaultdict

EXCLUDE_DIRS = {'.git', 'node_modules', 'venv', 'env', '__pycache__', '.github', 'scripts', 'docs', '.pytest_cache'}

def analyze_repo(repo_path="."):
    repo_graph = {"nodes": [], "edges": []}
    repo_stats = {
        "files_count": 0,
        "languages": defaultdict(int),
        "total_lines": 0,
        "components": []
    }

    file_nodes = {}
    edges = []

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for file in files:
            if file.startswith('.') or file.endswith('.json') or file.endswith('.lock') or file.endswith('.csv') or file.endswith('.pbix'):
                continue

            filepath = os.path.relpath(os.path.join(root, file), repo_path)
            ext = os.path.splitext(file)[1].lower()

            try:
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = len(content.splitlines())

                    repo_stats["files_count"] += 1
                    repo_stats["total_lines"] += lines

                    if ext == '.py':
                        repo_stats["languages"]["Python"] += 1
                        imports = extract_python_imports(content)
                        file_nodes[filepath] = {"type": "python", "imports": imports}
                    elif ext in ['.js', '.jsx']:
                        repo_stats["languages"]["JavaScript"] += 1
                        imports = extract_js_imports(content)
                        file_nodes[filepath] = {"type": "javascript", "imports": imports}
                    elif ext in ['.ts', '.tsx']:
                        repo_stats["languages"]["TypeScript"] += 1
                        imports = extract_js_imports(content)
                        file_nodes[filepath] = {"type": "typescript", "imports": imports}
                    elif ext == '.md':
                        repo_stats["languages"]["Markdown"] += 1
                        file_nodes[filepath] = {"type": "markdown", "imports": []}
                    else:
                        if ext:
                            repo_stats["languages"][ext[1:].upper()] += 1
                        file_nodes[filepath] = {"type": ext[1:] if ext else "unknown", "imports": []}
            except Exception:
                pass

    # Build graph
    for filepath, data in file_nodes.items():
        repo_graph["nodes"].append({"id": filepath, "label": os.path.basename(filepath), "type": data["type"]})
        repo_stats["components"].append(filepath)
        for imp in data["imports"]:
            edges.append({"source": filepath, "target": imp})

    repo_graph["edges"] = edges
    repo_stats["languages"] = dict(repo_stats["languages"])

    with open('repo_graph.json', 'w') as f:
        json.dump(repo_graph, f, indent=2)

    with open('repo_stats.json', 'w') as f:
        json.dump(repo_stats, f, indent=2)

def extract_python_imports(content):
    imports = []
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
    except Exception:
        pass
    return list(set(imports))

def extract_js_imports(content):
    imports = []
    import_regex = re.compile(r'import\s+.*?\s+from\s+[\'"](.*?)[\'"]')
    require_regex = re.compile(r'require\s*\(\s*[\'"](.*?)[\'"]\s*\)')

    for match in import_regex.findall(content):
        imports.append(match)
    for match in require_regex.findall(content):
        imports.append(match)
    return list(set(imports))

if __name__ == "__main__":
    analyze_repo()
