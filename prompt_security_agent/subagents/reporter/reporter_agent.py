from google.adk.agents import Agent
from ...config import GENAI_MODEL
from .prompt import REPORTER_PROMPT
from .tools import generate_security_report

reporter_agent = Agent(
    name="reporter_agent",
    model=GENAI_MODEL,
    description="Generates comprehensive security reports from vulnerability findings",
    instruction=REPORTER_PROMPT,
    tools=[generate_security_report],
    output_key="security_report",
)

