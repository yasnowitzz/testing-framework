"""
Configuration management for the testing framework
"""
import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv


class Config:
    """Configuration manager for the testing framework"""
    
    def __init__(self, env: str = "dev"):
        self.env = env
        self.config_dir = Path(__file__).parent.parent.parent / "config"
        
        # Load environment variables
        load_dotenv()
        
        # Load configuration
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from files and environment variables"""
        # Load base config
        self.config = self._load_yaml_config("base.yaml")
        
        # Override with environment variables
        self._override_with_env_vars()
    
    def _load_yaml_config(self, filename: str) -> Dict[str, Any]:
        """Load YAML configuration file"""
        config_file = self.config_dir / filename
        if config_file.exists():
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        return {}
    
    def _override_with_env_vars(self) -> None:
        """Override configuration with environment variables"""
        # API Ninjas Configuration
        if os.getenv("API_NINJAS_KEY"):
            if "api" not in self.config:
                self.config["api"] = {}
            if "api_ninjas" not in self.config["api"]:
                self.config["api"]["api_ninjas"] = {}
            self.config["api"]["api_ninjas"]["api_key"] = os.getenv("API_NINJAS_KEY")
        
        # Allure Configuration
        if os.getenv("ALLURE_RESULTS_DIR"):
            if "allure" not in self.config:
                self.config["allure"] = {}
            self.config["allure"]["results_dir"] = os.getenv("ALLURE_RESULTS_DIR")
        
        if os.getenv("ALLURE_REPORT_DIR"):
            if "allure" not in self.config:
                self.config["allure"] = {}
            self.config["allure"]["report_dir"] = os.getenv("ALLURE_REPORT_DIR")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (supports dot notation)"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def get_api_config(self, service_name: str) -> tuple[str, Optional[str]]:
        """Get API base URL and key for specified service"""
        base_url = self.get(f"api.{service_name}.base_url")
        api_key = self.get(f"api.{service_name}.api_key")
        
        # Default URLs for common services
        if not base_url:
            defaults = {
                "api_ninjas": "https://api.api-ninjas.com",
                "jsonplaceholder": "https://jsonplaceholder.typicode.com",
                "reqres": "https://reqres.in"
            }
            base_url = defaults.get(service_name)
        
        return base_url, api_key

