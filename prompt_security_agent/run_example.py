"""
Example script demonstrating how to use the Prompt Security Agent programmatically.
"""

from google.adk.sessions import Session
from prompt_security_agent import agent
from dotenv import load_dotenv

load_dotenv()


def main():
    """Run the prompt security agent on a target directory."""
    
    # Create a session
    session = Session()
    
    # Example 1: Scan a specific directory
    print("=" * 80)
    print("Prompt Security Agent - Example Usage")
    print("=" * 80)
    print()
    
    # You can modify this path to scan your own codebase
    target_directory = "./my_first_agent"
    
    message = f"Scan {target_directory} for prompt security vulnerabilities"
    
    print(f"Request: {message}")
    print()
    print("Running security analysis...")
    print()
    
    # Send message to the agent
    result = session.send_message(
        agent=agent,
        message=message
    )
    
    # Print the result
    print(result.text)
    
    # Access structured data from session state if needed
    if hasattr(session, 'state'):
        if 'scanned_prompts' in session.state:
            print(f"\nPrompts found: {len(session.state['scanned_prompts'])}")
        if 'vulnerability_findings' in session.state:
            print(f"Vulnerabilities found: {len(session.state['vulnerability_findings'])}")


if __name__ == "__main__":
    main()

