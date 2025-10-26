from typing import List, Dict, Any, Optional
from collections import Counter
import json


def generate_security_report(findings: List[Dict[str, Any]], scan_info: Optional[Dict[str, Any]] = None) -> str:
    """
    Generates a formatted security report from analysis findings.
    
    Args:
        findings: List of vulnerability findings
        scan_info: Information about the scan (directory, files scanned, etc.)
    
    Returns:
        Formatted security report as a string
    """
    if scan_info is None:
        scan_info = {}
    
    # Aggregate statistics
    total_prompts = scan_info.get('total_prompts', 0)
    total_files = scan_info.get('total_files', 0)
    
    # Count vulnerabilities by type and severity
    vuln_by_type = Counter()
    vuln_by_severity = Counter()
    
    for finding in findings:
        for vuln in finding.get('vulnerabilities', []):
            vuln_by_type[vuln.get('type', 'unknown')] += 1
            vuln_by_severity[vuln.get('severity', 'unknown')] += 1
    
    # Build report
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("PROMPT SECURITY ANALYSIS REPORT")
    report_lines.append("=" * 80)
    report_lines.append("")
    
    # Summary section
    report_lines.append("SUMMARY")
    report_lines.append("-" * 80)
    report_lines.append(f"Directory Scanned: {scan_info.get('directory', 'N/A')}")
    report_lines.append(f"Files Analyzed: {total_files}")
    report_lines.append(f"Prompts Found: {total_prompts}")
    report_lines.append(f"Total Vulnerabilities: {sum(vuln_by_severity.values())}")
    report_lines.append("")
    
    # Severity breakdown
    report_lines.append("SEVERITY BREAKDOWN")
    report_lines.append("-" * 80)
    severity_order = ['critical', 'high', 'medium', 'low', 'info']
    for severity in severity_order:
        count = vuln_by_severity.get(severity, 0)
        if count > 0:
            emoji = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🔵', 'info': '⚪'}.get(severity, '')
            report_lines.append(f"{emoji} {severity.upper()}: {count}")
    report_lines.append("")
    
    # Vulnerability types
    if vuln_by_type:
        report_lines.append("VULNERABILITY TYPES")
        report_lines.append("-" * 80)
        for vuln_type, count in vuln_by_type.most_common():
            report_lines.append(f"  • {vuln_type.replace('_', ' ').title()}: {count}")
        report_lines.append("")
    
    # Detailed findings
    if findings:
        report_lines.append("DETAILED FINDINGS")
        report_lines.append("-" * 80)
        report_lines.append("")
        
        finding_num = 1
        for finding in findings:
            vulnerabilities = finding.get('vulnerabilities', [])
            if not vulnerabilities:
                continue
            
            file_path = finding.get('file', 'Unknown')
            line_num = finding.get('line_number', 'N/A')
            prompt_preview = finding.get('prompt_text', '')[:100]
            
            report_lines.append(f"Finding #{finding_num}")
            report_lines.append(f"File: {file_path}:{line_num}")
            report_lines.append(f"Prompt Preview: {prompt_preview}...")
            report_lines.append("")
            
            for vuln in vulnerabilities:
                severity = vuln.get('severity', 'unknown').upper()
                vuln_type = vuln.get('type', 'unknown').replace('_', ' ').title()
                description = vuln.get('description', 'No description')
                
                report_lines.append(f"  [{severity}] {vuln_type}")
                report_lines.append(f"  Description: {description}")
                
                if 'pattern' in vuln:
                    report_lines.append(f"  Pattern: {vuln['pattern']}")
                
                report_lines.append("")
            
            finding_num += 1
            report_lines.append("-" * 40)
            report_lines.append("")
    
    # Recommendations
    report_lines.append("RECOMMENDATIONS")
    report_lines.append("-" * 80)
    
    recommendations = []
    
    if vuln_by_type.get('prompt_injection', 0) > 0:
        recommendations.append(
            "• Sanitize and validate all user inputs before including in prompts"
        )
        recommendations.append(
            "• Use parameterized prompts or template systems with input escaping"
        )
    
    if vuln_by_type.get('data_leakage', 0) > 0 or vuln_by_type.get('sensitive_data_exposure', 0) > 0:
        recommendations.append(
            "• Remove hardcoded credentials, API keys, and sensitive data from prompts"
        )
        recommendations.append(
            "• Use environment variables or secure vaults for credentials"
        )
    
    if vuln_by_type.get('prompt_leaking', 0) > 0:
        recommendations.append(
            "• Implement output filtering to prevent system prompt leakage"
        )
        recommendations.append(
            "• Add instructions to never reveal system prompts or instructions"
        )
    
    if vuln_by_type.get('jailbreak_attempts', 0) > 0:
        recommendations.append(
            "• Implement robust input validation and filtering"
        )
        recommendations.append(
            "• Use model safety features and content filtering"
        )
    
    if not recommendations:
        recommendations.append("• No specific recommendations - continue following security best practices")
    
    for rec in recommendations:
        report_lines.append(rec)
    
    report_lines.append("")
    report_lines.append("=" * 80)
    report_lines.append("END OF REPORT")
    report_lines.append("=" * 80)
    
    return "\n".join(report_lines)

