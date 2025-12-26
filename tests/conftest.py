"""Pytest configuration and fixtures for AI Council tests."""

import pytest
from pathlib import Path
from ai_council.utils.config import AICouncilConfig, create_default_config
from ai_council.core.models import (
    Task, Subtask, SelfAssessment, AgentResponse, FinalResponse,
    TaskType, ExecutionMode, RiskLevel, Priority
)


@pytest.fixture
def sample_config() -> AICouncilConfig:
    """Provide a sample configuration for testing."""
    return create_default_config()


@pytest.fixture
def sample_task() -> Task:
    """Provide a sample task for testing."""
    return Task(
        content="Analyze the benefits of renewable energy",
        execution_mode=ExecutionMode.BALANCED
    )


@pytest.fixture
def sample_subtask() -> Subtask:
    """Provide a sample subtask for testing."""
    return Subtask(
        parent_task_id="task-123",
        content="Research solar energy efficiency",
        task_type=TaskType.RESEARCH,
        priority=Priority.HIGH,
        risk_level=RiskLevel.LOW,
        accuracy_requirement=0.9
    )


@pytest.fixture
def sample_self_assessment() -> SelfAssessment:
    """Provide a sample self-assessment for testing."""
    return SelfAssessment(
        confidence_score=0.85,
        assumptions=["Current market data is accurate"],
        risk_level=RiskLevel.LOW,
        estimated_cost=0.05,
        token_usage=150,
        execution_time=2.5,
        model_used="gpt-4"
    )


@pytest.fixture
def sample_agent_response(sample_self_assessment: SelfAssessment) -> AgentResponse:
    """Provide a sample agent response for testing."""
    return AgentResponse(
        subtask_id="subtask-456",
        model_used="gpt-4",
        content="Solar energy efficiency has improved significantly...",
        self_assessment=sample_self_assessment,
        success=True
    )


@pytest.fixture
def sample_final_response() -> FinalResponse:
    """Provide a sample final response for testing."""
    return FinalResponse(
        content="Renewable energy offers multiple benefits including...",
        overall_confidence=0.88,
        models_used=["gpt-4", "claude-3"],
        success=True
    )


@pytest.fixture
def temp_config_file(tmp_path: Path) -> Path:
    """Provide a temporary configuration file for testing."""
    config_file = tmp_path / "test_config.yaml"
    config = create_default_config()
    config.save_to_file(config_file)
    return config_file