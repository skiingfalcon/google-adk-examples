# Prompt Security Agent Architecture

## Overview

The Prompt Security Agent is a multi-agent system designed to analyze codebases for prompt security vulnerabilities. It follows the same architectural pattern as the O'Reilly AI Agents GCP Module 5 solution, using Google's Agent Development Kit (ADK).

## Architecture Pattern

```
prompt_security_agent/
├── agent.py                    # Main orchestrator (SequentialAgent)
├── config.py                   # Configuration and constants
├── __init__.py                 # Package exports
├── README.md                   # User documentation
├── ARCHITECTURE.md             # This file
├── run_example.py              # Example usage script
└── subagents/                  # Specialized sub-agents
    ├── scanner/                # Step 1: Prompt Discovery
    │   ├── scanner_agent.py
    │   ├── prompt.py
    │   └── tools/
    │       ├── scan_directory_tool.py
    │       └── extract_prompts_tool.py
    ├── analyzer/               # Step 2: Vulnerability Analysis
    │   ├── analyzer_agent.py
    │   ├── prompt.py
    │   └── tools/
    │       └── vulnerability_check_tool.py
    └── reporter/               # Step 3: Report Generation
        ├── reporter_agent.py
        ├── prompt.py
        └── tools/
            └── generate_report_tool.py
```

## Agent Flow

```
User Request
    ↓
[Orchestrator Agent]
    ↓
    ├─→ [Scanner Agent] ─────────────────────┐
    │   • scan_directory()                   │
    │   • extract_prompts_from_file()        │
    │   • Output: scanned_prompts            │
    │                                         ↓
    ├─→ [Analyzer Agent] ────────────────────┤
    │   • check_vulnerability_patterns()     │
    │   • LLM-based analysis                 │
    │   • Output: vulnerability_findings     │
    │                                         ↓
    └─→ [Reporter Agent] ────────────────────┘
        • generate_security_report()
        • LLM-enhanced recommendations
        • Output: security_report
            ↓
        Final Report
```

## Components

### 1. Orchestrator Agent (`agent.py`)

**Type:** `SequentialAgent`

**Purpose:** Coordinates the three-stage security analysis pipeline

**Responsibilities:**
- Parse user requests to identify target directories
- Orchestrate the sequential execution of subagents
- Handle errors and provide user feedback
- Maintain session state across subagent invocations

### 2. Scanner Agent (`subagents/scanner/`)

**Type:** `Agent`

**Purpose:** Discover and extract prompts from code files

**Tools:**
- `scan_directory()`: Recursively scans directories for relevant files
- `extract_prompts_from_file()`: Extracts prompts using:
  - **AST Analysis**: For Python files, parses the abstract syntax tree
  - **Pattern Matching**: For all files, uses regex patterns

**Output Key:** `scanned_prompts`

**Detection Strategy:**
- Identifies variables/parameters with prompt-related names
- Extracts multi-line strings (50+ characters)
- Finds f-strings and template strings
- Supports: `.py`, `.txt`, `.md`, `.json`, `.yaml`, `.yml`, `.toml`

### 3. Analyzer Agent (`subagents/analyzer/`)

**Type:** `Agent`

**Purpose:** Analyze prompts for security vulnerabilities

**Tools:**
- `check_vulnerability_patterns()`: Pattern-based vulnerability detection

**Vulnerability Categories:**
1. **Prompt Injection** (HIGH-CRITICAL)
   - User input concatenation without sanitization
   - Override instructions patterns

2. **Data Leakage** (CRITICAL)
   - Hardcoded credentials
   - API keys and secrets

3. **Prompt Leaking** (MEDIUM-HIGH)
   - System prompt exposure risks
   - Instruction extraction patterns

4. **Jailbreak Attempts** (HIGH)
   - DAN (Do Anything Now) patterns
   - Safety bypass attempts

5. **Adversarial Prompts** (MEDIUM-HIGH)
   - Social engineering patterns
   - Manipulation attempts

6. **Unsafe Code Execution** (CRITICAL)
   - eval/exec usage
   - SQL injection patterns

7. **Sensitive Data Exposure** (HIGH)
   - PII in prompts
   - Email addresses, phone numbers, SSNs

**Output Key:** `vulnerability_findings`

**Analysis Approach:**
1. Pattern-based initial detection (tool)
2. LLM-based deep analysis (agent reasoning)
3. Context-aware risk assessment
4. Severity classification

### 4. Reporter Agent (`subagents/reporter/`)

**Type:** `Agent`

**Purpose:** Generate comprehensive security reports

**Tools:**
- `generate_security_report()`: Formats structured reports

**Report Sections:**
1. Executive Summary
2. Severity Breakdown
3. Vulnerability Types
4. Detailed Findings
5. Risk Analysis
6. Recommendations
7. Resources

**Output Key:** `security_report`

## Session State Management

The agent uses ADK's session state to pass data between subagents:

```python
session.state = {
    'scanned_prompts': [
        {
            'text': str,
            'file': str,
            'line_number': int,
            'type': str,
            'variable_name': str
        },
        ...
    ],
    'vulnerability_findings': [
        {
            'file': str,
            'line_number': int,
            'prompt_text': str,
            'vulnerabilities': [
                {
                    'type': str,
                    'severity': str,
                    'description': str,
                    'pattern': str (optional)
                },
                ...
            ]
        },
        ...
    ],
    'security_report': str
}
```

## Configuration

See `config.py` for:
- LLM model selection
- File extensions to scan
- Vulnerability categories
- Severity levels

## Design Principles

1. **Modularity**: Each subagent is self-contained with its own tools
2. **Separation of Concerns**: Scanner finds, analyzer evaluates, reporter presents
3. **Extensibility**: Easy to add new vulnerability types or tools
4. **Tool-First**: Pattern-based tools provide quick wins, LLMs add intelligence
5. **State Management**: Structured data flow via session state

## Comparison to Module 5 Pattern

This implementation follows the same pattern as the O'Reilly module:

| Aspect | Module 5 | Prompt Security Agent |
|--------|----------|----------------------|
| Main Agent | `LoopAgent` (with SequentialAgent) | `SequentialAgent` |
| Subagents | 4 (prompt, image, scoring, checker) | 3 (scanner, analyzer, reporter) |
| Tools | Custom tools per subagent | Custom tools per subagent |
| Config | `config.py` with env vars | `config.py` with env vars |
| State | Session state passing | Session state passing |
| Output Keys | Per-agent output keys | Per-agent output keys |

## Usage Examples

### Via ADK Web UI
```bash
uv run adk web prompt_security_agent
```

Then ask:
- "Scan the ./my_agents directory for security issues"
- "Analyze ./petstore_agent for prompt injection vulnerabilities"

### Programmatically
```python
from prompt_security_agent import agent
from google.adk.sessions import Session

session = Session()
result = session.send_message(
    agent=agent,
    message="Scan ./my_first_agent for vulnerabilities"
)
print(result.text)
```

## Future Enhancements

1. **LoopAgent Integration**: Add iterative refinement for high-severity findings
2. **Remediation Suggestions**: Auto-generate code fixes
3. **Custom Rules**: Allow users to define vulnerability patterns
4. **Report Formats**: JSON, PDF, HTML output options
5. **Integration**: CI/CD pipeline integration
6. **Historical Tracking**: Compare scans over time

