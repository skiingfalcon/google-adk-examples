from google.adk.agents import SequentialAgent
from dotenv import load_dotenv
from .subagents.scanner import scanner_agent
from .subagents.analyzer import analyzer_agent
from .subagents.reporter import reporter_agent

load_dotenv()

# Main orchestrator agent that runs the security analysis pipeline
# This follows a sequential pattern:
# 1. Scanner Agent: Finds and extracts prompts from code files
# 2. Analyzer Agent: Analyzes prompts for security vulnerabilities
# 3. Reporter Agent: Generates comprehensive security report

agent = SequentialAgent(
    name="prompt_security_agent",
    description="""
    Analyzes codebases for prompt security vulnerabilities.
    
    This agent performs a comprehensive security analysis of prompts in your codebase by:
    1. Scanning directories to find prompts in code files (Python, text, config files)
    2. Extracting prompts using AST analysis and pattern matching
    3. Analyzing prompts for security vulnerabilities (injection, data leakage, etc.)
    4. Generating a detailed security report with findings and recommendations
    """,
    sub_agents=[
        scanner_agent,    # Step 1: Scan and extract prompts
        analyzer_agent,   # Step 2: Analyze for vulnerabilities
        reporter_agent,   # Step 3: Generate report
    ],
)

# Alias for compatibility
root_agent = agent

