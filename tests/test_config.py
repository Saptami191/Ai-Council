"""Tests for configuration management."""

import pytest
import tempfile
from pathlib import Path
from ai_council.utils.config import (
    AICouncilConfig, ModelConfig, LoggingConfig, ExecutionConfig, CostConfig,
    load_config, create_default_config
)
from ai_council.core.models import ExecutionMode


class TestModelConfig:
    """Test ModelConfig data model."""
    
    def test_model_config_creation(self):
        """Test basic model config creation."""
        config = ModelConfig(
            name="gpt-4",
            provider="openai",
            api_key_env="OPENAI_API_KEY",
            cost_per_input_token=0.00003,
            cost_per_output_token=0.00006,
            max_context_length=8192
        )
        assert config.name == "gpt-4"
        assert config.provider == "openai"
        assert config.cost_per_input_token == 0.00003
        assert config.enabled is True


class TestAICouncilConfig:
    """Test AICouncilConfig main configuration class."""
    
    def test_config_creation(self):
        """Test basic config creation."""
        config = AICouncilConfig()
        assert config.logging.level == "INFO"
        assert config.execution.default_mode == ExecutionMode.BALANCED
        assert config.cost.max_cost_per_request == 10.0
        assert config.debug is False
    
    def test_config_validation(self):
        """Test config validation."""
        config = AICouncilConfig()
        config.execution.max_parallel_executions = -1
        
        with pytest.raises(ValueError, match="max_parallel_executions must be positive"):
            config.validate()
    
    def test_config_from_dict(self):
        """Test creating config from dictionary."""
        config_data = {
            "logging": {"level": "DEBUG"},
            "execution": {"default_mode": "fast", "max_parallel_executions": 10},
            "cost": {"max_cost_per_request": 20.0},
            "models": {
                "test-model": {
                    "provider": "test",
                    "api_key_env": "TEST_KEY",
                    "cost_per_input_token": 0.001
                }
            },
            "debug": True
        }
        
        config = AICouncilConfig.from_dict(config_data)
        assert config.logging.level == "DEBUG"
        assert config.execution.default_mode == ExecutionMode.FAST
        assert config.execution.max_parallel_executions == 10
        assert config.cost.max_cost_per_request == 20.0
        assert config.debug is True
        assert "test-model" in config.models
        assert config.models["test-model"].provider == "test"
    
    def test_config_to_dict(self):
        """Test converting config to dictionary."""
        config = create_default_config()
        config_dict = config.to_dict()
        
        assert "logging" in config_dict
        assert "execution" in config_dict
        assert "cost" in config_dict
        assert "models" in config_dict
        assert config_dict["execution"]["default_mode"] == "balanced"
    
    def test_config_file_operations(self):
        """Test saving and loading config from file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "test_config.yaml"
            
            # Create and save config
            original_config = create_default_config()
            original_config.debug = True
            original_config.save_to_file(config_path)
            
            # Load config from file
            loaded_config = AICouncilConfig.from_file(config_path)
            
            assert loaded_config.debug is True
            assert len(loaded_config.models) == len(original_config.models)
    
    def test_get_model_config(self):
        """Test getting model configuration."""
        config = create_default_config()
        
        gpt4_config = config.get_model_config("gpt-4")
        assert gpt4_config is not None
        assert gpt4_config.name == "gpt-4"
        
        nonexistent_config = config.get_model_config("nonexistent")
        assert nonexistent_config is None


class TestConfigLoading:
    """Test configuration loading functions."""
    
    def test_create_default_config(self):
        """Test creating default configuration."""
        config = create_default_config()
        
        assert isinstance(config, AICouncilConfig)
        assert len(config.models) >= 2  # Should have at least gpt-4 and claude-3
        assert "gpt-4" in config.models
        assert "claude-3" in config.models
    
    def test_load_config_default(self):
        """Test loading config with defaults."""
        config = load_config()
        
        assert isinstance(config, AICouncilConfig)
        assert config.logging.level == "INFO"
        assert config.execution.default_mode == ExecutionMode.BALANCED
    
    def test_load_config_from_file(self):
        """Test loading config from specific file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "custom_config.yaml"
            
            # Create a custom config file
            custom_config = create_default_config()
            custom_config.debug = True
            custom_config.logging.level = "DEBUG"
            custom_config.save_to_file(config_path)
            
            # Load the custom config
            loaded_config = load_config(config_path)
            
            assert loaded_config.debug is True
            assert loaded_config.logging.level == "DEBUG"