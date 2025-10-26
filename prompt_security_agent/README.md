# Prompt Security Agent

An AI agent that analyzes codebases for prompt security vulnerabilities.

## Overview

The Prompt Security Agent scans directories for prompts in code files, analyzes them for security vulnerabilities, and generates comprehensive security reports.

## Architecture

The agent follows a multi-agent pattern with three specialized subagents:

1. **Scanner Agent**: Identifies and extracts prompts from code files using pattern matching and AST analysis
2. **Analyzer Agent**: Analyzes extracted prompts for security vulnerabilities and risks
3. **Reporter Agent**: Generates detailed security reports with findings and recommendations

## Features

- 🔍 **Smart Prompt Detection**: Uses AST analysis and pattern matching to find prompts in various file formats
- 🛡️ **Vulnerability Detection**: Analyzes prompts for:
  - Prompt injection vulnerabilities
  - Data leakage risks
  - Prompt leaking attempts
  - Jailbreak vulnerabilities
  - Adversarial prompt patterns
  - Unsafe code execution risks
  - Sensitive data exposure
- 📊 **Comprehensive Reports**: Generates detailed security reports with severity ratings and remediation suggestions

## Usage

### Run with ADK Web UI

```bash
cd /Users/skifalcon/projects/adk-bootcamp-python
uv run adk web prompt_security_agent
```

### Run Programmatically

```python
from prompt_security_agent import agent
from google.adk.sessions import Session

session = Session()
result = session.send_message(
    agent=agent,
    message="Scan /path/to/your/codebase for prompt security vulnerabilities"
)
print(result.text)
```

### Environment Variables

- `GENAI_MODEL`: LLM model to use (default: "gemini-2.0-flash-exp")
- `TARGET_DIR`: Default directory to scan (default: ".")

## Example Prompts

- "Scan the ./my_agents directory for prompt security issues"
- "Analyze all prompts in this codebase for injection vulnerabilities"
- "Check /path/to/project for sensitive data in prompts"

## Security Checks

The agent checks for:

1. **Prompt Injection**: User input being directly concatenated into prompts
2. **Data Leakage**: Prompts that might expose sensitive information
3. **Prompt Leaking**: Vulnerabilities where the system prompt might be exposed
4. **Jailbreak Attempts**: Patterns that could bypass safety guardrails
5. **Adversarial Prompts**: Malicious prompt patterns
6. **Unsafe Code Execution**: Prompts that might lead to code execution
7. **Sensitive Data Exposure**: Hardcoded credentials, API keys, or PII in prompts

## Output

The agent provides a structured report including:
- Total prompts found
- Vulnerability summary by severity
- Detailed findings for each issue
- Remediation recommendations
- File locations and line numbers

