import os
import json
import subprocess
from openai import OpenAI

def get_recent_diff():
    try:
        # Get the diff of the last commit. If it's a new repo or no commits, this might fail.
        result = subprocess.run(['git', 'diff', 'HEAD~1', 'HEAD'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout[:5000] # Limit to 5000 chars to avoid huge token usage
    except Exception:
        pass
    return "No recent diff available or git is not initialized."

def generate_ai_summary():
    # If there is no OPENAI_API_KEY, we will create a dummy summary
    api_key = os.environ.get("OPENAI_API_KEY")

    stats_str = ""
    if os.path.exists('repo_stats.json'):
        with open('repo_stats.json', 'r') as f:
            stats = json.load(f)
            stats_str = json.dumps(stats, indent=2)

    diff_str = get_recent_diff()

    if not api_key:
        print("No OPENAI_API_KEY found. Generating dummy AI summary.")
        dummy_summary = {
            "overview": "This repository appears to be an automated self-documenting system.",
            "architecture": "The architecture consists of a set of Python scripts that analyze the codebase, generate dependency graphs, and automatically construct a cohesive documentation package including architecture diagrams and an updated README.",
            "components": "Key components include scripts for analysis, diagram generation, AI summarization, and README compilation.",
            "recent_changes": "The system was recently initialized with its core automation scripts."
        }
        with open('ai_summary.json', 'w') as f:
            json.dump(dummy_summary, f, indent=2)
        return

    client = OpenAI(api_key=api_key)

    prompt = f"""
    You are an AI Repository Documentation Agent.

    Here are the repository statistics:
    ```json
    {stats_str}
    ```

    Here is the recent git diff:
    ```diff
    {diff_str}
    ```

    Analyze the provided repository statistics and recent diff.
    Respond strictly in JSON format with the following keys:
    - "overview": A concise overview of what the repository does based on its contents.
    - "architecture": A description of the high-level system architecture.
    - "components": A summary of the key components and how they interact.
    - "recent_changes": A brief summary of what changed in the recent commit.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant that outputs JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" }
        )

        output = response.choices[0].message.content
        summary = json.loads(output)

        with open('ai_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)

        print("Successfully generated AI summary.")
    except Exception as e:
        print(f"Failed to generate AI summary via API: {e}")
        # Fallback to dummy
        dummy_summary = {
            "overview": "Overview generation failed.",
            "architecture": "Architecture generation failed.",
            "components": "Components generation failed.",
            "recent_changes": "Recent changes generation failed."
        }
        with open('ai_summary.json', 'w') as f:
            json.dump(dummy_summary, f, indent=2)

if __name__ == "__main__":
    generate_ai_summary()
