# 导包引入
from pathlib import Path

# 定义Profile类
class Profile:

    @staticmethod
    def get_project_root() -> Path:
        """
        设置获取项目根目录的一个方法
        :return: 返回的值就是项目根目录
        """
        return Path(__file__).parent.parent.parent