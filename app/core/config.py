import yaml
from functools import lru_cache
from app.config.base import BaseConfig
from app.utils.profile import Profile


@lru_cache()
def get_config(config_file="config.yaml", env=None) -> BaseConfig:
    """
    获取对应的环境变量
    :param config_file: 配置文件路径，默认为 "config.yaml"
    :param env: 环境变量，默认为 None，如果为 None 则根据 config.yaml 中的 env 字段获取
    :return: 不同环境对应的配置类对象
    """
    project_root = Profile.get_project_root()                   # 先获取项目根目录
    # 根据项目根目录去拼接到 "config.yaml" 文件在计算机上的绝对路径
    config_path = project_root.joinpath(config_file)            # 获取 config 文件路径
    with open(config_path, "r", encoding="utf-8") as f:         # 读取 yaml 配置文件
        yaml_config = yaml.safe_load(f)
    if env:                                                     # 根据环境是 dev 还是 prod，如果是非空的话
        yaml_config["env"] = env                                # 如果传进来的是 prod，则赋值给 yaml_config["env"]
    else:
        env = yaml_config.get("env", "dev")                     # 如若是空的话则设置其指定默认值为 "dev"
    # 根据环境获取对应的配置，此时要获取的是一个字典值(无论是 dev 下的字典的值 还是 prod 下面字典的值，它会把这些值封装成一个 Python 字典)
    env_config = yaml_config.get(env, {})
    # 返回对应的配置类实例，把获取到对应字典的值通过解包的方式传递到 base.py 各个变量上去
    return BaseConfig(**env_config)
