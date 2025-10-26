# Agent Handoff Mechanism in Prompt Security Agent

## Overview

The Prompt Security Agent uses **SequentialAgent** orchestration with **session state** for data passing between agents. This creates a clean pipeline where each agent builds on the previous agent's work.

## The Key Components

### 1. SequentialAgent (Orchestrator)

```python
agent = SequentialAgent(
    name="prompt_security_agent",
    sub_agents=[
        scanner_agent,    # Step 1
        analyzer_agent,   # Step 2  
        reporter_agent,   # Step 3
    ],
)
```

**What it does:**
- Executes subagents **in order** (sequential execution)
- Maintains a **shared session** across all subagents
- Each subagent completes before the next one starts

### 2. Output Keys (Data Storage)

Each subagent has an `output_key` that defines where it stores its results:

```python
scanner_agent = Agent(
    name="scanner_agent",
    tools=[scan_directory, extract_prompts_from_file],
    output_key="scanned_prompts",  # ✅ Stores results here
)

analyzer_agent = Agent(
    name="analyzer_agent", 
    tools=[check_vulnerability_patterns],
    output_key="vulnerability_findings",  # ✅ Stores results here
)

reporter_agent = Agent(
    name="reporter_agent",
    tools=[generate_security_report],
    output_key="security_report",  # ✅ Stores results here
)
```

### 3. Session State (Shared Memory)

All agents share the same `session.state` dictionary:

```python
session.state = {
    'scanned_prompts': [...],           # Written by scanner_agent
    'vulnerability_findings': [...],     # Written by analyzer_agent
    'security_report': "...",           # Written by reporter_agent
}
```

### 4. Prompt Instructions (Data Reading)

Each agent's prompt tells it **where to read** the previous agent's output:

**Analyzer Prompt:**
```python
"""
Access the scanned prompts from session.state['scanned_prompts'].
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                    Reads scanner's output
"""
```

**Reporter Prompt:**
```python
"""
Access the vulnerability findings from session.state['vulnerability_findings'].
                                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                           Reads analyzer's output
"""
```

## Data Flow Diagram

```
User Message: "Scan ./my_first_agent for vulnerabilities"
    ↓
┌─────────────────────────────────────────────────────────────────┐
│  SequentialAgent (prompt_security_agent)                        │
│  - Creates shared session                                       │
│  - Executes subagents in order                                  │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│  Step 1: scanner_agent                                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 1. Receives user message                                 │  │
│  │ 2. Calls scan_directory("./my_first_agent")             │  │
│  │ 3. Calls extract_prompts_from_file() for each file      │  │
│  │ 4. Collects all prompts                                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                         ↓                                       │
│  session.state['scanned_prompts'] = [                          │
│      {text: "...", file: "...", line_number: 7},              │
│      {text: "...", file: "...", line_number: 15},             │
│      ...                                                        │
│  ]                                                              │
└─────────────────────────────────────────────────────────────────┘
    ↓ HANDOFF via session.state
    ↓
┌─────────────────────────────────────────────────────────────────┐
│  Step 2: analyzer_agent                                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 1. Reads session.state['scanned_prompts']  ← READS      │  │
│  │ 2. For each prompt:                                      │  │
│  │    - Calls check_vulnerability_patterns()                │  │
│  │    - Applies LLM analysis                                │  │
│  │ 3. Compiles vulnerability findings                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                         ↓                                       │
│  session.state['vulnerability_findings'] = [                   │
│      {file: "...", vulnerabilities: [...], severity: "high"}, │
│      {file: "...", vulnerabilities: [...], severity: "low"},  │
│      ...                                                        │
│  ]                                                              │
└─────────────────────────────────────────────────────────────────┘
    ↓ HANDOFF via session.state
    ↓
┌─────────────────────────────────────────────────────────────────┐
│  Step 3: reporter_agent                                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 1. Reads session.state['vulnerability_findings'] ← READS│  │
│  │ 2. Calls generate_security_report()                      │  │
│  │ 3. Enhances with LLM recommendations                     │  │
│  │ 4. Formats final report                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                         ↓                                       │
│  session.state['security_report'] = """                        │
│  =====================================                          │
│  PROMPT SECURITY ANALYSIS REPORT                               │
│  =====================================                          │
│  ...                                                            │
│  """                                                            │
└─────────────────────────────────────────────────────────────────┘
    ↓
Final output returned to user
```

## The Handoff Mechanism - Step by Step

### Step 1 → Step 2 Handoff

1. **Scanner finishes** and stores results:
   ```python
   session.state['scanned_prompts'] = [...]  # Stored via output_key
   ```

2. **SequentialAgent** automatically invokes analyzer_agent

3. **Analyzer reads** scanner's output:
   ```python
   # Analyzer's instruction explicitly tells it:
   "Access the scanned prompts from session.state['scanned_prompts']"
   ```

4. **LLM (analyzer_agent)** knows to:
   - Look in `session.state['scanned_prompts']`
   - Process that data
   - Store new results in `session.state['vulnerability_findings']`

### Step 2 → Step 3 Handoff

Same pattern:

1. **Analyzer finishes** and stores results:
   ```python
   session.state['vulnerability_findings'] = [...]  # Stored via output_key
   ```

2. **SequentialAgent** automatically invokes reporter_agent

3. **Reporter reads** analyzer's output:
   ```python
   # Reporter's instruction explicitly tells it:
   "Access the vulnerability findings from session.state['vulnerability_findings']"
   ```

4. **LLM (reporter_agent)** knows to:
   - Look in `session.state['vulnerability_findings']`
   - Generate report
   - Store final report in `session.state['security_report']`

## Key Design Patterns

### 1. Convention Over Configuration
- Each agent knows what key to write to (`output_key`)
- Each agent is told what key to read from (in `instruction`)

### 2. Stateful Pipeline
- Shared session state acts as a "pipeline buffer"
- Each agent adds to the state, previous data remains accessible

### 3. Explicit Instructions
- Prompts explicitly tell agents where to find input data
- No "magic" - clear instructions for LLM to follow

### 4. Sequential Execution
- No parallelism - each agent completes before next starts
- Ensures data dependencies are satisfied

## Code Example: How to Access Session State

```python
from prompt_security_agent import agent
from google.adk.sessions import Session

session = Session()
result = session.send_message(
    agent=agent,
    message="Scan ./my_first_agent"
)

# Access intermediate results
prompts = session.state.get('scanned_prompts', [])
print(f"Stage 1 (Scanner): Found {len(prompts)} prompts")

findings = session.state.get('vulnerability_findings', [])  
print(f"Stage 2 (Analyzer): Found {len(findings)} issues")

report = session.state.get('security_report', '')
print(f"Stage 3 (Reporter):\n{report}")

# Final output (same as security_report)
print(f"Final result.text:\n{result.text}")
```

## Comparison: Sequential vs Other Patterns

### Sequential (What we use)
```
Agent1 → Agent2 → Agent3
  ↓       ↓       ↓
  A  →    B  →    C   (data flows linearly)
```
**Use when:** Each step depends on the previous step

### Parallel Pattern
```
        ┌→ Agent1 → A
Root → ├→ Agent2 → B
        └→ Agent3 → C
```
**Use when:** Tasks are independent, can run simultaneously

### Loop Pattern  
```
Agent1 → Agent2 → Check → (loop back if needed)
```
**Use when:** Need to iterate until condition is met

## Why This Pattern Works Well

✅ **Clear separation of concerns**: Each agent has one job  
✅ **Testable**: Can test each agent independently  
✅ **Debuggable**: Can inspect session state at each stage  
✅ **Maintainable**: Easy to add/remove/reorder agents  
✅ **Predictable**: Linear flow, no concurrency issues  

## Session State Lifecycle

```
1. User sends message
   → session.state = {}

2. Scanner runs
   → session.state = {scanned_prompts: [...]}

3. Analyzer runs  
   → session.state = {scanned_prompts: [...], vulnerability_findings: [...]}

4. Reporter runs
   → session.state = {scanned_prompts: [...], vulnerability_findings: [...], security_report: "..."}

5. Return to user
   → User receives final output
   → session.state persists for inspection
```

## Summary

The handoff mechanism is elegantly simple:

1. **SequentialAgent** orchestrates execution order
2. **output_key** tells each agent where to write
3. **session.state** is the shared data structure
4. **prompt instructions** tell agents where to read
5. **ADK runtime** handles all the plumbing automatically

No explicit handoff code needed - the framework handles it all through convention and shared state! 🎯

