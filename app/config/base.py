from pydantic_settings import BaseSettings
from pydantic import SecretStr


class AppConfig(BaseSettings):
    """
    FastAPI的应用配置
    """
    name: str               # 应用名称
    description: str        # 应用描述
    api: str                # 应用接口
    host: str               # 应用主机地址
    port: int               # 应用端口
    uvicorn: str            # uvicorn应用入口
    version: str            # 应用版本
    reload: bool            # 是否自动重载应用


class DatabaseConfig(BaseSettings):
    """
    PostgreSQL配置
    """
    host: str                   # 数据库主机地址
    port: int                   # 数据库端口
    username: str               # 数据库用户名
    password: SecretStr         # 数据库密码
    database: str               # 数据库名称
    driver_name: str            # 数据库连接配置
    echo: bool                  # 是否开启sqlalchemy日志
    max_overflow: int           # 允许溢出连接池大小的最大连接数
    pool_size: int              # 连接池大小，0表示连接数无限制
    pool_recycle: int           # 连接回收时间（单位：秒）
    pool_timeout: int           # 连接池中没有线程可用时，最多等待的时间（单位：秒）


class RedisConfig(BaseSettings):
    """
    Redis配置
    """
    host: str               # Redis主机地址
    port: int               # Redis端口
    username: str           # Redis用户名
    password: SecretStr     # Redis密码
    db: int                 # Redis数据库索引


class BaseConfig(BaseSettings):
    """
    基础配置所有环境通用的配置
    """
    app: AppConfig          # 基础/应用配置
    db: DatabaseConfig      # PostgreSQL配置
    redis: RedisConfig      # Redis配置