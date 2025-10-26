from google.adk.agents import Agent
from ...config import GENAI_MODEL
from .prompt import SCANNER_PROMPT
from .tools import scan_directory, extract_prompts_from_file, run_semgrep_scan, extract_prompts_with_semgrep

scanner_agent = Agent(
    name="scanner_agent",
    model=GENAI_MODEL,
    description="Scans directories and extracts prompts from code files using AST, pattern matching, and semgrep",
    instruction=SCANNER_PROMPT,
    tools=[scan_directory, extract_prompts_from_file, run_semgrep_scan, extract_prompts_with_semgrep],
    output_key="scanned_prompts",
)

