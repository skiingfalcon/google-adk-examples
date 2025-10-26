import os
from typing import List, Dict, Optional, Any
from pathlib import Path


def scan_directory(target_directory: str, extensions: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Scans a directory for files that may contain prompts.
    
    Args:
        target_directory: The directory path to scan
        extensions: List of file extensions to scan (e.g., ['.py', '.txt'])
                   If None, scans common code and text files
    
    Returns:
        Dictionary containing list of files found and scan statistics
    """
    if extensions is None:
        extensions = [".py", ".txt", ".md", ".json", ".yaml", ".yml", ".toml"]
    
    # Normalize the path
    target_path = Path(target_directory).resolve()
    
    if not target_path.exists():
        return {
            "error": f"Directory not found: {target_directory}",
            "files": [],
            "total_files": 0
        }
    
    if not target_path.is_dir():
        return {
            "error": f"Path is not a directory: {target_directory}",
            "files": [],
            "total_files": 0
        }
    
    # Find all matching files
    found_files = []
    excluded_dirs = {'__pycache__', '.git', 'node_modules', '.venv', 'venv', 'dist', 'build'}
    
    for root, dirs, files in os.walk(target_path):
        # Filter out excluded directories
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = Path(root) / file
                found_files.append({
                    "path": str(file_path),
                    "name": file,
                    "extension": file_path.suffix,
                    "size": file_path.stat().st_size
                })
    
    return {
        "files": found_files,
        "total_files": len(found_files),
        "scanned_directory": str(target_path),
        "extensions_scanned": extensions
    }

