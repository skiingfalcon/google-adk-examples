import os

# LLM Model configuration
GENAI_MODEL = os.getenv("GENAI_MODEL", "gemini-2.0-flash-exp")

# Scanner configuration
DEFAULT_TARGET_DIR = os.getenv("TARGET_DIR", ".")
SCAN_EXTENSIONS = [".py", ".txt", ".md", ".json", ".yaml", ".yml"]

# Analyzer configuration
VULNERABILITY_CATEGORIES = [
    "prompt_injection",
    "data_leakage",
    "prompt_leaking",
    "jailbreak_attempts",
    "adversarial_prompts",
    "unsafe_code_execution",
    "sensitive_data_exposure",
]

# Severity levels
SEVERITY_LEVELS = ["critical", "high", "medium", "low", "info"]

