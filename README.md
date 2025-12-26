# AI Council

A production-grade multi-agent orchestration system for coordinating AI models to solve complex problems.

## Overview

AI Council is a Python-based system that intelligently coordinates multiple specialized AI models as a unified decision-making entity. Unlike simple API wrappers, AI Council treats AI models as specialized agents with distinct strengths and weaknesses, ensuring no single model is blindly trusted for all tasks.

## Features

- **Intelligent Task Decomposition**: Automatically breaks complex problems into manageable subtasks
- **Smart Model Routing**: Routes tasks to the most appropriate AI models based on capabilities and requirements
- **Conflict Resolution**: Arbitrates between conflicting outputs from different models
- **Cost Optimization**: Balances cost, speed, and quality based on execution mode
- **Structured Self-Assessment**: Models provide confidence scores and metadata about their responses
- **Graceful Failure Handling**: Robust error handling and fallback mechanisms
- **Extensible Architecture**: Clean separation of concerns for easy maintenance and extension

## Architecture

The system follows a layered architecture with five main components:

1. **Analysis Layer**: Intent analysis and task decomposition
2. **Routing Layer**: Model selection and execution planning
3. **Execution Layer**: Model interface and response collection
4. **Arbitration Layer**: Conflict detection and resolution
5. **Synthesis Layer**: Final output generation and formatting

## Installation

```bash
# Install from source
git clone https://github.com/ai-council/ai-council.git
cd ai-council
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

## Quick Start

```python
from ai_council import AICouncil
from ai_council.core.models import ExecutionMode

# Initialize the system
council = AICouncil()

# Process a complex request
response = council.process(
    "Analyze the pros and cons of renewable energy adoption",
    execution_mode=ExecutionMode.BALANCED
)

print(response.content)
print(f"Confidence: {response.overall_confidence}")
print(f"Models used: {response.models_used}")
```

## Configuration

Create a `ai_council_config.yaml` file:

```yaml
execution:
  default_mode: balanced
  max_parallel_executions: 5
  enable_arbitration: true

models:
  gpt-4:
    provider: openai
    api_key_env: OPENAI_API_KEY
    capabilities: [reasoning, code_generation]
  
  claude-3:
    provider: anthropic
    api_key_env: ANTHROPIC_API_KEY
    capabilities: [research, fact_checking]

cost:
  max_cost_per_request: 10.0
  enable_cost_tracking: true
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run property-based tests
pytest -m property

# Format code
black ai_council tests
isort ai_council tests

# Type checking
mypy ai_council
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please read CONTRIBUTING.md for guidelines.