import ast
import re
from typing import List, Dict, Any
from pathlib import Path


def extract_prompts_from_file(file_path: str) -> Dict[str, Any]:
    """
    Extracts prompts from a file using AST analysis and pattern matching.
    
    Args:
        file_path: Path to the file to analyze
    
    Returns:
        Dictionary containing extracted prompts and metadata
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        return {
            "error": f"File not found: {file_path}",
            "prompts": []
        }
    
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        return {
            "error": f"Could not read file: {e}",
            "prompts": []
        }
    
    prompts = []
    
    # Python file - use AST analysis
    if file_path.suffix == '.py':
        prompts.extend(_extract_from_python_ast(content, file_path))
    
    # Pattern-based extraction for all files
    prompts.extend(_extract_with_patterns(content, file_path))
    
    # Remove duplicates while preserving order
    seen = set()
    unique_prompts = []
    for prompt in prompts:
        prompt_key = (prompt['text'][:100], prompt['line_number'])
        if prompt_key not in seen:
            seen.add(prompt_key)
            unique_prompts.append(prompt)
    
    return {
        "file": str(file_path),
        "prompts": unique_prompts,
        "total_prompts": len(unique_prompts)
    }


def _extract_from_python_ast(content: str, file_path: Path) -> List[Dict]:
    """Extract prompts from Python files using AST analysis."""
    prompts = []
    
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return prompts
    
    # Keywords that often indicate prompts
    prompt_indicators = [
        'prompt', 'instruction', 'system_prompt', 'user_prompt',
        'template', 'message', 'system_message', 'description'
    ]
    
    for node in ast.walk(tree):
        # Check string assignments
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    var_name = target.id.lower()
                    if any(indicator in var_name for indicator in prompt_indicators):
                        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                            prompts.append({
                                'text': node.value.value,
                                'line_number': node.lineno,
                                'variable_name': target.id,
                                'type': 'assignment',
                                'file': str(file_path)
                            })
        
        # Check function arguments
        if isinstance(node, ast.Call):
            for keyword in node.keywords:
                if keyword.arg and any(indicator in keyword.arg.lower() for indicator in prompt_indicators):
                    if isinstance(keyword.value, ast.Constant) and isinstance(keyword.value.value, str):
                        prompts.append({
                            'text': keyword.value.value,
                            'line_number': keyword.value.lineno if hasattr(keyword.value, 'lineno') else 0,
                            'parameter_name': keyword.arg,
                            'type': 'function_argument',
                            'file': str(file_path)
                        })
    
    return prompts


def _extract_with_patterns(content: str, file_path: Path) -> List[Dict]:
    """Extract prompts using regex patterns."""
    prompts = []
    
    # Pattern for common prompt structures
    patterns = [
        # Multi-line strings with prompt indicators
        r'(?:prompt|instruction|system_prompt|template)\s*=\s*["\']([^"\']{50,})["\']',
        # Triple-quoted strings (often used for prompts)
        r'["\']{{3}}((?:(?!["\']{{3}}).){100,}?)["\']{{3}}',
        # f-strings with prompts
        r'f["\']([^"\']{50,})["\']',
    ]
    
    lines = content.split('\n')
    
    for pattern in patterns:
        for match in re.finditer(pattern, content, re.DOTALL):
            text = match.group(1) if len(match.groups()) > 0 else match.group(0)
            
            # Find line number
            line_num = content[:match.start()].count('\n') + 1
            
            # Only include if it looks like a prompt (has some natural language)
            if len(text.split()) > 5:
                prompts.append({
                    'text': text.strip(),
                    'line_number': line_num,
                    'type': 'pattern_match',
                    'file': str(file_path)
                })
    
    return prompts

