"""
Ethical Edge Cognitive GRC Engine - System Configuration
File: config.py
"""
import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Ethical Edge Cognitive GRC"
    VERSION: str = "1.0.0-Alpha"
    API_V1_STR: str = "/api/v1"
    
    # Database Settings matching your db_manager / SessionLocal configurations
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./compliance_ledger.db")
    
    # Active Compliance Frameworks to be processed by run_compliance_checks.py
    ACTIVE_FRAMEWORKS: List[str] = ["UNICEF-CS-2026", "KING-V-SADC", "BDPA-2021"]
    
    # Global Default Safe Thresholds (Fallback if JSON framework fails to load)
    CRITICAL_TEMP_THRESHOLD: float = 40.0
    CRITICAL_FLOOD_METERS: float = 0.5

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
