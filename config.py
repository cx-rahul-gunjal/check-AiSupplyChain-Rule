"""
Configuration module for AI-BOM-POC application.
Handles environment variables, model configurations, and API keys.
"""

import os
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


# ====================
# Enums
# ====================

class ModelProvider(Enum):
    """Supported model providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    AZURE = "azure"
    LOCAL = "local"


class EnvironmentType(Enum):
    """Environment types."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


# ====================
# Configuration Classes
# ====================

@dataclass
class ModelConfig:
    """Configuration for an AI model."""
    name: str
    provider: ModelProvider
    api_key: Optional[str] = None
    endpoint: Optional[str] = None
    model_id: str = ""
    temperature: float = 0.7
    max_tokens: int = 2000
    timeout: int = 30


@dataclass
class MCPServerConfig:
    """Configuration for MCP servers."""
    name: str
    command: str
    args: List[str]
    env: Optional[Dict[str, str]] = None
    timeout: int = 30


@dataclass
class APIConfig:
    """Configuration for external APIs."""
    name: str
    base_url: str
    api_key: Optional[str] = None
    headers: Optional[Dict[str, str]] = None
    timeout: int = 10
    retry_count: int = 3


# ====================
# Main Configuration Class
# ====================

class Config:
    """Main configuration class for the application."""
    
    def __init__(self):
        self.environment = self._get_environment()
        self.debug = self._get_debug()
        self.log_level = self._get_log_level()
        
        # Model configurations
        self.models = self._initialize_models()
        
        # MCP configurations
        self.mcp_servers = self._initialize_mcp_servers()
        
        # API configurations
        self.apis = self._initialize_apis()
        
        # Feature flags
        self.features = self._initialize_features()
    
    @staticmethod
    def _get_environment() -> EnvironmentType:
        """Get environment from ENV variable."""
        env = os.getenv("ENV", "development").lower()
        try:
            return EnvironmentType[env.upper()]
        except KeyError:
            return EnvironmentType.DEVELOPMENT
    
    @staticmethod
    def _get_debug() -> bool:
        """Get debug flag from ENV variable."""
        return os.getenv("DEBUG", "false").lower() == "true"
    
    @staticmethod
    def _get_log_level() -> str:
        """Get log level from ENV variable."""
        return os.getenv("LOG_LEVEL", "INFO").upper()
    
    def _initialize_models(self) -> Dict[str, ModelConfig]:
        """Initialize model configurations."""
        return {
            "gpt4": ModelConfig(
                name="GPT-4",
                provider=ModelProvider.OPENAI,
                api_key=os.getenv("OPENAI_API_KEY"),
                model_id="gpt-4",
                temperature=0.7,
                max_tokens=2000
            ),
            "gpt35": ModelConfig(
                name="GPT-3.5-Turbo",
                provider=ModelProvider.OPENAI,
                api_key=os.getenv("OPENAI_API_KEY"),
                model_id="gpt-3.5-turbo",
                temperature=0.7,
                max_tokens=1000
            ),
            "claude3": ModelConfig(
                name="Claude 3",
                provider=ModelProvider.ANTHROPIC,
                api_key=os.getenv("ANTHROPIC_API_KEY"),
                model_id="claude-3-opus-20240229",
                temperature=0.7,
                max_tokens=2000
            ),
            "azure_gpt4": ModelConfig(
                name="Azure GPT-4",
                provider=ModelProvider.AZURE,
                api_key=os.getenv("AZURE_OPENAI_KEY"),
                endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                model_id="gpt-4-deployment",
                temperature=0.7,
                max_tokens=2000
            )
        }
    
    def _initialize_mcp_servers(self) -> Dict[str, MCPServerConfig]:
        """Initialize MCP server configurations."""
        return {
            "default": MCPServerConfig(
                name="AI-BOM-POC-Server",
                command="python",
                args=["-m", "mcp_server"],
                timeout=30
            ),
            "weather": MCPServerConfig(
                name="Weather-Service",
                command="python",
                args=["-m", "mcp_server"],
                env={"SERVICE_TYPE": "weather"},
                timeout=30
            ),
            "data": MCPServerConfig(
                name="Data-Service",
                command="python",
                args=["-m", "mcp_server"],
                env={"SERVICE_TYPE": "data"},
                timeout=30
            ),
            "search": MCPServerConfig(
                name="Search-Service",
                command="python",
                args=["-m", "mcp_server"],
                env={"SERVICE_TYPE": "search"},
                timeout=30
            )
        }
    
    def _initialize_apis(self) -> Dict[str, APIConfig]:
        """Initialize external API configurations."""
        return {
            "weather_api": APIConfig(
                name="WeatherAPI",
                base_url="https://api.weatherapi.com/v1",
                api_key=os.getenv("WEATHER_API_KEY"),
                timeout=10
            ),
            "openweather_api": APIConfig(
                name="OpenWeatherMap",
                base_url="https://api.openweathermap.org/data/2.5",
                api_key=os.getenv("OPENWEATHER_API_KEY"),
                timeout=10
            ),
            "github_api": APIConfig(
                name="GitHub API",
                base_url="https://api.github.com",
                api_key=os.getenv("GITHUB_TOKEN"),
                headers={"Accept": "application/vnd.github.v3+json"},
                timeout=10
            )
        }
    
    def _initialize_features(self) -> Dict[str, bool]:
        """Initialize feature flags."""
        return {
            "langchain_agents": os.getenv("ENABLE_LANGCHAIN_AGENTS", "true").lower() == "true",
            "crewai_agents": os.getenv("ENABLE_CREWAI_AGENTS", "true").lower() == "true",
            "pydantic_agents": os.getenv("ENABLE_PYDANTIC_AGENTS", "true").lower() == "true",
            "mcp_client": os.getenv("ENABLE_MCP_CLIENT", "true").lower() == "true",
            "mcp_server": os.getenv("ENABLE_MCP_SERVER", "true").lower() == "true",
            "parallel_execution": os.getenv("ENABLE_PARALLEL_EXECUTION", "true").lower() == "true",
            "caching": os.getenv("ENABLE_CACHING", "false").lower() == "true",
            "monitoring": os.getenv("ENABLE_MONITORING", "true").lower() == "true"
        }
    
    def get_model(self, model_name: str) -> Optional[ModelConfig]:
        """Get a specific model configuration."""
        return self.models.get(model_name)
    
    def get_mcp_server(self, server_name: str) -> Optional[MCPServerConfig]:
        """Get a specific MCP server configuration."""
        return self.mcp_servers.get(server_name)
    
    def get_api(self, api_name: str) -> Optional[APIConfig]:
        """Get a specific API configuration."""
        return self.apis.get(api_name)
    
    def is_feature_enabled(self, feature_name: str) -> bool:
        """Check if a feature is enabled."""
        return self.features.get(feature_name, False)
    
    def get_summary(self) -> Dict:
        """Get configuration summary."""
        return {
            "environment": self.environment.value,
            "debug": self.debug,
            "log_level": self.log_level,
            "models": list(self.models.keys()),
            "mcp_servers": list(self.mcp_servers.keys()),
            "apis": list(self.apis.keys()),
            "features_enabled": [k for k, v in self.features.items() if v],
            "features_disabled": [k for k, v in self.features.items() if not v]
        }


# ====================
# Logger Configuration
# ====================

class LoggerConfig:
    """Configuration for logging."""
    
    @staticmethod
    def get_logger_config(log_level: str = "INFO", debug: bool = False) -> Dict:
        """Get logging configuration."""
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
                },
                "detailed": {
                    "format": "%(asctime)s [%(levelname)s] %(name)s - %(filename)s:%(lineno)d - %(funcName)s(): %(message)s"
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": log_level,
                    "formatter": "detailed" if debug else "standard",
                    "stream": "ext://sys.stdout"
                },
                "file": {
                    "class": "logging.FileHandler",
                    "level": log_level,
                    "formatter": "detailed",
                    "filename": "ai_bom_poc.log"
                }
            },
            "root": {
                "level": log_level,
                "handlers": ["console", "file"]
            }
        }


# ====================
# Singleton Instance
# ====================

_config_instance: Optional[Config] = None


def get_config() -> Config:
    """Get or create the global configuration instance."""
    global _config_instance
    
    if _config_instance is None:
        _config_instance = Config()
    
    return _config_instance


def reset_config():
    """Reset the configuration instance (useful for testing)."""
    global _config_instance
    _config_instance = None


# ====================
# Default Values
# ====================

DEFAULT_CONFIG = {
    "TIMEOUT": 30,
    "RETRY_COUNT": 3,
    "BATCH_SIZE": 10,
    "MAX_WORKERS": 4,
    "CACHE_TTL": 300,
    "LOG_LEVEL": "INFO",
    "ENV": "development",
    "DEBUG": False
}


# ====================
# Configuration Validation
# ====================

class ConfigValidator:
    """Validates configuration."""
    
    @staticmethod
    def validate_model_config(config: ModelConfig) -> bool:
        """Validate model configuration."""
        if not config.name:
            return False
        if not config.provider:
            return False
        if config.temperature < 0 or config.temperature > 2:
            return False
        if config.max_tokens < 1:
            return False
        return True
    
    @staticmethod
    def validate_api_config(config: APIConfig) -> bool:
        """Validate API configuration."""
        if not config.name:
            return False
        if not config.base_url:
            return False
        if config.timeout < 1:
            return False
        return True
    
    @staticmethod
    def validate_mcp_config(config: MCPServerConfig) -> bool:
        """Validate MCP server configuration."""
        if not config.name:
            return False
        if not config.command:
            return False
        if not config.args:
            return False
        return True


# Example usage for demonstration
if __name__ == "__main__":
    config = get_config()
    
    print("\n=== Configuration Summary ===")
    import json
    print(json.dumps(config.get_summary(), indent=2))
    
    print("\n=== Available Models ===")
    for model_name, model_config in config.models.items():
        print(f"  {model_name}: {model_config.name} ({model_config.provider.value})")
    
    print("\n=== Available MCP Servers ===")
    for server_name, server_config in config.mcp_servers.items():
        print(f"  {server_name}: {server_config.name}")
    
    print("\n=== Available APIs ===")
    for api_name, api_config in config.apis.items():
        print(f"  {api_name}: {api_config.name}")
    
    print("\n=== Enabled Features ===")
    for feature, enabled in config.features.items():
        status = "✓" if enabled else "✗"
        print(f"  {status} {feature}")
