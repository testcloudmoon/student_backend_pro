import sys
from functools import lru_cache
from loguru import logger


class LogHelper:            # 实现日志系统

    def __init__(self):
        self.logger = logger            # 初始化日志记录器
        self.logger.remove()            # 移除所有已有的日志处理器，清空日志设置
        formatter = (                   # 定义日志输出的基本格式
            "<green>{time:YYYYMMDD HH:mm:ss}</green> | "        # 绿色显示时间
            "{process.name} | "                                 # 显示进程名
            "{thread.name} | "                                  # 显示线程名
            "<cyan>{module}</cyan>.<cyan>{function}</cyan>"     # 青色显示模块名和方法名
            ":<cyan>{line}</cyan> | "                           # 青色显示行号
            "<level>{level}</level>: "                          # 显示日志等级
            "<level>{message}</level>",                         # 显示日志内容
        )
        # 这里定义了详细的日志输出格式，包含时间、进程名、线程名、模块名、方法名、行号、日志等级和日志内容
        self.logger.add(                    # 添加日志处理器，将日志输出到控制台
            sys.stdout,                     # sys.stdout 表示标准输出，即控制台
            format=formatter[0],
        )

    @lru_cache
    def get_logger(self):
        # 获取日志记录器实例，使用 lru_cache 缓存结果，避免重复创建，对于整个系统来说，get_logger 调用一次就行
        return self.logger


LogHelpers = LogHelper()                # 创建 LogHelper 类的实例
log = LogHelpers.get_logger()           # 获取日志记录器
