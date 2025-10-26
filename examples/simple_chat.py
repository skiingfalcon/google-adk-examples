"""
Simple Chat Example
A basic example of how to interact with an ADK agent programmatically
"""

import os
from google.adk.agents import LlmAgent

def create_simple_agent():
    """Create a simple chat agent"""
    return LlmAgent(
        name="chat_agent",
        model="gemini-2.5-flash",
        description="A simple chat agent for basic conversations",
        instruction="You are a helpful assistant. Answer questions clearly and concisely."
    )

def main():
    """Main function to demonstrate agent usage"""
    print("Creating a simple chat agent...")
    agent = create_simple_agent()
    print(f"Agent '{agent.name}' created successfully!")
    print(f"Model: {agent.model}")
    print(f"Description: {agent.description}")

if __name__ == "__main__":
    main()

