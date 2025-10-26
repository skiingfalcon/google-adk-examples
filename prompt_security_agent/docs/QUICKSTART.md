# Prompt Security Agent - Quick Start Guide

## 🚀 What is this?

A production-ready AI agent that scans your codebase for prompt security vulnerabilities, built following Google ADK best practices and the O'Reilly AI Agents GCP Module 5 pattern.

## ⚡ Quick Start

### Option 1: ADK Web UI (Recommended)

```bash
cd /Users/skifalcon/projects/adk-bootcamp-python
uv run adk web prompt_security_agent
```

Then in the web UI, ask:
```
Scan the ./my_first_agent directory for prompt security vulnerabilities
```

### Option 2: Programmatic Usage

```bash
cd /Users/skifalcon/projects/adk-bootcamp-python
uv run python prompt_security_agent/run_example.py
```

Or import in your own code:
```python
from prompt_security_agent import agent
from google.adk.sessions import Session

session = Session()
result = session.send_message(
    agent=agent,
    message="Scan ./petstore_agent for security issues"
)
print(result.text)
```

## 📁 What Gets Analyzed?

The agent scans for prompts in:
- ✅ Python files (`.py`) - Uses AST analysis
- ✅ Text files (`.txt`)
- ✅ Markdown (`.md`)
- ✅ Config files (`.json`, `.yaml`, `.yml`, `.toml`)

## 🛡️ Security Checks

1. **Prompt Injection** - User input concatenation risks
2. **Data Leakage** - Hardcoded credentials and secrets
3. **Prompt Leaking** - System prompt exposure risks
4. **Jailbreak Attempts** - Safety bypass patterns
5. **Adversarial Prompts** - Malicious patterns
6. **Unsafe Code Execution** - eval/exec usage
7. **Sensitive Data** - PII, emails, phone numbers

## 📊 Sample Output

```
================================================================================
PROMPT SECURITY ANALYSIS REPORT
================================================================================

SUMMARY
--------------------------------------------------------------------------------
Directory Scanned: ./my_first_agent
Files Analyzed: 3
Prompts Found: 2
Total Vulnerabilities: 1

SEVERITY BREAKDOWN
--------------------------------------------------------------------------------
🟡 MEDIUM: 1

DETAILED FINDINGS
--------------------------------------------------------------------------------
Finding #1
File: ./my_first_agent/agent.py:7
Prompt Preview: You are a friendly assistant...

  [MEDIUM] Prompt Injection
  Description: Multiple variable substitutions detected - ensure user input is sanitized
  
RECOMMENDATIONS
--------------------------------------------------------------------------------
• Sanitize and validate all user inputs before including in prompts
• Use parameterized prompts or template systems with input escaping
```

## 🏗️ Architecture

```
Scanner Agent → Analyzer Agent → Reporter Agent
     ↓               ↓                 ↓
  Find prompts   Check vulns    Generate report
```

**3 Subagents:**
1. **Scanner** - Finds prompts using AST + pattern matching
2. **Analyzer** - Checks for 7 vulnerability types
3. **Reporter** - Creates detailed security reports

**8 Custom Tools:**
- `scan_directory()` - Directory traversal
- `extract_prompts_from_file()` - AST + regex extraction
- `check_vulnerability_patterns()` - Pattern-based detection
- `generate_security_report()` - Report formatting

## 📖 Example Prompts

Try asking the agent:

```
"Scan the ./shopping_agent directory for security issues"

"Analyze ./data_agent for prompt injection vulnerabilities"

"Check all agents in this codebase for sensitive data exposure"

"Scan ./news_agent and focus on data leakage risks"
```

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Change the LLM model
GENAI_MODEL = "gemini-2.0-flash-exp"

# Add more file extensions
SCAN_EXTENSIONS = [".py", ".txt", ".md", ".json"]

# Modify vulnerability categories
VULNERABILITY_CATEGORIES = [...]
```

## 📚 Documentation

- `README.md` - User guide and features
- `ARCHITECTURE.md` - Technical architecture details
- `config.py` - Configuration options

## 🎯 Try It Now!

1. **Scan your first agent:**
   ```bash
   uv run adk web prompt_security_agent
   # Then ask: "Scan ./my_first_agent for vulnerabilities"
   ```

2. **Scan all agents:**
   ```bash
   # Ask: "Scan the current directory for all prompt security issues"
   ```

3. **Export findings:**
   The agent provides detailed reports you can copy/paste for documentation

## 💡 Pro Tips

- **Specific Paths**: Always specify the directory to scan
- **Iterative**: Scan individual agents first, then whole codebase
- **Review**: Agent findings are suggestions - review in context
- **Fix & Rescan**: After fixing issues, run again to verify

## 🤝 Pattern Credits

This agent follows the same architectural pattern as the O'Reilly AI Agents on GCP - Module 5 solution, demonstrating:
- Multi-agent orchestration
- Sequential agent pattern
- Custom tool development
- Session state management
- Production-ready structure

Enjoy secure prompt engineering! 🔒

