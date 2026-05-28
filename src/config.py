"""
Configuration for the ADD 3.0 Architecture Design Tool.
"""
import os

# Gemini API Configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL_NAME = "gemini-3.1-pro-preview"

# Generation parameters
GENERATION_CONFIG = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 16384,
}

# File paths
PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "prompts")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
VIEWS_DIR = os.path.join(OUTPUT_DIR, "views")

# Iteration configuration
ITERATIONS = [
    {
        "name": "Iteration 1: Establishing an Overall System Structure",
        "prompt_file": "iteration1.txt",
    },
    {
        "name": "Iteration 2: Identifying Structures to Support Primary Functionality",
        "prompt_file": "iteration2.txt",
    },
    {
        "name": "Iteration 3: Addressing Reliability and Availability Quality Attributes",
        "prompt_file": "iteration3.txt",
    },
    {
        "name": "Iteration 4: Addressing Development and Operations",
        "prompt_file": "iteration4.txt",
    },
]
