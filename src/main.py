"""
ADD 3.0 Architecture Design Tool - Hotel Pricing System
========================================================
Automated interaction with Gemini to perform 4 iterations of ADD 3.0.

Usage:
    export GEMINI_API_KEY="your-api-key-here"
    python src/main.py
"""
import os
import sys
import datetime

import google.generativeai as genai

from config import (
    GEMINI_API_KEY,
    MODEL_NAME,
    GENERATION_CONFIG,
    PROMPTS_DIR,
    OUTPUT_DIR,
    VIEWS_DIR,
    ITERATIONS,
)
from utils import (
    get_timestamp,
    log_interaction,
    save_mermaid_views,
    save_conversation_log,
    calculate_stats,
    generate_report,
)


def load_prompt(filename):
    """Load a prompt file from the prompts directory."""
    filepath = os.path.join(PROMPTS_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def main():
    # --- Validate API Key ---
    if not GEMINI_API_KEY:
        print("ERROR: GEMINI_API_KEY environment variable is not set.")
        print("Please set it: export GEMINI_API_KEY='your-key-here'")
        sys.exit(1)

    # --- Setup ---
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(VIEWS_DIR, exist_ok=True)

    print("=" * 60)
    print("ADD 3.0 Architecture Design - Hotel Pricing System")
    print(f"Model: {MODEL_NAME}")
    print(f"Method: Direct LLM Interaction (Option 1)")
    print("=" * 60)

    # --- Initialize Gemini ---
    genai.configure(api_key=GEMINI_API_KEY)

    system_prompt = load_prompt("system_prompt.txt")

    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        generation_config=GENERATION_CONFIG,
        system_instruction=system_prompt,
    )

    chat = model.start_chat()

    # --- Run Iterations ---
    log_entries = []
    start_time = datetime.datetime.now()

    print(f"\nStart time: {get_timestamp()}")
    print("-" * 60)

    for i, iteration in enumerate(ITERATIONS, 1):
        iter_name = iteration["name"]
        prompt_text = load_prompt(iteration["prompt_file"])

        print(f"\n[{get_timestamp()}] Sending {iter_name}...")

        # Record user message
        user_timestamp = get_timestamp()
        log_interaction(log_entries, "user", prompt_text, timestamp=user_timestamp)

        # Send to Gemini
        try:
            response = chat.send_message(prompt_text)
        except Exception as e:
            print(f"  ERROR: {e}")
            log_interaction(
                log_entries, "model",
                f"[ERROR] API call failed: {e}",
                token_info=None,
            )
            continue

        # Extract response text and token info
        response_text = response.text
        token_info = None
        if hasattr(response, 'usage_metadata') and response.usage_metadata:
            metadata = response.usage_metadata
            token_info = {
                "prompt_tokens": getattr(metadata, 'prompt_token_count', 0),
                "candidates_tokens": getattr(metadata, 'candidates_token_count', 0),
                "total_tokens": getattr(metadata, 'total_token_count', 0),
            }

        # Record model response
        model_timestamp = get_timestamp()
        log_interaction(
            log_entries, "model", response_text,
            timestamp=model_timestamp, token_info=token_info,
        )

        # Save Mermaid views
        saved_views = save_mermaid_views(response_text, i, VIEWS_DIR)

        # Progress report
        print(f"  [{model_timestamp}] Response received.")
        print(f"  Response length: {len(response_text)} chars")
        if token_info:
            print(f"  Tokens - Prompt: {token_info['prompt_tokens']}, "
                  f"Response: {token_info['candidates_tokens']}, "
                  f"Total: {token_info['total_tokens']}")
        print(f"  Mermaid views saved: {len(saved_views)}")

    # --- Generate Outputs ---
    end_time = datetime.datetime.now()
    stats = calculate_stats(log_entries, start_time, end_time)

    print("\n" + "=" * 60)
    print("GENERATION COMPLETE")
    print("=" * 60)
    print(f"End time: {get_timestamp()}")
    print(f"Total time: {stats['time_cost_minutes']} minutes")
    print(f"Total tokens: {stats['total_tokens']} ({stats['token_consumption_k']}K)")
    print(f"Human interactions: {stats['human_interactions']}")

    # Save conversation log
    log_path = os.path.join(OUTPUT_DIR, "conversation_log.md")
    save_conversation_log(log_entries, log_path)
    print(f"\nConversation log saved: {log_path}")

    # Generate report
    report_path = os.path.join(OUTPUT_DIR, "report.md")
    generate_report(log_entries, stats, report_path)
    print(f"Report saved: {report_path}")

    # List saved views
    print(f"\nMermaid views saved in: {VIEWS_DIR}")
    for f in sorted(os.listdir(VIEWS_DIR)):
        if f.endswith('.mmd'):
            print(f"  - {f}")

    print("\n" + "=" * 60)
    print("DONE! Check the output/ directory for all deliverables.")
    print("=" * 60)


if __name__ == "__main__":
    main()
