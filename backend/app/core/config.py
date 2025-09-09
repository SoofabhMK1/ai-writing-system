# backend/app/core/config.py

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # 1. 定义独立的数据库连接参数
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SECRET_KEY: str
    
    # 2. 定义一个属性来动态构建数据库URL
    #    这个属性不会直接从环境变量读取，而是通过其他字段计算得出
    @property
    def DATABASE_URL(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host="db",  # 我们硬编码 'db'，因为这是容器网络中的服务名
                path=self.POSTGRES_DB,
            )
        )

    # 3. 指定 .env 文件作为配置来源
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )


settings = Settings()
