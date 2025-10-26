import subprocess
import json
import tempfile
import os
from typing import Dict, List, Any, Optional
from pathlib import Path


def run_semgrep_scan(target_directory: str, custom_rules: Optional[str] = None) -> Dict[str, Any]:
    """
    Run semgrep static analysis on a directory to find prompts and potential vulnerabilities.
    
    Args:
        target_directory: Directory to scan
        custom_rules: Optional custom semgrep rules (YAML format)
    
    Returns:
        Dictionary containing semgrep results and metadata
    """
    try:
        # Check if semgrep is installed
        result = subprocess.run(["semgrep", "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            return {
                "error": "Semgrep not installed. Install with: pip install semgrep",
                "results": [],
                "total_findings": 0
            }
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return {
            "error": "Semgrep not found. Install with: pip install semgrep",
            "results": [],
            "total_findings": 0
        }
    
    # Create temporary rules file if custom rules provided
    rules_file = None
    if custom_rules:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(custom_rules)
            rules_file = f.name
    
    try:
        # Build semgrep command
        cmd = [
            "semgrep",
            "--json",  # JSON output for parsing
            "--config=auto",  # Use auto config for security rules
            "--no-git-ignore",  # Don't respect .gitignore
            "--max-target-bytes=10000000",  # 10MB limit per file
            target_directory
        ]
        
        # Add custom rules if provided
        if rules_file:
            cmd.extend(["--config", rules_file])
        
        # Run semgrep
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
            cwd=target_directory
        )
        
        if result.returncode not in [0, 1]:  # 0=success, 1=findings found
            return {
                "error": f"Semgrep execution failed: {result.stderr}",
                "results": [],
                "total_findings": 0
            }
        
        # Parse JSON results
        try:
            semgrep_results = json.loads(result.stdout)
        except json.JSONDecodeError as e:
            return {
                "error": f"Failed to parse semgrep JSON output: {e}",
                "results": [],
                "total_findings": 0
            }
        
        # Process results
        findings = []
        for finding in semgrep_results.get("results", []):
            findings.append({
                "rule_id": finding.get("check_id", "unknown"),
                "message": finding.get("message", ""),
                "severity": finding.get("extra", {}).get("severity", "INFO"),
                "file": finding.get("path", ""),
                "line": finding.get("start", {}).get("line", 0),
                "column": finding.get("start", {}).get("col", 0),
                "end_line": finding.get("end", {}).get("line", 0),
                "end_column": finding.get("end", {}).get("col", 0),
                "code_snippet": finding.get("extra", {}).get("lines", ""),
                "metadata": finding.get("extra", {}).get("metadata", {})
            })
        
        return {
            "results": findings,
            "total_findings": len(findings),
            "scan_directory": target_directory,
            "semgrep_version": result.stdout.split('\n')[0] if result.stdout else "unknown",
            "errors": semgrep_results.get("errors", [])
        }
        
    finally:
        # Clean up temporary rules file
        if rules_file and os.path.exists(rules_file):
            os.unlink(rules_file)


def create_prompt_extraction_rules() -> str:
    """
    Create custom semgrep rules for prompt extraction.
    
    Returns:
        YAML string containing custom rules for finding prompts
    """
    return """
rules:
  # Find prompt variables in Python
  - id: prompt-variable-assignment
    patterns:
      - pattern: $VAR = $VALUE
      - metavariable-pattern:
          metavariable: $VAR
          patterns:
            - pattern-regex: "(prompt|instruction|system_prompt|user_prompt|template|message)"
      - metavariable-pattern:
          metavariable: $VALUE
          patterns:
            - pattern-regex: ".*[a-zA-Z]{20,}.*"  # Long string likely to be a prompt
    message: Found prompt variable assignment
    languages: [python]
    severity: INFO
    
  # Find prompt function arguments
  - id: prompt-function-argument
    patterns:
      - pattern: $FUNC(..., $ARG=$VALUE, ...)
      - metavariable-pattern:
          metavariable: $ARG
          patterns:
            - pattern-regex: "(prompt|instruction|system_prompt|template)"
      - metavariable-pattern:
          metavariable: $VALUE
          patterns:
            - pattern-regex: ".*[a-zA-Z]{20,}.*"
    message: Found prompt function argument
    languages: [python]
    severity: INFO
    
  # Find f-strings with prompts
  - id: prompt-f-string
    patterns:
      - pattern: f"$TEXT"
      - metavariable-pattern:
          metavariable: $TEXT
          patterns:
            - pattern-regex: ".*(prompt|instruction|system|template).*"
    message: Found potential prompt in f-string
    languages: [python]
    severity: INFO
    
  # Find hardcoded credentials (security issue)
  - id: hardcoded-credentials
    patterns:
      - pattern-regex: "(api[_-]?key|secret|password|token|credential)\\s*=\\s*['\"][^'\"]{10,}['\"]"
    message: Potential hardcoded credentials found
    languages: [python]
    severity: HIGH
    
  # Find eval/exec usage (security risk)
  - id: dangerous-exec
    patterns:
      - pattern: eval($EXPR)
      - pattern: exec($EXPR)
    message: Use of dangerous eval/exec function
    languages: [python]
    severity: HIGH
    
  # Find prompt injection patterns
  - id: prompt-injection-risk
    patterns:
      - pattern-regex: "(ignore\\s+(previous|all|above)|disregard\\s+(previous|all)|system:\\s*you\\s+are|new\\s+instructions?:)"
    message: Potential prompt injection pattern
    languages: [python]
    severity: MEDIUM
"""


def extract_prompts_with_semgrep(target_directory: str) -> Dict[str, Any]:
    """
    Extract prompts using semgrep with custom rules.
    
    Args:
        target_directory: Directory to scan
        
    Returns:
        Dictionary containing extracted prompts and metadata
    """
    custom_rules = create_prompt_extraction_rules()
    results = run_semgrep_scan(target_directory, custom_rules)
    
    if "error" in results:
        return results
    
    # Filter and format results for prompt extraction
    prompt_findings = []
    for finding in results["results"]:
        if finding["rule_id"] in [
            "prompt-variable-assignment",
            "prompt-function-argument", 
            "prompt-f-string"
        ]:
            prompt_findings.append({
                "text": finding["code_snippet"].strip(),
                "file": finding["file"],
                "line_number": finding["line"],
                "rule_type": finding["rule_id"],
                "severity": finding["severity"],
                "message": finding["message"]
            })
    
    return {
        "prompts": prompt_findings,
        "total_prompts": len(prompt_findings),
        "scan_directory": target_directory,
        "semgrep_findings": results["total_findings"],
        "errors": results.get("errors", [])
    }
