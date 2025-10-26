from google.adk.agents import Agent
from ...config import GENAI_MODEL
from .prompt import ANALYZER_PROMPT
from .tools import check_vulnerability_patterns

analyzer_agent = Agent(
    name="analyzer_agent",
    model=GENAI_MODEL,
    description="Analyzes prompts for security vulnerabilities using pattern matching and LLM analysis",
    instruction=ANALYZER_PROMPT,
    tools=[check_vulnerability_patterns],
    output_key="vulnerability_findings",
)

