import os
import pytest
import yaml
from app.core.config import get_config
from app.utils.profile import Profile

@pytest.fixture(autouse=True)
def clear_config_cache():
    """
    清除配置缓存 自动应用于每个测试
    """
    get_config.cache_clear()
    yield
    get_config.cache_clear()


@pytest.fixture
def fake_config_file():
    """
    创建一个基于实际配置文件的测试配置--尽量不去影响到或者使用真实的 "config.yaml" 文件，所以需要创建一个假的 "config.yaml" 文件
    """
    # 首先需要去读取实际的配置文件，拿到项目的根目录
    project_dir = Profile.get_project_root()
    # real_config_path = project_dir / "config.yaml"            # macOS 系统
    real_config_path = project_dir.joinpath("config.yaml")      # Windows系统
    # 再检查文件是否存在
    if not os.path.exists(real_config_path):                    # 如果当前路径不存在则去创建
        raise FileNotFoundError("File not found: config.yaml")
    with open(real_config_path, "r", encoding="utf-8") as f:    # 如果有的话，打开文件
        config_data = yaml.safe_load(f)         # 从文件对象中安全地加载 YAML 格式数据，并将其转换为 Python 原生数据结构
    # 去掉 env 变量，因为不需要，只需要测试 dev/prod 里面的值
    config_data.pop("env")
    # 创建测试专用的配置（可以基于实际配置修改某些值）--获取文件里面的值，其实就是拷贝一份
    test_config = config_data.copy()
    # mock一些测试特定的值
    if "dev" in test_config:
        test_config["dev"]["app"]["name"] = "Student Information Management System(dev)"
        test_config["dev"]["app"]["port"] = 8000
        test_config["dev"]["app"]["reload"] = True
        test_config["dev"]["db"]["host"] = "localhost"
        test_config["dev"]["db"]["database"] = "dev-db"
    if "prod" in test_config:
        test_config["prod"]["app"]["name"] = "Student Information Management System(prod)"
        test_config["prod"]["app"]["port"] = 8001
        test_config["prod"]["app"]["reload"] = False
        test_config["prod"]["db"]["host"] = "prod-host"
        test_config["prod"]["db"]["database"] = "prod-db"
    # 写入临时配置文件, file_name 为测试专用--"fake_config.yaml"文件需要加入到 gitignore ，因为不需要此文件上传到代码仓库
    file_name = "fake_config.yaml"          # 会在跟 "config.yaml" 文件同一层级的地方创建一个 "fake_config.yaml" 文件
    config_file = project_dir / file_name
    with open(config_file, "w", encoding="utf-8") as f:         # 写入文件
        yaml.dump(test_config, f)
    return file_name


class TestConfig:
    def test_dev_config(self, fake_config_file):            # fake_config_file 的值其实就是返回的 file_name
        """
        测试开发环境配置
        """
        config = get_config(fake_config_file, "dev")
        assert config.app.name == "Student Information Management System(dev)"
        assert config.app.port == 8000
        assert config.app.reload is True
        assert config.db.host == "localhost"
        assert config.db.database == "dev-db"

    def test_prod_config(self, fake_config_file):
        """
        测试生产环境配置
        """
        config = get_config(fake_config_file, "prod")
        assert config.app.name == "Student Information Management System(prod)"
        assert config.app.port == 8001
        assert config.app.reload is False
        assert config.db.host == "prod-host"
        assert config.db.database == "prod-db"

    def test_get_config_caching(self, fake_config_file):
        """
        测试get_config的缓存功能
        """
        # 连续调用两次get_config
        config1 = get_config(fake_config_file)
        config2 = get_config(fake_config_file)
        # 验证返回的是同一个对象
        assert config1 is config2

    def test_get_real_config_dev(self):
        """
        测试获取真实配置dev文件
        """
        # 调用get_config函数获取真实配置
        config = get_config()
        # 简单验证配置对象是否存在
        assert config is not None
        # 配置信息key对应的value
        assert config.app.name == "Student Information Management System"
        assert config.app.port == 8000
        assert config.app.reload is True
        assert config.db.host == "localhost"

    def test_get_real_config_prod(self):
        """
        测试获取真实配置prod文件
        """
        # 调用get_config函数获取真实配置 prod
        config = get_config(env="prod")
        # 简单验证配置对象是否存在
        assert config is not None
        # 配置信息key对应的value
        assert config.app.name == "Student Information Management System(prod)"
        assert config.app.port == 9999
        assert config.app.reload is False
        assert config.db.host == "localhost"
