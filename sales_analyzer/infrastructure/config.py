import logging
from enum import Enum

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

logger = logging.getLogger(__name__)


class ConfigModelField(str, Enum):
    MODEL_FIELDS = 'model_fields'
    ENV_PREFIX = 'env_prefix'


class AnalyzerConfig(BaseSettings):
    LOSS_MAKING_MARGIN_THRESHOLD: float = Field(
        default=30,
        description='Порог, с которого считаем, что товар немаржинальный'
    )
    BEST_SELLER_QUANTITY_THRESHOLD: int = Field(
        default=100,
        description='Количество, после которого блюдо считается бест селлером и добавляется в рекоммендации',
    )
    model_config = SettingsConfigDict(env_prefix='ANALYZER_CONFIG_')


class Config(BaseSettings):
    PROJECT_NAME: str = Field(default='sales_analyzer')
    ENVIRONMENT: str = Field(default='dev')
    DEBUG: bool = Field(default=False)
    ANALYZER_CONFIG: AnalyzerConfig = Field(default_factory=AnalyzerConfig)


config = Config()
