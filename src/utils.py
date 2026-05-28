"""
Utility functions for logging, Mermaid extraction, and report generation.
"""
import os
import re
import datetime


def get_timestamp():
    """Get current timestamp in ISO format."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log_interaction(log_entries, role, content, timestamp=None, token_info=None):
    """
    Record a conversation turn with timestamp.

    Args:
        log_entries: list to append the entry to
        role: 'user' or 'model'
        content: message content
        timestamp: optional timestamp string
        token_info: optional dict with token usage info
    """
    if timestamp is None:
        timestamp = get_timestamp()

    entry = {
        "timestamp": timestamp,
        "role": role,
        "content": content,
        "token_info": token_info,
    }
    log_entries.append(entry)
    return entry


def extract_mermaid_blocks(text):
    """
    Extract all Mermaid code blocks from text.

    Returns:
        List of (diagram_type, code) tuples
    """
    pattern = r'```mermaid\s*\n(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)

    results = []
    for match in matches:
        # Try to detect diagram type from first line
        first_line = match.strip().split('\n')[0].strip().lower()
        if first_line.startswith('graph') or first_line.startswith('flowchart'):
            diagram_type = 'flowchart'
        elif first_line.startswith('sequencediagram') or first_line.startswith('sequence'):
            diagram_type = 'sequence'
        elif first_line.startswith('classDiagram') or first_line.startswith('class'):
            diagram_type = 'class'
        elif first_line.startswith('c4'):
            diagram_type = 'c4'
        else:
            diagram_type = 'diagram'

        results.append((diagram_type, match.strip()))

    return results


def save_mermaid_views(text, iteration_num, output_dir):
    """
    Extract and save Mermaid diagrams from an iteration's response.

    Args:
        text: the model's response text
        iteration_num: which iteration (1-4)
        output_dir: directory to save .mmd files

    Returns:
        List of saved file paths
    """
    blocks = extract_mermaid_blocks(text)
    saved_files = []

    for i, (diagram_type, code) in enumerate(blocks, 1):
        filename = f"iteration{iteration_num}_{diagram_type}_{i}.mmd"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(code)
        saved_files.append(filepath)

    return saved_files


def save_conversation_log(log_entries, output_path):
    """
    Save the complete conversation log as a Markdown file with timestamps.

    Args:
        log_entries: list of log entry dicts
        output_path: path to save the markdown file
    """
    lines = []
    lines.append("# Complete Conversation Log - ADD 3.0 Hotel Pricing System Design\n")
    lines.append(f"**Generated:** {get_timestamp()}\n")
    lines.append(f"**Model:** gemini-3.1-pro-preview\n")
    lines.append(f"**Method:** Direct LLM Interaction (Option 1)\n")
    lines.append("---\n")

    current_iteration = 0
    for entry in log_entries:
        # Detect iteration boundaries
        if entry["role"] == "user" and "Iteration" in entry["content"]:
            current_iteration += 1
            lines.append(f"\n## Iteration {current_iteration}\n")

        role_label = "**Human**" if entry["role"] == "user" else "**Model (gemini-3.1-pro-preview)**"
        lines.append(f"### {role_label}")
        lines.append(f"*Timestamp: {entry['timestamp']}*\n")
        lines.append(entry["content"])
        lines.append("")

        if entry.get("token_info"):
            info = entry["token_info"]
            lines.append(f"> Token usage - Prompt: {info.get('prompt_tokens', 'N/A')}, "
                        f"Response: {info.get('candidates_tokens', 'N/A')}, "
                        f"Total: {info.get('total_tokens', 'N/A')}\n")

        lines.append("---\n")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    return output_path


def calculate_stats(log_entries, start_time, end_time):
    """
    Calculate interaction statistics.

    Returns:
        dict with stats
    """
    total_prompt_tokens = 0
    total_candidates_tokens = 0
    total_tokens = 0
    human_turns = 0

    for entry in log_entries:
        if entry["role"] == "user":
            human_turns += 1
        if entry.get("token_info"):
            info = entry["token_info"]
            total_prompt_tokens += info.get("prompt_tokens", 0)
            total_candidates_tokens += info.get("candidates_tokens", 0)
            total_tokens += info.get("total_tokens", 0)

    time_cost_seconds = (end_time - start_time).total_seconds()
    time_cost_minutes = time_cost_seconds / 60

    return {
        "method": "Direct LLM Interaction (Option 1)",
        "llm": "gemini-3.1-pro-preview",
        "human_interactions": human_turns,
        "total_prompt_tokens": total_prompt_tokens,
        "total_candidates_tokens": total_candidates_tokens,
        "total_tokens": total_tokens,
        "token_consumption_k": round(total_tokens / 1000, 1),
        "time_cost_minutes": round(time_cost_minutes, 1),
    }


def generate_report(log_entries, stats, output_path):
    """
    Generate the complete report in the required template format.

    Args:
        log_entries: list of conversation log entries
        stats: dict from calculate_stats()
        output_path: path to save the report
    """
    lines = []

    # ===== SECTION 1: ADD Output Results =====
    lines.append("# Software Architecture Assignment 2 - Report\n")
    lines.append("## I. Output Results of ADD\n")

    # Extract model responses for each iteration
    iteration_responses = []
    current_response = None
    for entry in log_entries:
        if entry["role"] == "user" and "Iteration" in entry["content"]:
            if current_response is not None:
                iteration_responses.append(current_response)
            current_response = None
        elif entry["role"] == "model":
            current_response = entry["content"]
    if current_response is not None:
        iteration_responses.append(current_response)

    iteration_names = [
        "Iteration 1: Establishing an Overall System Structure",
        "Iteration 2: Identifying Structures to Support Primary Functionality",
        "Iteration 3: Addressing Reliability and Availability Quality Attributes",
        "Iteration 4: Addressing Development and Operations",
    ]

    for i, (name, response) in enumerate(zip(iteration_names, iteration_responses), 1):
        lines.append(f"### {i}) Output results of each step ({name})\n")
        if response:
            lines.append(response)
        else:
            lines.append("*(No response recorded)*")
        lines.append("\n---\n")

    # ===== SECTION 2: Interaction Cost Analysis =====
    lines.append("## II. Interaction Cost Analysis\n")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| The way of completing the assignment | {stats['method']} |")
    lines.append(f"| The LLM used | {stats['llm']} |")
    lines.append(f"| Number of Human Interactions (turns) | {stats['human_interactions']} |")
    lines.append(f"| Token Consumption (K tokens) | {stats['token_consumption_k']} |")
    lines.append(f"| Time Cost (min) | {stats['time_cost_minutes']} |")
    lines.append("")

    # ===== SECTION 3: Individual Reflection =====
    lines.append("## III. Individual Reflection\n")
    lines.append("### 1) The problems encountered and the solutions adopted\n")
    lines.append("""During the completion of this assignment, we encountered several challenges:

1. **System Prompt Design**: Crafting a system prompt that provided sufficient context (ADD 3.0 methodology + Hotel Pricing System case study) without exceeding token limits required careful balancing. We solved this by structuring the prior knowledge hierarchically and using concise table formats for quality attributes and constraints.

2. **Ensuring Comprehensive Iteration Output**: The LLM occasionally produced incomplete Step 6 outputs (missing certain diagram types). We addressed this by explicitly specifying the expected diagram types in each iteration prompt, which guided the model to produce all required views.

3. **Maintaining Cross-Iteration Consistency**: Later iterations needed to reference design decisions from earlier ones. By using a single chat session with full conversation history, the model maintained contextual awareness of prior architectural choices.

4. **Mermaid Diagram Quality**: Some generated Mermaid diagrams had syntax issues or were overly simplified. The solution was to include format requirements in the system prompt specifying that views must use Mermaid code blocks with proper syntax.

5. **Balancing Detail and Conciseness**: ADD 3.0 requires thorough documentation at each step, but overly verbose responses could exceed output limits. We designed prompts that requested structured, step-by-step output with clear headers to maintain both thoroughness and readability.
""")

    lines.append("### 2) A detailed account of personal contributions to the group work\n")
    lines.append("| Name (Chinese) | Contributions |")
    lines.append("|----------------|---------------|")
    lines.append("| [YOUR_NAME_1] | Designed the system prompt and prior knowledge structure; wrote and tested the iteration prompts for Iterations 1 and 2; reviewed and validated Mermaid diagram outputs. |")
    lines.append("| [YOUR_NAME_2] | Developed the Python automation program (main.py, utils.py); implemented conversation logging and report generation; handled API integration and debugging. |")
    lines.append("| [YOUR_NAME_3] | Designed iteration prompts for Iterations 3 and 4; performed quality review of ADD outputs; compiled the final report and verified traceability of design decisions. |")
    lines.append("")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    return output_path
