"""Configuration management for AI Council."""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Any, Optional, List
import yaml
from ai_council.core.models import ExecutionMode, RiskLevel


@dataclass
class LoggingConfig:
    """Configuration for logging system."""
    level: str = "INFO"
    format_json: bool = False
    include_timestamp: bool = True
    include_caller: bool = False


@dataclass
class ModelConfig:
    """Configuration for a single AI model."""
    name: str = ""
    provider: str = ""
    api_key_env: str = ""
    base_url: Optional[str] = None
    max_retries: int = 3
    timeout_seconds: float = 30.0
    cost_per_input_token: float = 0.0
    cost_per_output_token: float = 0.0
    max_context_length: int = 4096
    capabilities: List[str] = field(default_factory=list)
    enabled: bool = True


@dataclass
class ExecutionConfig:
    """Configuration for execution behavior."""
    default_mode: ExecutionMode = ExecutionMode.BALANCED
    max_parallel_executions: int = 5
    default_timeout_seconds: float = 60.0
    max_retries: int = 3
    enable_arbitration: bool = True
    enable_synthesis: bool = True
    default_accuracy_requirement: float = 0.8


@dataclass
class CostConfig:
    """Configuration for cost management."""
    max_cost_per_request: float = 10.0
    currency: str = "USD"
    enable_cost_tracking: bool = True
    cost_alert_threshold: float = 5.0


@dataclass
class AICouncilConfig:
    """Main configuration class for AI Council."""
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    execution: ExecutionConfig = field(default_factory=ExecutionConfig)
    cost: CostConfig = field(default_factory=CostConfig)
    models: Dict[str, ModelConfig] = field(default_factory=dict)
    
    # System settings
    debug: bool = False
    environment: str = "production"
    data_dir: str = "./data"
    cache_dir: str = "./cache"
    
    @classmethod
    def from_file(cls, config_path: Path) -> "AICouncilConfig":
        """
        Load configuration from a YAML file.
        
        Args:
            config_path: Path to the configuration file
            
        Returns:
            Loaded configuration instance
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If config file is invalid YAML
            ValueError: If config contains invalid values
        """
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)
        
        return cls.from_dict(config_data or {})
    
    @classmethod
    def from_dict(cls, config_data: Dict[str, Any]) -> "AICouncilConfig":
        """
        Create configuration from a dictionary.
        
        Args:
            config_data: Configuration data as dictionary
            
        Returns:
            Configuration instance
        """
        # Extract and convert nested configurations
        logging_data = config_data.get('logging', {})
        execution_data = config_data.get('execution', {})
        cost_data = config_data.get('cost', {})
        models_data = config_data.get('models', {})
        
        # Convert execution mode if specified
        if 'default_mode' in execution_data:
            mode_str = execution_data['default_mode']
            if isinstance(mode_str, str):
                execution_data['default_mode'] = ExecutionMode(mode_str.lower())
        
        # Create model configurations
        models = {}
        for model_name, model_data in models_data.items():
            model_config = ModelConfig(name=model_name, **model_data)
            models[model_name] = model_config
        
        return cls(
            logging=LoggingConfig(**logging_data),
            execution=ExecutionConfig(**execution_data),
            cost=CostConfig(**cost_data),
            models=models,
            debug=config_data.get('debug', False),
            environment=config_data.get('environment', 'production'),
            data_dir=config_data.get('data_dir', './data'),
            cache_dir=config_data.get('cache_dir', './cache'),
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        
        Returns:
            Configuration as dictionary
        """
        return {
            'logging': {
                'level': self.logging.level,
                'format_json': self.logging.format_json,
                'include_timestamp': self.logging.include_timestamp,
                'include_caller': self.logging.include_caller,
            },
            'execution': {
                'default_mode': self.execution.default_mode.value,
                'max_parallel_executions': self.execution.max_parallel_executions,
                'default_timeout_seconds': self.execution.default_timeout_seconds,
                'max_retries': self.execution.max_retries,
                'enable_arbitration': self.execution.enable_arbitration,
                'enable_synthesis': self.execution.enable_synthesis,
                'default_accuracy_requirement': self.execution.default_accuracy_requirement,
            },
            'cost': {
                'max_cost_per_request': self.cost.max_cost_per_request,
                'currency': self.cost.currency,
                'enable_cost_tracking': self.cost.enable_cost_tracking,
                'cost_alert_threshold': self.cost.cost_alert_threshold,
            },
            'models': {
                name: {
                    'provider': config.provider,
                    'api_key_env': config.api_key_env,
                    'base_url': config.base_url,
                    'max_retries': config.max_retries,
                    'timeout_seconds': config.timeout_seconds,
                    'cost_per_input_token': config.cost_per_input_token,
                    'cost_per_output_token': config.cost_per_output_token,
                    'max_context_length': config.max_context_length,
                    'capabilities': config.capabilities,
                    'enabled': config.enabled,
                }
                for name, config in self.models.items()
            },
            'debug': self.debug,
            'environment': self.environment,
            'data_dir': self.data_dir,
            'cache_dir': self.cache_dir,
        }
    
    def save_to_file(self, config_path: Path) -> None:
        """
        Save configuration to a YAML file.
        
        Args:
            config_path: Path where to save the configuration
        """
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False, indent=2)
    
    def get_model_config(self, model_name: str) -> Optional[ModelConfig]:
        """
        Get configuration for a specific model.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Model configuration if found, None otherwise
        """
        return self.models.get(model_name)
    
    def validate(self) -> None:
        """
        Validate the configuration for consistency and completeness.
        
        Raises:
            ValueError: If configuration is invalid
        """
        # Validate execution config
        if self.execution.max_parallel_executions <= 0:
            raise ValueError("max_parallel_executions must be positive")
        
        if self.execution.default_timeout_seconds <= 0:
            raise ValueError("default_timeout_seconds must be positive")
        
        if not (0.0 <= self.execution.default_accuracy_requirement <= 1.0):
            raise ValueError("default_accuracy_requirement must be between 0.0 and 1.0")
        
        # Validate cost config
        if self.cost.max_cost_per_request <= 0:
            raise ValueError("max_cost_per_request must be positive")
        
        # Validate model configs
        for model_name, model_config in self.models.items():
            if not model_config.name:
                model_config.name = model_name
            
            if model_config.cost_per_input_token < 0:
                raise ValueError(f"Model {model_name}: cost_per_input_token cannot be negative")
            
            if model_config.cost_per_output_token < 0:
                raise ValueError(f"Model {model_name}: cost_per_output_token cannot be negative")
            
            if model_config.max_context_length <= 0:
                raise ValueError(f"Model {model_name}: max_context_length must be positive")


def load_config(config_path: Optional[Path] = None) -> AICouncilConfig:
    """
    Load configuration from file or environment variables.
    
    Args:
        config_path: Optional path to configuration file
        
    Returns:
        Loaded configuration
    """
    # Default config paths to try
    default_paths = [
        Path("ai_council_config.yaml"),
        Path("config/ai_council.yaml"),
        Path.home() / ".ai_council" / "config.yaml",
    ]
    
    if config_path:
        default_paths.insert(0, config_path)
    
    # Try to load from file
    for path in default_paths:
        if path.exists():
            config = AICouncilConfig.from_file(path)
            config.validate()
            return config
    
    # Fall back to default configuration
    config = AICouncilConfig()
    
    # Override with environment variables if present
    if os.getenv('AI_COUNCIL_DEBUG'):
        config.debug = os.getenv('AI_COUNCIL_DEBUG', '').lower() in ('true', '1', 'yes')
    
    if os.getenv('AI_COUNCIL_ENVIRONMENT'):
        config.environment = os.getenv('AI_COUNCIL_ENVIRONMENT', 'production')
    
    if os.getenv('AI_COUNCIL_LOG_LEVEL'):
        config.logging.level = os.getenv('AI_COUNCIL_LOG_LEVEL', 'INFO')
    
    config.validate()
    return config


def create_default_config() -> AICouncilConfig:
    """
    Create a default configuration with sample model configurations.
    
    Returns:
        Default configuration instance
    """
    config = AICouncilConfig()
    
    # Add sample model configurations
    config.models = {
        "gpt-4": ModelConfig(
            name="gpt-4",
            provider="openai",
            api_key_env="OPENAI_API_KEY",
            cost_per_input_token=0.00003,
            cost_per_output_token=0.00006,
            max_context_length=8192,
            capabilities=["reasoning", "code_generation", "creative_output"],
        ),
        "claude-3": ModelConfig(
            name="claude-3",
            provider="anthropic",
            api_key_env="ANTHROPIC_API_KEY",
            cost_per_input_token=0.000015,
            cost_per_output_token=0.000075,
            max_context_length=200000,
            capabilities=["reasoning", "research", "fact_checking"],
        ),
    }
    
    return config