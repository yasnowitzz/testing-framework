import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class ApiConfig:
    base_url: str
    api_key: str | None = None


@dataclass(frozen=True)
class UiConfig:
    base_url: str
    browser: str


@dataclass(frozen=True)
class AllureConfig:
    results_dir: str
    report_dir: str


@dataclass(frozen=True)
class Config:
    api_ninjas: ApiConfig
    allure: AllureConfig

    @staticmethod
    def load() -> "Config":
        api_ninjas = ApiConfig(
            base_url=os.getenv("API_NINJAS_BASE_URL", "https://api.api-ninjas.com"),
            api_key=os.getenv("API_NINJAS_KEY"),
        )
        allure = AllureConfig(
            results_dir=os.getenv("ALLURE_RESULTS_DIR", "reports/allure-results"),
            report_dir=os.getenv("ALLURE_REPORT_DIR", "reports/allure-report"),
        )
        return Config(api_ninjas=api_ninjas, allure=allure)
