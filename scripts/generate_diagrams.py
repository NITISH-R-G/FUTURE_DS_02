import json
import os

def generate_diagrams():
    if not os.path.exists('repo_graph.json'):
        print("repo_graph.json not found. Run analyze_repo.py first.")
        return

    with open('repo_graph.json', 'r') as f:
        graph_data = json.load(f)

    nodes = graph_data.get("nodes", [])
    edges = graph_data.get("edges", [])

    mermaid_code = ["```mermaid", "graph TD"]

    # Map node IDs to valid Mermaid IDs
    node_id_map = {}
    for i, node in enumerate(nodes):
        safe_id = f"node{i}"
        node_id_map[node["id"]] = safe_id
        # Escape characters that might break mermaid
        label = node["label"].replace('"', "'")
        mermaid_code.append(f'    {safe_id}["{label}"]:::class{node.get("type", "unknown")}')

    # Add edges
    for edge in edges:
        source = edge.get("source")
        target = edge.get("target")

        # If target is an external library not in nodes, we add a generic node for it
        if source in node_id_map:
            source_id = node_id_map[source]
            target_id = node_id_map.get(target)

            if not target_id:
                # Add a safe generic id for this target
                target_safe = "".join(c if c.isalnum() else "_" for c in target)
                target_id = f"ext_{target_safe}"
                node_id_map[target] = target_id
                mermaid_code.append(f'    {target_id}["{target}"]:::classExternal')

            mermaid_code.append(f'    {source_id} --> {target_id}')

    # Add some styling classes
    mermaid_code.append("    classDef classpython fill:#3572A5,stroke:#fff,stroke-width:2px,color:#fff;")
    mermaid_code.append("    classDef classjavascript fill:#f1e05a,stroke:#fff,stroke-width:2px,color:#333;")
    mermaid_code.append("    classDef classtypescript fill:#2b7489,stroke:#fff,stroke-width:2px,color:#fff;")
    mermaid_code.append("    classDef classExternal fill:#eee,stroke:#999,stroke-width:2px,color:#333;")
    mermaid_code.append("    classDef classunknown fill:#ccc,stroke:#fff,stroke-width:2px,color:#333;")

    mermaid_code.append("```")

    os.makedirs('docs', exist_ok=True)
    with open('docs/architecture.md', 'w') as f:
        f.write("# Repository Architecture\n\n")
        f.write("This diagram was automatically generated based on the codebase structure.\n\n")
        f.write("\n".join(mermaid_code))

    print("Generated docs/architecture.md")

if __name__ == "__main__":
    generate_diagrams()
